#!/bin/bash

TRACE_ROOT="/home/andrew/scratch/predict-T/arbitrary_input_traces"
LOG_ROOT="/home/andrew/scratch/predict-T/arbitrary_input_traces/package_model"

DEVICES=("SERVER" "LAPTOP" "MOBILE" "EMBEDDED" "PERF_UC" "LP_UP")
TRACE_DIRS=("server" "laptop" "mobile" "embedded" "perf_uc" "lp_uc")
LOG_DIRS=("server" "laptop" "mobile" "embedded" "perf_uc" "lp_uc")
VOLTAGE_AVP=("1.2" "1.2" "1.2" "1.2" "1.8" "3.3")
VOLTAGE_IDEAL=("1.08" "1.11995" "1.191995" "1.178" "1.7987" "3.29998")

PWM=("25" "50" "75")
SUPPLY=("IDEAL" "AVP")

for i in ${!DEVICES[@]}; do
  for j in ${!SUPPLY[@]}; do
    for l in ${!PWM[@]}; do
      for m in $(ls ${TRACE_ROOT}/${TRACE_DIRS[$i]}_${PWM[$l]}/*.csv); do
        # Run 
        if [ $j == 0 ]; then
          echo "python3 run.py $m ${VOLTAGE_IDEAL[$i]} ${DEVICES[$i]} ${SUPPLY[$j]} &"
          python3 run.py $m ${VOLTAGE_IDEAL[$i]} ${DEVICES[$i]} ${SUPPLY[$j]} &
        fi
        if [ $j == 1 ]; then
          echo "python3 run.py $m ${VOLTAGE_AVP[$i]} ${DEVICES[$i]} ${SUPPLY[$j]} &"
          python3 run.py $m ${VOLTAGE_AVP[$i]} ${DEVICES[$i]} ${SUPPLY[$j]} &
        fi
        while [ `jobs | wc -l` -ge 24 ]; do
          sleep 1
        done
      done

      while [ `jobs | wc -l` -ne 1 ]; do
        echo "`jobs | wc -l`"
        sleep 1
      done

      # Run Strip and Delete Logs
      for m in $(ls ${LOG_ROOT}/log/*.log); do 
        echo "python3 ../analysis/strip.py $m &"
        python3 ../analysis/strip.py $m &
        while [ `jobs | wc -l` -ge $(nproc) ]; do
          sleep 1
        done
      done

      while [ `jobs | wc -l` -ne 1 ]; do
        echo "`jobs | wc -l`"
        sleep 1
      done

      # Remove Logs
      echo "rm ${LOG_ROOT}/log/*.log"
      rm ${LOG_ROOT}/log/*.log

      # Move Directory
      echo "mv ${LOG_ROOT}/log ${LOG_ROOT}/${LOG_DIRS[$i]}_${SUPPLY[$j]}_${PWM[$l]}"
      mv ${LOG_ROOT}/log ${LOG_ROOT}/${LOG_DIRS[$i]}_${SUPPLY[$j]}_${PWM[$l]}
      
      # Make Log Dir
      echo "mkdir ${LOG_ROOT}/log"
      mkdir ${LOG_ROOT}/log
    done
  done
done
