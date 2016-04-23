
folder=2April12kLast
inclusive=0.163772972

python analysisShapesROOT.py --folder=${folder}_OSl1ml2_VTight_ZTT --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseZTT --qcdSF=${inclusive} --category=inclusive --fitShape=m_sv  --ES=True
python analysisShapesROOT.py --folder=${folder}_OSl1ml2_VTight_ZTT --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseZTT --qcdSF=${inclusive} --category=inclusive --fitShape=m_vis  --ES=True
