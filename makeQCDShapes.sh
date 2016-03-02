


for sign in OS SS; do
    for name in Medium_Loose Tight_Loose VTight_Loose Tight_Medium VTight_Medium VTight_Tight; do
        python analysis3Plots.py --folder=2Feb24c_${sign}l2_${name} --qcdMake=True --channels=tt --qcdMakeDM=${sign}_${name}
    done
    python analysis3Plots.py --folder=2Feb24c_${sign}IsoCut --qcdMake=True --channels=tt --qcdMakeDM=${sign}IsoCut
done


