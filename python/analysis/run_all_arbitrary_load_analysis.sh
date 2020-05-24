#!/bin/bash

LOG_ROOT="/home/andrew/scratch/predict-T/arbitrary_input_traces/package_model"
OUT_ROOT="/home/andrew/scratch/predict-T/arbitrary_input_traces"

#DEVICES=("SERVER" "MOBILE" "EMBEDDED" "PERF_UC" "LP_UP")
#LOG_DIRS=("server" "mobile" "embedded" "perf_uc" "lp_uc")
DEVICES=("PERF_UC" "LP_UP")
LOG_DIRS=("perf_uc" "lp_uc")
#DEVICES=("SERVER")
#LOG_DIRS=("server")

PWM=("25" "50" "75")
SUPPLY=("IDEAL" "AVP")

for i in ${!DEVICES[@]}; do
  for j in ${!SUPPLY[@]}; do
    for l in ${!PWM[@]}; do
      OUTDIR=${OUT_ROOT}/img/${LOG_DIRS[$i]}_${SUPPLY[$j]}_${PWM[$l]}
      OUTDIR_ENERGY=${OUT_ROOT}/energy/${LOG_DIRS[$i]}_${SUPPLY[$j]}_${PWM[$l]}
      INDIR=${LOG_ROOT}/${LOG_DIRS[$i]}_${SUPPLY[$j]}_${PWM[$l]}
      echo "mkdir ${OUTDIR}"
      mkdir ${OUTDIR}
      echo "mkdir ${OUTDIR_ENERGY}"
      mkdir ${OUTDIR_ENERGY}
      echo "python3 arbitrary_load_analysis.py \
        --input=${INDIR} \
        --headers=time,vin,iin,vout,iout \
        --img_out=${OUTDIR} \
        --device=${LOG_DIRS[$i]} \
        --name=${LOG_DIRS[$i]}_${SUPPLY[$j]}_${PWM[$l]} \
        --csv_out=${OUTDIR_ENERGY} & "
      python3 arbitrary_load_analysis.py \
        --input=${INDIR} \
        --headers=time,vin,iin,vout,iout \
        --img_out=${OUTDIR} \
        --device=${LOG_DIRS[$i]} \
        --name=${LOG_DIRS[$i]}_${SUPPLY[$j]}_${PWM[$l]} \
        --csv_out=${OUTDIR_ENERGY}
      #while [ `jobs | wc -l` -ge 32 ]; do
      #  sleep 1
      #done
    done
    #while [ `jobs | wc -l` -ne 1 ]; do
    #  echo "`jobs | wc -l`"
    #  sleep 1
    #done
  done
done

