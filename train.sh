#!/bin/bash

label=2
echo "first index = ${label}"
cp ./${label}1.train/input.json .
rm -r ${label}1.train
mkdir ${label}1.train
mv input.json ./${label}1.train
cd ${label}1.train
dp train input.json
dp freeze -o graph.pb
dp compress -i graph.pb -o graph-compress.pb
dp test -m graph-compress.pb -s ../${label}0.data/validation_data -n 40 -d results
