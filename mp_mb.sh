#!/bin/bash

#MICRO_BENCHMARKS=("mb_cache_coherence")
#MICRO_BENCHMARKS=("mb_cache_coherence" "mb_double_add" "mb_double_mul" "mb_int_add" "mb_int_mul" "mb_mem" "mb_phases" "mb_sleep")
#MICRO_BENCHMARKS=("mb_cache_coherence"  "mb_double_add" "mb_double_mul" "mb_int_add" "mb_int_mul" "mb_mem"       "mb_phases"    "mb_sleep")
#PROFILE_START=("1000000000"        "100000000"     "100000000"     "100000000"  "100000000"  "1000000000" "1000000000" "100000000")
MICRO_BENCHMARKS=("mb_double_add" "mb_double_mul" "mb_int_add" "mb_int_mul")
PROFILE_START=("1000000000"     "1000000000"     "1000000000"  "1000000000")
#DURATION=("5000" "10000" "50000" "100000" "500000" "1000000")
DURATION=("50000")
INTERVAL=("500")
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
      NAME=${MICRO_BENCHMARKS[$j]}_${INTERVAL[$i]}_${L1I[$k]}_${L1D[$k]}_${L2[$k]}_${L3[$k]}
      echo "
../gem5/build/X86/gem5.opt \
--outdir=./gem5_out/$NAME \
--mcpat_template=/home/andrew/research/predict-T/mcpat-template-x86-sc.xml \
--mcpat_path=/home/andrew/research/predict-T/mcpat \
--mcpat_out=/home/andrew/research/predict-T/mcpat_short_trace_033020 \
--mcpat_testname=$NAME \
--power_profile_start=${PROFILE_START[$j]} \
--power_profile_duration=${DURATION[$i]} \
--power_profile_interval=${INTERVAL[$i]} \
../gem5/configs/example/se.py \
--cmd=mcpat_bench/${MICRO_BENCHMARKS[$j]} \
--power_profile_interval=${INTERVAL[$i]} \
--num-cpus=4 \
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
  --mcpat_template=/home/andrew/research/predict-T/mcpat-template-x86-sc.xml \
  --mcpat_path=/home/andrew/research/predict-T/mcpat \
  --mcpat_out=/home/andrew/research/predict-T/mcpat_short_trace_033020 \
  --mcpat_testname=$NAME \
  --power_profile_start=${PROFILE_START[$j]} \
  --power_profile_duration=${DURATION[$i]} \
  --power_profile_interval=${INTERVAL[$i]} \
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
  --mem-size=8GB > text_out/$NAME.out &
      while [ `jobs | wc -l` -ge 16 ]; do
        sleep 1
      done
    done
  done
done

#../gem5/build/X86/gem5.opt \
#  --outdir=./gem5_out/ \
#  --mcpat_template=/home/andrew/research/predict-T/mcpat-template-x86.xml \
#  --mcpat_path=/home/andrew/research/predict-T/mcpat \
#  --mcpat_out=/home/andrew/research/predict-T/mcpat_bench_out \
#  --mcpat_testname=dijkstra_large_10000 \
#  --power_profile_start=100000000 \
#  --power_profile_duration=${DURATION[$i]} \
#  --power_profile_interval=${INTERVAL[$i]} \
#  ../gem5/configs/example/se.py \
#  --cmd=mcpat_bench/${MICRO_BENCHMARKS[$j]} \
#  --power_profile_interval=${INTERVAL[$i]} \
#  --num-cpus=4 \
#  --cpu-type=DerivO3CPU \
#  --bp-type=MultiperspectivePerceptronTAGE64KB \
#  --l1i_size=${L1I[$k]} \
#  --l1i-hwp-type=TaggedPrefetcher \
#  --l1d_size=${L1D[$k]} \
#  --l1d-hwp-type=TaggedPrefetcher \
#  --l2cache \
#  --num-l2caches=4 \
#  --l2_size=${L2[$k]} \
#  --l2-hwp-type=TaggedPrefetcher \
#  --l3cache \
#  --l3_size=${L3[$k]} \
#  --l3-hwp-type=BOPPrefetcher \
#  --caches \
#  --mem-size=8GB &
