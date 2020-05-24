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
  def __init__(self, component_id, component_name, stat_dict, config_dict, sim_dict):
    self.name = "cache"
    self.id = "cache"

    self.parameters = \
    {
      "config" : ["0,1,2,3,4,5,6,7","Cache Capacity, Block Width, Associativity, Bank, Throughput w.r.t. core clock, Latency w.r.t. core clock, Output Width, Cache Policy: 0 no write or write-though with non-write allocate; 1 write-back with write-allocate"],
      "buffer_sizes" : ["0,1,2,3","Cache controller buffer sizes: miss_buffer_size(MSHR), fill_buffer_size, prefetch_buffer_size, wb_buffer_size"],
      "clockrate" : ["1000","Clock rate in MHz"],
      "vdd" : ["1.2","Voltage"],
      "power_gating_vcc" : ["-1","-1 means default power gating"],
      "ports" : ["1,1,1","Number of R, W, RW ports"],
      "device_type" : ["0","0: HP, 1: LP"]
    }
    self.stats = \
    {
      "duty_cycle" : ["1.0",""],
      "read_accesses" : ["0", "Cache Read Accesses Total"],
      "read_misses" : ["0", "Cache Read Req Misses Total"],
      "write_accesses" : ["0", "Cache Write Accesses Total"],
      "write_misses" : ["0", "Cache Write Req Misses Total"],
      "conflicts" : ["0", "Cache Replacements"]
    }
    self.name = component_name
    self.id = component_id

    # Init the Cache Parameters and Stats:
    self.parameters["config"][0]=",".join([config_dict["size"],config_dict["tags.block_size"],config_dict["assoc"],"1","1",config_dict["response_latency"],config_dict["tags.block_size"],"0"])
    self.parameters["buffer_sizes"][0]=",".join([config_dict["mshrs"],config_dict["mshrs"],config_dict["mshrs"],config_dict["mshrs"]])
    self.parameters["clockrate"][0]=str((1.0e-6/float(config_dict["clock"]))*1.0e12)
    self.parameters["vdd"][0]=str(float(sim_dict["voltage"]))
    self.stats["read_accesses"][0]=str(int(stat_dict["ReadExReq_accesses::total"][1])+int(stat_dict["ReadCleanReq_accesses::total"][1])+int(stat_dict["ReadSharedReq_accesses::total"][1]))
    self.stats["read_misses"][0]=str(int(stat_dict["ReadCleanReq_misses::total"][1])+int(stat_dict["ReadExReq_misses::total"][1]))
    self.stats["write_accesses"][0]=str(int(stat_dict["WritebackDirty_accesses::total"][1])+int(stat_dict["WritebackClean_accesses::total"][1]))
    self.stats["write_misses"][0]=str(int(stat_dict["WritebackClean_accesses::total"][1])+int(stat_dict["WritebackClean_accesses::total"][1])-int(stat_dict["WritebackDirty_hits::total"][1])-int(stat_dict["WritebackDirty_hits::total"][1]))
    self.stats["conflicts"][0]=str(int(stat_dict["replacements"][1]))

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

class ICache:
  def __init__(self, component_id, component_name, stat_dict, config_dict, sim_dict):
    self.name = "icache"
    self.id = "icache"

    self.parameters = \
    {
      "icache_config" : ["0,1,2,3,4,5,6,7","Cache Capacity, Block Width, Associativity, Bank, Throughput w.r.t. core clock, Latency w.r.t. core clock, Output Width, Cache Policy: 0 no write or write-though with non-write allocate; 1 write-back with write-allocate"],
      "buffer_sizes" : ["0,1,2,3","Cache controller buffer sizes: miss_buffer_size(MSHR), fill_buffer_size, prefetch_buffer_size, wb_buffer_size"]
    }
    self.stats = \
    {
      "read_accesses" : ["0", "Cache Read Accesses Total"],
      "read_misses" : ["0", "Cache Read Req Misses Total"],
      "conflicts" : ["0", "Cache Replacements"]
    }

    self.name = component_name
    self.id = component_id

    # Init the Cache Parameters and Stats:
    self.parameters["icache_config"][0]=",".join([config_dict["size"],config_dict["tags.block_size"],config_dict["assoc"],"1","1",config_dict["response_latency"],config_dict["tags.block_size"],"0"])
    self.parameters["buffer_sizes"][0]=",".join([config_dict["mshrs"],config_dict["mshrs"],config_dict["mshrs"],config_dict["mshrs"]])
    self.stats["read_accesses"][0]=str(int(stat_dict["ReadReq_accesses::total"][1]))
    self.stats["read_misses"][0]=str(int(stat_dict["ReadReq_misses::total"][1]))
    self.stats["conflicts"][0]=str(int(stat_dict["replacements"][1]))

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

class DCache:
  def __init__(self, component_id, component_name, stat_dict, config_dict, sim_dict):
    self.name = "dcache"
    self.id = "dcache"

    self.parameters = \
    {
      "dcache_config" : ["0,1,2,3,4,5,6,7","Cache Capacity, Block Width, Associativity, Bank, Throughput w.r.t. core clock, Latency w.r.t. core clock, Output Width, Cache Policy: 0 no write or write-though with non-write allocate; 1 write-back with write-allocate"],
      "buffer_sizes" : ["0,1,2,3","Cache controller buffer sizes: miss_buffer_size(MSHR), fill_buffer_size, prefetch_buffer_size, wb_buffer_size"]
    }
    self.stats = \
    {
      "read_accesses" : ["0", "Cache Read Accesses Total"],
      "read_misses" : ["0", "Cache Read Req Misses Total"],
      "write_accesses" : ["0", "Cache Write Accesses Total"],
      "write_misses" : ["0", "Cache Write Req Misses Total"],
      "conflicts" : ["0", "Cache Replacements"]
    }

    self.name = component_name
    self.id = component_id

    # Init the Cache Parameters and Stats:
    self.parameters["dcache_config"][0]=",".join([config_dict["size"],config_dict["tags.block_size"],config_dict["assoc"],"1","1",config_dict["response_latency"],config_dict["tags.block_size"],"0"])
    self.parameters["buffer_sizes"][0]=",".join([config_dict["mshrs"],config_dict["mshrs"],config_dict["mshrs"],config_dict["mshrs"]])
    self.stats["read_accesses"][0]=str(int(stat_dict["ReadReq_accesses::total"][1]))
    self.stats["read_misses"][0]=str(int(stat_dict["ReadReq_misses::total"][1]))
    self.stats["write_accesses"][0]=str(int(stat_dict["WriteReq_accesses::total"][1]))
    self.stats["write_misses"][0]=str(int(stat_dict["WriteReq_misses::total"][1]))
    self.stats["conflicts"][0]=str(int(stat_dict["replacements"][1]))

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
