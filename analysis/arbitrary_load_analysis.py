import pandas as pd
import sys
import glob
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import argparse
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer
import cProfile

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="", help="input path where traces are located")
parser.add_argument('--headers', type=str, default="", help="the headers for the CSV")
args = parser.parse_args()

period = [20e-9, 100e-9, 200e-9, 1e-6, 2e-6, 10e-6, 20e-6, 100e-6]
slew_rate = list(np.arange(0.01, 0.3, 0.05))
amplitude = range(5, 95, 5)
duration=500e-6
timestep=1e-9
min_power = 5

"""3D Plots"""
# Slew Rate for different combinations of period, input_slew, and amplitude
max_supply_slew_rate_p = np.zeros((len(period), len(amplitude), len(slew_rate)))
max_supply_slew_rate_n = np.zeros((len(period), len(amplitude), len(slew_rate)))
supply_stabilization = np.zeros((len(period), len(amplitude), len(slew_rate)))
supply_cpp = np.zeros((len(period), len(amplitude), len(slew_rate)))
supply_v_droop = np.zeros((len(period), len(amplitude), len(slew_rate)))
supply_v_droop_len = np.zeros((len(period), len(amplitude), len(slew_rate)))
supply_phase_delay_rising = np.zeros((len(period), len(amplitude), len(slew_rate)))
supply_phase_delay_falling = np.zeros((len(period), len(amplitude), len(slew_rate)))

def get_files(path):
  return glob.glob(path+"/trace_*.csv")

def import_csv(file, headers):
  return pd.read_csv(file, header=None, names=headers)

def valid_combinations(files):
  keys = []
  for i in files:
    keys.append([int(i) for i in i.split(".")[0].split("/")[-1].split("_")[1:4]])
  return keys

def get_key(file):
  return [int(i) for i in file.split(".")[0].split("/")[-1].split("_")[1:4]]

def gen_sweep_space_scatter(axis_vals):
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter([math.log(i[0],10) for i in axis_vals], [i[1] for i in axis_vals], [i[2] for i in axis_vals], marker='o')
  ax.set_xlabel('log(period) [s]')
  ax.set_ylabel('slew rate [A/ns]')
  ax.set_zlabel('amplitude [A]')
  plt.show()

def keys_to_vals(keys):
  vals = []
  for i in keys:
    vals.append([period[i[0]], amplitude[i[2]], slew_rate[i[1]]])
  return vals

def average_rising_slew(signal, headers, ts, trigger_l, trigger_h, period):
  cmax = []
  flag = False
  ma = 0
  start_time = 100000
  end_time = start_time + int(period*3*1e9)
  prev = start_time - 1
  for i in range(start_time, end_time):
    if(ts[i] > trigger_l and ts[prev] <= trigger_l and not flag):
      flag = True
    if(ts[i] > trigger_h and ts[prev] <= trigger_h and flag):
      flag = False
    if flag:
      cmax.append(signal[i]-signal[prev])
    prev = i
  cmax = sum(cmax)/len(cmax)
  return cmax

def average_falling_slew(signal, headers, ts, trigger_l, trigger_h, period):
  cmin = []
  flag = False
  ma = 0
  start_time = 100000
  end_time = start_time + int(period*3*1e9)
  prev = start_time - 1
  for i in range(start_time, end_time):
    if(ts[i] < trigger_h and ts[prev] >= trigger_h and not flag):
      flag = True
    if(ts[i] < trigger_l and ts[prev] >= trigger_l and flag):
      flag = False
    if flag:
      cmin.append(abs(signal[i]-signal[prev]))
    prev = i
  cmin = sum(cmin)/len(cmin)
  return cmin

