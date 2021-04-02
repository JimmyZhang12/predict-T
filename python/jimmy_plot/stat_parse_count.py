import os
import util 

def calc_plot_stats(PREDICTOR, CLASS, TEST, OUTPUT_DIR, DATE, INSTRUCTIONS, PDN):
    HOME = os.environ['HOME']
    test_name = TEST + '_' + INSTRUCTIONS + '_' + '1' + '_' + CLASS + '_' + PDN + '_' + PREDICTOR
    path = HOME + '/' + OUTPUT_DIR + '/gem5_out/' + test_name + '/stats.txt'
    print(path)
    stats = open(path, 'r')

    cycle_dump = util.Cycle_Dump(stats)
    while (cycle_dump.parseCycle()):
        cycle_dump.dump()
        input() 

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

if __name__ == "__main__":



    PREDICTOR = 'HarvardPowerPredictor_1'
    CLASS = 'DESKTOP'
    OUTPUT_DIR = 'output_2_7'
    DATE = '2-23'
    INSTRUCTIONS = '1000'
    TEST = 'crc'    
    PDN = 'INTEL_DT'
    calc_plot_stats(PREDICTOR,CLASS,TEST,OUTPUT_DIR,DATE,INSTRUCTIONS,PDN)

