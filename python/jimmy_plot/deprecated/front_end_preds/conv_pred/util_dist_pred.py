import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from collections import deque


# class Event(Enum):
#     NO_EVENT = 0
#     BRANCH_T = 1
#     BRANCH_NT = 2
#     BRANCH_MP = 3
#     FETCH = 4
#     ICACHE_FETCH = 5 
#     ICACHE_BLOCK = 6
#     COMMIT_BLOCK = 7
#     IQ_FULL = 8
#     LSQ_FULL = 9
#     LOAD_EX = 10
#     LOAD_BLOCK = 11
#     LOAD_CFETCH = 12
#     DUMMY_EVENT = 13
#     DUMMY_EVENT2 = 14

event_map = {
    0:'NO_EVENT',
    1:'BRANCH_T',
    2:'BRANCH_NT',
    3:'BRANCH_MP',
    4:'FETCH',
    5:'TLB_STALL',
    6:'ICACHE_STALL',
    7:'COMMIT_BLOCK',
    8:'IQ_FULL',
    9:'LSQ_FULL',
    10:'LOAD_EX',
    11:'LOAD_WB',
    12:'LOAD_CFETCH',
    13:'STORE_EXECUTE',
    14:'STORE_WB',
    15:'INSTR_DISPATCH',
    16:'INSTR_ISSUE',
    17:'INSTR_EXECUTE',
    18:'INSTR_COMMIT',
    19:'MEM_MP',
    20:'EMPTY_EVENT',
    21:'DUMMY_EVENT2'
    }


class Cycle_Dump:
    def __init__(self, stats):
        self.ve_count = 0
        self.action_count = 0
        self.stats = stats
        self.stats.readline()
        keys = range(len(event_map.keys()))
        self.event_count = {k: 0 for k in keys}
        self.EOF = False
    def reset(self):
        self.new_events_var = [] #list of new events the current cycle
        self.new_events_prev_var = [] #list of new events the previous cycle of the cycle dump
        self.table_index_count = 0
        self.cycle = None
        self.supply_curr = None
        self.supply_volt = None
        self.supply_volt_prev = None
        self.anchorPC_var = None
        self.numCycles_var = None
        
        return
    def new_events(self,line):
        linespl = line.split()
        event = int(linespl[1])
        if event != 20: #TODO make this a enum
            self.event_count[event] += 1
            self.new_events_var.append(event)

        return
    def new_events_prev(self,line):
        linespl = line.split()
        event = int(linespl[1])
        if event != 20:
            self.event_count[event] += 1
            self.new_events_prev_var.append(event) 
        return
    def counter(self, line):
        linespl = line.split()
        self.cycle = int(linespl[1])
        return

    def supply_current(self, line):
        linespl = line.split()
        self.supply_curr = float(linespl[1])
        return
    def supply_voltage(self, line):
        linespl = line.split()
        self.supply_volt = float(linespl[1])
        return
    def supply_voltage_prev(self, line):
        linespl = line.split()
        self.supply_volt_prev = float(linespl[1])
        return
    def anchorPC(self, line):
        linespl = line.split()
        self.anchorPC_var = hex(int(linespl[1]))
        return
    def numCycles(self,line):
        linespl = line.split()
        self.numCycles_var = int(linespl[1])
        return

    def parseCycle(self):
        while(True):
            line = self.stats.readline()       
            if not line:
                return True
            #one cycle worth of stat dumps    
            if 'Begin Simulation Statistics' in line:
                self.stats.readline()
                return False
            stat_name = line.split()[0].split('.')[-1].split(':')[0]
            func = getattr(self, stat_name, False)
            if func:
                func(line)

    def dump(self):
        print('******* CYCLE: ',self.cycle,'*********')
        print('SUPPLY CURRENT: ', self.supply_curr)
        print('SUPPLY VOLTAGE     : ', self.supply_volt)
        #print('SUPPLY VOLTAGE_prev: ', self.supply_volt_prev)
        print('ANCHOR PC: ', self.anchorPC_var)
        print("New Events : ", " ".join([event_map[i] for i in self.new_events_var]) )
        print("New Events prev: ", " ".join([event_map[i] for i in self.new_events_prev_var]))



