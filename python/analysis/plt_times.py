import pandas as pd
import glob
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import argparse

raw_data_mobile_tos = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [28098,67612,62139,67636,20724,40895,52236],
  "IdealSensor" : [28514,66632,63939,68171,19947,42651,54294],
  "uArchEvent" :  [32041,68891,65767,70439,23166,43036,56343],
  "Signature" :   [29793,66790,64205,67635,19823,41566,52882],
  "T.a.S." :      [40470,67396,63857,66647,25576,44067,63489],
  "InstPending" : [32003,65364,60882,68886,22917,45615,54567]
}

raw_data_mobile_tos_standard = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [23465,58356,55989,57956,18315,1,1],
  "IdealSensor" : [25470,58356,55989,60857,18315,1,1],
  "uArchEvent" :  [23465,58356,55989,62088,18452,1,1],
  "Signature" :   [23539,58834,55450,58273,18309,1,1],
  "T.a.S." :      [35515,58643,56262,63405,24579,1,1],
  "InstPending" : [26117,58361,56126,62657,21777,1,1]
}

raw_data_laptop_tos = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [70445,65184,62909,62385,54590,62252,82334],
  "IdealSensor" : [44243,56213,52974,63043,27914,49397,41887],
  "uArchEvent" :  [40433,53999,51468,64540,29108,50093,47674],
  "Signature" :   [63819,60527,57595,62340,43048,53177,61285],
  "T.a.S." :      [59462,53868,50729,63739,29195,46762,43347],
  "InstPending" : [67375,60215,63580,64120,40961,53401,51883]
}

raw_data_laptop_tos_standard = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [12491,53481,50600,57762,15462,1,1],
  "IdealSensor" : [19157,53604,50600,57762,20680,1,1],
  "uArchEvent" :  [12899,53481,50600,57762,16263,1,1],
  "Signature" :   [12289,53593,49958,57593,15443,1,1],
  "T.a.S." :      [19093,53746,50729,64126,19331,1,1],
  "InstPending" : [16810,53608,50727,59512,21247,1,1]
}

raw_data_desktop_tos = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [15520,57650,55070,61485,21185,1,1],
  "IdealSensor" : [22163,57918,55622,62625,22357,1,1],
  "uArchEvent" :  [21050,56276,53668,67881,18891,1,1],
  "Signature" :   [27095,58104,54685,61782,21687,1,1],
  "T.a.S." :      [14870,56012,53404,68220,21883,1,1],
  "InstPending" : [13947,57122,53535,63290,23935,1,1]
}

raw_data_desktop_standard = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [15520,57650,55070,61485,21185,1,1],
  "IdealSensor" : [22163,57918,55622,62625,22357,1,1],
  "uArchEvent" :  [21050,56276,53668,67881,18891,1,1],
  "Signature" :   [27095,58104,54685,61782,21687,1,1],
  "T.a.S." :      [14870,56012,53404,68220,21883,1,1],
  "InstPending" : [13947,57122,53535,63290,23935,1,1]
}

#------------------------------------------------------------------------------------------------
# Base Systems for Characterization:
# 4 Mechanism,  [decor, sensor, uarch, signature]
# 7 Benchmarks, [dijkstra, fft, ffti, qsort, sha, toast, untoast]
# 3 PDN/CPU,    [mobile, laptop, desktop]
#------------------------------------------------------------------------------------------------
mobile = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [30698,59109,23523,67372,1,23073,22941],
  "IdealSensor" : [33944,65493,62643,66770,1,40871,24623],
  "uArchEvent" :  [31973,63322,23706,68689,1,23248,18729],
  "Signature" :   [30765,62660,23571,67223,1,22892,17871],
  "T.a.S." :      [1,1,1,1,1,1,1],
  "InstPending" : [1,1,1,1,1,1,1]
}

laptop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [71237,68759,19351,58794,1,120282,20624],
  "IdealSensor" : [68085,56412,53436,63161,1,53859,19636],
  "uArchEvent" :  [32163,51468,19201,64172,1,19929,10803],
  "Signature" :   [65333,57012,19672,58778,1,20086,10341],
  "T.a.S." :      [1,1,1,1,1,1,1],
  "InstPending" : [1,1,1,1,1,1,1]
}

