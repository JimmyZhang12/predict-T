import os
import sys
import re
from cpu import CPU
from supply import Supply
import subprocess
import tempfile
import math
import argparse
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

parser = argparse.ArgumentParser()
parser.add_argument('--outpath', type=str, default="", help="output path")
parser.add_argument('--duty', type=str, default="0.5", help="duty cycle")
parser.add_argument('--device', type=str, default="server", help="")
args = parser.parse_args()

def plot_line(x, y, title, xtitle, ytitle):
  fig, ax = plt.subplots(1,1)
  fig.set_size_inches(7,7)
  fig.suptitle(title, fontsize=16)
  ax.plot(x, y, label="% Imrovement")
  #ax.set_title(title)
  ax.set_ylabel(ytitle)
  ax.set_xlabel(xtitle)
  plt.legend()
  plt.show()
  #plt.savefig(outfile+"period_"+str(i)+".png")

duty_cycles = list(np.linspace(0.10, 0.90, 10))
amplitudes = list(np.linspace(5, 995, 10))
cpu = [[CPU(10e-6, i, 100, j, 5) for i in duty_cycles] for j in amplitudes]
ll = list(np.linspace(10e-6, 0.2e-3, 10))
supplies = [Supply(1e-3, i, 1.2, 0.9, 1000, 0) for i in ll]

energies = np.zeros((len(amplitudes), len(duty_cycles), len(ll)))
energies_o = np.zeros((len(amplitudes), len(duty_cycles)))
savings = np.zeros((len(amplitudes), len(duty_cycles), len(ll)))

supply_base = Supply(1e-3, 0.3e-3, 1.2, 0.9, 1000, 0)

time = 0
tick = 0
timestep = 1e-9
energy_originals = 0
duration=20e-6
while time < duration:
  for i in range(len(amplitudes)):
    for j in range(len(duty_cycles)):
      cpu[i][j].tick()
  for i in range(len(amplitudes)):
    for j in range(len(duty_cycles)):
      for k in range(len(supplies)):
        supplies[k].tick(cpu[i][j].get_i())
        energies[i][j][k] += supplies[k].get_p()*timestep
      supply_base.tick(cpu[i][j].get_i())
      energies_o[i][j] += supply_base.get_p()*timestep
  time += timestep
  if(tick% 1000 == 0):
    print(supply_base.get_v(), supply_base.get_v_proc(), supply_base.get_i())
  tick += 1
for i in range(len(amplitudes)):
  for j in range(len(duty_cycles)):
    for k in range(len(supplies)):
      savings[i][j][k] = 100*(energies_o[i][j] - energies[i][j][k])/energies_o[i][j]
print(savings)
#plot_line(list(lls, [100*(energy_original - e)/energy_original for e in energies], "Load Lines", "Rll (Ohms)", "%")
#plot_lines(list(lls, [100*(energy_original - e)/energy_original for e in energies], "Load Lines", "Rll (Ohms)", "%")
