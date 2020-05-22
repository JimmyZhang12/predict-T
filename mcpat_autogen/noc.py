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
# noc.py
#
# NoC class definition

from xml.etree import ElementTree
from xml.dom import minidom
from util import *

class NoC:
  def __init__(self, component_id, component_name, stat_dict, config_dict, sim_dict, **kwargs):
    self.name = "noc"
    self.id = "noc"

    self.parameters = \
    {
      "clockrate" : ["1000","Clock rate in MHz"],
      "vdd" : ["0","0 means using ITRS default vdd"],
      "power_gating_vcc" : ["-1","\"-1\" means using default power gating virtual power supply voltage constrained by technology and computed automatically"],
      "type" : ["1","0:bus, 1:NoC , for bus no matter how many nodes sharing the bus at each time only one node can send req"],
      "horizontal_nodes" : ["1","Vertical Nodes in NoC; Comes from chip layout"],
      "vertical_nodes" : ["1","Horizontal Nodes in NoC; Comes from chip layout"],
      "has_global_link" : ["0","1 has global link, 0 does not have global link"],
      "link_throughput" : ["1","Link throughput w.r.t clock"],
      "link_latency" : ["1","Link latency w.r.t clock"],
      "input_ports" : ["1",""],
      "output_ports" : ["1","For bus the I/O ports should be 1"],
      "flit_bits" : ["256",""],
      "chip_coverage" : ["1","When multiple NOC present, one NOC will cover part of the whole chip.  chip_coverage <=1"],
      "link_routing_over_percentage" : ["0.5","Links can route over other components or occupy whole area.  by default, 50% of the NoC global links routes over other components"]
    }
    self.stats = \
    {
      "total_accesses" : ["1","This is the number of total accesses within the whole network not for each router (pkt_count::total & bus in key)"],
      "duty_cycle" : ["1",""]
    }
    self.name = component_name
    self.id = component_id

    x,y = get_noc_dimensions(kwargs["num_cores"])

    # Init the NoC Parameters and Stats:
    self.parameters["clockrate"][0]=str((1.0e-6/float(config_dict["system.clk_domain.clock"]))*1.0e12)
    self.parameters["vdd"][0]=str(float(sim_dict["voltage"]))
    self.parameters["power_gating_vcc"][0]="-1"
    self.parameters["type"][0]="1"
    self.parameters["horizontal_nodes"][0]=str(x)
    self.parameters["vertical_nodes"][0]=str(y)
    self.parameters["has_global_link"][0]=str(0)
    self.parameters["link_throughput"][0]=str(1)
    self.parameters["link_latency"][0]=str(1)
    self.parameters["input_ports"][0]=str(2)
    self.parameters["output_ports"][0]=str(2)
    self.parameters["flit_bits"][0]=str(256)
    self.parameters["chip_coverage"][0]=str(1.0)
    self.parameters["link_routing_over_percentage"][0]=str(0.5)

    # Calculate the sum of all the packet counts:
    s = 0
    for key in stat_dict:
      if "pkt_count::total" in key and "bus" in key:
        s += int(stat_dict[key][1])

    self.stats["total_accesses"][0]=str(s)
    self.stats["duty_cycle"][0]=str(1.0)

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

