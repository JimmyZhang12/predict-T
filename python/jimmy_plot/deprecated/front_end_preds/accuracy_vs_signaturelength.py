#ASSUMES DATA WITH THROTTLING, NO DECOR STALL

import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


#PARAMETERS
HOME = os.environ['HOME']
# PREDICTORS = ['HarvardPowerPredictor','DecorOnly','IdealSensor','uArchEventPredictor']
PREDICTOR = 'HarvardPowerPredictor'
CLASS = 'LAPTOP'
TEST = 'dijkstra'


fig = plt.figure(figsize=(25,5))
ax = plt.axes()
SIG_LENGTH = [32,64,128,256,512]

for SIG_LEN in SIG_LENGTH:
    path = HOME + '/output_9_28/gem5_out/' + CLASS + '_' + PREDICTOR + '_1_no_throttle_on_restore_nodecor_nothrottle_sig' + str(SIG_LEN) + '/' + TEST + '.txt'
    print(path)
    stats = open(path , 'r')

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

    LEAD_TIME_CAP = 512
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
    plt.plot(xvar, yvar, linewidth=1.0, label = str(SIG_LEN))

fig.suptitle('Accuracy Over Lead Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ' )', fontsize=14)
fig.set_size_inches(7.5, 5.5)
plt.xlabel('Lead Time', fontsize=14) 
plt.ylabel('Accuracy (%)', fontsize=14)        
plt.legend()
plt.savefig('9-29_sig_length_sweep' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'.png')



        