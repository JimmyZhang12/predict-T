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
parser.add_argument('--resolution', type=str, default="1", help="Resolution in cpu-cycles")
parser.add_argument('--trace_len', type=str, default="1", help="Trace length in epochs")
parser.add_argument('--pdn', type=str, default="HARVARD", help="PDN Type")
parser.add_argument('--stat', type=str, default="vout", help="Plot")
args = parser.parse_args()

def get_files(path, name):
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
title = "Time Domain Trace"
print(files)
print(names)

apps = []
times = []

stat_to_plt = args.stat

for j in range(len(tests)):
  a = []
  t = []
  for csv in csvs[j]:
    if(args.end > args.warmup):
      a.append([i for i in np.array(csv[stat_to_plt][args.warmup:args.end])])
      t.append([i/1000 for i in np.array(csv["time"][args.warmup:args.end])])
    else:
      a.append([i for i in np.array(csv[stat_to_plt][args.warmup:])])
      t.append([i/1000 for i in np.array(csv["time"][args.warmup:])])
      print(len(np.array(csv[stat_to_plt][args.warmup:])), len(np.array(csv["time"][args.warmup:])))
  apps.append(a)
  times.append(t)

print(len(apps),len(times))

fig, axs = plt.subplots(len(tests), 1, tight_layout=False)
fig.set_size_inches(12,5*len(tests))
for j in range(len(tests)):
  for i, t, n in zip(apps[j], times[j], names[j]):
    axs[j].plot(t, i, linewidth=1, label=n)
  axs[j].legend()
  axs[j].set_title(tests[j])
  axs[j].set_yticks(np.arange(0.0,50,5))
  #axs[j].set_yticks(np.arange(0.9,1.1,0.05))
  axs[j].set_xlabel("Time (ns)")
  #axs[j].set_ylabel("10c Period (ps)")
  #axs[j].set_ylabel("Vout (V)")
  axs[j].set_ylabel("Iout (A)")
fig.suptitle(title+" "+pdn_model+" PDN; Resolution "+resolution+"c")
plt.show()
