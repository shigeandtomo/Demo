#!/bin/bash

first_index=3
start_stp=1
end_stp=1000
nat=16
omx_input_name="Cdia"
System_name="cdia"

# (start_stp- 1)*(nat+2) + 1=start_stp*nat-nat+2*start_stp-1
# end_stp*(nat+2)=end_stp*nat+2*end_stp
cd ${first_index}0.data
cp ${omx_input_name}.dat ${omx_input_name}_2.dat
# sed -n "$((start_stp+1)),$((end_stp+1))p" $prefix.evp > ${prefix}_2.evp
sed -n "$((start_stp*nat-nat+2*start_stp-1)), $((end_stp*nat+2*end_stp))p" ${System_name}.md > ${System_name}_2.md
# sed -n "12601, 14000p" ${prefix}.md > ${prefix}_2.md