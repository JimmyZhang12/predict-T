import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util
from statistics import mean
from enum import Enum

#PARAMETERS
HOME = os.environ['HOME']
PREDICTOR = 'HarvardPowerPredictor_1'
CLASS = 'DESKTOP'
TEST = 'crc'
path = HOME + '/output_11_6/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'

#PARAMETERS
SIG_SWEEP = 500
hit_auc = []
false_positive_auc = []
false_negative_auc = []
xvar_auc = []
false_pos_x_auc=[]

for i in range(3,SIG_SWEEP,10):
    SIGNATURE_LENGTH = i
    stats = open(path, 'r')
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

        VE.append(False)
        VE.append(harvard.VEflag)
        action.append(harvard.prev_cycle_predict != -1)
        action.append(harvard.curr_cycle_predict != -1)

    xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE, LEAD_TIME_CAP=50)  
    hit_auc.append(hits)
    false_positive_auc.append(false_pos)
    false_negative_auc.append(false_neg)
    xvar_auc.append(xvar)
    false_pos_x_auc.append(false_pos_x)

xvar_max = max([max(i) for i in xvar_auc])
false_pos_x_auc_max = max([max(i) for i in false_pos_x_auc])

for i in range(len(xvar_auc)):
    if len(hit_auc[i]) < xvar_max:
        hit_auc[i].extend([hit_auc[i][-1]] * (xvar_max-len(hit_auc[i])))        
    if len(false_negative_auc[i]) < xvar_max:
        false_negative_auc[i].extend([false_negative_auc[i][-1]] * (xvar_max-len(false_negative_auc[i])))
    if len(false_positive_auc[i]) < false_pos_x_auc_max:
        false_positive_auc[i].extend([false_positive_auc[i][-1]] * (false_pos_x_auc_max-len(false_positive_auc[i]))) 
for i in range(len(xvar_auc)):
    hit_auc[i] = sum(hit_auc[i])/xvar_max
    false_negative_auc[i] = sum(false_negative_auc[i])/xvar_max
    false_positive_auc[i] = sum(false_positive_auc[i])/false_pos_x_auc_max



f, ax1 = plt.subplots()
f.set_size_inches(10.5, 13.5)

xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE, LEAD_TIME_CAP=50)   
hit_auc = [x - mean(hit_auc) for x in hit_auc] 
false_negative_auc = [x - mean(false_negative_auc) for x in false_negative_auc] 
false_positive_auc = [x - mean(false_positive_auc) for x in false_positive_auc] 
#ax1.set_xlim([0,max(xvar)])
ax1.plot(range(3,SIG_SWEEP,10), hit_auc, color='black', linewidth=1.0, label='hits')
ax1.plot(range(3,SIG_SWEEP,10), false_negative_auc, color='red', linewidth=1.0, label='false negatives')
ax1.plot(range(3,SIG_SWEEP,10), false_positive_auc, color='blue', linewidth=1.0, label='false positives')
ax1.legend()
ax1.set_title('AUC over Signature Length' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST  + str(len(VE)) +')', fontsize=14)
ax1.set_xlabel('Signature Length', fontsize=14) 
plt.savefig(HOME+'/plot/11-4_auc' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')
