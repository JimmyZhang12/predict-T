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
# The above copyright notice and this permission notice shall be included in all # copies or substantial portions of the Software.  # 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

script_name="build_testbin.sh"

print_info () {
  green="\e[32m"
  nc="\e[0m"
  echo -e "$green[ $script_name ]$nc $1"
}

print_error () {
  red="\e[31m"
  nc="\e[0m"
  echo -e "$red[ $script_name ] Error:$nc $1"
  exit 1
}

source env.sh

# Create Directories:
if [ ! -d parsec_testbin ]; then
  print_info "Creating parsec_testbin"
  mkdir -p parsec_testbin
  if [ ! -d parsec_testbin/input ]; then
    print_info "Creating parsec_testbin/input"
    mkdir -p parsec_testbin/input
  fi
  if [ ! -d parsec_testbin/output ]; then
    print_info "Creating parsec_testbin/output"
    mkdir -p parsec_testbin/output
  fi
fi

if [ ! -d parsec_testbin_m5 ]; then
  print_info "Creating parsec_testbin_m5"
  mkdir -p parsec_testbin_m5
  if [ ! -d parsec_testbin_m5/input ]; then
    print_info "Creating parsec_testbin_m5/input"
    mkdir -p parsec_testbin_m5/input
  fi
  if [ ! -d parsec_testbin_m5/output ]; then
    print_info "Creating parsec_testbin_m5/output"
    mkdir -p parsec_testbin_m5/output
  fi
fi

#-----------------------------------------------------------------------------
#  ___ _      _   ___ _  _____  ___ _  _  ___  _    ___ ___ 
# | _ ) |    /_\ / __| |/ / __|/ __| || |/ _ \| |  | __/ __|
# | _ \ |__ / _ \ (__| ' <\__ \ (__| __ | (_) | |__| _|\__ \
# |___/____/_/ \_\___|_|\_\___/\___|_||_|\___/|____|___|___/
#
#-----------------------------------------------------------------------------
# Clean
if [ ! -z $CLEAN ]; then
	print_info "Cleaning Blackscholes"
	./bin/parsecmgmt -a fullclean -p blackscholes -c gcc-pthreads
	./bin/parsecmgmt -a fullclean -p blackscholes -c gcc-hooks
	./bin/parsecmgmt -a fulluninstall -p blackscholes -c gcc-pthreads
	./bin/parsecmgmt -a fulluninstall -p blackscholes -c gcc-hooks
fi

# Build
./bin/parsecmgmt -a build -p blackscholes -c gcc-pthreads
./bin/parsecmgmt -a build -p blackscholes -c gcc-hooks

# Copy exe
print_info "Copying Blackscholes Normal"
cp ./pkgs/apps/blackscholes/inst/amd64-linux.gcc-pthreads/bin/blackscholes ./parsec_testbin
print_info "Copying Blackscholes m5 Hook"
cp ./pkgs/apps/blackscholes/inst/amd64-linux.gcc-hooks/bin/blackscholes ./parsec_testbin_m5

# Copy Input Data
print_info "Copying Blackscholes Input Data"
pushd ./pkgs/apps/blackscholes/inputs
tar -xvf input_simlarge.tar
popd
cp ./pkgs/apps/blackscholes/inputs/in_64K.txt ./parsec_testbin/input/blackscholes.txt
cp ./pkgs/apps/blackscholes/inputs/in_64K.txt ./parsec_testbin_m5/input/blackscholes.txt


#-----------------------------------------------------------------------------
#  ___ _      _    _           _            _       
# | __| |_  _(_)__| |__ _ _ _ (_)_ __  __ _| |_ ___ 
# | _|| | || | / _` / _` | ' \| | '  \/ _` |  _/ -_)
# |_| |_|\_,_|_\__,_\__,_|_||_|_|_|_|_\__,_|\__\___|
#                                                   
#-----------------------------------------------------------------------------
# Clean
if [ ! -z $CLEAN ]; then
	print_info "Cleaning fluidanimate"
	./bin/parsecmgmt -a fullclean -p fluidanimate -c gcc-pthreads
	./bin/parsecmgmt -a fullclean -p fluidanimate -c gcc-hooks
	./bin/parsecmgmt -a fulluninstall -p fluidanimate -c gcc-pthreads
	./bin/parsecmgmt -a fulluninstall -p fluidanimate -c gcc-hooks
