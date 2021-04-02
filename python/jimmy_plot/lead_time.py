import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from datetime import datetime
import math
import random
from file_read_backwards import FileReadBackwards



def plot_single(data, DATE, NAME):
    #PARAMETERS
    FONTSIZE = 24
    HOME = os.environ['HOME']
 
    fig = plt.figure(figsize=(20,5))
    ax = plt.axes()
    fig.suptitle('lead time distribution', fontsize=FONTSIZE)

    for fn, data_ in data.items():
        x = list(data_.keys())
        y = list(data_.values())
        print(fn, sum(y))
        y_norm = [i/sum(y) for i in y]
        ax.plot(x, y_norm, linewidth=1.0, label=fn)

    ax.legend()
    ax.set_xlabel('Cycle (million)', fontsize=14)
    ax.set_ylim([0,1]) 
    ax.set_ylabel('num hits', fontsize=14)

    file_dir = HOME+ '/plot/' + DATE + NAME +'.png'
    plt.savefig(file_dir, dpi=300)
    print(file_dir)

def plot_separate(data, DATE, NAME):
    num_files = len(data.keys())
    fig = plt.figure(constrained_layout=True)          
    fig.set_size_inches(num_files*2, num_files*2)
    gs = fig.add_gridspec(num_files, 3)

    cnt = 0
    for file_name,_data in data.items():
        ax = fig.add_subplot(gs[cnt, :])

        x = list(_data.keys())
        y = list(_data.values())
        ax.plot(x, y, linewidth=1.0, label=file_name)
        ax.legend()
        ax.set_xlabel('lead time', fontsize=14) 
        ax.set_ylabel('amount', fontsize=14)
        cnt+=1

    HOME = os.environ['HOME']
    file_dir = HOME+ '/plot/' + DATE + NAME +'.png'
    plt.savefig(file_dir, dpi=300)
    print(file_dir)

def gather_data(files):
    storage = dict()
    for file in files:
        file_path = file[1]
        file_name = file[0]
        hit_storage = dict()
        with FileReadBackwards(file_path, encoding="utf-8") as frb:
            while True:
                line = frb.readline()
                if 'system.cpu.powerPred.hit_rate' in line and 'total' not in line:
                    stat_name = line.split()[0]
                    lead_time = int(stat_name.split('::')[-1])
                    hit_storage[lead_time] = int(float(line.split()[1]))
                    if lead_time == 0:
                        break
        storage[file_name] = hit_storage
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

def generate_path_spec(output_dir,config_name):
    HOME = os.environ['HOME']
    path = os.path.join(HOME, output_dir + '/gem5_out')
    list_subfolders_with_paths = []
    for i in TEST_LIST_spec:
        folder_name = os.path.join((i+config_name),'stats.txt')
        list_subfolders_with_paths.append([i,os.path.join(path,folder_name)])

    for i in list_subfolders_with_paths:
        print(i)

    return list_subfolders_with_paths

def generate_path_qsort():
    HOME = os.environ['HOME']
    file_path = os.path.join(HOME,'output_3_18/gem5_out')
    file_path = os.path.join(file_path,'qsort_10_100000_DESKTOP_HarvardPowerPredictorMitigation_drop5/stats.txt')
    # file_path = os.path.join(HOME,'output_3_19/gem5_out')
    # file_path = os.path.join(file_path,'qsort_10_100000_DESKTOP_HarvardPowerPredictorMitigation/stats.txt')
    file_name = 'qsort_10_100000_DESKTOP_HarvardPowerPredictor'

    return [[file_name,file_path]]


if __name__ == "__main__":
    output_dir = 'output_3_25_ideal_sensorthres=1.34_ve=1.33'
    config_name = '_35_500000_DESKTOP_IdealSensor'
    files = generate_path_spec(output_dir,config_name)
    data = gather_data(files)
    # for i in data.keys():
    #     print(i)
    #     print(data[i])
    plot_single(data = data, DATE="3-25-21", NAME= output_dir)