desktop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [58023,62402,22826,68575,1,23706,24211],
  "IdealSensor" : [61854,68579,64148,76647,1,80525,26825],
  "uArchEvent" :  [57656,63043,22891,70047,1,24311,9960],
  "Signature" :   [58512,62865,22916,68764,1,19180,8250],
  "T.a.S." :      [1,1,1,1,1,1,1],
  "InstPending" : [1,1,1,1,1,1,1]
}

speedup_mobile = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(mobile["DecorOnly"],mobile["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(mobile["IdealSensor"],mobile["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(mobile["uArchEvent"],mobile["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(mobile["Signature"],mobile["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(mobile["T.a.S."],mobile["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(mobile["InstPending"],mobile["DecorOnly"])]
}

speedup_laptop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(laptop["DecorOnly"],laptop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(laptop["IdealSensor"],laptop["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(laptop["uArchEvent"],laptop["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(laptop["Signature"],laptop["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(laptop["T.a.S."],laptop["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(laptop["InstPending"],laptop["DecorOnly"])]
}

speedup_desktop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(desktop["DecorOnly"],desktop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(desktop["IdealSensor"],desktop["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(desktop["uArchEvent"],desktop["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(desktop["Signature"],desktop["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(desktop["T.a.S."],desktop["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(desktop["InstPending"],desktop["DecorOnly"])]
}
data = [speedup_mobile, speedup_laptop, speedup_desktop]
name = ["Mobile", "Laptop", "Desktop"]
tick_labels = ["DecorOnly", "IdealSensor", "uArchEvent", "Signature"]
benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
fname = ["speedup_mobile.png", "speedup_laptop.png", "speedup_desktop.png"]
bounds = [[0.0,3.0,0.1],[0.0,3.0,0.1],[0.0,3.0,0.1]]
for k in range(len(data)):
  df=[data[k]["DecorOnly"],data[k]["IdealSensor"],data[k]["uArchEvent"],data[k]["Signature"]]
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
  ax.set_ylabel('Speedup (X)')
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
	"DecorOnly" :   [28098,67612,62139,67636,20724,40895,52236],
  "IdealSensor" : [28514,66632,63939,68171,19947,42651,54294],
  "uArchEvent" :  [32041,68891,65767,70439,23166,43036,56343],
  "Signature" :   [29793,66790,64205,67635,19823,41566,52882],
  "T.a.S." :      [40470,67396,63857,66647,25576,44067,63489],
  "InstPending" : [32003,65364,60882,68886,22917,45615,54567]
}

laptop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [70445,65184,62909,62385,54590,62252,82334],
  "IdealSensor" : [44243,56213,52974,63043,27914,49397,41887],
  "uArchEvent" :  [40433,53999,51468,64540,29108,50093,47674],
  "Signature" :   [63819,60527,57595,62340,43048,53177,61285],
  "T.a.S." :      [59462,53868,50729,63739,29195,46762,43347],
  "InstPending" : [67375,60215,63580,64120,40961,53401,51883]
}

desktop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [60137,61940,63114,70465,54424,77832,105528],
  "IdealSensor" : [61576,68604,64093,77183,56344,80881,111091],
  "uArchEvent" :  [61624,63859,63581,70383,54852,75369,107261],
  "Signature" :   [60594,67262,62996,72555,55553,77343,106184],
  "T.a.S." :      [60265,64140,63860,69893,54406,79301,108210],
  "InstPending" : [60049,62074,63189,71477,55950,76971,108127]
}
speedup_mobile = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(mobile["DecorOnly"],mobile["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(mobile["IdealSensor"],mobile["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(mobile["uArchEvent"],mobile["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(mobile["Signature"],mobile["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(mobile["T.a.S."],mobile["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(mobile["InstPending"],mobile["DecorOnly"])]
}

speedup_laptop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(laptop["DecorOnly"],laptop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(laptop["IdealSensor"],laptop["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(laptop["uArchEvent"],laptop["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(laptop["Signature"],laptop["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(laptop["T.a.S."],laptop["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(laptop["InstPending"],laptop["DecorOnly"])]
}

speedup_desktop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(desktop["DecorOnly"],desktop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(desktop["IdealSensor"],desktop["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(desktop["uArchEvent"],desktop["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(desktop["Signature"],desktop["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(desktop["T.a.S."],desktop["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(desktop["InstPending"],desktop["DecorOnly"])]
}

data = [speedup_mobile, speedup_laptop, speedup_desktop]
name = ["Mobile Throttle on Restore", "Laptop Throttle on Restore", "Desktop Throttle on Restore"]
tick_labels = ["DecorOnly", "IdealSensor", "uArchEvent", "Signature", "T.a.S", "InstPending"]
benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
fname = ["speedup_mobile_tor.png", "speedup_laptop_tor.png", "speedup_desktop_tor.png"]
bounds = [[0.0,2.0,0.1],[0.0,2.0,0.1],[0.0,2.0,0.1]]
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
	"DecorOnly" :   [23465,58356,55989,57956,18315,1,1],
  "IdealSensor" : [25470,58356,55989,60857,18315,1,1],
  "uArchEvent" :  [23465,58356,55989,62088,18452,1,1],
  "Signature" :   [23539,58834,55450,58273,18309,1,1],
  "T.a.S." :      [35515,58643,56262,63405,24579,1,1],
  "InstPending" : [26117,58361,56126,62657,21777,1,1]
}

laptop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [12491,53481,50600,57762,15462,1,1],
  "IdealSensor" : [19157,53604,50600,57762,20680,1,1],
  "uArchEvent" :  [12899,53481,50600,57762,16263,1,1],
  "Signature" :   [12289,53593,49958,57593,15443,1,1],
  "T.a.S." :      [19093,53746,50729,64126,19331,1,1],
  "InstPending" : [16810,53608,50727,59512,21247,1,1]
}

desktop = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [15520,57650,55070,61485,21185,1,1],
  "IdealSensor" : [22163,57918,55622,62625,22357,1,1],
  "uArchEvent" :  [21050,56276,53668,67881,18891,1,1],
  "Signature" :   [27095,58104,54685,61782,21687,1,1],
  "T.a.S." :      [14870,56012,53404,68220,21883,1,1],
  "InstPending" : [13947,57122,53535,63290,23935,1,1]
}

speedup_mobile = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(mobile["DecorOnly"],mobile["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(mobile["IdealSensor"],mobile["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(mobile["uArchEvent"],mobile["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(mobile["Signature"],mobile["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(mobile["T.a.S."],mobile["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(mobile["InstPending"],mobile["DecorOnly"])]
}

speedup_laptop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(laptop["DecorOnly"],laptop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(laptop["IdealSensor"],laptop["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(laptop["uArchEvent"],laptop["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(laptop["Signature"],laptop["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(laptop["T.a.S."],laptop["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(laptop["InstPending"],laptop["DecorOnly"])]
}

speedup_desktop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(desktop["DecorOnly"],desktop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(desktop["IdealSensor"],desktop["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(desktop["uArchEvent"],desktop["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(desktop["Signature"],desktop["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(desktop["T.a.S."],desktop["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(desktop["InstPending"],desktop["DecorOnly"])]
}

data = [speedup_mobile, speedup_laptop, speedup_desktop]
name = ["Mobile Throttle on Restore and Harvard PDN", "Laptop Throttle on Restore and Harvard PDN", "Desktop Throttle on Restore and Harvard PDN"]
tick_labels = ["DecorOnly", "IdealSensor", "uArchEvent", "Signature", "T.a.S", "InstPending"]
benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
fname = ["speedup_mobile_harvard_tor.png", "speedup_laptop_harvard_tor.png", "speedup_desktop_harvard_tor.png"]
bounds = [[0.0,1.5,0.1],[0.0,1.5,0.1],[0.0,1.5,0.1]]
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
