#!/bin/bash
# # Copyright (c) 2020 Andrew Smith
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all # copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

script_name="run_single.sh"

print_info () {
  green="\e[32m"
  nc="\e[0m"
  echo -e "$green[ $script_name ]$nc $1"
}

print_error () {
  red="\e[31m"
  nc="\e[0m"
  echo -e "$red[ $script_name ] Error:$nc $1"
  exit 1
}

#--------------------------------------------------------------------
# Check Environment
#--------------------------------------------------------------------
if [ -z "$VSIM_TOOLS" ]; then
  print_error "VSIM_TOOLS not set; source setup.sh"
  exit
fi
if [ -z "$PREDICT_T_ROOT" ]; then
  print_error "PREDICT_T_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$GEM5_ROOT" ]; then
  print_error "GEM5_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$OUTPUT_ROOT" ]; then
  print_error "OUTPUT_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$MCPAT_ROOT" ]; then
  print_error "OUTPUT_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$SIM_ROOT" ]; then
  print_error "SIM_ROOT not set; source setup.sh"
  exit 1
fi
if [ -z "$VSIM_IMAGE" ]; then print_error "VSIM_IMAGE not set; source setup.sh"
  exit 1
fi
print_info "VSIM_TOOLS $VSIM_TOOLS"
print_info "PREDICT_T_ROOT $PREDICT_T_ROOT"
print_info "GEM5_ROOT $GEM5_ROOT"
print_info "OUTPUT_ROOT $OUTPUT_ROOT"
print_info "MCPAT_ROOT $MCPAT_ROOT"
print_info "SIM_ROOT $SIM_ROOT"
print_info "VSIM_IMAGE $VSIM_IMAGE"

source $PREDICT_T_ROOT/runscript/util.sh

if [[ -z $(docker images -q $VSIM_IMAGE) ]]; then
  print_error "Docker container $VSIM_IMAGE is not built; source setup.sh"
  exit 1
fi

#--------------------------------------------------------------------
# Configure Test Specific Paths
#--------------------------------------------------------------------
TEST="$PREDICT_T_ROOT/testbin"
INPUT="$TEST/input"
OUTPUT="$TEST/output"
print_info "TEST $TEST"
print_info "INPUT $INPUT"
print_info "OUTPUT $OUTPUT"

TRAINING_ROOT="$OUTPUT_ROOT/training_data"
print_info "TRAINING_ROOT $TRAINING_ROOT"


#---------------------------------------------------
# Simulation Params
#---------------------------------------------------
# Configure Simulation Parameters
DURATION=("-1" "-1" "-1" "-1" "-1" "-1" "-1") # Data Points to Simulate
#INSTRUCTIONS=("10000" "25000" "25000" "25000" "25000" "25000" "25000") # Instructions to Simulate
INSTRUCTIONS=("10000" "10000" "10000" "10000" "10000" "10000")
# When to start ROI, in Sim Ticks, -or- ROI by setting "-1"
PROFILE_START=("-1" "-1" "-1" "-1" "-1" "-1" "-1") 

#DURATION=("-1") # Data Points to Simulate
#INSTRUCTIONS=("25000") # Instructions to Simulate
## When to start ROI, in Sim Ticks, -or- ROI by setting "-1"
#PROFILE_START=("-1") 

#---------------------------------------------------
# Device Params:
#---------------------------------------------------
# All: 

#DEVICE_TYPE=("MOBILE" "LAPTOP" "DESKTOP")
#McPAT_DEVICE_TYPE=("1" "1" "0")
#McPAT_SCALE_FACTOR=("0.5" "1.0" "1.0")
#NUM_CORES=("1" "1" "1")
#NUM_CORES=("4" "4" "8")
# Mobile:
#DEVICE_TYPE=("MOBILE")
#McPAT_DEVICE_TYPE=("1")
#McPAT_SCALE_FACTOR=("1") # This is a HACK, Fix McPAT to support < 22nm planar
#NUM_CORES=("1")
# Laptop:
#DEVICE_TYPE=("LAPTOP")
#McPAT_DEVICE_TYPE=("1")
#McPAT_SCALE_FACTOR=("1.0") # This is a HACK, Fix McPAT to support < 22nm planar
#NUM_CORES=("4")
# Desktop:
DEVICE_TYPE=("DESKTOP")
McPAT_DEVICE_TYPE=("0")
McPAT_SCALE_FACTOR=("1.0") # This is a HACK, Fix McPAT to support < 22nm planar
NUM_CORES=("1")

