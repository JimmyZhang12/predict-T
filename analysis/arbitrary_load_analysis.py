import pandas as pd
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
supply_vpp = np.zeros((len(period), len(amplitude), len(slew_rate)))
supply_stabilization = np.zeros((len(period), len(amplitude), len(slew_rate)))
supply_cpp = np.zeros((len(period), len(amplitude), len(slew_rate)))
supply_phase_delay = np.zeros((len(period), len(amplitude), len(slew_rate)))

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

def max_pos_slew_rate(df, headers):
  supply_current = df[headers[2]]
  prev = supply_current[10]
  cmax = 0
  for i in supply_current[10:]:
    cmax = max(i-prev, cmax)
    prev = i
  return cmax

def max_neg_slew_rate(df, headers):
  supply_current = df[headers[2]]
  prev = supply_current[10]
  cmin = 0
  for i in supply_current[10:]:
    cmin = min(i-prev, cmin)
    prev = i
  return abs(cmin)

def plot_P_A(x, y, data_vector, super_title):
  """ Plots Period on X axis Amplitude on Y axis """
  fig, axs = plt.subplots(2,3)
  fig.set_size_inches(20,15)
  fig.suptitle(super_title, fontsize=24)
  levels = np.linspace(data_vector[:,:,-1].min(), data_vector[:,:,-1].max(), 50)[1:]
  for ax, i in zip(axs.ravel(), range(len(slew_rate))):
    print(data_vector[:,:,i].shape)
    print(len(x))
    print(len(y))
    print(data_vector[:,:,i])
    CS = ax.contourf(x, y, data_vector[:,:,i], levels)
    #CS.set_under('k')
    CS.set_clim(levels[0], levels[-1])
    fig.colorbar(CS, ax=ax, shrink=0.9)
    ax.set_title("Load Slew "+"{:.3f}".format(slew_rate[i])+" [A/ns]")
    ax.set_ylabel("Period [s]")
    ax.set_xlabel("Amplitude [A]")
  plt.show()


path=args.input
headers=args.headers

files=get_files(path)
pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=len(files)).start()
keys=valid_combinations(files)
axis_vals=keys_to_vals(keys)
#gen_sweep_space_scatter(axis_vals)
i = 0
for file in files:
  i+=1
  key = get_key(file)
  csv = import_csv(file, headers)
  max_supply_slew_rate_n[key[0]][key[2]][key[1]] = max_neg_slew_rate(csv, headers)
  max_supply_slew_rate_p[key[0]][key[2]][key[1]] = max_pos_slew_rate(csv, headers)
  pbar.update(i)
pbar.finish()

plot_P_A(amplitude, period, max_supply_slew_rate_n, "Max Negative Supply Slew Rate")
plot_P_A(amplitude, period, max_supply_slew_rate_p, "Max Positive Supply Slew Rate")


