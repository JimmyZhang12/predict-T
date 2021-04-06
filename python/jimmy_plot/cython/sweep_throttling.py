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

TEST_LIST_spec=[
    # "400.perlbench", NO BINARIES
    # "401.bzip2", 
    # "403.gcc", 
    # "410.bwaves", 
    # # "416.gamess", NO BINARIES
    "429.mcf", 
    # "433.milc", 
    # # "434.zeusmp", 
    # "435.gromacs", 
    # "436.cactusADM", 
    # "437.leslie3d", 
    # "444.namd", 
    # "445.gobmk", 
    # "447.dealII", 
    # "450.soplex", 
    # "453.povray", 
    # "454.calculix", 
    # "456.hmmer", 
    # # "458.sjeng", 
    # "459.GemsFDTD", 
    # "462.libquantum", 
    # "464.h264ref", 
    # # # "470.lbm", 
    # "471.omnetpp", 
    # "473.astar", 
    # "481.wrf", \
    # "482.sphinx3", \
    # # "983.xalancbmk", \
    # # "998.specrand", \
    # # "999.specrand" \
    ]

class PDN:
    def __init__(self, L, C, R, VDC, CLK):
        self.L = L
        self.C = C
        self.R = R
        self.VDC = VDC
        self.CLK = CLK
        self.vout_2_cycle_ago = VDC
        self.vout_1_cycle_ago = VDC
        self.iout_1_cycle_ago = 0
        self.LmulC = self.L*self.C
        self.LdivR = self.L/self.R
    def reset(self):
        self.vout_2_cycle_ago = self.VDC
        self.vout_1_cycle_ago = self.VDC
        self.iout_1_cycle_ago = 0
    def get_volt(self, current):
        ts = 1/self.CLK
        
        vout = self.VDC*ts**2/(self.LmulC) \
            + self.vout_1_cycle_ago*(2 - ts/(self.LdivR)) \
            + self.vout_2_cycle_ago*(ts/(self.LdivR) \
            - 1 - ts**2/(self.LmulC)) \
            - current*self.R*ts**2/(self.LmulC) \
            - (1/self.C)*ts*(current - self.iout_1_cycle_ago)
            
        self.vout_2_cycle_ago = self.vout_1_cycle_ago
        self.vout_1_cycle_ago = vout
        self.iout_1_cycle_ago = current
        return vout


def run(test_name):
    #load data files
    HOME = os.environ['HOME']
    output_dir = 'output_4_1/gem5_out'

    file_path = os.path.join(HOME,output_dir)
    file_path = os.path.join(file_path,test_name)
    file_path = os.path.join(file_path,'power.bin')

    save_path = os.path.join(HOME,'plot/data')
    save_path = os.path.join(save_path,test_name+'_lead_time_sweep')
    print(file_path)
    print(save_path)
    with open(file_path, "rb") as binaryfile :
        myArr = bytearray(binaryfile.read())          
    power = np.frombuffer(myArr)
    #init pdn parameters
    VDC = 1.4
    THRES = 1.33
    L = 20e-12
    C = 1.32e-06
    R = 3.2e-3
    VDC = VDC
    CLK = 4E9

    stc_curr = 10.249102297480446
    total_curr = np.true_divide(power,VDC)
    dyn_curr = np.subtract(total_curr,stc_curr)
    #done init

    ve_cycle = sim_pdn.detect_VE_wrapper(
        total_curr,
        THRES,
        _L = L,
        _C = C,
        _R = R,
        _VDC = VDC,
        _CLK = CLK)
    num_VEs = len(ve_cycle)
    print(num_VEs)

    ve_ret = [[0,0,num_VEs]]
    for THROTTLE_TIME in range(10,150,5):
        for THROTTLE_LEADTIME in range(0,THROTTLE_TIME,5):
            #CYTHON  
            start_throttle = np.asarray([(i-THROTTLE_LEADTIME) for i in ve_cycle], dtype=np.int32)
            end_throttle = np.asarray([(i+THROTTLE_TIME) for i in ve_cycle], dtype=np.int32)

            ves = sim_pdn.detect_VE_throttle_wrapper(dyn_curr, stc_curr,
                THROTTLE_TIME, THROTTLE_LEADTIME,
                THRES, L, C, R, VDC, CLK, 
                start_throttle, end_throttle)

            print('LEADTIME=',THROTTLE_LEADTIME, 'THROTTLE_TIME=',THROTTLE_TIME, ves)
            ve_ret.append([THROTTLE_TIME,THROTTLE_LEADTIME,ves])
    np.save(save_path,np.array(ve_ret))


if __name__ == "__main__":
    for tn in TEST_LIST_spec:
        run(tn+'_35_500000_DESKTOP_IdealSensor')

    # run('qsort_10_100000_DESKTOP_HarvardPowerPredictor')