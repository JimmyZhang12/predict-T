# distutils: language = c++

from cython.view cimport array as cvarray
from libcpp cimport bool
import numpy as np
cimport numpy as np
import ve_dist_sim
from libcpp.deque cimport deque
from collections import deque as py_deque 

from libcpp.vector cimport vector
from cython.operator cimport dereference as deref, preincrement as inc


cdef class Calc_Accuracy:
    cdef int cycles_since_ve, cycles_since_pred, lead_time_max
    cdef public int ve_count, pred_count, caught_ves, caught_preds
    cdef deque[bint] pred_history

    def __cinit__(self, int lead_time):
        self.lead_time_max = lead_time
        self.cycles_since_pred = 0 
        self.cycles_since_ve = 0
        self.ve_count = 0
        for i in range(lead_time):
            self.pred_history.push_back(False)
   
    cdef public void update(self,bint ve, bint pred):
        self.pred_history.push_back(pred)
        self.pred_history.pop_front()
        if pred:
            self.pred_count += 1
            self.cycles_since_pred = 0
        else:
            self.cycles_since_pred +=1

        if ve:
            self.cycles_since_ve = 0
            self.ve_count += 1
            if self.cycles_since_pred < self.lead_time_max:
                self.caught_ves += 1
            
        else:
            self.cycles_since_ve +=1 

        if self.pred_history[0]:
            if self.cycles_since_ve <= self.lead_time_max:
                self.caught_preds += 1;   

    cdef public bint ve_caught(self):
        return (self.cycles_since_ve - self.cycles_since_pred) < self.lead_time_max

    cdef public double get_hitrate(self):
        cdef double hitrate = <float>self.caught_ves / <float>self.ve_count
        return hitrate

    cdef public double get_fprate(self):
        cdef double fprate
        if self.pred_count > 0:
            fprate = 1 - <float>self.caught_preds/<float>self.pred_count
        return fprate


cdef std_dev_predictor(
    Calc_Accuracy accuracy_tracker, 
    unsigned long[:] pc_data, 
    unsigned long [:] ve_cycle_data,
    double [:] voltage):

    cdef set ve_cycle = set(ve_cycle_data)
    (ve_dist,perc_pc,pc_std_dev,total_pcs,pc_list,data) = ve_dist_sim.ve_dist_wrapper(pc_data,ve_cycle_data)

    cdef set pred_pcs = set()
    cdef double last_pc = 0
    cdef int time_since_ve = 0
    for i in range(len(pc_data)):
        if pc_data[i] != 0:
            last_pc = pc_data[i]
        if i in ve_cycle and time_since_ve:
            time_since_ve = 0
            pred_pcs.add(last_pc)
        else:
            time_since_ve += 1

    print('num pcs: ', len(pred_pcs))

    cdef bint ve = False
    cdef bint pred = False
    cdef pred_history = py_deque([0]*10)
    cdef set pred_table = set()
    cdef vector[int] delay_queue
    cdef vector[int].iterator it = delay_queue.begin()

    for i in range(len(pc_data)):
        if i%10000000 == 0:
            print('cycle ',i,'.....')

        ve = False
        pred = False

        if i in ve_cycle:
            ve = True

        if pc_data[i] in pred_pcs:
            delay_queue.push_back(data[pc_data[i]][0]-40) #ve distance - leadtime
        it = delay_queue.begin()
        while(it != delay_queue.end()):
            val = &deref(it)
            val[0] = val[0]-1

            if deref(it) <=0 :
                pred = True
                it = delay_queue.erase(it)
            else:
                inc(it)
        accuracy_tracker.update(ve,pred)


        '''
        if pc_data[i] != 0:
            pred_history.append(pc_data[i])
            pred_history.popleft()
        ve = False
        pred = False

        if i in ve_cycle:
            ve = True

        if pred_history in tuple(pred_table):
            pred = True
        accuracy_tracker.update(ve,pred)

        if not accuracy_tracker.ve_caught():
            pred_table.add(pred_history)
        '''
    print('total preds: ', accuracy_tracker.pred_count)
    print('total ves: ', accuracy_tracker.ve_count)
    print('caught ves: ', accuracy_tracker.caught_ves)

    return (accuracy_tracker.get_hitrate(), accuracy_tracker.get_fprate())




cpdef run_prediction_wrapper(pc_data, ve_cycle_data, voltage):
    cdef unsigned long [:] pc_data_ = pc_data
    cdef unsigned long [:] ve_cycle_data_ = ve_cycle_data
    cdef double [:] voltage_ = voltage

    cdef accuracy_tracker = Calc_Accuracy(lead_time = 50)  

    return std_dev_predictor(accuracy_tracker,pc_data_, ve_cycle_data_, voltage_)

