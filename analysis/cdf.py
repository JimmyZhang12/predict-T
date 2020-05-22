import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="", help="input csv to take fft of")
parser.add_argument('--warmup', type=int, default=0, help="time in nanoseconds of the warmup")
parser.add_argument('--headers', type=str, default="", help="the headers for the CSV")
parser.add_argument('--data', type=str, default="", help="the data to take the FFT of")
args = parser.parse_args()

# Import the CSV
df=pd.read_csv(args.input, header=None, names=args.headers.split(","))

x=np.array(df[args.headers.split(",")[0]][args.warmup:])
y=np.array(df[args.data.split(",")[0]][args.warmup:])
#v=np.array(df[args.data.split(",")[1]][args.warmup:])

dy=[]
dv=[]
for i in range(1, len(y)):
	dy.append(abs(y[i]-y[i-1]))
	#dv.append(abs(v[i]-v[i-1]))

fig, ax = plt.subplots(figsize=(8, 4))

# plot the cumulative histogram
n, bins, patches = ax.hist(dy, 1000, density=False, histtype='step',
                           cumulative=True, linewidth=2, label=args.data.split(",")[0])
#ax.hist(dv, 1000, density=False, histtype='step',
#                           cumulative=True, linewidth=2, label=args.data.split(",")[1])

# Add a line showing the expected distribution.
#y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
#     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
#y = y.cumsum()
#y /= y[-1]
#ax.plot(bins, y, 'k--', linewidth=1.5, label='Theoretical')

# tidy up the figure
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Distribution of Transients seen at Supply')
#ax.set_xlim(0.9, 1.1)
ax.set_xlabel("I")
ax.set_ylabel("%")
plt.show()
