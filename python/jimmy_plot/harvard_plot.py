import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import harvard
import util
from enum import Enum
from datetime import datetime
import math


#mi optimal
L = 20e-12
C = 1.32e-06 
R =  0.0032
#spec optimal
# L = 2e-11  
# C = 7.6e-07  
# R = 0.0041
def calc_plot_stats(stats, CYCLE_START, CYCLE_END, IDENTIFIER):
    pdn = util.PDN(
        L = L,
        C = C,
        R = R,
        VDC = 1.4,
        CLK = 4E9,
    )
    harvard_pred = harvard.Harvard(
        TABLE_HEIGHT=30,
        SIGNATURE_LENGTH=32,
        HYSTERESIS=0.005,
        EMERGENCY_V= 0.96*1.4,
        LEAD_TIME=40
    )
    cycle_dump = util.Cycle_Dump(stats)

    supply_curr = [0]
    supply_volt = [0]
    action = [False]
    VE = [False]

    while True:
        cycle_dump.reset()
        EOF = cycle_dump.parseCycle()

        if EOF:
            break
        else:
            # voltage = pdn.get_curr(cycle_dump.supply_curr)
            # cycle_dump.supply_volt = voltage
            harvard_pred.tick(cycle_dump)

        supply_curr.append(cycle_dump.supply_curr)
        supply_volt.append(cycle_dump.supply_volt)
        action.append(harvard_pred.cycle_predict != -1)
        VE.append(harvard_pred.VEflag)

        if cycle_dump.cycle > CYCLE_END and CYCLE_END != -1:
            break


        # if cycle_dump.cycle % 1000 < 3:
        #     print (cycle_dump.cycle)

        # if cycle_dump.cycle > CYCLE_START: 
        #     cycle_dump.dump()
        #     harvard_pred.print()
        #     input()

        # if (harvard_pred.VEflag or harvard_pred.Actionflag) and cycle_dump.cycle > CYCLE_START: 
        #     cycle_dump.dump()
        #     harvard_pred.print()
        #     input()

    # print("EVENTS from stat dump")
    # for k,v in harvard_pred.event_count.items():
    #     print(harvard.valid_events[k], ": ", v)

    
    HOME = os.environ['HOME']
    np.save(HOME+'/plot/data/harvard_'+IDENTIFIER+'_supply_curr_'  + TEST, np.array(supply_curr))
    np.save(HOME+'/plot/data/harvard_'+IDENTIFIER+'_supply_volt_'  + TEST, np.array(supply_volt))
    np.save(HOME+'/plot/data/harvard_'+IDENTIFIER+'_action_'       + TEST, np.array(action))
    np.save(HOME+'/plot/data/harvard_'+IDENTIFIER+'_VE_'           + TEST, np.array(VE))


