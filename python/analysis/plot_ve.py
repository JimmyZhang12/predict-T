import pandas as pd
import glob
import numpy as np
import math
import sys
import re
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="", help="Input Path")
parser.add_argument('--cycles', type=int, default=8, help="Cycles between stat dumps")
parser.add_argument('--frequency', type=float, default=3.0e9, help="CPU Frequency")
parser.add_argument('--proc_class', type=str, default="Desktop", help="CPU Class")
args = parser.parse_args()

def get_files(path):
  files = glob.glob(path+"/*.txt")
  files = [i for i in files]
  files.sort()
  return files

def get_names(files):
  names = []
  for i in files:
    f = i.split("/")[-1].split(".")[0]
    print(f)
    names.append(f)
  return names

def get_traces(files, stat_name, cycles, freq):
  t = 0.0
  step = ((1/freq)*8)*1.0e9 # Time step in ns
  traces = []
  times = []
  for file in files:
    time = []
    trace = []
    t = 0.0
    with open(file, "r") as infile:
      for line in enumerate(infile):
        statline = line[1]
        statline = sstr = re.sub('\s+', ' ', statline).strip()
        if(stat_name in statline):
          #print(statline)
          trace.append(float(statline.split(" ")[1]))
          time.append(step*t)
          t+=1
    traces.append(trace)
    times.append(time)
  return [times, traces]

proc_class = args.proc_class
freq = args.frequency
cycles = args.cycles
input = args.input

print([proc_class, freq, cycles, input])

files = get_files(input)
names = get_names(files)

window_small = 500
window_large = 5000
window_l = 2000
window_us = window_l + window_small
window_ul = window_l + window_large

# Num VE
times,traces = get_traces(files, "num_ve", cycles, freq)
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(8,5)
for t, s, n in zip(times, traces, names):
  axs.plot(t[0:7000], s[0:7000], linewidth=1, label=n)
axs.legend()
axs.set_xlabel("Time (ns)")
axs.set_ylabel("Voltage Emergencies")
fig.suptitle("Number of Voltage Emergencies "+proc_class+" CPU+PDN")
plt.show()

# Num Threshold Crossing
times,traces = get_traces(files, "num_tc", cycles, freq)
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(8,5)
for t, s, n in zip(times, traces, names):
  axs.plot(t[0:7000], s[0:7000], linewidth=1, label=n)
axs.legend()
axs.set_xlabel("Time (ns)")
axs.set_ylabel("Threshold Crossings")
fig.suptitle("Number of Threshold Crossings "+proc_class+" CPU+PDN")
plt.show()

# Voltage
times,traces = get_traces(files, "supply_voltage ", cycles, freq)
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(8,5)
for t, s, n in zip(times, traces, names):
  axs.plot(t[window_l:window_ul], s[window_l:window_ul], linewidth=1, label=n)
axs.legend()
axs.set_xlabel("Time (ns)")
axs.set_ylabel("Supply Voltage (V)")
fig.suptitle("Supply Voltage "+proc_class+" CPU+PDN")
plt.show()

# Voltage Zoom
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(8,5)
for t, s, n in zip(times, traces, names):
  axs.plot(t[window_l:window_us], s[window_l:window_us], linewidth=1, label=n)
axs.legend()
axs.set_xlabel("Time (ns)")
axs.set_ylabel("Supply Voltage (V)")
fig.suptitle("Supply Voltage "+proc_class+" CPU+PDN")
plt.show()

# Current
times,traces = get_traces(files, "supply_current", cycles, freq)
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(8,5)
for t, s, n in zip(times, traces, names):
  axs.plot(t[window_l:window_ul], s[window_l:window_ul], linewidth=1, label=n)
axs.legend()
axs.set_xlabel("Time (ns)")
axs.set_ylabel("Supply Current (A)")
fig.suptitle("Supply Current "+proc_class+" CPU+PDN")
plt.show()

# Current Zoom
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(8,5)
for t, s, n in zip(times, traces, names):
  axs.plot(t[window_l:window_us], s[window_l:window_us], linewidth=1, label=n)
axs.legend()
axs.set_xlabel("Time (ns)")
axs.set_ylabel("Supply Voltage (V)")
fig.suptitle("Supply Voltage "+proc_class+" CPU+PDN")
plt.show()
