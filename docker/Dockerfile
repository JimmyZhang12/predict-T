FROM ubuntu:16.04

MAINTAINER "Andrew Smith <atsmith3@illinois.edu>"

ARG user
ARG wd
ARG uid="1000"
ARG gid="1000"

RUN apt-get update && \
  apt-get -y install git make m4 scons build-essential git m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev python-dev python python-pip python3 python3-dev

#RUN yum -y update && \
#  yum -y install csh ksh glibc.i686 sqlite elfutils-libelf-devel elfutils-libelf-devel.i686 @development-tools glibc-devel.i686
#
#RUN yum -y update && \
#  yum -y install vim gcc clang libgcc libgcc.i686 gcc-c++ libstdc++.i686 libstdc++ zlib zlib.i686
#
RUN apt-get update && \
  apt-get -y install csh ksh libc6-dev libc6-dev:i386 libc6 libc6:i386 sqlite libelf-dev libelf-dev:i386 libelf1 libelf1:i386

RUN apt-get update && \
  apt-get -y install vim gcc-multilib clang g++-multilib zlib1g:i386 zlib1g-dev:i386

RUN pip install --upgrade pip -i https://pypi.python.org/simple
RUN pip install six scons 

RUN groupadd -g ${gid} sim
RUN useradd -rm -d /home/${user} -s /bin/bash -g root -G sim -u ${uid} ${user}
RUN mkdir -p /run_vsim
RUN chown ${user} /run_vsim

WORKDIR ${wd}
