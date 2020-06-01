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
# __init__.py
# 
# Main python script for dynamically creating McPAT XML Files

from xml.etree import ElementTree
from xml.dom import minidom

from system import System
from util import *

def generate_xml(stat_file, config_file, out_file, **kwargs):
  def prettify(elem):
    """Return a pretty-printed XML string for the
    Element.  """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

  # Parse & build the context dictionaries:
  stat_dict = build_gem5_stat_dict(stat_file)
  config_dict = build_gem5_config_dict(config_file)
  sim_dict = build_gem5_sim_dict(**kwargs)

  # Build the system
  s = System("system", "system", stat_dict, config_dict, sim_dict)

  root = ElementTree.Element('component', id='root', name='root')
  root.append(s.xml())

  # write the XML
  with open(out_file, "w") as of:
    of.write(prettify(root))

  return 0

