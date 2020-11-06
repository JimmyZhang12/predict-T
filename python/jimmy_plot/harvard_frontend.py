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
TEST = 'toast'
path = HOME + '/output_11_4/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'
stats = open(path, 'r')
#PARAMETERS

CYCLE_START = 0
harvard = util.Harvard(10,10,0.005,1.358)
cycle_dump = util.Cycle_Dump(stats)
action = [False]
VE = [False]

while True:
    cycle_dump.reset()
    cycle_dump.parseCycle()
    EOF = harvard.tick(cycle_dump)

    if cycle_dump.cycle % 1000 < 3:
        print (cycle_dump.cycle)
    if cycle_dump.cycle > CYCLE_START: 
        cycle_dump.dump()
        print('______________________')
        harvard.print()
        input() 

    # VE.append(False)
    # if harvard.insertIndex != False and harvard.insertIndex_prev != False:
    #     VE.append(True)

    # if harvard.cycle1_prediction != False:
    #     action.append(True)
    # else:
    #     action.append(False)
    # if harvard.cycle2_prediction != False:
    #     action.append(True)
    # else:
    #     action.append(False)

    if EOF:
        break
    



f, (ax1, ax2) = plt.subplots(2, 1)
f.set_size_inches(10.5, 13.5)

xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE)   

ax1.set_xlim([0,max(xvar)])
ax1.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
ax1.plot(xvar, false_neg, color='red', linewidth=1.0, label='false negatives')
ax1.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
ax1.legend()
ax1.set_title('Accuracy Over Lead Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ', CYCLES: ' + str(len(VE)) +')', fontsize=14)
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

# plt.savefig(HOME+'/plot/11-4_frontend_Accuracy_Over_Lead_time' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')

        