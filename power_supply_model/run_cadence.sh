#!/bin/bash

SIM_ROOT="$PREDICT_T_ROOT/power_supply_model"

if [[ -z $(docker images -q centos7:cadence) ]]; then
  pushd docker && docker build --build-arg gid=$(id -g $(whoami)) --build-arg uid=$(id -u $(whoami)) --build-arg user=$(whoami) --build-arg wd=$SIM_ROOT -t centos7:cadence . && popd
fi

docker run --rm --memory 16g --network=host \
  --user $(id -u):$(id -g) \
  --name=$1 \
  -v /software:/software \
  -v /dev/shm/:/dev/shm/ \
  -v $VSIM_TOOLS:$VSIM_TOOLS \
  -v $SIM_ROOT:$SIM_ROOT \
  -e PREDICT_T_ROOT \
  centos7:cadence \
  ./run_vsim.sh $1 $2
#docker run --rm -t -i --memory 16g --network=host \
#  --user $(id -u):$(id -g) \
#  --name=$1 \
#  -v /software:/software \
#  -v /dev/shm/:/dev/shm/ \
#  -v $VSIM_TOOLS:$VSIM_TOOLS \
#  -v $SIM_ROOT:$SIM_ROOT \
#  -e PREDICT_T_ROOT \
#  centos7:cadence \
#  ./run_vsim.sh $1 $2
