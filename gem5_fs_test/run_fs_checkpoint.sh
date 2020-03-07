#!/bin/bash

GEM5_DIR='/home/andrew/research/gem5'
GEM5_BUILD='build/X86/gem5.opt'
RCS_SCRIPT='/home/andrew/research/gem5_fs_test/cp.rcs'
CONFIG_FILE='configs/example/fs.py'
#IMAGE='/home/andrew/research/gem5_fs_test/disks/m5_exit.squashfs.arm'
IMAGE='/home/andrew/research/gem5_fs_test/disks/linux-x86.img'
#IMAGE='/home/andrew/research/gem5_fs_test/disks/linux-x86_new_m5.img'
#IMAGE='benchmarks/FSmode/disks/aarch32-ubuntu-natty-headless.img'
KERNEL='/home/andrew/research/gem5_fs_test/binaries/x86_64-vmlinux-2.6.22.9'
#DTB='/home/andrew/research/gem5/system/arm/dt/armv7_gem5_v1_1cpu.dtb'
CHKPT_DIR='/home/andrew/research/gem5_fs_test/checkpoint'

$GEM5_DIR/$GEM5_BUILD -d ./checkpoint \
  --debug-flags=SyscallVerbose,PseudoInst,DistEthernet \
  $GEM5_DIR/$CONFIG_FILE \
  --script=$RCS_SCRIPT \
  --disk-image=$IMAGE \
  --cpu-type=AtomicSimpleCPU \
  --kernel=$KERNEL \
  --num-cpus=2 --caches --l2cache \
  --checkpoint-dir=$CHKPT_DIR
#  --checkpoint-at-end
#  --dtb-file=$DTB \
#  --machine-type=VExpress_GEM5_V1 \
#  --script=$RCS_SCRIPT \
#  --checkpoint-dir=$CHKPT_DIR -r 1
#  --mem-size=32GB \
#  --mem-channels=8 \
#  --mem-ranks=2 \
#  --mem-type=DDR4_2400_16x4 \
