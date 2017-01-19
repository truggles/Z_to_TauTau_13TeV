
ALL=/hdfs/store/user/caillol/LLTT_jan14

ls ${ALL}/data_DoubleMuon_Run2016B-v3/*.root                                              > hdfs/dataMM-B.txt 
ls ${ALL}/data_DoubleMuon_Run2016C/*.root                                                 > hdfs/dataMM-C.txt 
ls ${ALL}/data_DoubleMuon_Run2016D/*.root                                                 > hdfs/dataMM-D.txt 
ls ${ALL}/data_DoubleMuon_Run2016E/*.root                                                 > hdfs/dataMM-E.txt 
ls ${ALL}/data_DoubleMuon_Run2016F/*.root                                                 > hdfs/dataMM-F.txt 
ls ${ALL}/data_DoubleMuon_Run2016G/*.root                                                 > hdfs/dataMM-G.txt 
ls ${ALL}/data_DoubleMuon_Run2016H_v1/*.root                                              > hdfs/dataMM-H.txt 
ls ${ALL}/data_DoubleMuon_Run2016H_v2/*.root                                              >> hdfs/dataMM-H.txt # Combine all H into 1 file
ls ${ALL}/data_DoubleMuon_Run2016H_v3/*.root                                              >> hdfs/dataMM-H.txt 

ls ${ALL}/data_DoubleEG_Run2016B_v3/*.root                                                > hdfs/dataEE-B.txt 
ls ${ALL}/data_DoubleEG_Run2016C/*.root                                                   > hdfs/dataEE-C.txt 
ls ${ALL}/data_DoubleEG_Run2016D/*.root                                                   > hdfs/dataEE-D.txt 
ls ${ALL}/data_DoubleEG_Run2016E/*.root                                                   > hdfs/dataEE-E.txt 
ls ${ALL}/data_DoubleEG_Run2016F/*.root                                                   > hdfs/dataEE-F.txt 
ls ${ALL}/data_DoubleEG_Run2016G/*.root                                                   > hdfs/dataEE-G.txt 
ls ${ALL}/data_DoubleEG_Run2016H_v1/*.root                                                > hdfs/dataEE-H.txt 
ls ${ALL}/data_DoubleEG_Run2016H_v2/*.root                                                >> hdfs/dataEE-H.txt 
ls ${ALL}/data_DoubleEG_Run2016H_v3/*.root                                                >> hdfs/dataEE-H.txt 


ls ${ALL}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6_ext1-v2/*.root        > hdfs/DYJets.txt
ls ${ALL}/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root            > hdfs/DYJets1.txt 
ls ${ALL}/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root            > hdfs/DYJets2.txt 
ls ${ALL}/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root            > hdfs/DYJets3.txt 
ls ${ALL}/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root            > hdfs/DYJets4.txt 
ls ${ALL}/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8_v6-v1/*.root                    > hdfs/ggZZ2e2m.txt
ls ${ALL}/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8_v6-v1/*.root                   > hdfs/ggZZ2e2tau.txt
ls ${ALL}/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8_v6-v1/*.root                  > hdfs/ggZZ2m2tau.txt
ls ${ALL}/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8_v6-v1/*.root                       > hdfs/ggZZ4e.txt
ls ${ALL}/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8_v6-v1/*.root                      > hdfs/ggZZ4m.txt
ls ${ALL}/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8_v6-v1/*.root                     > hdfs/ggZZ4tau.txt
#ls ${ALL}/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root               > hdfs/TTJ.txt
#ls ${ALL}/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                           > hdfs/TTTT.txt
#ls ${ALL}/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root               > hdfs/TTZ.txt
ls ${ALL}/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_v6-v1/*.root                               > hdfs/TT.txt
ls ${ALL}/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                         > hdfs/WWW.txt
ls ${ALL}/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                            > hdfs/WWZ.txt
ls ${ALL}/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8_v6-v1/*.root                       > hdfs/WZ3l1nu.txt
#ls ${ALL}/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8_v6-v1/*.root                         > hdfs/WZ3l1nu.txt
ls ${ALL}/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                            > hdfs/WZZ.txt
ls ${ALL}/WZ_TuneCUETP8M1_13TeV-pythia8_v6-v1//*.root                                     > hdfs/WZ.txt
ls ${ALL}/ZZTo4L_13TeV_powheg_pythia8_v6-v1/*.root                                        > hdfs/ZZ4l.txt
#ls ${ALL}/ZZTo4L_13TeV-amcatnloFXFX-pythia8_v6-v1/*.root                                  > hdfs/ZZ4lAMCNLO.txt
ls ${ALL}/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                            > hdfs/ZZZ.txt
ls ${ALL}/ZZ_TuneCUETP8M1_13TeV-pythia8_v6-v1/*.root                                            > hdfs/ZZ.txt

#for MASS in 220 240 260 280 300 320 350 400; do
#    ls ${ALL}/AToZhToLLTauTau_M-${MASS}_13TeV_madgraph_4f_LO/*.root > hdfs/azh${MASS}.txt
#done

# Higgs samples
for MASS in 120 125 130; do
    ls ${ALL}/ZHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                       > hdfs/ZHTauTau${MASS}.txt
    #ls ${ALL}/ttHJetToTT_M${MASS}_13TeV_amcatnloFXFX_madspin_pythia8_v6-v1/*.root         > hdfs/ttHTauTau${MASS}.txt
    #ls ${ALL}/WminusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                  > hdfs/WMinusHTauTau${MASS}.txt
    #ls ${ALL}/WplusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                   > hdfs/WPlusHTauTau${MASS}.txt
    #ls ${ALL}/GluGluHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                  > hdfs/ggHtoTauTau${MASS}.txt
    #ls ${ALL}/VBFHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                     > hdfs/VBFHtoTauTau${MASS}.txt
done

# Higgs samples
for MASS in 125; do
    ls ${ALL}/WminusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                  > hdfs/WMinusHTauTau${MASS}.txt
    ls ${ALL}/WplusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                   > hdfs/WPlusHTauTau${MASS}.txt
done

