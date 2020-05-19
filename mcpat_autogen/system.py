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
# system.py
#
# Create a valid system from subcomponents

from xml.etree import ElementTree
from xml.dom import minidom

#from core import Core
from cache import Cache
from noc import NoC
from mc import MemoryController
from niu import NIU
from pcie import PCIE
from flash import FlashController

class System:
  name = "system"
  id = "system"

  #cores = list()
  l3 = None
  #noc = None
  #mem = None
  #niu = None
  #pcie = None
  #flash = None

  # Parameters are a dictionary with the key as the parameter name, and then a
  # value comment pair
  parameters = \
  {
    "number_of_cores" : ["1","The number of cores"],
    "number_of_L1Directories" : ["0","The number of L1 Directories"],
    "number_of_L2Directories" : ["0","The number of L2 Directories"],
    "number_of_L2s" : ["1","The number of L2s in each Cluster"],
    "Private_L2" : ["1","1: Private; 0: shared/coherent"],
    "number_of_L3s" : ["1","Number of L3 Caches"],
    "number_of_NoCs" : ["1","Number of NoCs"],
    "homogeneous_cores" : ["0","1: Homogeneous cores; 0: Heterogeneous core statistics"],
    "homogeneous_L2s" : ["0","1: Homogeneous L2; Heterogeneous L2 statistics"],
    "homogeneous_L1Directories" : ["0","1: Homogeneous L1 Directory; Heterogeneous L1 Directory statistics"],
    "homogeneous_L2Directories" : ["0","1: Homogeneous L2 Directory; Heterogeneous L2 Directory statistics"],
    "homogeneous_L3s" : ["1","1: Homogeneous L3; Heterogeneous L3 statistics"],
    "homogeneous_ccs" : ["1","1: Homogeneous Cache Controller; Heterogeneous Cache Controller statistics"],
    "homogeneous_NoCs" : ["1","1: Homogeneous Network on Chip; Heterogeneous Network on Chip statistics"],
    "core_tech_node" : ["22","Tech Process Node"],
    "target_core_clockrate" : ["1000","Core Clock Rate in MHz"],
    "temperature" : ["298","System Temperature in Kelvin"],
    "number_cache_levels" : ["3",""],
    "interconnect_projection_type" : ["0","0: Aggressive Wire Technology; 1: Conservative Wire Technology"],
    "device_type" : ["0","0: High Performance Type; 1: Low Standby Power; 2: Low Operating Power"],
    "longer_channel_device" : ["1","0: No use; 1: Use when possible"],
    "power_gating" : ["1","0: not enabled; 1: enabled"],
    "machine_bits" : ["64","n-Bit machine"],
    "virtual_address_width" : ["64","n-Bit virtual address"],
    "physical_address_width" : ["52","m-Bit physical address"],
    "virtual_memory_page_size" : ["4096","Virtual memory page size"]
  }

  # Stats are a dictionary with the key as the parameter name, and then a value
  # comment pair
  stats = \
  {
    "total_cycles" : ["1", "Total CPU Cycles"],
    "idle_cycles" : ["1", "Total Idle Cycles"],
    "busy_cycles" : ["0", "Total Busy Cycles (Total - Idle)"]
  }

  def __init__(self, component_id, component_name, stat_dict, config_dict):
    """ In the constructor, the parameters are populated from the config and
    the stats are populated from the stats. The subcomponents are also
    constructed and populated hierarchically """

    # Intialize the Parameters based on the config
    #self.parameters["number_of_cores"][0] =
    #self.parameters["number_of_L1Directories"][0] =
    #self.parameters["number_of_L2Directories"][0] =
    #self.parameters["number_of_L2s"][0] =
    #self.parameters["Private_L2"][0] =
    #self.parameters["number_of_L3s"][0] =
    #self.parameters["number_of_NoCs"][0] =
    #self.parameters["homogeneous_cores"][0] =
    #self.parameters["homogeneous_L2s"][0] =
    #self.parameters["homogeneous_L1Directories"][0] =
    #self.parameters["homogeneous_L2Directories"][0] =
    #self.parameters["homogeneous_L3s"][0] =
    #self.parameters["homogeneous_ccs"][0] =
    #self.parameters["homogeneous_NoCs"][0] =
    #self.parameters["core_tech_node"][0] =
    #self.parameters["target_core_clockrate"][0] =
    #self.parameters["temperature"][0] =
    #self.parameters["number_cache_levels"][0] =
    #self.parameters["device_type"][0] =
    #self.parameters["longer_channel_device"][0] =
    #self.parameters["power_gating"][0] =
    #self.parameters["machine_bits"][0] =
    #self.parameters["virtual_address_width"][0] =
    #self.parameters["physical_address_width"][0] =
    #self.parameters["virtual_memory_page_size"][0] =

    ## Intialize the Parameters based on the stats
    #self.stats["total_cycles"][0] =
    #self.stats["idle_cycles"][0] =
    #self.stats["busy_cycles"][0] =

    # Intialize all the devices
    #self.core = [Core(self.id+".core"+str(i),"core"+str(i), stat_dict, config_dict) for i in range(int(self.parameters["number_of_cores"][0]))]
    self.l3 = [Cache(self.id+".L3"+str(i), "L3"+str(i), stat_dict, config_dict) for i in range(int(self.parameters["number_of_L3s"][0]))]
    #self.noc = [NoC(self.id+".NoC"+str(i), "noc"+str(i), stat_dict, config_dict) for i in range(int(self.parameters["number_of_NoCs"][0]))]
    #self.mc = MemoryController(self.id+".mc", "mc", stat_dict, config_dict)
    #self.niu = NIU(self.id+".niu", "niu", stat_dict, config_dict)
    #self.pcie = PCIE(self.id+".pcie", "pcie", stat_dict, config_dict)
    #self.flash = FlashController(self.id+".flashc", "flashc", stat_dict, config_dict)

  def xml(self):
    """ Build an XML Tree from the parameters, stats, and subcomponents """
    top = ElementTree.Element('component', id=self.id, name=self.name)
    for key in sorted(self.parameters):
      top.append(ElementTree.Comment(", ".join(['param', key, self.parameters[key][1]])))
      top.append(ElementTree.Element('param', name=key, value=self.parameters[key][0]))
    for key in sorted(self.stats):
      top.append(ElementTree.Comment(", ".join(['stat', key, self.stats[key][1]])))
      top.append(ElementTree.Element('stat', name=key, value=self.stats[key][0]))
    #for c in self.core:
    #  top.append(c.xml())
    for c in self.l3:
      top.append(c.xml())
    #top.extend(self.mc.xml())
    #top.extend(self.niu.xml())
    #top.extend(self.pcie.xml())
    #top.extend(self.flash.xml())
    return top

