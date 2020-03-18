import vsim
import sys

vsim.initialize("a3lhsdflj234jf", 1)
with open("../test_load.csv", "r") as profile:
  data = profile.readlines()
  for point in data:
    vsim.set_driver_signals(1.0, float(point.split(",")[1].strip()), 0)
    vsim.get_voltage()
    #print(",".join([str(1.0), str(point.split(",")[1]), str(vsim.get_voltage())]), flush=True)
vsim.set_driver_signals(0,1,1)
vsim.get_voltage()
vsim.stop()
