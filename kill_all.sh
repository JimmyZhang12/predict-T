#!/bin/bash

for pid in $(ps -ef | grep "print_level 5" | awk '{print $2}'); do kill -9 $pid; done
for pid in $(ps -ef | grep "gem5.opt" | awk '{print $2}'); do kill -9 $pid; done
