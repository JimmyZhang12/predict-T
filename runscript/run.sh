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

source util.sh

script_name="run.sh"

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

name=("basicmath" "bitcnts" "qsort" "susan_smooth" "susan_edge" "susan_corner" "dijkstra" "patricia" "blowfish_encrypt" "blowfish_decrypt" "rijndael_encrypt" "rijndael_decrypt" "sha" "crc" "fft" "ffti" "toast" "untoast")
exe=("basicmath" "bitcnts" "qsort" "susan" "susan" "susan" "dijkstra" "patricia" "blowfish" "blowfish" "rijndael" "rijndael" "sha" "crc" "fft" "fft" "toast" "untoast")
opt=("" "1000" "${INPUT}/qsort_large.dat" "${INPUT}/susan_large.pgm ${output}/susan_large_s.pgm -s" "${INPUT}/susan_large.pgm ${output}/susan_large_s.pgm -e" "${INPUT}/susan_large.pgm ${output}/susan_large_s.pgm -c" "${INPUT}/dijkstra.dat" "${INPUT}/patricia_small.udp" "e ${INPUT}/blowfish_small.asc ${output}/blowfish_small.enc 1234567890abcdeffedcba0987654321" "d ${INPUT}/blowfish_small.enc ${output}/blowfish_small.asc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael_small.asc ${output}/rijndael_small.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/rijndael_small.enc ${output}/rijndael_small.asc d 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/sha_small.asc" "${INPUT}/crc_small.pcm" "4 4096" "4 8192 -i" "-fps -c ${INPUT}/toast_small.au" "-fps -c ${INPUT}/toast_small.gsm")
#name=("dijkstra" "toast" "susan_smooth" "fft")
#exe=("dijkstra" "toast" "susan" "fft")
#opt=("${INPUT}/dijkstra.dat" "-fps -c ${INPUT}/toast_small.au" "${INPUT}/susan_large.pgm ${output}/susan_large_s.pgm -s" "4 4096")
#name=("dijkstra")
#exe=("dijkstra")
#opt=("${INPUT}/dijkstra.dat")

#TABLE_SIZE=("1024" "4096")
#PC_START=("6" "10" "14")
#HISTORY_SIZE=("1" "2")
#TABLE_SIZE=("1024")
#PC_START=("6")
#HISTORY_SIZE=("2")
TABLE_SIZE=("256")
PC_START=("10")
HISTORY_SIZE=("2")


#--------------------------------------------------------------------
# Run
#--------------------------------------------------------------------
for j in ${!name[@]}; do 
  for i in ${!INTERVAL[@]}; do 
    for k in ${!L1D[@]}; do 
      for l in ${!TABLE_SIZE[@]}; do
        for m in ${!PC_START[@]}; do
          for o in ${!HISTORY_SIZE[@]}; do
            #TN="${name[$j]}_${TABLE_SIZE[$l]}_${PC_START[$m]}_${INTERVAL[$i]}_${HISTORY_SIZE[$o]}_SimplePredictorDisableBuck1MHz"
            TN="${name[$j]}_${TABLE_SIZE[$l]}_${PC_START[$m]}_${INTERVAL[$i]}_harvard_PDN_Test"
#            TN="${name[$j]}_${TABLE_SIZE[$l]}_${PC_START[$m]}_${INTERVAL[$i]}_mcSimplePredictorEnableBuck1MHz"
            se_single_core_xeon_e7_8893 $TN ${DURATION[$i]} ${INTERVAL[$i]} ${STEP[$i]} ${PROFILE_START[$i]} ${exe[$j]} "${opt[$j]}"
#            se_n_core_xeon_e7_8893 $TN ${DURATION[$i]} ${INTERVAL[$i]} ${STEP[$i]} ${PROFILE_START[$i]} ${exe[$j]} "${opt[$j]}" "4"
            while [ `jobs | wc -l` -ge 32 ]; do
              sleep 1
            done
          done
        done
      done
    done
  done
done
