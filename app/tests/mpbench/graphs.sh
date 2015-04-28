#!/bin/sh

PREFIX=$1

GRAPHS="latency roundtrip bandwidth bibw alltoall broadcast reduce allreduce"

for g in $GRAPHS
do
  echo "gnuplot ${PREFIX}_${g}.gp"
  gnuplot ${PREFIX}_${g}.gp
  if [ $? -ne 0 ]; then
    gperr=1
  else
    echo "Postscript graph is in ${PREFIX}_${g}.ps."
    gperr=0
  fi
done
