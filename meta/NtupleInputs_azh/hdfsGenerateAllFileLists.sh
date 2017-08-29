
DATA=/hdfs/store/user/truggles/ZH_data_aug26
MC=/hdfs/store/user/truggles/ZH_mc_aug26

ls ${DATA}/data_DoubleMuon_Run2016B*/*.root                                                > hdfs/dataMM-B.txt 
ls ${DATA}/data_DoubleMuon_Run2016C/*.root                                                 > hdfs/dataMM-C.txt 
ls ${DATA}/data_DoubleMuon_Run2016D/*.root                                                 > hdfs/dataMM-D.txt 
ls ${DATA}/data_DoubleMuon_Run2016E/*.root                                                 > hdfs/dataMM-E.txt 
ls ${DATA}/data_DoubleMuon_Run2016F/*.root                                                 > hdfs/dataMM-F.txt 
ls ${DATA}/data_DoubleMuon_Run2016G/*.root                                                 > hdfs/dataMM-G.txt 
ls ${DATA}/data_DoubleMuon_Run2016H*/*.root                                                > hdfs/dataMM-H.txt 

ls ${DATA}/data_DoubleEG_Run2016B*/*.root                                                   > hdfs/dataEE-B.txt 
ls ${DATA}/data_DoubleEG_Run2016C/*.root                                                    > hdfs/dataEE-C.txt 
ls ${DATA}/data_DoubleEG_Run2016D/*.root                                                    > hdfs/dataEE-D.txt 
ls ${DATA}/data_DoubleEG_Run2016E/*.root                                                    > hdfs/dataEE-E.txt 
ls ${DATA}/data_DoubleEG_Run2016F/*.root                                                    > hdfs/dataEE-F.txt 
ls ${DATA}/data_DoubleEG_Run2016G/*.root                                                    > hdfs/dataEE-G.txt 
ls ${DATA}/data_DoubleEG_Run2016H*/*.root                                                   > hdfs/dataEE-H.txt 


ls ${MC}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6*/*.root               > hdfs/DYJets.txt
ls ${MC}/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root            > hdfs/DYJets1.txt 
ls ${MC}/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root            > hdfs/DYJets2.txt 
ls ${MC}/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root            > hdfs/DYJets3.txt 
ls ${MC}/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root            > hdfs/DYJets4.txt 
ls ${MC}/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8_v6-v1/*.root                    > hdfs/ggZZ2e2m.txt
ls ${MC}/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8_v6-v1/*.root                   > hdfs/ggZZ2e2tau.txt
ls ${MC}/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8_v6-v1/*.root                  > hdfs/ggZZ2m2tau.txt
ls ${MC}/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8_v6-v1/*.root                       > hdfs/ggZZ4e.txt
ls ${MC}/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8_v6-v1/*.root                      > hdfs/ggZZ4m.txt
ls ${MC}/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8_v6-v1/*.root                     > hdfs/ggZZ4tau.txt
#ls ${MC}/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v6-v1/*.root               > hdfs/TTJ.txt
#ls ${MC}/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                           > hdfs/TTTT.txt
#ls ${MC}/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root               > hdfs/TTZ.txt
ls ${MC}/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_v6-v1/*.root                               > hdfs/TT.txt
ls ${MC}/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                         > hdfs/WWW.txt
ls ${MC}/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                            > hdfs/WWZ.txt
ls ${MC}/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8_v6-v1/*.root                       > hdfs/WZ3l1nu.txt
#ls ${MC}/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8_v6-v1/*.root                         > hdfs/WZ3l1nu.txt
ls ${MC}/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                            > hdfs/WZZ.txt
ls ${MC}/WZ_TuneCUETP8M1_13TeV-pythia8_v6*/*.root                                        > hdfs/WZ.txt
ls ${MC}/ZZTo4L_13TeV_powheg_pythia8_v6-v1/*.root                                        > hdfs/ZZ4l.txt
ls ${MC}/ZZTo4L_13TeV_powheg_pythia8_ext1_v6-v1/*.root                                   >> hdfs/ZZ4l.txt
#ls ${MC}/ZZTo4L_13TeV-amcatnloFXFX-pythia8_v6-v1/*.root                                  > hdfs/ZZ4lAMCNLO.txt
ls ${MC}/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v6-v1/*.root                            > hdfs/ZZZ.txt
ls ${MC}/ZZ_TuneCUETP8M1_13TeV-pythia8_v6*/*.root                                        > hdfs/ZZ.txt

for MASS in 220 240 260 280 300 320 340 350 400; do
    ls ${MC}/AToZhToLLTauTau_M-${MASS}_13TeV_madgraph_4f_LO*/*.root > hdfs/azh${MASS}.txt
done

# Higgs samples
for MASS in 110 120 125 130 140; do
    ls ${MC}/ZHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6*/*.root                       > hdfs/ZHTauTau${MASS}.txt
    #ls ${MC}/ttHJetToTT_M${MASS}_13TeV_amcatnloFXFX_madspin_pythia8_v6-v1/*.root         > hdfs/ttHTauTau${MASS}.txt
    ls ${MC}/WminusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6*/*.root                  > hdfs/WMinusHTauTau${MASS}.txt
    ls ${MC}/WplusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6*/*.root                   > hdfs/WPlusHTauTau${MASS}.txt
    ls ${MC}/GluGluHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6*/*.root                  > hdfs/ggHtoTauTau${MASS}.txt
    ls ${MC}/VBFHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6*/*.root                     > hdfs/VBFHtoTauTau${MASS}.txt
done

# Higgs samples
for MASS in 125; do
    #ls ${MC}/WminusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                  > hdfs/WMinusHTauTau${MASS}.txt
    #ls ${MC}/WplusHToTauTau_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                   > hdfs/WPlusHTauTau${MASS}.txt
    ls ${MC}/HZJ_HToWW_M${MASS}_13TeV_powheg_pythia8_v6-v1/*.root                       > hdfs/ZHWW${MASS}.txt
    ls ${MC}/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8_v6-v1/*.root               > hdfs/HZZ${MASS}.txt
done

