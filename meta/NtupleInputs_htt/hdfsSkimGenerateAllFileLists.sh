
ALL=/data/truggles/svFitApr01_SM-HTT_Merged
aHTT=/data/truggles/svFitAug21_aHTT_officialSigs_Merged
CHANNEL=tt


for SAMPLE in DYJets DYJets1 DYJets2 DYJets3 DYJets4 DYJetsLow DYJets1Low DYJets2Low EWKWMinus EWKWPlus EWKZ2l EWKZ2nu Tbar-tchan T-tchan TT Tbar-tW T-tW VV WJets WJets1 WJets2 WJets3 WJets4 WW1l1nu2q WWW WZ1l1nu2q WZ1l3nu WZ2l2q WZ3l1nu ZZ2l2q ZZ4l; do
    ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
done


#for SAMPLE in dataTT-B dataTT-C dataTT-D dataTT-E dataTT-F dataTT-G dataTT-H; do
#    ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
#done

for MASS in 110 120 125 130 140; do
    for SAMPLE in ggHtoTauTau VBFHtoTauTau WMinusHTauTau WPlusHTauTau ZHTauTau; do
        ls ${ALL}/${SAMPLE}${MASS}_*_${CHANNEL}.root > skimmed/${SAMPLE}${MASS}_${CHANNEL}.txt
    done
done

for MASS in 125; do
    for SAMPLE in HtoWW2l2nu VBFHtoWW2l2nu ttHTauTau; do
        ls ${ALL}/${SAMPLE}${MASS}_*_${CHANNEL}.root > skimmed/${SAMPLE}${MASS}_${CHANNEL}.txt
    done
done

for SAMPLE in VBF W Z; do
    for MODE in HtoTauTau0PHf05ph0125 HtoTauTau0L1f05ph0125 HtoTauTau0L1125 HtoTauTau0PM125 HtoTauTau0Mf05ph0125 HtoTauTau0PH125 HtoTauTau0M125; do
        ls ${aHTT}/${SAMPLE}${MODE}_*_${CHANNEL}.root > skimmed/${SAMPLE}${MODE}_${CHANNEL}.txt
    done
done

