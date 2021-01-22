import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import math
x = range(0,1000)
havard = [85 + (-85)*math.exp(-0.004*t) for t in x]
better = [95 + (-95)*math.exp(-0.01*t) for t in x]

plt.plot(x,havard,label="Signature Based")
plt.plot(x,better,label="Novel")

# plt.plot(,,label="Hit Rate")
plt.ylim([0,100])
plt.xlim([0,900])

plt.xlabel("Time")
plt.ylabel("Accuracy")
plt.legend(loc=4)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are offplt.legend()
HOME = os.environ['HOME']
file_dir = HOME+ '/plot/intel-1-21-plot2.png'
plt.savefig(file_dir, dpi=300)
print(file_dir)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# img = ax.scatter(l, c, r, c=hit_avg, cmap=plt.hot())

# fig.colorbar(img)

# HOME = os.environ['HOME']
# file_dir = HOME+ '/plot/sweep_test.png'
# plt.savefig(file_dir, dpi=300)
# print(file_dir)