# Strip the power supply output of all non numerics
import sys

a = []
with open(sys.argv[1], "r") as inf:
  a = inf.readlines()

with open(sys.argv[2], "w") as outf:
  for line in a:
    sline = line.strip()
    try:
      out = float(line.split(",")[0])
    except:
      continue
    outf.write(sline+"\n")
