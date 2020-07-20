#!/bin/bash

# Convert the Stats file to only the PowerPredictor Stats

G5_OUT=
TESTS=("dijkstra" "qsort" "fft" "ffti" "sha" "toast" "untoast")
#TESTS=("dijkstra" "qsort" "fft" "ffti" "susan_smooth" "toast" "untoast")
#DURATION=("25000" "5000" "25000" "25000" "5000" "25000" "25000")
DURATION=("25000" "10000" "25000" "25000" "25000" "25000" "25000")
#DURATION=("100000" "50000" "100000" "100000" "50000" "100000" "100000")
CLASS=("MOBILE" "LAPTOP" "DESKTOP")
PDN=("ARM" "INTEL_M" "INTEL_DT")

SRC=$1
TYPE=$2

for i in ${!TESTS[@]}; do 
  for j in ${!CLASS[@]}; do 
    P="$SRC/${TESTS[$i]}_${DURATION[$i]}_2_${CLASS[$j]}_${PDN[$j]}_${TYPE}_no_throttle_on_restore/stats.txt"
    D=$SRC/${CLASS[$j]}_${TYPE}_throttle_on_restore
    #echo "$P"
    if [ -f "$P" ]; then 
      echo "mkdir -p $D"
      mkdir -p $D
      echo "grep \"powerPred\|totalInstsReady\|icacheStallCycles\|instsReadyMax\" $P > \"$D/${TESTS[$i]}.txt\""
      grep "powerPred\|totalInstsReady\|icacheStallCycles\|instsReadyMax" $P > "$D/${TESTS[$i]}.txt"
      #echo "mv $P $D/${TESTS[$i]}.txt"
      #mv $P $D/${TESTS[$i]}.txt
    fi
  done
done
