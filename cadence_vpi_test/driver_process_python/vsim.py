import os
import sys
import re
import pickle
import time
from threading import Thread
from Queue import Queue
from time import sleep
import progressbar

import interprocess

thread = None

def initialize(name):
	global thread
  """ This function will launch the docker container for the verilog
  simulation. """
  def verilog_thread(name):
    """ This is the thread function for executing the verilog sim """
    cmd = ["./run_cadence.sh", name]
    p = subprocess.Popen(mcpat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    out = p.communicate()
    print(out[0])

	thread = Thread(target=verilog_thread, args=[name])
	thread.start()

  # Wait for the container to launch and the sim to run
	time.sleep(10)
	interprocess.create_shm(0, name)

	interprocess.set_driver_signals(1,4)
	interprocess.set_driver_signals(2,3)
	interprocess.set_driver_signals(3,2)
	interprocess.set_driver_signals(4,1)
