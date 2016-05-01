
folder=2April25b
inclusive=0.163350808

rm dataCardsShapes/htt/htt_tt.inputs-sm-13TeV.root
rm dataCardsShapes/htt/htt_tt.inputs-sm-13TeV_svFit.root

python analysisShapesROOT.py --folder=${folder}_OSl1ml2_VTight_ZTT --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseZTT --qcdSF=${inclusive} --category=inclusive --fitShape=m_sv  --ES=True
python analysisShapesROOT.py --folder=${folder}_OSl1ml2_VTight_ZTT --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseZTT --qcdSF=${inclusive} --category=inclusive --fitShape=m_vis  --ES=True
