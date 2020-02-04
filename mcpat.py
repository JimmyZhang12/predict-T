import os
import sys
import re
import subprocess
import tempfile
import math
from contextlib import contextmanager

# McPat Global Paths:
mcpat_path = "mcpat"
mcpat_exe = mcpat_path+"/mcpat"

class Device(object):
  def __init__(self, name="", data={}, depth=0):
    self.name = name
    self.data = data
    self.depth = depth
  def __str__(self):
    return self.name+" "+str(self.data)+" "+str(self.depth)
  def __repr__(self):
    return self.name+" "+str(self.data)+" "+str(self.depth)

class Node(object):
  def __init__(self, children=[], device=None):
    self.children = children
    self.device = device
  def __str__(self):
    return str(self.device)+" "+str(self.children)
  def __repr__(self):
    return str(self.device)+" "+str(self.children)

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
      sublist.append(dev)
      if dev.depth == root.depth + 1:
        #print(sublist)
        children.append(self.build(sublist))
        #print(children)
        sublist = []

    """ Post-Order Build Tree: """
    return Node(children, root)

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
  for line in lines:
    if "*****" in line or "Device Type=" in line:
      continue
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
    for attr in dev[1:]:
      data[attr.split("=")[0].strip()] = attr.split("=")[1].strip()
    ret.append(Device(dev[0].split(":")[0].strip(), data, math.floor((len(dev[0]) - len(dev[0].lstrip()))/2)))
  return ret





""" Returns an array of Epochs """
def parse_output(output_file):
  with open(output_file, "r") as of:
    lines = of.readlines()
    lines = strip_header(lines)
    lines = strip_space(lines)
    temp = split_list(lines)
    dev_list = to_devices(temp)
    for dev in dev_list:
      print(dev)
    print("\n")
    epoch = Epoch(dev_list)
    print("\n")
    print(epoch)

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

#Test Code:
#run_mcpat("mcpat_arm.xml", "0", "1", "mcpat.out", "mcpat.err")
parse_output("mcpat.out")