def plot_single(TEST, DATE, start_cycle, end_cycle):
    #PARAMETERS
    FONTSIZE = 18
    HOME = os.environ['HOME']

    supply_curr = np.load(HOME+'/plot/data/harvard_'+DATE+'_supply_curr_'  +TEST +'.npy')
    supply_volt = np.load(HOME+'/plot/data/harvard_'+DATE+'_supply_volt_'  +TEST +'.npy')
    action =      np.load(HOME+'/plot/data/harvard_'+DATE+'_action_'+TEST +'.npy')
    VE =          np.load(HOME+'/plot/data/harvard_'+DATE+'_VE_'+TEST +'.npy')

    print(len(supply_volt))

    end_cycle = min(end_cycle,len(supply_curr))

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2, 3)
    ax = fig.add_subplot(gs[0, :])
    # axb = fig.add_subplot(gs[1, :])
    # axd = fig.add_subplot(gs[2, :])
    axc = fig.add_subplot(gs[1, 0])

    fig.set_size_inches(15, 7.5)
    fig.suptitle('(Harvard)' +  ', DESKTOP, ' + TEST + ' )', fontsize=FONTSIZE)
    ax.set_ylabel('Supply Voltage', fontsize=FONTSIZE)
    ax2 = ax.twinx()
    ax2.set_ylabel('Current', color='tab:blue', fontsize=FONTSIZE)  # we already handled the x-label with ax1

    xvar = np.linspace(0,len(supply_volt),len(supply_volt))

    ax.set_title('Supply Voltage Over Time', fontsize=FONTSIZE)
    ax.plot(xvar, supply_volt,color='black', linewidth=1.0)
    ax.set_xlim(left = start_cycle, right = end_cycle)
    ax.set_ylim(bottom = min(i for i in supply_volt if i > 0.8), top = max(supply_volt))
    ax2.plot(xvar, supply_curr, color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_ylim([5,40])

    for i in range(len(supply_volt)):
        # if action[i]:
        #     ax.axvspan(i, i+1, color='red', alpha=0.15)
        if VE[i]:
            ax.axvspan(i, i+1, color='blue', alpha=0.3)

    print('NUM VEs: ', sum(VE))
    print('NUM actions: ', sum(action))

    xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE, LEAD_TIME_CAP=80)   
    axc.set_xlim([0,max(xvar[-1],false_pos_x[-1])])
    axc.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
    axc.plot(xvar, false_neg, color='red', linewidth=1.0, label='false negatives')
    axc.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
    axc.legend()
    axc.set_title('Accuracy', fontsize=14)
    axc.set_xlabel('Lead Time', fontsize=14) 
    axc.set_ylabel('(%)', fontsize=14)

    file_dir = HOME+ '/plot/' + DATE + '_Vs&Is_vs_time' + '_harvard_' + TEST +'.png'
    plt.savefig(file_dir, dpi=300)
    print(file_dir)

def plot_all(TEST_LIST, DATE):
    #PARAMETERS
    FONTSIZE = 12
    HOME = os.environ['HOME']
    x = np.arange(len(TEST_LIST))

    fig = plt.figure(constrained_layout=True)          
    fig.set_size_inches(25, 25)
    fig.suptitle('(Harvard)' +  ', DESKTOP)')

    gs = fig.add_gridspec(4, 5)

    ax = fig.add_subplot(gs[0, :])
    ax.set_xticks(x)
    ax.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)

    ax_fp = fig.add_subplot(gs[1, :])
    ax_fp.set_xticks(x)
    ax_fp.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)

    ax_fn = fig.add_subplot(gs[2, :])
    ax_fn.set_xticks(x)
    ax_fn.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)

    hit_avg = 0
    fp_avg = 0
    fn_avg = 0

    for x,TEST in enumerate(TEST_LIST):
        print("Plotting: ",TEST)
        HOME = os.environ['HOME']
        action =      np.load(HOME+'/plot/data/harvard_'+DATE+'_action_'+TEST +'.npy')
        VE =          np.load(HOME+'/plot/data/harvard_'+DATE+'_VE_'+TEST +'.npy')

        #correct stat dump being not every cycle
        action = np.roll(action,-1)

        xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action[-20000:],VE[-20000:], LEAD_TIME_CAP=40)   

        ax.bar(x,max(hits), color = 'RED')
        ax_fp.bar(x,min(false_pos), color = 'RED')
        ax_fn.bar(x,min(false_neg), color = 'RED')

        hit_avg += max(hits)
        fp_avg += min(false_pos)
        fn_avg += min(false_neg)
    hit_avg /= len(TEST_LIST)
    fp_avg /= len(TEST_LIST)
    fn_avg /= len(TEST_LIST)
    ax.set_title('Hit (Max) Average = ' + str(hit_avg), fontsize=FONTSIZE*2)
    ax_fp.set_title('False Pos (Min) Average = '+ str(fp_avg), fontsize=FONTSIZE*2)
    ax_fn.set_title('False Neg (Min) Average = '+ str(fn_avg), fontsize=FONTSIZE*2)

    plt.savefig(HOME+ '/plot/' + DATE + '_all_tests' + '_harvard.png', dpi=300)

