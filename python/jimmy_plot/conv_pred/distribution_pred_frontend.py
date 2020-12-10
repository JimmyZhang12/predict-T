import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util_dist_pred as util
from enum import Enum
from datetime import datetime


def calc_plot_stats(PREDICTOR, CLASS, TEST, OUTPUT_DIR, DATE, CYCLE_END):
    HOME = os.environ['HOME']
    path = HOME + '/' + OUTPUT_DIR + '/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'
    stats = open(path, 'r')

    dist_pred = util.Dist_Pred(
        HISTORY_WIDTH= 130,
        HYSTERESIS=0.005, 
        EMERGENCY_V=1.358, 
        TABLE_HEIGHT=20, 
        CONV_RADIUS=2,
        C_THRES=0.9,
        LEAD_TIME = 5)

    cycle_dump = util.Cycle_Dump(stats)

    supply_curr = []
    supply_volt = []
    conf = []
    action = []
    VE = []

    while True:
        cycle_dump.reset()
        EOF = cycle_dump.parseCycle()
        dist_pred.tick(cycle_dump)
        if EOF:
            break

        supply_curr.append(cycle_dump.supply_curr)
        supply_volt.append(cycle_dump.supply_volt)
        conf.append(max(dist_pred.convs_over_table))
        action.append(dist_pred.Actionflag)
        VE.append(dist_pred.VEflag)

        if cycle_dump.cycle % 1000 < 3:
            print (cycle_dump.cycle)

        if cycle_dump.cycle > CYCLE_END:
            break
        # if cycle_dump.cycle > CYCLE_START: 
        #     cycle_dump.dump()
        #     dist_pred.print()
        #     input()

        # if (dist_pred.VEflag or dist_pred.Actionflag) and cycle_dump.cycle > CYCLE_START: 
        #     cycle_dump.dump()
        #     dist_pred.print()
        #     input()

    #print how many events 
    for k,v in cycle_dump.event_count.items():
        print(util.event_map[k], ": ", v)

    np.save('plot/data/'+DATE+'_supply_curr_'  + TEST, np.array(supply_curr))
    np.save('plot/data/'+DATE+'_supply_volt_'  + TEST, np.array(supply_volt))
    np.save('plot/data/'+DATE+'_conf_'  + TEST, np.array(conf))
    np.save('plot/data/'+DATE+'_action_'+ TEST, np.array(action))
    np.save('plot/data/'+DATE+'_VE_'+ TEST, np.array(VE))


def plot(TEST, DATE, start_cycle, end_cycle):

    #PARAMETERS
    FONTSIZE = 18
    HOME = os.environ['HOME']

    supply_curr = np.load('plot/data/'+DATE+'_supply_curr_'  +TEST +'.npy')
    supply_volt = np.load('plot/data/'+DATE+'_supply_volt_'  +TEST +'.npy')
    conf =        np.load('plot/data/'+DATE+'_conf_'+TEST +'.npy')
    action =      np.load('plot/data/'+DATE+'_action_'+TEST +'.npy')
    VE =          np.load('plot/data/'+DATE+'_VE_'+TEST +'.npy')

    end_cycle = min(end_cycle,len(supply_curr))

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(3, 7)
    ax = fig.add_subplot(gs[0, :])
    axb = fig.add_subplot(gs[1, :])
    axc = fig.add_subplot(gs[2, 0])

    fig.set_size_inches(35, 10)
    fig.suptitle('(Dist_pred)' +  ', DESKTOP, ' + TEST + ' )', fontsize=FONTSIZE)
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

    axb.set_title('Convolution output', fontsize=FONTSIZE)
    axb.plot(xvar, conf)
    axb.set_ylim([0,1.3])
    axb.set_xlabel('Cycle', fontsize=FONTSIZE) 
    axb.set_xlim(left = start_cycle, right = end_cycle)
    axb.set_ylabel('Convolution Max', fontsize=FONTSIZE)  # we already handled the x-label with ax1

    for i in range(len(supply_volt)):
        if action[i]:
            ax.axvspan(i, i+1, color='red', alpha=0.15)
        if VE[i]:
            ax.axvspan(i, i+1, color='blue', alpha=0.3)

    print('NUM VEs: ', sum(VE))
    print('NUM actions: ', sum(action))

    xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE, LEAD_TIME_CAP=50)   
    axc.set_xlim([3,max(xvar)])
    axc.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
    axc.plot(xvar, false_neg, color='red', linewidth=1.0, label='false negatives')
    axc.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
    axc.legend()
    axc.set_title('Accuracy', fontsize=14)
    axc.set_xlabel('Lead Time', fontsize=14) 
    axc.set_ylabel('(%)', fontsize=14)

    plt.savefig(HOME+ '/passat/plot/' + DATE + '_Vs&Is_vs_time' + '_dist_pred_' + TEST +'.png', dpi=300)


if __name__ == "__main__":
    PREDICTOR = 'HarvardPowerPredictor_1'
    CLASS = 'DESKTOP'
    TEST = 'fft'
    OUTPUT_DIR = 'output_12_9'
    DATE = '12-9'
    END_CYCLE = 30000
    calc_plot_stats(PREDICTOR, CLASS, TEST, OUTPUT_DIR, DATE, END_CYCLE)

    PLOT_START_CYCLE = 5 
    PLOT_END_CYCLE = 10000
    plot(TEST, DATE, PLOT_START_CYCLE, PLOT_END_CYCLE)


    