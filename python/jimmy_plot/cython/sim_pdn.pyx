#example_cython.pyx
from cython.view cimport array as cvarray
from libcpp cimport bool
import numpy as np
cimport numpy as np



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
        
        cdef double vout = self.VDC*ts**2/(self.LmulC) \
            + self.vout_1_cycle_ago*(2 - ts/(self.LdivR)) \
            + self.vout_2_cycle_ago*(ts/(self.LdivR) \
            - 1 - ts**2/(self.LmulC)) \
            - current*self.R*ts**2/(self.LmulC) \
            - (1/self.C)*ts*(current - self.iout_1_cycle_ago)
            
        self.vout_2_cycle_ago = self.vout_1_cycle_ago
        self.vout_1_cycle_ago = vout
        self.iout_1_cycle_ago = current
        return vout


cdef get_voltage(double[:] current, double thres, PDN pdn):
    I = current.shape[0]
    cdef np.ndarray[double, ndim=1] volt = np.zeros([I], dtype=np.double)
    cdef list ve_cycle = []
    
    cdef int i
    for i in range(I):
        volt[i] = pdn.get_volt(current[i])
        if volt[i] < thres and volt[i-1] > thres:
            ve_cycle.append(i)
    cdef ve_cycle_ret = np.asarray(ve_cycle, np.uint)
    return [volt,ve_cycle_ret]

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
    double[:] throttle_curr, 
    double[:] reg_curr, 
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

    I = throttle_curr.shape[0]
    for i in range(I):
        if is_throttle:
            curr = throttle_curr[i]
        else:
            curr = reg_curr[i]

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

def detect_VE_throttle_wrapper(throttle_curr, reg_curr,
    THROTTLE_DUR, LEAD_TIME,
    _THRES, _L, _C, _R, _VDC, _CLK, _start_throttle, _end_throttle):
    cdef pdn = PDN(
        L = _L,
        C = _C,
        R = _R,
        VDC = _VDC,
        CLK = _CLK,
    )  
    cdef double [:] c_throttle_curr = throttle_curr
    cdef double [:] c_reg_curr = reg_curr

    cdef int [:] start_throttle = _start_throttle
    cdef int [:] end_throttle = _end_throttle

    return detect_VE_throttle(c_throttle_curr, c_reg_curr, 
        THROTTLE_DUR, LEAD_TIME,
        _THRES, pdn, start_throttle, end_throttle)

cpdef get_volt_wrapper(current, _THRES, _L, _C, _R, _VDC, _CLK):
    cdef pdn = PDN(
        L = _L,
        C = _C,
        R = _R,
        VDC = _VDC,
        CLK = _CLK,
    )  
    cdef double [:] c_current = current

    return get_voltage(c_current, _THRES, pdn)