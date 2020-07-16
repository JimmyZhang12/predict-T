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
	"DecorOnly" : [22493,41334,5603,71196,5628,5883],
  "IdealSensor" : [22561,41334,5400,70412,5628,5734],
  "uArchEvent" : [22664,41334,5682,99144,5628,5883],
  "Signature" : [22440,41851,5383,69103,5530,5668]
}

raw_data_laptop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","toast","untoast"],
	"DecorOnly" : [12780,36823,4388,83671,4657,4704],
  "IdealSensor" : [11470,36840,4382,71886,4618,4676],
  "uArchEvent" : [12617,36823,4388,78488,4730,4704],
  "Signature" : [14677,36673,4349,70668,4487,4614]
}

raw_data_desktop = \
{
	"names" : ["dijkstra","fft","ffti","qsort","toast","untoast"],
	"DecorOnly" : [80320,65381,6593,90318,7040,6946],
  "IdealSensor" : [47760,45920,5230,76110,5352,5484],
  "uArchEvent" : [102703,92929,6545,92191,7165,7251],
  "Signature" : [20779,39395,4749,75880,4643,4847]
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

#df = [speedup_desktop["DecorOnly"],speedup_desktop["IdealSensor"],speedup_desktop["uArchEvent"],speedup_desktop["Signature"]]
df = [speedup_laptop["DecorOnly"],speedup_laptop["IdealSensor"],speedup_laptop["uArchEvent"],speedup_laptop["Signature"]]
#df = [speedup_mobile["DecorOnly"],speedup_mobile["IdealSensor"],speedup_mobile["uArchEvent"],speedup_mobile["Signature"]]

# Setting the positions and width for the bars
pos = list(range(4))
width = 0.1

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
ax.set_title('Speedup w.r.t DeCoR Only; Laptop Class CPU+PDN')
#ax.set_title('Speedup w.r.t DeCoR Only; Mobile Class CPU+PDN')

# Set the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])

#ax.set_yticks(np.arange(0.0,4,0.5))
#ax.set_ylim(0.0, 4)
ax.set_yticks(np.arange(0.0,1.5,0.1))
ax.set_ylim(0.0, 1.5)
#ax.set_yticks(np.arange(0.0,1.5,0.1))
#ax.set_ylim(0.0, 1.5)
ax.set_axisbelow(True)
ax.grid(zorder=0, color="#c4c4c4", linestyle="-", linewidth=1, axis="y")

# Set the labels for the x ticks
ax.set_xticklabels(["DecorOnly", "IdealSensor", "uArchEvent", "Signature"])

# Adding the legend and showing the plot
plt.legend(["dijkstra","fft","ffti","qsort","toast","untoast"], loc='upper left')
#plt.grid()
plt.show()
