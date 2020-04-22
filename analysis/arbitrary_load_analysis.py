import pandas as pd
import glob
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default="", help="input path where traces are located")
parser.add_argument('--headers', type=str, default="", help="the headers for the CSV")
args = parser.parse_args()

period = [20e-9, 100e-9, 200e-9, 1e-6, 2e-6, 10e-6, 20e-6, 100e-6]
slew_rate = list(np.arange(0.01, 0.3, 0.05))
amplitude = range(5, 95, 5)
duration=500e-6
timestep=1e-9
min_power = 5

"""3D Plots"""
# Slew Rate for different combinations of period, input_slew, and amplitude
max_supply_slew_rate = np.zeros((len(period), len(slew_rate), len(amplitude)))
supply_vpp = np.zeros((len(period), len(slew_rate), len(amplitude)))
supply_stabilization = np.zeros((len(period), len(slew_rate), len(amplitude)))
supply_cpp = np.zeros((len(period), len(slew_rate), len(amplitude)))
supply_phase_delay = np.zeros((len(period), len(slew_rate), len(amplitude)))

def get_files(path):
  return glob.glob(path+"/trace_*.csv")

def import_csv(file, headers):
  return pd.read_csv(file, header=None, names=headers)

def valid_combinations(files):
  keys = []
  for i in files:
    keys.append([int(i) for i in i.split(".")[0].split("/")[-1].split("_")[1:4]])
  return keys

def gen_sweep_space_scatter(axis_vals):
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter([math.log(i[0],10) for i in axis_vals], [i[1] for i in axis_vals], [i[2] for i in axis_vals], marker='o') 
  ax.set_xlabel('log(period) [s]')
  ax.set_ylabel('slew rate [A/ns]')
  ax.set_zlabel('amplitude [A]')
  plt.show()

def keys_to_vals(keys):
  vals = []
  for i in keys:
    vals.append([period[i[0]], slew_rate[i[1]], amplitude[i[2]]])
  return vals

path=args.input
headers=args.headers

files=get_files(path)
keys=valid_combinations(files)
axis_vals=keys_to_vals(keys)
gen_sweep_space_scatter(axis_vals)
