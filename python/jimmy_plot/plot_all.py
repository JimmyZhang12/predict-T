import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import math

from file_read_backwards import FileReadBackwards
import os, util
from functools import reduce


def plot_all(storage, DATE,PREDICTOR):
    #PARAMETERS
    FONTSIZE = 12
    HOME = os.environ['HOME']
    TEST_LIST = []
    for i in storage:
        TEST_LIST.append(i[0])

    x = np.arange(len(TEST_LIST))
    fig = plt.figure(constrained_layout=True)          
    fig.set_size_inches(25, 25)
    fig.suptitle(PREDICTOR)

    gs = fig.add_gridspec(4, 5)

    ax_hit = fig.add_subplot(gs[0, :])
    ax_hit.set_xticks(x)
    ax_hit.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)
    ax_hit.set_ylim([0,1])

    ax_fp = fig.add_subplot(gs[1, :])
    ax_fp.set_xticks(x)
    ax_fp.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)
    ax_fp.set_ylim([0,1])

    hit_avg = 0
    fp_avg = 0

    for x, TEST in enumerate(TEST_LIST):
        data = storage[x][1]
        hits = data['powerPred.overall_hit_rate']
        false_ps = data['powerPred.overall_fp_rate']
        ax_hit.bar(x,hits, color = 'RED')
        ax_fp.bar(x,false_ps, color = 'RED')

        hit_avg += hits
        fp_avg += false_ps

    hit_avg /= len(TEST_LIST)
    fp_avg /= len(TEST_LIST)
    ax_hit.set_title('Hit (Max) Average = ' + str(hit_avg), fontsize=FONTSIZE*2)
    ax_fp.set_title('False Pos (Min) Average = '+ str(fp_avg), fontsize=FONTSIZE*2)

    graph_name = DATE+'_'+PREDICTOR+'_'+'plot-all.png'
    path = HOME+'/plot/'+graph_name
    print(path)
    plt.savefig(path, dpi=300)


def gather_plot_stats(TEST,DURATION,CYCLE_PERIOD,DEVICE_TYPE,PREDICTOR,OUTPUT_DIR,DATE):
    checker = { "powerPred.overall_fp_rate":False , "powerPred.overall_hit_rate":False} 

    HOME = os.environ['HOME']
    
    test_name = TEST +'_'+DURATION+'_' +CYCLE_PERIOD+'_'+DEVICE_TYPE+'_'+PREDICTOR
    print(test_name)
    path = HOME + '/' + OUTPUT_DIR + '/gem5_out/' + test_name + '/stats.txt'

    storage = {}
    for k in checker.keys():
        storage[k] = 0

    with FileReadBackwards(path, encoding="utf-8") as frb:
        while True:
            line = frb.readline()

            if not line:
                break
            for k in checker.keys():
                if k in line: 
                    checker[k] = True
                    if (line.split()[1]) == 'nan':
                        val = 0
                    else:
                        val = float(line.split()[1])
                    storage[k] = val

            if reduce(lambda a, b: a and b, checker.values()): 
                break
        return storage

TEST_LIST_spec=[
    # "400.perlbench", NO BINARIES
    # "401.bzip2", 
    # "403.gcc", 
    # "410.bwaves", 
    # # "416.gamess", NO BINARIES
    "429.mcf", 
    "433.milc", 
    # "434.zeusmp", 
    "435.gromacs", 
    "436.cactusADM", 
    "437.leslie3d", 
    "444.namd", 
    "445.gobmk", 
    # "447.dealII", 
    # "450.soplex", 
    "453.povray", 
    "454.calculix", 
    "456.hmmer", 
    # "458.sjeng", 
    "459.GemsFDTD", 
    "462.libquantum", 
    "464.h264ref", 
    # # "470.lbm", 
    "471.omnetpp", 
    "473.astar", 
    "481.wrf", \
    "482.sphinx3", \
    # # "983.xalancbmk", \
    # # "998.specrand", \
    # # "999.specrand" \
    ]

if __name__ == "__main__":
    DURATION = '35'
    CYCLE_PERIOD = '500000'
    DEVICE_TYPE = 'DESKTOP'
    PREDICTOR = 'IdealSensorHarvardMitigation'
    OUTPUT_DIR = 'output_3_25_IdealSensorHarvardMitigation_thres=1.34,table_size=3k,lt=[0,50]'
    DATE = '3-24_' + OUTPUT_DIR

    storage = []
    for TEST in TEST_LIST_spec:
        data = gather_plot_stats(TEST,DURATION,CYCLE_PERIOD,DEVICE_TYPE,PREDICTOR,OUTPUT_DIR,DATE)
        storage.append([TEST,data])

    print(storage)
    plot_all(storage, DATE,PREDICTOR)
