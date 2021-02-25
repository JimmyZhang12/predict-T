import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import util
from enum import Enum
from datetime import datetime
import math
import random

def plot_all(TEST_LIST, DATE):


    #PARAMETERS
    FONTSIZE = 12
    HOME = os.environ['HOME']
    x = np.arange(len(TEST_LIST))

    fig = plt.figure(constrained_layout=True)          
    fig.set_size_inches(25, 25)
    fig.suptitle('(Harvard)' +  ', DESKTOP)')

    gs = fig.add_gridspec(4, 5)

    ax = fig.add_subplot(gs[0, :])
    ax.set_xticks(x)
    ax.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)

    ax_fp = fig.add_subplot(gs[1, :])
    ax_fp.set_xticks(x)
    ax_fp.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)

    ax_fn = fig.add_subplot(gs[2, :])
    ax_fn.set_xticks(x)
    ax_fn.set_xticklabels(TEST_LIST,fontsize = FONTSIZE)

    hit_avg = 0
    fp_avg = 0
    fn_avg = 0

    for x,TEST in enumerate(TEST_LIST):
        print("Plotting: ",TEST)
        # HOME = os.environ['HOME']
        # action =      np.load(HOME+'/plot/data/harvard_'+DATE+'_action_'+TEST +'.npy')
        # VE =          np.load(HOME+'/plot/data/harvard_'+DATE+'_VE_'+TEST +'.npy')

        # xvar,hits,false_neg,false_pos_x,false_pos = util.accuracy(action[-20000:],VE[-20000:], LEAD_TIME_CAP=40)   

        ax.bar(x,hits[x], color = 'RED')
        ax_fp.bar(x,false_pos[x], color = 'RED')
        # ax_fn.bar(x,min(false_neg), color = 'RED')

        hit_avg += (hits[x])
        fp_avg += false_pos[x]
        # fn_avg += min(false_neg)
    hit_avg /= len(TEST_LIST)
    fp_avg /= len(TEST_LIST)
    # fn_avg /= len(TEST_LIST)
    ax.set_title('Hit (Max) Average = ' + str(hit_avg), fontsize=FONTSIZE*2)
    ax_fp.set_title('False Pos (Min) Average = '+ str(fp_avg), fontsize=FONTSIZE*2)
    ax_fn.set_title('False Neg (Min) Average = '+ str(fn_avg), fontsize=FONTSIZE*2)

    plt.savefig(HOME+ '/plot/' + DATE + '_all_tests' + '_conv.png', dpi=300)


if __name__ == "__main__":
    plot_all(util.TEST_LIST_spec, "02-19-20")
