import os
import sys
import re
import pickle
from threading import Thread
from Queue import Queue
from time import sleep
import progressbar

from mcpat import *

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
          keys[i][j] = str(float(stats[keys[i][j]][1]))
        elif keys[i][j] in config:
          keys[i][j] = str(float(config[keys[i][j]]))
        elif "stats" in keys[i][j] or "config" in keys[i][j]:
          keys[i][j] = "0"

    split_line[1] = ",".join([" ".join(y) for y in keys])
    print(split_line[1])
    # Evaluate
    expr = split_line[1].split(",")
    for i in range(len(expr)):
      try:
        expr[i] = str(int(max(math.ceil(eval(expr[i])),0)))
      except:
        expr[i] = "0"
    split_line[1] = ",".join(expr)
    print(split_line[1])

    #print(keys)
    #print("".join(split_line))
    return "".join(split_line)
  return xml_line

# m5_to_mcpat
# Takes in the output files from gem5 run (config.ini, stats.txt) and converts to a 
# McPat input xml file based on a template.
#def m5_to_mcpat(m5_stats_file, m5_config_file, mcpat_template_file, mcpat_output_path, testname):
def m5_to_mcpat(m5_stats_file, m5_config_file, mcpat_template_file, mcpat_output_path):
  stats = parse_stats(m5_stats_file)[-1]
  #print_stats(stats)
  config = parse_config(m5_config_file)
  #print_config(config)
  with open(mcpat_template_file, "r") as tf, open(mcpat_output_path, "w") as inf:
    in_xml = tf.readlines()
    out_xml = []
    for line in in_xml:
      out_xml.append(replace(line, stats, config))
    inf.writelines(out_xml)
#  if not os.path.isdir(mcpat_output_path):
#    os.mkdir(mcpat_output_path)
#
#  def mcpat_thread(config, iq, oq):
#    while not iq.empty():
#      work = iq.get()
#      t_f = "mcpat-template.xml"
#      i_f = os.path.join(mcpat_output_path,"mp_arm_"+str(work[0])+".xml")
#      o_f = os.path.join(mcpat_output_path,"mp_"+str(work[0])+".out")
#      e_f = os.path.join(mcpat_output_path,"mp_"+str(work[0])+".err")
#      with open(t_f, "r") as tf, open(i_f, "w") as inf:
#        in_xml = tf.readlines()
#        out_xml = []
#        for line in in_xml:
#          out_xml.append(replace(line, work[1], config))
#        inf.writelines(out_xml)
#      run_mcpat(i_f, "5", "1", o_f, e_f)
#      oq.put((work[0], parse_output(o_f)))

#  input_queue = Queue()
#  output_queue = Queue()
#  epochs = parse_stats(m5_stats_file)
#  config = parse_config(m5_config_file)
#  mcpat_trees = [None]*len(epochs)
#  threads = []
#
#  #""" Initialize Input Queue """
#  #for i, epoch in zip(range(len(epochs)), epochs):
#  #  input_queue.put((i, epoch))
#
#  #""" Launch Worker Threads """
#  #for i in range(16):
#  #  thr = Thread(target=mcpat_thread, args=[config, input_queue, output_queue])
#  #  thr.start()
#  #  threads.append(thr)
#
#  #bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]) #bar.start()
#  #while not input_queue.empty():
#  #  progress = int((len(epochs)-input_queue.qsize())*100/len(epochs))
#  #  bar.update(progress)
#  #  sleep(0.1)
#  #bar.finish()
#
#  #""" Dequeue from Output Queue """
#  #for thr in threads:
#  #  thr.join()
#
#  #while not output_queue.empty():
#  #  ret = output_queue.get()
#  #  mcpat_trees[ret[0]] = ret[1]
#
#  sfile = os.path.join(mcpat_output_path, testname+".pickle")
#
#  #with open(sfile, "w") as mpe:
#  #  pickle.dump(mcpat_trees, mpe)
#  with open(sfile, "r") as mpe:
#    mcpat_trees = pickle.load(mpe)
#  plot(mcpat_trees, testname, mcpat_output_path)


  #print_stats(stats)
  #print_config(config)
  #print("Num Stats: "+str(len(stats)))
  #print("Num Configs: "+str(len(config)))

# Test Code:
m5_to_mcpat("gem5_out/mb_double_add_10000_16kB_64kB_256kB_32MB/stats.txt", "gem5_out/mb_double_add_10000_16kB_64kB_256kB_32MB/config.ini", "mcpat-template-x86.xml", "mcpat_machine_bronk.xml")
