import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util_dist_pred as util
from enum import Enum
from datetime import datetime
import math

def calc_plot_stats(PREDICTOR, CLASS, TEST, OUTPUT_DIR, DATE, CYCLE_START, CYCLE_END):
    HOME = os.environ['HOME']
    path = HOME + '/' + OUTPUT_DIR + '/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'
    stats = open(path, 'r')

    dist_pred = util.Dist_Pred(
        HISTORY_WIDTH= 10,
        HYSTERESIS=0.005, 
        EMERGENCY_V=1.358, 
        TABLE_HEIGHT=10, 
        C_THRES=0.7,
        LEAD_TIME = 20)

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

        supply_curr.append(dist_pred.curr_1_cycles_ago)
        supply_curr.append(cycle_dump.supply_curr)
        supply_volt.append(dist_pred.volt_1_cycles_ago)
        supply_volt.append(cycle_dump.supply_volt)
        conf.append(dist_pred.conv_max_norm[-2])
        conf.append(dist_pred.conv_max_norm[-1])
        action.append(dist_pred.Actionflag_prev)
        action.append(dist_pred.Actionflag_curr)
        VE.append(dist_pred.VEflag_prev)
        VE.append(dist_pred.VEflag_curr)

        # print(dist_pred.VEflag_prev)
        # print(dist_pred.VEflag_curr)
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

    np.save('plot/data/conv'+DATE+'_supply_curr_'  + TEST, np.array(supply_curr))
    np.save('plot/data/conv'+DATE+'_supply_volt_'  + TEST, np.array(supply_volt))
    np.save('plot/data/conv'+DATE+'_conf_'  + TEST, np.array(conf))
    np.save('plot/data/conv'+DATE+'_action_'+ TEST, np.array(action))
    np.save('plot/data/conv'+DATE+'_VE_'+ TEST, np.array(VE))


def plot(TEST, DATE, start_cycle, end_cycle):

    #PARAMETERS
    FONTSIZE = 18
    HOME = os.environ['HOME']

    supply_curr = np.load('plot/data/conv'+DATE+'_supply_curr_'  +TEST +'.npy')
    supply_volt = np.load('plot/data/conv'+DATE+'_supply_volt_'  +TEST +'.npy')
    conf =        np.load('plot/data/conv'+DATE+'_conf_'+TEST +'.npy')
    action =      np.load('plot/data/conv'+DATE+'_action_'+TEST +'.npy')
    VE =          np.load('plot/data/conv'+DATE+'_VE_'+TEST +'.npy')

    print(len(supply_curr))
    print(len(supply_volt))

    end_cycle = min(end_cycle,len(supply_curr))

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(4, 7)
    ax = fig.add_subplot(gs[0, :])
    axb = fig.add_subplot(gs[1, :])
    axd = fig.add_subplot(gs[2, :])
    axc = fig.add_subplot(gs[3, 0])

    fig.set_size_inches(35, 15)
    fig.suptitle('(Conv_pred)' +  ', DESKTOP, ' + TEST + ' )', fontsize=FONTSIZE)
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

    #nonlinearity test
    # deriv = np.gradient(conf)
    # conf = np.true_divide(conf,max(conf))
    # conf = conf + np.true_divide(deriv,max(deriv))

    # #conf = np.sin(conf)
    # f = lambda x: (x**3)
    # conf = conf
    # conf = f(conf)


    axb.set_title('Convolution output', fontsize=FONTSIZE)
    axb.plot(xvar, conf)
    # axb.set_ylim([0,2])
    axb.set_xlabel('Cycle', fontsize=FONTSIZE) 
    axb.set_xlim(left = start_cycle, right = end_cycle)
    axb.set_ylabel('Convolution Max', fontsize=FONTSIZE)  # we already handled the x-label with ax1

    
    deriv = np.gradient(conf)
    axd.set_title('Convolution Deriv', fontsize=FONTSIZE)
    axd.plot(xvar, deriv)
    axd.set_ylim([-1,1])
    axd.set_xlabel('Cycle', fontsize=FONTSIZE) 
    axd.set_xlim(left = start_cycle, right = end_cycle)


    # action = []
    # for i in range(len(supply_volt)):
    #     if abs(deriv[i]) > 0.1:
    #         action.append(1)
    #         #ax.axvspan(i, i+1, color='red', alpha=0.15)
    #     else:
    #         action.append(0)

    for i in range(len(supply_volt)):
        if action[i]:
            ax.axvspan(i, i+1, color='red', alpha=0.15)
        if VE[i]:
            ax.axvspan(i, i+1, color='blue', alpha=0.3)

    print('NUM VEs: ', sum(VE))
    print('NUM actions: ', sum(action))

    xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action,VE, LEAD_TIME_CAP=80)   
    axc.set_xlim([3,max(xvar)])
    axc.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
    axc.plot(xvar, false_neg, color='red', linewidth=1.0, label='false negatives')
    axc.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
    axc.legend()
    axc.set_title('Accuracy', fontsize=14)
    axc.set_xlabel('Lead Time', fontsize=14) 
    axc.set_ylabel('(%)', fontsize=14)

    plt.savefig(HOME+ '/passat/plot/' + DATE + '_Vs&Is_vs_time' + '_dist_pred_' + TEST +'.png', dpi=300)
    print(HOME+ '/passat/plot/' + DATE + '_Vs&Is_vs_time' + '_dist_pred_' + TEST +'.png')

