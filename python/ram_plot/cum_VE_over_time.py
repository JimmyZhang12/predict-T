import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

HOME = os.environ['HOME']
PREDICTORS = ['HarvardPowerPredictor','DecorOnly']
#PREDICTOR = 'uArchEventPredictor'
CLASS = 'LAPTOP'
TEST = 'qsort'

fig = plt.figure()
ax = plt.axes()

for PREDICTOR in PREDICTORS:
    print(PREDICTOR)
    stats = open(HOME + '/output/gem5_out/' + CLASS + '_' + PREDICTOR + '_1_no_throttle_on_restore_2/' + TEST + '.txt', 'r')
    cum_voltage_emer = []

    line = stats.readline()
    while line:
        if 'system.cpu.powerPred.num_voltage_emergency' in line:
            linespl = line.split()
            cum_voltage_emer.append(int(linespl[1]))
        line = stats.readline()

    xvar = np.linspace(0,len(cum_voltage_emer),num=len(cum_voltage_emer)).tolist()
    plt.plot(xvar, cum_voltage_emer)





fig.suptitle('Cumulative Voltage Emergencies over Time' + '(' + CLASS + ', ' + TEST + ' )', fontsize=12)
plt.xlabel('Cycle', fontsize=12)
plt.ylabel('Count', fontsize=12)
ax.legend(PREDICTORS)

plt.savefig('Cumulative_VE_' + CLASS + '_' + TEST + '.png')

        