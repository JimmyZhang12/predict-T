#!/bin/bash

DEVICES=("server" "laptop" "mobile" "embedded" "perf_uc" "lp_uc")
ROOT="/home/andrew/scratch/predict-T/arbitrary_input_traces"
DUTY=("25" "50" "75")

for i in ${!DEVICES[@]}; do
  for j in ${!DUTY[@]}; do
    mkdir $ROOT/${DEVICES[$i]}_${DUTY[$j]}
  done
done

for i in ${!DEVICES[@]}; do
  for j in ${!DUTY[@]}; do
    python3 square_wave.py --outpath=$ROOT/${DEVICES[$i]}_${DUTY[$j]} --duty=0.${DUTY[$j]} --device=${DEVICES[$i]} &
    while [ `jobs | wc -l` -ge 32 ]; do
      sleep 1
    done
  done
done
