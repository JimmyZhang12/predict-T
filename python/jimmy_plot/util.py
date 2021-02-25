import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from collections import deque




class Cycle_Dump:
    cycles = 0

    def __init__(self, stats):
        self.stats = stats 
        self.ve_count = 0
        self.action_count = 0
        self.supply_curr = 0
        self.supply_volt = 0
        self.anchorPC = 0
        self.EOF = False

        self.stat_to_func = {
            "system.cpu.powerPred.supply_current": self.updateCurrent,
            "system.cpu.powerPred.supply_voltage": self.updateVoltage,
            'system.cpu.powerPred.event_count' : self.updateEventCount,
            "sim_ticks": self.updateCycles,
        }
        self.event_count = {}
        line = self.stats.readline() 
        line = self.stats.readline() 

        while(True):
            line = self.stats.readline() 
            while ('system' not in line and 'Begin Simulation Statistics' not in line):
                line = self.stats.readline() 

            #one cycle worth of stat dumps    
            if 'Begin Simulation Statistics' in line:
                break
            stat_name = line.split()[0].split(':')[0]
            if (stat_name == 'system.cpu.powerPred.event_count'):
                event_name = line.split()[0].split(':')[-1]
                event_count[event_name] = 0


    def updateCycles(self, line):
        self.cycles = int(line.split()[1]) / 250
        return 
    def updateCurrent(self,line):
        self.supply_curr = float(line.split()[1])
        return 
    def updateVoltage(self,line):
        self.supply_volt = float(line.split()[1])
        return 
    def updateEventCount(self,line):
        event_name = line.split()[0].split(':')[-1]
        self.event_count[event_name] = int(line.split()[1])


    def reset(self):        
        return


    def parseCycle(self):
        while(True):

            line = self.stats.readline() 
            while ('#' not in line and 'Begin Simulation Statistics' not in line):
                line = self.stats.readline() 

            if not line:
                return False
            #one cycle worth of stat dumps    
            if 'Begin Simulation Statistics' in line:
                return True

            stat_name = line.split()[0]
            if '::' in stat_name:
                stat_name = stat_name.split('::')[0]

            if (stat_name in self.stat_to_func.keys()):
                print(stat_name)
                print(line)
                func = self.stat_to_func[stat_name]
                func(line)

    def dump(self):
        print('******* CYCLE: ',self.cycles,'*********')
        print('SUPPLY CURRENT: ', self.supply_curr)
        print('SUPPLY VOLTAGE     : ', self.supply_volt)
        #print('SUPPLY VOLTAGE_prev: ', self.supply_volt_prev)
        print('ANCHOR PC: ', self.anchorPC)
        for k,v in self.event_count:
            print(k, " : ", v)
