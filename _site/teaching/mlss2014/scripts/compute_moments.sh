#!/bin/bash

script='{ sum[$1]+=$2; m2[$1]+=($2*$2); N[$1]+=1; } END { for (name in sum) { print "E["name"] = "sum[name]/N[name]"; Var["name"] = "(m2[name] - sum[name]*sum[name]/N[name])/N[name] }}'

if [ -t 0 ]; then
    # script running interactively
    grep -v "walltime(iteration" $1 | awk -F, "${script}" | sort
else
    # stdin coming from a pipe or file
    grep -v "walltime(iteration" | awk -F, "${script}" | sort
fi
