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
# tlb.py
#
# Translation Lookaside Buffer class definition

from xml.etree import ElementTree
from xml.dom import minidom

class TLB:
  def __init__(self, component_id, component_name, stat_dict, config_dict, sim_dict):
    self.name = "tlb"
    self.id = "tlb"

    self.parameters = \
    {
      "number_entries" : ["64","TLB Size; tlb.size"],
    }
    self.stats = \
    {
      "total_accesses" : ["","Total Acceses; dtb_walker_cache.tags.data_accesses"],
      "total_misses" : ["","Total Misses; dtb_walker_cache.tags.data_accesses"],
      "conflicts" : ["0","Conflicts to entries in the TLB"],
    }

    self.name = component_name
    self.id = component_id

    # Init the TLB Parameters and Stats:
    self.parameters["number_entries"][0]=str(int(config_dict["size"]))
    self.stats["total_accesses"][0]=str(int(stat_dict["tags.tag_accesses"][1]))
    self.stats["total_misses"][0]=str(int(stat_dict["replacements"][1]))
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

