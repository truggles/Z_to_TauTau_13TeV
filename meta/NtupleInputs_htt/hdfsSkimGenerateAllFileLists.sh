
#ALL=/data/truggles/httSept04svFitted
#ALL=/data/truggles/httSept06postSVFit

#ALL=/data/truggles/svFitSept16withPFMet
ALL=/data/truggles/oct31_VVL_Study
CHANNEL=tt

for SAMPLE in dataTT-B dataTT-C dataTT-D dataTT-E dataTT-F DYJets DYJets1 DYJets2 DYJets3 DYJets4 EWKWPlus EWKWMinus EWKZ2l EWKZ2nu WWW WWZ WZZ ZZZ Tbar-tchan T-tchan TT Tbar-tW T-tW WJets WJets1 WJets2 WJets3 WJets4 WW1l1nu2q WZ1l1nu2q WZ1l3nu WZ2l2q ZZ2l2q VV WZ3l1nu ; do
#for SAMPLE in dataTT-B dataTT-C dataTT-D dataTT-E dataTT-F; do
    ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
done

for MASS in 120 125 130; do
    for SAMPLE in ggHtoTauTau VBFHtoTauTau WMinusHTauTau WPlusHTauTau ZHTauTau; do
        ls ${ALL}/${SAMPLE}${MASS}_*_${CHANNEL}.root > skimmed/${SAMPLE}${MASS}_${CHANNEL}.txt
    done
done
