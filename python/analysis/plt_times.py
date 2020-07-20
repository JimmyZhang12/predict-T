import pandas as pd
import glob
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import argparse

#strategies = [ "None", "Decor", "IdealSensor", "uArchEvent", "Harvard" ]
strategies = [ "Decor", "IdealSensor", "uArchEvent", "Signature" ]

names = [ "Dijkstra", "FFT", "Rijndael Encrypt", "Toast" ]

#raw_data_3g = \
#{
#	"Type" : strategies,
#	"Dijkstra" : [736594/1e3,756592/1e3,1059895/1e3,756591/1e3,0/1e3],
#	"FFT" : [2949705/1e3,3049695/1e3,3016365/1e3,3199680/1e3,0/1e3],
#  "Rijndael Encrypt" : [5749425/1e3,4802853/1e3,5412792/1e3,4802853/1e3,0/1e3],
#  "Toast" : [1313202/1e3,1313202/1e3,1589841/1e3,1313202/1e3,0/1e3],
#}
#
#raw_data_4g = \
#{
#	"Type" : strategies,
#	"Dijkstra" : [567500/1e3,1357500/1e3,1005000/1e3,1392500/1e3,0/1e3],
#	"FFT" : [2212500/1e3,2550000/1e3,2485000/1e3,2450000/1e3,0/1e3],
#  "Rijndael Encrypt" : [4312500/1e3,6170000/1e3,5237500/1e3,5650000/1e3,0/1e3],
#  "Toast" : [985000/1e3,1162500/1e3,1317500/1e3,1162500/1e3,0/1e3],
#}

raw_data_mobile = \
{
	"names" : ["dijkstra","fft","ffti","qsort","toast","untoast"],
	"DecorOnly" : [30698,59109,23523,67372,23073,22941],
  "IdealSensor" : [33944,65493,62643,66770,40871,24623],
  "uArchEvent" : [31973,63322,23706,68689,23248,18729],
  "Signature" : [30765,62660,23571,67223,22892,17871]
}

raw_data_laptop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","toast","untoast"],
	"DecorOnly" : [71237,68759,19351,58794,20282,20624],
  "IdealSensor" : [68085,56412,53436,63161,53859,19636],
  "uArchEvent" : [32163,51468,19201,64172,19929,10803],
  "Signature" : [65333,57012,19672,58778,20086,10341]
}

raw_data_desktop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","toast","untoast"],
	"DecorOnly" : [58023,62402,22826,68575,23706,24211],
  "IdealSensor" : [61854,68579,64148,76647,80525,26825],
  "uArchEvent" : [57656,63043,22891,70047,24311,9960],
  "Signature" : [58512,62865,22916,68764,19180,8250]
}

raw_data_mobile_tos = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [28098,67612,62139,67636,1,40895,1],
  "IdealSensor" : [28514,66632,63939,68171,1,42651,1],
  "uArchEvent" :  [32041,68891,65767,70439,1,43036,1],
  "Signature" :   [29793,66790,64205,67635,1,41566,1],
  "T.a.S." :      [40470,67396,63857,66647,25576,44067,63489],
  "InstPending" : [32003,65364,60882,68886,22917,45615,54567]
}

raw_data_laptop_tos = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [70445,65184,62909,62385,1,62252,1],
  "IdealSensor" : [44243,56213,52974,63043,1,49397,1],
  "uArchEvent" :  [40433,53999,51468,64540,1,50093,1],
  "Signature" :   [63819,60527,57595,62340,1,53177,1],
  "T.a.S." :      [59462,53868,50729,63739,29195,46762,43347],
  "InstPending" : [67375,60215,63580,64120,40961,53401,51883]
}

raw_data_desktop_tos = \
{
	"names" :       ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
	"DecorOnly" :   [60137,61940,63114,70465,1,77832,1],
  "IdealSensor" : [61576,68604,64093,77183,1,80881,1],
  "uArchEvent" :  [61624,63859,63581,70383,1,75369,1],
  "Signature" :   [60594,67262,62996,72555,1,77343,1],
  "T.a.S." :      [60265,64140,63860,69893,54406,79301,108210],
  "InstPending" : [60049,62074,63189,71477,55950,76971,108127]
}