#VOLTAGE=("0.9" "1.2" "1.4")
#VOLTAGE_EMERGENCY=("0.873" "1.164" "1.358")
#VOLTAGE_THRESHOLD=("0.882" "1.176" "1.372")

VOLTAGE=("1.4")
VOLTAGE_EMERGENCY=("1.358")
VOLTAGE_THRESHOLD=("1.372")

#---------------------------------------------------
# Power Delivery Params
#---------------------------------------------------
#PDN=("ARM" "INTEL_M" "INTEL_DT")
#PDN=("HARVARD_M" "HARVARD_L" "HARVARD_D")
#PDN=("HARVARD")
PDN=("INTEL_DT")

#---------------------------------------------------
# Cache Params:
#---------------------------------------------------
# ALL:
#L1D=("4kB" "16kB" "64kB")
#L1I=("2kB" "8kB" "32kB")
#L2=("64kB" "128kB" "256kB")
#L3=("2MB" "8MB" "16MB")
# Mobile:
#L1D=("4kB")
#L1I=("2kB")
#L2=("64kB")
#L3=("2MB")
# Laptop:
#L1D=("16kB")
#L1I=("8kB")
#L2=("128kB")
#L3=("8MB")
# Desktop:
L1D=("64kB")
L1I=("32kB")
L2=("256kB")
L3=("16MB")

#---------------------------------------------------
# Predictor Params:
#---------------------------------------------------
# Stat Dump Cycles


PREDICTOR=(
#"IdealSensor" 
#"uArchEventPredictor" 
"HarvardPowerPredictor"
#"DecorOnly" 
)
#"DepAnalysis"
#"ThrottleAfterStall"
#"Test"
PPRED_TRAINED_MODEL=(
"bottom.txt"
"bottom.txt"
"bottom.txt"
"bottom.txt"
)
#"bottom.txt"
#"bottom.txt"
#"bottom.txt"
PPRED_EVENTS=(
"16"
"16"
"16"
"16"
)
#"16"
#"16"
#"16"
PPRED_ACTIONS=(
"1"
"1"
"1"
"1"
)
#"1"
#"1"
#"1"

#PREDICTOR=(
#"Test" 
#)
#PPRED_TRAINED_MODEL=(
#"bottom.txt"
#)
#PPRED_EVENTS=(
#"1"
#)
#PPRED_ACTIONS=(
#"1"
#)

#PREDICTOR=(
#"PerceptronPredictorUTA"
#"PerceptronPredictor"
#"PerceptronPredictor"
#"DNNPredictor"
#"DNNPredictor"
#)
## Bottom.txt is a meme; its ok for cringing
#PPRED_TRAINED_MODEL=(
#"bottom.txt"
#"${PREDICT_T_ROOT}/perceptron_DESKTOP_32_2_512_RAW.txt"
#"${PREDICT_T_ROOT}/perceptron_DESKTOP_32_8_512_RAW.txt"
#"${PREDICT_T_ROOT}/dnn_DESKTOP_32_2_1_32_8192_RAW.txt"
#"${PREDICT_T_ROOT}/dnn_DESKTOP_32_8_1_32_8192_STANDARDIZE.txt"
#)
#PPRED_EVENTS=(
#"16"
#"16"
#"16"
#"16"
#"16"
#)
#PPRED_ACTIONS=(
#"2"
#"2"
#"8"
#"2"
#"8"
#)

