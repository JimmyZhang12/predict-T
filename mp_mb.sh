#!/bin/bash

#MICRO_BENCHMARKS=("mb_cache_coherence")
#MICRO_BENCHMARKS=("mb_cache_coherence" "mb_double_add" "mb_double_mul" "mb_int_add" "mb_int_mul" "mb_mem" "mb_phases" "mb_sleep")
#MICRO_BENCHMARKS=("mb_cache_coherence"  "mb_double_add" "mb_double_mul" "mb_int_add" "mb_int_mul" "mb_mem"       "mb_phases"    "mb_sleep")
#PROFILE_START=("1000000000"        "100000000"     "100000000"     "100000000"  "100000000"  "1000000000" "1000000000" "100000000")
#MICRO_BENCHMARKS=("mb_cache_coherence" "mb_double_mul" "mb_int_add" "mb_mem" "mb_phases")
#PROFILE_START=("1000000000" "100000000" "100000000" "1000000000" "1000000000")
MICRO_BENCHMARKS=("dijkstra")
PROFILE_START=("-1")
#MICRO_BENCHMARKS=("mb_double_add" "mb_double_mul" "mb_int_add" "mb_int_mul")
#PROFILE_START=("10000000"     "10000000"     "10000000"  "10000000")
#DURATION=("5000" "10000" "50000" "100000" "500000" "1000000")
#DURATION=("2000000" "20000000" "200000000")
#INTERVAL=("2000"    "20000"    "200000")
#STEP=("1000"    "10000"    "100000")
DURATION=("10000")
INTERVAL=("1000")
STEP=("500")
#DURATION=("50000" "100000" "500000" "1000000" "5000000" "10000000")
#INTERVAL=("500"   "1000"   "5000"   "10000"   "50000"   "100000")

L1D=("64kB")
L1I=("16kB")
L2=("256kB")
L3=("32MB")
#L1D=("16kB" "32kB" "64kB")
#L1I=("4kB"  "8kB"  "16kB")
#L2=("64kB" "128kB" "256kB")
#L3=("8MB"  "16MB"  "32MB")

for j in ${!MICRO_BENCHMARKS[@]}; do 
  for i in ${!INTERVAL[@]}; do 
    for k in ${!L1D[@]}; do 
      NAME=${MICRO_BENCHMARKS[$j]}_${INTERVAL[$i]}
      #NAME=${MICRO_BENCHMARKS[$j]}_${INTERVAL[$i]}_${L1I[$k]}_${L1D[$k]}_${L2[$k]}_${L3[$k]}
      echo "
../gem5/build/X86/gem5.opt \
--outdir=./gem5_out/$NAME \
--mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
--mcpat_path=${PREDICT_T_ROOT}/mcpat \
--mcpat_out=${PREDICT_T_ROOT}/mcpat_out \
--mcpat_testname=$NAME \
--power_profile_start=${PROFILE_START[$j]} \
--power_profile_duration=${DURATION[$i]} \
--power_profile_interval=${INTERVAL[$i]} \
--ncverilog_path=${PREDICT_T_ROOT}/power_supply_model \
--ncverilog_step=${STEP[$i]} \
../gem5/configs/example/se.py \
--cmd=mcpat_bench/${MICRO_BENCHMARKS[$j]} \
--power_profile_interval=${INTERVAL[$i]} \
--num-cpus=1 \
--cpu-type=DerivO3CPU \
--l1i_size=${L1I[$k]} \
--l1i-hwp-type=TaggedPrefetcher \
--l1d_size=${L1D[$k]} \
--l1d-hwp-type=TaggedPrefetcher \
--l2cache \
--num-l2caches=4 \
--l2_size=${L2[$k]} \
--l2-hwp-type=TaggedPrefetcher \
--l3cache \
--l3_size=${L3[$k]} \
--l3-hwp-type=TaggedPrefetcher \
--caches \
--sys-clock=2GHz \
--mem-size=8GB > text_out/$NAME.out &"
../gem5/build/X86/gem5.opt \
  --outdir=./gem5_out/$NAME \
  --mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
  --mcpat_path=${PREDICT_T_ROOT}/mcpat \
  --mcpat_out=${PREDICT_T_ROOT}/mcpat_out \
  --mcpat_testname=$NAME \
  --power_profile_start=${PROFILE_START[$j]} \
  --power_profile_duration=${DURATION[$i]} \
  --power_profile_interval=${INTERVAL[$i]} \
  --ncverilog_path=${PREDICT_T_ROOT}/power_supply_model \
  --ncverilog_step=${STEP[$i]} \
  ../gem5/configs/example/se.py \
  --cmd=testbin/${MICRO_BENCHMARKS[$j]} \
  --opt=input/dijkstra.dat \
  --power_profile_interval=${INTERVAL[$i]} \
  --num-cpus=1 \
  --cpu-type=DerivO3CPU \
  --l1i_size=${L1I[$k]} \
  --l1i-hwp-type=TaggedPrefetcher \
  --l1d_size=${L1D[$k]} \
  --l1d-hwp-type=TaggedPrefetcher \
  --l2cache \
  --num-l2caches=4 \
  --l2_size=${L2[$k]} \
  --l2-hwp-type=TaggedPrefetcher \
  --l3cache \
  --l3_size=${L3[$k]} \
  --l3-hwp-type=TaggedPrefetcher \
  --caches \
  --sys-clock=2GHz \
  --mem-size=8GB > text_out/$NAME.out &
      while [ `jobs | wc -l` -ge 16 ]; do
        sleep 1
      done
    done
  done
done
