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
test_path = "testbin"

def get_stats_file(gem5_out):
  return os.path.join(gem5_out, "stats.txt")

def get_config_file(gem5_out):
  return os.path.join(gem5_out, "config.ini")

def run_gem5(cmd, opts, outname, outdir, num_cpus, cpu_type, l1i_size, l1d_size, l2_size, mcpat_template, mcpat_path, mcpat_out, mcpat_testname):
  global gem5_path
  global gem5_exe
  global gem5_cfg
  global gem5_out
  gem5 = [gem5_exe,
    "--outdir="+os.path.join(".", outdir),
    "--mcpat_template="+mcpat_template,
    "--mcpat_path="+mcpat_path,
    "--mcpat_out="+mcpat_out,
    "--mcpat_testname="+mcpat_testname,
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
  with open(os.path.join(".", outname+".out"), "w") as ostd, \
       open(os.path.join(".", outname+".err"), "w") as oerr:
    p = subprocess.Popen(gem5, stdout=ostd, stderr=oerr)
    p.wait()
  #out, err = p.communicate()
  #print(out)

#Test Code:
#print(get_stats_file("fft_small"))
#print(get_config_file("fft_small"))
#run_gem5("fft", "4 4096", "fft_small", "1", "DerivO3CPU", "16kB", "64kB", "256kB")
#../gem5/build/ARM/gem5.opt --outdir=./output/fft_small ../gem5/configs/example/se.py --cmd=tests/testbin/fft --options='4 4096' --num-cpus=1 --cpu-type=DerivO3CPU --l1i_size=16kB --l1d_size=64kB --l2cache --l2_size=256kB --cach
