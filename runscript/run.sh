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

#--------------------------------------------------------------------
# Check Environment
#--------------------------------------------------------------------
if [ -z "$VSIM_TOOLS" ]; then
  echo "[ run.sh ] error: VSIM_TOOLS not set; source setup.sh"
  exit
fi
if [ -z "$PREDICT_T_ROOT" ]; then
  echo "[ run.sh ] error: PREDICT_T_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$GEM5_ROOT" ]; then
  echo "[ run.sh ] error: GEM5_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$OUTPUT_ROOT" ]; then
  echo "[ run.sh ] error: OUTPUT_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$MCPAT_ROOT" ]; then
  echo "[ run.sh ] error: OUTPUT_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$SIM_ROOT" ]; then
  echo "[ run.sh ] error: SIM_ROOT not set; source setup.sh"
  exit 1
fi
if [ -z "$VSIM_IMAGE" ]; then
  echo "[ run.sh ] error: VSIM_IMAGE not set; source setup.sh"
  exit 1
fi
echo "[ run.sh ] VSIM_TOOLS $VSIM_TOOLS"
echo "[ run.sh ] PREDICT_T_ROOT $PREDICT_T_ROOT"
echo "[ run.sh ] GEM5_ROOT $GEM5_ROOT"
echo "[ run.sh ] OUTPUT_ROOT $OUTPUT_ROOT"
echo "[ run.sh ] MCPAT_ROOT $MCPAT_ROOT"
echo "[ run.sh ] SIM_ROOT $SIM_ROOT"
echo "[ run.sh ] VSIM_IMAGE $VSIM_IMAGE"

if [[ -z $(docker images -q $VSIM_IMAGE) ]]; then
  echo "[ run_cadence.sh ] error: Docker container $VSIM_IMAGE is not built; source setup.sh"
  exit 1
fi

#--------------------------------------------------------------------
# Configure Test Specific Paths
#--------------------------------------------------------------------
TEST="$PREDICT_T_ROOT/testbin"
INPUT="$TEST/input"
echo "[ run.sh ] TEST $TEST"
echo "[ run.sh ] INPUT $INPUT"


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

#name=("basicmath" "bitcnts" "qsort" "susan_smooth" "susan_edge" "susan_corner" "dijkstra" "patricia" "blowfish_encrypt" "blowfish_decrypt" "rijndael_encrypt" "rijndael_decrypt" "sha" "crc" "fft" "ffti" "toast" "untoast")
#exe=("basicmath" "bitcnts" "qsort" "susan" "susan" "susan" "dijkstra" "patricia" "blowfish" "blowfish" "rijndael" "rijndael" "sha" "crc" "fft" "fft" "toast" "untoast")
#opt=("" "1000" "${INPUT}/qsort_large.dat" "${INPUT}/susan_large.pgm ${output}/susan_large_s.pgm -s" "${INPUT}/susan_large.pgm ${output}/susan_large_s.pgm -e" "${INPUT}/susan_large.pgm ${output}/susan_large_s.pgm -c" "${INPUT}/dijkstra.dat" "${INPUT}/patricia_small.udp" "e ${INPUT}/blowfish_small.asc ${output}/blowfish_small.enc 1234567890abcdeffedcba0987654321" "d ${INPUT}/blowfish_small.enc ${output}/blowfish_small.asc 1234567890abcdeffedcba0987654321" "${INPUT}/rijndael_small.asc ${output}/rijndael_small.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/rijndael_small.enc ${output}/rijndael_small.asc d 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${INPUT}/sha_small.asc" "${INPUT}/crc_small.pcm" "4 4096" "4 8192 -i" "-fps -c ${INPUT}/toast_small.au" "-fps -c ${INPUT}/toast_small.gsm")
#name=("dijkstra" "toast" "susan_smooth" "fft")
#exe=("dijkstra" "toast" "susan" "fft")
#opt=("${INPUT}/dijkstra.dat" "-fps -c ${INPUT}/toast_small.au" "${INPUT}/susan_large.pgm ${output}/susan_large_s.pgm -s" "4 4096")
name=("dijkstra")
exe=("dijkstra")
opt=("${INPUT}/dijkstra.dat")

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
            TN="${name[$j]}_${TABLE_SIZE[$l]}_${PC_START[$m]}_${INTERVAL[$i]}_SimplePredictorEnableBuck1MHz"
