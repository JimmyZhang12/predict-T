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
if [ -z "$VSIM_IMAGE" ]; then
  print_error "VSIM_IMAGE not set; source setup.sh"
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
print_info "INPUT $OUTPUT"


#--------------------------------------------------------------------
# Configure Simulation Parameters
#--------------------------------------------------------------------
DURATION=("-1") # Data Points to Simulate
INSTRUCTIONS=("10000") # Instructions to Simulate
INTERVAL=("10000") # Sim Cycles
ROI_INTERVAL=("100")
# When to start ROI, in Sim Ticks, -or- ROI by setting "-1"
PROFILE_START=("-1") 
# Power Distribution Network Type:
PDN=("HARVARD")
#PREDICTOR=("DecorOnly" "uArchEventPredictor")
#PREDICTOR=("IdealSensor" "Test")
#PREDICTOR=("IdealSensor" "Test" "DecorOnly" "uArchEventPredictor")
#PREDICTOR=("IdealSensor" "DecorOnly" "uArchEventPredictor")
PREDICTOR=("HarvardPowerPredictor")
#PREDICTOR=("Test")

VOLTAGE="1.0"
CPU_CYCLES=("10")

L1D=("64kB")
L1I=("32kB")
L2=("256kB")
L3=("16MB")
#CLK=( "3.5GHz")
#CLK_=("3500000000")
CLK=( "3.0GHz"     "4.0GHz")
CLK_=("3000000000" "4000000000")
CID=( "3"          "4")
#CLK=( "4.0GHz")
#CLK_=("4000000000")
#CID=( "4")

name=("rijndael_encrypt" "dijkstra" "toast" "fft")
exe=("rijndael" "dijkstra" "toast" "fft")
opt=("${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/dijkstra.dat" "-fps -c ${INPUT}/toast.au" "4 4096")
#name=("fft")
#exe=("fft")
#opt=("4 4096")
#name=("rijndael_encrypt")
#exe=("rijndael")
#opt=("${INPUT}/rijndael.asc ${OUTPUT}/rijndael.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321")
#name=("toast")
#exe=("toast")
#opt=("-fps -c ${INPUT}/toast.au")

#--------------------------------------------------------------------
# Run
#--------------------------------------------------------------------
for j in ${!name[@]}; do 
  for i in ${!DURATION[@]}; do 
    for k in ${!L1D[@]}; do 
      for p in ${!PDN[@]}; do
        for c in ${!CLK[@]}; do 
          for cs in ${!CPU_CYCLES[@]}; do
            for pred in ${!PREDICTOR[@]}; do
              sleep 0.5
              TN="${name[$j]}_${INSTRUCTIONS[$i]}_${CPU_CYCLES[${cs}]}_${CID[$c]}_${PDN[$p]}_${PREDICTOR[$pred]}"
              se_sc_classic_mc_ncv $TN ${DURATION[$i]} ${INSTRUCTIONS[$i]} ${INTERVAL[$i]} ${PROFILE_START[$i]} ${exe[$j]} "${opt[$j]}" ${CLK[$c]} ${PDN[$p]} ${CLK_[$c]} $VOLTAGE ${CPU_CYCLES[${cs}]} ${PREDICTOR[$pred]}
              while [ `jobs | wc -l` -ge 16 ]; do
                sleep 1
              done
            done
          done
        done
      done
    done
  done
done

while [ `jobs | wc -l` -ne 1 ]; do
  sleep 1
done
