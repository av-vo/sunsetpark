#!/bin/bash

SRC_DIR=../data/protobuf
DST_DIR=../notebooks/als

PROTO_FILE=pulsewaves

rm $DST_DIR/${PROTO_FILE}_pb2.py

protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/$PROTO_FILE.proto

FILE=$DST_DIR/${PROTO_FILE}_pb2.py

if [[ "$?" == "0" && -f "$FILE" ]]
then
    echo "done"
else
	echo "failed"
fi