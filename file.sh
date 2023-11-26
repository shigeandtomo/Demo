#!/bin/bash

first_index=0
start_stp=700
end_stp=2000
nat=5
prefix=met

cd ${first_index}0.data
sed -n "$((start_stp+1)),$((end_stp+1))p" $prefix.evp > ${prefix}_2.evp
sed -n "$((nat*start_stp+start_stp-nat)), $((end_stp*nat+end_stp))p" $prefix.for > ${prefix}_2.for
cp $prefix.in ${prefix}_2.in
sed -n "$((nat*start_stp+start_stp-nat)), $((end_stp*nat+end_stp))p" $prefix.pos > ${prefix}_2.pos