import pandas as pd
import glob
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import argparse

#------------------------------------------------------------------------------------------------
# Base Systems for Characterization:
# 5 Mechanism,  [none, decor, sensor, uarch, signature]
# 6 Benchmarks, [dijkstra, fft, ffti, qsort, sha, toast, untoast]
# 3 PDN/CPU,    [mobile, laptop, desktop]
#------------------------------------------------------------------------------------------------
mobile = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [],
  "IdealSensor" : [],
  "uArchEvent" :  [],
  "Signature" :   [],
  "T.a.S." :      [],
  "InstPending" : []
}

laptop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [],
  "IdealSensor" : [],
  "uArchEvent" :  [],
  "Signature" :   [],
  "T.a.S." :      [],
  "InstPending" : []
}

desktop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [],
  "IdealSensor" : [],
  "uArchEvent" :  [],
  "Signature" :   [],
  "T.a.S." :      [],
  "InstPending" : []
}
data = [mobile, laptop, desktop]
name = ["Mobile", "Laptop", "Desktop"]
tick_labels = ["DecorOnly", "IdealSensor", "uArchEvent", "Signature", "T.a.S.", "InstPending"]
benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
fname = ["num_ve_mobile.png", "num_ve_laptop.png", "num_ve_desktop.png"]
bounds = [[0.0,500.0,50.0],[0.0,600.0,50.0],[0.0,900.0,50.0]]
for k in range(len(data)):
  df=[data[k]["DecorOnly"],data[k]["IdealSensor"],data[k]["uArchEvent"],data[k]["Signature"],data[k]["T.a.S."],data[k]["InstPending"]]
  pos = list(range(len(df)))
  width = 0.125
  fig, ax = plt.subplots(figsize=(10,5))
  i=0
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="dijkstra", color="w", hatch="/"*1, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="fft", color="w", hatch="o"*2, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="ffti", color="w", hatch="X"*4, fill="False", linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="qsort", color="w", hatch="/"*4, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="sha", color="w", hatch="-"*4, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="toast", color="w", hatch='\\'*4, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="untoast", color="w", hatch="."*4, fill=True, linewidth=1, edgecolor="k")
  ax.set_ylabel('Num Voltage Emergencies')
  ax.set_title(name[k])
  ax.set_xticks([p + 1.5 * width for p in pos])
  ax.set_yticks(np.arange(bounds[k][0],bounds[k][1],bounds[k][2]))
  ax.set_ylim(bounds[k][0],bounds[k][1])
  ax.set_axisbelow(True)
  ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")
  ax.set_xticklabels(tick_labels)
  #plt.legend(benchmarks, loc='upper left')
  plt.legend(benchmarks, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
  plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
  plt.savefig(fname[k])
  plt.show()



#------------------------------------------------------------------------------------------------
# System w/throttle on restore from DeCoR:
# 6 Mechanism,  [decor, sensor, uarch, signature, T.a.S., InstPending]
# 6 Benchmarks, [dijkstra, fft, ffti, qsort, sha, toast, untoast]
# 3 PDN/CPU,    [mobile, laptop, desktop]
#------------------------------------------------------------------------------------------------
mobile = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [62.0,426.0,409.0,421.0,74.0,188.0,195.0],
  "IdealSensor" : [51.0,421.0,398.0,415.0,63.0,186.0,191.0],
  "uArchEvent" :  [51.0,427.0,395.0,399.0,50.0,174.0,192.0],
  "Signature" :   [53.0,428.0,400.0,427.0,64.0,171.0,195.0],
  "T.a.S." :      [65.0,422.0,395.0,368.0,71.0,157.0,197.0],
  "InstPending" : [72.0,431.0,418.0,402.0,67.0,185.0,194.0]
}

laptop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [587.0,535.0,512.0,410.0,411.0,383.0,490.0],
  "IdealSensor" : [296.0,113.0,101.0,388.0,110.0,214.0,33.0],
  "uArchEvent" :  [263.0,6.0,7.0,239.0,123.0,219.0,122.0],
  "Signature" :   [520.0,420.0,381.0,409.0,297.0,284.0,266.0],
  "T.a.S." :      [454.0,3.0,0.0,388.0,116.0,173.0,25.0],
  "InstPending" : [542.0,421.0,494.0,389.0,257.0,244.0,120.0]
}

