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
  def verilog_thread(name, step):
    """ This is the thread function for executing the verilog sim """
    cmd = ["./run_cadence.sh", name, str(step)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    out = p.communicate()
    print(out[0])

  thread = Thread(target=verilog_thread, args=[name, step])
  thread.start()

  # Wait for the container to launch and the sim to run
  time.sleep(10)
  interprocess.create_shm(0, name)
  return


def set_driver_signals(voltage_setpoint, resistance, term_sim):
  interprocess.set_driver_signals(voltage_setpoint, resistance, term_sim)

def get_voltage():
  return interprocess.get_voltage()
