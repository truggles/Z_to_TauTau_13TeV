
FourE4MandDY4=/data/truggles/azhHalloweenSkim_svFitPrep_Merged
DATA=/data/truggles/zhSVFit_Nov05_newData_azh
ALL=/data/truggles/zhSVFit_Nov05_MC_azh

echo ""
echo "For svFit optimization ignore eeee and mmmm channels"
echo ""


# Preset samples
#for CHANNEL in eeet eett eemt eeem emmt mmtt mmmt emmm eeee mmmm; do
for CHANNEL in eeet eett eemt eeem emmt mmtt mmmt emmm; do
    for SAMPLE in ttZ ttZ2 DYJets DYJets1 DYJets2 DYJets3 DYJets4 ggZZ4m ggZZ2e2m ggZZ2e2tau ggZZ4e ggZZ2m2tau ggZZ4tau TT WWW WWZ WZ3l1nu WZZ WZ ZZ4l ZZZ; do
        ls ${ALL}/*${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done

    # SM Higgs
    for MASS in 110 120 125 130 140; do
        for SAMPLE in ZHTauTau WMinusHTauTau WPlusHTauTau ggHtoTauTau VBFHtoTauTau; do
            ls ${ALL}/*${SAMPLE}${MASS}_*_${CHANNEL}.root > skimmed/${SAMPLE}${MASS}_${CHANNEL}.txt
        done
    done
    for MASS in 125; do
        for SAMPLE in ZHWW HZZ; do
            ls ${ALL}/*${SAMPLE}${MASS}_*_${CHANNEL}.root > skimmed/${SAMPLE}${MASS}_${CHANNEL}.txt
        done
    done

    # AZH
    for MASS in 220 240 260 280 300 320 340 350 400; do
        ls ${ALL}/*azh${MASS}_*_${CHANNEL}.root > skimmed/azh${MASS}_${CHANNEL}.txt
    done
done

# for data
#for CHANNEL in eeet eett eemt eeem eeee; do
for CHANNEL in eeet eett eemt eeem; do
    for SAMPLE in dataEE-B dataEE-C dataEE-D dataEE-E dataEE-F dataEE-G dataEE-H; do
        ls ${DATA}/*${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done
    for SAMPLE in dataSingleE-B dataSingleE-C dataSingleE-D dataSingleE-E dataSingleE-F dataSingleE-G dataSingleE-H; do
        ls ${DATA}/*${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done
done
#for CHANNEL in emmt mmtt mmmt emmm mmmm; do
for CHANNEL in emmt mmtt mmmt emmm; do
    for SAMPLE in dataMM-B dataMM-C dataMM-D dataMM-E dataMM-F dataMM-G dataMM-H; do
        ls ${DATA}/*${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done
    for SAMPLE in dataSingleM-B dataSingleM-C dataSingleM-D dataSingleM-E dataSingleM-F dataSingleM-G dataSingleM-H; do
        ls ${DATA}/*${SAMPLE}_*_${CHANNEL}.root > skimmed/${SAMPLE}_${CHANNEL}.txt
    done
done



echo "Overwrite failed DYJets4 files from above for EETT and MMTT (no svFit)"
echo ""
ls ${FourE4MandDY4}/*DYJets4_*_eett.root > skimmed/DYJets4_eett.txt
ls ${FourE4MandDY4}/*DYJets4_*_mmtt.root > skimmed/DYJets4_mmtt.txt

