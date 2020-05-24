#!/bin/bash
#
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

if [ -z "$SIM_ROOT" ]; then
  echo "[ run_vsim.sh ] error: SIM_ROOT not set; source setup.sh"
  exit 1
fi

# Add the cadence tools to the PATH.
# Cadence AUG2016 is the cadence version that is currently tested on.
export PATH=/software/cadence-Aug2016/INNOVUS161/tools/bin/64bit:/software/cadence-Aug2016/INNOVUS1611/share/bin/64bit:/software/cadence-Aug2016/INNOVUS161/bin:/software/cadence-Aug2016/MMSIM151/tools/bin/64bit:/software/cadence-Aug2016/MMSIM151/share/bin:/software/cadence-Aug2016/MMSIM151/bin:/software/cadence-Aug2016/INCISIVE152/tools/bin/64bit:/software/cadence-Aug2016/INCISIVE152/share/bin:/software/cadence-Aug2016/INCISIVE152/bin:/software/cadence-Aug2016/IC617/tools.lnx86/leapfrog/bin:/software/cadence-Aug2016/IC617/tools.lnx86/dfII/bin:/software/cadence-Aug2016/IC617/tools.lnx86/bin:/software/cadence-Aug2016/IC617/share/bin:/software/cadence-Aug2016/IC617/bin:/software/cadence-Aug2016/ETS131/tools.lnx86/bin:/software/cadence-Aug2016/ETS131/share/bin:/software/cadence-Aug2016/ETS131/bin:/software/cadence-Aug2016/EDI142/tools.lnx86/bin:/software/cadence-Aug2016/EDI142/share/bin:/software/cadence-Aug2016/EDI142/bin:/software/cadence-Aug2016/ADW166/tools.lnx86/bin:/software/cadence-Aug2016/ADW166/share/bin:/software/cadence-Aug2016/ADW166/bin:$PATH

# U of I License server:
export LM_LICENSE_FILE=5280@cadence.webstore.illinois.edu

# This variable must be set when working on an unsupported OS.
# So far only CentOS 7 with GLIBC version 2.17 has worked.
export OA_UNSUPPORTED_PLAT=linux_rhel50_gcc48x

pushd /run_vsim
ln -s $SIM_ROOT/interprocess.cpp ./interprocess.c
ln -s $SIM_ROOT/interprocess.h .
ln -s $SIM_ROOT/circuit_model.vams .
ln -s $SIM_ROOT/predictive_supply.vams .
ln -s $SIM_ROOT/board_package.vams .
ln -s $SIM_ROOT/resistor.vams .
ln -s $SIM_ROOT/scf.scs .

# BUILD 64 Bit VPI Library:
gcc interprocess.c -O0 -g -DWITH_VPI -std=c11 -D_XOPEN_SOURCE=500 -fPIC -fpermissive -shared -I/software/cadence-Aug2016/INCISIVE152/tools.lnx86/include -lpthread -o interprocess.so

# RUN 64 Bit version of VSIM:
#+define+${3}=1 \
#+define+${4}=1 \
ncverilog \
  +define+SHM_NAME=\\\"${1}\\\" \
  +define+STEP_SIZE=${2} \
  circuit_model.vams \
  +access+r -loadvpi ./interprocess.so:register_create_shm \
  -loadvpi ./interprocess.so:register_destroy_shm \
  -loadvpi ./interprocess.so:register_wait_driver_data \
  -loadvpi ./interprocess.so:register_get_voltage_setpoint \
  -loadvpi ./interprocess.so:register_get_effective_resistance \
  -loadvpi ./interprocess.so:register_get_prediction \
  -loadvpi ./interprocess.so:register_get_enable \
  -loadvpi ./interprocess.so:register_get_terminate_simulation \
  -loadvpi ./interprocess.so:register_ack_driver_data \
  -loadvpi ./interprocess.so:register_send_voltage \
  -loadvpi ./interprocess.so:register_send_current \
  -loadvpi ./interprocess.so:register_ack_simulation \
  -top circuit_model \
  -analogcontrol scf.scs > "$OUTPUT_ROOT/circuit_model/log/${1}_out.log"
