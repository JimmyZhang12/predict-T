import pandas as pd
import glob
import numpy as np
import math
import sys
import re
import matplotlib.pyplot as plt
import argparse
from scipy import stats, optimize, interpolate

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
  def parse_trace(fd, length, step):
    t = 0.0
    trace = []
    time = []
    for line in enumerate(infile):
      statline = line[1]
      statline = sstr = re.sub('\s+', ' ', statline).strip()
      if(stat_name in statline):
        #print(statline)
        if(stat_name == "state "):
          trace.append(float(statline.split(" ")[1])-1.0)
        else:
          trace.append(float(statline.split(" ")[1]))
        time.append(step*t)
        t+=1
      if t != -1 and t >= length:
        return trace, time
    return trace, time

  step = ((1/freq)*8)*1.0e9 # Time step in ns
  traces = []
  times = []
  for file in files:
    time = []
    trace = []
    with open(file, "r") as infile:
      trace, time = parse_trace(infile, 100000, step)
    traces.append(trace)
    times.append(time)
  return [times, traces]

def parse(stalls, instructions_pending, sys_voltage, cycles):
  new_stall = False
  unstall_time = 0
  stall_time = 0.0
  min_voltage = 1000
  pending_inst = 0
  peak_pending_inst = 0
  stall_duration = []
  average_pending_inst = []
  minimum_voltage = []
  first = True
  time = 0
  for i in range(1, len(stalls)):
    time += cycles
    if(stalls[i] == cycles and stalls[i-1] != cycles):
      # We are beginning a new ICache Stall
      print("Stall Begin @ "+str(time))
      if not first:
        #average_pending_inst.append(pending_inst/max(unstall_time, 1))
        average_pending_inst.append(peak_pending_inst)
        minimum_voltage.append(min_voltage)
      pending_inst = 0
      peak_pending_inst = 0
      unstall_time = 0
      min_voltage = 1000
      stall_time = 0.0
      new_stall = True
      first = False
      assert(len(minimum_voltage) == len(average_pending_inst))
      assert(len(minimum_voltage) == len(stall_duration))
    elif(new_stall == True and stalls[i] != cycles):
      # We are ending a ICache Stall Cycle
      print("Stall End @ "+str(time))
      stall_duration.append(stall_time)
      new_stall = False

    if(new_stall):
      stall_time += cycles
    else:
      if(sys_voltage[i] < min_voltage):
        min_voltage = sys_voltage[i]
        print("MinVoltage "+str(min_voltage)+" @ "+str(time))
    if(not new_stall and unstall_time < 12*cycles):
      unstall_time += cycles
      pending_inst += instructions_pending[i]
      if(peak_pending_inst < instructions_pending[i]):
        peak_pending_inst = instructions_pending[i]

  ml = min(len(minimum_voltage), len(average_pending_inst))
  ml = min(ml, len(stall_duration))
  return stall_duration[0:ml], average_pending_inst[0:ml], minimum_voltage[0:ml]

def parse_decode_stall(stalls, instructions_pending, sys_voltage, cycles):
  new_stall = False
  unstall_time = 2
  stall_time = 0.0
  min_voltage = 1000
  pending_inst = 0
  peak_pending_inst = 0
  stall_duration = []
  unstall_duration = []
  average_pending_inst = []
  minimum_voltage = []
  time = 0
  for i in range(1, len(stalls)):
    time += cycles
    if(stalls[i] == 1 and stalls[i-1] != 1):
      # We are beginning a new ICache Stall
      print("Stall Begin @ "+str(time))
      stall_time = 0.0
      new_stall = True
      assert(len(minimum_voltage) == len(average_pending_inst))
      assert(len(minimum_voltage) == len(stall_duration))
    elif(new_stall == True and stalls[i] != 1):
      # We are ending a ICache Stall Cycle
      print("Stall End @ "+str(time))
      stall_duration.append(stall_time)
      unstall_duration.append(unstall_time)
      average_pending_inst.append(pending_inst/unstall_time)
      minimum_voltage.append(min_voltage)
      pending_inst = 0
      peak_pending_inst = 0
      unstall_time = 0
      min_voltage = 1000
      new_stall = False

    if(new_stall):
      stall_time += cycles
    if(sys_voltage[i] < min_voltage):
      min_voltage = sys_voltage[i]
      print("MinVoltage "+str(min_voltage)+" @ "+str(time))
    if(not new_stall):
      unstall_time += cycles
      pending_inst += instructions_pending[i]
      if(peak_pending_inst < instructions_pending[i]):
        peak_pending_inst = instructions_pending[i]

  ml = min(len(minimum_voltage), len(average_pending_inst))
  ml = min(ml, len(stall_duration))
  return stall_duration[0:ml], average_pending_inst[0:ml], minimum_voltage[0:ml], unstall_duration[0:ml]

proc_class = args.proc_class
freq = args.frequency
cycles = args.cycles
input = args.input

print([proc_class, freq, cycles, input])

files = get_files(input)
names = get_names(files)

times, stalls = get_traces(files, "icacheStallCycles", cycles, freq)
times, instrs = get_traces(files, "instsReadyMax", cycles, freq)
times, volt = get_traces(files, "supply_voltage ", cycles, freq)

times, stalls = get_traces(files, "decode_idle", cycles, freq)
times, instrs = get_traces(files, "insts_available", cycles, freq)

total_sd = []
total_api = []
total_mv = []
total_ud = []
for i in range(len(names)):
  sd, api, mv, ud = parse_decode_stall(stalls[i], instrs[i], volt[i], cycles)
  total_sd += sd
  total_api += api
  total_mv += mv
  total_ud += ud

print(len(total_sd), len(total_api), len(total_mv))

# Stall Duration v Instructions Pending
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(5,5)
plt.scatter(total_sd, total_api, s=0.75, c="k", alpha=1.0)
#axs.legend()
axs.set_xlabel("Stall Duration")
axs.set_ylabel("Instructions Pending")
fig.suptitle(proc_class)
plt.show()

print(stats.pearsonr(total_sd, total_api))

# Stall Duration v Min Voltage
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(5,5)
plt.scatter(total_sd, total_mv, s=0.75, c="k", alpha=1.0)
#axs.legend()
axs.set_xlabel("Stall Duration")
axs.set_ylabel("Minimum Voltage")
fig.suptitle(proc_class)
plt.show()
print(stats.pearsonr(total_sd, total_mv))

# Instructions Pending v Min Voltage
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(5,5)
plt.scatter(total_api, total_mv, s=0.75, c="k", alpha=1.0)
#axs.legend()
axs.set_xlabel("Instructions Pending")
axs.set_ylabel("Minimum Voltage")
fig.suptitle(proc_class)
plt.show()
print(stats.pearsonr(total_api, total_mv))

# Instructions Pending v Min Voltage
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(5,5)
plt.scatter(total_api, total_ud, s=0.75, c="k", alpha=1.0)
#axs.legend()
axs.set_xlabel("Avg Instructions Pending")
axs.set_ylabel("Duration")
fig.suptitle(proc_class)
plt.show()
print(stats.pearsonr(total_api, total_ud))

