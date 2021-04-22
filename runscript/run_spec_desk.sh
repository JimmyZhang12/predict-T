
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

script_name="run_spec_desk.sh"

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
DURATION=("150") # Data Points to Simulate
START_DELAY=("10000000")
# Stat Dump Cycles
CPU_CYCLES=("1000000")

## When to start ROI, in Sim Ticks, -or- ROI by setting "-1"
PROFILE_START=("-1") #TODO this doesnt do anything right now
INSTRUCTIONS=("-1") #TODO nor this?


#---------------------------------------------------
# Device Params:
#---------------------------------------------------
# All: 

# Desktop:
DEVICE_TYPE=("DESKTOP")
McPAT_DEVICE_TYPE=("0")
McPAT_SCALE_FACTOR=("1.0") # This is a HACK, Fix McPAT to support < 22nm planar
NUM_CORES=("1")

VOLTAGE=("1.4")
VOLTAGE_EMERGENCY=("1.3")
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

# Desktop:
L1D=("64kB")
L1I=("32kB")
L2=("256kB")
L3=("16MB")

#---------------------------------------------------
# Predictor Params:
#---------------------------------------------------

PREDICTOR=(
"HarvardPowerPredictorMitigation"
# "HarvardPowerPredictor"
# "IdealSensor"
# "IdealSensorHarvardMitigation"
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
THROTTLE_CLK=$(echo "scale=30;2*10^9" | bc)
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
name=(
	"459.GemsFDTD" \
)

dir=(
	"$HOME/passat/spec2006/benchspec/CPU2006/459.GemsFDTD/run/run_base_ref_amd64-m64-gcc43-nn.0000/" \
)

cmd=(
	"GemsFDTD_base.amd64-m64-gcc43-nn" \
)

opt=(
	"" \
)

stdin=(
	"" \
)




#---------------------------------------------------
# PDN PARAMS:
#---------------------------------------------------

L=$(echo "scale=30;20*10^-12" | bc)
C=$(echo "scale=30;1.32*10^-6" | bc)
R=$(echo "scale=30;3.2*10^-3" | bc)

# L=$(echo "scale=30;20*10^-12" | bc)
# R=$(echo "scale=30;1.32*10^-6" | bc)
# C=$(echo "scale=30;3.2*10^-3" | bc)

# L=$(echo "scale=30;30*10^-12" | bc)
# R=$(echo "scale=30;2.32*10^-6" | bc)
# C=$(echo "scale=30;3.2*10^-3" | bc)

#--------------------------------------------------------------------
# Run
#--------------------------------------------------------------------
for j in ${!name[@]}; do 
  for pred in ${!PREDICTOR[@]}; do
  	cd ${dir[$j]}

    sleep 10
    TN="${name[$j]}_${DURATION}_${CPU_CYCLES}_${DEVICE_TYPE}_${PREDICTOR[$pred]}"
    echo $TN

    se_classic_mc_ncv_spec \
        $TN \
        ${DURATION} \
        ${INSTRUCTIONS} \
        ${PROFILE_START} \
        ${cmd[$j]} \
        "${opt[$j]}" \
        ${CLK} \
        ${PDN} \
        ${CLK_} \
        ${VOLTAGE} \
        ${CPU_CYCLES[0]} \
        ${PREDICTOR[$pred]} \
        ${NUM_CORES} \
        ${L1I} \
        ${L1D} \
        ${L2} \
        ${L3} \
        ${CORE_WIDTH} \
        ${FETCH_BUFFER_SIZE} \
        ${FETCH_QUEUE_SIZE} \
        ${LOAD_QUEUE_SIZE} \
        ${STORE_QUEUE_SIZE} \
        ${NUM_ROB} \
        ${NUM_ROB_ENTRIES} \
        ${INT_PHYS_REGS} \
        ${FP_PHYS_REGS} \
        ${VEC_PHYS_REGS} \
        ${VEC_PRED_PHYS_REGS} \
        ${INSTR_QUEUE_SIZE} \
        ${INT_ALU_COUNT} \
        ${INT_MULT_DIV_COUNT} \
        ${FP_ALU_COUNT} \
        ${FP_MULT_DIV_COUNT} \
        ${SIMD_UNIT_COUNT} \
        ${McPAT_DEVICE_TYPE} \
        ${McPAT_SCALE_FACTOR} \
        ${PPRED_TRAINED_MODEL[$pred]} \
        ${PPRED_EVENTS[$pred]} \
        ${PPRED_ACTIONS[$pred]} \
        ${VOLTAGE_EMERGENCY} \
        ${VOLTAGE_THRESHOLD} \
        ${L} \
        ${C} \
        ${R} \
        ${START_DELAY} \
        ${THROTTLE_CLK} \
        ${stdin[$j]} \


    while [ `jobs | wc -l` -ge 6 ]; do
      sleep 1
    done
  done
done

while [ `jobs | wc -l` -ne  1 ]; do
  sleep 1
done

