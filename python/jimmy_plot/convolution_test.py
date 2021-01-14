import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util
from enum import Enum
from datetime import datetime
import math


def plot_single(TEST, DATE, start_cycle, end_cycle):
    #PARAMETERS
    FONTSIZE = 18
    HOME = os.environ['HOME']

    supply_curr = np.load(HOME+'/plot/data/harvard_'+DATE+'_supply_curr_'  +TEST +'.npy')
    #supply_volt = np.load(HOME+'/plot/data/harvard_'+DATE+'_supply_volt_'  +TEST +'.npy')
    end_cycle = min(end_cycle,len(supply_curr))
    if (start_cycle > len(supply_curr)):
        end_cycle = len(supply_curr)
        start_cycle = min(0, len(supply_curr) - (end_cycle-start_cycle))

    R = 3E-3
    L = 30E-12
    C = 1E-6

    # R = 1.5E-3
    # L = 30E-12
    # C = 1.2E-6

    # R = 0.5E-3
    # L = 2.39E-12
    # C = 1E-6

    ts = 1/4E9
    vdc = 1.4

    # R = 0.5e-3
    # L = 2.4e-12
    # C = 1e-6
    N = end_cycle
    
    vout = np.zeros(int(N))
    vout[0] = vdc
    vout[1] = vdc

    for i in range(2,int(N)):
        vout[i] = vdc*ts**2/(L*C)\
            + vout[i-1]*(2 - ts/(L/R)) \
            + vout[i-2]*(ts/(L/R) \
            - 1 - ts**2/(L*C))\
            - supply_curr[i]*R*ts**2/(L*C)
  
    supply_volt = vout

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2, 7)
    ax = fig.add_subplot(gs[0, :])

    fig.set_size_inches(20, 7.5)
    fig.suptitle('(Harvard)' +  ', DESKTOP, ' + TEST + ' )', fontsize=FONTSIZE)
    ax.set_ylabel('Supply Voltage', fontsize=FONTSIZE)
   
    ax.set_xlim(left = start_cycle, right = end_cycle)
    ax.set_ylim(bottom = 1.3, top = 1.5)

    ax2 = ax.twinx()
    ax2.set_ylabel('Current', color='tab:blue', fontsize=FONTSIZE)  # we already handled the x-label with ax1
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_ylim([min(i for i in supply_curr if i > 0.8), max(supply_curr)])
    ax.set_title('Supply Voltage Over Time', fontsize=FONTSIZE)
    #plot
    xvar = np.linspace(0,len(supply_volt),len(supply_volt))
    ax.plot(xvar, supply_volt,color='black', linewidth=1.0)

    supply_volt = np.load(HOME+'/plot/data/harvard_'+DATE+'_supply_volt_'  +TEST +'.npy')
    xvar = np.linspace(0,len(supply_volt),len(supply_volt))
    ax.plot(xvar, supply_volt,color='green', linewidth=1.0)

    xvar = np.linspace(0,len(supply_curr),len(supply_curr))
    ax2.plot(xvar, supply_curr, color='tab:blue')


    
    file_dir = HOME+ '/plot/conv_test.png'
    plt.savefig(file_dir, dpi=300)
    print(file_dir)

# clk = 4E9
# # R = 0.5e-3
# # L = 2.4e-12
# # C = 1e-6
# R, L, C = 1, 1, 1
# vdc = 1.4
# N = 1e3
# ts = (1/clk)/N
# ts = 1
# def vc(curr):
#     v_ret = [vdc] * 2

#     vout_2_diff = [0,0]
#     vout_1_diff = [0,0]
#     for i in range(2,len(curr)):
#         if(i%1000 == 0):
#             print(i," / ", len(curr))
#         vout_1_diff.append((v_ret[-2] - v_ret[-1]) / ts)
#         #vout_2_diff.append((vout_1_diff[-2] - vout_1_diff[-1]) / ts)
#         vout_2_diff.append(0)

#         vout = vdc - R*C*vout_1_diff[-1] - R*curr[i] - L*C*vout_2_diff[-1]
#         v_ret.append(vout)
#     print(vout_1_diff)
#     print(vout_2_diff)
#     print(v_ret)
#     return v_ret
        
    
if __name__ == "__main__":

    HOME = os.environ['HOME']
    OUTPUT_DIR = 'output_1_7'
    NUM_INSTR = '40000'
    VERSION = '1'
    PDN = 'DESKTOP_INTEL_DT'
    PREDICTOR = 'HarvardPowerPredictor_1'
    IDENTIFIER = "1-11"

    TEST = 'fft'
    plot_single(TEST, IDENTIFIER, 10000,15000)
    # HOME = os.environ['HOME']
    # supply_curr = np.load(HOME+'/plot/data/harvard_'+IDENTIFIER+'_supply_curr_'  +TEST +'.npy')
    
    # ts = 1/4E9
    # R = 0.5e-3
    # L = 2.4e-12
    # C = 1e-6
    # vdc = 1.4
    # iout = supply_curr
    # N = 1000
    
    # vout = np.zeros(int(N))
    # vout[0] = vdc
    # vout[1] = vdc

    # for i in range(2,int(N)):
    #     vout[i] = vdc*ts**2/(L*C)\
    #         + vout[i-1]*(2 - ts/(L/R)) \
    #         + vout[i-2]*(ts/(L/R) \
    #         - 1 - ts**2/(L*C))\
    #         - iout[i]*R*ts**2/(L*C)


    # plt.plot((np.arange(0,int(N),1))*ts,vout,lw=3,mfc='w',mew=3,ms=12)
        
    # file_dir = HOME+ '/plot/conv_test.png'
    # plt.savefig(file_dir, dpi=300)
    # print(file_dir)


    