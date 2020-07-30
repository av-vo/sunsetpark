#!/bin/bash

DATA_DIR=../data

find $DATA_DIR/pw -type f -exec rm -rf {} \;
find $DATA_DIR/pwmsg -type f -exec rm -rf {} \;
find $DATA_DIR/laz -type f -exec rm -rf {} \;
