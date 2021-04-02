#example_cython.pyx
from cython.view cimport array as cvarray
from libcpp cimport bool
import numpy as np


cdef class PDN:
    cdef double L,C,R,VDC,CLK
    cdef double vout_2_cycle_ago, vout_1_cycle_ago, iout_1_cycle_ago
    cdef double LmulC, LdivR
    def __cinit__(self, double L, double C, double R, double VDC, double CLK):
        self.L = L
        self.C = C
        self.R = R
        self.VDC = VDC
        self.CLK = CLK
        self.vout_2_cycle_ago = VDC
        self.vout_1_cycle_ago = VDC
        self.iout_1_cycle_ago = 0
        self.LmulC = self.L*self.C
        self.LdivR = self.L/self.R
    cdef void reset(self):
        self.vout_2_cycle_ago = self.VDC
        self.vout_1_cycle_ago = self.VDC
        self.iout_1_cycle_ago = 0
    cdef double get_volt(self, double current):
        ts = 1/self.CLK
        
        vout = self.VDC*ts**2/(self.LmulC) \
            + self.vout_1_cycle_ago*(2 - ts/(self.LdivR)) \
            + self.vout_2_cycle_ago*(ts/(self.LdivR) \
            - 1 - ts**2/(self.LmulC)) \
            - current*self.R*ts**2/(self.LmulC) \
            - (1/self.C)*ts*(current - self.iout_1_cycle_ago)
            
        self.vout_2_cycle_ago = self.vout_1_cycle_ago
        self.vout_1_cycle_ago = vout
        self.iout_1_cycle_ago = current
        return vout


cdef detect_VE(double[:] current, double thres, PDN pdn):
    cdef list ve_cycle = []

    cdef int count = 0
    cdef double v_prev = pdn.VDC
    cdef double v_curr = pdn.VDC

    I = current.shape[0]
    for i in range(I):
        v_curr = pdn.get_volt(current[i])
        if v_curr < thres and v_prev > thres:
            count+=1
            ve_cycle.append(i)
        v_prev = v_curr
    return ve_cycle

cdef int detect_VE_throttle(
    double[:] dyn_current, 
    double stc_current,
    int throttle_dur,
    int lead_time,
    double thres, 
    PDN pdn, 
    int[:] start_throttle,
    int[:] end_throttle):

    cdef int count = 0
    cdef double v_prev = pdn.VDC
    cdef double v_curr = pdn.VDC
    cdef bint is_throttle = False
    cdef double curr = 0
    cdef int start_throttle_ind = 0
    cdef int end_throttle_ind = 0

    I = dyn_current.shape[0]
    for i in range(I):
        if is_throttle:
            curr = dyn_current[i]/2 + stc_current
        else:
            curr = dyn_current[i] + stc_current

        v_curr = pdn.get_volt(curr)
        if v_curr < thres and v_prev > thres:
            count+=1
        
        if start_throttle[start_throttle_ind] == i:
            if start_throttle_ind != start_throttle.shape[0]-1: 
                start_throttle_ind+=1
                is_throttle = True
                pdn.CLK = 2E9

        if end_throttle[end_throttle_ind] == i:
            if end_throttle_ind != end_throttle.shape[0]-1: 
                end_throttle_ind+=1
                is_throttle = False
                pdn.CLK = 4E9
        
        v_prev = v_curr
    return count


cpdef detect_VE_wrapper(current, _THRES, _L, _C, _R, _VDC, _CLK):
    cdef pdn = PDN(
        L = _L,
        C = _C,
        R = _R,
        VDC = _VDC,
        CLK = _CLK,
    )  
    cdef double [:] c_current = current

    return detect_VE(c_current, _THRES, pdn)

cpdef detect_VE_throttle_wrapper(dyn_current, stc_current,
    THROTTLE_DUR, LEAD_TIME,
    _THRES, _L, _C, _R, _VDC, _CLK, _start_throttle, _end_throttle):
    cdef pdn = PDN(
        L = _L,
        C = _C,
        R = _R,
        VDC = _VDC,
        CLK = _CLK,
    )  
    cdef double [:] c_dyn_current = dyn_current
    cdef int [:] start_throttle = _start_throttle
    cdef int [:] end_throttle = _end_throttle

    return detect_VE_throttle(c_dyn_current, stc_current, 
        THROTTLE_DUR, LEAD_TIME,
        _THRES, pdn, start_throttle, end_throttle)