def average_phase_delay(time, supply_current, device_current, headers, triggerA, triggerB, period):
  pdr = []
  pdf = []
  start_time = 0
  start_range = 100000
  end_range = start_range + int(period*3*1e9)
  prev = 0
  flag = False
  for i in range(start_range, end_range):
    # Rising Edge
    if(device_current[i] > triggerA and device_current[prev] <= triggerA and not flag):
      start_time = time[i]
      flag = True
    # Falling Edge
    if(device_current[i] < triggerA and device_current[prev] >= triggerA and not flag):
      start_time = time[i]
      flag = True
    # Rising Edge
    if(supply_current[i] > triggerB and supply_current[prev] <= triggerB and flag):
      pdr.append(time[i]-start_time)
      flag = False
    # Falling Edge
    if(supply_current[i] < triggerB and supply_current[prev] >= triggerB and flag):
      pdf.append(time[i]-start_time)
      flag = False
    prev = i
  averagef = sum(pdf)/len(pdf)
  averager = sum(pdr)/len(pdr)
  return [averagef,averager]

def p_p(time, signal, headers, ts, trigger, period):
  cmin = []
  cmax = []
  start_time = 0
  prev = 0
  flag = False
  fp = False
  ma = 0
  mi = 100000
  start_time = 100000
  end_time = start_time + int(period*3*1e9)
  prev = start_time - 1
  for i in range(start_time, end_time):
    # Peak
    if(ts[i] > trigger and ts[prev] <= trigger and not flag):
      flag = True
    # Min
    if(ts[i] < trigger and ts[prev] >= trigger and  flag):
      flag = False
    if flag:
      ma = max(signal[i], ma)
      if not fp:
        cmin.append(mi)
        mi = 100000
    if not flag:
      mi = min(signal[i], mi)
      if fp:
        cmax.append(ma)
        ma = 0
    fp = flag
    prev = i
  cmin = sum(cmin)/len(cmin)
  cmax = sum(cmax)/len(cmax)
  return cmax - cmin

def dc_offset(time, signal, headers, ts, trigger, period):
  cmin = []
  cmax = []
  start_time = 0
  prev = 0
  flag = False
  fp = False
  ma = 0
  mi = 100000
  start_time = 100000
  end_time = start_time + int(period*3*1e9)
  prev = start_time - 1
  for i in range(start_time, end_time):
    # Peak
    if(ts[i] > trigger and ts[prev] <= trigger and not flag):
      flag = True
    # Min
    if(ts[i] < trigger and ts[prev] >= trigger and  flag):
      flag = False
    if flag:
      ma = max(signal[i], ma)
      if not fp:
        cmin.append(mi)
        mi = 100000
    if not flag:
      mi = min(signal[i], mi)
      if fp:
        cmax.append(ma)
        ma = 0
    fp = flag
    prev = i
  cmin = sum(cmin)/len(cmin)
  cmax = sum(cmax)/len(cmax)
  return (cmax + cmin)/2

def plot_P_A(x, y, data_vector, super_title):
  """ Plots Period on X axis Amplitude on Y axis """
  fig, axs = plt.subplots(2,3)
  fig.set_size_inches(20,10)
  fig.suptitle(super_title, fontsize=24)
  mi = 10000000
  ma = 0
  for i in range(len(period)):
    for j in range(len(amplitude)):
      for k in range(len(slew_rate)):
        print(data_vector[i,j,k])
        if(data_vector[i,j,k] != 0.0):
          mi = min(data_vector[i,j,k], mi)
  for i in range(len(period)):
    for j in range(len(amplitude)):
      for k in range(len(slew_rate)):
        ma = max(data_vector[i,j,k], ma)
  levels = np.linspace(mi, ma, 100)[1:]
  print(levels)
  for ax, i in zip(axs.ravel(), range(len(slew_rate))):
    print(data_vector[:,:,i].shape)
    print(len(x))
    print(len(y))
    print(data_vector[:,:,i])
    CS = ax.contourf(x, [math.log(i,10) for i in y], data_vector[:,:,i], levels)
    CS.set_clim(levels[0], levels[-1])
    fig.colorbar(CS, ax=ax, shrink=0.9)
    ax.set_title("Load Slew "+"{:.3f}".format(slew_rate[i])+" [A/ns]")
    ax.set_ylabel("log(Period) [s]")
    ax.set_xlabel("Amplitude [A]")
  plt.show()