class Dist_Pred:

    class State(Enum):
        NORMAL = 0
        EMERGENCY = 1 

    def __init__(self, HISTORY_WIDTH, HYSTERESIS, EMERGENCY_V, TABLE_HEIGHT, C_THRES, LEAD_TIME):
        self.LEAD_TIME = LEAD_TIME
        self.C_THRES = C_THRES
        self.TABLE_HEIGHT = TABLE_HEIGHT
        self.HISTORY_WIDTH = HISTORY_WIDTH
        self.HISTORY_HEIGHT = len(event_map.keys())
        self.HYSTERESIS = HYSTERESIS
        self.EMERGENCY_V = EMERGENCY_V

        self.STATE = self.State.NORMAL
        self.history = [deque([0]*HISTORY_WIDTH) for _ in range(self.HISTORY_HEIGHT)]
        self.table = [np.zeros((self.HISTORY_HEIGHT, self.HISTORY_WIDTH))]*TABLE_HEIGHT
        self.convs_over_table = []

        #conv max for this cycle and prev cycle
        self.conv_max = deque([0]*600)
        self.conv_max_norm = deque([0]*600)

        self.conf_min = 0
        self.LRU = [0]*TABLE_HEIGHT

        self.VEflag_curr = False
        self.VEflag_prev = False
        self.Actionflag_prev = False
        self.Actionflag_curr = False

        self.cycles_since_pred = 0
        self.prev_max_conf = 0
        self.volt_2_cycles_ago = 0
        self.volt_1_cycles_ago = 0
        self.curr_2_cycles_ago = 0
        self.curr_1_cycles_ago = 0
        #debug
        #self.table[0] = np.ones((self.HISTORY_HEIGHT, self.HISTORY_WIDTH))
    


    def tick(self, cycle_dump):
        self.volt_1_cycles_ago = (self.volt_2_cycles_ago + cycle_dump.supply_volt)/2
        self.curr_1_cycles_ago = (self.curr_2_cycles_ago + cycle_dump.supply_curr)/2

        #advance two cycles 
        #FIRST cycle
        self.Actionflag_prev = False
        self.insert_index = -1
        for i in range(self.TABLE_HEIGHT): self.LRU[i] += 1
        self.cycles_since_pred += 1
        self.addCycle(cycle_dump.new_events_prev_var)
        #search the table
        self.convs_over_table = self.convolution()
        self.push_convmax(max(self.convs_over_table))
        #predict
        if self.predict():
            self.Actionflag_prev = True
            self.LRU[self.convs_over_table.index(max(self.convs_over_table))] = 0
            self.cycles_since_pred = 0

        self.VEflag_prev = False
        #try to insert to table
        if (self.volt_2_cycles_ago > self.EMERGENCY_V and self.volt_1_cycles_ago < self.EMERGENCY_V):
            self.VEflag_prev = True
            if self.cycles_since_pred > self.LEAD_TIME:
                self.insert_index = self.insert()



        #second cycle
        self.Actionflag_curr = False
        self.insert_index = -1
        for i in range(self.TABLE_HEIGHT):self.LRU[i] += 1
        self.cycles_since_pred += 1
        self.addCycle(cycle_dump.new_events_var)

        #search the table
        self.convs_over_table = self.convolution()
        self.push_convmax(max(self.convs_over_table))
        #predict
        if self.predict():
            self.Actionflag_curr = True
            self.cycles_since_pred = 0
            self.LRU[self.convs_over_table.index(max(self.convs_over_table))] = 0

        #try to insert to table
        self.VEflag_curr = False
        if (self.volt_1_cycles_ago > self.EMERGENCY_V and cycle_dump.supply_volt < self.EMERGENCY_V):
            self.VEflag_curr = True
            if self.cycles_since_pred > self.LEAD_TIME:
                self.insert_index = self.insert()

        self.volt_2_cycles_ago = cycle_dump.supply_volt
        self.curr_2_cycles_ago = cycle_dump.supply_curr


    def predict(self):
        prediction = (self.conv_max_norm[-2] < self.C_THRES and self.conv_max_norm[-1] > self.C_THRES) \
                and (self.cycles_since_pred > 20)
        return prediction

    def push_convmax(self, conv_max):
        self.conv_max.popleft()
        self.conv_max.append(conv_max)

        self.conv_max_norm.popleft()
        
        norm_conv_max = (conv_max - min(self.conv_max)) / (max(self.conv_max) - min(self.conv_max))
        # norm_conv_max = conv_max
        self.conv_max_norm.append(norm_conv_max)

    def addCycle(self, new_events):
        for row in self.history:
            row.popleft()
            row.append(0)

        for event in event_map.keys():
            if event in new_events:
                self.history[event][-1] += 1

    def convolution(self):
        conf_over_table = []
        history_np = np.fliplr(np.array(self.history))
        for entry in self.table:
            conv_temp = 0
            for i in range(self.HISTORY_HEIGHT):
                if sum(history_np[i]) > 0:
                    conv_temp += sum(np.convolve(entry[i], history_np[i]) )

            conf_over_table.append(conv_temp)
        return conf_over_table
        
    def insert(self):
        index = self.LRU.index(max(self.LRU))
        self.table[index] = np.array(self.history)
        self.LRU[index] = 0
        return index  
           
    def print(self):
        for j in range(self.TABLE_HEIGHT):
            for i,e in enumerate(self.history):
                print(list(self.table[j][i])," : ", event_map[i])
            print()
        if self.VEflag_curr or self.VEflag_prev:
            print('Entering EMERGENCY state')
        else:
            print(self.STATE)
        if self.insert_index != -1:
            print("Insert Entry Index: ", self.insert_index)
        for i,e in enumerate(self.history):
            print(list(e)," : ", event_map[i])
        # print('LRU: ', self.LRU)
        print('CONV result: ', self.convs_over_table)


