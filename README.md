# Z_to_TauTau_13TeV
This repository is for the CMS analysis of Z -> TauTau (emu and di-hadronic tau final states) at 13TeV

The analysis relies on flat Ntuple output from UW's Final State Analysis: https://github.com/uwcms/FinalStateAnalysis/tree/miniAOD_dev

1. make a list of all FSA ntuples by background / data sample in 'meta/NtupleInputs_[25/50]ns'

2. make sure DAS paths are all in makeMeta.py, and run it gather meta info on samples

3. run analysis0PUTemplates to generate nvtx pile up reweighting templates

4. run all samples though analysis1BaselineCuts.py do:
    a. Initial cuts
    b. Isolation order and pick perfered event permutation
    c. Generate you historgrams

5. run python analysis1BaselineCuts.py --bkgs=WJets to make a smooth WJets background shape

6. QCD...

8. TT...

9. Plot your histos with analysis3Plots.py
