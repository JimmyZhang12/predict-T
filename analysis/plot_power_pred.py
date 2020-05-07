import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from file_read_backwards import FileReadBackwards
import argparse
import re

def parse_stats(stat_file):
  epoch = []
  stats = {}
  with FileReadBackwards(stat_file, encoding="utf-8") as sf:
    for line in sf:
      if line.strip() == "":
        continue
      elif "End Simulation Statistics" in line:
        stats = {}
      elif "Begin Simulation Statistics" in line:
        epoch.append(stats)
      else:
        stat = []
        sstr = re.sub('\s+', ' ', line).strip()
        if('-----' in sstr):
          continue
        elif(sstr == ''):
          continue
        elif(sstr.split(' ')[1] == '|'):
          # Ruby Stats
          l = []
          for i in sstr.split('|')[1:]:
            l.append(i.strip().split(' '))
          stat.append("ruby_multi")
          stat.append(l)
        else:
          stat.append("single")
          stat.append(sstr.split(' ')[1])
        stats["stats."+sstr.split(' ')[0]] = stat
  print("Read "+str(len(epoch))+" Epochs")
  return epoch

parser = argparse.ArgumentParser()
parser.add_argument('--inputs', type=str, default="", help="comma separated input files")
parser.add_argument('--stat', type=str, default="error", help="Stat to plot")
parser.add_argument('--title', type=str, default="", help="name of the plot")
args = parser.parse_args()

stat_files = args.inputs.split(",")
#print([",".join(i.split("_")[1:3]+[i.split("_")[4]]) for i in stat_files])
#names = [",".join(i.split("_")[1:3]+[i.split("_")[4]]) for i in stat_files]
print([",".join(i.split("_")[1:3]) for i in stat_files])
names = [",".join(i.split("_")[1:3]) for i in stat_files]
stats = []
for i in range(len(stat_files)):
    epoch = parse_stats(stat_files[i])
    temp = []
    for e in epoch:
        temp.append(int(e[args.stat][1]))
    stats.append(temp[::-1])

print(stats)
max_len = 0
for i in range(len(stats)):
    max_len = max(len(stats[i]), max_len)

epoch = range(max_len)
for i in range(len(stats)):
    plt.plot(epoch, stats[i], linewidth=1, label=names[i])
plt.ylabel("Error")
plt.xlabel("Time (us)")
plt.legend(loc='right')
plt.title(args.title)
plt.show()
