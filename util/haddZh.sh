#!/usr/bin/env bash

pushd ${1}

for CHAN in eeet eett eemt eeem emmt mmtt mmmt emmm; do 
    hadd -f ZHTauTau125_${CHAN}.root ZHTauTau125_*_${CHAN}.root
done

popd
