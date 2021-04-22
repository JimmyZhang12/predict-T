from cython.view cimport array as cvarray
from libcpp cimport bool
import numpy as np
cimport numpy as np


cdef long_latency_cycles_(double[:] current, double idle_curr, int idle_cycle_thres):
    cdef list idle_cycle = []
    cdef int idle_count = 0

    I = current.shape[0]
    for i in range(I):
        if current[i] > 30:
            idle_count += 1
        else:
            if idle_count > idle_cycle_thres:
                idle_cycle.append(i)
            idle_count = 0


    return idle_cycle

cpdef long_latency_cycles(current, idle_curr, idle_cycle_thres):  
    cdef double [:] current_ = current
    return long_latency_cycles_(current_, idle_curr, idle_cycle_thres)