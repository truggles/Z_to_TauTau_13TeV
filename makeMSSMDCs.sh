
folderTT=2April12kLast
inclusive=0.163772972
nobtag=0.168389058
btag=0.105142826
#var=mt_sv_mssm
var=m_sv_mssm
#var=m_vis_mssm

#rm dataCardsShapes/mssm/htt_tt.inputs-mssm-13TeV_MtsvFit.root

python analysisShapesROOT.py --folder=${folderTT}_OSl1ml2_VTight_ZTT --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseZTT --qcdSF=${inclusive} --category=inclusive --mssm=True --fitShape=${var} --btag=False  --ES=True --tauPt=True

python analysisShapesROOT.py --folder=${folderTT}_OSl1ml2_VTight_NoBTL --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseNoBTL --qcdSF=${nobtag} --category=nobtag --mssm=True --fitShape=${var} --btag=False  --ES=True --tauPt=True

python analysisShapesROOT.py --folder=${folderTT}_OSl1ml2_VTight_BTL --channel=tt --useQCDMake=True --useQCDMakeName=OSl1m_VTight_LooseBTL --qcdSF=${btag} --category=btag --mssm=True --fitShape=${var} --btag=True  --ES=True --tauPt=True

#folderTT=2Feb24c
#folderEM=2Feb25a_em
#
#
#rm dataCardsShapes/mssm/htt_tt.inputs-mssm-13TeV.root
#rm dataCardsShapes/mssm/htt_tt.inputs-mssm-13TeV_svFit.root
#rm dataCardsShapes/mssm/htt_em.inputs-mssm-13TeV.root
#rm dataCardsShapes/mssm/htt_em.inputs-mssm-13TeV_svFit.root
#
#python analysisShapesROOT.py --folder=${folderTT}_OSsig --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2loose --channels=tt --qcdSF=0.757525 --fitShape=m_vis
#python analysisShapesROOT.py --folder=${folderTT}_OSsig --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2loose --channels=tt --qcdSF=0.757525 --fitShape=m_sv
#
#python analysisShapesROOT.py --folder=${folderTT}_OSsigNoBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2looseNoBT --channels=tt --qcdSF=0.775067 --fitShape=m_vis --category=nobtag
#python analysisShapesROOT.py --folder=${folderTT}_OSsigNoBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2looseNoBT --channels=tt --qcdSF=0.775067 --fitShape=m_sv --category=nobtag
#
#python analysisShapesROOT.py --folder=${folderTT}_OSsigBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2looseBT --channels=tt --qcdSF=0.192879 --fitShape=m_vis --category=btag
#python analysisShapesROOT.py --folder=${folderTT}_OSsigBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=OSl2looseBT --channels=tt --qcdSF=0.192879 --fitShape=m_sv --category=btag
#
#
#
#
#python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCut --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCut --channels=em --fitShape=m_vis
#python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCut --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCut --channels=em --fitShape=m_sv
#
#python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCutNoBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCutNoBT --channels=em --fitShape=m_vis --category=nobtag
#python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCutNoBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCutNoBT --channels=em --fitShape=m_sv --category=nobtag
#
#python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCutBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCutBT --channels=em --fitShape=m_vis --category=btag
#python analysisShapesROOT.py --folder=${folderEM}_OSpZetaCutBT --mssm=True --sync=True --useQCDMake=True --useQCDMakeName=SSpZetaCutBT --channels=em --fitShape=m_sv --category=btag
