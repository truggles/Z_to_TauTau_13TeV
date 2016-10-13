
ALL=/data/truggles/azhOct12Merged

# Preset samples
for CHANNEL in eemm eeet eett eemt eeem emmt mmtt mmmt emmm eeee mmmm; do
    for SAMPLE in TT DYJets DYJets1 DYJets2 DYJets3 DYJets4 WZ3l1nu WWW ZZ4l ZZ4lAMCNLO ggZZ4m ggZZ2e2m ggZZ2e2tau ggZZ4e ggZZ2m2tau ggZZ4tau; do
        ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done

    # SM Higgs
    for MASS in 120 125 130; do
        for SAMPLE in ggHtoTauTau VBFHtoTauTau WMinusHTauTau WPlusHTauTau ZHTauTau ttHTauTau; do
            ls ${ALL}/${SAMPLE}${MASS}_*_${CHANNEL}.root > skimmed/${SAMPLE}${MASS}_${CHANNEL}.txt
        done
    done

    # AZH
    for MASS in 220 240 260 280 300 320 350 400; do
        ls ${ALL}/azh${MASS}_*_${CHANNEL}.root > skimmed/azh${MASS}_${CHANNEL}.txt
    done
done

# for data
for CHANNEL in eemm eeet eett eemt eeem eeee; do
    for SAMPLE in dataEE-B dataEE-C dataEE-D dataEE-E dataEE-F; do
        ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done
done
for CHANNEL in eemm emmt mmtt mmmt emmm mmmm; do
    for SAMPLE in dataMM-B dataMM-C dataMM-D dataMM-E dataMM-F; do
        ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done
done
