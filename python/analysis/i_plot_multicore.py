import pandas as pd
import glob
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="", help="input path/to/file")
parser.add_argument('--name', type=str, default="", help="name of plot")
parser.add_argument('--nc', type=int, default=1, help="num cores to plot")
parser.add_argument('--timestep', type=float, default=2.5, help="timestep in ns")

args = parser.parse_args()

cores = [[] for i in range(args.nc)]
time = []
i = 0
t = 0
#print(cores)
with open(args.input, 'r') as infile:
  for line in infile.readlines():
    #print(i%args.nc)
    key = int(i%args.nc)
    if key == 0:
      cores[0].append(float(line.strip()))
    if key == 1:
      cores[1].append(float(line.strip()))
    if key == 2:
      cores[2].append(float(line.strip()))
    if key == 3:
      cores[3].append(float(line.strip()))
    if key == 4:
      cores[4].append(float(line.strip()))
    if key == 5:
      cores[5].append(float(line.strip()))
    if key == 6:
      cores[6].append(float(line.strip()))
    if key == 7:
      cores[7].append(float(line.strip()))
    if key == 0:
      #print("Append time "+str(t*args.timestep))
      time.append(t*args.timestep)
      t+=1
    i+=1

print(i)
print([len(i) for i in cores],len(time))

fig, axs = plt.subplots(tight_layout=True)
fig.set_size_inches(8, 4)
for i in range(len(cores)):
  axs.plot(time, cores[i], label="Core "+str(i))
#axs.stackplot(time, cores, labels=["Core "+str(i) for i in range(len(cores))])
axs.legend()
#axs.set_yticks(np.arange(0.0,1.0,0.1))
axs.set_xlabel("Time (ns)")
#axs.set_ylabel("% Runtime Dynamic Current (A)")
axs.set_ylabel("Core Runtime Dynamic Current (A)")
axs.title.set_text("Fluidanimate 8c/8t Small Caches")
plt.show()
