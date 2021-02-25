import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from datetime import datetime
import math
import random
def plot_single(TEST, DATE):
    #PARAMETERS
    FONTSIZE = 18
    HOME = os.environ['HOME']

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2, 3)
    axb = fig.add_subplot(gs[0, :])
    axd = fig.add_subplot(gs[1, :])

    fig.suptitle('(_conv_)' +  ', DESKTOP, ' + "435.gromacs" + ' )', fontsize=FONTSIZE)

    axb.plot(xvar, hits, color='black', linewidth=1.0, label='hits')
    axb.legend()
    axb.set_title('Accuracy', fontsize=14)
    axd.set_xlabel('Cycle (million)', fontsize=14) 
    axb.set_ylabel('(%)', fontsize=14)
    axb.set_ylim([0,100])


    axd.plot(false_pos_x, false_pos, color='blue', linewidth=1.0, label='false positives')
    axd.legend()
    axd.set_title('False Positive', fontsize=14)
    axd.set_xlabel('Cycle (million)', fontsize=14) 
    axd.set_ylabel('(%)', fontsize=14)
    axd.set_ylim([0,100])

    file_dir = HOME+ '/plot/' + DATE + 'acccury_over_time' + '_conv_' + TEST +'.png'
    plt.savefig(file_dir, dpi=300)
    print(file_dir)

if __name__ == "__main__":
    plot_single("435.gromacs", "02-19-20")