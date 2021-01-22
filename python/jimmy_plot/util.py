import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from collections import deque, defaultdict



class PDN:
    def __init__(self, L, C, R, VDC, CLK):
        self.L = L
        self.C = C
        self.R = R
        self.VDC = VDC
        self.CLK = CLK
        self.vout_2_cycle_ago = VDC
        self.vout_1_cycle_ago = VDC
        self.iout_1_cycle_ago = 0
    def get_curr(self, current):
        ts = 1/self.CLK
        LmulC = self.L*self.C
        LdivR = self.L/self.R
        vout = self.VDC*ts**2/(LmulC) \
            + self.vout_1_cycle_ago*(2 - ts/(LdivR)) \
            + self.vout_2_cycle_ago*(ts/(LdivR) \
            - 1 - ts**2/(LmulC)) \
            - current*self.R*ts**2/(LmulC) \
            - (1/self.C)*ts*(current - self.iout_1_cycle_ago)
            
        self.vout_2_cycle_ago = self.vout_1_cycle_ago
        self.vout_1_cycle_ago = vout
        self.iout_1_cycle_ago = current
        return vout


class Events(Enum):
    NO_EVENT = 1
    BRANCH_T = 2
    BRANCH_NT = 3 
    BRANCH_MP = 4
    FETCH = 5 
    TLB_STALL = 6 
    ICACHE_STALL = 7
    COMMIT_BLOCK = 8
    IQ_FULL = 9
    LSQ_FULL = 10 
    LOAD_EX = 11
    LOAD_WB = 12
    LOAD_CFETCH = 13
    STORE_EXECUTE = 14
    STORE_WB = 15
    INSTR_DISPATCH = 16
    INSTR_ISSUE = 17
    INSTR_EXECUTE = 18
    INSTR_COMMIT = 19
    MEM_MP = 20
    EMPTY_EVENT = 21
    DUMMY_EVENT2 = 22
    #from other stats
    DCACHE_MISS = 23
    ICACHE_MISS = 24
    L2_MISS = 25
    TLB_MISS = 16

class Cycle_Dump:
    event_map = {
        #from new_events_stats
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
        21:'DUMMY_EVENT2',
        #from other stats
        22:'DCACHE_MISS',
        23:'ICACHE_MISS',
        24:'L2_MISS',
        25:'TLB_MISS',
    }
    new_events_blacklist = {
        0:'NO_EVENT',
        20:'EMPTY_EVENT',
        21:'DUMMY_EVENT2',
    }

    def __init__(self, stats):
        self.ve_count = 0
        self.action_count = 0
        self.stats = stats
        self.stats.readline()
        self.stats.readline()
        
        self.new_events_var = [] #list of new events the current cycle
        self.new_events_prev_var = [] #list of new events the previous cycle of the cycle dump
        self.table_index_count = 0
        self.cycle = None
        self.supply_curr = None
        self.supply_volt = None
        self.supply_volt_prev = None
        self.anchorPC_var = None
        self.numCycles_var = None

        self.branchMispredicts_count = 0
        self.memOrderViolationEvents_count = 0
        self.DcacheMisses_count = 0
        self.IcacheMisses_count = 0
        self.TLBcacheMisses_count = 0
        self.L2cacheMisses_count = 0

        keys = self.event_map.keys()
        self.event_count = {k: 0 for k in keys}
        self.EOF = False


    def reset(self):
        for e in self.new_events_var:
            self.event_count[e] += 1

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
        if (not event in self.new_events_blacklist.keys()) and (event not in self.new_events_var):
            self.new_events_var.append(event)
        return
    # # def new_events_prev(self,line):
    # #     linespl = line.split()
    # #     event = int(linespl[1])
    # #     if event != 20:
    # #         self.event_count[event] += 1
    # #         self.new_events_prev_var.append(event) 
    #     return
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

    def anchorPC(self, line):
        linespl = line.split()
        self.anchorPC_var = hex(int(linespl[1]))
        return
    def numCycles(self,line):
        linespl = line.split()
        self.numCycles_var = int(linespl[1])
        return

    # def branchMispredicts(self,line):
    #     linespl = line.split()
    #     val = int(linespl[1])
    #     if val > self.branchMispredicts_count:
    #         self.branchMispredicts_count = val
    #         self.new_events_var.append(3) #normally enum but its 2am
    
    # def memOrderViolationEvents(self,line):
    #     linespl = line.split()
    #     val = int(linespl[1])
    #     if val > self.memOrderViolationEvents_count:
    #         self.memOrderViolationEvents_count = val
    #         self.new_events_var.append(8) #normally enum but its 2am

    def overall_misses(self,line):
        linespl = line.split()
        val = int(linespl[1])
        cache = line.split()[0].split('.')[-2]

        if (cache == 'l2'):
            if val > self.L2cacheMisses_count:
                self.L2cacheMisses_count = val
                self.new_events_var.append(24) #normally enum but its 2am
        if (cache == 'dcache'):
            if val > self.DcacheMisses_count:
                self.DcacheMisses_count = val
                self.new_events_var.append(22) #normally enum but its 2am
        if (cache == 'icache'):
            if val > self.IcacheMisses_count:
                self.IcacheMisses_count = val
                self.new_events_var.append(23) #normally enum but its 2am
        if (cache == 'itb_walker_cache' or cache == 'dtb_walker_cache'):
            if val > self.TLBcacheMisses_count:
                self.TLBcacheMisses_count = val
                self.new_events_var.append(25) #normally enum but its 2am

    def parseCycle(self):
        while(True):
            line = self.stats.readline()  
            if not line:
                return True
            #end of 1 cycle of stat dump    
            elif (not line.upper().isupper()):
                for _ in range(4):
                    self.stats.readline()
                    if not line:
                        return True
                return False
            else:
            #one cycle worth of stat dumps    
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
        #print("EVENTS: ", [event_map[e] for e in self.new_events_var])
        # print("New Events : ", " ".join([event_map[i] for i in self.new_events_var]) )
        print("***********************************")


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

    # print(false_neg)
    # print(false_pos)
    return [xvar,hits,false_neg,false_pos_x,false_pos]  


TEST_LIST_spec=[
    #"400.perlbench", NO BINARIES
    "401.bzip2", 
    "403.gcc", 
    "410.bwaves", 
    #"416.gamess", NO BINARIES
    "429.mcf", 
    "433.milc", 
    "434.zeusmp", 
    "435.gromacs", 
    "436.cactusADM", 
    "437.leslie3d", 
    "444.namd", 
    "445.gobmk", 
    "447.dealII", 
    "450.soplex", 
    "453.povray", 
    "454.calculix", 
    "456.hmmer", 
    "458.sjeng", 
    "459.GemsFDTD", 
    "462.libquantum", 
    "464.h264ref", 
    "470.lbm", 
    "471.omnetpp", 
    "473.astar", 
    # "481.wrf", \
    # "482.sphinx3", \
    # "983.xalancbmk", \
    # "998.specrand", \
    # "999.specrand" \
    ]

TEST_LIST_mi = [
    "basicmath", 
    "bitcnts", 
    "blowfish_decrypt", 
    "blowfish_encrypt", 
    "qsort", 
    "susan_smooth",
    # "susan_edge", 
    # "susan_corner", 
    "dijkstra", 
    "rijndael_decrypt", 
    # "rijndael_encrypt", 
    "sha", 
    "crc", 
    "fft", 
    "ffti", 
    "toast", 
    "untoast"
]
