#!/bin/bash
#
# Copyright (c) 2020 Andrew Smith
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

se_single_core_xeon_e7_8893() {
  TN=$1
  DURATION=$2
  INTERVAL=$3
  STEP=$4
  PROFILE_START=$5
  EXE=$6
  OPT=$7
  L1I="32kB"
  L1D="64kB"
  L2="256kB"
  L3="16MB"

  #echo "Test Name: $TN, Duration: $DURATION, Interval: $INTERVAL, Step: $STEP, Profile Start: $PROFILE_START, Exe: $EXE, Opt: $OPT"

#  --power_pred_type=TestPowerPredictor \
#  --power_pred_table_size=${TABLE_SIZE[$l]} \
#  --power_pred_pc_start=${PC_START[$m]} \
#  --power_pred_history_size=${HISTORY_SIZE[$o]} \
  
  echo "
../gem5/build/X86/gem5.opt \
--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
--mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
--mcpat_path=${PREDICT_T_ROOT}/mcpat \
--mcpat_out=${OUTPUT_ROOT}/mcpat_out \
--mcpat_testname=$TN \
--power_profile_start=${PROFILE_START[$i]} \
--power_profile_duration=${DURATION[$i]} \
--power_profile_interval=${INTERVAL[$i]} \
--ncverilog_path=${PREDICT_T_ROOT}/package_model \
--ncverilog_step=${STEP[$i]} \
../gem5/configs/example/se.py \
--cmd=testbin/${exe[$j]} \
--opt=\"${opt[$j]}\" \
--power_profile_interval=${INTERVAL[$i]} \
--num-cpus=1 \
--cpu-type=DerivO3CPU \
--l1i_size=${L1I} \
--l1i-hwp-type=TaggedPrefetcher \
--l1d_size=${L1D} \
--l1d-hwp-type=TaggedPrefetcher \
--l2cache \
--num-l2caches=1 \
--l2_size=${L2} \
--l2-hwp-type=TaggedPrefetcher \
--l3cache \
--l3_size=${L3} \
--l3-hwp-type=TaggedPrefetcher \
--caches \
--sys-clock=3.5GHz \
--mem-size=8GB > ${OUTPUT_ROOT}text_out/$TN.out &"
  ../gem5/build/X86/gem5.opt \
    --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
    --mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
    --mcpat_path=${PREDICT_T_ROOT}/mcpat \
    --mcpat_out=${OUTPUT_ROOT}/mcpat_out \
    --mcpat_testname=$TN \
    --power_profile_start=${PROFILE_START[$i]} \
    --power_profile_duration=${DURATION[$i]} \
    --power_profile_interval=${INTERVAL[$i]} \
    --ncverilog_path=${PREDICT_T_ROOT}/package_model \
    --ncverilog_step=${STEP[$i]} \
    ../gem5/configs/example/se.py \
    --cmd=testbin/${exe[$j]} \
    --opt="${opt[$j]}" \
    --power_profile_interval=${INTERVAL[$i]} \
    --num-cpus=1 \
    --cpu-type=DerivO3CPU \
    --l1i_size=${L1I} \
    --l1i-hwp-type=TaggedPrefetcher \
    --l1d_size=${L1D} \
    --l1d-hwp-type=TaggedPrefetcher \
    --l2cache \
    --num-l2caches=1 \
    --l2_size=${L2} \
    --l2-hwp-type=TaggedPrefetcher \
    --l3cache \
    --l3_size=${L3} \
    --l3-hwp-type=TaggedPrefetcher \
    --caches \
    --sys-clock=3.5GHz \
    --mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &
}

se_n_core_xeon_e7_8893() {
  TN=$1
  DURATION=$2
  INTERVAL=$3
  STEP=$4
  PROFILE_START=$5
  EXE=$6
  OPT=$7
  NCORES=$8
  L1I="32kB"
  L1D="64kB"
  L2="256kB"
  L3="16MB"

  #echo "Test Name: $TN, Duration: $DURATION, Interval: $INTERVAL, Step: $STEP, Profile Start: $PROFILE_START, Exe: $EXE, Opt: $OPT, NCores: $NCORES"
  #exit

#  --power_pred_type=TestPowerPredictor \
#  --power_pred_table_size=${TABLE_SIZE[$l]} \
#  --power_pred_pc_start=${PC_START[$m]} \
#  --power_pred_history_size=${HISTORY_SIZE[$o]} \
  
  echo "
../gem5/build/X86/gem5.opt \
--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
--mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
--mcpat_path=${PREDICT_T_ROOT}/mcpat \
--mcpat_out=${OUTPUT_ROOT}/mcpat_out \
--mcpat_testname=$TN \
--power_profile_start=${PROFILE_START} \
--power_profile_duration=${DURATION} \
--power_profile_interval=${INTERVAL} \
--ncverilog_path=${PREDICT_T_ROOT}/package_model \
--ncverilog_step=${STEP} \
../gem5/configs/example/se.py \
--cmd=testbin/${EXE} \
--opt=\"${OPT}\" \
--power_profile_interval=${INTERVAL} \
--num-cpus=$NCORES \
--cpu-type=DerivO3CPU \
--l1i_size=${L1I} \
--l1i-hwp-type=TaggedPrefetcher \
--l1d_size=${L1D} \
--l1d-hwp-type=TaggedPrefetcher \
--l2cache \
--num-l2caches=1 \
--l2_size=${L2} \
--l2-hwp-type=TaggedPrefetcher \
--l3cache \
--l3_size=${L3} \
--l3-hwp-type=TaggedPrefetcher \
--caches \
--sys-clock=3.5GHz \
--mem-size=8GB > ${OUTPUT_ROOT}text_out/$TN.out &"
  ../gem5/build/X86/gem5.opt \
    --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
    --mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
    --mcpat_path=${PREDICT_T_ROOT}/mcpat \
    --mcpat_out=${OUTPUT_ROOT}/mcpat_out \
    --mcpat_testname=$TN \
    --power_profile_start=${PROFILE_START} \
    --power_profile_duration=${DURATION} \
    --power_profile_interval=${INTERVAL} \
    --ncverilog_path=${PREDICT_T_ROOT}/package_model \
    --ncverilog_step=${STEP} \
    ../gem5/configs/example/se.py \
    --cmd=testbin/${EXE} \
    --opt="${OPR}" \
    --power_profile_interval=${INTERVAL} \
    --num-cpus=$NCORES \
    --cpu-type=DerivO3CPU \
    --l1i_size=${L1I} \
    --l1i-hwp-type=TaggedPrefetcher \
    --l1d_size=${L1D} \
    --l1d-hwp-type=TaggedPrefetcher \
    --l2cache \
    --num-l2caches=$NCORES \
    --l2_size=${L2} \
    --l2-hwp-type=TaggedPrefetcher \
    --l3cache \
    --l3_size=${L3} \
    --l3-hwp-type=TaggedPrefetcher \
    --caches \
    --sys-clock=3.5GHz \
    --mem-size=8GB 
#> ${OUTPUT_ROOT}/text_out/$TN.out &
}
