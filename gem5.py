import os
import sys
import re
import subprocess
import tempfile
from contextlib import contextmanager

# Gem5 Global Paths:
gem5_path = "../gem5"
gem5_exe = os.path.join(gem5_path, "build/ARM/gem5.opt")
gem5_cfg = os.path.join(gem5_path, "configs/example/se.py")
gem5_out = os.path.join(".", "output")
test_path = "tests/testbin"

def get_stats_file(name):
  return os.path.join(gem5_out, os.path.join(name, "stats.txt"))

def get_config_file(name):
  return os.path.join(gem5_out, os.path.join(name, "config.ini"))

def run_gem5(cmd, opts, output_name, num_cpus, cpu_type, l1i_size, l1d_size, l2_size):
  global gem5_path
  global gem5_exe
  global gem5_cfg
  global gem5_out
  gem5 = [gem5_exe,
    "--outdir="+os.path.join(gem5_out, output_name),
    gem5_cfg,
    "--cmd="+os.path.join(test_path, cmd),
    "--options="+opts,
    "--num-cpus="+num_cpus,
    "--cpu-type="+cpu_type,
    "--l1i_size="+l1i_size,
    "--l1d_size="+l1d_size,
    "--l2cache",
    "--l2_size="+l2_size,
    "--caches"]
  print(" ".join(gem5))
  with open(os.path.join(test_path, "output/"+output_name+".out"), "w") as ostd, \
       open(os.path.join(test_path, "output/"+output_name+".err"), "w") as oerr:
    p = subprocess.Popen(gem5, stdout=ostd, stderr=oerr)
    p.wait()
  #out, err = p.communicate()
  #print(out)

#Test Code:
#print(get_stats_file("fft_small"))
#print(get_config_file("fft_small"))
run_gem5("fft", "4 4096", "fft_small", "1", "DerivO3CPU", "16kB", "64kB", "256kB")
