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

script_name="run_mc.sh"

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
  print_error "MCPAT_ROOT not set; source setup.sh"
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
print_info "TEST $TEST"
print_info "INPUT $INPUT"


#--------------------------------------------------------------------
# Configure Simulation Parameters
#--------------------------------------------------------------------
DURATION=("10000000")
INTERVAL=("1000000")
STEP=("1000")
PROFILE_START=("0")

L1D=("64kB")
L1I=("32kB")
L2=("256kB")
L3=("16MB")

name=("vector_add")
exe=("vector_add")
opt=("65536 %s")
NC=("1" "2" "4" "6" "8" "12" "16" "20" "24" "32")
#NC=("1" "2" "4" "6" "8")
#NC=("12" "16" "20" "24")
CLK=("3.5GHz")
#CLK=("1.5GHz" "2.0GHz" "2.5GHz" "3.0GHz" "3.5GHz")

#--------------------------------------------------------------------
# Run
#--------------------------------------------------------------------
for j in ${!name[@]}; do 
  for i in ${!INTERVAL[@]}; do 
    for k in ${!L1D[@]}; do 
      for t in ${!NC[@]}; do
        for c in ${!CLK[@]}; do
          # Test Name
          #TN="test_${name[$j]}_${NC[$t]}c_${CLK[$c]}_ruby_nmp_nncv"
          TN="test_${name[$j]}_${NC[$t]}c_${CLK[$c]}_classic_nmp_nncv"

          # Format the options with the num cores
          if [ $(echo "${opt[$j]}" | grep -o "%s" | wc -w) -eq 1 ]; then
            printf -v OPTIONS "${opt[$j]}" ${NC[$t]}
          elif [ $(echo "${opt[$j]}" | grep -o "%s" | wc -w) -eq 2 ]; then
            printf -v OPTIONS "${opt[$j]}" ${NC[$t]} ${NC[$t]}
          fi

          # Run on System
          #se_mc_ruby_nmc_nncv $TN ${EXE[$j]} "${OPTIONS}" ${NC[$t]} ${CLK[$c]}
          se_mc_classic_nmc_nncv $TN ${exe[$j]} "${OPTIONS}" ${NC[$t]} ${CLK[$c]}
          while [ `jobs | wc -l` -ge 32 ]; do
            sleep 1
          done
        done
      done
    done
  done
done
