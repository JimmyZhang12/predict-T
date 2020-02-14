import sys
import os
import subprocess
import tempfile
import shutil
from contextlib import contextmanager

from m5_to_mcpat import m5_to_mcpat
from gem5 import *
from mcpat import *

from threading import Thread
from Queue import Queue

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

class Benchmark:
  def __init__(self, name, cmd, opt, text_out, gem5_out, mcpat_out):
    self.name = name
    self.cmd = cmd
    self.opt = opt
    self.text_out = text_out
    self.gem5_out = gem5_out
    self.mcpat_out = mcpat_out

#benchmarks = [Benchmark("basicmath", "basicmath_small", "", "text_out/basicmath", "gem5_out/basicmath", "mcpat_out/basicmath"),
#              Benchmark("bitcnts", "bitcnts", "10000", "text_out/bitcnts", "gem5_out/bitcnts", "mcpat_out/bitcnts"),
#              Benchmark("qsort_small", "qsort_small", "input/qsort_small.dat", "text_out/qsort_small", "gem5_out/qsort_small", "mcpat_out/qsort_small"),
#              Benchmark("qsort_large", "qsort_large", "input/qsort_large.dat", "text_out/qsort_large", "gem5_out/qsort_large", "mcpat_out/qsort_large"),
#              Benchmark("susan_small_s", "susan", "input/susan_small.pgm output/susan_small_s.pgm -s", "text_out/susan_small_s", "gem5_out/susan_small_s", "mcpat_out/susan_small_s"),
#              Benchmark("susan_small_e", "susan", "input/susan_small.pgm output/susan_small_e.pgm -e", "text_out/susan_small_e", "gem5_out/susan_small_e", "mcpat_out/susan_small_e"),
#              Benchmark("susan_small_c", "susan", "input/susan_small.pgm output/susan_small_c.pgm -c", "text_out/susan_small_c", "gem5_out/susan_small_c", "mcpat_out/susan_small_c"),
#              Benchmark("susan_large_s", "susan", "input/susan_large.pgm output/susan_large_s.pgm -s", "text_out/susan_large_s", "gem5_out/susan_large_s", "mcpat_out/susan_large_s"),
#              Benchmark("susan_large_e", "susan", "input/susan_large.pgm output/susan_large_e.pgm -e", "text_out/susan_large_e", "gem5_out/susan_large_e", "mcpat_out/susan_large_e"),
#              Benchmark("susan_large_c", "susan", "input/susan_large.pgm output/susan_large_c.pgm -c", "text_out/susan_large_c", "gem5_out/susan_large_c", "mcpat_out/susan_large_c"),
#              Benchmark("dijkstra_small", "dijkstra_small", "input/dijkstra.dat", "text_out/dijkstra_small", "gem5_out/dijkstra_small", "mcpat_out/dijkstra_small"),
#              Benchmark("dijkstra_large", "dijkstra_large", "input/dijkstra.dat", "text_out/dijkstra_large", "gem5_out/dijkstra_large", "mcpat_out/dijkstra_large"),
#              Benchmark("patricia_small", "patricia", "input/patricia_small.udp", "text_out/patricia_small", "gem5_out/patricia_small", "mcpat_out/patricia_small"),
#              Benchmark("blowfish_e", "blowfish", "e input/blowfish_small.asc output/blowfish_small.enc 1234567890abcdeffedcba0987654321", "text_out/blowfish_e", "gem5_out/blowfish_e", "mcpat_out/blowfish_e"),
#              Benchmark("blowfish_d", "blowfish", "d input/blowfish_small.enc output/blowfish_small.asc 1234567890abcdeffedcba0987654321", "text_out/blowfish_d", "gem5_out/blowfish_d", "mcpat_out/blowfish_d"),
#              Benchmark("rijndael_e", "rijndael", "input/rijndael_small.asc output/rijndael_small.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321", "text_out/rijndael_e", "gem5_out/rijndael_e", "mcpat_out/rijndael_e"),
#              Benchmark("rijndael_d", "rijndael", "input/rijndael_small.enc output/rijndael_small.asc d 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321", "text_out/rijndael_d", "gem5_out/rijndael_d", "mcpat_out/rijndael_d"),
#              Benchmark("sha", "sha", "input/sha_small.asc", "text_out/sha", "gem5_out/sha", "mcpat_out/sha"),
#              Benchmark("crc", "crc", "input/crc_small.pcm", "text_out/crc", "gem5_out/crc", "mcpat_out/crc"),
#              Benchmark("fft", "fft", "4 4096", "text_out/fft", "gem5_out/fft", "mcpat_out/fft"),
#              Benchmark("fft_i", "fft", "4 8192 -i", "text_out/fft_i", "gem5_out/fft_i", "mcpat_out/fft_i"),
#              Benchmark("toast", "toast", "-fps -c input/toast_small.au", "text_out/toast", "gem5_out/toast", "mcpat_out/toast"),
#              Benchmark("untoast", "untoast", "-fps -c input/untoast_small.gsm", "text_out/untoast", "gem5_out/untoast", "mcpat_out/untoast")]
benchmarks = [Benchmark("untoast", "untoast", "-fps -c input/toast_small.gsm", "text_out/untoast", "gem5_out/untoast", "mcpat_out/untoast")]
#benchmarks = [Benchmark("susan_large_s", "susan", "input/susan_large.pgm output/susan_large_s.pgm -s", "text_out/susan_large_s", "gem5_out/susan_large_s", "mcpat_out/susan_large_s"),
#              Benchmark("susan_large_e", "susan", "input/susan_large.pgm output/susan_large_e.pgm -e", "text_out/susan_large_e", "gem5_out/susan_large_e", "mcpat_out/susan_large_e"),
#              Benchmark("susan_large_c", "susan", "input/susan_large.pgm output/susan_large_c.pgm -c", "text_out/susan_large_c", "gem5_out/susan_large_c", "mcpat_out/susan_large_c"),
#              Benchmark("dijkstra_small", "dijkstra_small", "input/dijkstra.dat", "text_out/dijkstra_small", "gem5_out/dijkstra_small", "mcpat_out/dijkstra_small"),
#              Benchmark("dijkstra_large", "dijkstra_large", "input/dijkstra.dat", "text_out/dijkstra_large", "gem5_out/dijkstra_large", "mcpat_out/dijkstra_large"),
#              Benchmark("patricia_small", "patricia", "input/patricia_small.udp", "text_out/patricia_small", "gem5_out/patricia_small", "mcpat_out/patricia_small")]

def run(args):
  def m5_benchmark_thread(iq):
    while not iq.empty():
      test = iq.get()
      run_gem5(test.cmd,test.opt,test.text_out,test.gem5_out,"1","DerivO3CPU","16kB","64kB","256kB")

  # First run Gem5 for each benchmark:
  for test in benchmarks:
    run_gem5(test.cmd,test.opt,test.text_out,test.gem5_out,"1","DerivO3CPU","16kB","64kB","256kB")

  #input = Queue()
  #threads = []

  #for test in benchmarks:
  #  input.put(test)

  #for i in range(16):
  #  thr = Thread(target=m5_benchmark_thread, args=[input])
  #  thr.start()
  #  threads.append(thr)

  #for thr in threads:
  #  thr.join()

  # Convert Output to McPat:
  #for test in benchmarks:
  #  m5_to_mcpat(get_stats_file(test.gem5_out), get_config_file(test.gem5_out), "mcpat-template.xml", test.mcpat_out, test.name)

  # Run McPat:

run(args)
