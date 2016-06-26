
DATA=june26_ztt_data
TT=june26_ztt_TT
BKGS=june26_ztt_MC
SIGNALS=april08_signals
DYBIG=april08_DYJets250Mil



ls /data/truggles/${DATA}/data_Tau_Run2016B_25ns/submit/make_ntuples_cfg-*/*.root                           > data_tt.txt 
#ls /data/truggles/${DATA}/data_MuonEG_Run2015D_16Dec2015_25ns/submit/make_ntuples_cfg-*/*.root              > data_em.txt 
#ls /data/truggles/${DYBIG}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJetsBig.txt 
ls /data/truggles/${BKGS}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                 > DYJets.txt 
ls /data/truggles/${BKGS}/DYJetsToLL_M-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJetsHigh.txt 
ls /data/truggles/${BKGS}/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJets1.txt 
ls /data/truggles/${BKGS}/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJets2.txt 
ls /data/truggles/${BKGS}/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJets3.txt 
ls /data/truggles/${BKGS}/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                > DYJets4.txt 
#ls /data/truggles/${BKGS}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/*/*/*.root                > DYJetsFXFX.txt 
ls /data/truggles/${BKGS}/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root             > DYJetsLow.txt 
ls /data/truggles/${BKGS}/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/*/*/*.root     > T-tchan.txt 
ls /data/truggles/${BKGS}/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/*/*/*.root > Tbar-tchan.txt 
ls /data/truggles/${BKGS}/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/*/*/*.root     > Tbar-tW.txt 
ls /data/truggles/${BKGS}/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/*/*/*.root         > T-tW.txt 
ls /data/truggles/${TT}/TT_TuneCUETP8M1_13TeV-powheg-pythia8/*/*/*.root                                     > TT.txt 
ls /data/truggles/${BKGS}/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                      > WJets.txt 
ls /data/truggles/${BKGS}/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                     > WJets1.txt 
ls /data/truggles/${BKGS}/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                     > WJets2.txt 
ls /data/truggles/${BKGS}/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                     > WJets3.txt 
ls /data/truggles/${BKGS}/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root                     > WJets4.txt 
ls /data/truggles/${BKGS}/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root                         > WW1l1nu2q.txt 
#ls /data/truggles/${BKGS}/WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/*/*/*.root                         > WZJets.txt
ls /data/truggles/${BKGS}/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root                         > WZ1l1nu2q.txt 
ls /data/truggles/${BKGS}/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root                           > WZ1l3nu.txt 
#ls /data/truggles/${BKGS}/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/*/*/*.root                           > WZ3l1nu.txt 
ls /data/truggles/${BKGS}/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root                            > WZ2l2q.txt 
ls /data/truggles/${BKGS}/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root                            > ZZ2l2q.txt 
#ls /data/truggles/${BKGS}/ZZTo4L_13TeV-amcatnloFXFX-pythia8/*/*/*.root                                      > ZZ4l.txt 
ls /data/truggles/${BKGS}/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root                           > VV.txt 


#echo $jobId
#
#for MASS in 80 90 100 110 120 130 140 160 180 200 250 300 350 400 450 500 600 700 800 900 1000 1200 1400 1500 1600 1800 2000 2300 2600 2900 3200; do
#    ls /data/truggles/${SIGNALS}/SUSYGluGluToHToTauTau_M-${MASS}_TuneCUETP8M1_13TeV-pythia8/submit/make_ntuples_cfg-*/*.root > ggH${MASS}.txt
#    ls /data/truggles/${SIGNALS}/SUSYGluGluToBBHToTauTau_M-${MASS}_TuneCUETP8M1_13TeV-pythia8/submit/make_ntuples_cfg-*/*.root > bbH${MASS}.txt
#done
#
#for MASS in 120 125 130; do
#    ls /data/truggles/${SIGNALS}/GluGluHToTauTau_M${MASS}_13TeV_powheg_pythia8/submit/make_ntuples_cfg-*/*.root > ggHtoTauTau${MASS}.txt
#    ls /data/truggles/${SIGNALS}/VBFHToTauTau_M${MASS}_13TeV_powheg_pythia8/submit/make_ntuples_cfg-*/*.root > VBFHtoTauTau${MASS}.txt
#done



