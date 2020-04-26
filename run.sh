#!/bin/bash
#
# run_mibench.sh
#
# Run mibench executables on the predict-T framework

source setup.sh

output=output
input=input

DURATION=("1000000000")
INTERVAL=("1000000")
STEP=("1000")
PROFILE_START=("-1")

L1D=("64kB")
L1I=("32kB")
L2=("256kB")
L3=("16MB")

name=("basicmath" "bitcnts" "qsort" "susan_smooth" "susan_edge" "susan_corner" "dijkstra" "patricia" "blowfish_encrypt" "blowfish_decrypt" "rijndael_encrypt" "rijndael_decrypt" "sha" "crc" "fft" "ffti" "toast" "untoast")
exe=("basicmath" "bitcnts" "qsort" "susan" "susan" "susan" "dijkstra" "patricia" "blowfish" "blowfish" "rijndael" "rijndael" "sha" "crc" "fft" "fft" "toast" "untoast")
opt=("" "1000" "${input}/qsort_large.dat" "${input}/susan_large.pgm ${output}/susan_large_s.pgm -s" "${input}/susan_large.pgm ${output}/susan_large_s.pgm -e" "${input}/susan_large.pgm ${output}/susan_large_s.pgm -c" "${input}/dijkstra.dat" "${input}/patricia_small.udp" "e ${input}/blowfish_small.asc ${output}/blowfish_small.enc 1234567890abcdeffedcba0987654321" "d ${input}/blowfish_small.enc ${output}/blowfish_small.asc 1234567890abcdeffedcba0987654321" "${input}/rijndael_small.asc ${output}/rijndael_small.enc e 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${input}/rijndael_small.enc ${output}/rijndael_small.asc d 1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321" "${input}/sha_small.asc" "${input}/crc_small.pcm" "4 4096" "4 8192 -i" "-fps -c ${input}/toast_small.au" "-fps -c ${input}/toast_small.gsm")
#name=("dijkstra" "toast" "untoast")
#exe=("dijkstra" "toast" "untoast")
#opt=("${input}/dijkstra.dat" "-fps -c ${input}/toast_small.au" "-fps -c ${input}/toast_small.gsm")

for j in ${!name[@]}; do 
  for i in ${!INTERVAL[@]}; do 
    for k in ${!L1D[@]}; do 
      TN="${name[$j]}_${INTERVAL[$i]}_2500u"
#--debug-flags=TestPowerPred,StatEvent \
  #--debug-flags=TestPowerPred,StatEvent \
      echo "
../gem5/build/X86/gem5.opt \
--outdir=${OUTPUT_ROOT}/gem5_out/$TN \
--mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
--mcpat_path=${PREDICT_T_ROOT}/mcpat \
--mcpat_out=${OUTPUT_ROOT}/mcpat_out \
--mcpat_testname=$TN \
--power_profile_start=${PROFILE_START[$i]} \
--power_profile_duration=${DURATION[$i]} \
--power_profile_interval=${INTERVAL[$i]} \
--ncverilog_path=${PREDICT_T_ROOT}/package_model \
--ncverilog_step=${STEP[$i]} \
../gem5/configs/example/se.py \
--cmd=testbin/${exe[$j]} \
--opt=\"${opt[$j]}\" \
--power_profile_interval=${INTERVAL[$i]} \
--num-cpus=1 \
--cpu-type=DerivO3CPU \
--l1i_size=${L1I[$k]} \
--l1i-hwp-type=TaggedPrefetcher \
--l1d_size=${L1D[$k]} \
--l1d-hwp-type=TaggedPrefetcher \
--l2cache \
--num-l2caches=1 \
--l2_size=${L2[$k]} \
--l2-hwp-type=TaggedPrefetcher \
--l3cache \
--l3_size=${L3[$k]} \
--l3-hwp-type=TaggedPrefetcher \
--caches \
--sys-clock=3.5GHz \
--mem-size=8GB > ${OUTPUT_ROOT}text_out/$TN.out &"
../gem5/build/X86/gem5.opt \
  --outdir=${OUTPUT_ROOT}/gem5_out/$TN \
  --mcpat_template=${PREDICT_T_ROOT}/mcpat-template-x86-sc.xml \
  --mcpat_path=${PREDICT_T_ROOT}/mcpat \
  --mcpat_out=${OUTPUT_ROOT}/mcpat_out \
  --mcpat_testname=$TN \
  --power_profile_start=${PROFILE_START[$i]} \
  --power_profile_duration=${DURATION[$i]} \
  --power_profile_interval=${INTERVAL[$i]} \
  --ncverilog_path=${PREDICT_T_ROOT}/package_model \
  --ncverilog_step=${STEP[$i]} \
  ../gem5/configs/example/se.py \
  --cmd=testbin/${exe[$j]} \
  --opt="${opt[$j]}" \
  --power_profile_interval=${INTERVAL[$i]} \
  --num-cpus=1 \
  --cpu-type=DerivO3CPU \
  --l1i_size=${L1I[$k]} \
  --l1i-hwp-type=TaggedPrefetcher \
  --l1d_size=${L1D[$k]} \
  --l1d-hwp-type=TaggedPrefetcher \
  --l2cache \
  --num-l2caches=1 \
  --l2_size=${L2[$k]} \
  --l2-hwp-type=TaggedPrefetcher \
  --l3cache \
  --l3_size=${L3[$k]} \
  --l3-hwp-type=TaggedPrefetcher \
  --caches \
  --sys-clock=3.5GHz \
  --mem-size=8GB > ${OUTPUT_ROOT}/text_out/$TN.out &
      while [ `jobs | wc -l` -ge 32 ]; do
        sleep 1
      done
    done
  done
done
