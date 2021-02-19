import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

freq_scale  = np.array( ["1","0.5","0.4","0.2"] )
mobile = [1550, 41, 0, 0]
laptop = [243, 0, 0, 0]
desktop = [381, 375, 369,2]

fig = plt.figure()
ax = plt.axes()

width = 0.8

TEST = "qsort"
CLASSES = ["mobile", "laptop", "desktop"] 
PLOT_NAME = "9-24_cumulative_VE_freq.png"

fig, (ax1,ax2,ax3) = plt.subplots(3)
fig.set_size_inches(5, 6.5, forward=True)

ax1.bar(freq_scale, mobile, width)
ax2.bar(freq_scale, laptop, width)
ax3.bar(freq_scale, desktop,width)

ax1.set_title('mobile')
ax2.set_title('laptop')
ax3.set_title('desktop')



fig.suptitle('Cumulative Voltage Emergencies over Frequency' + ', ' + TEST + ' )', fontsize=12)
plt.xlabel('frequency scaling', fontsize=12)
plt.ylabel('Count', fontsize=12)
ax.legend(CLASSES)

print(PLOT_NAME)
plt.savefig(PLOT_NAME)