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

# Make a histo, but fill it later so we can keep track of events for ALL histos at once
def makeHisto( cutName, varBins, varMin, varMax ) :
	hist = ROOT.TH1F( cutName, cutName, varBins, varMin, varMax )
	return hist
			
# Provides a list of histos to create for both channels
def getGeneralHistoDict() :
	genVarMap = {
		'LT' : ('LT', 100, 0, 400),
		'Mt' : ('Mt', 100, 0, 400),
		'pfMetEt' : ('pfMetEt', 100, 0, 400),
		'bjetCISVVeto20Medium' : ('bjetCISVVeto20Medium', 60, 0, 5),
		'jetVeto30' : ('jetVeto30', 100, 0, 10),
        'eVetoZTT10' : ('eVetoZTT10', 20, 0, 2),
        'mVetoZTT10' : ('eVetoZTT10', 20, 0, 2),
		'jet1Pt' : ('jet1Pt', 100, 0, 400),
		'jet1Eta' : ('jet1Eta', 100, -5, 5),
		'jet2Pt' : ('jet2Pt', 100, 0, 400),
		'jet2Eta' : ('jet2Eta', 100, -5, 5),
        'GenWeight' : ('GenWeight', 1000, -300000, 300000),
        'nvtx' : ('nvtx', 50, 0, 50),
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
		'Z_SS' : ('e_m_SS', 20, 0, 2),
		'ePt' : ('ePt', 100, 0, 400),
		'eEta' : ('eEta', 100, -5, 5),
		'eJetPt' : ('eJetPt', 100, 0, 400),
		'mPt' : ('mPt', 100, 0, 400),
		'mEta' : ('mEta', 100, -5, 5),
		'mJetPt' : ('mJetPt', 100, 0, 400),
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
		'Z_SS' : ('t1_t2_SS', 20, 0, 2),
		't1Pt' : ('t1Pt', 100, 0, 400),
		't1Eta' : ('t1Eta', 100, -5, 5),
		't1ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t1ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 10),
		't1MtToPFMET' : ('t1MtToPFMET', 100, 0, 400),
		't1DecayMode' : ('t1DecayMode', 15, 0, 15),
		't1JetPt' : ('t1JetPt', 100, 0, 400),
        't1Mass' : ('t1Mass', 400, 0, 4),
		't2Pt' : ('t2Pt', 100, 0, 400),
		't2Eta' : ('t2Eta', 100, -5, 5),
		't2ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t2ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 10),
		't2MtToPFMET' : ('t2MtToPFMET', 100, 0, 400),
		't2DecayMode' : ('t2DecayMode', 15, 0, 15),
		't2JetPt' : ('t2JetPt', 100, 0, 400),
        't2Mass' : ('t2Mass', 400, 0, 4),
	}
	return chanVarMap

# Apply RunII cuts one at a time
def getCutMap( ch ) :
	cutMap = OrderedDict()
	if ch == 'em':
		cutMap['l1_l2_Pt_Eta'] = 'ePt > 13 && eAbsEta < 2.5 && mPt > 9 && mAbsEta < 2.4'
		cutMap['l1_l2_Iso'] = 'eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault < 0.15'
		cutMap['MuElecCuts'] = 'mPFIDMedium == 1 && eCBIDMedium == 1 && mNormTrkChi2 < 3'
		cutMap['l1_l2_dz_dxy'] = 'abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045'
		cutMap['lepton_veto'] = 'eVetoZTT10 == 0 && muVetoZTT10 == 0'
	if ch == 'tt':
		cutMap['l1_l2_Pt_Eta'] = 't1Pt > 40 && t1AbsEta < 2.1 && t2Pt > 40 && t2AbsEta < 2.1'
		cutMap['l1_l2_Iso'] = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0'
		cutMap['TauVertex'] = 'abs(t1VZ - pvZ) < 0.2 && abs(t2VZ - pvZ) < 0.2'
		cutMap['TauAntiCuts'] = 't1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
		cutMap['lepton_veto'] = 'eVetoZTT10 == 0 && muVetoZTT10 == 0'
	return cutMap

