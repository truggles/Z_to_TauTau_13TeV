
pushd /data/$USER/${1}

hadd -f dataRedBkg_${2}.root data*-?_*_${2}.root

for SAMPLE in TT WZ3l1nu ZZ4l ggZZ ttZ; do
    hadd -f mc_${SAMPLE}_${2}.root ${SAMPLE}*_${2}.root
done

hadd -f mc_DYJets_${2}.root DYJets[^4]*_${2}.root
hadd -f mc_DYJets4_${2}.root DYJets4*_${2}.root

#hadd -f mc_Reducible_${2}.root mc_DYJets_${2}.root mc_DYJets4_${2}.root mc_TT_${2}.root mc_WZ3l1nu_${2}.root
#hadd -f mc_Irreducible_${2}.root mc_ZZ4l_${2}.root mc_ggZZ_${2}.root mc_ttZ_${2}.root

popd
