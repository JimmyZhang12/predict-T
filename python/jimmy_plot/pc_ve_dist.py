import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import math
import struct 
import os
from functools import reduce
import time
import sim_pdn
from collections import defaultdict
import ve_dist_sim

def get_data(test_name,file_name,_dtype):
    output_dir = 'output_4_9_vedist/gem5_out'
    HOME = os.environ['HOME']

    file_path = os.path.join(HOME,output_dir)
    file_path = os.path.join(file_path,test_name)
    file_path = os.path.join(file_path,file_name)
    print(file_path)
    print('loading...')

    with open(file_path, "rb") as binaryfile :
        myArr = bytearray(binaryfile.read())          
    data = np.frombuffer(myArr, dtype=_dtype)
    return data

def run():
    VDC = 1.4
    THRES = 1.3
    L = 20e-12
    C = 1.32e-06
    R = 3.2e-3
    CLK = 4E9
    tn = '459.GemsFDTD_130_1000000_DESKTOP_HarvardPowerPredictorMitigation'

    pc_data = get_data(tn, 'taken_branch.bin',np.uint)
    power = get_data(tn, 'power.bin', np.double)
    curr = np.true_divide(power, VDC)
    print('1. getting voltage...')
    [_,ve_cycle] = sim_pdn.get_volt_wrapper(curr,THRES,L,C,R,VDC,CLK)
    print('   done!')
    print('2. calculating stats...')
    (ve_dist,perc_pc,pc_std_dev,total_pcs) = ve_dist_sim.ve_dist_wrapper(pc_data,ve_cycle)
    print('   done!')

    HOME = os.environ['HOME']
    DATE = '4-14'
    fig, (ax,bx) = plt.subplots(nrows=2, ncols=1)
    ax2 = ax.twinx()

    ax.plot(range(len(ve_dist)), ve_dist,linewidth=0.5, color='black', label="cycles to VE")
    ax2.plot(range(len(perc_pc)), perc_pc,linewidth=0.5, color='blue', alpha=0.5, label="percent of taken branches")
    bx.plot(range(len(pc_std_dev)), pc_std_dev,linewidth=0.5, color='blue', alpha=0.5, label="percent of taken branches")

    fig.suptitle('total taken branches: '+str(total_pcs))
    ax.set_xlabel('taken branch', fontsize=18) 
    ax.set_ylabel('distance to VE', fontsize=18)
    ax2.set_ylabel('percent of taken branches', fontsize=18)
    # ax.set_xlim([0,1500])
    # ax.set_ylim([0,1000])


    plot_path = HOME+'/plot/' + DATE + 'gems_long_test_ve_dist' + '.png'
    plt.savefig(plot_path, dpi=150)
    print(plot_path)
            
if __name__ == "__main__":
    run()
