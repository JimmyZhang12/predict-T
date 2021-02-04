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
# se_classic_mc_ncv
#   Syscall Emulation, Classic Caches, and McPAT+NCVERILOG
#------------------------------------------------------------------------------
se_classic_mc_ncv() {
  TN=$1
  DUR=$2
  INSTRS=$3
  PS=$4
  EXE=$5
  OPT=$6
  CLK=$7
  P=$8
  F=${9}
  V=${10}
  CS=${11}
  PRED=${12}
  NCORE=${13}
  L1I_=${14}
  L1D_=${15}
  L2_=${16}
  L3_=${17}
  CW=${18}     # Core Width (8)
  FBS=${19}    # Fetch Buffer Size (64)
  FQS=${20}    # Fetch Queue Size (32)
  LQS=${21}    # Load Queue Size (32)
  SQS=${22}    # Store Queue Size (32)
  NROB=${23}   # Num Reorder Buffers (1)
  NROBE=${24}  # Num ROB Entries (192)
  NIPR=${25}   # Num Integer Physical Registers (256)
  NFPPR=${26}  # Num FP Physical Registers (256)
  NVR=${27}    # Num Vector Physical Registers (256)
  NVPR=${28}   # Num Vector Pred Physical Registers (32)
  IQS=${29}    # Instruction Queue Size (64)
  IALUC=${30}  # Integer ALU Count (6)
  IMDC=${31}   # Integer Multiply Divide Unit Count (4)
  FPALUC=${32} # FP ALU Count (4)
  FPMDC=${33}  # FP Multiply Divide Unit Count (2)
  SIMDC=${34}  # SIMD Unit Count (2)
  MPDT=${35}   # McPAT Device Type, [0,1,2]
  MPSF=${36}   # McPAT Scaling Factor, HACK, Make MCPAT natively support < 22nm
  PTM=${37}    # Path to Pretrained Power Predictor Model
  PPEVENT=${38} # Num Events in DNN/Perceptron/Perceptron UTA
  PPACTION=${39} # Num Actions in DNN/Perceptron
  PPVE=${40}   # Voltage Emergency Level
  PPVTH=${41}  # Voltage Threshold Level; applies to sensor predictor
  L=${42}
  C=${43}
  R=${44}

  echo "RUNNING: "${TEST}/${EXE} 

  time $GEM5_ROOT/build/X86/gem5.opt \
    --write_stripped_stats \
    --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
    --mcpat_enable \
    --mcpat_path=${MCPAT_ROOT} \
    --mcpat_out=${OUTPUT_ROOT}/mcpat_out \
    --mcpat_testname=$TN \
    --mcpat_device_type=$MPDT \
    --mcpat_use_fg_pg \
    --mcpat_save_space \
    --mcpat_scale_factor=$MPSF \
    --power_profile_start=${PS} \
    --power_profile_duration=${DUR} \
    --power_profile_instrs=${INSTRS} \
    --ncverilog_enable \
    --ncverilog_warmup=10 \
    --ncverilog_path=${PREDICT_T_ROOT}/circuit_model \
    --power-supply-type=$P \
    --pdn_L=${L} \
    --pdn_C=${C} \
    --pdn_R=${R} \
    --pdn_VDC=${V} \
    --pdn_CLK=${F} \
    $GEM5_ROOT/configs/example/se.py \
    --cmd=${TEST}/${EXE} \
    --opt="${OPT}" \
    --power_pred_cpu_cycles=${CS} \
    --power_pred_cpu_freq=${F} \
    --power_pred_voltage=${V} \
    --power_pred_voltage_emergency=${PPVE} \
    --power_pred_voltage_threshold=${PPVTH} \
    --power_pred_type=${PRED} \
    --power_pred_train_name=${TRAINING_ROOT}/${TN}.csv \
    --power_pred_model=${PTM} \
    --power_pred_events=${PPEVENT} \
    --power_pred_actions=${PPACTION} \
    --num-cpus=${NCORE} \
    --cpu_superscalar_width=$CW \
    --cpu_fetch_buffer_size=$FBS \
    --cpu_fetch_q_size=$FQS \
    --cpu_lq_size=$LQS \
    --cpu_sq_size=$SQS \
    --cpu_num_robs=$NROB \
    --cpu_num_rob_entries=$NROBE \
    --cpu_phys_int_regs=$NIPR \
    --cpu_phys_fp_regs=$NFPPR \
    --cpu_phys_vec_regs=$NVR \
    --cpu_phys_vec_pred_regs=$NVPR \
    --cpu_num_iq_entries=$IQS \
    --cpu_intALUcount=$IALUC \
    --cpu_intMULDIVcount=$IMDC \
    --cpu_fpALUcount=$FPALUC \
    --cpu_fpMULDIVcount=$FPMDC \
    --cpu_simdcount=$SIMDC \
    --cpu-type=DerivO3CPU \
    --l1i_size=${L1I_} \
    --l1d_size=${L1D_} \
    --l2cache \
    --num-l2caches=${NCORE} \
    --l2_size=${L2_} \
    --l3cache \
    --l3_size=${L3_} \
    --caches \
    --sys-clock=${CLK} \
    --mem-size=8GB #> ${OUTPUT_ROOT}/text_out/$TN.out &
}