def plot_all(TEST_LIST, DATE):
    #PARAMETERS
    FONTSIZE = 12
    HOME = os.environ['HOME']
    x = np.arange(len(TEST_LIST))

    fig = plt.figure(constrained_layout=True)          
    fig.set_size_inches(25, 25)
    fig.suptitle('(Convolution)' +  ', DESKTOP)')

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

    def average(y,x):
        auc = 0
        for i in range(len(y)):
            auc += y[i] * x[i]
        auc /= x[-1]
        return auc
    #PARAMETERS
    FONTSIZE = 18
    HOME = os.environ['HOME']


    for x,TEST in enumerate(TEST_LIST):
        print("Plotting: ",TEST)
        action =      np.load('plot/data/conv'+DATE+'_action_'+TEST +'.npy')
        VE =          np.load('plot/data/conv'+DATE+'_VE_'+TEST +'.npy')

        #correct stat dump being not every cycle
        action = np.roll(action,-1)

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
    ax.set_title('Hit (Max) Average = ' + str(hit_avg), fontsize=FONTSIZE)
    ax_fp.set_title('False Pos (Min) Average = '+ str(fp_avg), fontsize=FONTSIZE)
    ax_fn.set_title('False Neg (Min) Average = '+ str(fn_avg), fontsize=FONTSIZE)

    plt.savefig(HOME+ '/passat/plot/conv' + DATE + 'all_tests.png', dpi=300)
    print(HOME+ '/passat/plot/conv' + DATE + 'all_tests.png')

if __name__ == "__main__":
    PREDICTOR = 'HarvardPowerPredictor_1'
    CLASS = 'DESKTOP'
    OUTPUT_DIR = 'output_12_10'
    DATE = '12-17'
    START_CYCLE = 1
    END_CYCLE = 30000  

    TEST = 'different_cycle'
    # calc_plot_stats(PREDICTOR, CLASS, TEST, OUTPUT_DIR, DATE, START_CYCLE, END_CYCLE)

    PLOT_START_CYCLE = 10000
    PLOT_END_CYCLE = 15000
    plot(TEST, DATE, PLOT_START_CYCLE, PLOT_END_CYCLE)

    # TEST_LIST =["same_cycle", "different_cycle", "basicmath", "bitcnts", 
    #     "qsort", "susan_smooth", "susan_edge", "susan_corner", "dijkstra", "rijndael_decrypt", "sha", "crc", "fft", "ffti", 
    #     "toast", "untoast"]
    # for t in TEST_LIST:
    #     print(t)
    #     calc_plot_stats(PREDICTOR, CLASS, t, OUTPUT_DIR, DATE, START_CYCLE, END_CYCLE)
    # TEST_LIST =["same_cycle", "different_cycle", "basicmath", "bitcnts", 
    #             "qsort", "dijkstra", "sha", "crc", "fft", "ffti", 
    #             "toast", "untoast", "rijndael_decrypt", "susan_smooth", "susan_edge", "susan_corner"]
    # plot_all(TEST_LIST, DATE)


    