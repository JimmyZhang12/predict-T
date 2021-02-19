import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

HOME = os.environ['HOME']
PREDICTORS = ['HarvardPowerPredictor','DecorOnly','IdealSensor','uArchEventPredictor']
PREDICTOR = 'HarvardPowerPredictor'
CLASS = ['DESKTOP','MOBILE','LAPTOP']
CLASS = 'MOBILE'
TEST = 'dijkstra'

fig = plt.figure()
ax = plt.axes()


print(PREDICTOR)

stat_path = HOME + '/output_9_24/gem5_out/' + CLASS + '_' + PREDICTOR + '_1_no_throttle_on_restore_2_9-24_nodecor_yesthrottle/' + TEST + '.txt'
plot_name = HOME + '/plot/9-24_Cumulative_VE_0.2freq' + CLASS + '_' + TEST + '.png'

#stat_path = HOME + '/output/gem5_out/' + CLASS + '_' + PREDICTOR + '_1_no_throttle_on_restore_2/' + TEST + '.txt'
#plot_name = HOME + '/plot/9-24_Cumulative_VE' + CLASS + '_' + TEST + '.png'

stats = open(stat_path, 'r')
print(stat_path)
cum_voltage_emer = []

line = stats.readline()
while line:
    if 'system.cpu.powerPred.num_voltage_emergency' in line:
        linespl = line.split()
        cum_voltage_emer.append(int(linespl[1]))
    line = stats.readline()

xvar = np.linspace(0,len(cum_voltage_emer),num=len(cum_voltage_emer)).tolist()
print(max(cum_voltage_emer))
plt.plot(xvar, cum_voltage_emer)


fig.suptitle('Cumulative Voltage Emergencies over Time' + '(' + CLASS + ', ' + TEST + ' )', fontsize=12)
plt.xlabel('Cycle', fontsize=12)
plt.ylabel('Count', fontsize=12)
ax.legend(PREDICTORS)

print(plot_name)

print(max(cum_voltage_emer))
#plt.savefig(plot_name)

        