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
# 7 Benchmarks, [dijkstra, fft, ffti, qsort, sha, toast, untoast]
# 3 PDN/CPU,    [mobile, laptop, desktop]
#------------------------------------------------------------------------------------------------
mobile = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "None" :        [184.0,1835.0,1692.0,2559.0,205.0,505.0,836.0],
	"DecorOnly" :   [1,1,1,1,1,1,1],
  "IdealSensor" : [1,1,1,1,1,1,1],
  "uArchEvent" :  [1,1,1,1,1,1,1],
  "Signature" :   [1,1,1,1,1,1,1],
  "T.a.S." :      [1,1,1,1,1,1,1],
  "InstPending" : [1,1,1,1,1,1,1]
}

laptop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "None" :        [190.0,211.0,192.0,402.0,96.0,93.0,116.0],
	"DecorOnly" :   [1,1,1,1,1,1,1],
  "IdealSensor" : [1,1,1,1,1,1,1],
  "uArchEvent" :  [1,1,1,1,1,1,1],
  "Signature" :   [1,1,1,1,1,1,1],
  "T.a.S." :      [1,1,1,1,1,1,1],
  "InstPending" : [1,1,1,1,1,1,1]
}

desktop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "None" :        [152.0,425.0,402.0,426.0,98.0,170.0,354.0],
	"DecorOnly" :   [1,1,1,1,1,1,1],
  "IdealSensor" : [1,1,1,1,1,1,1],
  "uArchEvent" :  [1,1,1,1,1,1,1],
  "Signature" :   [1,1,1,1,1,1,1],
  "T.a.S." :      [1,1,1,1,1,1,1],
  "InstPending" : [1,1,1,1,1,1,1]
}
data = [mobile, laptop, desktop]
name = ["Mobile", "Laptop", "Desktop"]
tick_labels = ["None","DecorOnly", "IdealSensor", "uArchEvent", "Signature"]
benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
fname = ["num_ve_mobile.png", "num_ve_laptop.png", "num_ve_desktop.png"]
bounds = [[0.0,500.0,50.0],[0.0,600.0,50.0],[0.0,900.0,50.0]]
for k in range(len(data)):
  df=[data[k]["None"],data[k]["DecorOnly"],data[k]["IdealSensor"],data[k]["uArchEvent"],data[k]["Signature"]]
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

# Rates for the Base Systems
mobile_rates = [0.002940675076713263,0.011792048667637736,0.011332785596913626,0.016934459209063477,0.004644173261644415,0.005748391209324915,0.006546115136455702]
laptop_rates = [0.006774653626731867,0.0017261125654450262,0.0016601118599181804,0.0030666957279860503,0.002850162866449512,0.0015421278047301396,0.0014625781722816219]
desktop_rates = [0.007362914163921721,0.003803540424922587,0.003782959742532889,0.0034736945105841677,0.003495007132667618,0.0033371284990773823,0.004956594791374965]
avg_rates = [0.008562664022536162, 0.0027260632319346285, 0.004315977037868761]
avg_rates_s = [1e3*i for i in avg_rates]
bars = np.arange(len(avg_rates_s))
fig, ax = plt.subplots(figsize=(5,5))
plt.bar(bars, avg_rates_s, color="w", hatch="/"*4, fill=True, linewidth=1, edgecolor="k")
ax.set_xticks(bars)
ax.set_xticklabels(['Mobile', 'Laptop', 'Desktop'])
ax.set_ylabel('Rate (VE/us)')
ax.set_title("Voltage Emergency Rate")
ax.set_yticks(np.arange(0.0,10.0,1.0))
ax.set_ylim(0.0,10.0)
ax.set_axisbelow(True)
ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")
plt.savefig("ve_rates_none.png")
plt.show()






#------------------------------------------------------------------------------------------------
# System w/throttle on restore from DeCoR:
# 6 Mechanism,  [decor, sensor, uarch, signature, T.a.S., InstPending]
# 7 Benchmarks, [dijkstra, fft, ffti, qsort, sha, toast, untoast]
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
# 7 Benchmarks, [dijkstra, fft, ffti, qsort, sha, toast, untoast]
# 3 PDN/CPU,    [mobile, laptop, desktop]
#------------------------------------------------------------------------------------------------
mobile = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [0,0,0,0,0,86.0,83.0],
  "IdealSensor" : [0,0,0,0,0,110.0,125.0],
  "uArchEvent" :  [0,0,0,0,0,78.0,75.0],
  "Signature" :   [0,0,0,0,0,84.0,81.0],
  "T.a.S." :      [0,0,0,0,0,76.0,56.0],
  "InstPending" : [0,0,0,0,0,101.0,90.0]
}

laptop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [0,0,0,0,0,47.0,20.0],
  "IdealSensor" : [0,0,0,0,0,158.0,86.0],
  "uArchEvent" :  [0,0,0,0,0,76.0,21.0],
  "Signature" :   [0,0,0,0,0,42.0,33.0],
  "T.a.S." :      [0,0,0,0,0,16.0,9.0],
  "InstPending" : [0,0,0,0,0,71.0,14.0]
}

desktop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [60.0,200.0,186.0,393.0,84.0,103.0,28.0],
  "IdealSensor" : [110.0,209.0,199.0,398.0,81.0,110.0,49.0],
  "uArchEvent" :  [103.0,9.0,6.0,4.0,46.0,84.0,27.0],
  "Signature" :   [171.0,201.0,189.0,394.0,86.0,100.0,22.0],
  "T.a.S." :      [0.0,7.0,1.0,1.0,42.0,81.0,7.0],
  "InstPending" : [0.0,116.0,12.0,1.0,75.0,88.0,9.0]
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

# Rates:
for k in range(len(data)):
  df=[data[k]["None"],data[k]["DecorOnly"],data[k]["IdealSensor"],data[k]["uArchEvent"],data[k]["Signature"]]
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
