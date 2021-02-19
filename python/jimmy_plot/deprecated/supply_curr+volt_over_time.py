#ASSUMES DATA WITH THROTTLING, NO DECOR STALL

import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

class Cycle_Dump:
    stat = None
    supply_current = None
    supply_voltage = None

    def __init__(self, stats):
        self.stats = stats
        self.stats.readline()

    def getValue(self, line):
        linespl = line.split()
        return float(linespl[1])

    # statToFunc = {
    #     "system.cpu.powerPred.supply_current" : (getValue, supply_current),
    #     "system.cpu.powerPred.supply_voltage" : (getValue, supply_voltage)
    # }

    def parseCycle(self):
        while(True):
            line = self.stats.readline()
                   
            if not line:
                return True
            #end of 1 cycle of stat dump    
            elif (not line.upper().isupper()):
                for _ in range(4):
                    self.stats.readline()
                return False
            else:
                stat_name = line.split()[0].split(':')[0]
                #if stat_name in self.statToFunc.keys():
                if stat_name == "system.cpu.powerPred.supply_current":
                    self.supply_current = self.getValue(line)
                elif stat_name == "system.cpu.powerPred.supply_voltage":
                    self.supply_voltage = self.getValue(line)


    def dump(self):
        print('******* CYCLE: ',self.cycle,'*********')
        print('SUPPLY CURRENT: ', self.supply_curr)
        print('SUPPLY VOLTAGE: ', self.supply_volt)

#PARAMETERS
HOME = os.environ['HOME']
OUTPUT_DIR = 'output_1_6'
TEST = 'crc'
NUM_INSTR = '1001'
VERSION = '1'
PDN = 'DESKTOP_INTEL_DT'
PREDICTOR = 'HarvardPowerPredictor_1'
path = HOME+'/'+OUTPUT_DIR+'/gem5_out/'+TEST+'_'+NUM_INSTR+'_'+VERSION+'_'+PDN+'_'+PREDICTOR+'/stats.txt'
print(path)
stats = open(path, 'r')

start_cycle = 0
end_cycle = 1000
#END PARAMETERS

fig = plt.figure(figsize=(60,5))
ax = plt.axes()
fig.suptitle('Supply Voltage Over Time' + '(' + PREDICTOR + ', ' + PDN + ', ' + TEST + ' )', fontsize=14)
ax.set_xlabel('Cycle', fontsize=18) 
ax.set_ylabel('Supply Voltage', fontsize=18)
ax2 = ax.twinx()
ax2.set_ylabel('Current', color='tab:blue', fontsize=18)  # we already handled the x-label with ax1
voltage = [0]
current =[0]

cycle_dump = Cycle_Dump(stats)
while True:
    EOF = cycle_dump.parseCycle()
    if EOF:
        break

    voltage.append(cycle_dump.supply_voltage)
    current.append(cycle_dump.supply_current)

xvar = np.linspace(0,len(voltage),len(voltage))

ax.plot(xvar, voltage,color='black', linewidth=1.0)
ax.set_ylim(bottom = min(i for i in voltage if i > 0.8), top = max(voltage))

ax2.plot(xvar, current, color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.set_ylim([min(i for i in current if i > 0.8), max(current)])

plt.xlim(left = start_cycle, right = min(end_cycle,len(xvar)) )
plt.savefig(HOME+'/plot/1-6_1x_Vs&Is_vs_time_' + PDN + '_' + TEST +'.png', dpi=300)

