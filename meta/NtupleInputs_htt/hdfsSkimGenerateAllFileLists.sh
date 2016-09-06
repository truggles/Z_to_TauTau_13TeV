
ALL=/data/truggles/httSept04svFitted
CHANNEL=tt

for SAMPLE in dataTT-B dataTT-C dataTT-D dataTT-E dataTT-F DYJetsAMCNLO DYJets DYJets1 DYJets2 DYJets3 DYJets4 Tbar-tchan T-tchan TT Tbar-tW T-tW WJets WJets1 WJets2 WJets3 WJets4 WW1l1nu2q WZ1l1nu2q WZ1l3nu WZ2l2q ZZ2l2q VV ggHtoTauTau120 ggHtoTauTau125 ggHtoTauTau130 VBFHtoTauTau120 VBFHtoTauTau125 VBFHtoTauTau130; do
    ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
done
