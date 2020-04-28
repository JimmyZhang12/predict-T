import vsim
import sys


vset = sys.argv[2]
mem = sys.argv[1].split(".")[0].split("/")[-1]
vsim.initialize(mem, 1, sys.argv[3], sys.argv[4])
# Warmup Period:
with open(sys.argv[1].split(".")[0]+".csv", "r") as profile:
  data = profile.readlines()
  for point in data:
    vsim.set_driver_signals(float(vset), float(point.split(",")[1].strip()), 0)
    vsim.get_voltage()
vsim.set_driver_signals(float(vset),1,1)
vsim.get_voltage()
#vsim.stop()
