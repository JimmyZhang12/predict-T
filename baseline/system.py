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

def plot_2D(x, y, z, data_vector, super_title, outfile, title):
  """ Plots Period on X axis Amplitude on Y axis """
  fig, axs = plt.subplots(2,3)
  fig.set_size_inches(20,10)
  fig.suptitle(super_title, fontsize=24)
  mi = 10000000
  ma = 0
  for i in range(len(x)):
    for j in range(len(y)):
      for k in range(len(z)):
        if(data_vector[i,j,k] != 0.0):
          mi = min(data_vector[i,j,k], mi)
  for i in range(len(x)):
    for j in range(len(y)):
      for k in range(len(z)):
        ma = max(data_vector[i,j,k], ma)
  levels = np.linspace(mi, ma, 1000)[:]
  print(levels)
  for ax, i in zip(axs.ravel(), range(len(z))):
    print(data_vector[:,:,i].shape)
    print(len(x))
    print(len(y))
    print(data_vector[:,:,i])
    CS = ax.contourf(x, y, data_vector[:,:,i], levels, cmap=plt.cm.bone)
    CS2 = ax.contour(CS, levels=CS.levels[::100], colors='r')
    CS2.set_clim(levels[0], levels[-1])
    ax.clabel(CS2, fmt='%.2f', colors='w', fontsize=10)
    fig.colorbar(CS, ax=ax, shrink=0.9)
    ax.set_title("Virtual Load Line "+"{:.3f}".format(1e3*z[i])+" [mOhm]")
    ax.set_ylabel("Duty Cycle")
    ax.set_xlabel("Amplitude [A]")
  plt.show()
  #plt.savefig(outfile+title+".png")

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

imax = 5
imin = 0.1
vmin = 1.05
vmax = 1.2
rpdn = 0.2e-3
rll = (vmax - vmin)/imax

duty_cycles = list(np.linspace(0.10, 0.90, 10))
amplitudes = list(np.linspace(imin, imax-imin, 10))
cpu = [[CPU(10e-6, i, 100, j, imin) for i in duty_cycles] for j in amplitudes]
ll = list(np.linspace(10e-6, 0.8*rll, 6))
supplies = [Supply(rpdn, i, vmax, vmin, imax, 0) for i in ll]

energies = np.zeros((len(amplitudes), len(duty_cycles), len(ll)))
energies_o = np.zeros((len(amplitudes), len(duty_cycles)))
savings = np.zeros((len(amplitudes), len(duty_cycles), len(ll)))

supply_base = Supply(rpdn, rll, vmax, vmin, imax, 0)

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
plot_2D(amplitudes, duty_cycles, ll, savings, "R_pdn: "+str(rpdn)+"[Ohm]; Imax: "+str(imax)+"[A]; Vcc_max: "+str(vmax)+"[V]; Vcc_min: "+str(vmin)+"[V]", "", "")
#plot_line(list(lls, [100*(energy_original - e)/energy_original for e in energies], "Load Lines", "Rll (Ohms)", "%")
#plot_lines(list(lls, [100*(energy_original - e)/energy_original for e in energies], "Load Lines", "Rll (Ohms)", "%")
