#!/bin/bash

for pid in $(ps -ef | grep "python3 run.py" | awk '{print $2}'); do kill -9 $pid; done
for pid in $(ps -ef | grep "ncverilog" | awk '{print $2}'); do kill -9 $pid; done
