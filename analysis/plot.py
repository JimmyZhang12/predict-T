# FFT
# 
# Generate an FFT with scipy and matplotlib
# 04/03/2020

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="", help="input csv to take fft of")
parser.add_argument('--title', type=str, default="", help="name of the plot")
parser.add_argument('--warmup', type=int, default=0, help="time in nanoseconds of the warmup")
parser.add_argument('--headers', type=str, default="", help="the headers for the CSV")
parser.add_argument('--data', type=str, default="", help="the data to to plot")
args = parser.parse_args()

# Import the CSV
df=pd.read_csv(args.input, header=None, names=args.headers.split(","))

x=np.array(df[args.headers.split(",")[0]][args.warmup:])/1000
y=np.array(df[args.data.split(",")[0]][args.warmup:])
v=np.array(df[args.data.split(",")[1]][args.warmup:])
z=np.array(df[args.data.split(",")[2]][args.warmup:])
w=np.array(df[args.data.split(",")[3]][args.warmup:])

#fig, ax1 = plt.subplots()
#ax1.plot(x, y, color="blue")
#ax1.set_ylabel("Req (Ohm)")
#ax1.set_xlabel("Time (ns)")
#ax2 = ax1.twinx()
#ax2.plot(x, v, color="orange")
#ax2.set_ylabel("Vout (V)")
#fig.tight_layout()
#plt.show()

plt.subplot(2, 1, 1)
plt.plot(x, y, x, z)
plt.ylabel("V")
plt.xlabel("Time (us)")
plt.title(args.title)

plt.subplot(2, 1, 2)
plt.plot(x, v, x, w)
plt.ylabel("A")
plt.xlabel('Time (us)')
plt.show()
