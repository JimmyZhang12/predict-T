#ASSUMES DATA WITH THROTTLING, NO DECOR STALL

import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

class Cycle_Dump:
    def __init__(self):
        self.ve_count = 0
        self.action_count = 0
        return

    def reset(self):
        self.ve_flag = False
        self.ve_flag_prev = []
        self.action_flag = False
        self.cycle = None
        self.supply_curr = None
        self.supply_volt = None
        self.pred_state = None
        self.numCycles_var = None
        return

    def num_voltage_emergency(self, line):
        linespl = line.split()
        ve_read = int(linespl[1])
        if ve_read > self.ve_count:
            self.ve_count = ve_read
            self.ve_flag = True
        return
    def total_action(self, line):
        linespl = line.split()
        action_read = int(linespl[1])
        if action_read > self.action_count:
            self.action_count = action_read
            self.action_flag = True
        return
    def counter(self, line):
        linespl = line.split()
        self.cycle = int(linespl[1])
        return
    def state(self, line):
        linespl = line.split()
        self.pred_state = int(linespl[1])
        return
    def supply_current(self, line):
        linespl = line.split()
        self.supply_curr = float(linespl[1])
        return
    def supply_voltage(self, line):
        linespl = line.split()
        self.supply_volt = float(linespl[1])
        return
    def numCycles(self,line):
        linespl = line.split()
        self.numCycles_var = int(linespl[1])
        return
    #PARAMETERS
HOME = os.environ['HOME']
PREDICTOR = 'HarvardPowerPredictor_1'
CLASS = 'DESKTOP'
TEST = 'different_cycle'
path = HOME + '/output_11_18/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'
print(path)
#PARAMETERS
stats = open(path, 'r')

fig = plt.figure(figsize=(10,5))
ax = plt.axes()
fig.suptitle('Supply Voltage Over Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ' )', fontsize=14)
ax.set_xlabel('Cycle', fontsize=14) 
ax.set_ylabel('Supply Voltage', fontsize=14)
ax2 = ax.twinx()
ax2.set_ylabel('Current', color='tab:blue')  # we already handled the x-label with ax1
voltage = [0]
current =[0]

#read line by lin
line = stats.readline()
line = stats.readline()

cycle_dump = Cycle_Dump()
while line:
    cycle_dump.reset()
    while(True):   
        #one cycle worth of stat dumps    
        if 'Begin Simulation Statistics' in line or not line:
            break
        stat_name = line.split()[0].split('.')[-1].split(':')[0]
        func = getattr(cycle_dump, stat_name, False)
        if func:
            func(line)
        line = stats.readline()   
    
    for _ in range(cycle_dump.numCycles_var):
        voltage.append(None)
        current.append(None)
    #implicit assumption stat dumps are every 2 cycles
    voltage[-1] = cycle_dump.supply_volt
    current[-1] = cycle_dump.supply_curr
    voltage[-2] = (voltage[-1]+voltage[-3])/2
    current[-2] = (current[-1]+current[-3])/2
    if cycle_dump.ve_flag:
        ax.axvspan(len(voltage), len(voltage)+1, color='blue', alpha=0.15)
    #if cycle_dump.action_flag:
    #    ax.axvspan(len(voltage), len(voltage)+1, color='red', alpha=0.3)
    line = stats.readline()
    if cycle_dump.cycle > 10000:
        break

xvar = np.linspace(0,len(voltage),len(voltage))
start_cycle = 8000
end_cycle = 8500
ax.plot(xvar, voltage,color='black', linewidth=1.0)
ax.set_ylim(bottom = min(i for i in voltage if i > 0.8), top = max(voltage))

ax2.plot(xvar, current, color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.set_ylim([min(i for i in current if i > 0.8), max(current)])

plt.xlim(left = start_cycle, right = end_cycle)
plt.savefig(HOME +'/passat/plot/11-18_Supply_Volt+Curr_Over_Time' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png', dpi=300)
