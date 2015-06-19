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
	name = "%s%s%s" % ( sample, channel, cutName )
	hist = ROOT.TH1F( var, var, varBins, varMin, varMax )

	for i in range( tree.GetEntries() ):
		tree.GetEntry( i )
		num = getattr( tree, var )
		hist.Fill( num )
	return hist
			
# Provides a list of histos to create for both channels
def getGeneralHistoDict() :
	genVarMap = {
		'LT' : ('LT', 500, 0, 500),
		'Mt' : ('Mt', 500, 0, 500),
		'pfMetEt' : ('pfMetEt', 500, 0, 500),
		'bjetCISVVeto20' : ('bjetCISVVeto20', 60, 0, 5),
		'jetVeto30' : ('jetVeto30', 100, 0, 10),
	}
	return genVarMap
			
# Provides a list of histos to create for 'EM' channel
def getEMHistoDict() :
	chanVarMap = {
		'Z_Pt' : ('e_m_Pt', 500, 0, 500),
		'Z_Mass' : ('e_m_Mass', 80, 50, 130),
		'Z_SS' : ('e_m_SS', 21, -1, 1),
		'ePt' : ('ePt', 500, 0, 500),
		'eEta' : ('eEta', 101, -5, 5),
		'mPt' : ('mPt', 500, 0, 500),
		'mEta' : ('mEta', 101, -5, 5),
		'eRelPFIsoDB' : ('eRelPFIsoDB', 100, 0, 10),
		'ePVDZ' : ('ePVDZ', 21, -1, 1),
		'ePVDXY' : ('ePVDXY', 21, -1, 1),
		'mRelPFIsoDBDefault' : ('mRelPFIsoDBDefault', 100, 0, 10),
		'mPVDZ' : ('mPVDZ', 21, -1, 1),
		'mPVDXY' : ('mPVDXY', 21, -1, 1),
		'mIsGlobal' : ('mPVDXY', 10, -1, 1),
		'mNormTrkChi2' : ('mNormTrkChi2', 100, 0, 10),
	}
	return chanVarMap

# Provides a list of histos to create for 'TT' channel
def getTTHistoDict() :
	chanVarMap = {
		'Z_Pt' : ('t1_t2_Pt', 500, 0, 500),
		'Z_Mass' : ('t1_t2_Mass', 80, 50, 130),
		'Z_SS' : ('t1_t2_SS', 21, -1, 1),
		't1Pt' : ('t1Pt', 500, 0, 500),
		't1Eta' : ('t1Eta', 101, -5, 5),
#		't1AgainstElectronVLooseMVA5' : ('t1AgainstElectronVLooseMVA5', 11, -1, 1),
#		't1AgainstMuonLoose3' : ('t1AgainstMuonLoose3', 11, -1, 1),
		't1ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t1ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 10),
		't2Pt' : ('t2Pt', 500, 0, 500),
		't2Eta' : ('t2Eta', 101, -5, 5),
#		't2AgainstElectronVLooseMVA5' : ('t2AgainstElectronVLooseMVA5', 11, -1, 1),
#		't2AgainstMuonLoose3' : ('t2AgainstMuonLoose3', 11, -1, 1),
		't2ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t2ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 10),
	}
	return chanVarMap

def getCutMap( ch, l1, l2 ) :
	cutMap = OrderedDict()
	cutMap['ZMass'] = 'abs( %s_%s_Mass - 90 ) < 30' % (l1, l2)
	if ch == 'em': cutMap['l1Pt'] = 'ePt > 50'
	if ch == 'tt': cutMap['l1Pt'] = 't1Pt > 75'
	return cutMap

#channels = {'em' : ( ['e', 'm'],
#					 ['abs(e_m_Mass-90) < 30', 'e_m_SS == 0', 'ePt > 20', 'abs(eEta) < 2.3', 'mPt > 10', 'abs(mEta) < 2.1', 'ePVDZ < 0.2', 'ePVDXY < 0.045', 'mPVDZ < 0.2', 'mPVDXY < 0.045', 'eRelPFIsoDB < 0.15', 'mRelPFIsoDBDefault < 0.15', 'mIsGlobal == 1', 'mNormTrkChi2 < 3.0' ] ),
#		    'tt' : ( ['t1', 't2'],
#					 ['abs(t1_t2_Mass-90) < 30', 't1_t2_SS == 0', 't1Pt > 40', 'abs(t1Eta) < 2.1', 't2Pt > 40', 'abs(t2Eta) < 2.1', 't1AgainstElectronVLooseMVA5 > 0.5', 't1AgainstMuonLoose3 > 0.5', 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0', 't2AgainstElectronVLooseMVA5 > 0.5', 't2AgainstMuonLoose3 > 0.5', 't2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0' ] )
#}

