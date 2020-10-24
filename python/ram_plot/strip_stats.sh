#!/bin/bash

# Convert the Stats file to only the PowerPredictor Stats
#wc -l /home/kanungo3/output/gem5_out/fft_10000_2_MOBILE_ARM_DecorOnly_1_no_throttle_on_restore/stats.txt
# grep "system.cpu.iew.branchMispredicts\|sim_insts\|system.cpu.committed\|powerPred\|totalInstsReady\|icacheStallCycles\|instsReadyMax\|system.cpu.iew.exec_branches" /home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_half_freq_throttle_on_restore/stats.txt > stats_1.txt
# G5_OUT=
# #TESTS=("dijkstra" "sha" "untoast")
# TESTS=("fft" "qsort")
# #TESTS=("dijkstra" "qsort" "fft" "ffti" "sha")
# #TESTS=("toast" "untoast")
# #DURATION=("10000" "25000" "25000")
# DURATION=("10000" "10000")
# #DURATION=("25000" "10000" "25000" "25000" "25000")
# #DURATION=("25000" "25000")
# CLASS=("MOBILE" "LAPTOP" "DESKTOP")
# PDN=("ARM" "INTEL_M" "INTEL_DT")
# #PDN=("HARVARD_M" "HARVARD_L" "HARVARD_D")

# SRC="/home/kanungo3/output/gem5_out"
# TYPE="uArchEventPredictor_1"

# for i in ${!TESTS[@]}; do 
#   for j in ${!CLASS[@]}; do 
#     P=$SRC/${TESTS[$i]}_${DURATION[$i]}_2_${CLASS[$j]}_${PDN[$j]}_${TYPE}_no_throttle_on_restore/stats.txt
#     D=$SRC/${CLASS[$j]}_${TYPE}_no_throttle_on_restore_2
#     echo "$P"
#     if [ -f "$P" ]; then 
#       echo "mkdir -p $D"
#       mkdir -p $D
#       echo "grep \"powerPred\|totalInstsReady\|icacheStallCycles\|instsReadyMax\" $P > \"$D/${TESTS[$i]}.txt\""
#       grep "powerPred\|totalInstsReady\|icacheStallCycles\|instsReadyMax" $P > "$D/${TESTS[$i]}.txt"
#       #echo "mv $P $D/${TESTS[$i]}.txt"
#       #mv $P $D/${TESTS[$i]}.txt
#     fi
#   done
# done

# paths=("/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_half_freq_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_no_stall_yes_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_no_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_half_freq_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_no_stall_yes_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_no_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_half_freq_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_no_stall_yes_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_no_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_throttle_on_restore")
# type=("half_freq_throttle_on_restore" "no_stall_yes_throttle_on_restore" "no_throttle_on_restore" "throttle_on_restore" "half_freq_throttle_on_restore" "no_stall_yes_throttle_on_restore" "no_throttle_on_restore" "throttle_on_restore" "half_freq_throttle_on_restore" "no_stall_yes_throttle_on_restore" "no_throttle_on_restore" "throttle_on_restore")
# out=("Desktop" "Desktop" "Desktop" "Desktop" "Laptop" "Laptop" "Laptop" "Laptop" "Mobile" "Mobile" "Mobile" "Mobile")

paths=("/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_no_emergency_state_half_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_no_emergency_state_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_w_emergency_state_d_sorted_half_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_w_emergency_state_d_sorted_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_w_emergency_state_half_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_DESKTOP_INTEL_DT_DecorOnly_1_w_emergency_state_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_no_emergency_state_half_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_no_emergency_state_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_w_emergency_state_d_sorted_half_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_w_emergency_state_d_sorted_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_w_emergency_state_half_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_LAPTOP_INTEL_M_DecorOnly_1_w_emergency_state_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_no_emergency_state_half_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_no_emergency_state_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_w_emergency_state_d_sorted_half_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_w_emergency_state_d_sorted_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_w_emergency_state_half_throttle_on_restore" "/home/kanungo3/output/gem5_out/qsort_10000_2_MOBILE_ARM_DecorOnly_1_w_emergency_state_throttle_on_restore")

type=("no_emergency_state_half_throttle_on_restore" "no_emergency_state_throttle_on_restore" "w_emergency_state_d_sorted_half_throttle_on_restore" "w_emergency_state_d_sorted_throttle_on_restore" "w_emergency_state_half_throttle_on_restore" "w_emergency_state_throttle_on_restore" "no_emergency_state_half_throttle_on_restore" "no_emergency_state_throttle_on_restore" "w_emergency_state_d_sorted_half_throttle_on_restore" "w_emergency_state_d_sorted_throttle_on_restore" "w_emergency_state_half_throttle_on_restore" "w_emergency_state_throttle_on_restore" "no_emergency_state_half_throttle_on_restore" "no_emergency_state_throttle_on_restore" "w_emergency_state_d_sorted_half_throttle_on_restore" "w_emergency_state_d_sorted_throttle_on_restore" "w_emergency_state_half_throttle_on_restore" "w_emergency_state_throttle_on_restore")

out=("Desktop" "Desktop" "Desktop" "Desktop" "Desktop" "Desktop" "Laptop" "Laptop" "Laptop" "Laptop" "Laptop" "Laptop" "Mobile" "Mobile" "Mobile" "Mobile" "Mobile" "Mobile")
for i in ${!paths[@]}; do 
    P="${paths[$i]}/stats.txt"
    D="/home/kanungo3/output/gem5_stripped/${out[$i]}"
    echo "$P"
    if [ -f "$P" ]; then 
      echo "mkdir -p $D"
      mkdir -p $D
      echo "grep \"system.cpu.numCycles\|system.cpu.iew.branchMispredicts\|sim_insts\|system.cpu.committed\|powerPred\|totalInstsReady\|icacheStallCycles\|instsReadyMax\|system.cpu.iew.exec_branches\" $P > \"$D/${type[$i]}.txt\""
      grep "system.cpu.numCycles\|system.cpu.iew.branchMispredicts\|sim_insts\|system.cpu.committed\|powerPred\|totalInstsReady\|icacheStallCycles\|instsReadyMax\|system.cpu.iew.exec_branches" $P > "$D/${type[$i]}.txt"
      #echo "mv $P $D/${TESTS[$i]}.txt"
      #mv $P $D/${TESTS[$i]}.txt
    fi
done