# Apply Phys14 cuts one at a time
def getCutMapPhys14( ch ) :
	cutMap = OrderedDict()
	if ch == 'em':
		cutMap['l1_l2_Pt_Eta'] = 'ePt > 13 && eAbsEta < 2.5 && mPt > 9 && mAbsEta < 2.4'
		cutMap['l1_l2_Iso'] = 'eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault < 0.15'
		cutMap['MuElecCuts'] = 'mPFIDLoose == 1 && eCBIDMedium == 1 && mNormTrkChi2 < 3'
		cutMap['l1_l2_dz_dxy'] = 'abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045'
	if ch == 'tt':
		cutMap['l1_l2_Pt_Eta'] = 't1Pt > 40 && t1AbsEta < 2.1 && t2Pt > 40 && t2AbsEta < 2.1'
		cutMap['l1_l2_Iso'] = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0'
		cutMap['TauVertex'] = 'abs(t1VZ - pvZ) < 0.2 && abs(t2VZ - pvZ) < 0.2'
		cutMap['TauAntiCuts'] = 't1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
	return cutMap

# Apply QCD estimation cuts one at a time
def getCutMapQuickQCD( ch ) :
	cutMap = OrderedDict()
	if ch == 'em':
		cutMap['qcd_pre'] = 'e_m_SS == 0 && ePt > 13 && eAbsEta < 2.5 && mPt > 10 && mAbsEta < 2.4 && mPFIDLoose == 1 && mNormTrkChi2 < 3 && abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045 && eVetoZTT10 == 0 && muVetoZTT10 == 0 && eRelPFIsoDB < 0.2 && mRelPFIsoDBDefault < 1.0'
		cutMap['qcd_post'] = 'eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault < 0.15 && eCBIDMedium == 1 && mPFIDMedium == 1'
	if ch == 'tt':
		cutMap['qcd_pre'] = 't1_t2_SS == 0 && t1Pt > 45 && t1AbsEta < 2.1 && t2Pt > 45 && t2AbsEta < 2.1 && t1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 10.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 10.0 && t1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5 && abs(t1VZ - pvZ) < 0.2 && abs(t2VZ - pvZ) < 0.2 && eVetoZTT10 == 0 && muVetoZTT10 == 0 && t1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0'
		cutMap['qcd_post'] = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0'
	return cutMap

