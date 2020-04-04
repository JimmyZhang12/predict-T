# FFT
# 
# Generate an FFT with scipy and matplotlib
# 04/03/2020

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_csv', type=str, default="", help="input csv to take fft of")
parser.add_argument('--warmup_time', type=int, default=0, help="time in nanoseconds of the warmup")
parser.add_argument('--headers', type=str, default="", help="the headers for the CSV")
parser.add_argument('--data_frame', type=str, default="", help="the data to to plot")
args = parser.parse_args()

# Import the CSV
df=pd.read_csv(args.input_csv, header=None, names=args.headers.split(","))

x=np.array(df[args.headers.split(",")[0]][args.warmup_time:])
y=np.array(df[args.data_frame.split(",")[0]][args.warmup_time:])
v=np.array(df[args.data_frame.split(",")[1]][args.warmup_time:])

fig, ax1 = plt.subplots()
ax1.plot(x, y, color="blue")
ax1.set_ylabel("Req (Ohm)")
ax1.set_xlabel("Time (ns)")
ax2 = ax1.twinx()
ax2.plot(x, v, color="orange")
ax2.set_ylabel("Vout (V)")
fig.tight_layout()
plt.show()
