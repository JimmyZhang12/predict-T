import pandas as pd
import glob
import numpy as np
import math
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="", help="input path")
parser.add_argument('--warmup', type=int, default=100000, help="time in nanoseconds of the warmup")
parser.add_argument('--end', type=int, default=0, help="time in nanoseconds of end of the plot")
#parser.add_argument('--headers', type=str, default="", help="the headers for the CSV")
#parser.add_argument('--data', type=str, default="", help="the data to to plot")
args = parser.parse_args()

def get_files(path):
  return glob.glob(path+"/*.csv")

def get_csvs(files, csv_names):
  dfs = []
  for file in files:
    dfs.append(pd.read_csv(file, header=None, names=csv_names.split(",")))
  return dfs

def get_names(files, str_replace):
  names = []
  for file in files:
    names.append(file.split("/")[-1].replace(str_replace, ""))
  return names

files = get_files(args.input)
csvs = get_csvs(files, "time,vin,iin,vout,iout,rout,rlast,rnext,dr")
names = get_names(files, "_1000000_PRED_TEST_out.csv")
print(files)
print(names)

apps = []
times = []

for csv in csvs:
  if(args.end > args.warmup):
    apps.append([i for i in np.array(csv["vout"][args.warmup:args.end])])
    times.append([i/1000 for i in np.array(csv["time"][args.warmup:args.end])])
  else:
    apps.append([i for i in np.array(csv["vout"][args.warmup:])])
    times.append([i/1000 for i in np.array(csv["time"][args.warmup:])])

plt.subplot(1, 1, 1)
#plt.hold(True)
for i, t, n in zip(apps, times, names):
  plt.plot(t, i, linewidth=1, label=n)
plt.ylabel("I (A)")
plt.xlabel("Time (us)")
plt.legend(loc='right')
plt.title("MiBench Application Profiles")
plt.show()
