#!/bin/bash

GEM5="/home/andrew/research/gem5"
PRED_T="/home/andrew/research/predict-T"

pushd docker && docker build --build-arg user=$(whoami) -t predict_t:build_run . && popd
docker run --rm -t -i --user $(id -u):$(id -g) --name=m5 -v $GEM5:$GEM5 -v $PRED_T:$PRED_T predict_t:build_run
