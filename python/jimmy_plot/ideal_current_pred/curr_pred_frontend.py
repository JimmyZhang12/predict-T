import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util
from enum import Enum
from datetime import datetime
import math

def calc_plot_stats(PREDICTOR, CLASS, TEST, OUTPUT_DIR, DATE, CYCLE_START, CYCLE_END):
    HOME = os.environ['HOME']
    path = HOME + '/' + OUTPUT_DIR + '/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'
    stats = open(path, 'r')

    harvard = util.Harvard(
        TABLE_HEIGHT=128,
        SIGNATURE_LENGTH=64,
        HYSTERESIS=0.005,
        EMERGENCY_V=1.358,
        LEAD_TIME=20
    )
    cycle_dump = util.Cycle_Dump(stats)

    supply_curr = [0]
    supply_volt = [0]
    VE = [False]

    while True:
        cycle_dump.reset()
        EOF = cycle_dump.parseCycle()
        harvard.tick(cycle_dump)
        if EOF:
            break

        supply_curr.append(None)
        supply_curr.append(cycle_dump.supply_curr)
        supply_curr[-2] = (supply_curr[-1] + supply_curr[-3])/2

        supply_volt.append(None)
        supply_volt.append(cycle_dump.supply_volt)
        supply_volt[-2] = (supply_volt[-1] + supply_volt[-3])/2

        VE.append(False)
        VE.append(harvard.VEflag)

        # if cycle_dump.cycle % 1000 < 3:
        #     print (cycle_dump.cycle)

        if cycle_dump.cycle > CYCLE_END:
            break
        # if cycle_dump.cycle > CYCLE_START: 
        #     cycle_dump.dump()
        #     harvard.print()
        #     input()

        # if (harvard.VEflag or harvard.Actionflag) and cycle_dump.cycle > CYCLE_START: 
        #     cycle_dump.dump()
        #     harvard.print()
        #     input()

    #print how many events 
    for k,v in cycle_dump.event_count.items():
        print(util.event_map[k], ": ", v)

    np.save('plot/data/ideal_curr'+DATE+'_supply_curr_'  + TEST, np.array(supply_curr))
    np.save('plot/data/ideal_curr'+DATE+'_supply_volt_'  + TEST, np.array(supply_volt))
    np.save('plot/data/ideal_curr'+DATE+'_VE_'           + TEST, np.array(VE))


def plot_single(TEST, DATE, start_cycle, end_cycle):
    #PARAMETERS
    FONTSIZE = 18
    HOME = os.environ['HOME']

    supply_curr = np.load('plot/data/ideal_curr'+DATE+'_supply_curr_'  +TEST +'.npy')
    supply_volt = np.load('plot/data/ideal_curr'+DATE+'_supply_volt_'  +TEST +'.npy')
    VE =          np.load('plot/data/ideal_curr'+DATE+'_VE_'+TEST +'.npy')
    action = []

    supply_curr_deriv = np.gradient(supply_curr)
    #harcoded for desktop
    CURR_THRES = 1
    for i in range(len(supply_volt)):
        if(abs(supply_curr_deriv[i] > CURR_THRES)):
            action.append(True)
        else:
            action.append(False)

    end_cycle = min(end_cycle,len(supply_curr))

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(4, 7)
    ax = fig.add_subplot(gs[0, :])
    axb = fig.add_subplot(gs[1, :])
    # axd = fig.add_subplot(gs[2, :])
    axc = fig.add_subplot(gs[2, 0])

    fig.set_size_inches(40, 15)
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
    ax2.set_ylim([min(i for i in supply_curr if i > 0.8), max(supply_curr)])

    axb.set_title('Current Derivative ', fontsize=FONTSIZE)
    axb.plot(xvar, supply_curr_deriv)
    axb.set_xlabel('Cycle', fontsize=FONTSIZE) 
    axb.set_xlim(left = start_cycle, right = end_cycle)


    for i in range(len(supply_volt)):
        if action[i]:
            ax.axvspan(i, i+1, color='red', alpha=0.15)
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

    plt.savefig(HOME+ '/passat/plot/' + DATE + '_Vs&Is_vs_time' + '_ideal_curr_' + TEST +'.png', dpi=300)
    print(HOME+ '/passat/plot/' + DATE + '_Vs&Is_vs_time' + '_ideal_curr_' + TEST +'.png')

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
    ax.set_ylim([0,100])

    ax_fp = fig.add_subplot(gs[1, :])
    ax_fp.set_xticks(x)
    ax_fp.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)
    ax_fp.set_ylim([0,100])

    ax_fn = fig.add_subplot(gs[2, :])
    ax_fn.set_xticks(x)
    ax_fn.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)
    ax_fn.set_ylim([0,100])


    hit_avg = 0
    fp_avg = 0
    fn_avg = 0

    def average(y,x):
        auc = 0
        for i in range(len(y)):
            auc += y[i] * x[i]
        auc /= x[-1]
        return auc

    for x,TEST in enumerate(TEST_LIST):
        print("Plotting: ",TEST)
        VE =          np.load('plot/data/ideal_curr'+DATE+'_VE_'+TEST +'.npy')
        supply_curr = np.load('plot/data/ideal_curr'+DATE+'_supply_curr_'  +TEST +'.npy')

        action = []

        supply_curr_deriv = np.gradient(supply_curr)
        # harcoded for desktop
        CURR_THRES = 1.15
        for i in range(len(supply_curr)):
            if(abs(supply_curr_deriv[i] > CURR_THRES)):
                action.append(True)
            else:
                action.append(False)
        # CURR_THRES = 12
        # for i in range(len(supply_curr)):
        #     if(supply_curr[i] > CURR_THRES and supply_curr[i-1] < CURR_THRES):
        #         action.append(True)
        
        #     else:
        #         action.append(False)
        #correct stat dump being not every cycle

        xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE, LEAD_TIME_CAP=40)   

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

    plt.savefig(HOME+ '/passat/plot/' + DATE + '_all_tests' + '_ideal_curr.png', dpi=300)


if __name__ == "__main__":
    PREDICTOR = 'HarvardPowerPredictor_1'
    CLASS = 'DESKTOP'
    TEST = 'fft'
    OUTPUT_DIR = 'output_12_10'
    DATE = '12-17'
    START_CYCLE = 9050
    END_CYCLE = 30000  

    # calc_plot_stats(PREDICTOR, CLASS, TEST, OUTPUT_DIR, DATE, START_CYCLE, END_CYCLE)
    # PLOT_START_CYCLE = 10000
    # PLOT_END_CYCLE = 15000
    # plot_single(TEST, DATE, PLOT_START_CYCLE, PLOT_END_CYCLE)
    
    # TEST_LIST =["same_cycle", "different_cycle", "basicmath", "bitcnts", 
    #     "qsort", "susan_smooth", "susan_edge", "susan_corner", "dijkstra", "rijndael_decrypt", "sha", "crc", "fft", "ffti", 
    #     "toast", "untoast"]

    # for t in TEST_LIST:
    #     print(t)
    #     calc_plot_stats(PREDICTOR, CLASS, t, OUTPUT_DIR, DATE, START_CYCLE, END_CYCLE)
    # calc_plot_stats(PREDICTOR, CLASS, TEST, OUTPUT_DIR, DATE, START_CYCLE, END_CYCLE)

    TEST_LIST =["same_cycle", "different_cycle", "basicmath", "bitcnts", 
        "qsort", "dijkstra", "sha", "crc", "fft", "ffti", 
        "toast", "untoast", "rijndael_decrypt", "susan_smooth", "susan_edge", "susan_corner"]
    plot_all(TEST_LIST, DATE)




    