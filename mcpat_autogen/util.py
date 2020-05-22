# MIT License
#
# Copyright (c) 2020 Andrew Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# util.py
#
# Misc functions to handle I/O and building of the dictionaries

import os
import sys
import re
from file_read_backwards import FileReadBackwards
from functools import reduce

def build_gem5_stat_dict(file):
  """ Build a dict of stats from the Gem5 stats.txt """
  stats = {}
  with FileReadBackwards(file, encoding="utf-8") as sf:
    for line in sf:
      if line.strip() == "":
        continue
      elif "End Simulation Statistics" in line:
        stats = {}
      elif "Begin Simulation Statistics" in line:
        return stats
      else:
        stat = []
        sstr = re.sub('\s+', ' ', line).strip()
        if('-----' in sstr):
          continue
        elif(sstr == ''):
          continue
        elif(sstr.split(' ')[1] == '|'):
          # Ruby Stats
          l = []
          for i in sstr.split('|')[1:]:
            l.append(i.strip().split(' '))
          stat.append("ruby_multi")
          stat.append(l)
        else:
          stat.append("single")
          stat.append(sstr.split(' ')[1])
        stats[sstr.split(' ')[0]] = stat
  return stats

def build_gem5_config_dict(file):
  """ Build a dict of system parameters from the Gem5 config.ini """
  config = {}
  hierarchy = ""
  with open(file, "r") as cf:
    lines = cf.readlines()
    for line in lines:
      cstr = re.sub('\s+', ' ', line).strip()
      if(cstr == ''):
        continue
      if("[" in cstr and "]" in cstr):
        hierarchy=cstr.replace("[", "").replace("]", "")+"."
        continue
      else:
        #print(hierarchy, cstr)
        config[hierarchy+cstr.split('=')[0]] = cstr.split('=')[1].strip()
  return config

def build_gem5_sim_dict(**kwargs):
  """ Build a sim_dict of parameters & stats coming directly from the runtime,
  such as instantaneous voltage, and temperature of the device"""
  sim_dict = {}
  for key, val in kwargs.items():
    sim_dict[key] = val
  return sim_dict

def prune_dict(path, d):
  """ Returns a new dictionary of all the items on the specified path """
  new = {}
  for key, val in d.items():
    if path in key:
      new[key.replace(path, "")]=val
    if "system.clk_domain.clock" in key:
      new[key.replace("system.clk_domain.","")]=val
  return new

def get_noc_dimensions(nc):
  def factors(n):
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
  def build_pairs(n, l):
    f_pairs = []
    for i in range(len(l)):
      for j in range(len(l)):
        if l[i]*l[j] == n:
          f_pairs.append([l[i], l[j]])
    return f_pairs
  f = build_pairs(nc,list(factors(nc)))
  min_sum = 100000
  min_x = 0
  min_y = 0
  for elem in f:
    if(sum(elem) < min_sum):
      min_sum = sum(elem)
      min_x = elem[0]
      min_y = elem[1]
  return min_x, min_y

