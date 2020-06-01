# Copyright (c) 2020 Andrew Smith
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math
import sys
import argparse

parser = argparse.ArgumentParser(description='Calculate LC based on a R,Q,F0, for a second order PDN model')
parser.add_argument('-r','--dc_resistance',type=float,required=True,help='The DC Resistance of the PDN')
parser.add_argument('-q','--quality',type=float,required=True,help='The Quality Factor of the PDN')
parser.add_argument('-f','--resonant_freq',type=float,required=True,help='The resonant frequency f0 of the PDN')
args = parser.parse_args()

r = args.dc_resistance
q = args.quality
f0 = args.resonant_freq

l = r*q/(2*math.pi*f0)
c = 1/(math.pow((2*math.pi)*f0,2)*l)
print("R: "+str(r)+" Q: "+str(q)+" L: "+str(l)+" C: "+str(c))
