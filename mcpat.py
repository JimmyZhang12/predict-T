import os
import sys
import re
import subprocess
import tempfile
import math
from collections import defaultdict
from contextlib import contextmanager

import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt

# McPat Global Paths:
mcpat_path = "mcpat"
mcpat_exe = mcpat_path+"/mcpat"

class Device(object):
  def __init__(self, name="", data={}, depth=0):
    self.name = name
    self.data = data
    self.depth = depth
  def __str__(self):
    return "  "*self.depth+self.name+" "+str(self.data)
  def __repr__(self):
    return "  "*self.depth+self.name+" "+str(self.data)

class Node(object):
  def __init__(self, children=[], device=None):
    self.children = children
    self.device = device
  def __str__(self):
    modules = []
    modules.append(str(self.device))
    for child in self.children:
      modules.append(str(child))
    return "\n".join(modules)
  def __repr__(self):
    modules = []
    modules.append(str(self.device))
    for child in self.children:
      modules.append(str(child))
    return "\n".join(modules)

class Epoch(object):
  def __init__(self, device_list = []):
    if len(device_list) != 0:
      self.dev_tree = self.build(device_list)
    else:
      self.dev_tree = None
  def __str__(self):
    return str(self.dev_tree)
  def __repr__(self):
    return str(self.dev_tree)

  def build(self, devices):
    """ Base Cases """
    if len(devices) == 0:
      return None
    if len(devices) == 1 and isinstance(devices[0], Device):
      return Node([], devices[0])

    """ Recursive Case """
    root = devices[0]
    children = []
    sublist = []
    for dev in devices[1:]:
      if dev.depth == root.depth + 1:
        node = self.build(sublist)
        if node != None:
          children.append(node)
          #print(node)
        sublist = []
      sublist.append(dev)
    node = self.build(sublist)
    if node != None:
      children.append(node)

    """ Post-Order Build Tree: """
    return Node(children, root)

  def find(self, path):
    def _find(path, subtree):
      #print(path, subtree.device.name)

      """ Base Case """
      if path.split(":")[0] == subtree.device.name and len(path.split(":")) == 1:
        return subtree.device
      elif len(path.split(":")) == 1:
        return None

      """ Recursive Case """
      for i in subtree.children:
        if i.device.name == path.split(":")[1]:
          return _find(":".join(path.split(":")[1:]), i)
      return None

    return _find(path, self.dev_tree)



def parse_output(output_file):
  def strip_header(lines):
    start = False
    ret = []
    for line in lines:
      if("Processor:" in line):
        start = True
      if start:
        ret.append(line)
    return ret

  def strip_space(lines):
    ret = []
    last_line_star = False
    start_core = False
    for line in lines:
      if "Core:" in line:
        start_core = True
        if last_line_star:
          #Fix spacing after ******
          ret.append("  "+line)
          last_line_star = False
      elif "*****" in line:
        last_line_star = True
      elif "Device Type=" in line or "     Local Predictor:" in line:
        continue
      else:
        if last_line_star:
          #Fix spacing after ******
          ret.append("  "+line)
          last_line_star = False
        elif start_core:
          ret.append(line.replace(" ", "", 2))
        else:
          ret.append(line)
    return ret

  def line_to_dict(line):
    ret = {}
    temp = line.split(":")[0].split("=")
    ret["lspace"] = len(temp[0]) - len(temp[0].lstrip())
    return ret

  def split_list(lines):
    ret = []
    sub = []
    for i in lines:
      if i == "\n":
        ret.append(sub)
        sub = []
      else:
        sub.append(i.rstrip())
    return ret

  def to_devices(intermediate_dev_list):
    ret = []
    for dev in intermediate_dev_list:
      data = {}
      #print(dev)
      for attr in dev[1:]:
        data[attr.split("=")[0].strip()] = attr.split("=")[1].strip()
      ret.append(Device(dev[0].split(":")[0].strip(), data, int(math.floor((len(dev[0]) - len(dev[0].lstrip()))/2))))
      if ret[-1].depth == 4:
        ret[-1].depth = 3
      if ret[-1].depth == 5:
        ret[-1].depth = 3
      if ret[-1].depth == 6:
        ret[-1].depth = 4
    return ret

  """ Returns an Epochs """
  with open(output_file, "r") as of:
    lines = of.readlines()
    lines = strip_header(lines)
    lines = strip_space(lines)
    temp = split_list(lines)
    dev_list = to_devices(temp)
    epoch = Epoch(dev_list)
    return epoch

def run_mcpat(xml, print_level, opt_for_clk, ofile, errfile):
  global mcpat_path
  global mcpat_exe
  mcpat = [mcpat_exe,
    "-infile",
    xml,
    "-print_level",
    print_level,
    "-opt_for_clk",
    opt_for_clk]
  print(" ".join(mcpat))
  with open(ofile, "w") as ostd, open(errfile, "w") as oerr:
    p = subprocess.Popen(mcpat, stdout=ostd, stderr=oerr)
    p.wait()

def plot(epochs):
  def get_data(epochs, path):
    data = defaultdict(list)
    for epoch in epochs:
      for key, value in epoch.find(path).data.items():
        data[key].append(value)
    return data


  def plot_components_line(components):
    def format_values(data):
      """ Convert the data elements to their values """
      for key, value in data.items():
        for i in range(len(value)):
          data[key][i] = float(value[i].strip().split()[0])
      return data

    def create_data_frame(data):
      total = []
      for i in range(len(data.itervalues().next())):
        sum = 0
        for key, value in data.items():
          if key != "Area":
            sum += value[i]
        total.append(sum)
      return total
    """ Plot a component dict as a line chart """

  components1 = {}
  proc_totals = get_data(epochs, "Processor")
  components1["Processor:Core"] = get_data(epochs, "Processor:Core")
  components1["Processor:L2"] = get_data(epochs, "Processor:L2")
  components1["Processor:Memory Controller"] = get_data(epochs, "Processor:Memory Controller")
  components1["Processor:NOC"] = get_data(epochs, "Processor:NOC")

  print(components1)

#Test Code:
#run_mcpat("mcpat_arm.xml", "5", "1", "mcpat.out", "mcpat.err")
#epoch = parse_output("mcpat.out")
#print(epoch.find("Processor:Total Cores"))
#print(epoch.find("Processor:Core:Instruction Fetch Unit:Branch Target Buffer"))
#print(epoch.find("Processor:NOC:Router:Arbiter"))
