import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util_dist_pred as util
from enum import Enum
from datetime import datetime
import math

def calc_plot_stats(stats, CYCLE_START, CYCLE_END, IDENTIFIER):

    dist_pred = util.Dist_Pred(
        HISTORY_WIDTH= 10,
        HYSTERESIS=0.005, 
        EMERGENCY_V=1.358, 
        TABLE_HEIGHT=25, 
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
        if EOF:
            break
        else:
            dist_pred.tick(cycle_dump)


        supply_curr.append(cycle_dump.supply_curr)
        supply_volt.append(cycle_dump.supply_volt)
        conf.append(dist_pred.conv_max_norm[-1])
        action.append(dist_pred.Actionflag_curr)
        VE.append(dist_pred.VEflag_curr)

        # print(dist_pred.VEflag_prev)
        # print(dist_pred.VEflag_curr)
        if cycle_dump.cycle % 1000 < 1:
            print (cycle_dump.cycle)

        if cycle_dump.cycle > CYCLE_END and CYCLE_END != -1:
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
        print(util.event_map_pred[k], ": ", v)
        
    HOME = os.environ['HOME']
    np.save(HOME+'/plot/data/conv'+IDENTIFIER+'_supply_curr_'  + TEST, np.array(supply_curr))
    np.save(HOME+'/plot/data/conv'+IDENTIFIER+'_supply_volt_'  + TEST, np.array(supply_volt))
    np.save(HOME+'/plot/data/conv'+IDENTIFIER+'_conf_'  + TEST, np.array(conf))
    np.save(HOME+'/plot/data/conv'+IDENTIFIER+'_action_'+ TEST, np.array(action))
    np.save(HOME+'/plot/data/conv'+IDENTIFIER+'_VE_'+ TEST, np.array(VE))


def plot_single(TEST, DATE, start_cycle, end_cycle):

    #PARAMETERS
    FONTSIZE = 18
    HOME = os.environ['HOME']

    supply_curr = np.load(HOME+'/plot/data/conv'+DATE+'_supply_curr_'  +TEST +'.npy')
    supply_volt = np.load(HOME+'/plot/data/conv'+DATE+'_supply_volt_'  +TEST +'.npy')
    conf =        np.load(HOME+'/plot/data/conv'+DATE+'_conf_'+TEST +'.npy')
    action =      np.load(HOME+'/plot/data/conv'+DATE+'_action_'+TEST +'.npy')
    VE =          np.load(HOME+'/plot/data/conv'+DATE+'_VE_'+TEST +'.npy')

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

    dir = HOME+ '/plot/' + DATE + '_Vs&Is_vs_time' + '_dist_pred_' + TEST +'.png'
    plt.savefig(dir, dpi=300)
    print(dir)

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
        action =      np.load(HOME+'/plot/data/conv'+DATE+'_action_'+TEST +'.npy')
        VE =          np.load(HOME+'/plot/data/conv'+DATE+'_VE_'+TEST +'.npy')

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

    dir = HOME+ '/plot/conv_' + DATE + '_all_tests.png'
    plt.savefig(dir, dpi=300)
    print(dir)

if __name__ == "__main__":
    HOME = os.environ['HOME']
    OUTPUT_DIR = 'spec_output_1_7'
    NUM_INSTR = '40000'
    VERSION = '1'
    PDN = 'DESKTOP_INTEL_DT'
    PREDICTOR = 'HarvardPowerPredictor_1'

    # TEST = 'crc'
    # path = HOME+'/'+OUTPUT_DIR+'/gem5_out/'+TEST+'_'+NUM_INSTR+'_'+VERSION+'_'+PDN+'_'+PREDICTOR+'/stats.txt'
    # print(path)
    # stats = open(path, 'r')
    # calc_plot_stats(stats, CYCLE_START=653, CYCLE_END=-1, IDENTIFIER=IDENTIFIER)

    # PLOT_START_CYCLE = 10000
    # PLOT_END_CYCLE = 15000
    # plot_single(TEST, IDENTIFIER, PLOT_START_CYCLE, PLOT_END_CYCLE)
    
    # TEST_LIST =["basicmath", "bitcnts", "blowfish_decrypt", "blowfish_encrypt", 
    #     "qsort", "susan_smooth", "susan_edge", "susan_corner", "dijkstra", 
    #     "rijndael_decrypt", "rijndael_encrypt", "sha", "crc", "fft", "ffti", 
    #     "toast", "untoast"]
    # IDENTIFIER = "1-7"

    TEST_LIST=[
    #"400.perlbench", \ NO BINARIES
    "401.bzip2", \
    "403.gcc", \
    "410.bwaves", \
    #"416.gamess", \ NO BINARIES
    "429.mcf", \
    "433.milc", \
    "434.zeusmp", \
    "435.gromacs", \
    "436.cactusADM", \
    "437.leslie3d", \
    "444.namd", \
    "445.gobmk", \
    "447.dealII", \
    "450.soplex", \
    "453.povray", \
    "454.calculix", \
    "456.hmmer", \
    "458.sjeng", \
    "459.GemsFDTD", \
    "462.libquantum", \
    "464.h264ref", \
    "470.lbm", \
    "471.omnetpp", \
    "473.astar", \
    # "481.wrf", \
    # "482.sphinx3", \
    # "983.xalancbmk", \
    # "998.specrand", \
    # "999.specrand" \
    ]
    NUM_INSTR = ""
    IDENTIFIER = "1-7_spec"

    for TEST in TEST_LIST:
        path = HOME+'/'+OUTPUT_DIR+'/gem5_out/'+TEST+'_'+NUM_INSTR+'_'+VERSION+'_'+PDN+'_'+PREDICTOR+'/stats.txt'
        print(path)
        stats = open(path, 'r')
        calc_plot_stats(stats, CYCLE_START=1000, CYCLE_END=-1, IDENTIFIER=IDENTIFIER)
    plot_all(TEST_LIST, IDENTIFIER)



    