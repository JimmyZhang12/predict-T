import os
import sys
import re
import subprocess
import tempfile
import math
from collections import defaultdict
from contextlib import contextmanager
import pickle

from mcpat import *

benchmark = sys.argv[1]
cycles_per_epoch = sys.argv[2]
freq = sys.argv[3]

#Runtime Dynamic,Total Leakage,Area,Peak Dynamic,Peak Power,Gate Leakage,Subthreshold Leakage,Subthreshold Leakage with power gating

def calc_total_power(data):
  # Add Runtime Dynamic to Gate Leakage and Subthreshold Leakage with Power Gating
  return float(data[0]) + float(data[7]) + float(data[5])

def calc_req(power, voltage):
  return voltage*voltage/power

sfile = os.path.join("./mcpat_out/"+benchmark, benchmark+".pickle")
cfile = os.path.join("./mcpat_out/"+benchmark, benchmark+".csv")
with open(sfile, "r") as mpe:
  epochs = pickle.load(mpe)

with open(cfile, "w") as csv:
  i = 0
  for epoch in epochs:
    # Get the data for the processor (Root of tree):
    data_line = []
    header = []
    for key, value in epoch.find("Processor").data.items():
      header.append(key)
      data_line.append(value.split(" ")[0])

    # Calculate Total Power:
    power = calc_total_power(data_line)
    data = []
    #data.append(str(power))
    #header.append("Total Power")
    req = calc_req(power, 1.0)
    data.append(str(i*float(cycles_per_epoch)/float(freq)))
    data.append(str(req))
    #header.append("Req")
    csv.write(",".join(data)+"\n")
    print(",".join(data))
    i+=1
