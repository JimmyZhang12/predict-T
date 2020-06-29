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

script_name="run_parsec.sh"

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
TEST="$PREDICT_T_ROOT/parsec_testbin_m5"
INPUT="$TEST/input"
OUTPUT="$TEST/output"
print_info "TEST $TEST"
print_info "INPUT $INPUT"
print_info "OUTPUT $OUTPUT"

TRAINING_ROOT="$OUTPUT_ROOT/training_data"
print_info "TRAINING_ROOT $TRAINING_ROOT"


#--------------------------------------------------------------------
# Configure Simulation Parameters
#--------------------------------------------------------------------
DURATION=("-1")
INSTRUCTIONS=("50000" "100000" "150000" "200000") # Instructions to Simulate
#INSTRUCTIONS=("200000") # Instructions to Simulate

# When to start ROI, in Sim Ticks, -or- ROI by setting "-1"
PROFILE_START=("-1") 

# Power Distribution Network Type:
PDN=("HARVARD")
#PREDICTOR=("DecorOnly" "uArchEventPredictor")
#PREDICTOR=("IdealSensor" "Test")
#PREDICTOR=("IdealSensor" "Test" "DecorOnly" "uArchEventPredictor")
#PREDICTOR=("IdealSensor" "DecorOnly" "uArchEventPredictor")
#PREDICTOR=("HarvardPowerPredictor")
#PREDICTOR=("PerceptronPredictor")
PREDICTOR=("Test")

VOLTAGE="1.0"
CPU_CYCLES=("10")

L1D=("4kB" "16kB" "64kB")
L1I=("2kB" "8kB" "32kB")
L2=("64kB" "128kB" "256kB")
L3=("2MB" "8MB" "16MB")
CACHE=("SMALL" "MEDIUM" "LARGE")

#L1D=("4kB")
#L1I=("2kB")
#L2=("64kB")
#L3=("2MB")
#CACHE=("SMALL")

CLK=( "4.0GHz")
CLK_=("4000000000")
CID=( "4")

#NC=("8")
NC=("1" "2" "4" "8")

#LITHOGRAPHY=("22" "28" "32" "45" "65" "90")

#name=("swaptions" "freqmine" "fluidanimate" "blackscholes" "vips" "canneal")
#exe=("swaptions" "freqmine" "fluidanimate" "blackscholes" "vips" "canneal")
#opt=( \
#  "\055ns 1000 -sm 100000 -nt %s -sd 012384701" \
#  "${INPUT}/freqmine.dat 1" \
#  "%s 100 ${INPUT}/fluidanimate.fluid" \
#  "%s ${INPUT}/blackscholes.txt ${OUTPUT}/blackscholes_%s.txt" \
#  "\055\055vips-concurrency=%s im_benchmark ${INPUT}/vips.v ${OUTPUT}/vips_%s.v" \
#  "%s 10000 300 ${INPUT}/canneal.nets 30000"
#)
name=("swaptions" "fluidanimate" "blackscholes" "canneal")
exe=("swaptions" "fluidanimate" "blackscholes" "canneal")
opt=( \
  "\055ns 1000 -sm 100000 -nt %s -sd 012384701" \
  "%s 10000 ${INPUT}/fluidanimate.fluid" \
  "%s ${INPUT}/blackscholes.txt ${OUTPUT}/blackscholes_%s.txt" \
  "%s 10000 300 ${INPUT}/canneal.nets 30000"
)
#name=("swaptions")
#exe=("swaptions")
#opt=( \
#  "\055ns 1000 -sm 100000 -nt %s -sd 012384701" \
#)
#name=("freqmine")
#exe=("freqmine")
#opt=( \
#  "${INPUT}/freqmine.dat 1" \
#)
#name=("fluidanimate")
#exe=("fluidanimate")
#opt=( \
#  "%s 10000 ${INPUT}/fluidanimate.fluid" \
#)
#name=("vips")
#exe=("vips")
#opt=( \
#  "\055\055vips-concurrency=%s im_benchmark ${INPUT}/vips.v ${OUTPUT}/vips_%s.v" \
#)
#name=("blackscholes")
#exe=("blackscholes")
#opt=( \
#  "%s ${INPUT}/blackscholes.txt ${OUTPUT}/blackscholes_%s.txt" \
#)
#name=("canneal")
#exe=("canneal")
#opt=( \
#  "%s 10000 300 ${INPUT}/canneal.nets 30000"
#)

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
              for t in ${!NC[@]}; do
                # Test Name
                sleep 0.5
                TN="${name[$j]}_${INSTRUCTIONS[$t]}_${CPU_CYCLES[${cs}]}_${CID[$c]}_${PDN[$p]}_${PREDICTOR[$pred]}_${NC[$t]}core_${CACHE[$k]}"

                # Format the options with the num cores
                if [ $(echo "${opt[$j]}" | grep -o "%s" | wc -w) -eq 1 ]; then
                  printf -v OPTIONS "${opt[$j]}" ${NC[$t]}
                elif [ $(echo "${opt[$j]}" | grep -o "%s" | wc -w) -eq 2 ]; then
                  printf -v OPTIONS "${opt[$j]}" ${NC[$t]} ${NC[$t]}
                fi

                se_classic_mc_ncv $TN ${DURATION[$i]} ${INSTRUCTIONS[$t]} ${PROFILE_START[$i]} ${exe[$j]} "$OPTIONS" ${CLK[$c]} ${PDN[$p]} ${CLK_[$c]} $VOLTAGE ${CPU_CYCLES[${cs}]} ${PREDICTOR[$pred]} ${NC[$t]} ${L1I[$k]} ${L1D[$k]} ${L2[$k]} ${L3[$k]}
                while [ `jobs | wc -l` -ge 32 ]; do
                  sleep 1
                done
              done
            done
          done
        done
      done
    done
  done
done
