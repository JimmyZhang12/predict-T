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
import predictor_sim
import test

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

    pc_data = get_data(tn, 'taken_branch.bin',np.uint64)
    power = get_data(tn, 'power.bin', np.double)
    curr = np.true_divide(power, VDC)
    print('1. getting voltage...')
    [voltage,ve_cycle] = sim_pdn.get_volt_wrapper(curr,THRES,L,C,R,VDC,CLK)
    print('   done!')
    print('2. running predictor...')
    (hr,fp) = predictor_sim.run_prediction_wrapper(pc_data, ve_cycle, voltage)
    print('   done!')
    print("hit rate: ", hr)
    print("false pos rate:", fp)


            
if __name__ == "__main__":
    run()
