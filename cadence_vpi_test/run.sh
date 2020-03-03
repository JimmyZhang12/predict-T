#!/bin/bash

# BUILD:
#gcc hello_vpi.c -m32 -fPIC -shared -I/software/cadence-Aug2016/INCISIVE152/tools.lnx86/include -o hello_vpi.so
gcc interprocess.c -O0 -g -DWITH_VPI -std=c11 -D_XOPEN_SOURCE=500 -m32 -fPIC -shared -I/software/cadence-Aug2016/INCISIVE152/tools.lnx86/include -lpthread -o interprocess.so

# RUN:
#irun tb.vams -top DAC6_TB +access+r -v ./hello_vpi.so -analogcontrol scf.scs
ncverilog \
  tb.vams \
  +access+r -loadvpi ./interprocess.so:register_create_shm \
  -loadvpi ./interprocess.so:register_destroy_shm \
  -loadvpi ./interprocess.so:register_wait_driver_data \
  -loadvpi ./interprocess.so:register_get_voltage_setpoint \
  -loadvpi ./interprocess.so:register_get_effective_resistance \
  -loadvpi ./interprocess.so:register_get_terminate_simulation \
  -loadvpi ./interprocess.so:register_ack_driver_data \
  -loadvpi ./interprocess.so:register_send_powersupply_stats \
  -top DAC6_TB \
  -analogcontrol scf.scs

