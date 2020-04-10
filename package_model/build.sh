#!/bin/bash

g++ -Wall -shared -std=c++11 -DINTERPROCESS_PYTHON -D_XOPEN_SOURCE=500 -fPIC `python3 -m pybind11 --includes` interprocess.cpp -o interprocess`python3-config --extension-suffix` -lpthread -lrt 
#gcc -Wall -shared -std=c11 -D_XOPEN_SOURCE=500 -fPIC interprocess.c -o libinterprocess.so -lpthread -lrt 
