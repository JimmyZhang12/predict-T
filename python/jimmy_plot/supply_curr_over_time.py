
import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


#PARAMETERS
HOME = os.environ['HOME']
PREDICTORS = ['HarvardPowerPredictor','DecorOnly','IdealSensor','uArchEventPredictor']
PREDICTOR = 'HarvardPowerPredictor'
CLASS = 'DESKTOP'
TEST = 'qsort'


fig = plt.figure(figsize=(25,5))
ax = plt.axes()

path = HOME + '/output_10_7/gem5_out/' + CLASS + '_' + PREDICTOR + '_1_vector_3/' + TEST + '.txt'
stats = open(path, 'r')
print(path)


yvar = [0]
curr_var = [0]
action_count = 0
VE_count = 0

fig, ax1 = plt.subplots()
fig.set_size_inches(10.5, 7.5)

#read line by line
line = stats.readline()
while line:
    if 'system.cpu.numCycles' in line:
        linespl = line.split()
        num_new_cycles = int(linespl[1])
        for i in range(num_new_cycles):
            yvar.append(None)
            curr_var.append(None)

    elif 'system.cpu.powerPred.supply_voltage' in line and 'system.cpu.powerPred.supply_voltage_dv' not in line:
        linespl = line.split()
        yvar[-1] = float(linespl[1])

        #if moved forward 2 cycles, middle cycle is average of adjacent cycles
        if yvar[-2] == None:
            yvar[-2] = (yvar[-1] + yvar[-3])/2
    
    elif 'system.cpu.powerPred.supply_current' in line:
        linespl = line.split()
        curr_var[-1] = float(linespl[1])

        #if moved forward 2 cycles, middle cycle is average of adjacent cycles
        if curr_var[-2] == None:
            curr_var[-2] = (curr_var[-1] + curr_var[-3])/2
    
    elif 'system.cpu.powerPred.total_action' in line:
        linespl = line.split()
        action_read = int(linespl[1])
        if action_read > action_count:
            action_count = action_read
            ax1.axvspan(len(yvar), len(yvar)+1, color='red', alpha=0.3)
    elif 'system.cpu.powerPred.num_voltage_emergency'in line:
        linespl = line.split()
        VE_read = int(linespl[1])
        if VE_read > VE_count:
            VE_count = VE_read
            ax1.axvspan(len(yvar), len(yvar)+1, color='blue', alpha=0.6)


    line = stats.readline()


start_cycle = 11000
end_cycle = 12000

xvar = np.linspace(0,len(yvar),len(yvar))

fig, ax1 = plt.subplots()
fig.set_size_inches(10.5, 7.5)
color = 'tab:red'
ax1.set_xlabel('cycle')
ax1.set_ylabel('voltage', color=color)
ax1.plot(xvar, yvar, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim([1.32,1.4])

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('current', color=color)  # we already handled the x-label with ax1
ax2.plot(xvar, curr_var, color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim([0,25])


plt.xlim(left = start_cycle, right = end_cycle) 
#plt.ylim(bottom = min(i for i in yvar if i > 0.8), top = max(yvar))
#plt.ylim(bottom = min(i for i in curr_var if i > 3), top = max(yvar))

plt.savefig('10-9_Supply_Voltage_Over_Time_sig=256' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')

print(len(yvar))
print(action_count)
print(VE_count)


        