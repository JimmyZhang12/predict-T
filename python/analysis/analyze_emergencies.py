import pandas as pd
import glob
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="", help="input path")
parser.add_argument('--warmup', type=int, default=1, help="time in nanoseconds of the warmup")
parser.add_argument('--end', type=int, default=0, help="time in nanoseconds of end of the plot")
parser.add_argument('--tests', type=str, default="", help="test names to read in")
parser.add_argument('--pdn', type=str, default="HARVARD", help="PDN Type")
parser.add_argument('--e_low', type=float, default=0.95)
parser.add_argument('--e_high', type=float, default=1.05)
parser.add_argument('--resolution', type=str, default="1", help="Resolution in cpu-cycles")
parser.add_argument('--trace_len', type=str, default="1", help="Trace length in epochs")
#parser.add_argument('--headers', type=str, default="", help="the headers for the CSV")
#parser.add_argument('--data', type=str, default="", help="the data to to plot")
args = parser.parse_args()

def get_files(path, name):
  print(name)
  files = glob.glob(path+"/*"+name+"*.csv")
  files = [i for i in files]
  files.sort()
  return files

def get_csvs(files, csv_names):
  dfs = []
  for file in files:
    dfs.append(pd.read_csv(file, header=None, names=csv_names.split(",")))
  return dfs

def get_names(files, name, trace_len, resolution, pdn):
  names = []
  for file in files:
    names.append(file.split("/")[-1].replace(name+"_"+trace_len+"_"+resolution+"_", "").replace("_"+pdn+"_IdealSensor_out.csv", ""))
  return names

pdn_model=args.pdn
tests = args.tests.split(",")
resolution = args.resolution
trace_len = args.trace_len
files = []
csvs = []
names = []
for name in tests:
  files.append(get_files(args.input, name))
  csvs.append(get_csvs(files[-1], "time,vin,va,vb,vout,_vout_mean,vout_mean,iin,iout,proc_load,enable,prediction,ttn,rt"))
  names.append(get_names(files[-1], name, trace_len, resolution, pdn_model))
print(files)
print(names)

apps = []
times = []

stat_to_plt = "vout"

for j in range(len(tests)):
  a = []
  t = []
  for csv in csvs[j]:
    if(args.end > args.warmup):
      a.append([i for i in np.array(csv[stat_to_plt][args.warmup:args.end])])
      t.append([i for i in np.array(csv["time"][args.warmup:args.end])])
    else:
      a.append([i for i in np.array(csv[stat_to_plt][args.warmup:])])
      t.append([i for i in np.array(csv["time"][args.warmup:])])
      print(len(np.array(csv[stat_to_plt][args.warmup:])), len(np.array(csv["time"][args.warmup:])))
  apps.append(a)
  times.append(t)

print(len(apps),len(times))


emergency_above = args.e_high
emergency_below = args.e_low

### % Picoseconds In Emergency Low/High
percentage_in_emergency_low = []
percentage_in_emergency_high = []
for i in apps:
  plow = []
  phigh = []
  for app in i:
    p_l=0
    p_u=0
    p_total=0
    for voltage in app:
      if voltage > emergency_above:
        p_u+=1
      if voltage < emergency_below:
        p_l+=1
      p_total+=1
    plow.append(p_l/p_total)
    phigh.append(p_u/p_total)
  percentage_in_emergency_low.append(plow)
  percentage_in_emergency_high.append(phigh)


fig, axs = plt.subplots(1, len(tests), tight_layout=False)
fig.set_size_inches(5*len(tests),6)
for i in range(len(tests)):
  axs[i].bar(range(len(percentage_in_emergency_low[i])), percentage_in_emergency_low[i], label="Emergency Low")
  axs[i].bar(range(len(percentage_in_emergency_high[i])), percentage_in_emergency_high[i], label="Emergency High")
  axs[i].legend()
  axs[i].set_title(tests[i])
  axs[i].set_yticks(np.arange(0.0,1.05,0.05))
  axs[i].set_xticks(range(len(percentage_in_emergency_low[i])), minor=False)
  axs[i].set_xticklabels(names[i], minor=False)
  axs[i].set_xlabel("Clock Freq")
  axs[i].set_ylabel("% Execution Time")
fig.suptitle("%Execution time in Voltage Emergency; "+pdn_model+" PDN, ["+str(emergency_below)+","+str(emergency_above)+"]")
plt.show()

### Consecutive Picoseconds spent in Emergency Low:
min_time = 10000000000
for i in times:
  for j in i:
    print(len(j))
    if len(j) < min_time:
      min_time = len(j)

print(min_time)

histogram_low = []
histogram_high = []
for i in apps:
  histl = []
  histh = []
  for app in i:
    time_start = 0
    above = False
    below = False
    hl = []
    hh = []
    for i in range(min_time):
      voltage_prev = app[i-1]
      voltage = app[i]
      if voltage > emergency_above and voltage_prev <= emergency_above:
        above = True
        time_start = i
      if voltage < emergency_above and voltage_prev >= emergency_above:
        above = False
        hh.append(i-time_start)
      if voltage < emergency_below and voltage_prev >= emergency_below:
        below = True
        time_start = i
      if voltage > emergency_below and voltage_prev <= emergency_below:
        below = False
        hl.append(i-time_start)
    hl_filter = []
    hh_filter = []
    for i in hl:
      if i > 10:
        hl_filter.append(i)
    for i in hh:
      if i > 10:
        hh_filter.append(i)
    histl.append(hl_filter)
    histh.append(hh_filter)
  histogram_low.append(histl)
  histogram_high.append(histh)

n_bins = 50

print(histogram_low)

fig, axs = plt.subplots(len(apps), len(apps[0]), sharex=True, sharey=True, tight_layout=False)
fig.set_size_inches(4*len(apps[0]),4*len(apps))
for i in range(len(apps)):
  for j in range(len(apps[0])):
    axs[i][j].hist([histogram_low[i][j],histogram_high[i][j]], bins=n_bins, histtype='bar', stacked=True, label=["Emergency Low", "Emergency High"])
    axs[i][j].legend()
    axs[i][j].set_title(" ".join([names[i][j],tests[i]]))
    axs[i][j].set_xlabel("Time (ps)")
    axs[i][j].set_ylabel("#")
fig.suptitle("Distribution of Emergency Length; "+pdn_model+" PDN, ["+str(emergency_below)+","+str(emergency_above)+"]")
plt.show()
