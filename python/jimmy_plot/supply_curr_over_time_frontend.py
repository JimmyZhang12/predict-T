#ASSUMES DATA WITH THROTTLING, NO DECOR STALL

import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util

#PARAMETERS
HOME = os.environ['HOME']
PREDICTOR = 'HarvardPowerPredictor_1'
CLASS = 'DESKTOP'
TEST = 'fft'
path = HOME + '/output_11_6/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'
stats = open(path, 'r')
#PARAMETERS


fig = plt.figure(figsize=(120,5))
ax = plt.axes()
fig.suptitle('Supply Voltage Over Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ' )', fontsize=14)
ax.set_xlabel('Cycle', fontsize=14) 
ax.set_ylabel('Supply Voltage', fontsize=14)
ax2 = ax.twinx()
ax2.set_ylabel('Current', color='tab:blue')  # we already handled the x-label with ax1
voltage = [0]
current =[0]

CYCLE_START = 0
SIGNATURE_LENGTH = 600
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
    
    for _ in range(2): #TODO dont hardcode this to 2
        voltage.append(None)
        current.append(None)
    #implicit assumption stat dumps are every 2 cycles
    voltage[-1] = cycle_dump.supply_volt
    current[-1] = cycle_dump.supply_curr
    voltage[-2] = (voltage[-1]+voltage[-3])/2
    current[-2] = (current[-1]+current[-3])/2
    if harvard.VEflag:
        ax.axvspan(len(voltage), len(voltage)+1, color='blue', alpha=0.15)
    if harvard.Actionflag:
       ax.axvspan(len(voltage), len(voltage)+1, color='red', alpha=0.3)

xvar = np.linspace(0,len(voltage),len(voltage))
start_cycle = 1000
end_cycle = 41000
ax.plot(xvar, voltage,color='black', linewidth=1.0)
ax.set_ylim(bottom = min(i for i in voltage if i > 0.8), top = max(voltage))

ax2.plot(xvar, current, color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.set_ylim([min(i for i in current if i > 0.8), max(current)])

plt.xlim(left = start_cycle, right = end_cycle)
plt.savefig(HOME+'/passat/plot/11-10_Vs&Is_vs_time' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'_0.5.png', dpi=300)