fi

# Build
./bin/parsecmgmt -a build -p fluidanimate -c gcc-pthreads
./bin/parsecmgmt -a build -p fluidanimate -c gcc-hooks

# Copy exe
print_info "Copying fluidanimate Normal"
cp ./pkgs/apps/fluidanimate/inst/amd64-linux.gcc-pthreads/bin/fluidanimate ./parsec_testbin
print_info "Copying fluidanimate m5 Hook"
cp ./pkgs/apps/fluidanimate/inst/amd64-linux.gcc-hooks/bin/fluidanimate ./parsec_testbin_m5

# Copy Input Data
print_info "Copying fluidanimate Input Data"
pushd ./pkgs/apps/fluidanimate/inputs
tar -xvf input_simlarge.tar
popd
cp ./pkgs/apps/fluidanimate/inputs/in_300K.fluid ./parsec_testbin/input/fluidanimate.fluid
cp ./pkgs/apps/fluidanimate/inputs/in_300K.fluid ./parsec_testbin_m5/input/fluidanimate.fluid


#-----------------------------------------------------------------------------
#  ___                  _   _             
# / __|_ __ ____ _ _ __| |_(_)___ _ _  ___
# \__ \ V  V / _` | '_ \  _| / _ \ ' \(_-<
# |___/\_/\_/\__,_| .__/\__|_\___/_||_/__/
#                 |_|                     
#-----------------------------------------------------------------------------
# Clean
if [ ! -z $CLEAN ]; then
	print_info "Cleaning swaptions"
	./bin/parsecmgmt -a fullclean -p swaptions -c gcc-pthreads
	./bin/parsecmgmt -a fullclean -p swaptions -c gcc-hooks
	./bin/parsecmgmt -a fulluninstall -p swaptions -c gcc-pthreads
	./bin/parsecmgmt -a fulluninstall -p swaptions -c gcc-hooks
fi

# Build
./bin/parsecmgmt -a build -p swaptions -c gcc-pthreads
./bin/parsecmgmt -a build -p swaptions -c gcc-hooks

# Copy exe
print_info "Copying swaptions Normal"
cp ./pkgs/apps/swaptions/inst/amd64-linux.gcc-pthreads/bin/swaptions ./parsec_testbin
print_info "Copying swaptions m5 Hook"
cp ./pkgs/apps/swaptions/inst/amd64-linux.gcc-hooks/bin/swaptions ./parsec_testbin_m5


#-----------------------------------------------------------------------------
#  ___                   _          
# | __| _ ___ __ _ _ __ (_)_ _  ___ 
# | _| '_/ -_) _` | '  \| | ' \/ -_)
# |_||_| \___\__, |_|_|_|_|_||_\___|
#               |_|                 
#-----------------------------------------------------------------------------
# Clean
if [ ! -z $CLEAN ]; then
	print_info "Cleaning freqmine"
	./bin/parsecmgmt -a fullclean -p freqmine -c gcc-openmp
	./bin/parsecmgmt -a fullclean -p freqmine -c gcc-hooks
	./bin/parsecmgmt -a fulluninstall -p freqmine -c gcc-openmp
	./bin/parsecmgmt -a fulluninstall -p freqmine -c gcc-hooks
fi

# Build
./bin/parsecmgmt -a build -p freqmine -c gcc-openmp
./bin/parsecmgmt -a build -p freqmine -c gcc-hooks

