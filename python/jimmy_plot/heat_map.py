import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
# import util
# from enum import Enum
# from datetime import datetime
# import math
# from mpl_toolkits.mplot3d import Axes3D

HOME = os.environ['HOME']
sweep = np.load(HOME+'/plot/data/PDN_SWEEP_HARVARD_2.npy')

# print(sweep)
# L = 10E-12 + l * ((60E-12 - 10E-12)/5)
# C = 0.2E-6 + c * ((3E-6 - 0.2E-6)/5)
# R = 0.5E-3 + r * ((5E-3 - 0.5E-3)/5)

# averages.append([l,c,r,hit_avg, fp_avg, fn_avg])
exit

l = sweep[:,0]
c = sweep[:,1]
r = sweep[:,2]
hit_avg = sweep[:,3]
fp_avg = sweep[:,4]
fn_avg = sweep[:,5]

plot_x = []
plot_hr = []
plot_fp = []

for i in range(5**3):
    if sweep[i,3] > 40:
        l =  sweep[i,0]
        c =  sweep[i,1]
        r =  sweep[i,2]

        L = 10 + l * ((60 - 10)/5)
        L *= 1E-12
        C = 0.2E-6 + c * ((3E-6 - 0.2E-6)/5)
        R = 0.5E-3 + r * ((5E-3 - 0.5E-3)/5)
        print(sweep[i,:], L," ",C," ",R)
        plot_x.append(L)
        plot_hr.append(sweep[i,3])
        plot_fp.append(sweep[i,4])

plt.plot(plot_x,plot_fp,label="False Positive Rate")
plt.plot(plot_x,plot_hr,label="Hit Rate")
plt.ylim([0,100])
plt.xlabel("Inductance")
plt.ylabel("%")
plt.title("Accuracy vs Inductance over 50k Cycles of SPEC2006 ")
plt.xticks([x*10E-12 for x in range(2,7)])
plt.legend()
HOME = os.environ['HOME']
file_dir = HOME+ '/plot/intel-1-21-plot.png'
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