import os
import sys
import re
import subprocess
import tempfile
import math

peak_power = 5
min_power = 0.5
timestep = 100e-9
time = 0

power = min_power

on_time = [10e-6, 100e-6, 1000e-6]
off_time = [10e-6, 100e-6, 1000e-6]

rise_time = 1000e-9
fall_time = 1000e-9
start_time = 0
rise_flag = 0
fall_flag = 0

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
    power = min_power + delta*math.sin((math.pi/2)*dt/rise_time)
    if(dt >= rise_time):
      rise_flag = 0
  if(fall_flag == 1):
    power = peak_power - delta*math.sin((math.pi/2)*dt/fall_time)
    if(dt >= fall_time):
      fall_flag = 0

def calc_req(power, voltage):
  return voltage*voltage/power

for i in range(len(on_time)):
  for j in range(len(off_time)):
    with open("dummy_load/test_load_"+str(i)+"_"+str(j)+".csv", "w") as of:
      time = 0
      period_count = 0
      while(period_count < 20):
        # Start with off:
        t1 = time
        decrease_power()
        while(time < t1 + off_time[j]):
          calculate_power()
          res = calc_req(power, 1.0)
          of.write(",".join([str(time),str(res),str(power)])+"\n")
          time += timestep
        t1 = time
        increase_power()
        while(time < t1 + on_time[i]):
          calculate_power()
          res = calc_req(power, 1.0)
          of.write(",".join([str(time),str(res),str(power)])+"\n")
          time += timestep
        period_count+=1
