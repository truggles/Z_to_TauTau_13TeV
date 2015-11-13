#folder=25ns3oct14

for run in 254790 254833 258425 259721
do
    hadd -f ${run}/${run}.root ${run}/${run}_*.root
done
