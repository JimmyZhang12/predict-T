import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from datetime import datetime
import math
import random
from cython.sim_pdn import get_volt_wrapper


def run(test_name,DATE):
  
    VDC = 1.4
    THRES = 1.33
    L = 20e-12
    C = 1.32e-06
    R = 3.2e-3
    CLK = 4E9

    for tn in test_name:
        HOME = os.environ['HOME']
        output_dir = 'output_4_22/gem5_out'

        file_path = os.path.join(HOME,output_dir)
        file_path = os.path.join(file_path,tn)
        file_path = os.path.join(file_path,'power.bin')
        print(file_path)
        with open(file_path, "rb") as binaryfile :
            myArr = bytearray(binaryfile.read())          
        power = np.frombuffer(myArr)

        curr = np.true_divide(power, VDC)

        [voltage,ve_cycle] = get_volt_wrapper(curr,THRES,L,C,R,VDC,CLK)
        print('TOTAL VEs', len(ve_cycle))
       

if __name__ == "__main__":
    # test_name = ['qsort_10_100000_DESKTOP_HarvardPowerPredictor_nothrottle',
    #     'qsort_10_100000_DESKTOP_HarvardPowerPredictor_throttle']
    # test_name = ['454.calculix_50_1000000_DESKTOP_HarvardPowerPredictorMitigation']
    test_name = ['qsort_10_100000_DESKTOP_LongLatencyPredictor']
    run(test_name,'4-22')