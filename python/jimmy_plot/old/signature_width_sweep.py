import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util
from enum import Enum

HOME = os.environ['HOME']
f, (ax1) = plt.subplots()
f.set_size_inches(6, 5)

# xvar = [4,8,16,32,64,128,256]
# hit = [95,91,85,82,75,72,68]
# falsepos = [80.9,79.85,70.3,69.2,50,45, 45]
# ax1.plot(xvar, hit, color='black', linewidth=1.0, label='hits')
# ax1.plot(xvar, falsepos, color='red', linewidth=1.0, label='false positives')
# ax1.legend()
# #ax1.set_title('Accuracy Over Lead Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST  + str(len(VE)) +')', fontsize=14)
# ax1.set_title('Dijkstra, Desktop,', fontsize=14)
# ax1.set_xlabel('Signature Width', fontsize=14) 
# ax1.set_ylabel('Accuracy (%)', fontsize=14)

# plt.savefig(HOME+'/passat/plot/11-26_sig_sweep_fft.png')

xvar = [2,3,4]
hit = [57,87,70]
ax1.plot(xvar, hit, color='gray', linewidth=1.0, label='hits')
#ax1.plot(xvar, falsepos, color='red', linewidth=1.0, label='false positives')
ax1.legend()
#ax1.set_title('Accuracy Over Lead Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST  + str(len(VE)) +')', fontsize=14)
#ax1.set_title('Dijkstra, Desktop,', fontsize=14)
ax1.set_xlabel('PDN', fontsize=14) 
ax1.set_ylabel('Accuracy (%)', fontsize=14)
ax1.set_xlim([1.5,4.5])

locs, labels = plt.xticks()            # Get locations and labels
plt.xticks([2,3,4], ["good", "moderate", "bad"])  # Set locations and labels

plt.savefig(HOME+'/passat/plot/11-26_goodbadugly_fft.png')

