#folder=25ns3oct14

pushd ${1}

for shape in DYJets TTJets Tbar-tW T-tW WJets WW WZJets ZZ data VBFHtoTauTau ggHtoTauTau
do
    for channel in em tt
    do
        hadd ${shape}_${channel}.root ${shape}_*_${channel}.root
    done
done

popd
