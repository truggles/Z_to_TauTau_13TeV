#!/usr/bin/env bash

pushd ${1}

for CHAN in eeet eett eemt eeem emmt mmtt mmmt emmm eeee mmmm; do 
    hadd -f azh300_${CHAN}.root azh300_*_${CHAN}.root
done

popd
