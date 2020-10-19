#!/bin/bash

# Convert the Stats file to only the PowerPredictor Stats

G5_OUT=
#TESTS=("dijkstra" "sha" "untoast")
TESTS=("qsort" "dijkstra")
#TESTS=("dijkstra" "qsort" "fft" "ffti" "sha")
#TESTS=("toast" "untoast")
#DURATION=("10000" "25000" "25000")
DURATION=("10000" "15000" "15000")
#DURATION=("25000" "10000" "25000" "25000" "25000")
#DURATION=("25000" "25000")
CLASS=("MOBILE" "LAPTOP" "DESKTOP")
PDN=("ARM" "INTEL_M" "INTEL_DT")
#PDN=("HARVARD_M" "HARVARD_L" "HARVARD_D")

SRC="$HOME/output_10_14/gem5_out"
#TYPE="DecorOnly_1"
TYPE="HarvardPowerPredictor_1"
#TYPE="IdealSensor_1"
#TYPE="uArchEventPredictor_1"



for i in ${!TESTS[@]}; do 
  for j in ${!CLASS[@]}; do 
    P="$SRC/${TESTS[$i]}_${DURATION[$i]}_2_${CLASS[$j]}_${PDN[$j]}_${TYPE}_nodummy/stats.txt"
    D="$SRC/${CLASS[$j]}_${TYPE}"

    echo "$P"
    if [ -f "$P" ]; then 
      echo "mkdir -p $D"
      mkdir -p $D
      #echo "grep \"powerPred\|system.cpu.numCycles\|totalInstsReady\|num_voltage_emergency\|instsReadyMax\" $P > \"$D/${TESTS[$i]}.txt\""
      #grep "system.cpu.powerPred.frequency\|sim_insts\|system.cpu.commit.committedOps\|Current State" $P > "$D/${TESTS[$i]}.txt"
      grep "powerPred\|Begin Simulation Statistics\|numCycles\|committedInsts\|system.cpu.fetch.Insts" $P > "$D/${TESTS[$i]}.txt"
      #echo "mv $P $D/${TESTS[$i]}.txt"
      #mv $P $D/${TESTS[$i]}.txt
    fi
  done
done
