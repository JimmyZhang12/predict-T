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

from tlb import TLB
from btb import BTB
from cache import Cache
from branchpred import Predictor

class Core:
  name = "core"
  id = "core"

  parameters = \
  {
  }
  stats = \
  {
  }

  predictor = None
  itlb = None
  icache = None
  dtlb = None
  dcache = None
  btb = None


  def __init__(self, component_id, component_name, stat_dict, config_dict):
    self.name = component_name
    self.id = component_id

    # Init the Directory Parameters and Stats:

    self.predictor = Predictor(self.id+".predictor","PBT",stat_dict,config_dict)
    self.itlb = TLB(self.id+".itlb","itlb",stat_dict,config_dict)
    self.icache = Cache(self.id+".icache","icache",stat_dict,config_dict)
    self.dtlb = TLB(self.id+".dtlb","dtlb",stat_dict,config_dict)
    self.dcache = Cache(self.id+".dcache","dcache",stat_dict,config_dict)
    self.btb = BTB(self.id+".BTB","BTB",stat_dict,config_dict)

  def xml(self):
    """ Build an XML Tree from the parameters, stats, and subcomponents """
    top = ElementTree.Element('component', id=self.id, name=self.name)
    for key in sorted(self.parameters):
      top.append(ElementTree.Comment(", ".join(['param', key, self.parameters[key][1]])))
      top.append(ElementTree.Element('param', name=key, value=self.parameters[key][0]))
    for key in sorted(self.stats):
      top.append(ElementTree.Comment(", ".join(['stat', key, self.stats[key][1]])))
      top.append(ElementTree.Element('stat', name=key, value=self.stats[key][0]))
    top.append(self.predictor.xml())
    top.append(self.itlb.xml())
    top.append(self.icache.xml())
    top.append(self.dtlb.xml())
    top.append(self.dcache.xml())
    top.append(self.btb.xml())
    return top

