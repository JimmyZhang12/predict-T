import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import harvard
import util
from enum import Enum
from datetime import datetime
import math

def plot_single(TEST, DATE):
    #PARAMETERS
    FONTSIZE = 18
    HOME = os.environ['HOME']

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2, 3)
    axb = fig.add_subplot(gs[0, :])
    axd = fig.add_subplot(gs[1, :])

    fig.suptitle('(Harvard)' +  ', DESKTOP, ' + "403.gcc" + ' )', fontsize=FONTSIZE)

    xvar = [x for x in range(22)]
    hits = [0,2,8,6,14,34,34,45,41,56,50,56,58,57,55,60,66,63,68,67,68,66]

    for i,x in enumerate(hits):
        hits.insert(i,x)
    axb.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
    axb.legend()
    axb.set_title('Accuracy', fontsize=14)
    axd.set_xlabel('Cycle (million)', fontsize=14) 
    axb.set_ylabel('(%)', fontsize=14)
    axb.set_ylim([0,100])


    false_pos_x = [x for x in range(22)]
    false_pos = [58,74,71,54,60,61,56,55,56,53,54,59,58,55,52,56,54,48,45,46,48,47]
    axd.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
    axd.legend()
    axd.set_title('False Positive', fontsize=14)
    axd.set_xlabel('Cycle (million)', fontsize=14) 
    axd.set_ylabel('(%)', fontsize=14)
    axd.set_ylim([0,100])

    file_dir = HOME+ '/plot/' + DATE + 'acccury_over_time' + '_harvard_' + TEST +'.png'
    plt.savefig(file_dir, dpi=300)
    print(file_dir)

if __name__ == "__main__":
    plot_single("403.gcc", "02-11-20")