import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util_dist_pred as util

#PARAMETERS
TEST = 'fft'
HOME = os.environ['HOME']
supply_curr = np.load(HOME + '/passat/12-3_supply_curr' + '_' + TEST +'.npy')
supply_volt = np.load(HOME + '/passat/12-3_supply_volt' + '_' + TEST +'.npy')
predictor_out = np.load(HOME + '/passat/12-3_predictor_out' + '_' + TEST +'.npy')
#PARAMETERS
max_conv = [max(i) for i in predictor_out]

start_cycle = 0
end_cycle = len(max_conv)

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(3, 7)
ax = fig.add_subplot(gs[0, :])
axb = fig.add_subplot(gs[1, :])
axc = fig.add_subplot(gs[2, 0])

FONTSIZE = 18

fig.set_size_inches(35, 10)
fig.suptitle('(Dist_pred)' +  ', DESKTOP, ' + TEST + ' )', fontsize=FONTSIZE)
ax.set_ylabel('Supply Voltage', fontsize=FONTSIZE)
ax2 = ax.twinx()
ax2.set_ylabel('Current', color='tab:blue', fontsize=FONTSIZE)  # we already handled the x-label with ax1

xvar = np.linspace(0,len(supply_volt),len(supply_volt))
start_cycle = 7000    
end_cycle = 8000
ax.set_title('Supply Voltage Over Time', fontsize=FONTSIZE)
ax.plot(xvar, supply_volt,color='black', linewidth=1.0)
ax.set_xlim(left = start_cycle, right = min(end_cycle,len(xvar)) )
ax.set_ylim(bottom = min(i for i in supply_volt if i > 0.8), top = max(supply_volt))

ax2.plot(xvar, supply_curr, color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.set_ylim([min(i for i in supply_curr if i > 0.8), max(supply_curr)])

axb.set_title('Convolution output', fontsize=FONTSIZE)
axb.plot(xvar, max_conv)
axb.set_ylim([0.5,1.3])
axb.set_xlabel('Cycle', fontsize=FONTSIZE) 
axb.set_xlim(left = start_cycle, right = min(end_cycle,len(xvar)) )
axb.set_ylabel('Convolution Max', fontsize=FONTSIZE)  # we already handled the x-label with ax1


VE = []
action = []
V_THRES = 1.358
C_THRES = 0.9
for i in range(1,len(supply_volt)):
    if supply_volt[i] < V_THRES and supply_volt[i-1] > V_THRES:
        ax.axvspan(i, i+1, color='blue', alpha=0.15)
    VE.append(supply_volt[i] < V_THRES and supply_volt[i-1] > V_THRES)
    if max_conv[i] > C_THRES and max_conv[i-1] < C_THRES:
        ax.axvspan(i, i+1, color='RED', alpha=0.3)
    action.append(max_conv[i] > C_THRES and max_conv[i-1] < C_THRES)


print(len(VE))
print(len(action))

xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE, LEAD_TIME_CAP=50)   

axc.set_xlim([3,max(xvar)])
axc.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
axc.plot(xvar, false_neg, color='red', linewidth=1.0, label='false negatives')
axc.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
axc.legend()
axc.set_title('Accuracy', fontsize=14)
axc.set_xlabel('Lead Time', fontsize=14) 
axc.set_ylabel('(%)', fontsize=14)

plt.savefig(HOME+'/passat/plot/11-18_Vs&Is_vs_time' + '_dist_pred_' + TEST +'.png', dpi=300)