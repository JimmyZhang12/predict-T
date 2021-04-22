import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from datetime import datetime
import math
import random
import sim_pdn


def run(test_name,DATE):
    HOME = os.environ['HOME']
    plt.tight_layout()
    fig = plt.figure(figsize=(120,5))
    ax = plt.axes()
    fig.suptitle('Supply Voltage Over Time', fontsize=14)
    ax.set_xlabel('Cycle', fontsize=18) 
    ax.set_ylabel('Supply Voltage', fontsize=18)
    ax2 = ax.twinx()
    ax2.set_ylabel('Current', color='tab:blue', fontsize=18)  # we already handled the x-label with ax1
    xplot_min = int(0.5e6)
    xplot_max = int(0.501e6)

    VDC = 1.4
    THRES = 1.3
    L = 20e-12
    C = 1.32e-06
    R = 3.2e-3
    CLK = 4E9

    for tn in test_name:

        output_dir = 'output_4_22/gem5_out'

        file_path = os.path.join(HOME,output_dir)
        file_path = os.path.join(file_path,tn)
        file_path = os.path.join(file_path,'power.bin')
        print(file_path)
        with open(file_path, "rb") as binaryfile :
            myArr = bytearray(binaryfile.read())          
        power = np.frombuffer(myArr)

        curr = np.true_divide(power, VDC)
        print(curr[500000:500500])

        [voltage,ve_cycle] = sim_pdn.get_volt_wrapper(curr,THRES,L,C,R,VDC,CLK)
        print('TOTAL VEs', len(ve_cycle))
        ve_cycle = [(i-xplot_min) for i in ve_cycle if (i<xplot_max and i>xplot_min) ]
        for ve in ve_cycle:
            ax.axvspan(ve,ve+1,alpha=0.8)

        voltage = voltage[xplot_min:xplot_max]
        curr = curr[xplot_min:xplot_max]

        ax.plot(range(0,len(voltage),1), voltage,linewidth=0.5, color='black')
        ax2.plot(range(0,len(curr),1), curr,linewidth=0.5)
        print(int(len(curr)/30))
        ax.set_xticks(
            range(0,len(curr),
                int(len(curr)/30)
            )
        )
        # ax.set_xlabel(
        #     range(xplot_min,xplot_max,
        #         int(len(curr)/30)
        #     ))
    

    plot_path = HOME+'/plot/' + DATE + '_throttle_test' + '.png'
    plt.savefig(plot_path, dpi=100,bbox_inches='tight')
    print(plot_path)

if __name__ == "__main__":
    # test_name = ['qsort_10_100000_DESKTOP_HarvardPowerPredictor_nothrottle',
    #     'qsort_10_100000_DESKTOP_HarvardPowerPredictor_throttle']
    # test_name = ['454.calculix_50_1000000_DESKTOP_HarvardPowerPredictorMitigation']
    test_name = ['qsort_10_100000_DESKTOP_LongLatencyPredictor']
    run(test_name,'4-22')