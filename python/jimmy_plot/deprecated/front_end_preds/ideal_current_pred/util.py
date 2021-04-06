import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from collections import deque


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

event_map_filter = {
    3:'BRANCH_MP',
    5:'TLB_STALL',
    6:'ICACHE_STALL',
    7:'COMMIT_BLOCK',
    16:'INSTR_ISSUE',
    19:'MEM_MP',
    }


class Cycle_Dump:
    def __init__(self, stats):
        self.ve_count = 0
        self.action_count = 0
        self.stats = stats
        #self.stats.readline()
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
        print('SUPPLY VOLTAGE: ', self.supply_volt)
        #print('SUPPLY VOLTAGE_prev: ', self.supply_volt_prev)
        print('ANCHOR PC: ', self.anchorPC_var)
        # print("New Events : ", " ".join([event_map[i] for i in self.new_events_var]) )
        # print("New Events prev: ", " ".join([event_map[i] for i in self.new_events_prev_var]))

class Entry:
    def __init__(self, pc, events):
            self.pc = pc
            self.events = list(events)

    def equals(self, entry):
        if (self.pc == entry.pc and self.events == entry.events):
            return True
        return False

class Harvard:
    class State(Enum):
        NORMAL = 0
        EMERGENCY = 1 

    def __init__(self,TABLE_HEIGHT, SIGNATURE_LENGTH, HYSTERESIS, EMERGENCY_V, LEAD_TIME):
        self.TABLE_HEIGHT = TABLE_HEIGHT
        self.SIGNATURE_LENGTH = SIGNATURE_LENGTH
        self.HYSTERESIS = HYSTERESIS
        self.EMERGENCY_V = EMERGENCY_V
        self.LEAD_TIME = LEAD_TIME
        self.STATE = self.State.NORMAL

        self.lru = [0] * TABLE_HEIGHT
        self.h_table =  [ Entry(0,[20]*SIGNATURE_LENGTH) for _ in range(TABLE_HEIGHT)]
        self.history = deque([0]*SIGNATURE_LENGTH)
        self.cycle_since_pred = 0
        self.prev_volt = 0

        self.insertIndex_prev = -1
        self.insertIndex = -1
        self.prev_cycle_predict = -1
        self.curr_cycle_predict = -1

        self.VEflag = False
        self.Actionflag = False

    def tick(self, cycle_dump):
        self.insertIndex_prev = -1
        self.insertIndex = -1
        self.prev_cycle_predict = -1
        self.curr_cycle_predict = -1
        self.VEflag = False
        self.Actionflag = False
        for i in range(self.TABLE_HEIGHT):
            self.lru[i] += 1

        #advance two cycles 
        #first cycle
        self.cycle_since_pred += 1
        history_prev = deque(self.history)
        self.history_insert(cycle_dump.new_events_prev_var)
        self.entry_prev = Entry(cycle_dump.anchorPC_var, self.history)
        if (history_prev != self.history):
            self.prev_cycle_predict = self.find(self.entry_prev)
            if self.prev_cycle_predict != -1:
                self.cycle_since_pred = 0
        #second cycle
        self.cycle_since_pred += 1
        history_prev = deque(self.history)
        self.history_insert(cycle_dump.new_events_var)
        self.entry_curr = Entry(cycle_dump.anchorPC_var, self.history)
        if (history_prev != self.history):
            self.curr_cycle_predict = self.find(self.entry_curr)
            if self.curr_cycle_predict != -1:
                self.cycle_since_pred = 0

        if (cycle_dump.supply_volt < self.EMERGENCY_V and self.prev_volt > self.EMERGENCY_V):
            self.VEflag = True
            if self.cycle_since_pred > self.LEAD_TIME:
                if self.curr_cycle_predict == -1:
                    self.insertIndex = self.insert(self.entry_prev)
                if self.prev_cycle_predict == -1:
                    self.insertIndex_prev = self.insert(self.entry_curr)


        self.prev_volt = cycle_dump.supply_volt
        if (self.prev_cycle_predict != -1) and (self.curr_cycle_predict != -1):
            self.Actionflag = True

        return

    def history_insert(self, events):
        events_compact = []
        for e in events:
            if e not in events_compact and e in event_map_filter.keys():
                events_compact.append(e)

        for e in events_compact:
            self.history.popleft()
            self.history.append(e)

    def find(self, entry):
        for i in range(self.TABLE_HEIGHT):
            if self.h_table[i].equals(entry):
                self.lru[i] = 0
                return i
        return -1
    def insert(self, entry):
        index = self.lru.index(max(self.lru))
        self.h_table[index] = entry
        self.lru[index] = 0
        return index

    def print(self):
        for i in range(self.TABLE_HEIGHT):
            print(i,':  ', self.h_table[i].pc,  [event_map[e] for e in self.h_table[i].events])
        print("HISTORY: ", [event_map[e] for e in self.history])

        if self.prev_cycle_predict != -1:
            print('cycle PREDICTION HIGH prev :' + str(self.prev_cycle_predict))
        if self.curr_cycle_predict != -1:
            print('cycle PREDICTION HIGH curr :' + str(self.curr_cycle_predict)) 
        if self.insertIndex_prev != -1:
            print('insert ENTRY prev :' + str(self.insertIndex_prev))
        if self.insertIndex != -1:
            print('insert ENTRY curr :' + str(self.insertIndex)) 
        if self.VEflag:
            print('Entering EMERGENCY state')
        else:
            print(self.STATE)


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
