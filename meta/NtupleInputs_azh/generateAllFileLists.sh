
DATA=june25_data
BKGS=june25_AtoZh80X



ls /data/truggles/${DATA}/data_DoubleMuon_Run2016B_25ns/submit/make_ntuples_cfg-*/*.root                    > data_mm.txt 
ls /data/truggles/${DATA}/data_DoubleEG_Run2016B_25ns/submit/make_ntuples_cfg-*/*.root                      > data_ee.txt 
ls /data/truggles/${BKGS}/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJets1.txt 
ls /data/truggles/${BKGS}/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJets2.txt 
ls /data/truggles/${BKGS}/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJets3.txt 
ls /data/truggles/${BKGS}/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJets4.txt 
ls /data/truggles/${BKGS}/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/*/*/*.root                      > ggZZ2m2t.txt
ls /data/truggles/${BKGS}/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/*/*/*.root                           > ggZZ4e.txt
ls /data/truggles/${BKGS}/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/*/*/*.root                          > ggZZ4m.txt
ls /data/truggles/${BKGS}/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                   > TTJ.txt
ls /data/truggles/${BKGS}/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/*/*/*.root                               > TTTT.txt
ls /data/truggles/${BKGS}/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/*/*/*.root                   > TTZ.txt
ls /data/truggles/${BKGS}/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/*/*/*.root                             > WZ3l1nu.txt
ls /data/truggles/${BKGS}/WminusHToTauTau_M125_13TeV_powheg_pythia8/*/*/*.root                              > WplusHtoTauTau.txt
ls /data/truggles/${BKGS}/WplusHToTauTau_M125_13TeV_powheg_pythia8/*/*/*.root                               > WminusHtoTauTau.txt
ls /data/truggles/${BKGS}/ZHToTauTau_M125_13TeV_powheg_pythia8/*/*/*.root                                   > ZHtoTauTau.txt
ls /data/truggles/${BKGS}/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root                            > ZZ2l2q.txt
ls /data/truggles/${BKGS}/ZZTo4L_13TeV_powheg_pythia8/*/*/*.root                                            > ZZ4l.txt







