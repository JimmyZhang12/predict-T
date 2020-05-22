#!/bin/bash

for i in $(ls $1/*.log); do 
  python3 strip.py $i &
  while [ `jobs | wc -l` -ge $(nproc) ]; do
    sleep 1
  done
done


while [ `jobs | wc -l` -ne 1 ]; do
  sleep 1
done
