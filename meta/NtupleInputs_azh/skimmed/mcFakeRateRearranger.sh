

for CHANNEL in eeet eett eemt eeem; do
    cp DYJets_${CHANNEL}.txt dataEE-B_${CHANNEL}.txt
    cp DYJets1_${CHANNEL}.txt dataEE-C_${CHANNEL}.txt
    cp DYJets2_${CHANNEL}.txt dataEE-D_${CHANNEL}.txt
    cp DYJets3_${CHANNEL}.txt dataEE-E_${CHANNEL}.txt
    cp DYJets4_${CHANNEL}.txt dataEE-F_${CHANNEL}.txt
    cp WZ3l1nu_${CHANNEL}.txt dataEE-G_${CHANNEL}.txt
    cp TT_${CHANNEL}.txt dataEE-H_${CHANNEL}.txt



    #cat DYJets1_${CHANNEL}.txt >> dataEE-B_${CHANNEL}.txt
    #cat DYJets2_${CHANNEL}.txt >> dataEE-B_${CHANNEL}.txt
    #cat DYJets3_${CHANNEL}.txt >> dataEE-B_${CHANNEL}.txt
    #cat DYJets4_${CHANNEL}.txt >> dataEE-B_${CHANNEL}.txt
done

for CHANNEL in emmt mmtt mmmt emmm; do
    cp DYJets_${CHANNEL}.txt dataMM-B_${CHANNEL}.txt
    cp DYJets1_${CHANNEL}.txt dataMM-C_${CHANNEL}.txt
    cp DYJets2_${CHANNEL}.txt dataMM-D_${CHANNEL}.txt
    cp DYJets3_${CHANNEL}.txt dataMM-E_${CHANNEL}.txt
    cp DYJets4_${CHANNEL}.txt dataMM-F_${CHANNEL}.txt
    cp WZ3l1nu_${CHANNEL}.txt dataMM-G_${CHANNEL}.txt
    cp TT_${CHANNEL}.txt dataMM-H_${CHANNEL}.txt



    #cat DYJets1_${CHANNEL}.txt >> dataMM-B_${CHANNEL}.txt
    #cat DYJets2_${CHANNEL}.txt >> dataMM-B_${CHANNEL}.txt
    #cat DYJets3_${CHANNEL}.txt >> dataMM-B_${CHANNEL}.txt
    #cat DYJets4_${CHANNEL}.txt >> dataMM-B_${CHANNEL}.txt
done

