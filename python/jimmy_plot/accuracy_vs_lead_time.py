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
TEST = 'qsort'

fig = plt.figure(figsize=(25,5))
ax = plt.axes()

stats = open(HOME + '/output_10_14/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt', 'r')
yvar = [0]
action = [False]
VE     = [False] 
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
            #plt.axvspan(len(yvar), len(yvar)+1, color='red', alpha=0.3)

    #elif 'system.cpu.powerPred.frequency' in line:
    #    linespl = line.split()
    #    freq = int(linespl[1])
    #    if freq == 1750000000:
    #        plt.axvspan(len(yvar), len(yvar)+1, color='red', alpha=0.1)
    

    elif 'system.cpu.powerPred.num_voltage_emergency'in line:
        linespl = line.split()
        VE_read = int(linespl[1])

        if VE_read > VE_count:
            VE[-1] = True
            VE_count +=1
            #plt.axvspan(len(yvar), len(yvar)+1, color='blue', alpha=0.6)


    line = stats.readline()

print(VE_count)

LEAD_TIME_CAP = 100
bins = dict()
ve_ind = 0
action_ind = 0 
for i,ve in enumerate(VE):
    if ve:
        j = 0
        while j < LEAD_TIME_CAP and i-j>=0:
            if action[i-j]:
                if j in bins.keys():
                    bins[j] += 1
                else:
                    bins[j] = 1
                break
            j+=1
            
xvar = []
yvar = []
running_sum = 0
for i in range(LEAD_TIME_CAP):
    if i in bins.keys():
        running_sum += bins[i]
        xvar.append(i)
        yvar.append(100 * running_sum / VE_count)


plt.plot(xvar, yvar,color='black', linewidth=3.0)
fig.suptitle('Accuracy Over Lead Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ' )', fontsize=14)
fig.set_size_inches(7.5, 5.5)
plt.xlabel('Lead Time', fontsize=14) 
plt.ylabel('Accuracy (%)', fontsize=14)
plt.savefig('10-16_Accuracy_Over_Lead_time' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')

print(bins)

#print(len(yvar))
#print(sum(VE))
#print(len(action))

# start_cycle = 30000
# end_cycle = 32000

# xvar = np.linspace(0,len(yvar),len(yvar))

# plt.plot(xvar, yvar,color='black', linewidth=1.0)

# plt.xlim(left = start_cycle, right = end_cycle) 
# plt.ylim(bottom = min(i for i in yvar if i > 0.8), top = max(yvar))

# fig.suptitle('Supply Voltage Over Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ' )', fontsize=14)
# plt.xlabel('Cycle', fontsize=14) 
# plt.ylabel('Supply Voltage', fontsize=14)
# plt.savefig('9-24_Supply_Voltage_Over_Time' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')

# print(action_count)
# print(VE_count)
# print(len(xvar))
# print(sum(VE))


        