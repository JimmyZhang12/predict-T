import pandas as pd
import glob
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
from yellowbrick.style.palettes import PALETTES, SEQUENCES, color_palette
from yellowbrick.style import set_palette
import argparse

#strategies = [ "None", "Decor", "IdealSensor", "uArchEvent", "Harvard" ]
strategies = [ "Decor", "IdealSensor", "uArchEvent", "Signature" ]

names = [ "Dijkstra", "FFT", "Rijndael Encrypt", "Toast" ]

none_3g = [ 736594, 2949705, 5749425, 1313202 ]

none_4g = [ 567500, 2212500, 4312500, 985000 ]

decor_3g = [ 756592, 3049695, 4802853, 1313202 ]

decor_4g= [ 1357500, 2550000, 6170000, 1162500 ]

ideal_sensor_3g = [ 1059895, 3016365, 5412792, 1589841 ]

ideal_sensor_4g = [ 1005000, 2485000, 5237500, 1317500 ]

uarch_3g = [ 756591, 3199680, 4802853, 1313202 ]

uarch_4g= [ 1392500, 2450000, 5650000, 1162500 ]

harvard_3g = [ 803253, 2949705, 4639536, 1299870 ]

harvard_4g = [ 882500, 2602500, 6270000, 1377500 ]

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

raw_data_3g = \
{
	"Type" : strategies,
	"Dijkstra" : [756592/1e3,1059895/1e3,756591/1e3,803253/1e3],
	"FFT" : [3049695/1e3,3016365/1e3,3199680/1e3,2949705/1e3],
  "Rijndael" : [4802853/1e3,5412792/1e3,4802853/1e3,4639536/1e3],
  "Toast" : [1313202/1e3,1589841/1e3,1313202/1e3,1299870/1e3]
}

raw_data_4g = \
{
	"Type" : strategies,
	"Dijkstra" : [1357500/1e3,1005000/1e3,1392500/1e3,882500/1e3],
	"FFT" : [2550000/1e3,2485000/1e3,2450000/1e3,2602500/1e3],
  "Rijndael" : [6170000/1e3,5237500/1e3,5650000/1e3,6270000/1e3],
  "Toast" : [1162500/1e3,1317500/1e3,1162500/1e3,1377500/1e3]
}

speedup_3g = \
{
  "Type" : strategies,
  "Dijkstra" :  [raw_data_3g["Dijkstra"][0]/i for i in raw_data_3g["Dijkstra"]],
  "FFT" :       [raw_data_3g["FFT"][0]/i for i in raw_data_3g["FFT"]],
  "Rijndael" :  [raw_data_3g["Rijndael"][0]/i for i in raw_data_3g["Rijndael"]],
  "Toast" :     [raw_data_3g["Toast"][0]/i for i in raw_data_3g["Toast"]]
}

speedup_4g = \
{
  "Type" : strategies,
  "Dijkstra" :  [raw_data_4g["Dijkstra"][0]/i for i in raw_data_4g["Dijkstra"]],
  "FFT" :       [raw_data_4g["FFT"][0]/i for i in raw_data_4g["FFT"]],
  "Rijndael" :  [raw_data_4g["Rijndael"][0]/i for i in raw_data_4g["Rijndael"]],
  "Toast" :     [raw_data_4g["Toast"][0]/i for i in raw_data_4g["Toast"]]
}

set_palette("colorblind")

df_3g = pd.DataFrame(speedup_3g, columns=["Type","Dijkstra","FFT","Rijndael","Toast"])
df_4g = pd.DataFrame(speedup_4g, columns=["Type","Dijkstra","FFT","Rijndael","Toast"])

# Setting the positions and width for the bars
pos = list(range(len(df_3g['Dijkstra'])))
width = 0.1

# Plotting the bars
fig, ax = plt.subplots(figsize=(10,5))

#plt.bar(pos,
#        df_3g['Dijkstra'],
#        width,
#        label=df_3g['Type'][0])
#plt.bar([p + width for p in pos],
#        df_3g['FFT'],
#        width,
#        label=df_3g['Type'][1])
#plt.bar([p + width*2 for p in pos],
#        df_3g['Rijndael'],
#        width,
#        label=df_3g['Type'][2])
#plt.bar([p + width*3 for p in pos],
#        df_3g['Toast'],
#        width,
#        label=df_3g['Type'][3])

plt.bar([p + width*0 for p in pos],
        df_4g['Dijkstra'],
        width,
        label=df_4g['Type'][0])
plt.bar([p + width*1 for p in pos],
        df_4g['FFT'],
        width,
        label=df_4g['Type'][1])
plt.bar([p + width*2 for p in pos],
        df_4g['Rijndael'],
        width,
        label=df_4g['Type'][2])
plt.bar([p + width*3 for p in pos],
        df_4g['Toast'],
        width,
        label=df_4g['Type'][3])

# Set the y axis label
#ax.set_ylabel('Time (ns)')
ax.set_ylabel('Speedup (X)')

# Set the chart's title
#ax.set_title('Speedup w.r.t DeCoR only for 3000 Instructions @ 3.0GHz')
ax.set_title('Speedup w.r.t DeCoR only for 3000 Instructions @ 4.0GHz')
#ax.set_title('Total Execution Time for 3000 Instructions @ 3.0GHz')
#ax.set_title('Total Execution Time for 3000 Instructions @ 4.0GHz')

# Set the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])

ax.set_yticks(np.arange(0.0,1.6,0.1))
ax.set_ylim(0.0, 1.6)

# Set the labels for the x ticks
ax.set_xticklabels(df_3g['Type'])

# Adding the legend and showing the plot
plt.legend(["Dijkstra","FFT","Rijndael Encrypt","Toast"], loc='upper left')
#plt.grid()
plt.show()
