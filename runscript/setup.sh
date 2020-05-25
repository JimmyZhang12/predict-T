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

#--------------------------------------------------------------------
# Paths
#  ____   _  _____ _   _ ____
# |  _ \ / \|_   _| | | / ___|
# | |_) / _ \ | | | |_| \___ \
# |  __/ ___ \| | |  _  |___) |
# |_| /_/   \_\_| |_| |_|____/
#
#--------------------------------------------------------------------
export VSIM_TOOLS="$HOME/cadence"
export PREDICT_T_ROOT="$HOME/predict-T"
export GEM5_ROOT="$HOME/gem5"
export OUTPUT_ROOT="$HOME/scratch/predict-T"
export MCPAT_ROOT="$HOME/mcpat"
export SIM_ROOT="$PREDICT_T_ROOT/circuit_model"

echo "[ setup.sh ] export VSIM_TOOLS $VSIM_TOOLS"
echo "[ setup.sh ] export PREDICT_T_ROOT $PREDICT_T_ROOT"
echo "[ setup.sh ] export GEM5_ROOT $GEM5_ROOT"
echo "[ setup.sh ] export OUTPUT_ROOT $OUTPUT_ROOT"
echo "[ setup.sh ] export MCPAT_ROOT $MCPAT_ROOT"
echo "[ setup.sh ] export SIM_ROOT $SIM_ROOT"

#--------------------------------------------------------------------
# Build any requiered Docker Images
#  ____   ___   ____ _  _______ ____
# |  _ \ / _ \ / ___| |/ | ____|  _ \
# | | | | | | | |   | ' /|  _| | |_) |
# | |_| | |_| | |___| . \| |___|  _ <
# |____/ \___/ \____|_|\_|_____|_| \_\
#
#--------------------------------------------------------------------
export VSIM_IMAGE="centos7:cadence"
echo "[ setup.sh ] export VSIM_IMAGE $VSIM_IMAGE"
if [[ -z $(docker images -q $VSIM_IMAGE) ]]; then
  ddir="$PREDICT_T_ROOT/circuit_model/docker"
  echo "[ setup.sh ] Building docker image $VSIM_IMAGE with command:"
  echo "docker build --build-arg gid=$(id -g $(whoami)) --build-arg uid=$(id -u $(whoami)) --build-arg user=$(whoami) --build-arg wd=$SIM_ROOT -t $VSIM_IMAGE $ddir"
  docker build --build-arg gid=$(id -g $(whoami)) --build-arg uid=$(id -u $(whoami)) --build-arg user=$(whoami) --build-arg wd=$SIM_ROOT -t $VSIM_IMAGE $ddir
  if [ $? -ne 0 ]; then 
    echo "[ setup.sh ] error: Building docker image $VSIM_IMAGE with dockerfile: $ddir/Dockerfile failed."
  fi
else
  echo "[ setup.sh ] Docker image $VSIM_IMAGE exists, continuing..."
fi

#--------------------------------------------------------------------
# Output Directories
#   ___  _   _ _____ ____  _   _ _____   ____ ___ ____  
#  / _ \| | | |_   _|  _ \| | | |_   _| |  _ \_ _|  _ \ 
# | | | | | | | | | | |_) | | | | | |   | | | | || |_) |
# | |_| | |_| | | | |  __/| |_| | | |   | |_| | ||  _ < 
#  \___/ \___/  |_| |_|    \___/  |_|   |____/___|_| \_\
#                                                       
#--------------------------------------------------------------------
if [ ! -d $OUTPUT_ROOT ]; then
  echo "[ setup.sh ] creating $OUTPUT_ROOT"
  mkdir -p $OUTPUT_ROOT
fi

if [ ! -d $OUTPUT_ROOT/gem5_out ]; then
  echo "[ setup.sh ] creating $OUTPUT_ROOT/gem5_out"
  mkdir -p $OUTPUT_ROOT/gem5_out
fi

if [ ! -d $OUTPUT_ROOT/text_out ]; then
  echo "[ setup.sh ] creating $OUTPUT_ROOT/text_out"
  mkdir -p $OUTPUT_ROOT/text_out
fi

if [ ! -d $OUTPUT_ROOT/mcpat_out ]; then
  echo "[ setup.sh ] creating $OUTPUT_ROOT/mcpat_out"
  mkdir -p $OUTPUT_ROOT/mcpat_out
fi

if [ ! -d $OUTPUT_ROOT/circuit_model/log ]; then
  echo "[ setup.sh ] creating $OUTPUT_ROOT/circuit_model/log"
  mkdir -p $OUTPUT_ROOT/circuit_model/log
fi
