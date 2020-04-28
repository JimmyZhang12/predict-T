import pandas as pd
import sys
import glob
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import argparse
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer
import cProfile

parser = argparse.ArgumentParser()
args = parser.parse_args()

cmax = 150
current=np.linspace(0.0, cmax, num=cmax)

def load_line(vid, ll, current):
  voltage = []
  for i in current:
    voltage.append(vid - i*ll)
  return voltage

def voltage_cbulk(rpa, current, voltage):
  voltage_cbulk=[]
  for i in range(len(current)):
    voltage_cbulk.append(current[i]*rpa + voltage[i])
  return voltage_cbulk

vid_norm = 1.2
vout_norm = load_line(vid_norm, 0.0008, current)
vout_bulk = voltage_cbulk(0.0008, current, vout_norm)

new_ll = 1e-6
vout_min = vout_norm[-1]
vid_new = new_ll*cmax+vout_min

vout_new = load_line(vid_new, new_ll, current)
vout_bulk_new = voltage_cbulk(0.0008, current, vout_new)

fig, ax = plt.subplots(1,1)
fig.set_size_inches(20,7)
fig.suptitle("Load Lines", fontsize=24)
ax.plot(current, vout_norm, label="Vout @ Processor LL:0.8mOhm")
ax.plot(current, vout_bulk, label="Vout @ CBulk LL:0.8mOhm")
ax.plot(current, vout_new, label="Vout @ Processor LL:1uOhm")
ax.plot(current, vout_bulk_new, label="Vout @ CBulk LL:1uOhm")
#ax.set_title()
ax.set_ylabel("Voltage [V]")
ax.set_xlabel("Current [A]")
plt.legend()
plt.show()
