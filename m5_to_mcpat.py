import os
import sys
import re

def parse_stats(stat_file):
  epoch = []
  stats = {}
  with open(stat_file, "r") as sf:
    for line in sf:
      if line.strip() == "":
        continue
      elif "End Simulation Statistics" in line:
        epoch.append(stats)
      elif "Begin Simulation Statistics" in line:
        stats = {}
      else:
        stat = []
        sstr = re.sub('\s+', ' ', line).strip()
        if('-----' in sstr):
          continue
        elif(sstr == ''):
          continue
        elif(sstr.split(' ')[1] == '|'):
          # Ruby Stats
          l = []
          for i in sstr.split('|')[1:]:
            l.append(i.strip().split(' '))
          stat.append("ruby_multi")
          stat.append(l)
        else:
          stat.append("single")
          stat.append(sstr.split(' ')[1])
        stats["stats."+sstr.split(' ')[0]] = stat
  print("Read "+str(len(epoch))+" Epochs")
  return epoch

def print_stats(stats):
  for sname, stat in stats.items():
    if(stat[0] == "single"):
      print(sname+" "+stat[1])
    elif(stat[0] == "ruby_multi"):
      print(sname+" "+" ".join(" ".join(x) for x in stat[1]))

def parse_config(config_file):
  config = {}
  hierarchy = ""
  with open(config_file, "r") as cf:
    lines = cf.readlines()
    for line in lines:
      cstr = re.sub('\s+', ' ', line).strip()
      if(cstr == ''):
        continue
      if("[" in cstr and "]" in cstr):
        hierarchy="config."+cstr.replace("[", "").replace("]", "")+"."
        continue
      else:
        config[hierarchy+cstr.split('=')[0]] = cstr.split('=')[1].strip()
  return config

def print_config(config):
  for cname, config in config.items():
    print(cname+" "+config)

# replace
# Replaces the REPLACE{...} with the appropriate value from the dictionary
# Returns a string with the substituted lines
def replace(xml_line, stats, config):
  if('REPLACE{' in xml_line):
    split_line = re.split('REPLACE{|}', xml_line)
    #print(split_line)
    keys = [x.strip().split(" ") for x in re.split(',', split_line[1])]
    for i in range(len(keys)):
      for j in range(len(keys[i])):
        if keys[i][j] in stats:
          keys[i][j] = stats[keys[i][j]][1]
        elif keys[i][j] in config:
          keys[i][j] = config[keys[i][j]]
        elif "stats" in keys[i][j] or "config" in keys[i][j]:
          keys[i][j] = "0"
    #print(keys)
    split_line[1] = ",".join([" ".join(y) for y in keys])
    #print("".join(split_line))
    return "".join(split_line)
  return xml_line

# m5_to_mcpat
# Takes in the output files from gem5 run (config.ini, stats.txt) and converts to a 
# McPat input xml file based on a template.
def m5_to_mcpat(m5_stats_file, m5_config_file, mcpat_template_file, mcpat_input_file):
  epoch = parse_stats(m5_stats_file)
  config = parse_config(m5_config_file)
  for stats in epoch:
    with open(mcpat_template_file, "r") as mct, open(mcpat_input_file, "w") as mc:
      in_xml = mct.readlines()
      out_xml = []
      for line in in_xml:
        out_xml.append(replace(line, stats, config))
      mc.writelines(out_xml)

  #print_stats(stats)
  #print_config(config)
  #print("Num Stats: "+str(len(stats)))
  #print("Num Configs: "+str(len(config)))

# Test Code:
#m5_to_mcpat("gem5/output/fft_small_x86/stats.txt", "gem5/output/fft_small_x86/config.ini", "mcpat_template.xml", "mcpat_x86.xml")
m5_to_mcpat("output/fft_small/stats.txt", "output/fft_small/config.ini", "mcpat-template.xml", "mcpat_arm.xml")
