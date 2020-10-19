#ASSUMES DATA WITH THROTTLING, NO DECOR STALL

import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


#PARAMETERS
# HOME = os.environ['HOME']
# PREDICTORS = ['HarvardPowerPredictor','DecorOnly','IdealSensor','uArchEventPredictor']
# PREDICTOR = 'HarvardPowerPredictor'
# CLASS = 'LAPTOP'
# TEST = 'fft'


fig = plt.figure(figsize=(25,5))
ax = plt.axes()

stats = open(HOME + '/output_9_10/gem5_out/' + CLASS + '_' + PREDICTOR + '_1_no_throttle_on_restore_2/' + TEST + '.txt', 'r')
yvar = [0]
action_count = 0
VE_count = 0

#read line by line
line = stats.readline()
while line:
    if 'system.cpu.numCycles' in line:
        linespl = line.split()
        num_new_cycles = int(linespl[1])
        for i in range(num_new_cycles):
            yvar.append(None)

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
            action_count = action_read
            plt.axvspan(len(yvar), len(yvar)+1, color='red', alpha=0.3)

    #elif 'system.cpu.powerPred.frequency' in line:
    #    linespl = line.split()
    #    freq = int(linespl[1])
    #    if freq == 1750000000:
    #        plt.axvspan(len(yvar), len(yvar)+1, color='red', alpha=0.1)
    

    elif 'system.cpu.powerPred.num_voltage_emergency'in line:
        linespl = line.split()
        VE_read = int(linespl[1])
        if VE_read > VE_count:
            VE_count = VE_read
            plt.axvspan(len(yvar), len(yvar)+1, color='blue', alpha=0.6)


    line = stats.readline()

start_cycle = 30000
end_cycle = 32000

xvar = np.linspace(0,len(yvar),len(yvar))

plt.plot(xvar, yvar,color='black', linewidth=1.0)

plt.xlim(left = start_cycle, right = end_cycle) 
plt.ylim(bottom = min(i for i in yvar if i > 0.8), top = max(yvar))

fig.suptitle('Supply Voltage Over Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ' )', fontsize=14)
plt.xlabel('Cycle', fontsize=14) 
plt.ylabel('Supply Voltage', fontsize=14)
plt.savefig('9-10_Supply_Voltage_Over_Time_short' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')

print(action_count)
print(VE_count)
print(len(xvar))


        