se_classic_mc_ncv_spec() {
  TN=$1
  DUR=$2
  INSTRS=$3
  PS=$4
  CMD=$5
  OPT=$6
  CLK=$7
  P=$8
  F=${9}
  V=${10}
  CS=${11}
  PRED=${12}
  NCORE=${13}
  L1I_=${14}
  L1D_=${15}
  L2_=${16}
  L3_=${17}
  CW=${18}     # Core Width (8)
  FBS=${19}    # Fetch Buffer Size (64)
  FQS=${20}    # Fetch Queue Size (32)
  LQS=${21}    # Load Queue Size (32)
  SQS=${22}    # Store Queue Size (32)
  NROB=${23}   # Num Reorder Buffers (1)
  NROBE=${24}  # Num ROB Entries (192)
  NIPR=${25}   # Num Integer Physical Registers (256)
  NFPPR=${26}  # Num FP Physical Registers (256)
  NVR=${27}    # Num Vector Physical Registers (256)
  NVPR=${28}   # Num Vector Pred Physical Registers (32)
  IQS=${29}    # Instruction Queue Size (64)
  IALUC=${30}  # Integer ALU Count (6)
  IMDC=${31}   # Integer Multiply Divide Unit Count (4)
  FPALUC=${32} # FP ALU Count (4)
  FPMDC=${33}  # FP Multiply Divide Unit Count (2)
  SIMDC=${34}  # SIMD Unit Count (2)
  MPDT=${35}   # McPAT Device Type, [0,1,2]
  MPSF=${36}   # McPAT Scaling Factor, HACK, Make MCPAT natively support < 22nm
  PTM=${37}    # Path to Pretrained Power Predictor Model
  PPEVENT=${38} # Num Events in DNN/Perceptron/Perceptron UTA
  PPACTION=${39} # Num Actions in DNN/Perceptron
  PPVE=${40}   # Voltage Emergency Level
  PPVTH=${41}  # Voltage Threshold Level; applies to sensor predictor
  STDIN=${42}
  STDOUT=${43}

  
  #--debug-flags=StatEvent \
    #--ncverilog_feedback \
  #gdb --args $GEM5_ROOT/build/X86/gem5.debug \
  time $GEM5_ROOT/build/X86/gem5.opt \
    --write_stripped_stats \
    --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
    --mcpat_enable \
    --mcpat_path=${MCPAT_ROOT} \
    --mcpat_out=${OUTPUT_ROOT}/mcpat_out \
    --mcpat_testname=$TN \
    --mcpat_device_type=$MPDT \
    --mcpat_use_fg_pg \
    --mcpat_save_space \
    --mcpat_scale_factor=$MPSF \
    --power_profile_start=${PS} \
    --power_profile_duration=${DUR} \
    --power_profile_instrs=${INSTRS} \
    --ncverilog_enable \
    --ncverilog_warmup=10 \
    --ncverilog_path=${PREDICT_T_ROOT}/circuit_model \
    --power-supply-type=$P \
    $GEM5_ROOT/configs/example/se.py \
    --cmd=${CMD} \
    --opt="${OPT}" \
    --input="${STDIN}" \
    --output="${STOUT}" \
    --power_pred_cpu_cycles=${CS} \
    --power_pred_cpu_freq=${F} \
    --power_pred_voltage=${V} \
    --power_pred_voltage_emergency=${PPVE} \
    --power_pred_voltage_threshold=${PPVTH} \
    --power_pred_type=${PRED} \
    --power_pred_train_name=${TRAINING_ROOT}/${TN}.csv \
    --power_pred_model=${PTM} \
    --power_pred_events=${PPEVENT} \
    --power_pred_actions=${PPACTION} \
    --num-cpus=${NCORE} \
    --cpu_superscalar_width=$CW \
    --cpu_fetch_buffer_size=$FBS \
    --cpu_fetch_q_size=$FQS \
    --cpu_lq_size=$LQS \
    --cpu_sq_size=$SQS \
    --cpu_num_robs=$NROB \
    --cpu_num_rob_entries=$NROBE \
    --cpu_phys_int_regs=$NIPR \
    --cpu_phys_fp_regs=$NFPPR \
    --cpu_phys_vec_regs=$NVR \
    --cpu_phys_vec_pred_regs=$NVPR \
    --cpu_num_iq_entries=$IQS \
    --cpu_intALUcount=$IALUC \
    --cpu_intMULDIVcount=$IMDC \
    --cpu_fpALUcount=$FPALUC \
    --cpu_fpMULDIVcount=$FPMDC \
    --cpu_simdcount=$SIMDC \
    --cpu-type=DerivO3CPU \
    --l1i_size=${L1I_} \
    --l1d_size=${L1D_} \
    --l2cache \
    --num-l2caches=${NCORE} \
    --l2_size=${L2_} \
    --l3cache \
    --l3_size=${L3_} \
    --caches \
    --sys-clock=${CLK} \
    --mem-size=8GB #> ${OUTPUT_ROOT}/text_out/$TN.out &
}
