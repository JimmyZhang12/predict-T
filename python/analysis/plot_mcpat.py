# FFT
# 
# Generate an FFT with scipy and matplotlib
# 04/03/2020

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="", help="input csv")
parser.add_argument('--title', type=str, default="", help="name of the plot")
parser.add_argument('--warmup', type=int, default=0, help="time in nanoseconds of the warmup")
parser.add_argument('--end', type=int, default=0, help="time in nanoseconds of end of the plot")
parser.add_argument('--headers', type=str, default="", help="the headers for the CSV")
parser.add_argument('--data', type=str, default="", help="the data to to plot")
args = parser.parse_args()

# Import the CSV
df=pd.read_csv(args.input, header=None, names=args.headers.split(","))

y=[]

x=np.array(df[args.headers.split(",")[0]][args.warmup:args.end])/1000

for i in range(len(args.data.split(","))):
  if(args.end > args.warmup):
    y.append(np.array(df[args.data.split(",")[i]][args.warmup:args.end]))
  else:
    y.append(np.array(df[args.data.split(",")[i]][args.warmup:]))

for i in range(len(args.data.split("."))):
  plt.plot(x, y[i], linewidth=2, label=args.data.split(",")[i])

plt.xlabel("Time (us)")
plt.legend(loc='right')
plt.title(args.title)
plt.show()
