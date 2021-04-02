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

def plot(data, DATE):
    HOME = os.environ['HOME']

    fig = plt.figure(figsize=(60,5))
    ax = plt.axes()
    fig.suptitle('Supply Voltage Over Time', fontsize=14)
    ax.set_xlabel('Cycle', fontsize=18) 
    ax.set_ylabel('Supply Voltage', fontsize=18)
    ax2 = ax.twinx()
    ax2.set_ylabel('Current', color='tab:blue', fontsize=18)  # we already handled the x-label with ax1

    file_name, file_data = data
    current = file_data['system.cpu.powerPred.supply_current']
    voltage = file_data['system.cpu.powerPred.supply_voltage']

    xvar = np.linspace(0,len(voltage),len(voltage))

    ax.plot(xvar, voltage,color='black', linewidth=1.0)
    ax.set_ylim(bottom= 1.31, top =1.4)

    ax2.plot(xvar, current, color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_ylim(bottom=0, top=5+max(current))
    
    plot_path = HOME+'/plot/' + DATE + '_voltage+current_' + file_name + '.png'
    plt.savefig(plot_path, dpi=300)
    print(plot_path)

def gather_data(files):
    file_path = files[1]
    file_name = files[0]

    stats = open(file_path, 'r')
    line = stats.readline()   

    f_storage = dict()
    f_storage['system.cpu.powerPred.supply_current'] = list()
    f_storage['system.cpu.powerPred.supply_voltage'] = list()

    while (line): 
        line = stats.readline()   
        if 'system.cpu.powerPred.supply_current' in line:
            val = float(line.split()[1])
            f_storage['system.cpu.powerPred.supply_current'].append(val) 
        elif 'system.cpu.powerPred.supply_voltage' in line and 'prev' not in line:
            val = float(line.split()[1])
            f_storage['system.cpu.powerPred.supply_voltage'].append(val) 
            
    return [file_name, f_storage]

def gen_files_paths():

    file_name = 'qsort_3000_1_DESKTOP_HarvardPowerPredictor'

    HOME = os.environ['HOME']
    file_path = os.path.join(HOME, 'output_3_8/gem5_out')
    
    folder_name = file_name + '/stats.txt'

    file_path = os.path.join(file_path,folder_name)
    print(file_path)

    return [file_name,file_path]


if __name__ == "__main__":
    files = gen_files_paths()
    data = gather_data(files)
    plot(data = data, DATE='3-11-2021')