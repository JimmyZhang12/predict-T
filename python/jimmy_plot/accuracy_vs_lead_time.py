#ASSUMES DATA WITH THROTTLING, NO DECOR STALL

import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


#PARAMETERS
HOME = os.environ['HOME']
# PREDICTORS = ['HarvardPowerPredictor','DecorOnly','IdealSensor','uArchEventPredictor']
PREDICTOR = 'HarvardPowerPredictor_1'
CLASS = 'DESKTOP'
TEST = 'toast'


stats = open(HOME + '/output_11_4/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt', 'r')
yvar = [0]
action = [False]
VE = [False] 
action_count = 0
VE_count = 0

#read line by line
line = stats.readline()
while line:
    if 'numCycles' in line:
        linespl = line.split()
        num_new_cycles = int(linespl[1])
        for i in range(num_new_cycles):
            yvar.append(None)
            action.append(False)
            VE.append(False)
    elif 'system.cpu.powerPred.supply_voltage' in line and 'system.cpu.powerPred.supply_voltage_dv' not in line:
        linespl = line.split()
        yvar[-1] = float(linespl[1])

        #if moved forward 2 cycles, middle cycle is average of adjacent cycles
        if yvar[-2] == None:
            yvar[-2] = (yvar[-1] + yvar[-3])/2
    
    elif 'system.cpu.powerPred.total_action' in line:
        linespl = line.split()
        action_read = int(linespl[1])
        if action_read > action_count:
            action[-1] = True
            action_count = action_read

    elif 'system.cpu.powerPred.counter'in line:
        linespl = line.split()
        cnt = int(linespl[1])
        if cnt%1000 < 2:
            print(cnt)

    elif 'system.cpu.powerPred.num_voltage_emergency'in line:
        linespl = line.split()
        VE_read = int(linespl[1])

        if VE_read > VE_count:
            VE[-1] = True
            VE_count +=1


    line = stats.readline()


LEAD_TIME_CAP = 100

def accuracy(action,VE):
    bins = dict()
    act_bins = dict()
 
    for i,ve in enumerate(VE):
        if ve:
            for j in range(0,LEAD_TIME_CAP):
                if i-j < 0: break
                if action[i-j]:
                    if j in bins.keys(): bins[j] += 1
                    else: bins[j] = 1
                    break
            for j in range(0,LEAD_TIME_CAP):
                if i-j < 0: break
                if j in act_bins.keys(): act_bins[j] += 1
                else: act_bins[j] = 1

    xvar = [-1]
    hits = [-1]
    false_neg = [-1]
    running_sum = 0
    VE_count = sum(VE)
    for i in sorted(bins):
        running_sum += bins[i]
        false_neg.append(100*(VE_count - running_sum) / VE_count)
        xvar.append(i)
        hits.append(100 * running_sum / VE_count)

    false_pos_x = [-1]
    false_pos = [-1]
    action_count = act_bins[LEAD_TIME_CAP-1]
    for i in sorted(act_bins):
        false_pos.append(100*(action_count - act_bins[i] ) / action_count)
        false_pos_x.append(i)   
        
    for i in range(len(xvar)):
        xvar[i] = xvar[i] + 1 
    for i in range(len(false_pos_x)):
        false_pos_x[i] = false_pos_x[i] + 1
    print(bins)
    print(act_bins)
    return [xvar,hits,false_neg,false_pos_x,false_pos] 


f, (ax1, ax2) = plt.subplots(2, 1)
f.set_size_inches(10.5, 13.5)

xvar,hits,false_neg,false_pos_x,false_pos = accuracy(action,VE)   


ax1.set_xlim([0,max(xvar)])
ax1.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
ax1.plot(xvar, false_neg, color='red', linewidth=1.0, label='false negatives')
ax1.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
ax1.legend()
ax1.set_title('Accuracy Over Lead Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ', CYCLES: ' + str(len(VE)) +')', fontsize=14)
ax1.set_xlabel('Lead Time', fontsize=14) 
ax1.set_ylabel('Accuracy (%)', fontsize=14)

CYCLE_FROM_END = len(action)//2
xvar,hits,false_neg,false_pos_x,false_pos = accuracy(action[0:9800],VE[0:9800])   

ax2.set_xlim([0,max(xvar)])
ax2.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
ax2.plot(xvar, false_neg, color='red', linewidth=1.0, label='false negatives')
ax2.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
ax2.set_title('second half of cycles', fontsize=14)
ax2.set_xlabel('Lead Time', fontsize=14) 
ax2.set_ylabel('Accuracy (%)', fontsize=14)

plt.savefig(HOME+'/plot/11-4_Accuracy_Over_Lead_time' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')
