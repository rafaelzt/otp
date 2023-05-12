#!/bin/sh

SIZE=32
FILE_NAME="key.hex"

openssl rand -hex $SIZE > $FILE_NAME 
tr -d '\n' < $FILE_NAME > $FILE_NAME.tmp
rm $FILE_NAME && mv $FILE_NAME.tmp $FILE_NAME

echo "Generated $FILE_NAME with $SIZE bytes"
