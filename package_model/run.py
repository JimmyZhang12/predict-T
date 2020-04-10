import vsim
import sys

vsim.initialize("mb_mem_2000", 250)
# Warmup Period:
with open("mb_mem_2000.csv", "r") as profile:
  data = profile.readlines()
  for i in range(400): # 100us Warmup
    vsim.set_driver_signals(1.0, float(data[0].split(",")[1].strip()), 0)
    vsim.get_voltage()
  for point in data:
    vsim.set_driver_signals(1.0, float(point.split(",")[1].strip()), 0)
    vsim.get_voltage()
    #print(",".join([str(1.0), str(point.split(",")[1]), str(vsim.get_voltage())]), flush=True)
vsim.set_driver_signals(0,1,1)
vsim.get_voltage()
#vsim.stop()
