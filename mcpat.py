import os
import sys
import re
import subprocess
import tempfile
from contextlib import contextmanager

# McPat Global Paths:
mcpat_path = "mcpat"
mcpat_exe = mcpat_path+"/mcpat"

def run_mcpat(xml, print_level, opt_for_clk, ofile, errfile):
  global mcpat_path
  global mcpat_exe
  mcpat = [mcpat_exe,
    "-infile",
    xml,
    "-print_level",
    print_level,
    "-opt_for_clk",
    opt_for_clk]
  print(" ".join(mcpat))
  with open(ofile, "w") as ostd, open(errfile, "w") as oerr:
    p = subprocess.Popen(mcpat, stdout=ostd, stderr=oerr)
    p.wait()

#Test Code:
#run_mcpat("mcpat_arm.xml", "2", "1", "mcpat.out", "mcpat.err")
