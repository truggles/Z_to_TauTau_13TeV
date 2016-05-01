
folderTT=2April25b
inclusive=0.163350808
nobtag=0.168036706
btag=0.104697487
#var=mt_sv_mssm
#var=m_sv_mssm
#var=m_vis_mssm

rm dataCardsShapes/mssm/htt_tt.inputs-mssm-13TeV_MtsvFit.root
rm dataCardsShapes/mssm/htt_tt.inputs-mssm-13TeV_svFit.root

for var in mt_sv_mssm m_sv_mssm; do
    python analysisShapesROOT.py --folder=${folderTT}_OSl1ml2_VTight_ZTT --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseZTT --qcdSF=${inclusive} --category=inclusive --mssm=True --fitShape=${var} --btag=False  --ES=True --tauPt=True
    
    python analysisShapesROOT.py --folder=${folderTT}_OSl1ml2_VTight_NoBTL --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseNoBTL --qcdSF=${nobtag} --category=nobtag --mssm=True --fitShape=${var} --btag=False  --ES=True --tauPt=True
    
    python analysisShapesROOT.py --folder=${folderTT}_OSl1ml2_VTight_BTL --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseBTL --qcdSF=${btag} --category=btag --mssm=True --fitShape=${var} --btag=True  --ES=True --tauPt=True
done



