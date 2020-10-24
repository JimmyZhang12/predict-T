import pandas as pd
import glob
import numpy as np
import math
import sys
import re
import matplotlib.pyplot as plt
import argparse


def get_files(path):
  files = glob.glob(path+"/*")
  files = [i for i in files]
  files.sort()
  return files

files = get_files("/home/kanungo3/output/gem5_out")

files_list = []
type_list = []
out_list = []
for f in files:
    if "DecorOnly_1" in f:
        files_list.append(f)
        type_list.append(f.split("_1_")[-1])
        if "DESKTOP" in f:
            out_list.append("Desktop")
        if "LAPTOP" in f:
            out_list.append("Laptop")
        if "MOBILE" in f:
            out_list.append("Mobile")

print(files_list,"\n")

print(type_list,"\n")

print(out_list,"\n")
