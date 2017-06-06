
ALL=/data/truggles/azhMay31skimMerged
AZH=/data/truggles/azhJune06skimMerged

# Preset samples
for CHANNEL in eeet eett eemt eeem emmt mmtt mmmt emmm eeee mmmm; do
    #for SAMPLE in DYJets DYJets1 DYJets2 DYJets3 DYJets4 ggZZ4m ggZZ2e2m ggZZ2e2tau ggZZ4e ggZZ2m2tau ggZZ4tau TT WWW WWZ WZ3l1nu WZZ WZ ZZ4l ZZZ; do
    for SAMPLE in DYJets DYJets1 DYJets2 DYJets3 DYJets4 ggZZ2e2m ggZZ2e2tau ggZZ2m2tau ggZZ4tau TT WWW WWZ WZ3l1nu WZZ WZ ZZ4l ZZZ; do
        ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done

    # SM Higgs
    for MASS in 110 120 125 130 140; do
        for SAMPLE in ZHTauTau; do
            ls ${ALL}/${SAMPLE}${MASS}_*_${CHANNEL}.root > skimmed/${SAMPLE}${MASS}_${CHANNEL}.txt
        done
    done
    for MASS in 125; do
        for SAMPLE in WMinusHTauTau WPlusHTauTau ZHWW; do
            ls ${ALL}/${SAMPLE}${MASS}_*_${CHANNEL}.root > skimmed/${SAMPLE}${MASS}_${CHANNEL}.txt
        done
    done

    ls ${AZH}/ggZZ4e_*_${CHANNEL}.root > skimmed/ggZZ4e_${CHANNEL}.txt
    ls ${AZH}/ggZZ4m_*_${CHANNEL}.root > skimmed/ggZZ4m_${CHANNEL}.txt
    # AZH
    for MASS in 220 240 260 280 300 320 340 350 400; do
        ls ${AZH}/azh${MASS}_*_${CHANNEL}.root > skimmed/azh${MASS}_${CHANNEL}.txt
    done
done

# for data
for CHANNEL in eeet eett eemt eeem eeee; do
    for SAMPLE in dataEE-B dataEE-C dataEE-D dataEE-E dataEE-F dataEE-G dataEE-H; do
        ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done
done
for CHANNEL in emmt mmtt mmmt emmm mmmm; do
    for SAMPLE in dataMM-B dataMM-C dataMM-D dataMM-E dataMM-F dataMM-G dataMM-H; do
        ls ${ALL}/${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done
done



