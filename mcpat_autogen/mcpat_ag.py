# MIT License
# 
# Copyright (c) 2020 Andrew Smith
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# mcpat_ag.py
# 
# Main python script for dynamically creating McPAT XML Files

from xml.etree import ElementTree
from xml.dom import minidom

from system import System
from util import *

def prettify(elem):
  """Return a pretty-printed XML string for the
  Element.  """
  rough_string = ElementTree.tostring(elem, 'utf-8')
  reparsed = minidom.parseString(rough_string)
  return reparsed.toprettyxml(indent="  ")


def testbench():
  """ Testbench code """
  #stat_file = "/scratch/atsmith3/predict-T/gem5_out/bitcnts_256_10_1000000_SimplePredictorEnableBuck1MHz/stats.txt"
  stat_file = "/scratch/atsmith3/predict-T/gem5_out/basicmath_256_10_1000000_mcSimplePredictorEnableBuck1MHz/stats.txt"
  #config_file = "/scratch/atsmith3/predict-T/gem5_out/bitcnts_256_10_1000000_SimplePredictorEnableBuck1MHz/config.ini"
  config_file = "/scratch/atsmith3/predict-T/gem5_out/basicmath_256_10_1000000_mcSimplePredictorEnableBuck1MHz/config.ini"

  # Parse & build the context dictionaries:
  stat_dict = build_gem5_stat_dict(stat_file)
  config_dict = build_gem5_config_dict(config_file)
  sim_dict = build_gem5_sim_dict(voltage="1.2", temperature="300")

  # Build the system
  s = System("system", "system", stat_dict, config_dict, sim_dict)

  root = ElementTree.Element('component', id='root', name='root')
  root.append(s.xml())

  # Print the XML
  print(prettify(root))
  return 0

if __name__ == "__main__":
  testbench()
