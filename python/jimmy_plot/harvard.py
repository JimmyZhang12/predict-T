import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from collections import deque, defaultdict

valid_events = {
    0:'NO_EVENT',
    1:'BRANCH_T',
    2:'BRANCH_NT',
    3:'BRANCH_MP',
    19:'MEM_MP',
    20:'EMPTY_EVENT',

    22:'DCACHE_MISS',
    23:'ICACHE_MISS',
    24:'L2_MISS',
    25:'TLB_MISS',
}


class Entry:
    def __init__(self, pc=0, events=[]):
            self.pc = pc
            self.events = tuple(events)

    def equals(self, entry):
        if entry is None:
            return False
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
        self.h_table =  [ Entry(0,[0]*SIGNATURE_LENGTH) for _ in range(TABLE_HEIGHT)]
        self.history = deque([0]*SIGNATURE_LENGTH)
        self.cycle_since_pred = 0

        self.insertIndex = -1
        self.cycle_predict = -1

        self.VEflag = False
        self.Actionflag = False
        self.prev_volt = 0
        self.curr_entry = None
        self.prev_entry = Entry()
        self.event_count = defaultdict(lambda: 0)
        

    def tick(self, cycle_dump):
        events = []
        for e in cycle_dump.new_events_var:
            if e in valid_events.keys():
                events.append(e)


        self.insertIndex = -1
        self.cycle_predict = -1
        self.VEflag = False
        self.Actionflag = False

        for i in range(self.TABLE_HEIGHT):
            self.lru[i] += 1

        #update
        self.cycle_since_pred += 1
        self.history_insert(events)
        self.curr_entry = Entry(pc=cycle_dump.anchorPC_var, events=self.history)
        #predict
        #if not self.curr_entry.equals(self.prev_entry): #and self.cycle_since_pred > self.LEAD_TIME:
        if events or (self.prev_entry.pc != self.curr_entry.pc):
            self.cycle_predict = self.find(self.curr_entry)
            if self.cycle_predict != -1:
                self.cycle_since_pred = 0
                self.Actionflag = True

        if (cycle_dump.supply_volt < self.EMERGENCY_V and self.prev_volt > self.EMERGENCY_V):
            self.VEflag = True
            if self.cycle_since_pred > self.LEAD_TIME:
                self.insertIndex = self.insert(self.curr_entry)
        
        self.prev_volt = cycle_dump.supply_volt
        self.prev_entry = self.curr_entry
        return

    def history_insert(self, events):
        for e in events:
            self.event_count[e] += 1
            self.history.popleft()
            self.history.append(e)

    def find(self, entry):
        for i, table_entry in enumerate(self.h_table):
            if entry.equals(table_entry):
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
            print(i,':  ',self.lru[i], self.h_table[i].pc,  [valid_events[e] for e in self.h_table[i].events])
        print("HISTORY: ", [valid_events[e] for e in self.history])
        print("Cycles since Prediction: ", self.cycle_since_pred)
        if self.Actionflag:
            print('cycle PREDICTION HIGH :' + str(self.cycle_predict)) 
        if self.VEflag:
            print('Entering EMERGENCY state')
            print('insert ENTRY :' + str(self.insertIndex)) 
        else:
            print(self.STATE)