# A version which applies all cuts at once RunII
def quickCutMap( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['BaseLine'] = 'ePt > 13 && eAbsEta < 2.5 && mPt > 10 && mAbsEta < 2.4 && e_m_DR > 0.3 && ePassesConversionVeto == 1 && eMissingHits <= 1 && mPFIDMedium == 1 && abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045 && ( (singleESingleMuPass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1 && ePt > 24) || (singleMuSingleEPass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1 && mPt > 24) ) && eMVANonTrigWP80 == 1'
        cutMap['PostSync'] = 'e_m_SS == 0 && eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault < 0.15 && eVetoZTT10 == 0 && muVetoZTT10 == 0'
    if ch == 'tt':
        cutMap['BaseLine'] = 't1Pt > 45 && t1AbsEta < 2.1 && t2Pt > 45 && t2AbsEta < 2.1 && t1_t2_DR > 0.5 && abs(t1VZ - pvZ) < 0.2 && abs(t2VZ - pvZ) < 0.2 && eVetoZTT10 == 0 && muVetoZTT10 == 0 && abs( t1Charge ) == 1 && abs( t2Charge ) == 1 && doubleTauPass == 1 && t1MatchesDoubleTau40Path == 1 && t2MatchesDoubleTau40Path == 1'
        cutMap['PostSync'] = 't1_t2_SS == 0 && t1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
    return cutMap
	
# QCD DATA DRIVEN MODELING RunII - JULY 28 2015
def quickCutMapDataSS( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['BaseLine'] = 'ePt > 13 && eAbsEta < 2.5 && mPt > 10 && mAbsEta < 2.4 && e_m_DR > 0.3 && ePassesConversionVeto == 1 && eMissingHits <= 1 && mPFIDMedium == 1 && abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045 && ( (singleESingleMuPass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1 && ePt > 24) || (singleMuSingleEPass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1 && mPt >24) ) && eMVANonTrigWP80 == 1'
        cutMap['SS_DATA'] = 'e_m_SS == 1 && eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault < 0.15 && eVetoZTT10 == 0 && muVetoZTT10 == 0'
    if ch == 'tt':
        cutMap['BaseLine'] = 't1Pt > 45 && t1AbsEta < 2.1 && t2Pt > 45 && t2AbsEta < 2.1 && t1_t2_DR > 0.5 && abs(t1VZ - pvZ) < 0.2 && abs(t2VZ - pvZ) < 0.2 && eVetoZTT10 == 0 && muVetoZTT10 == 0 && abs( t1Charge ) == 1 && abs( t2Charge ) == 1 && doubleTauPass == 1 && t1MatchesDoubleTau40Path == 1 && t2MatchesDoubleTau40Path == 1'
        cutMap['SS_DATA'] = 't1_t2_SS == 1 && t1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
    return cutMap
	
# QCD DATA DRIVEN MODELING RunII - JULY 30 2015
def quickCutMapDataInversion( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['BaseLine'] = 'ePt > 13 && eAbsEta < 2.5 && mPt > 10 && mAbsEta < 2.4 && e_m_DR > 0.3 && ePassesConversionVeto == 1 && eMissingHits <= 1 && mPFIDMedium == 1 && abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045 && ( (singleESingleMuPass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1 && ePt > 24) || (singleMuSingleEPass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1 && mPt > 24) ) && eMVANonTrigWP80 == 1'
        #cutMap['Invert_DATA'] = 'e_m_SS == 0 && eRelPFIsoDB > 0.15 && mRelPFIsoDBDefault > 0.15 && eVetoZTT10 == 0 && muVetoZTT10 == 0'
        cutMap['Invert_DATA'] = 'eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault > 0.15 && eVetoZTT10 == 0 && muVetoZTT10 == 0'
    if ch == 'tt':
        cutMap['BaseLine'] = 't1Pt > 45 && t1AbsEta < 2.1 && t2Pt > 45 && t2AbsEta < 2.1 && t1_t2_DR > 0.5 && abs(t1VZ - pvZ) < 0.2 && abs(t2VZ - pvZ) < 0.2 && eVetoZTT10 == 0 && muVetoZTT10 == 0 && abs( t1Charge ) == 1 && abs( t2Charge ) == 1 && doubleTauPass == 1 && t1MatchesDoubleTau40Path == 1 && t2MatchesDoubleTau40Path == 1'
        #cutMap['Invert_DATA'] = 't1_t2_SS == 0 && t1ByCombinedIsolationDeltaBetaCorrRaw3Hits > 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits > 1.0 && t1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
        cutMap['Invert_DATA'] = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits > 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits > 1.0 && t1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
    return cutMap
# A version which applies all cuts at once Phys14
def quickCutMapPhys14( ch ) :
	cutMap = OrderedDict()
	if ch == 'em':
		cutMap['BaseLine'] = 'ePt > 13 && eAbsEta < 2.5 && mPt > 9 && mAbsEta < 2.4 && eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault < 0.15 && mPFIDLoose == 1 && mNormTrkChi2 < 3 && eCBIDMedium == 1 && abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045'
	if ch == 'tt':
		cutMap['BaseLine'] = 't1Pt > 40 && t1AbsEta < 2.1 && t2Pt > 40 && t2AbsEta < 2.1 && t1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5 && abs(t1VZ - pvZ) < 0.2 && abs(t2VZ - pvZ) < 0.2'
	return cutMap

#channels = {'em' : ( ['e', 'm'],
#					 ['abs(e_m_Mass-90) < 30', 'e_m_SS == 0', 'ePt > 20', 'abs(eEta) < 2.3', 'mPt > 10', 'abs(mEta) < 2.1', 'ePVDZ < 0.2', 'ePVDXY < 0.045', 'mPVDZ < 0.2', 'mPVDXY < 0.045', 'eRelPFIsoDB < 0.15', 'mRelPFIsoDBDefault < 0.15', 'mIsGlobal == 1', 'mNormTrkChi2 < 3.0' ] ),
#		    'tt' : ( ['t1', 't2'],
#					 ['abs(t1_t2_Mass-90) < 30', 't1_t2_SS == 0', 't1Pt > 40', 'abs(t1Eta) < 2.1', 't2Pt > 40', 'abs(t2Eta) < 2.1', 't1AgainstElectronVLooseMVA5 > 0.5', 't1AgainstMuonLoose3 > 0.5', 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0', 't2AgainstElectronVLooseMVA5 > 0.5', 't2AgainstMuonLoose3 > 0.5', 't2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0' ] )
#}

