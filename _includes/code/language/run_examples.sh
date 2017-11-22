#!/bin/bash

if [ "$#" -eq 0 ]; then
  n=1
else
  n=$1
fi

for f in `find . -name '*.anglican' -print`
do
  echo Running $f
  anglican -s $f -n $n 2>&1 | awk '/,/ && !/^\[/{st = index($0,","); print substr($0,st+1); next}{print $0}' > $f.output
done
