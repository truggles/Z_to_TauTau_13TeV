
DATA=july21_azh_data
BKGS=june25_AtoZh80X
SIG=july31_azh
ZZ=july19_azh_ZZ
ZZAMCNLO=aug02_azh
WZ=july21_azh_WZ_2
TT=july28_azh_TT
DY=july28_azh_DY
DYJB=july29_azh_DYjb
ALL=aug03_azh
reHLT=aug04_azh

ls /data/truggles/${ALL}/data_DoubleMuon_Run2016*_25ns/submit/make_ntuples_cfg-*/*.root                  > dataMM.txt 
ls /data/truggles/${ALL}/data_DoubleEG_Run2016*_25ns/submit/make_ntuples_cfg-*/*.root                    > dataEE.txt 
ls /data/truggles/${ALL}/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root              > DYJets1.txt 
ls /data/truggles/${ALL}/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root              > DYJets2.txt 
ls /data/truggles/${ALL}/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root              > DYJets3.txt 
ls /data/truggles/${ALL}/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root              > DYJets4.txt 
ls /data/truggles/${ALL}/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8/*/*/*.root                      > ggZZ2e2m.txt
ls /data/truggles/${ALL}/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8/*/*/*.root                     > ggZZ2e2tau.txt
ls /data/truggles/${ALL}/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/*/*/*.root                    > ggZZ2m2tau.txt
ls /data/truggles/${ALL}/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/*/*/*.root                         > ggZZ4e.txt
ls /data/truggles/${ALL}/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/*/*/*.root                        > ggZZ4m.txt
ls /data/truggles/${ALL}/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8/*/*/*.root                       > ggZZ4tau.txt
#ls /data/truggles/${ALL}/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                   > TTJ.txt
#ls /data/truggles/${ALL}/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/*/*/*.root                               > TTTT.txt
#ls /data/truggles/${ALL}/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/*/*/*.root                   > TTZ.txt
ls /data/truggles/${ALL}/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/*/*/*.root                           > WZ3l1nu.txt
ls /data/truggles/${ZZ}/ZZTo4L_13TeV_powheg_pythia8/*/*/*.root                                           > ZZ4l.txt
ls /data/truggles/${reHLT}/ZZTo4L_13TeV-amcatnloFXFX-pythia8/*/*/*.root                                  > ZZ4lAMCNLO.txt
ls /data/truggles/${ALL}/TT_TuneCUETP8M1_13TeV-powheg-pythia8/*/*/*.root                                 > TT.txt
ls /data/truggles/${ALL}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root               > DYJets.txt

# Higgs associated
ls /data/truggles/${reHLT}/WminusHToTauTau_M125_13TeV_powheg_pythia8/*/*/*.root                          > WMinusHTauTau.txt
ls /data/truggles/${reHLT}/WplusHToTauTau_M125_13TeV_powheg_pythia8/*/*/*.root                           > WPlusHTauTau.txt
ls /data/truggles/${reHLT}/ZHToTauTau_M125_13TeV_powheg_pythia8/*/*/*.root                               > ZHTauTau.txt
ls /data/truggles/${reHLT}/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root                 > ttHTauTau.txt


for MASS in 220 240 260 280 300 320 350 400; do
    ls /data/truggles/${reHLT}/AToZhToLLTauTau_M-${MASS}_13TeV_madgraph_4f_LO/submit/make_ntuples_cfg-*/*.root > azh${MASS}.txt
done



