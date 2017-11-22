#!/bin/bash

script='BEGIN { SUBSEP=" = "; } { vars[$1,$2] += 1; N[$1]+=1 } END { for (val in vars) { split(val,sep,SUBSEP); print "p("val") = "vars[val]/N[sep[1]] } }'

if [ -t 0 ]; then
    # script running interactively
    grep -v "^walltime(iteration" $1 | awk -F, "${script}" | sort
else
    # stdin coming from a pipe or file
    grep -v "^walltime(iteration" | awk -F, "${script}" | sort
fi

