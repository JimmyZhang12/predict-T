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
# cache.py
#
# Create and populate a cache class

from xml.etree import ElementTree
from xml.dom import minidom

class Cache:
  name = "cache"
  id = "cache"
  LLC = False

  parameters = \
  {
    "icache_config" : ["0,1,2,3,4,5,6,7", "Cache Capacity, Block Width, Associativity, Bank, Throughput w.r.t. core clock, Latency w.r.t. core clock, Output Width, Cache Policy: 0 no write or write-though with non-write allocate; 1 write-back with write-allocate"],
    "buffer_sizes" : ["0,1,2,3", "Cache controller buffer sizes: miss_buffer_size(MSHR), fill_buffer_size, prefetch_buffer_size, wb_buffer_size"]
  }
  stats = \
  {
    "read_accesses" : ["1", "Cache Read Accesses Total"],
    "read_misses" : ["1", "Cache Read Req Misses Total"],
    "conflicts" : ["1", "Cache Replacements"]
  }

  def __init__(self, component_id, component_name, stat_dict, config_dict):
    self.name = component_name
    self.id = component_id

    # Init the Cache Parameters and Stats:
    #parameters["icache_config"][0]=
    #parameters["buffer_sizes"][0]=
    #stats["read_accesses"][0]=
    #stats["read_misses"][0]=
    #stats["conflicts"][0]=

  def xml(self):
    """ Build an XML Tree from the parameters, stats, and subcomponents """
    top = ElementTree.Element('component', id=self.id, name=self.name)
    for key in sorted(self.parameters):
      top.append(ElementTree.Comment(", ".join(['param', key, self.parameters[key][1]])))
      top.append(ElementTree.Element('param', name=key, value=self.parameters[key][0]))
    for key in sorted(self.stats):
      top.append(ElementTree.Comment(", ".join(['stat', key, self.stats[key][1]])))
      top.append(ElementTree.Element('stat', name=key, value=self.stats[key][0]))
    return top
