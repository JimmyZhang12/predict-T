import pandas as pd
import glob
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import argparse

#------------------------------------------------------------------------------------------------
# Base Systems for Characterization:
# 4 Mechanism,  [decor, sensor, uarch, signature]
# 7 Benchmarks, [dijkstra, fft, ffti, qsort, sha, toast, untoast]
# 3 PDN/CPU,    [mobile, laptop, desktop]
#------------------------------------------------------------------------------------------------
mobile = \
{
  "names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [31090,63448,59109,67372,20112,1,1],
  "IdealSensor" : [33944,65493,62643,66770,20452,1,1],
  "uArchEvent" :  [31942,67464,63322,68689,25699,1,1],
  "Signature" :   [30337,65927,62660,67223,21057,1,1],
  "T.a.S." :      [1,1,1,1,1,1,1],
  "InstPending" : [1,1,1,1,1,1,1]
}

laptop = \
{
  "names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [72642,69036,68759,58794,55161,1,1],
  "IdealSensor" : [68085,56412,53436,63161,29677,1,1],
  "uArchEvent" :  [57103,53999,51468,64172,28010,1,1],
  "Signature" :   [53732,60792,57012,58778,41080,1,1],
  "T.a.S." :      [1,1,1,1,1,1,1],
  "InstPending" : [1,1,1,1,1,1,1]
}

desktop = \
{
  "names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [57711,64126,62402,68575,51750,1,1],
  "IdealSensor" : [61854,68579,64148,76647,56137,1,1],
  "uArchEvent" :  [61218,66537,63043,70047,56806,1,1],
  "Signature" :   [57071,65799,62865,68764,53216,1,1],
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
#data = [speedup_mobile, speedup_laptop, speedup_desktop]
#name = ["Mobile", "Laptop", "Desktop"]
#tick_labels = ["DecorOnly", "IdealSensor", "uArchEvent", "Signature"]
#benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
#fname = ["speedup_mobile.png", "speedup_laptop.png", "speedup_desktop.png"]
#bounds = [[0.0,3.0,0.1],[0.0,3.0,0.1],[0.0,3.0,0.1]]
#for k in range(len(data)):
#  df=[data[k]["DecorOnly"],data[k]["IdealSensor"],data[k]["uArchEvent"],data[k]["Signature"]]
#  pos = list(range(len(df)))
#  width = 0.125
#  fig, ax = plt.subplots(figsize=(10,5))
#  i=0
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="dijkstra", color="w", hatch="/"*1, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="fft", color="w", hatch="o"*2, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="ffti", color="w", hatch="X"*4, fill="False", linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="qsort", color="w", hatch="/"*4, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="sha", color="w", hatch="-"*4, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="toast", color="w", hatch='\\'*4, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="untoast", color="w", hatch="."*4, fill=True, linewidth=1, edgecolor="k")
#  ax.set_ylabel('Speedup (X)')
#  ax.set_title(name[k])
#  ax.set_xticks([p + 1.5 * width for p in pos])
#  ax.set_yticks(np.arange(bounds[k][0],bounds[k][1],bounds[k][2]))
#  ax.set_ylim(bounds[k][0],bounds[k][1])
#  ax.set_axisbelow(True)
#  ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")
#  ax.set_xticklabels(tick_labels)
#  #plt.legend(benchmarks, loc='upper left')
#  plt.legend(benchmarks, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#  plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
#  plt.savefig(fname[k])
#  plt.show()



#------------------------------------------------------------------------------------------------
# System w/throttle on restore from DeCoR:
# 6 Mechanism,  [decor, sensor, uarch, signature, T.a.S., InstPending]
# 7 Benchmarks, [dijkstra, fft, ffti, qsort, sha, toast, untoast]
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