def global_avg(TEST_LIST, DATE):
    #PARAMETERS
    hit_avg = 0
    fp_avg = 0
    fn_avg = 0

    for x,TEST in enumerate(TEST_LIST):
        HOME = os.environ['HOME']
        action =      np.load(HOME+'/plot/data/harvard_'+DATE+'_action_'+TEST +'.npy')
        VE =          np.load(HOME+'/plot/data/harvard_'+DATE+'_VE_'+TEST +'.npy')

        xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE, LEAD_TIME_CAP=40)   

        hit_avg += max(hits)
        fp_avg += min(false_pos)
        fn_avg += min(false_neg)

    hit_avg /= len(TEST_LIST)
    fp_avg /= len(TEST_LIST)
    fn_avg /= len(TEST_LIST)

    return hit_avg, fp_avg, fn_avg


if __name__ == "__main__":
    HOME = os.environ['HOME']
    OUTPUT_DIR = 'output_1_20'
    NUM_INSTR = '2000'
    VERSION = '1'
    PDN = 'DESKTOP_INTEL_DT'
    PREDICTOR = 'HarvardPowerPredictor_1'
    IDENTIFIER = "1-20"

    # IDENTIFIER = "spec_1-11"
    # NUM_INSTR = "10000000000"
    # OUTPUT_DIR = 'spec_output_1_7'

    TEST = 'crc'
    path = HOME+'/'+OUTPUT_DIR+'/gem5_out/'+TEST+'_'+NUM_INSTR+'_'+VERSION+'_'+PDN+'_'+PREDICTOR+'/stats.txt'
    print(path)
    stats = open(path, 'r')
    calc_plot_stats(stats, CYCLE_START=0, CYCLE_END=-1, IDENTIFIER=IDENTIFIER)
    # for TEST in util.TEST_LIST_mi:
    plot_single(TEST, IDENTIFIER, start_cycle=0, end_cycle=20000)
    


    # for TEST in util.TEST_LIST_spec:
    #     path = HOME+'/'+OUTPUT_DIR+'/gem5_out/'+TEST+'_'+NUM_INSTR+'_'+VERSION+'_'+PDN+'_'+PREDICTOR+'/stats.txt'
    #     print(path)
    #     stats = open(path, 'r')
    #     calc_plot_stats(stats, CYCLE_START=1000, CYCLE_END=-1, IDENTIFIER=IDENTIFIER)
    # plot_all(util.TEST_LIST_spec, IDENTIFIER)

# R = 3.2E-3
# L = 25E-12
# C = 0.9E-6
    # averages = []
    # for l in range(1,6):
    #     for c in range(1,6):
    #         for r in range(1,6):
    #             L = 10E-12 + l * ((60E-12 - 10E-12)/5)
    #             C = 0.2E-6 + c * ((3E-6 - 0.2E-6)/5)
    #             R = 0.5E-3 + r * ((5E-3 - 0.5E-3)/5)
    #             print(l," ",c," ",r," of ", 5**3)

    #             for TEST in util.TEST_LIST_spec:
    #                 path = HOME+'/'+OUTPUT_DIR+'/gem5_out/'+TEST+'_'+NUM_INSTR+'_'+VERSION+'_'+PDN+'_'+PREDICTOR+'/stats.txt'
    #                 stats = open(path, 'r')
    #                 print(TEST)
    #                 calc_plot_stats(stats, CYCLE_START=1000, CYCLE_END=-1, IDENTIFIER=IDENTIFIER)
    #             hit_avg, fp_avg, fn_avg = global_avg(util.TEST_LIST_spec, IDENTIFIER)
    #             averages.append([l,c,r,hit_avg, fp_avg, fn_avg])

    #             np.save(HOME+'/plot/data/PDN_SWEEP_HARVARD_spec', np.array(averages))

    
                




    