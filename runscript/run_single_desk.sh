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
  print_error "MCPAT not set; source setup.sh"
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
DURATION=("10") # Data Points to Simulate
START_DELAY=("1000000") # delay power simulation by this many cycles (-1 to start on pseudo instr is NOT WORKING)
CPU_CYCLES=("100000") # Stat Dump Cycles

#TODO jimmy figure what these do now
## When to start ROI, in Sim Ticks, -or- ROI by setting "-1"
PROFILE_START=("-1") 
INSTRUCTIONS=("-1")

#---------------------------------------------------
# Device Params:
#---------------------------------------------------
# Desktop:
DEVICE_TYPE=("DESKTOP")
McPAT_DEVICE_TYPE=("0")
McPAT_SCALE_FACTOR=("1.0") # This is a HACK, Fix McPAT to support < 22nm planar
NUM_CORES=("1")

VOLTAGE=("1.4")
VOLTAGE_EMERGENCY=("1.35")
VOLTAGE_THRESHOLD=("1.372")

#---------------------------------------------------
# Power Delivery Params
#---------------------------------------------------
PDN=("INTEL_DT") #TODO old framework, currently does nothing

#---------------------------------------------------
# Cache Params:
#---------------------------------------------------
L1D=("64kB")
L1I=("32kB")
L2=("256kB")
L3=("16MB")

#---------------------------------------------------
# Predictor Params:
#---------------------------------------------------

PREDICTOR=(
# "HarvardPowerPredictorMitigation"
"HarvardPowerPredictor"

)

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

#---------------------------------------------------
# CPU Params:
#---------------------------------------------------
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

# name=("basicmath" "bitcnts" "qsort" "susan_smooth" "susan_edge" "susan_corner" "dijkstra" "blowfish_encrypt" "blowfish_decrypt" "rijndael_encrypt" "rijndael_decrypt" "sha" "crc" "fft" "ffti" "toast" "untoast")
# exe=("basicmath" "bitcnts" "qsort" "susan" "susan" "susan" "dijkstra" "blowfish" "blowfish" "rijndael" "rijndael" "sha" "crc" "fft" "fft" "toast" "untoast")
# opt=("" "1000" "${INPUT}/qsort.dat" "${INPUT}/susan.pgm ${OUTPUT}/susan_s.pgm -s" "${INPUT}/susan.pgm ${OUTPUT}/susan_e.pgm -e" "${INPUT}/susan.pgm ${OUTPUT}/susan_c.pgm -c" "${INPUT}/dijkstra.dat" "e ${INPUT}/blowfish.asc ${OUTPUT}/blowfish.enc 1234567890abcdeffedcba0987654321" "d ${INPUT}/blowfish.enc ${OUTPUT}/blowfish.asc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/rijndael.enc ${OUTPUT}/rijndael.asc d 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/sha.asc" "${INPUT}/crc.pcm" "4 4096" "4 8192 -i" "-fps -c ${INPUT}/toast.au" "-fps -c ${INPUT}/untoast.au.run.gsm")

#name=("qsort" "dijkstra" "fft" "ffti" "sha" "toast" "untoast")
#exe=("qsort" "dijkstra" "fft" "fft" "sha" "toast" "untoast")
#opt=("${INPUT}/qsort.dat" "${INPUT}/dijkstra.dat" "4 4096" "4 8192 -i" "${INPUT}/sha.asc" "-fps -c ${INPUT}/toast.au" "-fps -c ${INPUT}/untoast.au.run.gsm")
#name=("qsort" "dijkstra")
#exe=("qsort" "dijkstra")
#opt=("${INPUT}/qsort.dat" "${INPUT}/dijkstra.dat")

#name=( "blowfish_encrypt" "rijndael_decrypt" "sha" "crc" "toast" "untoast")
#exe=("blowfish" "rijndael" "sha" "crc" "toast" "untoast")
#opt=("e ${INPUT}/blowfish.asc ${OUTPUT}/blowfish.enc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/sha.asc" "${INPUT}/crc.pcm" "-fps -c ${INPUT}/toast.au" "-fps -c ${INPUT}/untoast.au.run.gsm")

#name=("susan_corner" "blowfish_encrypt" "rijndael_decrypt")
#exe=("susan" "blowfish" "rijndael")
#opt=("${INPUT}/susan.pgm ${OUTPUT}/susan_c.pgm -c" "e ${INPUT}/blowfish.asc ${OUTPUT}/blowfish.enc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321")

#name=("blowfish_encrypt" "rijndael_decrypt")
#exe=("blowfish" "rijndael")
#opt=("${INPUT}/blowfish.asc ${OUTPUT}/blowfish.enc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321")

#name=("toast")
#exe=("toast")
#opt=("-fps -c ${INPUT}/toast.au")

# name=("crc") 
# exe=("crc")
# opt=("${INPUT}/crc.pcm")

# name=("fft")
# exe=("fft")
# opt=("4 4096")

name=("qsort")
exe=("qsort")
opt=("${INPUT}/qsort.dat")


#name=("different_cycle" "same_cycle") 
#exe=("different_cycle" "same_cycle")
#opt=("" "")

#name=("same_cycle") 
#exe=("same_cycle")
#opt=("")


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

#---------------------------------------------------
# PDN PARAMS:
#---------------------------------------------------

L=$(echo "scale=15;20*10^-12" | bc)
R=$(echo "scale=15;1.32*10^-6" | bc)
C=$(echo "scale=15;3.2*10^-3" | bc)

#--------------------------------------------------------------------
# Run
#--------------------------------------------------------------------
for j in ${!name[@]}; do 
  for i in ${!DEVICE_TYPE[@]}; do
    for pred in ${!PREDICTOR[@]}; do
      sleep 10
      TN="${name[$j]}_${DURATION}_${CPU_CYCLES}_${DEVICE_TYPE}_${PREDICTOR[$pred]}"
      echo $TN
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
          ${VOLTAGE_THRESHOLD[$i]} \
          ${L} \
          ${C} \
          ${R} \
          ${START_DELAY[0]}
          

      while [ `jobs | wc -l` -ge 4 ]; do
        sleep 1
      done
    done
  done
done

while [ `jobs | wc -l` -ne 1 ]; do
  sleep 1
done
