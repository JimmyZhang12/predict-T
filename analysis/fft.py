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
parser.add_argument('--data_frame', type=str, default="", help="the data to take the FFT of")
args = parser.parse_args()

# Import the CSV
df=pd.read_csv(args.input_csv, header=None, names=args.headers.split(","))

x=np.array(df[args.headers.split(",")[0]][args.warmup_time:])
y=np.array(df[args.data_frame.split(",")[0]][args.warmup_time:])
v=np.array(df[args.data_frame.split(",")[1]][args.warmup_time:])

x = 1/x

rate=1e9
sample_freq=(1/rate)
t = np.arange(0, (sample_freq)*len(x), sample_freq)
p = 20*np.log10(np.abs(np.fft.rfft(y)))
v = 20*np.log10(np.abs(np.fft.rfft(v)))
f = np.linspace(0, rate/2, len(p))
plt.plot(f[1:1000], p[1:1000], f[1:1000], v[1:1000])
plt.ylabel("Magnitude (dB)")
plt.xlabel("Freq (Hz)")
plt.show()

