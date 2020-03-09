FROM ubuntu:16.04
MAINTAINER "Andrew Smith <atsmith3@illinois.edu>"

ARG user="andrew"

# Packages for building gem5
RUN apt-get update && \
    apt-get install -y gcc-multilib make valgrind git gdb build-essential && \
    apt-get install -y flex bison autoconf zlib1g-dev libgoogle-perftools-dev

RUN apt-get update && \
    apt-get install -y gcc make python python-pip && \
    pip install --upgrade pip && \
    pip install six scons

# For building & Running Pybind for Verilog Sim:

# Running Predict-T
RUN apt-get update && \
    apt-get install -y python-tk

RUN pip install --upgrade pip && \
    pip install progressbar numpy matplotlib

RUN groupadd -g 1000 m5
RUN useradd -rm -d /home/${user} -s /bin/bash -g root -G m5 -u 1000 ${user}

WORKDIR /home/${user}
