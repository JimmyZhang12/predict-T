import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


class Cycle_Dump:
    event_map = {
        0:'NO_EVENT',
        1:'BRANCH_T',
        2:'BRANCH_NT',
        3:'BRANCH_MP',
        4:'FETCH',
        5:'ICACHE_FETCH',
        6:'ICACHE_BLOCK',
        7:'COMMIT_BLOCK',
        8:'IQ_FULL',
        9:'LSQ_FULL',
        10:'DCACHE_BLOCK',
        11:'DCACHE_MISS',
        12:'DUMMY_EVENT'
    }
    state_map = {
        0: 'INVALID',
        1: 'NORMAL',
        2: 'THROTTLE',
        3: 'EMERGENCY'
    }
    def __init__(self,TABLE_SIZE, SIGNATURE_LENGTH):
        self.TABLE_SIZE = TABLE_SIZE
        self.SIGNATURE_LENGTH = SIGNATURE_LENGTH
        self.ve_count = 0
        self.action_count = 0
    def reset(self):
        self.signature = []
        self.table = [[] for _ in range(TABLE_SIZE)]
        self.table_index_count = 0
        self.ve_flag = False
        self.action_flag = False
        self.table_insert_index = None
        self.table_find_index = None
        self.cycle = None
        self.supply_curr = None
        self.pred_state = None
        self.anchorPC_var = None
        return

    def inserted_New_Entry(self, line):
        linespl = line.split()
        event = self.event_map[int(linespl[1])]
        self.signature.append(event) 
        return
    def num_voltage_emergency(self, line):
        linespl = line.split()
        ve_read = int(linespl[1])
        if ve_read > self.ve_count:
            self.ve_count = ve_read
            self.ve_flag = True
        return
    def total_action(self, line):
        linespl = line.split()
        action_read = int(linespl[1])
        if action_read > self.action_count:
            self.action_count = action_read
            self.action_flag = True
        return
    def counter(self, line):
        linespl = line.split()
        self.cycle = int(linespl[1])
        return
    def state(self, line):
        linespl = line.split()
        self.pred_state = int(linespl[1])
        return
    def supply_current(self, line):
        linespl = line.split()
        self.supply_curr = float(linespl[1])
        return
    def table_dump(self, line):
        linespl = line.split()
        event = self.event_map[int(linespl[1])]
        self.table[self.table_index_count//self.SIGNATURE_LENGTH].append(event)
        self.table_index_count+=1
        return
    def last_insert_index(self, line):
        linespl = line.split()
        self.table_insert_index = int(linespl[1])
        return
    def last_find_index(self, line):
        linespl = line.split()
        self.table_find_index = int(linespl[1])
        return
    def anchorPC(self, line):
        linespl = line.split()
        self.anchorPC_var = hex(int(linespl[1]))
        return

    def dump(self):
        print('******* CYCLE: ',self.cycle,'*********')
        print('HARVARD STATE: ', self.state_map[self.pred_state])
        print('SUPPLY CURRENT: ', self.supply_curr)
        print('ANCHOR PC: ', self.anchorPC_var)
        #print('ANCHOR PC: ', self.anchorPC)
        if self.ve_flag: print('Voltage Emergency High')
        if self.action_flag: print('Prediction High')
        print('ENTRY INSERTED AT INDEX: ', self.table_insert_index)
        print('ENTRY HIT AT INDEX: ', self.table_find_index)
        print("HISTORY REGISTER : ", self.signature)
        for i in range(TABLE_SIZE):
            print(i,':  ', self.table[i])
        

#PARAMETERS
SIGNATURE_LENGTH = 12
TABLE_SIZE = 32
CYCLE_START = 20000
HOME = os.environ['HOME']
PREDICTOR = 'HarvardPowerPredictor_1'
CLASS = 'DESKTOP'
TEST = 'qsort'

path = HOME + '/output_10_14/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'
stats = open(path, 'r')
print(path)
#PARAMETERS

cycle_dump = Cycle_Dump(TABLE_SIZE, SIGNATURE_LENGTH)

line = stats.readline()
line = stats.readline()
while line:
    cycle_dump.reset()
    while(True):       
        if 'Begin Simulation Statistics' in line or not line:
            break
        elif 'system.cpu.powerPred' in line:
            stat_name = line.split()[0].split('.')[3].split(':')[0]
            func = getattr(cycle_dump, stat_name, False)
            if func is not False:
                func(line)
        line = stats.readline()      

    if cycle_dump.cycle % 1000 < 3:
        print (cycle_dump.cycle)
    if cycle_dump.cycle > CYCLE_START:
        cycle_dump.dump()
        input() 
    # if cycle_dump.ve_flag or cycle_dump.action_flag:
    #     cycle_dump.dump()
    #     input() 
    line = stats.readline()

        