#!/bin/bash

for i in $(ls ${1}/*.csv); do
  python3 run.py $i ${2} &
  while [ `jobs | wc -l` -ge 24 ]; do
    sleep 1
  done
done
