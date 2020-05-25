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
# pcie.py
#
# PCIe class definition

from xml.etree import ElementTree
from xml.dom import minidom

class PCIE:
  """ On chip PCIe controller, including Phy. For a minimum PCIe packet
  size of 84B at 8Gb/s per lane (PCIe 3.0), a new packet arrives every
  84ns. The low bound of clock rate of a PCIe per lane logic is 120Mhz
  Note: McPAT does not track individual pcie controllers, instead, it
  takes the total accesses and calculate the average power per pcie
  controller or per channel. This is sufficent for most application. """

  name = "pcie"
  id = "pcie"

  parameters = \
  {
    "type" : ["0","1: low power; 0 high performance"],
    "withPHY" : ["1",""],
    "clockrate" : ["350","Clock Rate in MHz"],
    "number_units" : ["0",""],
    "num_channels" : ["8","Possible values: 2 ,4 ,8 ,16 ,32"]
  }
  stats = \
  {
    "duty_cycle" : ["1.0","achievable max load <= 1.0"],
    "total_load_perc" : ["0.0","Percentage of total achived load to total achivable bandwidth"]
  }

  def __init__(self, component_id, component_name, stat_dict, config_dict):
    self.name = component_name
    self.id = component_id

    # Init the PCIE Parameters and Stats:
    #parameters["type"][0]=
    #parameters["withPHY"][0]=
    #parameters["clockrate"][0]=
    #parameters["number_units"][0]=
    #parameters["num_channels"][0]=
    #stats["duty_cycle"][0]=
    #stats["total_load_perc"][0]=

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
