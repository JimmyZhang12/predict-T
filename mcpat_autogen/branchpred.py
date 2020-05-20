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
# branchpred.py
#
# Branch Predictor Class instide of a Core Class

from xml.etree import ElementTree
from xml.dom import minidom

class Predictor:
  """ branch predictor; tournament predictor see Alpha implementation """
  name = "predictor"
  id = "predictor"

  parameters = \
  {
    "local_predictor_size" : ["10,3","Local Predictor Size"],
    "local_predictor_entries" : ["1024","Number of Entries in Local Predictor"],
    "global_predictor_entries" : ["4096","Global Predictor Entries"],
    "global_predictor_bits" : ["2","Bits per entry in Global Predictor"],
    "chooser_predictor_entries" : ["4096","Number of entries in the Chooser"],
    "chooser_predictor_bits" : ["2","Bits per entry in the chooser"]
  }
  stats = \
  {
  }

  def __init__(self, component_id, component_name, stat_dict, config_dict):
    self.name = component_name
    self.id = component_id

    # Init the Cache Parameters and Stats:
    #parameters["local_predictor_size"][0]=
    #parameters["local_predictor_entries"][0]=
    #parameters["global_predictor_entries"][0]=
    #parameters["global_predictor_bits"][0]=
    #parameters["chooser_predictor_entries"][0]=
    #parameters["chooser_predictor_bits"][0]=

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
