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

if __name__ == "__main__":

    PREDICTOR = 'HarvardPowerPredictor_1'
    CLASS = 'DESKTOP'
    OUTPUT_DIR = 'output_2_7'
    DATE = '2-23'
    INSTRUCTIONS = '1000'
    TEST = 'crc'    
    PDN = 'INTEL_DT'
    calc_plot_stats(PREDICTOR,CLASS,TEST,OUTPUT_DIR,DATE,INSTRUCTIONS,PDN)

