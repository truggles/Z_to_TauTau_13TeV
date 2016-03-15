

## For normal single lepton loose cuts
#for sign in SS OS; do
#    for name in Medium_Loose Tight_Loose VTight_Loose Tight_Medium VTight_Medium VTight_Tight; do
#        python analysis3Plots.py --folder=2Feb24c_${sign}l2_${name}BT --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}_${name}BT
#    done
#    python analysis3Plots.py --folder=2Feb24c_${sign}IsoCutBT --qcdMake=True --text=True --channels=tt --qcdMakeDM=${sign}IsoCutBT
#done

# For l1 tight
for sign in SS OS; do
    for name in Medium_Loose Tight_Loose VTight_Loose Tight_Medium VTight_Medium VTight_Tight; do
        python analysis3Plots.py --folder=2Feb24c_${sign}l1tl2_${name}BT --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1t_${name}BT
        python analysis3Plots.py --folder=2Feb24c_${sign}l1tl2_${name} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1t_${name}
    done
done

# For l1 medium
for sign in SS OS; do
    for name in Medium_Loose Tight_Loose VTight_Loose Tight_Medium VTight_Medium VTight_Tight; do
        python analysis3Plots.py --folder=2Feb24c_${sign}l1ml2_${name}BT --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}BT
        python analysis3Plots.py --folder=2Feb24c_${sign}l1ml2_${name} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}
    done
done
