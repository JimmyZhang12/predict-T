#!/bin/bash

for test in $(ls ./mcpat_out); do
  python mcpat_pickle_to_csv.py $test 50000000 1000000000
done