def plot_time_domain(time, ds, i, name, xtitle, ytitle):
  fig, ax = plt.subplots(1,1)
  fig.set_size_inches(20,7)
  fig.suptitle(name, fontsize=24)
  range_low = 100000
  range_high = range_low + int(period[i]*3*1e9)
  for j in range(len(amplitude)):
    for k in range(len(slew_rate)):
      if ds[i][j][k] != None:
        ax.plot(time[range_low:range_high], ds[i][j][k][range_low:range_high], label=str(amplitude[j])+"_"+"{:.3f}".format(slew_rate[k]))
  ax.set_title("Period "+str(period[i]))
  ax.set_ylabel(ytitle)
  ax.set_xlabel(xtitle)
  plt.legend()
  plt.show()


path=args.input
headers=args.headers

files=get_files(path)
pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=len(files)).start()
keys=valid_combinations(files)
axis_vals=keys_to_vals(keys)
#gen_sweep_space_scatter(axis_vals)
i = 0
v_in = [[[None for x in range(len(slew_rate))] for x in range(len(amplitude))] for x in range(len(period))]
i_in = [[[None for x in range(len(slew_rate))] for x in range(len(amplitude))] for x in range(len(period))]
v_out = [[[None for x in range(len(slew_rate))] for x in range(len(amplitude))] for x in range(len(period))]
i_out = [[[None for x in range(len(slew_rate))] for x in range(len(amplitude))] for x in range(len(period))]

for file in files[0:]:
  i+=1
  key = get_key(file)
  csv = import_csv(file, headers)
  time = [float(i/1e9) for i in csv[headers[0]]]
  v_in[key[0]][key[2]][key[1]] = [float(i) for i in csv[headers[1]]]
  supply_current = i_in[key[0]][key[2]][key[1]] = [float(i) for i in csv[headers[2]]]
  v_out[key[0]][key[2]][key[1]] = [float(i) for i in csv[headers[3]]]
  device_current = i_out[key[0]][key[2]][key[1]] = [float(i) for i in csv[headers[4]]]

  supply_cpp[key[0]][key[2]][key[1]] = p_p(time, supply_current, headers, device_current, 5+amplitude[key[2]]/2, period[key[0]])
  dc_o = dc_offset(time, supply_current, headers, device_current, 5+amplitude[key[2]]/2, period[key[0]])
  max_supply_slew_rate_n[key[0]][key[2]][key[1]] = average_falling_slew(supply_current, headers, device_current, 5+3*amplitude[key[2]]/8, 5+5*amplitude[key[2]]/8, period[key[0]])
  max_supply_slew_rate_p[key[0]][key[2]][key[1]] = average_rising_slew(supply_current, headers, device_current, 5+3*amplitude[key[2]]/8, 5+5*amplitude[key[2]]/8, period[key[0]])
  a = average_phase_delay(time, supply_current, device_current, headers, 5+amplitude[key[2]]/2, 5+amplitude[key[2]]/2, period[key[0]])
  supply_phase_delay_falling[key[0]][key[2]][key[1]] = a[0]
  supply_phase_delay_rising[key[0]][key[2]][key[1]] = a[1]
  pbar.update(i)
pbar.finish()

#for i in range(len(period)):
#  plot_time_domain(time, i_in, i, "Supply Current", "Time [s]", "Current [A]")
#for i in range(len(period)):
#  plot_time_domain(time, i_out, i, "Device Current", "Time [s]", "Current [A]")
#for i in range(len(period)):
#  plot_time_domain(time, v_in, i, "Supply Voltage", "Time [s]", "Voltage [V]")
#for i in range(len(period)):
#  plot_time_domain(time, v_out, i, "Device Voltage", "Time [s]", "Voltage [V]")

plot_P_A(amplitude, period, max_supply_slew_rate_n, "Average Falling Supply Slew Rate")
plot_P_A(amplitude, period, max_supply_slew_rate_p, "Average Rising Supply Slew Rate")
#plot_P_A(amplitude, period, supply_phase_delay_rising, "Phase Delay Rising Edge")
#plot_P_A(amplitude, period, supply_phase_delay_falling, "Phase Delay Falling Edge")
#plot_P_A(amplitude, period, supply_cpp, "Supply Current Peak to Peak")