#---------------------------------------------------
# CPU Params:
#---------------------------------------------------
#CLK=( "3GHz"     "3.5GHz"     "4GHz")
#CLK_=("3000000000" "3500000000" "4000000000")
# Superscalar Core Width
#CORE_WIDTH=("6" "6" "8")
# Fetch Params
#FETCH_BUFFER_SIZE=("16" "32" "64")
#FETCH_QUEUE_SIZE=("8" "16" "32")
# LQ/SQ Size
#LOAD_QUEUE_SIZE=("8" "16" "32")
#STORE_QUEUE_SIZE=("8" "16" "32")
# ReorderBuffer Params
#NUM_ROB=("1" "1" "1")
#NUM_ROB_ENTRIES=("48" "96" "192")
# Regfile Params
#INT_PHYS_REGS=("64" "128" "256")
#3FP_PHYS_REGS=("64" "128" "256")
#VEC_PHYS_REGS=("64" "128" "256")
#VEC_PRED_PHYS_REGS=("8" "16" "32")
# Instruction Queue Size
#INSTR_QUEUE_SIZE=("16" "32" "64")
# Functional Unit Counts
#INT_ALU_COUNT=("6" "6" "8")
#INT_MULT_DIV_COUNT=("4" "4" "6")
#FP_ALU_COUNT=("2" "4" "6")
#FP_MULT_DIV_COUNT=("1" "2" "4")
#SIMD_UNIT_COUNT=("1" "2" "4")

# Mobile
#CLK=( "2.0GHz")
#CLK_=("2000000000")
## Superscalar Core Width
#CORE_WIDTH=("2")
## Fetch Params
#FETCH_BUFFER_SIZE=("16")
#FETCH_QUEUE_SIZE=("8")
## LQ/SQ Size
#LOAD_QUEUE_SIZE=("8")
#STORE_QUEUE_SIZE=("8")
## ReorderBuffer Params
#NUM_ROB=("1")
#NUM_ROB_ENTRIES=("48")
## Regfile Params
#INT_PHYS_REGS=("64")
#FP_PHYS_REGS=("64")
#VEC_PHYS_REGS=("64")
#VEC_PRED_PHYS_REGS=("8")
## Instruction Queue Size
#INSTR_QUEUE_SIZE=("16")
## Functional Unit Counts
#INT_ALU_COUNT=("6")
#INT_MULT_DIV_COUNT=("4")
#FP_ALU_COUNT=("2")
#FP_MULT_DIV_COUNT=("1")
#SIMD_UNIT_COUNT=("1")

# Laptop
#CLK=( "3.0GHz")
#CLK_=("3000000000")
## Superscalar Core Width
#CORE_WIDTH=("4")
## Fetch Params
#FETCH_BUFFER_SIZE=("32")
#FETCH_QUEUE_SIZE=("16")
## LQ/SQ Size
#LOAD_QUEUE_SIZE=("16")
#STORE_QUEUE_SIZE=("16")
## ReorderBuffer Params
#NUM_ROB=("1")
#NUM_ROB_ENTRIES=("96")
## Regfile Params
#INT_PHYS_REGS=("128")
#FP_PHYS_REGS=("128")
#VEC_PHYS_REGS=("128")
#VEC_PRED_PHYS_REGS=("16")
## Instruction Queue Size
#INSTR_QUEUE_SIZE=("32")
## Functional Unit Counts
#INT_ALU_COUNT=("6")
#INT_MULT_DIV_COUNT=("4")
#FP_ALU_COUNT=("4")
#FP_MULT_DIV_COUNT=("2")
#SIMD_UNIT_COUNT=("1")

# Desktop
CLK=( "4GHz")
CLK_=("4000000000")
## Superscalar Core Width
CORE_WIDTH=("8")
## Fetch Params
FETCH_BUFFER_SIZE=("64")
FETCH_QUEUE_SIZE=("32")
## LQ/SQ Size
LOAD_QUEUE_SIZE=("32")
STORE_QUEUE_SIZE=("32")
## ReorderBuffer Params
NUM_ROB=("1")
NUM_ROB_ENTRIES=("192")
## Regfile Params
INT_PHYS_REGS=("256")
FP_PHYS_REGS=("256")
VEC_PHYS_REGS=("256")
VEC_PRED_PHYS_REGS=("32")
## Instruction Queue Size
INSTR_QUEUE_SIZE=("64")
## Functional Unit Counts
INT_ALU_COUNT=("8")
INT_MULT_DIV_COUNT=("6")
FP_ALU_COUNT=("6")
FP_MULT_DIV_COUNT=("4")
SIMD_UNIT_COUNT=("4")

