#!/bin/bash

DATA_DIR=../data

#find $DATA_DIR/pw -type f -exec rm -rf {} \;
#find $DATA_DIR/pwmsg -type f -exec rm -rf {} \;
#find $DATA_DIR/laz -type f -exec rm -rf {} \;

DIRS=$(ls $DATA_DIR)

for DIR in $DIRS
do
	#echo "$DIR"
	if [[ ( "$DIR" != "sample" ) && ( "$DIR" != "metadata" ) && ( "$DIR" != "protobuf" ) ]]
	then
		echo "removing $DATA_DIR/$DIR"
		rm -rf $DATA_DIR/$DIR
	fi
done 
