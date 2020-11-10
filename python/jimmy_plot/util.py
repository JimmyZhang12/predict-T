import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum

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
    13:'DUMMY_EVENT',
    14:'DUMMY_EVENT2'
    }

class Cycle_Dump:
    def __init__(self, stats):
        self.ve_count = 0
        self.action_count = 0
        self.stats = stats
        self.stats.readline()
        self.stats.readline()
        self.EOF = False
    def reset(self):
        self.signature = []
        self.signature_prev = []
        self.table_index_count = 0
        self.cycle = None
        self.supply_curr = None
        self.supply_volt = None
        self.supply_volt_prev = None
        self.anchorPC_var = None
        self.numCycles_var = None
        
        return
    def inserted_New_Entry(self, line):
        linespl = line.split()
        event = event_map[int(linespl[1])]
        self.signature.append(event) 
        return
    def inserted_New_Entry_prev(self, line):
        linespl = line.split()
        event = event_map[int(linespl[1])]
        self.signature_prev.append(event) 
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
        print('SUPPLY VOLTAGE_prev: ', self.supply_volt_prev)
        print('ANCHOR PC: ', self.anchorPC_var)
        print("HISTORY REGISTER     : ", self.signature)
        print("HISTORY REGISTERprev : ", self.signature_prev)



class Harvard:
    class State(Enum):
        NORMAL = 0
        EMERGENCY = 1 

    def __init__(self,TABLE_HEIGHT, SIGNATURE_LENGTH, HYSTERESIS, EMERGENCY_V):
        self.TABLE_HEIGHT = TABLE_HEIGHT
        self.SIGNATURE_LENGTH = SIGNATURE_LENGTH
        self.HYSTERESIS = HYSTERESIS
        self.EMERGENCY_V = EMERGENCY_V
        self.STATE = self.State.NORMAL
        self.lru = [0] * TABLE_HEIGHT
        self.h_table =  [([event_map[1]] * SIGNATURE_LENGTH) for _ in range(TABLE_HEIGHT)]
        self.insertIndex_prev = -1
        self.insertIndex = -1
        self.prev_cycle_predict = -1
        self.curr_cycle_predict = -1
        self.sig = []
        self.sig_prev = []
        self.VEflag = False
        self.Actionflag = False

    def tick(self, cycle_dump):
        curr_sig = cycle_dump.signature[-1*self.SIGNATURE_LENGTH:]
        prev_sig = cycle_dump.signature_prev[-1*self.SIGNATURE_LENGTH:]

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
        if (prev_sig != self.sig_prev):
            self.prev_cycle_predict = self.find(prev_sig)
        if (curr_sig != self.sig):
            self.curr_cycle_predict = self.find(curr_sig)
        self.sig = curr_sig
        self.sig_prev = prev_sig

        if self.STATE is self.State.NORMAL:
            if cycle_dump.supply_volt < self.EMERGENCY_V and cycle_dump.supply_volt > 0.01:
                self.VEflag = True
                self.STATE = self.State.EMERGENCY
                if self.curr_cycle_predict == -1:
                    self.insertIndex = self.insert(curr_sig)
                if self.prev_cycle_predict == -1:
                    self.insertIndex_prev = self.insert(prev_sig)
        elif self.STATE is self.State.EMERGENCY:
            if cycle_dump.supply_volt > self.EMERGENCY_V + self.HYSTERESIS:
                self.STATE = self.State.NORMAL

        if (self.prev_cycle_predict != -1) and (self.curr_cycle_predict != -1):
            self.Actionflag = True

        return
        
    def find(self, entry):
        for i in range(self.TABLE_HEIGHT):
            if self.h_table[i] == entry:
                self.lru[i] = 0
                return i
        return -1
    def insert(self, entry):
        index = self.lru.index(max(self.lru))
        self.h_table[index] = entry
        self.lru[index] = 0
        return index

    def print(self):
        # for i in range(self.TABLE_HEIGHT):
        #     print(i,':  ', self.h_table[i])
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
                if i-j < 0: break
                if action[i-j]:
                    if j in act_bins.keys(): act_bins[j] += 1
                    else: act_bins[j] = 1

    print(bins)
    print(act_bins)

    xvar = [-1]
    hits = [-1]
    false_neg = [-1]
    running_sum = 0
    VE_count = sum(VE)
    for i in sorted(bins):
        running_sum += bins[i]
        false_neg.append(100*(VE_count - running_sum) / VE_count)
        xvar.append(i)
        hits.append(100 * running_sum / VE_count)

    false_pos_x = [-1]
    false_pos = [-1]
    action_count = sum(action)
    running_sum = 0
    for i in sorted(act_bins):
        running_sum += act_bins[i]
        false_pos.append(100*(action_count - running_sum ) / action_count)
        false_pos_x.append(i)   
        
    for i in range(len(xvar)):
        xvar[i] = xvar[i] + 1 
    for i in range(len(false_pos_x)):
        false_pos_x[i] = false_pos_x[i] + 1

    return [xvar,hits,false_neg,false_pos_x,false_pos] 
