
folderTT=2Feb24c
folderEM=2Feb25a_em


rm dataCardsShapes/mssm/htt_tt.inputs-mssm-13TeV.root
rm dataCardsShapes/mssm/htt_tt.inputs-mssm-13TeV_svFit.root
rm dataCardsShapes/mssm/htt_em.inputs-mssm-13TeV.root
rm dataCardsShapes/mssm/htt_em.inputs-mssm-13TeV_svFit.root

python analysisShapesROOT.py --folder=${folderTT}_OSsig --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2loose --channels=tt --qcdSF=0.757525 --fitShape=m_vis
python analysisShapesROOT.py --folder=${folderTT}_OSsig --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2loose --channels=tt --qcdSF=0.757525 --fitShape=m_sv

python analysisShapesROOT.py --folder=${folderTT}_OSsigNoBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2looseNoBT --channels=tt --qcdSF=0.775067 --fitShape=m_vis --category=nobtag
python analysisShapesROOT.py --folder=${folderTT}_OSsigNoBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2looseNoBT --channels=tt --qcdSF=0.775067 --fitShape=m_sv --category=nobtag

python analysisShapesROOT.py --folder=${folderTT}_OSsigBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2looseBT --channels=tt --qcdSF=0.192879 --fitShape=m_vis --category=btag
python analysisShapesROOT.py --folder=${folderTT}_OSsigBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2looseBT --channels=tt --qcdSF=0.192879 --fitShape=m_sv --category=btag




python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCut --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCut --channels=em --fitShape=m_vis
python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCut --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCut --channels=em --fitShape=m_sv

python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCutNoBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCutNoBT --channels=em --fitShape=m_vis --category=nobtag
python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCutNoBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCutNoBT --channels=em --fitShape=m_sv --category=nobtag

python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCutBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCutBT --channels=em --fitShape=m_vis --category=btag
python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCutBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCutBT --channels=em --fitShape=m_sv --category=btag
