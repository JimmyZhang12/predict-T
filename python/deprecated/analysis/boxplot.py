import pandas as pd
import glob
import numpy as np
#import seaborn as sns
import math
import sys
import matplotlib.pyplot as plt
import argparse
import statistics

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
parser.add_argument('--stat', type=str, default="vout", help="Plot")
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
    #names.append(file.split("/")[-1].replace(name+"_"+trace_len+"_"+resolution+"_", "").replace("_"+pdn+"_DecorOnly_out.csv", ""))
    #names.append(file.split("/")[-1].replace(name+"_"+trace_len+"_"+resolution+"_", "").replace("_"+pdn+"_IdealSensor_out.csv", ""))
    #names.append(file.split("/")[-1].replace(name+"_"+trace_len+"_"+resolution+"_", "").replace("_"+pdn+"_uArchEventPredictor_out.csv", ""))
    names.append(file.split("/")[-1].replace(name+"_"+trace_len+"_"+resolution+"_", "").replace("_"+pdn+"_HarvardPowerPredictor_out.csv", ""))
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

stat_to_plt = args.stat

emergency_above = args.e_high
emergency_below = args.e_low

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
    a[-1] = [a[-1][i] for i in range(0,len(a[-1]),10)]
    t[-1] = [t[-1][i] for i in range(0,len(t[-1]),10)]
  apps.append(a)
  times.append(t)

print(len(apps),len(times))

fig, axs = plt.subplots(len(tests), 1, tight_layout=False)
#fig, axs = plt.subplots(len(tests), 1, sharey=True, tight_layout=False)
fig.set_size_inches(5,5*len(tests))
for i in range(len(tests)):
  print(names[i])
  print(len(apps[i]))
  axs[i].boxplot(apps[i], whis=(0,100))
  axs[i].legend()
  axs[i].set_title(tests[i])
  axs[i].set_yticks(np.arange(0.9,1.10,0.01))
  #axs[i].set_xticks(range(len(names[i])), minor=False)
  axs[i].set_xticklabels(names[i])
  axs[i].set_xlabel("GHz")
  axs[i].set_ylabel("Voltage")
  #axs[i].set_ylabel("I Load (A)")
#fig.suptitle("Load Current "+pdn_model+" PDN")
fig.suptitle("Supply Voltage "+pdn_model+" PDN")
plt.show()
