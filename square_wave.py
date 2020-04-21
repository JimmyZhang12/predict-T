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


period = [2e-9, 5e-9, 10e-9, 50e-9, 100e-9, 500e-9, 1e-6, 5e-6, 10e-6, 50e-6, 100e-6, 500e-6, 1e-3]
slew_rate = list(np.arange(0.01, 0.3, 0.05))
amplitude = range(5, 100, 4)
duration=5e-3
timestep=1e-9
min_power = 1


parser = argparse.ArgumentParser()
parser.add_argument('--outpath', type=str, default="", help="output path")
args = parser.parse_args()

outpath = args.outpath

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
  if (((peak_power - min_power)/slew_rate)/1e9 > half_p):
    return False
  return True

def trace(period, slew_rate, min_power, peak_power, timestep, duration, outpath, per_idx, sl_idx, amp_idx):
  time = 0
  half_p = period/2;
  power = min_power
  if (((peak_power - min_power)/slew_rate)/1e9 > half_p):
    return False

  outname = "trace_"+str(per_idx)+"_"+str(sl_idx)+"_"+str(amp_idx)+".csv"
  outfile = os.path.join(outpath,outname)
  with open(outfile, "w") as of:
    time = 0
    power = min_power
    while(time < duration):
      # Start with off:
      t1 = time
      while(time < t1 + half_p):
        power = decrease_power(power, min_power, slew_rate)
        res = calc_req(power, 1.0)
        of.write(",".join([str(time),str(res),str(power)])+"\n")
        time += timestep
      t1 = time
      while(time < t1 + half_p):
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
