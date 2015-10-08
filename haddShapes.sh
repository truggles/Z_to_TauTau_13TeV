folder=25ns3oct08QCD

pushd ${folder}

for shape in DYJets TT Tbar_tW T_tW WJets WW WZJets ZZ data
do
    for channel in em tt
    do
        hadd ${shape}_${channel}.root ${shape}_*_${channel}.root
    done
done

popd