# Copy exe
print_info "Copying freqmine Normal"
cp ./pkgs/apps/freqmine/inst/amd64-linux.gcc-openmp/bin/freqmine ./parsec_testbin
print_info "Copying freqmine m5 Hook"
cp ./pkgs/apps/freqmine/inst/amd64-linux.gcc-hooks/bin/freqmine ./parsec_testbin_m5

# Copy Input Data
print_info "Copying freqmine Input Data"
pushd ./pkgs/apps/freqmine/inputs
tar -xvf input_simlarge.tar
popd
cp ./pkgs/apps/freqmine/inputs/kosarak_990k.dat ./parsec_testbin/input/freqmine.dat
cp ./pkgs/apps/freqmine/inputs/kosarak_990k.dat ./parsec_testbin_m5/input/freqmine.dat


#-----------------------------------------------------------------------------
#   ___                         _ 
#  / __|__ _ _ _  _ _  ___ __ _| |
# | (__/ _` | ' \| ' \/ -_) _` | |
#  \___\__,_|_||_|_||_\___\__,_|_|
#                                 
#-----------------------------------------------------------------------------
# Clean
if [ ! -z $CLEAN ]; then
	print_info "Cleaning canneal"
	./bin/parsecmgmt -a fullclean -p canneal -c gcc-pthreads
	./bin/parsecmgmt -a fullclean -p canneal -c gcc-hooks
	./bin/parsecmgmt -a fulluninstall -p canneal -c gcc-pthreads
	./bin/parsecmgmt -a fulluninstall -p canneal -c gcc-hooks
fi

# Build
./bin/parsecmgmt -a build -p canneal -c gcc-pthreads
./bin/parsecmgmt -a build -p canneal -c gcc-hooks

# Copy exe
print_info "Copying canneal Normal"
cp ./pkgs/kernels/canneal/inst/amd64-linux.gcc-pthreads/bin/canneal ./parsec_testbin
print_info "Copying canneal m5 Hook"
cp ./pkgs/kernels/canneal/inst/amd64-linux.gcc-hooks/bin/canneal ./parsec_testbin_m5

# Copy Input Data
print_info "Copying canneal Input Data"
pushd ./pkgs/kernels/canneal/inputs
tar -xvf input_simlarge.tar
popd
cp ./pkgs/kernels/canneal/inputs/400000.nets ./parsec_testbin/input/canneal.nets
cp ./pkgs/kernels/canneal/inputs/400000.nets ./parsec_testbin_m5/input/canneal.nets


#-----------------------------------------------------------------------------
# __   _____ ___  ___ 
# \ \ / /_ _| _ \/ __|
#  \ V / | ||  _/\__ \
#   \_/ |___|_|  |___/
#                     
#-----------------------------------------------------------------------------
# Clean
if [ ! -z $CLEAN ]; then
	print_info "Cleaning vips"
	./bin/parsecmgmt -a fullclean -p vips -c gcc-pthreads
	./bin/parsecmgmt -a fullclean -p vips -c gcc-hooks
	./bin/parsecmgmt -a fulluninstall -p vips -c gcc-pthreads
	./bin/parsecmgmt -a fulluninstall -p vips -c gcc-hooks
fi

# Build
./bin/parsecmgmt -a build -p vips -c gcc-pthreads
./bin/parsecmgmt -a build -p vips -c gcc-hooks

# Copy exe
print_info "Copying vips Normal"
cp ./pkgs/apps/vips/inst/amd64-linux.gcc-pthreads/bin/vips ./parsec_testbin
print_info "Copying vips m5 Hook"
cp ./pkgs/apps/vips/inst/amd64-linux.gcc-hooks/bin/vips ./parsec_testbin_m5

# Copy Input Data
print_info "Copying vips Input Data"
pushd ./pkgs/apps/vips/inputs
tar -xvf input_simlarge.tar
popd
cp ./pkgs/apps/vips/inputs/bigben_2662x5500.v ./parsec_testbin/input/vips.v
cp ./pkgs/apps/vips/inputs/bigben_2662x5500.v ./parsec_testbin_m5/input/vips.v
