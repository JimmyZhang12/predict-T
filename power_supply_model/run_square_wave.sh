#!/bin/bash

for i in $(ls /scratch/predict-T/arbitrary_input_traces/*.csv); do
  python3 run.py $i &
  while [ `jobs | wc -l` -ge 32 ]; do
    sleep 1
  done
done
