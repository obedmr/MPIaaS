#!/bin/bash

echo "#--------------------------------------#"
echo "Start"
echo "#--------------------------------------#"

pushd tests/busybox

wget -nc http://www.busybox.net/downloads/busybox-1.22.1.tar.bz2
tar -xvf *.tar.bz2
cd busybox-1.22.1 && make allnoconfig && cd ..
cp .config busybox-1.22.1/.config
cd busybox-1.22.1 && make && cd ..
cd busybox-1.22.1/testsuite && ./runtest

popd