desktop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [525.0,442.0,571.0,471.0,467.0,665.0,830.0],
  "IdealSensor" : [530.0,441.0,537.0,435.0,441.0,563.0,778.0],
  "uArchEvent" :  [531.0,438.0,536.0,444.0,448.0,577.0,806.0],
  "Signature" :   [524.0,572.0,532.0,529.0,459.0,616.0,824.0],
  "T.a.S." :      [526.0,444.0,559.0,438.0,445.0,592.0,820.0],
  "InstPending" : [524.0,441.0,541.0,486.0,461.0,578.0,802.0]
}
data = [mobile, laptop, desktop]
name = ["Mobile Throttle after Rollback", "Laptop Throttle after Rollback", "Desktop Throttle after Rollback"]
tick_labels = ["DecorOnly", "IdealSensor", "uArchEvent", "Signature", "T.a.S.", "InstPending"]
benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
fname = ["num_ve_mobile_tor.png", "num_ve_laptop_tor.png", "num_ve_desktop_tor.png"]
bounds = [[0.0,500.0,50.0],[0.0,600.0,50.0],[0.0,900.0,50.0]]
for k in range(len(data)):
  df=[data[k]["DecorOnly"],data[k]["IdealSensor"],data[k]["uArchEvent"],data[k]["Signature"],data[k]["T.a.S."],data[k]["InstPending"]]
  pos = list(range(len(df)))
  width = 0.125
  fig, ax = plt.subplots(figsize=(10,5))
  i=0
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="dijkstra", color="w", hatch="/"*1, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="fft", color="w", hatch="o"*2, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="ffti", color="w", hatch="X"*4, fill="False", linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="qsort", color="w", hatch="/"*4, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="sha", color="w", hatch="-"*4, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="toast", color="w", hatch='\\'*4, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="untoast", color="w", hatch="."*4, fill=True, linewidth=1, edgecolor="k")
  ax.set_ylabel('Num Voltage Emergencies')
  ax.set_title(name[k])
  ax.set_xticks([p + 1.5 * width for p in pos])
  ax.set_yticks(np.arange(bounds[k][0],bounds[k][1],bounds[k][2]))
  ax.set_ylim(bounds[k][0],bounds[k][1])
  ax.set_axisbelow(True)
  ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")
  ax.set_xticklabels(tick_labels)
  #plt.legend(benchmarks, loc='upper left')
  plt.legend(benchmarks, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
  plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
  plt.savefig(fname[k])
  plt.show()


#------------------------------------------------------------------------------------------------
# System w/throttle on restore from DeCoR and Harvard PDNs for each
# 6 Mechanism,  [decor, sensor, uarch, signature, T.a.S., InstPending]
# 6 Benchmarks, [dijkstra, fft, ffti, qsort, sha, toast, untoast]
# 3 PDN/CPU,    [mobile, laptop, desktop]
#------------------------------------------------------------------------------------------------
mobile = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [],
  "IdealSensor" : [],
  "uArchEvent" :  [],
  "Signature" :   [],
  "T.a.S." :      [],
  "InstPending" : []
}

laptop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [],
  "IdealSensor" : [],
  "uArchEvent" :  [],
  "Signature" :   [],
  "T.a.S." :      [],
  "InstPending" : []
}

desktop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [],
  "IdealSensor" : [],
  "uArchEvent" :  [],
  "Signature" :   [],
  "T.a.S." :      [],
  "InstPending" : []
}
data = [mobile, laptop, desktop]
name = ["Mobile+Harvard PDN Throttle after Rollback", "Laptop+Harvard PDN Throttle after Rollback", "Desktop+Harvard PDN Throttle after Rollback"]
tick_labels = ["DecorOnly", "IdealSensor", "uArchEvent", "Signature", "T.a.S.", "InstPending"]
benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
fname = ["num_ve_mobile_harvard_tor.png", "num_ve_laptop_harvard_tor.png", "num_ve_desktop_harvard_tor.png"]
bounds = [[0.0,500.0,50.0],[0.0,600.0,50.0],[0.0,900.0,50.0]]
for k in range(len(data)):
  df=[data[k]["DecorOnly"],data[k]["IdealSensor"],data[k]["uArchEvent"],data[k]["Signature"],data[k]["T.a.S."],data[k]["InstPending"]]
  pos = list(range(len(df)))
  width = 0.125
  fig, ax = plt.subplots(figsize=(10,5))
  i=0
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="dijkstra", color="w", hatch="/"*1, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="fft", color="w", hatch="o"*2, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="ffti", color="w", hatch="X"*4, fill="False", linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="qsort", color="w", hatch="/"*4, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="sha", color="w", hatch="-"*4, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="toast", color="w", hatch='\\'*4, fill=True, linewidth=1, edgecolor="k")
  i+=1
  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="untoast", color="w", hatch="."*4, fill=True, linewidth=1, edgecolor="k")
  ax.set_ylabel('Num Voltage Emergencies')
  ax.set_title(name[k])
  ax.set_xticks([p + 1.5 * width for p in pos])
  ax.set_yticks(np.arange(bounds[k][0],bounds[k][1],bounds[k][2]))
  ax.set_ylim(bounds[k][0],bounds[k][1])
  ax.set_axisbelow(True)
  ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")
  ax.set_xticklabels(tick_labels)
  #plt.legend(benchmarks, loc='upper left')
  plt.legend(benchmarks, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
  plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
  plt.savefig(fname[k])
  plt.show()