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
# directory.py
#
# Directory Controller class definition

from xml.etree import ElementTree
from xml.dom import minidom

class Directory:
  """ Altough there are multiple access types,
  Performance simulator needs to cast them into reads
  or writes e.g. the invalidates can be considered as
  writes """

  name = "directory"
  id = "directory"

  parameters = \
  {
    "Directory_type" : ["0",""],
    "Dir_config" : ["512,4,0,1,1, 1","cam based shadowed tag. 1 directory cache"],
    "buffer_sizes" : ["16, 16, 16, 16","the parameters are capacity,block_width, associativity,bank, throughput w.r.t. core clock, latency w.r.t. core clock, all the buffer related are optional"],
    "clockrate" : ["1000","Clock rate in MHz"],
    "ports" : ["1,1,1","number of r, w, and rw search ports"],
    "device_type" : ["0",""]
  }
  stats = \
  {
    "read_accesses" : ["0","Read Accesses to the directory controller"],
    "write_accesses" : ["0","Write Accesses to the directory controller"],
    "read_misses" : ["0","Read Misses"],
    "write_misses" : ["0","Write Misses"],
    "conflicts" : ["0","Conflicts"]
  }

  def __init__(self, component_id, component_name, stat_dict, config_dict):
    self.name = component_name
    self.id = component_id

    # Init the Directory Parameters and Stats:
    #parameters["Directory_type"][0]=
    #parameters["Dir_config"][0]=
    #parameters["buffer_sizes"][0]=
    #parameters["clockrate"][0]=
    #parameters["ports"][0]=
    #parameters["device_type"][0]=
    #stats["read_accesses"][0]=
    #stats["write_accesses"][0]=
    #stats["read_misses"][0]=
    #stats["write_misses"][0]=
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