#---------------------------------------------------
# Test Executables:
#---------------------------------------------------
#name=("rijndael_encrypt" "dijkstra" "toast" "fft")
#exe=("rijndael" "dijkstra" "toast" "fft")
#opt=("${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/dijkstra.dat" "-fps -c ${INPUT}/toast.au" "4 4096")
#name=("basicmath" "bitcnts" "qsort" "susan_smooth" "susan_edge" "susan_corner" "dijkstra" "blowfish_encrypt" "blowfish_decrypt" "rijndael_encrypt" "rijndael_decrypt" "sha" "crc" "fft" "ffti" "toast" "untoast")
#exe=("basicmath" "bitcnts" "qsort" "susan" "susan" "susan" "dijkstra" "blowfish" "blowfish" "rijndael" "rijndael" "sha" "crc" "fft" "fft" "toast" "untoast")
#opt=("" "1000" "${INPUT}/qsort.dat" "${INPUT}/susan.pgm ${OUTPUT}/susan_s.pgm -s" "${INPUT}/susan.pgm ${OUTPUT}/susan_e.pgm -e" "${INPUT}/susan.pgm ${OUTPUT}/susan_c.pgm -c" "${INPUT}/dijkstra.dat" "e ${INPUT}/blowfish.asc ${OUTPUT}/blowfish.enc 1234567890abcdeffedcba0987654321" "d ${INPUT}/blowfish.enc ${OUTPUT}/blowfish.asc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/rijndael.enc ${OUTPUT}/rijndael.asc d 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/sha.asc" "${INPUT}/crc.pcm" "4 4096" "4 8192 -i" "-fps -c ${INPUT}/toast.au" "-fps -c ${INPUT}/untoast.au.run.gsm")
#name=("qsort" "dijkstra" "fft" "ffti" "sha" "toast" "untoast")
#exe=("qsort" "dijkstra" "fft" "fft" "sha" "toast" "untoast")
#opt=("${INPUT}/qsort.dat" "${INPUT}/dijkstra.dat" "4 4096" "4 8192 -i" "${INPUT}/sha.asc" "-fps -c ${INPUT}/toast.au" "-fps -c ${INPUT}/untoast.au.run.gsm")
#name=("qsort" "dijkstra")
#exe=("qsort" "dijkstra")
#opt=("${INPUT}/qsort.dat" "${INPUT}/dijkstra.dat")

#name=("susan_corner" "blowfish_encrypt" "rijndael_decrypt" "sha" "crc" "toast" "untoast")
#exe=("susan" "blowfish" "rijndael" "sha" "crc" "toast" "untoast")
#opt=("${INPUT}/susan.pgm ${OUTPUT}/susan_c.pgm -c" "e ${INPUT}/blowfish.asc ${OUTPUT}/blowfish.enc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/sha.asc" "${INPUT}/crc.pcm" "-fps -c ${INPUT}/toast.au" "-fps -c ${INPUT}/untoast.au.run.gsm")

#name=("susan_corner" "blowfish_encrypt" "rijndael_decrypt")
#exe=("susan" "blowfish" "rijndael")
#opt=("${INPUT}/susan.pgm ${OUTPUT}/susan_c.pgm -c" "e ${INPUT}/blowfish.asc ${OUTPUT}/blowfish.enc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321")

#name=("blowfish_encrypt" "rijndael_decrypt")
#exe=("blowfish" "rijndael")
#opt=("${INPUT}/blowfish.asc ${OUTPUT}/blowfish.enc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321")

