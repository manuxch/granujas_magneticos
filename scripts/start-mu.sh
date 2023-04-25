#!/usr/bin/bash

m=1000
cont=0

iname="params-mu.tpl"
for i in $( seq 0 40 2000 )
do
    oname=$(printf "%04d" ${i})
    echo ${i} ${oname}
    in_file=params-mu-${oname}.in
    sed -e "s/__mu__/${i}/g" ${iname} > ${in_file}
    let cont++
done
let cont--
sed -e"s/__N__/${cont}/g" submit.tpl > submit.sh
sbatch submit.sh
