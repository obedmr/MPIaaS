#!/bin/bash

echo "#--------------------------------------#"
echo "Start"
echo "#--------------------------------------#"

pushd test &> /dev/null
#./runtest -v > ../busybox.log 2>&1
./runtest -v | tee ../busybox.log
popd &> /dev/null

