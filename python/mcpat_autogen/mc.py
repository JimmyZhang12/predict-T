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
# mc.py
#
# Memory Controller class definition

from xml.etree import ElementTree
from xml.dom import minidom

class MemoryController:
  """ Memory controllers are for DDR(2,3...) DIMMs
  current version of McPAT uses published values for
  base parameters of memory controller improvements on
  MC will be added in later versions. """

  """ Current McPAT version only supports homogeneous
  memory controllers """

  """McPAT will add the control bus width to the
  address bus width automatically. McPAT does not track
  individual mc, instead, it takes the total accesses
  and calculate the average power per MC or per
  channel. This is sufficient for most application.
  Further track down can be easily added in later
  versions."""
  def __init__(self, component_id, component_name, stat_dict, config_dict, sim_dict):
    self.name = "mc"
    self.id = "mc"

    self.parameters = \
    {
      "type" : ["0","1: low power; 0 high performance"],
      "mc_clock" : ["2666","DIMM IO bus clock rate MHz"],
      "vdd" : ["0","0 means using ITRS default vdd"],
      "power_gating_vcc" : ["-1","\"-1\" means using default power gating virtual power supply voltage constrained by technology and computed automatically"],
      "peak_transfer_rate" : ["20000","MB/S"],
      "block_size" : ["64","B"],
      "number_mcs" : ["4",""],
      "memory_channels_per_mc" : ["1",""],
      "number_ranks" : ["2",""],
      "withPHY" : ["0",""],
      "req_window_size_per_channel" : ["32",""],
      "IO_buffer_size_per_channel" : ["32",""],
      "databus_width" : ["128",""],
      "addressbus_width" : ["52",""]
    }
    self.stats = \
    {
      "memory_accesses" : ["0","mem_ctrls.writeReqs + mem_ctrls.readReqs"],
      "memory_reads" : ["0","mem_ctrls.readReqs"],
      "memory_writes" : ["0","mem_ctrls.writeReqs"]
    }

    self.name = component_name
    self.id = component_id

    # Init the Memory Controller Parameters and Stats:
    self.parameters["type"][0]="0"
    self.parameters["mc_clock"][0]=str(int(config_dict["tCK"])*2)
    self.parameters["vdd"][0]=str(float(config_dict["VDD"]))
    self.parameters["power_gating_vcc"][0]="-1"
    self.parameters["peak_transfer_rate"][0]=str(int(stat_dict["bw_total::total"][1])/1e6)
    self.parameters["block_size"][0]="64"
    self.parameters["number_mcs"][0]="4"
    self.parameters["memory_channels_per_mc"][0]="2"
    self.parameters["number_ranks"][0]="2"
    self.parameters["withPHY"][0]="0"
    self.parameters["req_window_size_per_channel"][0]="32"
    self.parameters["IO_buffer_size_per_channel"][0]="64"
    self.parameters["databus_width"][0]="128"
    self.parameters["addressbus_width"][0]="52"
    self.stats["memory_accesses"][0]=str(int(stat_dict["readReqs"][1])+int(stat_dict["writeReqs"][1]))
    self.stats["memory_reads"][0]=str(int(stat_dict["readReqs"][1]))
    self.stats["memory_writes"][0]=str(int(stat_dict["writeReqs"][1]))

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

