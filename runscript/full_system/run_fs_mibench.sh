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

script_name="run_fs_mibench.sh"

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

#--------------------------------------------------------------------
# Check Environment
#--------------------------------------------------------------------
if [ -z "$VSIM_TOOLS" ]; then
  print_error "VSIM_TOOLS not set; source setup.sh"
  exit
fi
if [ -z "$PREDICT_T_ROOT" ]; then
  print_error "PREDICT_T_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$GEM5_ROOT" ]; then
  print_error "GEM5_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$OUTPUT_ROOT" ]; then
  print_error "OUTPUT_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$MCPAT_ROOT" ]; then
  print_error "OUTPUT_ROOT not set; source setup.sh"
  exit
fi
if [ -z "$SIM_ROOT" ]; then
  print_error "SIM_ROOT not set; source setup.sh"
  exit 1
fi
if [ -z "$VSIM_IMAGE" ]; then
  print_error "VSIM_IMAGE not set; source setup.sh"
  exit 1
fi
print_info "VSIM_TOOLS $VSIM_TOOLS"
print_info "PREDICT_T_ROOT $PREDICT_T_ROOT"
print_info "GEM5_ROOT $GEM5_ROOT"
print_info "OUTPUT_ROOT $OUTPUT_ROOT"
print_info "MCPAT_ROOT $MCPAT_ROOT"
print_info "SIM_ROOT $SIM_ROOT"
print_info "VSIM_IMAGE $VSIM_IMAGE"

source $PREDICT_T_ROOT/runscript/util.sh

if [[ -z $(docker images -q $VSIM_IMAGE) ]]; then
  print_error "Docker container $VSIM_IMAGE is not built; source setup.sh"
  exit 1
fi

#RCS_SCRIPT="${PREDICT_T_ROOT}/runscript/full_system/cp.rcs"
RCS_SCRIPT="${PREDICT_T_ROOT}/runscript/full_system/run_mibench.rcs"
CONFIG_FILE="${GEM5_ROOT}/configs/example/fs.py"
#IMAGE="${PREDICT_T_ROOT}/runscript/full_system/disks/base.img"
#IMAGE="${PREDICT_T_ROOT}/runscript/full_system/disks/linux-x86.img"
IMAGE="${PREDICT_T_ROOT}/runscript/full_system/disks/x86root-parsec.img"
#IMAGE="${PREDICT_T_ROOT}/runscript/full_system/disks/linux-x86-5.4.44.img"

#KERNEL="${PREDICT_T_ROOT}/runscript/full_system/binaries/x86_64-vmlinux-4.9.186"
#KERNEL="${PREDICT_T_ROOT}/runscript/full_system/binaries/x86_64-vmlinux-2.6.22.9"
KERNEL="${PREDICT_T_ROOT}/runscript/full_system/binaries/x86_64-vmlinux-2.6.28.4-smp"
#KERNEL="${PREDICT_T_ROOT}/runscript/full_system/binaries/x86_64-vmlinux-5.4.44"
CHKPT_DIR="${OUTPUT_ROOT}/gem5_cpt"
G5_OUT="${OUTPUT_ROOT}/gem5_out"

TN="fs_mibench_derivO3_4"
CPT="fs_cpt_AtomicSimpleCPU_4"

$GEM5_ROOT/build/X86/gem5.opt \
  -d ${G5_OUT}/$TN \
  $CONFIG_FILE \
  --script=$RCS_SCRIPT \
  --disk-image=$IMAGE \
  --kernel=$KERNEL \
  --num-cpus=4 \
  --caches \
  --l2cache \
  --checkpoint-dir=$CHKPT_DIR/$CPT -r 1 \
  --cpu-type=DerivO3CPU \
  --num-l2caches=4

#gdb --args $GEM5_ROOT/build/X86/gem5.debug \
#  -d ${G5_OUT}/$TN \
#  $CONFIG_FILE \
#  --script=$RCS_SCRIPT \
#  --disk-image=$IMAGE \
#  --kernel=$KERNEL \
#  --num-cpus=4 \
#  --caches \
#  --l2cache \
#  --checkpoint-dir=$CHKPT_DIR/$CPT -r 1 \
#  --cpu-type=DerivO3CPU \
#  --num-l2caches=4

#  --cpu-type=DerivO3CPU \
#  --cpu-type=AtomicSimpleCPU \
#  --restore-with-cpu=DerivO3CPU \
#  --script=$RCS_SCRIPT \
#  --checkpoint-dir=$CHKPT_DIR -r 1
#  --checkpoint-at-end
#  --dtb-file=$DTB \
#  --machine-type=VExpress_GEM5_V1 \
#  --script=$RCS_SCRIPT \
#  --mem-size=32GB \
#  --mem-channels=8 \
#  --mem-ranks=2 \
#  --mem-type=DDR4_2400_16x4 \

#$GEM5_ROOT/build/X86/gem5.opt \
#  -d ${CHKPT_DIR}/$TN \
#  $CONFIG_FILE \
#  --cpu-type=AtomicSimpleCPU \
#  --disk-image=$IMAGE \
#  --kernel=$KERNEL \
#  --num-cpus=4 --ruby \
#  --caches --l2cache --l2_size=512kB --num-dirs=4 --num-l2=4 \
#  --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 \
