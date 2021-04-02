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

script_name="unit_test.sh"

print_info () {
  echo -e "[ $script_name ] $1"
}

print_pass () {
  green="\e[32m"
  nc="\e[0m"
  echo -e "$green[ $script_name ] PASS:$nc $1"
}

print_error () {
  red="\e[31m"
  nc="\e[0m"
  echo -e "$red[ $script_name ] ERROR:$nc $1"
}

print_test_results () {
  green="\e[32m"
  red="\e[31m"
  nc="\e[0m"
  echo -e "[ $script_name ] Passed $green$1$nc; Failed $red$2$nc; out of $3 Unit Tests"
}


#--------------------------------------------------------------------
# Check Environment
#  _____ _   ___     __   ____ _   _ _____ ____ _  __
# | ____| \ | \ \   / /  / ___| | | | ____/ ___| |/ /
# |  _| |  \| |\ \ / /  | |   | |_| |  _|| |   | ' / 
# | |___| |\  | \ V /   | |___|  _  | |__| |___| . \ 
# |_____|_| \_|  \_/     \____|_| |_|_____\____|_|\_\
#                                                    
#--------------------------------------------------------------------
if [ -z "$MCPAT_ROOT" ]; then
  print_error "MCPAT_ROOT not set; source setup.sh"
  exit
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
OUTPUT="./test_output"
if [ ! -d $OUTPUT ]; then
  print_info "Creating $OUTPUT"
  mkdir -p $OUTPUT
else
  print_info "Cleaning $OUTPUT"
  rm $OUTPUT/*
fi

GOLDEN="./test_expected"

TEST="./tmp"
if [ ! -d $TEST ]; then
  print_info "Creating $TEST"
  mkdir -p $TEST
else
  print_info "Cleaning $TEST"
  rm $TEST/*
fi
cp *.py $TEST/

#--------------------------------------------------------------------
# Run Tests
#  _____ _____ ____ _____ ____  
# |_   _| ____/ ___|_   _/ ___| 
#   | | |  _| \___ \ | | \___ \ 
#   | | | |___ ___) || |  ___) |
#   |_| |_____|____/ |_| |____/ 
#                             
#--------------------------------------------------------------------
INPUT="./test_input"
PASS_COUNT=0
TOTAL_COUNT=0
FAIL_COUNT=0
for t in $(ls $INPUT); do 
  TOTAL_COUNT=$((TOTAL_COUNT + 1))
  python $TEST/__init__.py $INPUT/$t/stats.txt $INPUT/$t/config.ini $OUTPUT/$t.xml > $OUTPUT/$t.out 2> $OUTPUT/$t.err
  if [ -s $OUTPUT/$t.err ] || [ ! -s $OUTPUT/$t.xml ];
  then
    print_error "$t Autogen; check $OUTPUT/$t.err"
    FAIL_COUNT=$((FAIL_COUNT + 1))
  #else
		#$MCPAT_ROOT/mcpat -i $OUTPUT/$t.xml > $OUTPUT/${t}_mcpat.out 2> $OUTPUT/${t}_mcpat.err
		#if [ -s $OUTPUT/${t}_mcpat.err ];
		#then
    #  print_error "$t McPAT; check $OUTPUT/${t}_mcpat.err"
    #  FAIL_COUNT=$((FAIL_COUNT + 1))
    #else
    #  if [ $(grep -rnI "nan\|inf" $OUTPUT/${t}_mcpat.out | wc -l) -eq 0 ];
    #  then
    #    if [ $(diff $GOLDEN/$t.out $OUTPUT/${t}_mcpat.out | wc -l) -eq 0 ];
    #    then
    #      print_pass "$t"
    #      PASS_COUNT=$((PASS_COUNT + 1))
    #    else
    #      print_error "$t MCPAT; differed from expected output"
    #      FAIL_COUNT=$((FAIL_COUNT + 1))
    #    fi
    #  else
    #    print_error "$t MCPAT; found nan/inf in output"
    #    FAIL_COUNT=$((FAIL_COUNT + 1))
    #  fi
    #fi
  fi
done
print_test_results $PASS_COUNT $FAIL_COUNT $TOTAL_COUNT