#data = [speedup_mobile, speedup_laptop, speedup_desktop]
#name = ["Mobile Throttle on Restore", "Laptop Throttle on Restore", "Desktop Throttle on Restore"]
#tick_labels = ["DecorOnly", "IdealSensor", "uArchEvent", "Signature", "T.a.S", "InstPending"]
#benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
#fname = ["speedup_mobile_tor.png", "speedup_laptop_tor.png", "speedup_desktop_tor.png"]
#bounds = [[0.0,2.0,0.1],[0.0,2.0,0.1],[0.0,2.0,0.1]]
#for k in range(len(data)):
#  df=[data[k]["DecorOnly"],data[k]["IdealSensor"],data[k]["uArchEvent"],data[k]["Signature"],data[k]["T.a.S."],data[k]["InstPending"]]
#  pos = list(range(len(df)))
#  width = 0.125
#  fig, ax = plt.subplots(figsize=(10,5))
#  i=0
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="dijkstra", color="w", hatch="/"*1, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="fft", color="w", hatch="o"*2, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="ffti", color="w", hatch="X"*4, fill="False", linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="qsort", color="w", hatch="/"*4, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="sha", color="w", hatch="-"*4, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="toast", color="w", hatch='\\'*4, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="untoast", color="w", hatch="."*4, fill=True, linewidth=1, edgecolor="k")
#  ax.set_ylabel('Num Voltage Emergencies')
#  ax.set_title(name[k])
#  ax.set_xticks([p + 1.5 * width for p in pos])
#  ax.set_yticks(np.arange(bounds[k][0],bounds[k][1],bounds[k][2]))
#  ax.set_ylim(bounds[k][0],bounds[k][1])
#  ax.set_axisbelow(True)
#  ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")
#  ax.set_xticklabels(tick_labels)
#  #plt.legend(benchmarks, loc='upper left')
#  plt.legend(benchmarks, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#  plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
#  plt.savefig(fname[k])
#  plt.show()

it = \
{
  "names" :       ["Mobile","Laptop","Desktop"],
  "IdealSensor" : [sum(speedup_mobile["IdealSensor"])/len(speedup_mobile["IdealSensor"]), \
                   sum(speedup_laptop["IdealSensor"])/len(speedup_laptop["IdealSensor"]), \
                   sum(speedup_desktop["IdealSensor"])/len(speedup_desktop["IdealSensor"])],
  "uArchEvent" :  [sum(speedup_mobile["uArchEvent"])/len(speedup_mobile["uArchEvent"]), \
                   sum(speedup_laptop["uArchEvent"])/len(speedup_laptop["uArchEvent"]), \
                   sum(speedup_desktop["uArchEvent"])/len(speedup_desktop["uArchEvent"])],
  "Signature" :   [sum(speedup_mobile["Signature"])/len(speedup_mobile["Signature"]), \
                   sum(speedup_laptop["Signature"])/len(speedup_laptop["Signature"]), \
                   sum(speedup_desktop["Signature"])/len(speedup_desktop["Signature"])],
  "T.a.S." :      [sum(speedup_mobile["T.a.S."])/len(speedup_mobile["T.a.S."]), \
                   sum(speedup_laptop["T.a.S."])/len(speedup_laptop["T.a.S."]), \
                   sum(speedup_desktop["T.a.S."])/len(speedup_desktop["T.a.S."])],
  "InstPending" : [sum(speedup_mobile["InstPending"])/len(speedup_mobile["InstPending"]), \
                   sum(speedup_laptop["InstPending"])/len(speedup_laptop["InstPending"]), \
                   sum(speedup_desktop["InstPending"])/len(speedup_desktop["InstPending"])],
}

name = ["Average Speedup Across Systems"]
tick_labels = ["IdealSensor", "uArchEvent", "Signature", "T.a.S.", "InstPending"]
benchmarks = ["Mobile","Latop","Desktop"]
fname = ["speedup_constrained.png"]
bounds = [[0,2,0.1,0]]
df=[it["IdealSensor"],it["uArchEvent"],it["Signature"],it["T.a.S."],it["InstPending"]]
pos = list(range(len(df)))
width = 0.2
fig, ax = plt.subplots(figsize=(10,5))
i=0
plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label=benchmarks[i], color="w", hatch="/"*4, fill=True, linewidth=1, edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label=benchmarks[i], color="w", hatch="\\"*4, fill=True, linewidth=1, edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label=benchmarks[i], color="w", hatch="X"*4, fill="True", linewidth=1, edgecolor="k")
ax.set_ylabel('Speedup (X)')
ax.set_title(name[0])
ax.set_xticks([p + 1.5 * width for p in pos])
ax.set_yticks(np.arange(bounds[0][0],bounds[0][1],bounds[0][2]))
ax.set_ylim(bounds[0][0],bounds[0][1])
ax.set_axisbelow(True)
ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")
b = ax.get_ygridlines()
b[bounds[0][3]].set_color('k')
ax.set_xticklabels(tick_labels)
#plt.legend(benchmarks, loc='upper left')
plt.legend(benchmarks, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
plt.savefig(fname[0])
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
  "DecorOnly" :   [32846,58489,56254,68327,19005,33934,50720],
  "IdealSensor" : [42124,58621,56386,69668,19580,35955,55040],
  "uArchEvent" :  [38324,59028,56121,68284,19163,37111,51255],
  "Signature" :   [34422,59126,55847,68771,19229,35038,50343],
  "T.a.S." :      [37677,58643,56266,70464,25292,41389,61009],
  "InstPending" : [33424,58625,56390,70242,23759,40431,52858]
}

