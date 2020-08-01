#!/bin/bash

# Fetch Sunset Park and Dublin data from NYU SDR
# Usage:
# Example: ./fetch.sh d15 115601 pc

PROJECT=$1
RECORD=$2
TYPE=$3

# move to the directory that contains the script 
cd $(dirname $0)

case "$TYPE" in
	pc)
		TAG="\<.*pc.*$RECORD.*\>"
		DST_DIR=../data/pc-laz
		;;
	fwf-las)
		TAG="\<.*fwf_las.*$RECORD.*\>"
		DST_DIR=../data/fwf-las
		;;
	fwf-pw)
		TAG="\<.*fwf_plswvs.*$RECORD.*\>"
		DST_DIR=../data/fwf-pw
		;;
	*)
		"$TYPE is not a known type\nAvailable type: [pc, fwf-las, fwf-pw]"
		exit 1
esac 

TMP_DIR="tmp$(date +%s).$$"  &&
grep $TAG ../data/metadata/$PROJECT-bitstreams.json | tr -d ',' | xargs wget -nd --no-check-certificate -P $TMP_DIR &&
unzip $TMP_DIR/*.zip -d $TMP_DIR && rm -rf $TMP_DIR/*.zip &&
mkdir -p $DST_DIR  &&
find $TMP_DIR -type f -exec echo "moving" {} "to $DST_DIR" \; -exec mv {} $DST_DIR \; && 
rm -rf $TMP_DIR &&
echo "Check $(realpath $DST_DIR) for output"