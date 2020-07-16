#!/bin/bash

# Convert the Stats file to only the PowerPredictor Stats

SRC=$1
ARCHIVE=$2

for file in $(ls $SRC/*.txt); do 
  D=$(basename $file .txt)
  echo "grep \"powerPred\" $file > \"$SRC/$D.out\""
  grep "powerPred" $file > "$SRC/$D.out"
done

if [ ! -d "$SRC/$ARCHIVE" ]; then
  echo "mkdir $SRC/$ARCHIVE"
  mkdir $SRC/$ARCHIVE
fi

echo "mv $SRC/*.txt $SRC/$ARCHIVE/"
mv $SRC/*.txt $SRC/$ARCHIVE/

echo "tar -cvf $SRC/$ARCHIVE.tar.gz $SRC/$ARCHIVE/"
tar -cvf $SRC/$ARCHIVE.tar.gz $SRC/$ARCHIVE/ > /dev/null

echo "xz $SRC/$ARCHIVE.tar.gz"
xz $SRC/$ARCHIVE.tar.gz
