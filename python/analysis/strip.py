# Strip the power supply output of all non numerics
import sys

a = []

infile = sys.argv[1]

fname = sys.argv[1].split(".")
fname[-1]="csv"

outfile = ".".join(fname)

with open(infile, "r") as inf:
  a = inf.readlines()

with open(outfile, "w") as outf:
  for line in a:
    sline = line.strip()
    try:
      out = float(line.split(",")[0])
    except:
      continue
    outf.write(sline+"\n")
