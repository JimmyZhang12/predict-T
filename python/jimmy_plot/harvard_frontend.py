import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util
from enum import Enum

#PARAMETERS
HOME = os.environ['HOME']
PREDICTOR = 'HarvardPowerPredictor_1'
CLASS = 'DESKTOP'
TEST = 'different_cycle'
path = HOME + '/output_11_11_2/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'
stats = open(path, 'r')
#PARAMETERS

CYCLE_START = 2000
SIGNATURE_LENGTH = 32
harvard = util.Harvard(TABLE_HEIGHT=128,SIGNATURE_LENGTH=SIGNATURE_LENGTH,HYSTERESIS=0.005,EMERGENCY_V=1.358)
cycle_dump = util.Cycle_Dump(stats)
action = [False]
VE = [False]

while True:
    cycle_dump.reset()
    EOF = cycle_dump.parseCycle()
    harvard.tick(cycle_dump)
    if EOF:
        break

    if cycle_dump.cycle % 1000 < 3:
        print (cycle_dump.cycle)
    # if cycle_dump.cycle > CYCLE_START: 
    #     cycle_dump.dump()
    #     harvard.print()
    #     input()

    if (harvard.VEflag or harvard.Actionflag) and cycle_dump.cycle > CYCLE_START: 
        cycle_dump.dump()
        harvard.print()
        input()

    VE.append(False)
    VE.append(harvard.VEflag)
    action.append(harvard.prev_cycle_predict != -1)
    action.append(harvard.curr_cycle_predict != -1)

print(sum(VE))
print(sum(action))

f, (ax1) = plt.subplots()
f.set_size_inches(10.5, 8.5)

xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE, LEAD_TIME_CAP=50)   

ax1.set_xlim([0,max(xvar)])
ax1.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
ax1.plot(xvar, false_neg, color='red', linewidth=1.0, label='false negatives')
ax1.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
ax1.legend()
ax1.set_title('Accuracy Over Lead Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST  + str(len(VE)) +')', fontsize=14)
ax1.set_xlabel('Lead Time', fontsize=14) 
ax1.set_ylabel('Accuracy (%)', fontsize=14)

# CYCLE_FROM_END = len(action)//2
# xvar,hits,false_neg,false_pos_x,false_pos = accuracy(action[0:9800],VE[0:9800])   

# ax2.set_xlim([0,max(xvar)])
# ax2.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
# ax2.plot(xvar, false_neg, color='red', linewidth=1.0, label='false negatives')
# ax2.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
# ax2.set_title('second half of cycles', fontsize=14)
# ax2.set_xlabel('Lead Time', fontsize=14) 
# ax2.set_ylabel('Accuracy (%)', fontsize=14)

plt.savefig(HOME+'/passat/plot/11-10_frontend_Acc_vs_LT' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')

        