#            TN="${name[$j]}_${TABLE_SIZE[$l]}_${PC_START[$m]}_${INTERVAL[$i]}_mcSimplePredictorEnableBuck1MHz"
            se_single_core_xeon_e7_8893 $TN ${DURATION[$i]} ${INTERVAL[$i]} ${STEP[$i]} ${PROFILE_START[$i]} ${exe[$j]} "${opt[$j]}"
#            se_n_core_xeon_e7_8893 $TN ${DURATION[$i]} ${INTERVAL[$i]} ${STEP[$i]} ${PROFILE_START[$i]} ${exe[$j]} "${opt[$j]}" "4"
#--debug-flags=SimpleHistoryPowerPred,PowerPred,StatEvent \
  #--debug-flags=SimpleHistoryPowerPred \
  #--debug-flags=TestPowerPred,PowerPred,StatEvent \
#--power_pred_type=SimpleHistoryPowerPredictor \
#      echo "
#../gem5/build/X86/gem5.opt \
#--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
#--mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
#--mcpat_path=${PREDICT_T_ROOT}/mcpat \
#--mcpat_out=${OUTPUT_ROOT}/mcpat_out \
#--mcpat_testname=$TN \
#--power_profile_start=${PROFILE_START[$i]} \
#--power_profile_duration=${DURATION[$i]} \
#--power_profile_interval=${INTERVAL[$i]} \
#--ncverilog_path=${PREDICT_T_ROOT}/package_model \
#--ncverilog_step=${STEP[$i]} \
#../gem5/configs/example/se.py \
#--cmd=testbin/${exe[$j]} \
#--opt=\"${opt[$j]}\" \
#--power_profile_interval=${INTERVAL[$i]} \
#--power_pred_type=TestPowerPredictor \
#--power_pred_table_size=${TABLE_SIZE[$l]} \
#--power_pred_pc_start=${PC_START[$m]} \
#--power_pred_history_size=${HISTORY_SIZE[$o]} \
#--num-cpus=1 \
#--cpu-type=DerivO3CPU \
#--l1i_size=${L1I[$k]} \
#--l1i-hwp-type=TaggedPrefetcher \
#--l1d_size=${L1D[$k]} \
#--l1d-hwp-type=TaggedPrefetcher \
#--l2cache \
#--num-l2caches=1 \
#--l2_size=${L2[$k]} \
#--l2-hwp-type=TaggedPrefetcher \
#--l3cache \
#--l3_size=${L3[$k]} \
#--l3-hwp-type=TaggedPrefetcher \
#--caches \
#--sys-clock=3.5GHz \
#--mem-size=8GB > ${OUTPUT_ROOT}text_out/$TN.out &"
#../gem5/build/X86/gem5.opt \
#  --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
#  --mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
#  --mcpat_path=${PREDICT_T_ROOT}/mcpat \
#  --mcpat_out=${OUTPUT_ROOT}/mcpat_out \
#  --mcpat_testname=$TN \
#  --power_profile_start=${PROFILE_START[$i]} \
#  --power_profile_duration=${DURATION[$i]} \
#  --power_profile_interval=${INTERVAL[$i]} \
#  --ncverilog_path=${PREDICT_T_ROOT}/package_model \
#  --ncverilog_step=${STEP[$i]} \
#  ../gem5/configs/example/se.py \
#  --cmd=testbin/${exe[$j]} \
#  --opt="${opt[$j]}" \
#  --power_profile_interval=${INTERVAL[$i]} \
#  --power_pred_type=TestPowerPredictor \
#  --power_pred_table_size=${TABLE_SIZE[$l]} \
#  --power_pred_pc_start=${PC_START[$m]} \
#  --power_pred_history_size=${HISTORY_SIZE[$o]} \
#  --num-cpus=1 \
#  --cpu-type=DerivO3CPU \
#  --l1i_size=${L1I[$k]} \
#  --l1i-hwp-type=TaggedPrefetcher \
#  --l1d_size=${L1D[$k]} \
#  --l1d-hwp-type=TaggedPrefetcher \
#  --l2cache \
#  --num-l2caches=1 \
#  --l2_size=${L2[$k]} \
#  --l2-hwp-type=TaggedPrefetcher \
#  --l3cache \
#  --l3_size=${L3[$k]} \
#  --l3-hwp-type=TaggedPrefetcher \
#  --caches \
#  --sys-clock=3.5GHz \
#  --mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &
            while [ `jobs | wc -l` -ge 32 ]; do
              sleep 1
            done
          done
        done
      done
    done
  done
done
