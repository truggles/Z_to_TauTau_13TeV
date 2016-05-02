
# For normal single lepton loose cuts
#for sign in SS OS; do
#    for name in Medium_Loose Tight_Loose VTight_Loose Tight_Medium VTight_Medium VTight_Tight; do
#    #for name in Medium_Loose Tight_Medium VTight_Tight; do
#        python analysis3Plots.py --folder=${folder}_${sign}l2_${name}BT --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}_${name}BT
#        python analysis3Plots.py --folder=${folder}_${sign}l2_${name} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}_${name}
#    done
#    python analysis3Plots.py --folder=${folder}_${sign}l2_VTight_ --qcdMake=True --text=True --channels=tt --qcdMakeDM=${sign}__VTight
#    python analysis3Plots.py --folder=${folder}_${sign}l2_VTight_BT --qcdMake=True --text=True --channels=tt --qcdMakeDM=${sign}__VTightBT
#done

# For l1 tight
#for sign in SS OS; do
#    for name in Medium_Loose Tight_Loose VTight_Loose Tight_Medium VTight_Medium VTight_Tight; do
#    #for name in Medium_Loose Tight_Medium VTight_Tight; do
#        python analysis3Plots.py --folder=${folder}_${sign}l1tl2_${name}BT --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1t_${name}BT
#        python analysis3Plots.py --folder=${folder}_${sign}l1tl2_${name} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1t_${name}
#    done
#done




# For l1 medium
#folder=2April12kLast
folder=2April25b
folder=2May01
rm plotsOut.txt
echo `date` >> plotsOut.txt
for sign in SS OS; do
    #for name in Medium_Loose VTight_Loose Tight_Medium VTight_Tight VTight_; do
    for name in VTight_Loose VTight_; do
        python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}ZTT --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}ZTT --btag=False
        python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}BTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}BTL --btag=True
        python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}NoBTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}NoBTL --btag=False
    done
done

#XXX python analysis3Plots.py --folder=${folder}_OSl1ml2_VTight_LooseZTT --text=True --qcdMake=True --channels=tt --qcdMakeDM=OSl1m_VTight_LooseZTT --btag=False


## For l1 medium
#folder=2Mar29a
#for sign in SS OS; do
#    #for name in Medium_Loose VTight_Loose Tight_Medium VTight_Tight VTight_; do
#    for name in VTight_Loose VTight_; do
#        #XXX python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}BTM --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}BTM --btag=True
#        #XXX python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}BTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}BTL --btag=True
#        #XXX python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}NoBTM --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}NoBTM --btag=False
#        #XXX python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}NoBTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}NoBTL --btag=False
#        python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}BTMallJ --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}BTMallJ --btag=True
#        python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}BTLallJ --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}BTLallJ --btag=True
#        python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}BTMjl1 --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}BTMjl1 --btag=True
#        python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name}BTLjl1 --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}BTLjl1 --btag=True
#        #python analysis3Plots.py --folder=${folder}_${sign}l1ml2_${name} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1m_${name}
#    done
##    for name in Medium_Loose VTight_Loose Tight_Medium VTight_Tight VTight_; do
##        python analysis3Plots.py --folder=${folder}_${sign}l1vtl2_${name}BTM --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1vt_${name}BTM
##        python analysis3Plots.py --folder=${folder}_${sign}l1vtl2_${name}BTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1vt_${name}BTL
##        python analysis3Plots.py --folder=${folder}_${sign}l1vtl2_${name}NoBTM --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1vt_${name}NoBTM
##        python analysis3Plots.py --folder=${folder}_${sign}l1vtl2_${name}NoBTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1vt_${name}NoBTL
##    done
##    for name in Medium_Loose VTight_Loose Tight_Medium VTight_Tight VTight_; do
##        python analysis3Plots.py --folder=${folder}_${sign}l1ll2_${name}BTM --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1l_${name}BTM
##        python analysis3Plots.py --folder=${folder}_${sign}l1ll2_${name}BTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1l_${name}BTL
##        python analysis3Plots.py --folder=${folder}_${sign}l1ll2_${name}NoBTM --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1l_${name}NoBTM
##        python analysis3Plots.py --folder=${folder}_${sign}l1ll2_${name}NoBTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1l_${name}NoBTL
##    done
##    for name in Medium_Loose VTight_Loose Tight_Medium VTight_Tight VTight_; do
##        python analysis3Plots.py --folder=${folder}_${sign}l1tl2_${name}BTM --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1t_${name}BTM
##        python analysis3Plots.py --folder=${folder}_${sign}l1tl2_${name}BTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1t_${name}BTL
##        python analysis3Plots.py --folder=${folder}_${sign}l1tl2_${name}NoBTM --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1t_${name}NoBTM
##        python analysis3Plots.py --folder=${folder}_${sign}l1tl2_${name}NoBTL --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}l1t_${name}NoBTL
##    done
#done
#
#
### For l1 tight
##for sign in SS OS; do
##    for name in Medium_Loose VTight_Loose Tight_Medium VTight_Tight; do
##        python analysis3Plots.py --folder=${folder}_${sign}Pt1Gtrl1tl2_${name} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}Pt1Gtrl1t_${name}
##        python analysis3Plots.py --folder=${folder}_${sign}Pt1Gtrl1ml2_${name} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}Pt1Gtrl1m_${name}
##        python analysis3Plots.py --folder=${folder}_${sign}Pt2Gtrl1tl2_${name} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}Pt2Gtrl1t_${name}
##        python analysis3Plots.py --folder=${folder}_${sign}Pt2Gtrl1ml2_${name} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${sign}Pt2Gtrl1m_${name}
##    done
##done
#
#
##for sign in SS OS; do
##    #for name in Medium_Loose VTight_Loose Tight_Medium VTight_Tight; do
##    for btag in L M; do
##        for l2 in Sig t1lt2l; do
##            python analysis3Plots.py --folder=${btag}BTag${sign}${l2} --text=True --qcdMake=True --channels=tt --qcdMakeDM=${btag}BTag${sign}${l2}
##        done
##    done
##done
