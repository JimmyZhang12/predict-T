import os
import sys
import re
import pickle
import time
import subprocess
from threading import Thread
from time import sleep

import interprocess

thread = None

def initialize(name, step):
  global thread
  """ This function will launch the docker container for the verilog
  simulation. """
  def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
      output = process.stdout.readline()
      if output == '' and process.poll() is not None:
        break
      #if output:
        #print(output.strip(), flush=True)
    rc = process.poll()
    return rc

  def verilog_thread(name, step):
    """ This is the thread function for executing the verilog sim """
    run_command(["./run_cadence.sh", name, str(step)])


  if os.path.exists(os.path.join("/dev/shm", name)):
    os.remove(os.path.join("/dev/shm", name))

  thread = Thread(target=verilog_thread, args=[name, step])
  thread.setDaemon(True)
  thread.start()

  # Wait for the container to launch and the sim to run
  while not os.path.isfile(os.path.join("/dev/shm", name)):
    sleep(1)
  interprocess.create_shm(0, name)
  return


def set_driver_signals(voltage_setpoint, resistance, term_sim):
  interprocess.set_driver_signals(voltage_setpoint, resistance, term_sim)

def get_voltage():
  return interprocess.get_voltage()

def stop():
  subprocess.Popen(['reset']).wait()
