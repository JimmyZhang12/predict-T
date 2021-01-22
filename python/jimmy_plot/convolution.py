import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from collections import deque

valid_events = {
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
    18:'INSTR_COMMIT',
    19:'MEM_MP',
    22:'DCACHE_MISS',
    23:'ICACHE_MISS',
    24:'L2_MISS',
    25:'TLB_MISS'
}

event_to_row = dict()
for i,k in enumerate(valid_events.keys()):
    event_to_row[k] = i
row_to_event = dict()
for i,k in enumerate(valid_events.keys()):
    row_to_event[i] = k

class Conv_Pred:

    class State(Enum):
        NORMAL = 0
        EMERGENCY = 1 

    def __init__(self, HISTORY_WIDTH, HYSTERESIS, EMERGENCY_V, TABLE_HEIGHT, C_THRES, LEAD_TIME):
        self.LEAD_TIME = LEAD_TIME
        self.C_THRES = C_THRES
        self.TABLE_HEIGHT = TABLE_HEIGHT
        self.HISTORY_WIDTH = HISTORY_WIDTH
        self.HISTORY_HEIGHT = len(valid_events.keys())
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

        self.VEflag = False
        self.Actionflag = False

        self.cycles_since_pred = 0
        self.prev_max_conf = 0
        self.volt_1_cycles_ago = 0
        self.events = None

        #debug
        self.cd = None
        #self.table[0] = np.ones((self.HISTORY_HEIGHT, self.HISTORY_WIDTH))

    def tick(self, cycle_dump):
        self.cd = cycle_dump

        self.events = []
        for e in cycle_dump.new_events_var:
            if e in valid_events.keys():
                self.events.append(event_to_row[e])

        self.Actionflag = False
        self.insert_index = -1
        for i in range(self.TABLE_HEIGHT):self.LRU[i] += 1
        self.cycles_since_pred += 1
        self.addCycle(self.events)

        #search the table
        self.convs_over_table = self.convolution()
        self.push_convmax(max(self.convs_over_table))
        #predict
        if self.predict():
            self.Actionflag = True
            self.cycles_since_pred = 0
            self.LRU[self.convs_over_table.index(max(self.convs_over_table))] = 0

        #try to insert to table
        self.VEflag = False
        if (self.volt_1_cycles_ago > self.EMERGENCY_V and cycle_dump.supply_volt < self.EMERGENCY_V):
            self.VEflag = True
            if self.cycles_since_pred > self.LEAD_TIME:
                self.insert_index = self.insert()

        self.volt_1_cycles_ago = cycle_dump.supply_volt

    def predict(self):
        prediction = (self.conv_max_norm[-2] < self.C_THRES and self.conv_max_norm[-1] > self.C_THRES) \
                and (self.cycles_since_pred > self.LEAD_TIME)
        return prediction

    def push_convmax(self, conv_max):
        self.conv_max.popleft()
        self.conv_max.append(conv_max)

        self.conv_max_norm.popleft()
        denom = max(self.conv_max) - min(self.conv_max)
        if denom > 0 :
            norm_conv_max = (conv_max - min(self.conv_max)) / denom
        else:
            norm_conv_max = 0
        # norm_conv_max = conv_max
        self.conv_max_norm.append(norm_conv_max)

    def addCycle(self, new_events):
        for row in self.history:
            row.popleft()
            row.append(0)

        for event in valid_events.keys():
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
        # for j in range(self.TABLE_HEIGHT):
        #     for i,e in enumerate(self.history):
        #         print(list(self.table[j][i])," : ", event_map_pred[i])
        #     print()
        print('HISTORY')
        for i,e in enumerate(self.history):
            print(list(e)," : ", valid_events[row_to_event[i]])
        print()

        if self.VEflag:
            print('Entering EMERGENCY state')
        else:
            print(self.STATE)
        if self.Actionflag:
            print("Prediction High")
        if self.insert_index != -1:
            print("Insert Entry Index: ", self.insert_index)

        # print('LRU: ', self.LRU)
        print('CONV result: ', self.convs_over_table)
        # print('new events: ', [self.cd.event_map[i] for i in self.cd.new_events_var])
        # print(self.events)
        # print(event_to_row)
        print('new events: ', [valid_events[row_to_event[i]] for i in self.events])

        # self.conv_max_norm.popleft()
        # denom = max(self.conv_max) - min(self.conv_max)
        # if denom > 0 :
        #     norm_conv_max = (conv_max - min(self.conv_max) / denom)
        # else:
        #     norm_conv_max = 0
        # # norm_conv_max = conv_max
        # self.conv_max_norm.append(norm_conv_max)