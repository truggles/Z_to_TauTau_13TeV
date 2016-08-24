

# For l1 medium
folder=2June29a
rm plotsOut.txt
echo `date` >> plotsOut.txt
for sign in SS OS; do
    #for name in Medium_Loose VTight_Loose Tight_Medium VTight_Tight VTight_; do
    for name in VTight_Loose VTight_; do
        python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}ZTT --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1ml2_${name}ZTT --btag=False
        #python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}BTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}BTL --btag=True
        #python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}NoBTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}NoBTL --btag=False
    done
done

#XXX python analysis3Plots.py --folder=${folder}_OSl1ml2_VTight_LooseZTT --text=True --qcdMake=True --channels=tt --qcdMakeDM=OSl1m_VTight_LooseZTT --btag=False


