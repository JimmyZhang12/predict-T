import os
import sys
import re
import subprocess
import tempfile
import math
import argparse
import numpy as np
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

parser = argparse.ArgumentParser()
parser.add_argument('--outpath', type=str, default="", help="output path")
parser.add_argument('--duty', type=str, default="0.5", help="duty cycle")
parser.add_argument('--device', type=str, default="server", help="")
args = parser.parse_args()

if(args.device == "server"):
  period = [20e-9, 100e-9, 200e-9, 1e-6, 2e-6, 10e-6, 20e-6, 100e-6]
  slew_rate = list(np.arange(0.01, 0.3, 0.05))
  amplitude = [25,50,95]
  duration=500e-6
  timestep=1e-9
  min_power = 5

if(args.device == "laptop"):
  period = [200e-9, 1e-6, 2e-6, 10e-6, 20e-6, 100e-6]
  slew_rate = list(np.arange(0.01, 0.3, 0.05))
  amplitude = [10,25,50]
  duration=500e-6
  timestep=1e-9
  min_power = 1

if(args.device == "mobile"):
  period = [200e-9, 1e-6, 2e-6, 10e-6, 20e-6, 100e-6]
  slew_rate = list(np.arange(0.01, 0.3, 0.05)/(2000/3000))
  amplitude = [1,3,5]
  duration=500e-6
  timestep=1e-9
  min_power = 0.1

if(args.device == "embedded"):
  period = [200e-9, 1e-6, 2e-6, 10e-6, 20e-6, 100e-6]
  slew_rate = list(np.arange(0.01, 0.3, 0.05)/(1500/3000))
  amplitude = [0.5,1,2]
  duration=500e-6
  timestep=1e-9
  min_power = 0.1

if(args.device == "perf_uc"):
  period = [200e-9, 1e-6, 2e-6, 10e-6, 20e-6, 100e-6]
  slew_rate = list(np.arange(0.01, 0.3, 0.05)/(120/3000))
  amplitude = [0.05,0.1,0.15]
  duration=500e-6
  timestep=1e-9
  min_power = 0.01

if(args.device == "lp_uc"):
  period = [200e-9, 1e-6, 2e-6, 10e-6, 20e-6, 100e-6]
  slew_rate = list(np.arange(0.01, 0.3, 0.05)/(10/3000))
  amplitude = [0.003,0.005,0.010]
  duration=500e-6
  timestep=1e-9
  min_power = 0.001

outpath = args.outpath

duty = float(args.duty)

def increase_power(power, max_power, slew_rate):
  return min(max_power, power+slew_rate)

def decrease_power(power, min_power, slew_rate):
  return max(min_power, power-slew_rate)

def calc_req(power, voltage):
  return voltage*voltage/power

def arg_check(period, slew_rate, min_power, peak_power, timestep, duration, outpath, per_idx, sl_idx, amp_idx):
  time = 0
  half_p = period/2;
  power = min_power
  min_rr = 2e-5
  max_rr = 5e-6
  if (((peak_power - min_power)/slew_rate)/1e9 > min(duty*period, (1-duty)*period)):
    return False
  if(period < max_rr and (peak_power - min_power) > 25):
    return False
  if(period < min_rr and (peak_power - min_power) > (2e-5/period)*100):
    return False
  return True

def trace(period, slew_rate, min_power, peak_power, timestep, duration, outpath, per_idx, sl_idx, amp_idx):
  time = 0
  half_p = period/2;
  power = min_power
  min_rr = 2e-5
  max_rr = 5e-6
  if (((peak_power - min_power)/slew_rate)/1e9 > min(duty*period, (1-duty)*period)):
    return False
  if(period < max_rr and (peak_power - min_power) > 25):
    return False
  if(period < min_rr and (peak_power - min_power) > (2e-5/period)*100):
    return False

  outname = "trace_"+str(per_idx)+"_"+str(sl_idx)+"_"+str(amp_idx)+".csv"
  outfile = os.path.join(outpath,outname)
  with open(outfile, "w") as of:
    time = 0
    power = min_power
    while(time < duration):
      # Start with off:
      t1 = time
      while(time < t1 + (1-duty)*period):
        power = decrease_power(power, min_power, slew_rate)
        res = calc_req(power, 1.0)
        of.write(",".join([str(time),str(res),str(power)])+"\n")
        time += timestep
      t1 = time
      while(time < t1 + duty*period):
        power = increase_power(power, peak_power, slew_rate)
        res = calc_req(power, 1.0)
        of.write(",".join([str(time),str(res),str(power)])+"\n")
        time += timestep
  return True

total = len(period)*len(slew_rate)*len(amplitude)
total = 0
for i in range(len(period)):
  for j in range(len(slew_rate)):
    for k in range(len(amplitude)):
      if(arg_check(period[i], slew_rate[j], min_power, min_power+amplitude[k], timestep, duration, outpath, i, j, k)):
        total += 1
pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=total).start()

total = 0
for i in range(len(period)):
  for j in range(len(slew_rate)):
    for k in range(len(amplitude)):
      if(trace(period[i], slew_rate[j], min_power, min_power+amplitude[k], timestep, duration, outpath, i, j, k)):
        total += 1
      pbar.update(total)
pbar.finish()
