
ALL=/data/truggles/2016-ZTT-April11Merged
CHANNEL=tt

#for SAMPLE in dataTT-C dataTT-D DYJets DYJetsBig DYJetsLow DYJetsHigh DYJets1 DYJets2 DYJets3 DYJets4 Tbar-tchan T-tchan TT Tbar-tW T-tW WJets WJets1 WJets2 WJets3 WJets4 WW1l1nu2q WZJets WZ3l1nu WZ1l1nu2q WZ1l3nu WZ2l2q ZZ2l2q ZZ4l VV ggHtoTauTau120 ggHtoTauTau125 ggHtoTauTau130 VBFHtoTauTau120 VBFHtoTauTau125 VBFHtoTauTau130; do
for SAMPLE in DYJets DYJetsBig DYJetsLow DYJetsHigh DYJets1 DYJets2 DYJets3 DYJets4 Tbar-tchan T-tchan TT Tbar-tW T-tW WJets WJets1 WJets2 WJets3 WJets4 WW1l1nu2q WZJets WZ3l1nu WZ1l1nu2q WZ1l3nu WZ2l2q ZZ2l2q ZZ4l VV ggHtoTauTau120 ggHtoTauTau125 ggHtoTauTau130 VBFHtoTauTau120 VBFHtoTauTau125 VBFHtoTauTau130; do
    ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
done
