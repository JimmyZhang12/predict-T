import os
import sys
import re
import subprocess
import tempfile
import math
import argparse

rise_flag = 0
fall_flag = 0

parser = argparse.ArgumentParser()
parser.add_argument('--peak-power', type=str, default="5", help="Peak Power")
parser.add_argument('--min-power', type=str, default="0.5", help="Min Power")
parser.add_argument('--on-time', type=str, default="100e-9", help="")
parser.add_argument('--off-time', type=str, default="100e-9", help="")
parser.add_argument('--rise-time', type=str, default="10e-9", help="")
parser.add_argument('--fall-time', type=str, default="10e-9", help="")
parser.add_argument('--rise-function', type=str, default="sin", help="")
parser.add_argument('--fall-function', type=str, default="sin", help="")
parser.add_argument('--timescale', type=str, default="1e-9", help="Smallest time unit")
parser.add_argument('--periods', type=int, default=10, help="Periods to run")

args = parser.parse_args()

peak_power = float(args.peak_power)
min_power = float(args.min_power)
timestep = float(args.timescale)
time = 0

power = min_power

on_time = float(args.on_time)
off_time = float(args.off_time)

rise_time = float(args.rise_time)
fall_time = float(args.fall_time)
start_time = 0


def increase_power():
  global start_time
  global rise_flag
  if(rise_flag == 0):
    rise_flag = 1
    start_time = time

def decrease_power():
  global start_time
  global fall_flag
  if(fall_flag == 0):
    fall_flag = 1
    start_time = time

def calculate_power():
  global power
  global rise_flag
  global fall_flag
  delta = peak_power - min_power
  dt = time - start_time
  if(rise_flag == 1):
    print(start_time, dt/rise_time, delta)
    if(args.rise_function == "sin"):
      power = min_power + delta*(math.sin((math.pi)*dt/rise_time-math.pi/2)+1)/2
    elif(args.rise_function == "exp"):
      power = min_power + delta*(math.exp(dt/rise_time)-1)/(math.e-1)
    else:
      power = min_power + delta*dt/rise_time
    if(dt >= rise_time):
      rise_flag = 0
  if(fall_flag == 1):
    if(args.fall_function == "sin"):
      power = peak_power - delta*(math.sin((math.pi)*dt/fall_time-math.pi/2)+1)/2
    elif(args.fall_function == "exp"):
      power = peak_power - delta*(math.exp(dt/rise_time)-1)/(math.e-1)
    else:
      power = peak_power - delta*dt/fall_time
    if(dt >= fall_time):
      fall_flag = 0

def calc_req(power, voltage):
  return voltage*voltage/power

with open("test_load.csv", "w") as of:
  time = 0
  period_count = 0
  while(period_count < args.periods):
    # Start with off:
    t1 = time
    decrease_power()
    while(time < t1 + off_time):
      calculate_power()
      res = calc_req(power, 1.0)
      of.write(",".join([str(time),str(res),str(power)])+"\n")
      time += timestep
    t1 = time
    increase_power()
    while(time < t1 + on_time):
      calculate_power()
      res = calc_req(power, 1.0)
      of.write(",".join([str(time),str(res),str(power)])+"\n")
      time += timestep
    period_count+=1
