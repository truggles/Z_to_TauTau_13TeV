
ALL=/hdfs/store/user/caillol/SMHTT_aug16_v2


ls ${ALL}/data_MuonEG_Run2016[B,C,D,E,F]/make_ntuples_cfg-*.root                                         > hdfs/dataEM.txt 
ls ${ALL}/data_Tau_Run2016[B,C,D,E,F]/make_ntuples_cfg-*.root                                            > hdfs/dataTT.txt 
ls ${ALL}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                 > hdfs/DYJets.txt 
ls ${ALL}/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                > hdfs/DYJets1.txt 
ls ${ALL}/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                > hdfs/DYJets2.txt 
ls ${ALL}/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                > hdfs/DYJets3.txt 
ls ${ALL}/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                > hdfs/DYJets4.txt 
ls ${ALL}/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/make_ntuples_cfg-*.root     > hdfs/T-tchan.txt 
ls ${ALL}/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/make_ntuples_cfg-*.root > hdfs/Tbar-tchan.txt 
ls ${ALL}/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/make_ntuples_cfg-*.root     > hdfs/Tbar-tW.txt 
ls ${ALL}/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/make_ntuples_cfg-*.root         > hdfs/T-tW.txt 
ls ${ALL}/TT_TuneCUETP8M1_13TeV-powheg-pythia8/make_ntuples_cfg-*.root                                   > hdfs/TT.txt 
ls ${ALL}/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                      > hdfs/WJets.txt 
ls ${ALL}/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                     > hdfs/WJets1.txt 
ls ${ALL}/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                     > hdfs/WJets2.txt 
ls ${ALL}/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                     > hdfs/WJets3.txt 
ls ${ALL}/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                     > hdfs/WJets4.txt 
ls ${ALL}/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/make_ntuples_cfg-*.root                         > hdfs/WW1l1nu2q.txt 
ls ${ALL}/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/make_ntuples_cfg-*.root                         > hdfs/WZ1l1nu2q.txt 
ls ${ALL}/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/make_ntuples_cfg-*.root                           > hdfs/WZ1l3nu.txt 
ls ${ALL}/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/make_ntuples_cfg-*.root                            > hdfs/WZ2l2q.txt 
ls ${ALL}/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/make_ntuples_cfg-*.root                            > hdfs/ZZ2l2q.txt 
ls ${ALL}/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/make_ntuples_cfg-*.root                           > hdfs/VV.txt 
#ls ${ALL}/WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/*/*/make_ntuples_cfg-*                         > hdfs/WZJets.txt
#ls ${ALL}/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/*/*/make_ntuples_cfg-*                           > hdfs/WZ3l1nu.txt 
#ls ${ALL}/ZZTo4L_13TeV-amcatnloFXFX-pythia8/*/*/make_ntuples_cfg-*                                      > hdfs/ZZ4l.txt 
#ls ${DYBIG}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/make_ntuples_cfg-*               > hdfs/DYJetsBig.txt 
#ls ${ALL}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/*/*/make_ntuples_cfg-*                > hdfs/DYJetsFXFX.txt 
#ls ${ALL}/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/make_ntuples_cfg-*             > hdfs/DYJetsLow.txt 
#ls ${ALL}/DYJetsToLL_M-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/make_ntuples_cfg-*.root                > hdfs/DYJetsHigh.txt 


#echo $jobId
#
#for MASS in 80 90 100 110 120 130 140 160 180 200 250 300 350 400 450 500 600 700 800 900 1000 1200 1400 1500 1600 1800 2000 2300 2600 2900 3200; do
#    ls ${ALL}/SUSYGluGluToHToTauTau_M-${MASS}_TuneCUETP8M1_13TeV-pythia8/submit/make_ntuples_cfg-*/make_ntuples_cfg-* > ggH${MASS}.txt
#    ls ${ALL}/SUSYGluGluToBBHToTauTau_M-${MASS}_TuneCUETP8M1_13TeV-pythia8/submit/make_ntuples_cfg-*/make_ntuples_cfg-* > bbH${MASS}.txt
#done

for MASS in 120 125 130; do
    ls ${ALL}/GluGluHToTauTau_M${MASS}_13TeV_powheg_pythia8/make_ntuples_cfg-*.root                      > hdfs/ggHtoTauTau${MASS}.txt
    ls ${ALL}/VBFHToTauTau_M${MASS}_13TeV_powheg_pythia8/make_ntuples_cfg-*.root                         > hdfs/VBFHtoTauTau${MASS}.txt
done