def accuracy(action,VE,LEAD_TIME_CAP):
    bins = dict()
    act_bins = dict()
 
    for i,ve in enumerate(VE):
        if ve:
            for j in range(0,LEAD_TIME_CAP):
                if i-j < 0: break
                if action[i-j]:
                    if j in bins.keys(): bins[j] += 1
                    else: bins[j] = 1
                    break
            for j in range(0,LEAD_TIME_CAP):
                if i-j < 0 or (VE[i-j] and j>0): break
                if action[i-j]:
                    if j in act_bins.keys(): act_bins[j] += 1
                    else: act_bins[j] = 1

    # print(bins)
    # print(act_bins)

    xvar = [0]
    hits = [0]
    false_neg = [100]
    running_sum = 0
    VE_count = sum(VE)
    for key in sorted(bins.keys()):
        running_sum += bins[key]
        false_neg.append(100*(VE_count - running_sum) / VE_count)
        xvar.append(key)
        hits.append(100 * running_sum / VE_count)

    # print(hits)
    # print(xvar)
    false_pos_x = [0]
    false_pos = [100]

    action_count = sum(action)
    running_sum = 0
    for k, v in sorted(act_bins.items()):
        running_sum += v 
        false_pos.append(100*(action_count - running_sum) / action_count)
        false_pos_x.append(k)   

    if (xvar[-1] < false_pos_x[-1]):
        xvar.append(false_pos_x[-1])
        hits.append(hits[-1])
        false_neg.append(false_neg[-1])
    if (xvar[-1] > false_pos_x[-1]):
        false_pos_x.append(xvar[-1])
        false_pos.append(false_pos[-1])

    return [xvar,hits,false_neg,false_pos_x,false_pos]   