#name=("sha" "crc" "toast" "untoast")
#exe=("sha" "crc" "toast" "untoast")
#opt=("${INPUT}/sha.asc" "${INPUT}/crc.pcm" "-fps -c ${INPUT}/toast.au" "-fps -c ${INPUT}/untoast.au.run.gsm")

name=("fft")
exe=("fft")
opt=("4 4096")

#name=("qsort") 
#exe=("qsort")
#opt=("${INPUT}/qsort.dat")

#name=("sha" "untoast")
#exe=("sha" "untoast")
#opt=("${INPUT}/sha.asc" "-fps -c ${INPUT}/untoast.au.run.gsm")
#name=("blowfish_encrypt")
#exe=("blowfish")
#opt=("e ${INPUT}/blowfish.asc ${OUTPUT}/blowfish.enc 1234567890abcdeffedcba0987654321")
#name=("fft")
#exe=("fft")
#opt=("4 4096")
#name=("rijndael_encrypt")
#exe=("rijndael")
#opt=("${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321")
#name=("toast"i)
#exe=("toast")
#opt=("-fps -c ${INPUT}/toast.au")
#name=("dijkstra")
#exe=("dijkstra")
#opt=("${INPUT}/dijkstra.dat")

#--------------------------------------------------------------------
# Run
#--------------------------------------------------------------------
for j in ${!name[@]}; do 
  for i in ${!DEVICE_TYPE[@]}; do
    for pred in ${!PREDICTOR[@]}; do
      for k in 
        sleep 10
        TN="${name[$j]}_${INSTRUCTIONS[$j]}_${CPU_CYCLES[0]}_${DEVICE_TYPE[$i]}_${PDN[$i]}_${PREDICTOR[$pred]}_${PPRED_ACTIONS[$pred]}_nodummy"
        se_classic_mc_ncv \
            $TN ${DURATION[$j]} \
            ${INSTRUCTIONS[$j]} \
            ${PROFILE_START[$j]} \
            ${exe[$j]} \
            "${opt[$j]}" \
            ${CLK[$i]} \
            ${PDN[$i]} \
            ${CLK_[$i]} \
            ${VOLTAGE[$i]} \
            ${CPU_CYCLES[0]} \
            ${PREDICTOR[$pred]} \
            ${NUM_CORES[$i]} \
            ${L1I[$i]} \
            ${L1D[$i]} \
            ${L2[$i]} \
            ${L3[$i]} \
            ${CORE_WIDTH[$i]} \
            ${FETCH_BUFFER_SIZE[$i]} \
            ${FETCH_QUEUE_SIZE[$i]} \
            ${LOAD_QUEUE_SIZE[$i]} \
            ${STORE_QUEUE_SIZE[$i]} \
            ${NUM_ROB[$i]} \
            ${NUM_ROB_ENTRIES[$i]} \
            ${INT_PHYS_REGS[$i]} \
            ${FP_PHYS_REGS[$i]} \
            ${VEC_PHYS_REGS[$i]} \
            ${VEC_PRED_PHYS_REGS[$i]} \
            ${INSTR_QUEUE_SIZE[$i]} \
            ${INT_ALU_COUNT[$i]} \
            ${INT_MULT_DIV_COUNT[$i]} \
            ${FP_ALU_COUNT[$i]} \
            ${FP_MULT_DIV_COUNT[$i]} \
            ${SIMD_UNIT_COUNT[$i]} \
            ${McPAT_DEVICE_TYPE[$i]} \
            ${McPAT_SCALE_FACTOR[$i]} \
            ${PPRED_TRAINED_MODEL[$pred]} \
            ${PPRED_EVENTS[$pred]} \
            ${PPRED_ACTIONS[$pred]} \
            ${VOLTAGE_EMERGENCY[$i]} \
            ${VOLTAGE_THRESHOLD[$i]}
      while [ `jobs | wc -l` -ge 9 ]; do
        sleep 1
      done
    done
  done
done

while [ `jobs | wc -l` -ne 1 ]; do
  sleep 1
done