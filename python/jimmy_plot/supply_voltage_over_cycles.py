#ASSUMES DATA WITH THROTTLING, NO DECOR STALL

import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


#PARAMETERS
HOME = os.environ['HOME']
PREDICTORS = ['HarvardPowerPredictor_1']
#CLASSES = ['LAPTOP_INTEL_M_','DESKTOP_INTEL_DT_','MOBILE_ARM_']
CLASSES = ["DESKTOP_INTEL_DT_"]

TESTS = ['qsort']
start_cycle = 32000
end_cycle = 35000
commited = False
totals = []
num_issues = 0
num_emergencies = 0
for TEST in TESTS:
    for PREDICTOR in PREDICTORS:
        for CLASS in CLASSES:
            fig = plt.figure(figsize=(25,5))
            ax = plt.axes()

            stats = open(HOME + '/output_10_14/gem5_out/' +TEST+"_10000_2_"+ CLASS + PREDICTOR + '_nodummy/'+ 'stats.txt', 'r')
            yvar_v = [0]
            yvar_i=[0]
            action_count = 0
            VE_count = 0

            #read line by line
            total = 0
            line = stats.readline()
            while line:
                if 'system.cpu.numCycles' in line:
                    linespl = line.split()
                    num_new_cycles = int(linespl[1])
                    total +=num_new_cycles
                    for i in range(num_new_cycles):
                        yvar_v.append(None)
                        yvar_i.append(None)
                elif "system.cpu.powerPred.num_voltage_emergency" in line:
                    linespl = line.split()
                    num_emergencies = linespl[1]
                elif 'system.cpu.powerPred.supply_voltage' in line and 'system.cpu.powerPred.supply_voltage_dv' not in line:
                    linespl = line.split()
                    yvar_v[-1] = float(linespl[1])

                    #if moved forward 2 cycles, middle cycle is average of adjacent cycles
                    if yvar_v[-2] == None:
                        yvar_v[-2] = (yvar_v[-1] + yvar_v[-3])/2

                elif 'system.cpu.powerPred.supply_current' in line:
                    linespl = line.split()
                    yvar_i[-1] = float(linespl[1])

                    #if moved forward 2 cycles, middle cycle is average of adjacent cycles
                    if yvar_i[-2] == None:
                        yvar_i[-2] = (yvar_i[-1] + yvar_i[-3])/2
                
                elif 'system.cpu.powerPred.total_action' in line:
                    linespl = line.split()
                    action_read = int(linespl[1])
                    if action_read > action_count:
                        action_count = action_read
                        plt.axvspan(len(yvar_v), len(yvar_v)+1, color='blue', alpha=0.3)
                
                elif 'system.cpu.powerPred.num_voltage_emergency'in line:
                    linespl = line.split()
                    VE_read = int(linespl[1])
                    if VE_read > VE_count:
                        VE_count = VE_read
                        # plt.axvspan(len(yvar_v), len(yvar_v)+1, color='red', alpha=0.3)

                elif "system.cpu.powerPred.state" in line:
                    linespl = line.split()
                    state = int(linespl[1])
                    if state==3:
                        plt.axvspan(len(yvar_v), len(yvar_v)+1, color='red', alpha=0.15)
                    if state==2:
                        plt.axvspan(len(yvar_v), len(yvar_v)+1, color='yellow', alpha=0.15)
                        if commited:
                            num_issues+=1
                            #print("issues with stall")
                elif "system.cpu.commit.committedOps" in line:
                    linespl = line.split()
                    number_commited = int(linespl[1])
                    if (number_commited>0):
                        commited = True
                    else:
                        commited = False
                line = stats.readline()

            totals.append(total)
            print(num_issues)
            print(num_emergencies)
            xvar = np.linspace(0,len(yvar_v),len(yvar_v))

            plt.plot(xvar, yvar_v,color='black', linewidth=1.0)
            plt.ylim(bottom = min(i for i in yvar_v if i > 0.8), top = max(yvar_v))

            
            fig.suptitle('Supply Voltage Over Time' + '(' + PREDICTOR + ', ' + CLASS + ', ' + TEST + ' )', fontsize=14)
            plt.xlabel('Cycle', fontsize=14) 
            plt.ylabel('Supply Voltage', fontsize=14)

            ax2 = ax.twinx()

            color = 'tab:blue'
            ax2.set_ylabel('Current', color=color)  # we already handled the x-label with ax1
            ax2.plot(xvar, yvar_i, color=color)
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.set_ylim([min(i for i in yvar_i if i > 0.8), max(yvar_i)])

            #plt.savefig('Images/9-18_Supply_Voltage_Over_Time' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'_half_thr.png', dpi=300)
            plt.xlim(left = start_cycle, right = end_cycle) 
            plt.savefig('9-27_Supply_Volt+Curr_Over_Time' + '_' + PREDICTOR + '_' + CLASS + '_' + TEST +'_0.5.png', dpi=300)

            print(totals)