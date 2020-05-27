import matplotlib.pyplot as plt
import numpy as mp
import math
import statistics
import pickle

from mcpat import *

def get_data(epochs, path):
  data = defaultdict(list)
  for epoch in epochs:
    for key, value in epoch.find(path).data.items():
      data[key].append(value)
  return data

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

def calculate_deltas(app_epochs):
  deltas = []
  data = get_data(epochs, "Processor")
  data = format_values(data)
  totals = total(data)
  print(statistics.mean(totals), statistics.stdev(totals))


mcpat_output_path = "mcpat_out/dijkstra_large"
testname = "dijkstra_large"
sfile = os.path.join(mcpat_output_path, testname+".pickle")

with open(sfile, "r") as mpe:
  epochs = pickle.load(mpe)

calculate_deltas(epochs)
