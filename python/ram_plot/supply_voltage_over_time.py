import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

HOME = os.environ['HOME']
PREDICTORS = ['HarvardPowerPredictor','DecorOnly','IdealSensor','uArchEventPredictor']
PREDICTOR = 'HarvardPowerPredictor'
CLASS = 'DESKTOP'
TEST = 'qsort'

fig = plt.figure(figsize=(25,5))
ax = plt.axes()

stats = open(HOME + '/output_stalloff_throttleon/gem5_out/' + CLASS + '_' + PREDICTOR + '_1_no_throttle_on_restore_2/' + TEST + '.txt', 'r')
yvar = []
action_count = 0
action_history = []


line = stats.readline()
while line:
    if 'system.cpu.powerPred.supply_voltage' in line and 'system.cpu.powerPred.supply_voltage_dv' not in line:
        linespl = line.split()
        yvar.append(float(linespl[1]))
    
    elif 'system.cpu.powerPred.total_action' in line:
        linespl = line.split()
        action_read = float(linespl[1])
        if action_count == action_read:
            action_history.append(False)
        else:
            action_history.append(True)
            action_count = action_read
    line = stats.readline()



start_cycle = 0
#end_cycle = 10000
#yvar = yvar[start_cycle:end_cycle+1]
#action_history = action_history[start_cycle:end_cycle+1]
#xvar = np.linspace(0,end_cycle,num=(end_cycle-start_cycle+1))

xvar = np.linspace(0,10000,10000)

print(xvar)

plt.plot(xvar, yvar,color='black', linewidth=1.0)
for index,action in enumerate(action_history):
    if action:
        plt.axvspan(start_cycle+index, start_cycle+index+1, color='red', alpha=0.5)





fig.suptitle('Supply Voltage Over Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ' )', fontsize=14)
plt.xlabel('Cycle', fontsize=14) 
plt.ylabel('Supply Voltage', fontsize=14)
plt.savefig('9-10_Supply_Voltage_Over_Time' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')

        