speedup_mobile = \
{
	"names" : ["dijkstra","fft","ffti","qsort","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(raw_data_mobile["DecorOnly"],raw_data_mobile["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(raw_data_mobile["IdealSensor"],raw_data_mobile["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(raw_data_mobile["uArchEvent"],raw_data_mobile["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(raw_data_mobile["Signature"],raw_data_mobile["DecorOnly"])],
}

speedup_laptop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(raw_data_laptop["DecorOnly"],raw_data_laptop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(raw_data_laptop["IdealSensor"],raw_data_laptop["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(raw_data_laptop["uArchEvent"],raw_data_laptop["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(raw_data_laptop["Signature"],raw_data_laptop["DecorOnly"])],
}

speedup_desktop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(raw_data_desktop["DecorOnly"],raw_data_desktop["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(raw_data_desktop["IdealSensor"],raw_data_desktop["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(raw_data_desktop["uArchEvent"],raw_data_desktop["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(raw_data_desktop["Signature"],raw_data_desktop["DecorOnly"])],
}

speedup_mobile_tos = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(raw_data_mobile_tos["DecorOnly"],raw_data_mobile_tos["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(raw_data_mobile_tos["IdealSensor"],raw_data_mobile_tos["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(raw_data_mobile_tos["uArchEvent"],raw_data_mobile_tos["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(raw_data_mobile_tos["Signature"],raw_data_mobile_tos["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(raw_data_mobile_tos["T.a.S."],raw_data_mobile_tos["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(raw_data_mobile_tos["InstPending"],raw_data_mobile_tos["DecorOnly"])]
}

speedup_laptop_tos = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(raw_data_laptop_tos["DecorOnly"],raw_data_laptop_tos["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(raw_data_laptop_tos["IdealSensor"],raw_data_laptop_tos["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(raw_data_laptop_tos["uArchEvent"],raw_data_laptop_tos["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(raw_data_laptop_tos["Signature"],raw_data_laptop_tos["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(raw_data_laptop_tos["T.a.S."],raw_data_laptop_tos["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(raw_data_laptop_tos["InstPending"],raw_data_laptop_tos["DecorOnly"])]
}

speedup_desktop_tos = \
{
	"names" : ["dijkstra","fft","ffti","qsort","sha","toast","untoast"],
  "DecorOnly" :   [baseline/test for test,baseline in zip(raw_data_desktop_tos["DecorOnly"],raw_data_desktop_tos["DecorOnly"])],
  "IdealSensor" : [baseline/test for test,baseline in zip(raw_data_desktop_tos["IdealSensor"],raw_data_desktop_tos["DecorOnly"])],
  "uArchEvent" :      [baseline/test for test,baseline in zip(raw_data_desktop_tos["uArchEvent"],raw_data_desktop_tos["DecorOnly"])],
  "Signature" :     [baseline/test for test,baseline in zip(raw_data_desktop_tos["Signature"],raw_data_desktop_tos["DecorOnly"])],
  "T.a.S." :      [baseline/test for test,baseline in zip(raw_data_desktop_tos["T.a.S."],raw_data_desktop_tos["DecorOnly"])],
  "InstPending" :     [baseline/test for test,baseline in zip(raw_data_desktop_tos["InstPending"],raw_data_desktop_tos["DecorOnly"])]
}

#df = [speedup_desktop["DecorOnly"],speedup_desktop["IdealSensor"],speedup_desktop["uArchEvent"],speedup_desktop["Signature"]]
#df = [speedup_laptop["DecorOnly"],speedup_laptop["IdealSensor"],speedup_laptop["uArchEvent"],speedup_laptop["Signature"]]
#df = [speedup_mobile["DecorOnly"],speedup_mobile["IdealSensor"],speedup_mobile["uArchEvent"],speedup_mobile["Signature"]]
#df = [speedup_desktop_tos["DecorOnly"],speedup_desktop_tos["IdealSensor"],speedup_desktop_tos["uArchEvent"],speedup_desktop_tos["Signature"],speedup_desktop_tos["T.a.S."],speedup_desktop_tos["InstPending"]]
#df = [speedup_laptop_tos["DecorOnly"],speedup_laptop_tos["IdealSensor"],speedup_laptop_tos["uArchEvent"],speedup_laptop_tos["Signature"],speedup_laptop_tos["T.a.S."],speedup_laptop_tos["InstPending"]]
df = [speedup_mobile_tos["DecorOnly"],speedup_mobile_tos["IdealSensor"],speedup_mobile_tos["uArchEvent"],speedup_mobile_tos["Signature"],speedup_mobile_tos["T.a.S."],speedup_mobile_tos["InstPending"]]

# Setting the positions and width for the bars
pos = list(range(len(df)))
width = 0.125

# Plotting the bars
fig, ax = plt.subplots(figsize=(10,5))

print(pos)
i=0
plt.bar([p + width*i for p in pos],
        [j[i] for j in df],
        width,
        label="dijkstra",
        color="w",
        hatch="/"*1,
        fill=True,
        linewidth=1,
        edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos],
        [j[i] for j in df],
        width,
        label="fft",
        color="w",
        hatch="o"*2,
        fill=True,
        linewidth=1,
        edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos],
        [j[i] for j in df],
        width,
        label="ffti",
        color="w",
        hatch="X"*4,
        fill="False",
        linewidth=1,
        edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos],
        [j[i] for j in df],
        width,
        label="qsort",
        color="w",
        hatch="/"*4,
        fill=True,
        linewidth=1,
        edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos],
        [j[i] for j in df],
        width,
        label="sha",
        color="w",
        hatch="-"*4,
        fill=True,
        linewidth=1,
        edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos],
        [j[i] for j in df],
        width,
        label="toast",
        color="w",
        hatch='\\'*4,
        fill=True,
        linewidth=1,
        edgecolor="k")
i+=1
plt.bar([p + width*i for p in pos],
        [j[i] for j in df],
        width,
        label="untoast",
        color="w",
        hatch="."*4,
        fill=True,
        linewidth=1,
        edgecolor="k")

# Set the y axis label
#ax.set_ylabel('Time (ns)')
ax.set_ylabel('Speedup (X)')

# Set the chart's title
#ax.set_title('Speedup w.r.t DeCoR Only; Desktop Class CPU+PDN')
#ax.set_title('Speedup w.r.t DeCoR Only; Laptop Class CPU+PDN')
ax.set_title('Speedup w.r.t DeCoR Only; Mobile Class CPU+PDN')

# Set the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])

#ax.set_yticks(np.arange(0.9,1.1,0.01))
#ax.set_ylim(0.9, 1.1)
#ax.set_yticks(np.arange(0.5,2.5,0.05))
#ax.set_ylim(0.5, 2.5)
ax.set_yticks(np.arange(0.66,1.1,0.02))
ax.set_ylim(0.66, 1.1)
ax.set_axisbelow(True)
ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")

# Set the labels for the x ticks
ax.set_xticklabels(["DecorOnly", "IdealSensor", "uArchEvent", "Signature", "T.a.S.", "InstPending"])

# Adding the legend and showing the plot
plt.legend(["dijkstra","fft","ffti","qsort","sha","toast","untoast"], loc='upper left')
#plt.grid()
plt.show()
