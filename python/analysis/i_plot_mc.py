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
args = parser.parse_args()

def get_files(path):
  files = glob.glob(path+"/*.csv")
  files = [i for i in files]
  files.sort()
  return files

def get_names(files):
  names = []
  for file in files:
    if "SMALL" in file:
      names.append("SMALL")
    if "MEDIUM" in file:
      names.append("MEDIUM")
    if "LARGE" in file:
      names.append("LARGE")
  return names

files = get_files(args.input)
names = get_names(files)
print(files)
print(names)

apps = []
times = []

stat_to_plt = "iout"

for file in files[0:2]:
  c_title="time,vin,va,vb,vout,_vout_mean,vout_mean,iin,iout,proc_load,enable,prediction,ttn,rt"
  df= pd.read_csv(file, header=None, names=c_title.split(","))
  apps.append([i for i in np.array(df[stat_to_plt][args.warmup:])])
  times.append([i/1000 for i in np.array(df["time"][args.warmup:])])
  print(len(times[-1]), len(apps[-1]))

print(len(apps),len(times))

fig, axs = plt.subplots(1, 1, tight_layout=True)
fig.set_size_inches(8,4)
for i, t, n in zip(apps, times, names):
  axs.plot(t, i, linewidth=1, label=n)
axs.legend()
#axs.set_yticks(np.arange(0.70,1.10,0.05))
axs.set_xlabel("Time (ns)")
#axs.set_ylabel("Vout (V)")
axs.set_ylabel("Idevice (A)")
fig.suptitle("Device Current Swaptions 8c/8t Harvard PDN")
plt.show()
