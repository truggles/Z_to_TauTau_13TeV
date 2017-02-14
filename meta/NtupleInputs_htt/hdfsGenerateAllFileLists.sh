
#ALL=/hdfs/store/user/truggles/SMHTT_mc_jan23_JES
#DATA=/hdfs/store/user/caillol/SMHTT_data_jan17
ALL=/hdfs/store/user/truggles/SMHTT_jan31
V2=/hdfs/store/user/truggles/SMHTT_jan31_v2

ls ${ALL}/data_Tau_Run2016B_v3/*.root                                            		 > hdfs/dataTT-B.txt 
ls ${ALL}/data_Tau_Run2016C/*.root                                            		     > hdfs/dataTT-C.txt 
ls ${ALL}/data_Tau_Run2016D/*.root                                            		     > hdfs/dataTT-D.txt 
ls ${V2}/data_Tau_Run2016E/*.root                                            		     > hdfs/dataTT-E.txt 
ls ${ALL}/data_Tau_Run2016F/*.root                                            		     > hdfs/dataTT-F.txt 
ls ${ALL}/data_Tau_Run2016G/*.root                                            		     > hdfs/dataTT-G.txt 
ls ${ALL}/data_Tau_Run2016H_v1/*.root                                            		 > hdfs/dataTT-H.txt 
ls ${ALL}/data_Tau_Run2016H_v2/*.root                                            		 >> hdfs/dataTT-H.txt 
ls ${ALL}/data_Tau_Run2016H_v3/*.root                                            		 >> hdfs/dataTT-H.txt 
ls ${ALL}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6_ext1-v2/*.root                 > hdfs/DYJets.txt 
ls ${ALL}/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root                > hdfs/DYJets1.txt 
ls ${ALL}/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root                > hdfs/DYJets2.txt 
ls ${ALL}/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root                > hdfs/DYJets3.txt 
ls ${ALL}/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root                > hdfs/DYJets4.txt 
ls ${ALL}/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root             > hdfs/DYJetsLow.txt 
ls ${ALL}/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_v6-v1/*.root > hdfs/Tbar-tchan.txt 
ls ${ALL}/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_v6-v1/*.root     > hdfs/T-tchan.txt 
ls ${ALL}/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v6_ext1-v1/*.root     > hdfs/Tbar-tW.txt 
ls ${ALL}/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v6_ext1-v1/*.root         > hdfs/T-tW.txt 
ls ${ALL}/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_v6-v1/*.root                                   > hdfs/TT.txt 
ls ${ALL}/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8_v6_ext1-v1/*.root                           > hdfs/VV.txt 
ls ${ALL}/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6*-v1/*.root                      > hdfs/WJets.txt 
ls ${ALL}/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6*-v1/*.root                     > hdfs/WJets1.txt # Wildcard should get WJets extensions as the come in
ls ${ALL}/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6*-v1/*.root                     > hdfs/WJets2.txt 
ls ${ALL}/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6*-v1/*.root                     > hdfs/WJets3.txt 
ls ${ALL}/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6*-v1/*.root                     > hdfs/WJets4.txt 
ls ${ALL}/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8_v6-v1/*.root                         > hdfs/WW1l1nu2q.txt 
ls ${ALL}/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                             > hdfs/WWW.txt
ls ${ALL}/WW_TuneCUETP8M1_13TeV-pythia8_v6*-v1/*.root                                          > hdfs/WW.txt
ls ${ALL}/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8_v6-v1/*.root                           > hdfs/WZ3l1nu.txt 
ls ${ALL}/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8_v6-v3/*.root                         > hdfs/WZ1l1nu2q.txt 
ls ${ALL}/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_v6-v1/*.root                           > hdfs/WZ1l3nu.txt 
ls ${ALL}/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_v6-v1/*.root                            > hdfs/WZ2l2q.txt 
ls ${ALL}/WZ_TuneCUETP8M1_13TeV-pythia8_v6*-v1/*.root                            > hdfs/WZ.txt 
ls ${ALL}/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_v6-v1/*.root                            > hdfs/ZZ2l2q.txt 
###ls ${ALL}/EWKWPlus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8_v6-v1/*.root                       > hdfs/EWKWPlus.txt
###ls ${ALL}/EWKWMinus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8_v6-v1/*.root                      > hdfs/EWKWMinus.txt
###ls ${ALL}/EWKZ2Jets_ZToLL_M-50_13TeV-madgraph-pythia8_v6-v1/*.root                            > hdfs/EWKZ2l.txt
###ls ${ALL}/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8_v6-v1/*.root                               > hdfs/EWKZ2nu.txt
#ls ${ALL}/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                                > hdfs/WWZ.txt
###ls ${ALL}/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                                > hdfs/ZZZ.txt
#ls ${ALL}/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                                > hdfs/WZZ.txt
ls ${ALL}/ZZ_TuneCUETP8M1_13TeV-pythia8_v6-v1/*.root                                          > hdfs/ZZ.txt
#ls ${ALL}/WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v6-v1/*/*/*                         > hdfs/WZJets.txt
ls ${ALL}/ZZTo4L_13TeV-amcatnloFXFX-pythia8_v6_ext1-v1/*.root                                      > hdfs/ZZ4l.txt 


#for MASS in 120 125 130; do
for MASS in 125; do
    ls ${ALL}/GluGluHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                      > hdfs/ggHtoTauTau${MASS}.txt
    ls ${ALL}/VBFHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                         > hdfs/VBFHtoTauTau${MASS}.txt
    ls ${ALL}/GluGluHToWWTo2L2Nu_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root            > hdfs/HtoWW2l2nu${MASS}.txt
    #ls ${ALL}/VBFHToWWTo2L2Nu_M${MASS}_13TeV_powheg_JHUgen_pythia8_v6-v1/*.root            > hdfs/VBFHtoWW2l2nu${MASS}.txt
    ls ${ALL}/WminusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                        > hdfs/WMinusHTauTau${MASS}.txt
    ls ${ALL}/WplusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                         > hdfs/WPlusHTauTau${MASS}.txt
    ls ${ALL}/ZHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                             > hdfs/ZHTauTau${MASS}.txt
done



