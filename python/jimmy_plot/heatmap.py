import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import decimal 
import numpy as np
import os

TEST_LIST_spec=[
    # "400.perlbench", NO BINARIES
    # "401.bzip2", 
    # "403.gcc", 
    # "410.bwaves", 
    # # "416.gamess", NO BINARIES
    "429.mcf", 
    "433.milc", 
    # "434.zeusmp", 
    "435.gromacs", 
    "436.cactusADM", 
    "437.leslie3d", 
    "444.namd", 
    "445.gobmk", 
    # "447.dealII", 
    # "450.soplex", 
    "453.povray", 
    "454.calculix", 
    "456.hmmer", 
    # "458.sjeng", 
    "459.GemsFDTD", 
    "462.libquantum", 
    "464.h264ref", 
    # # "470.lbm", 
    "471.omnetpp", 
    "473.astar", 
    "481.wrf", \
    "482.sphinx3", \
    # # "983.xalancbmk", \
    # # "998.specrand", \
    # # "999.specrand" \
    ]


def plot(x,y,num_ves):
    fig, ax = plt.subplots()
    im = ax.imshow(num_ves)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x)))
    ax.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x)
    ax.set_yticklabels(y)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(y)):
        for j in range(len(x)):
            val = str(round(num_ves[i, j]*100,1))
            text = ax.text(j, i, val,
                        ha="center", va="center", color="w")
    FONTSIZE = 20
    ax.set_title("Percent VE not Mitigated - lower is better", fontsize = FONTSIZE)
    ax.set_xlabel("Throttle Duration", fontsize = FONTSIZE)
    ax.set_ylabel("Lead Time")

    fig.set_size_inches(18.5, 18.5)

    HOME = os.environ['HOME']
    DATE = '4-2-2021_'
    NAME = 'HEATMAP qsort'
    file_dir = HOME+ '/plot/' + DATE + NAME +'.png'
    plt.savefig(file_dir, dpi=300)
    print(file_dir)

def run_all(load_paths):
    total_ves = 0
    raw_data = np.load(load_paths[0])
    x = []
    y = []
    for i in raw_data:
        x.append(i[0])
        y.append(i[1])

    x = list(set(x))
    x.sort()
    y = list(set(y))
    y.sort()

    num_ves = np.zeros((len(y), len(x)))

    for load_path in load_paths:

        raw_data = np.load(load_path)
        total_ves += raw_data[0][2]
        for i in raw_data:
            x_ind = x.index(i[0])
            y_ind = y.index(i[1])
            num_ves[y_ind][x_ind] += i[2]
    np.true_divide(num_ves,total_ves)
    plot(x,y,num_ves)

def run(load_path):
    raw_data = np.load(load_path)
    total_ves = raw_data[0][2]
    x = []
    y = []
    for i in raw_data:
        x.append(i[0])
        y.append(i[1])

    x = list(set(x))
    x.sort()
    y = list(set(y))
    y.sort()

    num_ves = np.zeros((len(y), len(x)))

    for i in raw_data:
        x_ind = x.index(i[0])
        y_ind = y.index(i[1])
        num_ves[y_ind][x_ind] = i[2]/total_ves

    plot(x,y,num_ves)


if __name__ == "__main__":
    HOME = os.environ['HOME']
    
    # load_paths = []
    # for tn in TEST_LIST_spec:
    #     test_name = tn + '_35_500000_DESKTOP_IdealSensor'
    #     load_path = os.path.join(HOME,'plot/data')
    #     load_path = os.path.join(load_path,test_name+'_lead_time_sweep.npy')
    #     load_paths.append(load_path)
    # run_all(load_paths)

    test_name = 'qsort_lead_time_sweep'
    load_path = os.path.join(HOME,'plot/data')
    load_path = os.path.join(load_path,test_name+'.npy')

    # for tn in TEST_LIST_spec:
    #     run(tn+'_35_500000_DESKTOP_IdealSensor')

    run(load_path)