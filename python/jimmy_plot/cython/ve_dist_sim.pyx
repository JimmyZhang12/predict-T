from cython.view cimport array as cvarray
from libcpp cimport bool
import numpy as np
import math
cimport numpy as np

'''
inputs:
    pc_data: 1 data value per cycle
        if taken branch on cycle i, pc_data[i] = target pc
        else pc_data[i] = 0
    ve_cycle_data: list of cycles where VEs happen

returns:
    (avg_ve_dist,perc_pc,total_pcs)
    list avg_ve_dist:, index is a pc, value avg cycles of pc occurance after VE
    list perc_pc:, index is a pc, value pc's percentage of total taken PCs 
    int total_pcs:, total number of taken branches
    list pc_list, the list of pcs 
'''
cdef ve_dist(unsigned long[:] pc_data, unsigned long [:] ve_cycle_data):
    np.sort(ve_cycle_data)
    np.append(ve_cycle_data, 1e30)

    cdef dict pc_freq = {}
    cdef dict pc_cum_ve_dist = {}

    cdef unsigned long pc
    cdef unsigned int ve_cycle_ind = 0

    I = pc_data.shape[0]
    for i in range(I):
        if i > ve_cycle_data[ve_cycle_ind+1]:
            ve_cycle_ind += 1
        pc = pc_data[i]
        if pc != 0:
            if pc not in pc_freq:
                pc_freq[pc] = 0
            if pc not in pc_cum_ve_dist:
                pc_cum_ve_dist[pc] = 0
            pc_freq[pc]+=1
            pc_cum_ve_dist[pc] += (i - ve_cycle_data[ve_cycle_ind])
    
    for pc in pc_freq.keys(): #normalize pc_freq 
        val = pc_cum_ve_dist[pc]
        val /= pc_freq[pc] 
        pc_cum_ve_dist[pc] = val


    cdef dict pc_std_dev = {}
    ve_cycle_ind = 0
    I = pc_data.shape[0]
    for i in range(I):
        if i > ve_cycle_data[ve_cycle_ind+1]:
            ve_cycle_ind += 1
        pc = pc_data[i]
        if pc != 0:
            if pc not in pc_std_dev:
                pc_std_dev[pc] = 0
            pc_std_dev[pc]+= ((i - ve_cycle_data[ve_cycle_ind]) - pc_cum_ve_dist[pc])**2
    for pc in pc_std_dev.keys(): #normalize pc_freq 
        val = pc_std_dev[pc]
        val /= pc_freq[pc] 
        val = math.sqrt(val)
        pc_std_dev[pc] = val

    #convert to arrays that can be ploted
    avg_vedist = [(pc, dist) for pc, dist in pc_cum_ve_dist.items()]
    avg_vedist.sort(key = lambda x: x[1]) 
    total_pcs = sum(pc_freq.values())

    ret_data = dict()
    for pc, dist in pc_cum_ve_dist.items():
        pc_stnd_dev = pc_std_dev[pc]
        perc_pc = pc_freq[pc]/total_pcs 
        ret_data[pc] = (dist,perc_pc,pc_stnd_dev)
        
    avg_ve_dist = [i[1] for i in avg_vedist] 
    pc_list = [i[0] for i in avg_vedist] 
    perc_pc = [pc_freq[i[0]]/total_pcs for i in avg_vedist]
    pc_stnd_dev = [pc_std_dev[i[0]] for i in avg_vedist]

    return (avg_ve_dist,perc_pc,pc_stnd_dev,total_pcs,pc_list,ret_data)


cpdef ve_dist_wrapper(pc_data, ve_cycle_data):
    cdef unsigned long [:] pc_data_ = pc_data
    cdef unsigned long [:] ve_cycle_data_ = ve_cycle_data

    return ve_dist(pc_data_, ve_cycle_data_)

