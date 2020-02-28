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

def print_to_csv(epochs, fname):
  with open(fname, "w") as ocsv:
    for epoch in epochs:
      # Get the data for the processor (Root of tree):
      data_line = []
      for key, value in epoch.find("Processor").data.items():
        data_line.append(value)
      ocsv.write(",".join(data_line)+"\n")


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
  #print(" ".join(mcpat))
  with open(ofile, "w") as ostd, open(errfile, "w") as oerr:
    p = subprocess.Popen(mcpat, stdout=ostd, stderr=oerr)
    p.wait()

def plot(epochs, testname, path):
  def get_data(epochs, path):
    data = defaultdict(list)
    for epoch in epochs:
      for key, value in epoch.find(path).data.items():
        data[key].append(value)
    return data


  def plot_components_line(components, title, fname):
    def format_values(data):
      """ Convert the data elements to their values """
      for key, value in data.items():
        for i in range(len(value)):
          data[key][i] = float(value[i].strip().split()[0])
      return data

    def total(data):
      total = []
      for i in range(len(data.itervalues().next())):
        sum = 0
        for key, value in data.items():
          if key == "Runtime Dynamic" or key == "Gate Leakage" or key == "Subthreshold Leakage with power gating":
            sum += value[i]
        total.append(sum)
      return total

    fig, plts = plt.subplots(len(components), 1)

    plt.subplots_adjust(hspace=0.35)
    fig.set_size_inches(20, 20)

    """ Plot a component dict as a line chart """
    i = 0
    for key, value in components.items():
      data = format_values(value)
      data = total(data)
      plts[i].plot(range(len(data)), data, label=key.split(":")[-1])
      plts[i].set_xlabel("Epoch")
      plts[i].set_ylabel("Power (W)")
      plts[i].ticklabel_format(useOffset=False)
      #plts[i].set_title(key.split(":")[1]+" Power")
      print(data)
      plts[i].legend()
      i+=1
    fig.suptitle(title)
    #plt.show()
    plt.savefig(fname)

  def plot_components_hierarchy(components, title, fname):
    def format_values(data):
      """ Convert the data elements to their values """
      for key, value in data.items():
        for i in range(len(value)):
          data[key][i] = float(value[i].strip().split()[0])
      return data

    def total(data):
      total = []
      for i in range(len(data.itervalues().next())):
        sum = 0
        for key, value in data.items():
          if key == "Runtime Dynamic" or key == "Gate Leakage" or key == "Subthreshold Leakage with power gating":
            sum += value[i]
        total.append(sum)
      return total

    fig, plts = plt.subplots(len(components), 1)
    plt.subplots_adjust(hspace=0.25)
    fig.set_size_inches(10, 20, dpi=300)

    """ Plot a component dict as a line chart """
    i = 0
    for key, value in components.items():
      for unit, d, in value.items():
        data = format_values(d)
        data = total(data)
        plts[i].plot(range(len(data)), data, label=unit.split(":")[-1])
      plts[i].set_title(key.split(":")[1]+" Power")
      plts[i].set_xlabel("Epoch)")
      plts[i].set_ylabel("Power (W)")
      plts[i].legend()
      i+=1
    plt.savefig(fname)


  components1 = {}
  proc_totals = get_data(epochs, "Processor")
  components1["Processor:Core"] = get_data(epochs, "Processor:Core:Load Store Unit")
  components1["Processor:L2"] = get_data(epochs, "Processor:L2")
  components1["Processor:Memory Controller"] = get_data(epochs, "Processor:Memory Controller")
  components1["Processor:NOC"] = get_data(epochs, "Processor:NOC")
  plot_components_line(components1, "Processor", os.path.join(path, testname+"_processor.png"))

  componentC = {"Processor:Core:Instruction Fetch Unit": get_data(epochs, "Processor:Core:Instruction Fetch Unit"),
                "Processor:Core:Renaming Unit": get_data(epochs, "Processor:Core:Renaming Unit"),
                "Processor:Core:Load Store Unit": get_data(epochs, "Processor:Core:Load Store Unit"),
                "Processor:Core:Memory Management Unit": get_data(epochs, "Processor:Core:Memory Management Unit"),
                "Processor:Core:Execution Unit:Register Files": get_data(epochs, "Processor:Core:Execution Unit:Register Files"),
                "Processor:Core:Execution Unit:Instruction Scheduler": get_data(epochs, "Processor:Core:Execution Unit:Instruction Scheduler"),
                "Processor:Core:Execution Unit:Integer ALUs (Count": get_data(epochs, "Processor:Core:Execution Unit:Integer ALUs (Count"),
                "Processor:Core:Execution Unit:Floating Point Units (FPUs) (Count": get_data(epochs, "Processor:Core:Execution Unit:Floating Point Units (FPUs) (Count")}
  componentMC={"Processor:Memory Controller:Front End Engine": get_data(epochs, "Processor:Memory Controller:Front End Engine"),
               "Processor:Memory Controller:Transaction Engine": get_data(epochs, "Processor:Memory Controller:Transaction Engine"),
               "Processor:Memory Controller:PHY": get_data(epochs, "Processor:Memory Controller:PHY")}
  componentNOC={"Processor:NOC:Router": get_data(epochs, "Processor:NOC:Router"),
                "Processor:NOC:Router:Virtual Channel Buffer": get_data(epochs, "Processor:NOC:Router:Virtual Channel Buffer"),
                "Processor:NOC:Router:Crossbar": get_data(epochs, "Processor:NOC:Router:Crossbar"),
                "Processor:NOC:Router:Arbiter": get_data(epochs, "Processor:NOC:Router:Arbiter"),
                "Processor:NOC:Per Router Links": get_data(epochs, "Processor:NOC:Per Router Links")}
  plot_components_line(componentC, "Core", os.path.join(path,testname+"_core.png"))
  plot_components_line(componentMC, "Memory Controller", os.path.join(path, testname+"_mc.png"))
  plot_components_line(componentNOC, "NOC", os.path.join(path,testname+"_noc.png"))

#Test Code:
#run_mcpat("mcpat_arm.xml", "5", "1", "mcpat.out", "mcpat.err")
#epoch = parse_output("mcpat.out")
#print(epoch.find("Processor:Total Cores"))
#print(epoch.find("Processor:Core:Instruction Fetch Unit:Branch Target Buffer"))
#print(epoch.find("Processor:NOC:Router:Arbiter"))
