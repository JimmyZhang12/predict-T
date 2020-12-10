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
        10:'LOAD_EX',
        11:'LOAD_BLOCK',
        12:'LOAD_CFETCH',
        13:'LOAD_DISPATCH',
        14:'DUMMY_EVENT2'
    }

    state_map = {
        0: 'INVALID',
        1: 'NORMAL',
        2: 'THROTTLE',
        3: 'EMERGENCY'
    }
    def __init__(self,TABLE_HEIGHT, SIGNATURE_LENGTH):
        self.TABLE_HEIGHT = TABLE_HEIGHT
        self.SIGNATURE_LENGTH = SIGNATURE_LENGTH
        self.ve_count = 0
        self.action_count = 0
        self.h_table =  [([self.event_map[1]] * SIGNATURE_LENGTH) for _ in range(TABLE_SIZE)]
    def reset(self):
        self.signature = []
        self.signature_prev = []
        self.table = [[] for _ in range(self.TABLE_HEIGHT)]
        self.table_index_count = 0
        self.ve_flag = False
        self.ve_flag_prev = []
        self.action_flag = False
        self.table_insert_index = None
        self.table_insert_index_prev = None
        self.table_find_index = None
        self.cycle = None
        self.supply_curr = None
        self.supply_volt = None
        self.pred_state = None
        self.anchorPC_var = None
        self.numCycles_var = None
        
        return
    def inserted_New_Entry(self, line):
        linespl = line.split()
        event = self.event_map[int(linespl[1])]
        self.signature.append(event) 
        return
    def inserted_New_Entry_prev(self, line):
        linespl = line.split()
        event = self.event_map[int(linespl[1])]
        self.signature_prev.append(event) 
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
    def supply_voltage(self, line):
        linespl = line.split()
        self.supply_volt = float(linespl[1])
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
    def last_insert_index_prev(self, line):
        linespl = line.split()
        self.table_insert_index_prev = int(linespl[1])
        return
    def last_find_index(self, line):
        linespl = line.split()
        self.table_find_index = int(linespl[1])
        return
    def anchorPC(self, line):
        linespl = line.split()
        self.anchorPC_var = hex(int(linespl[1]))
        return
    def numCycles(self,line):
        linespl = line.split()
        self.numCycles_var = int(linespl[1])
        return
    def update(self):
        if self.table_insert_index < self.TABLE_HEIGHT and self.table_insert_index > -1:
            self.h_table[self.table_insert_index] = self.signature
        if self.numCycles_var == 2:
            if self.table_insert_index_prev < self.TABLE_HEIGHT and self.table_insert_index_prev > -1:
                self.h_table[self.table_insert_index_prev] = self.signature_prev
        return

    def dump(self):
        print('******* CYCLE: ',self.cycle,'*********')
        print('HARVARD STATE: ', self.state_map[self.pred_state])
        print('SUPPLY CURRENT: ', self.supply_curr)
        print('SUPPLY VOLTAGE: ', self.supply_volt)
        print('ANCHOR PC: ', self.anchorPC_var)
        if self.ve_flag: print('Voltage Emergency High', self.ve_count)
        if self.action_flag: print('Prediction High')
        print('ENTRY INSERTED AT INDEX_prev: ', self.table_insert_index_prev)
        print('ENTRY INSERTED AT INDEX     : ', self.table_insert_index)
        print('ENTRY HIT AT INDEX: ', self.table_find_index)
        print("HISTORY REGISTER     : ", self.signature)
        print("HISTORY REGISTERprev : ", self.signature_prev)

        # for i in range(self.TABLE_HEIGHT):
        #     print(i,':  ', self.table[i])
        print('____________')
        for i in range(self.TABLE_HEIGHT):
            print(i,':  ', self.h_table[i])
               

#PARAMETERS
HOME = os.environ['HOME']
PREDICTOR = 'HarvardPowerPredictor_1'
CLASS = 'DESKTOP'
TEST = 'crc'

path = HOME + '/output_10_29/gem5_out/' + CLASS + '_' + PREDICTOR + '/' + TEST + '.txt'
stats = open(path, 'r')
print(path)
#PARAMETERS

CYCLE_START = 0

line = stats.readline()
line = stats.readline()
while 'Begin Simulation Statistics' not in line:
    if 'table_dump' in line:
        TABLE_SIZE = line.split()[0].split('.')[-1].split(':')[2]
    elif 'inserted_New_Entry' in line:
        SIGNATURE_LENGTH = line.split()[0].split('.')[-1].split(':')[2]
    line = stats.readline()
line = stats.readline()
#TABLE_SIZE = int(TABLE_SIZE)+1
SIGNATURE_LENGTH = int(SIGNATURE_LENGTH)+1
TABLE_SIZE = 16*SIGNATURE_LENGTH
cycle_dump = Cycle_Dump(TABLE_SIZE//SIGNATURE_LENGTH, SIGNATURE_LENGTH)

while line:
    cycle_dump.reset()
    while(True):   
        #one cycle worth of stat dumps    
        if 'Begin Simulation Statistics' in line or not line:
            break
        stat_name = line.split()[0].split('.')[-1].split(':')[0]
        func = getattr(cycle_dump, stat_name, False)
        if func:
            func(line)

        line = stats.readline()    
    cycle_dump.update()

    # if cycle_dump.table_insert_index!=-1 or cycle_dump.table_insert_index_prev!=-1:
    #     cycle_dump.dump()
    #     input() 
    if cycle_dump.cycle % 1000 < 3:
        print (cycle_dump.cycle)
    if cycle_dump.cycle > CYCLE_START:
        cycle_dump.dump()
        input() 
    # if cycle_dump.ve_flag:
    #     cycle_dump.dump()
    #     input() 
    line = stats.readline()
print(cycle_dump.ve_count)
print(cycle_dump.action_count)

        