import os
import sys
import re
import subprocess
import tempfile
from contextlib import contextmanager

# Gem5 Global Paths:
gem5_path = "../gem5"
gem5_exe_arm = os.path.join(gem5_path, "build/ARM/gem5.opt")
gem5_exe_x86 = os.path.join(gem5_path, "build/X86/gem5.opt")
gem5_cfg = os.path.join(gem5_path, "configs/example/se.py")
test_path = "testbin"

def get_stats_file(gem5_out):
  return os.path.join(gem5_out, "stats.txt")

def get_config_file(gem5_out):
  return os.path.join(gem5_out, "config.ini")

def run_gem5(cmd, opts, outname, outdir, cpu_type, mcpat_template, mcpat_path, mcpat_out, mcpat_testname, ps):
  global gem5_path
  global gem5_exe
  global gem5_cfg
  global gem5_out
  if cpu_type == "ARM":
    gem5 = [gem5_exe_arm,
      "--outdir="+os.path.join(".", outdir),
      "--mcpat_template="+mcpat_template,
      "--mcpat_path="+mcpat_path,
      "--mcpat_out="+mcpat_out,
      "--mcpat_testname="+mcpat_testname,
      "--power_profile_start=400000000",
      "--power_profile_duration=2000",
      "--power_profile_interval=1000",
      gem5_cfg,
      "--cmd="+os.path.join(test_path, cmd),
      "--options="+opts,
      "--power_profile_interval=1000",
      "--num-cpus=1",
      "--cpu-type=DerivO3CPU",
      "--l1i_size=16kB",
      "--l1d_size=64kB",
      "--l2cache",
      "--l2_size=256kB",
      "--caches",
      "--mem-size=8GB"]
  if cpu_type == "XeonE7-8893":
    gem5 = [gem5_exe_x86,
      "--outdir="+os.path.join(".", outdir),
      "--mcpat_template="+mcpat_template,
      "--mcpat_path="+mcpat_path,
      "--mcpat_out="+mcpat_out,
      "--mcpat_testname="+mcpat_testname,
      "--power_profile_start=4000000",
      "--power_profile_duration=1000",
      "--power_profile_interval=500",
      "--ncverilog_path="+ps,
      gem5_cfg,
      "--cmd="+os.path.join(test_path, cmd),
      "--options="+opts,
      "--power_profile_interval=500",
      "--num-cpus=1",
      "--cpu-type=DerivO3CPU",
      "--l1i_size=16kB",
      "--l1i-hwp-type=TaggedPrefetcher",
      "--l1d_size=64kB",
      "--l1d-hwp-type=TaggedPrefetcher",
      "--l2cache",
      "--num-l2caches=1",
      "--l2_size=256kB",
      "--l2-hwp-type=TaggedPrefetcher",
      "--l3cache",
      "--l3_size=32MB",
      "--l3-hwp-type=TaggedPrefetcher",
      "--caches",
      "--sys-clock=2GHz",
      "--mem-size=8GB"]
  if cpu_type == "Simple":
    gem5 = [gem5_exe_x86,
      "--outdir="+os.path.join(".", outdir),
      "--mcpat_disable",
      gem5_cfg,
      "--cmd="+os.path.join(test_path, cmd),
      "--options="+opts,
      "--num-cpus=1",
      "--cpu-type=AtomicSimpleCPU",
      "--l1i_size=16kB",
      "--l1d_size=64kB",
      "--l2cache",
      "--l2_size=256kB",
      "--caches",
      "--mem-size=8GB"]
  print(" ".join(gem5))
  with open(os.path.join(".", outname+".out"), "w") as ostd, \
       open(os.path.join(".", outname+".err"), "w") as oerr:
    p = subprocess.Popen(gem5, stdout=ostd, stderr=oerr)
    p.wait()
  #out, err = p.communicate()
  #print(out)

# --list-hwp-types: TaggedPrefetcher, BOPPrefetcher, StridePrefetcher ...
# --list-bp-types: localbp, BiModeBP, TAGE, LTAGE, MultiperspectivePerceptron....
#"--power_profile_start=400000000",

#Test Code:
#print(get_stats_file("fft_small"))
#print(get_config_file("fft_small"))
#run_gem5("fft", "4 4096", "fft_small", "1", "DerivO3CPU", "16kB", "64kB", "256kB")
#../gem5/build/ARM/gem5.opt --outdir=./output/fft_small ../gem5/configs/example/se.py --cmd=tests/testbin/fft --options='4 4096' --num-cpus=1 --cpu-type=DerivO3CPU --l1i_size=16kB --l1d_size=64kB --l2cache --l2_size=256kB --cach
