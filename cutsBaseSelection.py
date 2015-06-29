import ROOT
from collections import OrderedDict

def makeZCut( chain, l1, l2 ) :
	#print "l1 %s, l2 %s" % (l1, l2)
	outTree = chain.CopyTree( "abs( %s_%s_Mass - 90 ) < 30" % (l1, l2) )
	return outTree

def makeGenCut( inTree, cutString ) :
	#print "l1 %s, l2 %s" % (l1, l2)
	outTree = inTree.CopyTree( cutString )
	return outTree

def makeHisto( tree, sample, channel, cutName, var, varBins, varMin, varMax ) :
	hist = ROOT.TH1F( cutName, cutName, varBins, varMin, varMax )

	eventSet = set()
	for i in range( tree.GetEntries() ):
		tree.GetEntry( i )
		eventTup = ( tree.run, tree.lumi, tree.evt )
		if eventTup not in eventSet:
			num = getattr( tree, var )
			hist.Fill( num )
			eventSet.add( eventTup )
		#else: print "Found dup: %i, %i, %i" % eventTup
	return hist
			
# Provides a list of histos to create for both channels
def getGeneralHistoDict() :
	genVarMap = {
		'LT' : ('LT', 100, 0, 400),
		'Mt' : ('Mt', 100, 0, 400),
		'pfMetEt' : ('pfMetEt', 100, 0, 400),
		'bjetCISVVeto20Medium' : ('bjetCISVVeto20Medium', 60, 0, 5),
		'jetVeto30' : ('jetVeto30', 100, 0, 10),
	}
	return genVarMap
def getGeneralHistoDictPhys14() :
	genVarMap = {
		'LT' : ('LT', 100, 0, 400),
		'Mt' : ('Mt', 100, 0, 400),
		'pfMetEt' : ('pfMetEt', 100, 0, 400),
		'bjetCISVVeto20Medium' : ('bjetCISVVeto20', 60, 0, 5),
		'jetVeto30' : ('jetVeto30', 100, 0, 10),
	}
	return genVarMap
			
# Provides a list of histos to create for 'EM' channel
def getEMHistoDict() :
	chanVarMap = {
		'Z_Pt' : ('e_m_Pt', 100, 0, 400),
		'Z_Mass' : ('e_m_Mass', 100, 0, 400),
		'Z_SS' : ('e_m_SS', 20, -1, 1),
		'ePt' : ('ePt', 100, 0, 400),
		'eEta' : ('eEta', 100, -5, 5),
		'mPt' : ('mPt', 100, 0, 400),
		'mEta' : ('mEta', 100, -5, 5),
		'eRelPFIsoDB' : ('eRelPFIsoDB', 200, 0, 2),
		'ePVDZ' : ('ePVDZ', 100, -1, 1),
		'ePVDXY' : ('ePVDXY', 100, -.2, .2),
		'mRelPFIsoDBDefault' : ('mRelPFIsoDBDefault', 200, 0, 2),
		'mPVDZ' : ('mPVDZ', 100, -1, 1),
		'mPVDXY' : ('mPVDXY', 100, -.2, .2),
		'eMtToPFMET' : ('eMtToPFMET', 100, 0, 400),
		'mMtToPFMET' : ('mMtToPFMET', 100, 0, 400),
		'mNormTrkChi2' : ('mNormTrkChi2', 40, 0, 10),
	}
	return chanVarMap

# Provides a list of histos to create for 'TT' channel
def getTTHistoDict() :
	chanVarMap = {
		'Z_Pt' : ('t1_t2_Pt', 100, 0, 400),
		'Z_Mass' : ('t1_t2_Mass', 100, 0, 400),
		'Z_SS' : ('t1_t2_SS', 20, -1, 1),
		't1Pt' : ('t1Pt', 100, 0, 400),
		't1Eta' : ('t1Eta', 100, -5, 5),
#		't1AgainstElectronVLooseMVA5' : ('t1AgainstElectronVLooseMVA5', 11, -1, 1),
#		't1AgainstMuonLoose3' : ('t1AgainstMuonLoose3', 11, -1, 1),
		't1ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t1ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 10),
		't2Pt' : ('t2Pt', 100, 0, 400),
		't2Eta' : ('t2Eta', 100, -5, 5),
#		't2AgainstElectronVLooseMVA5' : ('t2AgainstElectronVLooseMVA5', 11, -1, 1),
#		't2AgainstMuonLoose3' : ('t2AgainstMuonLoose3', 11, -1, 1),
		't2ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t2ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 10),
		't1MtToPFMET' : ('t1MtToPFMET', 100, 0, 400),
		't2MtToPFMET' : ('t2MtToPFMET', 100, 0, 400),
	}
	return chanVarMap

# Apply cuts one at a time
def getCutMap( ch ) :
	cutMap = OrderedDict()
	if ch == 'em':
		cutMap['l1_l2_Pt_Eta'] = 'ePt > 13 && eAbsEta < 2.5 && mPt > 9 && mAbsEta < 2.4'
		cutMap['l1_l2_Iso'] = 'eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault < 0.15'
		cutMap['muonCuts'] = 'mIsGlobal == 1 && mNormTrkChi2 < 3.0'
		cutMap['l1_l2_dz_dxy'] = 'abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045'
	if ch == 'tt':
		cutMap['l1_l2_Pt_Eta'] = 't1Pt > 40 && t1AbsEta < 2.1 && t2Pt > 40 && t2AbsEta < 2.1'
		cutMap['l1_l2_Iso'] = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0'
		cutMap['TauAntiCuts'] = 't1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
	return cutMap

# A version which applies all cuts at once
def quickCutMap( ch ) :
	cutMap = OrderedDict()
	if ch == 'em':
		cutMap['BaseLine'] = 'ePt > 13 && eAbsEta < 2.5 && mPt > 9 && mAbsEta < 2.4 && eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault < 0.15 && mIsGlobal == 1 && mNormTrkChi2 < 3.0 && abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045'
	if ch == 'tt':
		cutMap['BaseLine'] = 't1Pt > 40 && t1AbsEta < 2.1 && t2Pt > 40 && t2AbsEta < 2.1 && t1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
	return cutMap
	

#channels = {'em' : ( ['e', 'm'],
#					 ['abs(e_m_Mass-90) < 30', 'e_m_SS == 0', 'ePt > 20', 'abs(eEta) < 2.3', 'mPt > 10', 'abs(mEta) < 2.1', 'ePVDZ < 0.2', 'ePVDXY < 0.045', 'mPVDZ < 0.2', 'mPVDXY < 0.045', 'eRelPFIsoDB < 0.15', 'mRelPFIsoDBDefault < 0.15', 'mIsGlobal == 1', 'mNormTrkChi2 < 3.0' ] ),
#		    'tt' : ( ['t1', 't2'],
#					 ['abs(t1_t2_Mass-90) < 30', 't1_t2_SS == 0', 't1Pt > 40', 'abs(t1Eta) < 2.1', 't2Pt > 40', 'abs(t2Eta) < 2.1', 't1AgainstElectronVLooseMVA5 > 0.5', 't1AgainstMuonLoose3 > 0.5', 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0', 't2AgainstElectronVLooseMVA5 > 0.5', 't2AgainstMuonLoose3 > 0.5', 't2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0' ] )
#}

