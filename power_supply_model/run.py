import vsim
import sys

mem = sys.argv[1].split(".")[0].split("/")[-1]
vsim.initialize(mem, 1)
# Warmup Period:
with open(sys.argv[1].split(".")[0]+".csv", "r") as profile:
  data = profile.readlines()
  for i in range(0): # 0us Warmup
    vsim.set_driver_signals(1.0, float(data[0].split(",")[1].strip()), 0)
    vsim.get_voltage()
  for point in data:
    vsim.set_driver_signals(1.0, float(point.split(",")[1].strip()), 0)
    vsim.get_voltage()
    #print(",".join([str(1.0), str(point.split(",")[1]), str(vsim.get_voltage())]), flush=True)
vsim.set_driver_signals(0,1,1)
vsim.get_voltage()
#vsim.stop()
