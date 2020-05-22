#!/bin/bash

SIM_ROOT="$PREDICT_T_ROOT/package_model"

if [[ -z $(docker images -q centos7_test:cadence) ]]; then
  pushd docker && docker build --build-arg gid=$(id -g $(whoami)) --build-arg uid=$(id -u $(whoami)) --build-arg user=$(whoami) --build-arg wd=$SIM_ROOT -t centos7_test:cadence . && popd
fi

docker run --rm --memory 16g --network=host \
  --user $(id -u):$(id -g) \
  --name=$1 \
  -v /software:/software \
  -v /dev/shm/:/dev/shm/ \
  -v $VSIM_TOOLS:$VSIM_TOOLS \
  -v $SIM_ROOT:$SIM_ROOT \
  -v $OUTPUT_ROOT:$OUTPUT_ROOT \
  -e PREDICT_T_ROOT \
  -e OUTPUT_ROOT \
  centos7_test:cadence \
  ./run_vsim.sh $1 $2
  #./run_vsim.sh $1 $2 $3 $4
