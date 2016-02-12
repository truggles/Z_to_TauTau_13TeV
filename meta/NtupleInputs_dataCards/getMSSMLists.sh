#!/bin/bash

#export jobId=jan25_mssmAndHiggs76x
export jobId=feb10_bkgsAndSignals
echo $jobId

for MASS in 80 90 100 110 120 130 140 160 180 200 250 300 350 400 450 500 600 700 800 900 1000 1200 1400 1500 1600 1800 2000 2300 2600 2900 3200; do
    echo "ls /data/truggles/${jobId}/SUSYGluGluToHToTauTau_M-${MASS}_TuneCUETP8M1_13TeV-pythia8/submit/make_ntuples_cfg-*/*.root > ggH${MASS}.txt"
    ls /data/truggles/${jobId}/SUSYGluGluToHToTauTau_M-${MASS}_TuneCUETP8M1_13TeV-pythia8/submit/make_ntuples_cfg-*/*.root > ggH${MASS}.txt
done

for MASS in 80 90 100 110 120 130 140 160 180 200 250 300 350 400 450 500 600 700 800 900 1000 1200 1400 1500 1600 1800 2000 2300 2600 2900 3200; do
    echo "ls /data/truggles/${jobId}/SUSYGluGluToBBHToTauTau_M-${MASS}_TuneCUETP8M1_13TeV-pythia8/submit/make_ntuples_cfg-*/*.root > bbH${MASS}.txt"
    ls /data/truggles/${jobId}/SUSYGluGluToBBHToTauTau_M-${MASS}_TuneCUETP8M1_13TeV-pythia8/submit/make_ntuples_cfg-*/*.root > bbH${MASS}.txt
done

for MASS in 120 125 130; do
    echo "ls /data/truggles/jan25_mssmAndHiggs76x/GluGluHToTauTau_M${MASS}_13TeV_powheg_pythia8/submit/make_ntuples_cfg-*/*.root > ggHtoTauTau${MASS}.txt"
    ls /data/truggles/jan25_mssmAndHiggs76x/GluGluHToTauTau_M${MASS}_13TeV_powheg_pythia8/submit/make_ntuples_cfg-*/*.root > ggHtoTauTau${MASS}.txt
    echo "ls /data/truggles/jan25_mssmAndHiggs76x/VBFHToTauTau_M${MASS}_13TeV_powheg_pythia8/submit/make_ntuples_cfg-*/*.root > VBFHtoTauTau${MASS}.txt"
    ls /data/truggles/jan25_mssmAndHiggs76x/VBFHToTauTau_M${MASS}_13TeV_powheg_pythia8/submit/make_ntuples_cfg-*/*.root > VBFHtoTauTau${MASS}.txt
done