laptop = \
{
  "names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [14453,53604,50600,61527,17487,28794,36208],
  "IdealSensor" : [31336,55554,53482,62805,25856,40182,43012],
  "uArchEvent" :  [23599,53906,50600,63586,18579,33920,36303],
  "Signature" :   [21452,53593,49958,61492,17532,28485,37635],
  "T.a.S." :      [19093,53746,50851,64126,20117,33115,42520],
  "InstPending" : [18413,53608,50727,59645,24249,37304,42428]
}

desktop = \
{
  "names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [15520,57650,55070,61485,21185,34999,37827],
  "IdealSensor" : [22163,57918,55622,62625,22357,36333,41556],
  "uArchEvent" :  [21050,56276,53668,67881,18891,34582,38341],
  "Signature" :   [27095,58104,54685,61782,21687,34974,36409],
  "T.a.S." :      [14870,56012,53404,68220,21883,37333,42417],
  "InstPending" : [13947,57122,53535,63290,23935,37471,42282]
}

speedup_mobile = \
{
  "names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(mobile["DecorOnly"],mobile["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(mobile["IdealSensor"],mobile["DecorOnly"])],
  "uArchEvent" :  [baseline/test for test,baseline in zip(mobile["uArchEvent"],mobile["DecorOnly"])],
  "Signature" :   [baseline/test for test,baseline in zip(mobile["Signature"],mobile["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(mobile["T.a.S."],mobile["DecorOnly"])],
  "InstPending" : [baseline/test for test,baseline in zip(mobile["InstPending"],mobile["DecorOnly"])]
}

speedup_laptop = \
{
  "names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(laptop["DecorOnly"],laptop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(laptop["IdealSensor"],laptop["DecorOnly"])],
  "uArchEvent" :  [baseline/test for test,baseline in zip(laptop["uArchEvent"],laptop["DecorOnly"])],
  "Signature" :   [baseline/test for test,baseline in zip(laptop["Signature"],laptop["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(laptop["T.a.S."],laptop["DecorOnly"])],
  "InstPending" : [baseline/test for test,baseline in zip(laptop["InstPending"],laptop["DecorOnly"])]
}

speedup_desktop = \
{
  "names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(desktop["DecorOnly"],desktop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(desktop["IdealSensor"],desktop["DecorOnly"])],
  "uArchEvent" :  [baseline/test for test,baseline in zip(desktop["uArchEvent"],desktop["DecorOnly"])],
  "Signature" :   [baseline/test for test,baseline in zip(desktop["Signature"],desktop["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(desktop["T.a.S."],desktop["DecorOnly"])],
  "InstPending" : [baseline/test for test,baseline in zip(desktop["InstPending"],desktop["DecorOnly"])]
}

#data = [speedup_mobile, speedup_laptop, speedup_desktop]
#name = ["Mobile Throttle on Restore and Harvard PDN", "Laptop Throttle on Restore and Harvard PDN", "Desktop Throttle on Restore and Harvard PDN"]
#tick_labels = ["DecorOnly", "IdealSensor", "uArchEvent", "Signature", "T.a.S", "InstPending"]
#benchmarks = ["dijkstra","fft","ffti","qsort","sha","toast","untoast"]
#fname = ["speedup_mobile_harvard_tor.png", "speedup_laptop_harvard_tor.png", "speedup_desktop_harvard_tor.png"]
#bounds = [[0.0,1.5,0.1],[0.0,1.5,0.1],[0.0,1.5,0.1]]
#for k in range(len(data)):
#  df=[data[k]["DecorOnly"],data[k]["IdealSensor"],data[k]["uArchEvent"],data[k]["Signature"],data[k]["T.a.S."],data[k]["InstPending"]]
#  pos = list(range(len(df)))
#  width = 0.125
#  fig, ax = plt.subplots(figsize=(10,5))
#  i=0
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="dijkstra", color="w", hatch="/"*1, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="fft", color="w", hatch="o"*2, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="ffti", color="w", hatch="X"*4, fill="False", linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="qsort", color="w", hatch="/"*4, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="sha", color="w", hatch="-"*4, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="toast", color="w", hatch='\\'*4, fill=True, linewidth=1, edgecolor="k")
#  i+=1
#  plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label="untoast", color="w", hatch="."*4, fill=True, linewidth=1, edgecolor="k")
#  ax.set_ylabel('Num Voltage Emergencies')
#  ax.set_title(name[k])
#  ax.set_xticks([p + 1.5 * width for p in pos])
#  ax.set_yticks(np.arange(bounds[k][0],bounds[k][1],bounds[k][2]))
#  ax.set_ylim(bounds[k][0],bounds[k][1])
#  ax.set_axisbelow(True)
#  ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")
#  ax.set_xticklabels(tick_labels)
#  #plt.legend(benchmarks, loc='upper left')
#  plt.legend(benchmarks, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#  plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
#  plt.savefig(fname[k])
#  plt.show()

it = \
{
  "names" :       ["Mobile","Laptop","Desktop"],
  "IdealSensor" : [sum(speedup_mobile["IdealSensor"])/len(speedup_mobile["IdealSensor"]), \
                   sum(speedup_laptop["IdealSensor"])/len(speedup_laptop["IdealSensor"]), \
                   sum(speedup_desktop["IdealSensor"])/len(speedup_desktop["IdealSensor"])],
  "uArchEvent" :  [sum(speedup_mobile["uArchEvent"])/len(speedup_mobile["uArchEvent"]), \
                   sum(speedup_laptop["uArchEvent"])/len(speedup_laptop["uArchEvent"]), \
                   sum(speedup_desktop["uArchEvent"])/len(speedup_desktop["uArchEvent"])],
  "Signature" :   [sum(speedup_mobile["Signature"])/len(speedup_mobile["Signature"]), \
                   sum(speedup_laptop["Signature"])/len(speedup_laptop["Signature"]), \
                   sum(speedup_desktop["Signature"])/len(speedup_desktop["Signature"])],
  "T.a.S." :      [sum(speedup_mobile["T.a.S."])/len(speedup_mobile["T.a.S."]), \
                   sum(speedup_laptop["T.a.S."])/len(speedup_laptop["T.a.S."]), \
                   sum(speedup_desktop["T.a.S."])/len(speedup_desktop["T.a.S."])],
  "InstPending" : [sum(speedup_mobile["InstPending"])/len(speedup_mobile["InstPending"]), \
                   sum(speedup_laptop["InstPending"])/len(speedup_laptop["InstPending"]), \
                   sum(speedup_desktop["InstPending"])/len(speedup_desktop["InstPending"])],
}

name = ["Average Speedup Across Systems"]
tick_labels = ["IdealSensor", "uArchEvent", "Signature", "T.a.S.", "InstPending"]
benchmarks = ["Mobile","Latop","Desktop"]
fname = ["speedup_unconstrained.png"]
bounds = [[0,2,0.1,0]]
df=[it["IdealSensor"],it["uArchEvent"],it["Signature"],it["T.a.S."],it["InstPending"]]
pos = list(range(len(df)))
width = 0.2
fig, ax = plt.subplots(figsize=(10,5))
i=0
plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label=benchmarks[i], color="w", hatch="/"*4, fill=True, linewidth=1, edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label=benchmarks[i], color="w", hatch="\\"*4, fill=True, linewidth=1, edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos], [j[i] for j in df], width, label=benchmarks[i], color="w", hatch="X"*4, fill="True", linewidth=1, edgecolor="k")
ax.set_ylabel('Speedup (X)')
ax.set_title(name[0])
ax.set_xticks([p + 1.5 * width for p in pos])
ax.set_yticks(np.arange(bounds[0][0],bounds[0][1],bounds[0][2]))
ax.set_ylim(bounds[0][0],bounds[0][1])
ax.set_axisbelow(True)
ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")
b = ax.get_ygridlines()
b[bounds[0][3]].set_color('k')
ax.set_xticklabels(tick_labels)
#plt.legend(benchmarks, loc='upper left')
plt.legend(benchmarks, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
plt.savefig(fname[0])
plt.show()
