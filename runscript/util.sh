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

#------------------------------------------------------------------------------
# se_sc_classic_mc_ncv
#   Syscall Emulation with Single Core, Classic Caches, and McPAT+NCVERILOG
#------------------------------------------------------------------------------
se_sc_classic_mc_ncv() {
  TN=$1
  DUR=$2
  INT=$3
  PS=$4
  EXE=$5
  OPT=$6
  CLK=$7
  P=$8
  F=$9
  V=${10}
  CS=${11}
  L1I="32kB"
  L1D="64kB"
  L2="256kB"
  L3="16MB"
  
  echo "
$GEM5_ROOT/build/X86/gem5.opt \
--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
--mcpat_enable \
--mcpat_path=${PREDICT_T_ROOT}/mcpat \
--mcpat_out=${OUTPUT_ROOT}/mcpat_out \
--mcpat_testname=$TN \
--power_profile_start=${PS} \
--power_profile_duration=${DUR} \
--power_profile_interval=${INT} \
--ncverilog_enable \
--ncverilog_warmup=10 \
--ncverilog_path=${PREDICT_T_ROOT}/circuit_model \
--power-supply-type=$P \
../gem5/configs/example/se.py \
--cmd=testbin/${EXE} \
--opt=\"${OPT}\" \
--power_profile_interval=100 \
--power_profile_initial_stats_interval=${INT} \
--power_pred_cpu_cycles=${CS} \
--power_pred_cpu_freq=${F} \
--power_pred_voltage=${V} \
--power_pred_voltage_emergency=0.95 \
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
--sys-clock=$CLK \
--mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &"
  #--debug-flags=StatEvent \
  #gdb --args $GEM5_ROOT/build/X86/gem5.opt \
    #--ncverilog_feedback \
  time $GEM5_ROOT/build/X86/gem5.opt \
    --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
    --mcpat_enable \
    --mcpat_path=${MCPAT_ROOT} \
    --mcpat_out=${OUTPUT_ROOT}/mcpat_out \
    --mcpat_testname=$TN \
    --power_profile_start=${PS} \
    --power_profile_duration=${DUR} \
    --power_profile_interval=${INT} \
    --ncverilog_enable \
    --ncverilog_warmup=10 \
    --ncverilog_path=${PREDICT_T_ROOT}/circuit_model \
    --power-supply-type=$P \
    $GEM5_ROOT/configs/example/se.py \
    --cmd=$PREDICT_T_ROOT/testbin/${EXE} \
    --opt="${OPT}" \
    --power_profile_interval=100 \
    --power_profile_initial_stats_interval=${INT} \
    --power_pred_cpu_cycles=${CS} \
    --power_pred_cpu_freq=${F} \
    --power_pred_voltage=${V} \
    --power_pred_voltage_emergency=0.95 \
    --power_pred_type=Test \
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

#------------------------------------------------------------------------------
# se_sc_classic_mc_ncv_debug
#   Syscall Emulation with Single Core, Classic Caches, and McPAT+NCVERILOG
#------------------------------------------------------------------------------
se_sc_classic_mc_ncv_debug() {
  TN=$1
  DUR=$2
  INT=$3
  PS=$4
  EXE=$5
  OPT=$6
  CLK=$7
  P=$8
  F=$9
  V=${10}
  CS=${11}
  L1I="32kB"
  L1D="64kB"
  L2="256kB"
  L3="16MB"
  
  echo "
$GEM5_ROOT/build/X86/gem5.opt \
--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
--mcpat_enable \
--mcpat_path=${PREDICT_T_ROOT}/mcpat \
--mcpat_out=${OUTPUT_ROOT}/mcpat_out \
--mcpat_testname=$TN \
--power_profile_start=${PS} \
--power_profile_duration=${DUR} \
--power_profile_interval=${INT} \
--ncverilog_enable \
--ncverilog_warmup=10 \
--ncverilog_path=${PREDICT_T_ROOT}/circuit_model \
--power-supply-type=$P \
../gem5/configs/example/se.py \
--cmd=testbin/${EXE} \
--opt=\"${OPT}\" \
--power_profile_interval=100 \
--power_profile_initial_stats_interval=${INT} \
--power_pred_cpu_cycles=${CS} \
--power_pred_cpu_freq=${F} \
--power_pred_voltage=${V} \
--power_pred_voltage_emergency=0.95 \
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
--sys-clock=$CLK \
--mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &"
  #gdb --args $GEM5_ROOT/build/X86/gem5.debug \
    #--ncverilog_feedback \
  gdb --args $GEM5_ROOT/build/X86/gem5.debug \
    --debug-flags=StatEvent \
    --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
    --mcpat_enable \
    --mcpat_path=${MCPAT_ROOT} \
    --mcpat_out=${OUTPUT_ROOT}/mcpat_out \
    --mcpat_testname=$TN \
    --power_profile_start=${PS} \
    --power_profile_duration=${DUR} \
    --power_profile_interval=${INT} \
    --ncverilog_enable \
    --ncverilog_warmup=10 \
    --ncverilog_path=${PREDICT_T_ROOT}/circuit_model \
    --power-supply-type=$P \
    $GEM5_ROOT/configs/example/se.py \
    --cmd=$PREDICT_T_ROOT/testbin/${EXE} \
    --opt="${OPT}" \
    --power_profile_interval=100 \
    --power_profile_initial_stats_interval=${INT} \
    --power_pred_type=IdealSensor \
    --power_pred_cpu_cycles=${CS} \
    --power_pred_cpu_freq=${F} \
    --power_pred_voltage=${V} \
    --power_pred_voltage_emergency=0.95 \
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
    --mem-size=8GB
}

#------------------------------------------------------------------------------
# se_mc_classic_mc_ncv
#   Syscall Emulation with Multiple Cores, Classic Caches, and McPAT+NCVERILOG
#------------------------------------------------------------------------------
se_mc_classic_mc_ncv() {
  TN=$1
  DUR=$2
  INT=$3
  S=$4
  PS=$5
  EXE=$6
  OPT=$7
  NPROC=$8
  CLK=$9
  L1I="32kB"
  L1D="64kB"
  L2="256kB"
  L3="16MB"

#  --power_pred_type=TestPowerPredictor \
#  --power_pred_table_size=${TABLE_SIZE[$l]} \
#  --power_pred_pc_start=${PC_START[$m]} \
#  --power_pred_history_size=${HISTORY_SIZE[$o]} \
  
  echo "
../gem5/build/X86/gem5.opt \
--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
--mcpat_enable \
--mcpat_path=${PREDICT_T_ROOT}/mcpat \
--mcpat_out=${OUTPUT_ROOT}/mcpat_out \
--mcpat_testname=$TN \
--power_profile_start=${PS} \
--power_profile_duration=${DUR} \
--power_profile_interval=${INT} \
--ncverilog_enable \
--ncverilog_path=${PREDICT_T_ROOT}/package_model \
--ncverilog_step=${S} \
../gem5/configs/example/se.py \
--cmd=testbin/${EXE} \
--opt=\"${OPT}\" \
--power_profile_interval=${INT} \
--num-cpus=$NPROC \
--cpu-type=DerivO3CPU \
--l1i_size=${L1I} \
--l1i-hwp-type=TaggedPrefetcher \
--l1d_size=${L1D} \
--l1d-hwp-type=TaggedPrefetcher \
--l2cache \
--num-l2caches=$NPROC \
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
    --mcpat_enable \
    --mcpat_path=${PREDICT_T_ROOT}/mcpat \
    --mcpat_out=${OUTPUT_ROOT}/mcpat_out \
    --mcpat_testname=$TN \
    --power_profile_start=${PS} \
    --power_profile_duration=${DUR} \
    --power_profile_interval=${INT} \
    --ncverilog_enable \
    --ncverilog_path=${PREDICT_T_ROOT}/package_model \
    --ncverilog_step=${S} \
    ../gem5/configs/example/se.py \
    --cmd=testbin/${EXE} \
    --opt="${OPT}" \
    --power_profile_interval=${INT} \
    --num-cpus=$NPROC \
    --cpu-type=DerivO3CPU \
    --l1i_size=${L1I} \
    --l1i-hwp-type=TaggedPrefetcher \
    --l1d_size=${L1D} \
    --l1d-hwp-type=TaggedPrefetcher \
    --l2cache \
    --num-l2caches=$NPROC \
    --l2_size=${L2} \
    --l2-hwp-type=TaggedPrefetcher \
    --l3cache \
    --l3_size=${L3} \
    --l3-hwp-type=TaggedPrefetcher \
    --caches \
    --sys-clock=$CLK \
    --mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &
}



#------------------------------------------------------------------------------
# se_mc_classic_nmc_nncv
#   Syscall Emulation with Multiple Cores, Classic Caches, and No McPAT, No
#   NCVERILOG
#------------------------------------------------------------------------------
se_mc_classic_nmc_nncv() {
  TN=$1
  EXE=$2
  OPT=$3
  NPROC=$4
  CLK=$5
  L1I="32kB"
  L1D="64kB"
  L2="256kB"
  L3="16MB"
  
  echo "
$GEM5_ROOT/build/X86/gem5.opt \
--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
../gem5/configs/example/se.py \
--cmd=testbin/${EXE} \
--opt=\"${OPT}\" \
--num-cpus=$NPROC \
--cpu-type=DerivO3CPU \
--l1i_size=${L1I} \
--l1i-hwp-type=TaggedPrefetcher \
--l1d_size=${L1D} \
--l1d-hwp-type=TaggedPrefetcher \
--l2cache \
--num-l2caches=$NPROC \
--l2_size=${L2} \
--l2-hwp-type=TaggedPrefetcher \
--l3cache \
--l3_size=${L3} \
--l3-hwp-type=TaggedPrefetcher \
--caches \
--sys-clock=$CLK \
--mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &"
  $GEM5_ROOT/build/X86/gem5.opt \
    --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
    $GEM5_ROOT/configs/example/se.py \
    --cmd=$PREDICT_T_ROOT/testbin/${EXE} \
    --opt="${OPT}" \
    --num-cpus=$NPROC \
    --cpu-type=DerivO3CPU \
    --l1i_size=${L1I} \
    --l1i-hwp-type=TaggedPrefetcher \
    --l1d_size=${L1D} \
    --l1d-hwp-type=TaggedPrefetcher \
    --l2cache \
    --num-l2caches=$NPROC \
    --l2_size=${L2} \
    --l2-hwp-type=TaggedPrefetcher \
    --l3cache \
    --l3_size=${L3} \
    --l3-hwp-type=TaggedPrefetcher \
    --caches \
    --sys-clock=$CLK \
    --mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &
}



#------------------------------------------------------------------------------
# se_mc_ruby_nmc_nncv
#   Syscall Emulation with Multiple Cores, Ruby MESI_Three_Level Caches, and
#   No McPAT, No NCVERILOG
#------------------------------------------------------------------------------
se_mc_ruby_nmc_nncv() {
  TN=$1
  EXE=$2
  OPT=$3
  NPROC=$4
  CLK=$5
  L1I="32kB"
  L1D="64kB"
  L2="256kB"
  L3="16MB"
  
  echo "
$GEM5_ROOT/build/X86_MESI_Three_Level/gem5.opt \
--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
../gem5/configs/example/se.py \
--cmd=testbin/${EXE} \
--opt=\"${OPT}\" \
--num-cpus=$NPROC \
--cpu-type=DerivO3CPU \
--ruby \
--l0i_size=${L1I} \
--l0d_size=${L1D} \
--l1_size=${L2} \
--l2_size=${L3} \
--sys-clock=$CLK \
--mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &"
  $GEM5_ROOT/build/X86_MESI_Three_Level/gem5.opt \
    --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
    $GEM5_ROOT/configs/example/se.py \
    --cmd=$PREDICT_T_ROOT/testbin/${EXE} \
    --opt="${OPT}" \
    --num-cpus=$NPROC \
    --cpu-type=DerivO3CPU \
    --ruby \
    --l0i_size=${L1I} \
    --l0d_size=${L1D} \
    --l1_size=${L2} \
    --l2_size=${L3} \
    --sys-clock=$CLK \
    --mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &
}



#------------------------------------------------------------------------------
# se_mc_ruby_nmc_nncv_debug
#   Syscall Emulation with Multiple Cores, Ruby MESI_Three_Level Caches, and
#   No McPAT, No NCVERILOG, Run in GDB
#------------------------------------------------------------------------------
se_mc_ruby_nmc_nncv_debug() {
  TN=$1
  EXE=$2
  OPT=$3
  NPROC=$4
  CLK=$5
  L1I="32kB"
  L1D="64kB"
  L2="256kB"
  L3="16MB"
  
  echo "
gdb --args $GEM5_ROOT/build/X86_MESI_Three_Level/gem5.debug \
--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
../gem5/configs/example/se.py \
--cmd=testbin/${EXE} \
--opt=\"${OPT}\" \
--num-cpus=$NPROC \
--cpu-type=DerivO3CPU \
--ruby \
--l0i_size=${L1I} \
--l0d_size=${L1D} \
--l1_size=${L2} \
--l2_size=${L3} \
--sys-clock=$CLK \
--mem-size=8GB"
gdb --args \
  $GEM5_ROOT/build/X86_MESI_Three_Level/gem5.debug \
  --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
  $GEM5_ROOT/configs/example/se.py \
  --cmd=$PREDICT_T_ROOT/testbin/${EXE} \
  --opt="${OPT}" \
  --num-cpus=$NPROC \
  --cpu-type=DerivO3CPU \
  --ruby \
  --l0i_size=${L1I} \
  --l0d_size=${L1D} \
  --l1_size=${L2} \
  --l2_size=${L3} \
  --sys-clock=$CLK \
  --mem-size=8GB
}
