import sys
import os
import subprocess
import tempfile
import shutil
from contextlib import contextmanager

from m5_to_mcpat import m5_to_mcpat
from gem5 import *
from mcpat import *

import argparse

# Create Unique Temp Directory
# gem5 and mcpat will interface through this directory
#   The directory will delete after 
#
#@contextmanager
#def mcpat_io():
#  tempdir = tempfile.mkdtemp()
#  io_files = {}
#  io_files["mcpat_dir"] = os.path.join(tempdir,"mcpat")
#  os.mkdir(io_files["mcpat_dir"])
#  io_files["gem5_dir"] = os.path.join(tempdir,"gem5")
#  os.mkdir(io_files["gem5_dir"])
#  try:
#    yield io_files
#  finally:
#    shutil.rmtree(tempdir)

parser = argparse.ArgumentParser()
parser.add_argument('--cmd', type=str, default="basicmath_small", help="executable in testbin")
parser.add_argument('--opt', type=str, default="", help="options")
parser.add_argument('--template_xml', type=str, default="tempalte.xml", help="path to template xml for McPAT input")
args = parser.parse_args()


def run(args):
  # First run Gem5:
  run_gem5("fft", "4 4096", "fft_small", "1", "DerivO3CPU", "16kB", "64kB", "256kB")

  # Convert Output to McPat:
  m5_to_mcpat(get_stats_file("fft_small"), get_config_file("fft_small"), "mcpat-template.xml", "mcpat_arm.xml")

  # Run McPat:
  run_mcpat("mcpat_arm.xml", "5", "1", "mcpat.out", "mcpat.err")


  # Convert output:

  #run_gem5("fft", "4 4096", "fft_small", "1", "DerivO3CPU", "16kB", "64kB", "256kB")

run(args)
