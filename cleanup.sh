#!/bin/bash

BENCHMARKS=("basicmath" "bitcnts" "qsort_small" "qsort_large" "susan_small_s" "susan_small_e" "susan_small_c" "susan_large_s" "susan_large_e" "susan_large_c" "dijkstra_small" "dijkstra_large" "patricia_small" "blowfish_e" "blowfish_d" "rijndael_e" "rijndael_d" "sha" "crc" "fft" "fft_i" "toast" "untoast")

clean () {
  if [[ -n $(ls /dev/shm/ | grep "$1") ]]; then 
    echo "rm /dev/shm/$1"
    rm /dev/shm/$1
  fi
  if [[ -n $(docker container ls | grep "$1") ]]; then
    echo "docker container kill $1"
    docker container kill $1
  fi
}

for b in ${BENCHMARKS[@]}; do
  clean $b
done
