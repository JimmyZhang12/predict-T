#!/bin/bash

# BUILD:
gcc hello_vpi.c -m32 -fPIC -shared -I/software/cadence-Aug2016/INCISIVE152/tools.lnx86/include -o hello_vpi.so

# RUN:
#irun tb.vams -top DAC6_TB +access+r -v ./hello_vpi.so -analogcontrol scf.scs
ncverilog tb.vams +access+r -loadvpi ./hello_vpi.so:register_hello -top DAC6_TB -analogcontrol scf.scs

