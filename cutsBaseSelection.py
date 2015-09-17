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
		'LT' : ('LT', 600, 0, 600),
		'Mt' : ('Mt', 600, 0, 600),
		'pfMetEt' : ('pfMetEt', 100, 0, 400),
		'pfMetPhi' : ('pfMetPhi', 100, -5, 5),
		'mvaMetEt' : ('mvaMetEt', 100, 0, 400),
		'mvaMetPhi' : ('mvaMetPhi', 100, -5, 5),
		'bjetCISVVeto20Medium' : ('bjetCISVVeto20Medium', 60, 0, 5),
		'njetspt20' : ('jetVeto20ZTT', 100, 0, 10),
		'nbtag' : ('bjetCISVVeto20MediumZTT', 100, 0, 10),
        'eVetoZTT10' : ('eVetoZTT10new2', 20, 0, 2),
        'mVetoZTT10' : ('eVetoZTT10new2', 20, 0, 2),
		'jet1Pt' : ('jet1Pt', 100, 0, 400),
		'jet1Eta' : ('jet1Eta', 100, -5, 5),
		'jet2Pt' : ('jet2Pt', 100, 0, 400),
		'jet2Eta' : ('jet2Eta', 100, -5, 5),
        'GenWeight' : ('GenWeight', 1000, -300000, 300000),
        'nvtx' : ('nvtx', 50, 0, 50),
	}
	return genVarMap
			
# Provides a list of histos to create for 'EM' channel
def getEMHistoDict() :
	chanVarMap = {
		'Z_Pt' : ('e_m_Pt', 100, 0, 400),
		'Z_Mass' : ('e_m_Mass', 600, 0, 600),
		'Z_SS' : ('e_m_SS', 20, 0, 2),
		'ePt' : ('ePt', 100, 0, 400),
		'eEta' : ('eEta', 100, -5, 5),
		'eJetPt' : ('eJetPt', 100, 0, 400),
		'mPt' : ('mPt', 100, 0, 400),
		'mEta' : ('mEta', 100, -5, 5),
		'mJetPt' : ('mJetPt', 100, 0, 400),
		'eRelIsoDB03' : ('eIsoDB03', 200, 0, 1),
		#'ePVDZ' : ('ePVDZ', 100, -1, 1),
		#'ePVDXY' : ('ePVDXY', 100, -.2, .2),
		'mRelIsoDB03' : ('mIsoDB03', 200, 0, 1),
		#'mPVDZ' : ('mPVDZ', 100, -1, 1),
		#'mPVDXY' : ('mPVDXY', 100, -.2, .2),
		'eMtToMET' : ('eMtToMET', 100, 0, 400),
		'mMtToMET' : ('mMtToMET', 100, 0, 400),
	}
	return chanVarMap

# Provides a list of histos to create for 'TT' channel
def getTTHistoDict() :
	chanVarMap = {
		'Z_Pt' : ('t1_t2_Pt', 400, 0, 400),
		'Z_Mass' : ('t1_t2_Mass', 600, 0, 600),
		'Z_SS' : ('t1_t2_SS', 20, 0, 2),
		't1Pt' : ('t1Pt', 100, 0, 400),
		't1Eta' : ('t1Eta', 100, -5, 5),
		't1ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t1ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 5),
		#'t1ByIsolationMVA3newDMwLTraw' : ('t1ByIsolationMVA3newDMwLTraw', 100, -1, 1),
		#'t1ByIsolationMVA3newDMwoLTraw' : ('t1ByIsolationMVA3newDMwoLTraw', 100, -1, 1),
		#'t1ByIsolationMVA3oldDMwLTraw' : ('t1ByIsolationMVA3oldDMwLTraw', 100, -1, 1),
		#'t1ByIsolationMVA3oldDMwoLTraw' : ('t1ByIsolationMVA3oldDMwoLTraw', 100, -1, 1),
		't1ChargedIsoPtSum' : ('t1ChargedIsoPtSum', 100, 0, 10),
		't1NeutralIsoPtSum' : ('t1NeutralIsoPtSum', 100, 0, 10),
		't1PuCorrPtSum' : ('t1PuCorrPtSum', 40, 0, 40),
		't1MtToPFMET' : ('t1MtToPFMET', 100, 0, 400),
		't1DecayMode' : ('t1DecayMode', 12, 0, 12),
		't1JetPt' : ('t1JetPt', 100, 0, 400),
        't1Mass' : ('t1Mass', 60, 0, 3),
		't2Pt' : ('t2Pt', 100, 0, 400),
		't2Eta' : ('t2Eta', 100, -5, 5),
		't2ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t2ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 5),
		#'t2ByIsolationMVA3newDMwLTraw' : ('t1ByIsolationMVA3newDMwLTraw', 100, -1, 1),
		#'t2ByIsolationMVA3newDMwoLTraw' : ('t1ByIsolationMVA3newDMwoLTraw', 100, -1, 1),
		#'t2ByIsolationMVA3oldDMwLTraw' : ('t1ByIsolationMVA3oldDMwLTraw', 100, -1, 1),
		#'t2ByIsolationMVA3oldDMwoLTraw' : ('t1ByIsolationMVA3oldDMwoLTraw', 100, -1, 1),
		't2ChargedIsoPtSum' : ('t1ChargedIsoPtSum', 100, 0, 10),
		't2NeutralIsoPtSum' : ('t1NeutralIsoPtSum', 100, 0, 10),
		't2PuCorrPtSum' : ('t1PuCorrPtSum', 40, 0, 40),
		't2MtToPFMET' : ('t2MtToPFMET', 100, 0, 400),
		't2DecayMode' : ('t2DecayMode', 12, 0, 12),
		't2JetPt' : ('t2JetPt', 100, 0, 400),
        't2Mass' : ('t2Mass', 60, 0, 3),
	}
	return chanVarMap

# EM Baseline
emKin   = 'ePt > 13 && eAbsEta < 2.5 && mPt > 10 && mAbsEta < 2.4'
eID     = 'ePassesConversionVeto == 1 && eMissingHits <= 1 && eMVANonTrigWP80 == 1' #eCBIDMedium == 1
mID     = 'mPFIDMedium == 1'
emDR    = 'e_m_DR > 0.3'
emVtx   = 'abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045'
#e23m8   = '(singleESingleMuPass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1 && eMu8Ele23Filter == 1 && mMu8Ele23Filter == 1 && ePt > 24)'
#m23e12  = '(singleMuSingleEPass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1 && eMu23Ele12Filter == 1 && mMu23Ele12Filter == 1 && mPt > 24)'
e23m8   = '(singleESingleMuPass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1  && ePt > 24)'
m23e12  = '(singleMuSingleEPass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1  && mPt > 24)'
# EM PostSync
emOS    = 'e_m_SS == 0'
emSS    = 'e_m_SS == 1'
emIso   = 'eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault < 0.15'
extraVeto   = 'eVetoZTT10 == 0 && muVetoZTT10 == 0'
# EM Studies
emQCDPreIso = 'eRelPFIsoDB < 0.2 && mRelPFIsoDBDefault < 1.0'
emIsoInvertM    = 'eRelPFIsoDB < 0.15 && mRelPFIsoDBDefault > 0.15'

# TT Baseline
ttKin   = 't1Pt > 45 && t1AbsEta < 2.1 && t2Pt > 45 && t2AbsEta < 2.1'
ttCharge    = 'abs( t1Charge ) == 1 && abs( t2Charge ) == 1'
ttDR    = 't1_t2_DR > 0.5'
ttVtx   = 'abs( t1PVDZ ) < 0.2 && abs( t2PVDZ ) < 0.2'
tt40    = 'doubleTauPass == 1 && t1MatchesDoubleTau40Path == 1 && t2MatchesDoubleTau40Path == 1 && t1DoubleTau40Filter > 0 && t2DoubleTau40Filter > 0'
# TT PostSync
ttOS    = 't1_t2_SS == 0'
ttSS    = 't1_t2_SS == 1'
ttIso   = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0'
ttDisc  = 't1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
# TT Studies
ttIsoInvert = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits > 2.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits > 2.0'
ttQCDPreIso = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0'

# A version which applies all cuts at once RunII
def quickCutMapSingleCut( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['PostSync'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e23m8 + ' || ' + m23e12 + ') && ' + emOS + ' && ' + emIso + ' && ' + extraVeto
    if ch == 'tt':
        cutMap['PostSync'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && ' + ttVtx + ' && ' + ttOS + ' && ' + ttIso + ' && ' + ttDisc + ' && ' + extraVeto + ' && ' + tt40
    return cutMap

# 2 stage RunII
def quickCutMap( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['BaseLine'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e23m8 + ' || ' + m23e12 + ')'
        cutMap['PostSync'] = emOS + ' && ' + emIso + ' && ' + extraVeto
    if ch == 'tt':
        cutMap['BaseLine'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && '  + ttVtx + ' && ' + tt40
        cutMap['PostSync'] = ttOS + ' && ' + ttIso + ' && ' + ttDisc + ' && ' + extraVeto
    return cutMap
    
# Selection which only does baseline for sync sample
def quickCutMapSync( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['BaseLine'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e23m8 + ' || ' + m23e12 + ')'
    if ch == 'tt':
        cutMap['BaseLine'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && '  + ttVtx + ' && ' + tt40
    return cutMap
    

# QCD DATA DRIVEN MODELING RunII - JULY 28 2015
def quickCutMapDataSS( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['BaseLine'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e23m8 + ' || ' + m23e12 + ')'
        cutMap['PostSync'] = emSS + ' && ' + emIso + ' && ' + extraVeto
    if ch == 'tt':
        cutMap['BaseLine'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && ' + ttVtx
        cutMap['PostSync'] = ttSS + ' && ' + ttIso + ' && ' + ttDisc + ' && ' + extraVeto
    return cutMap
	
# QCD DATA DRIVEN MODELING RunII - JULY 30 2015
def quickCutMapDataInversion( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['BaseLine'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e23m8 + ' || ' + m23e12 + ')'
        cutMap['Invert_DATA'] = emIsoInvertM + ' && ' + extraVeto
    if ch == 'tt':
        cutMap['BaseLine'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && ' + ttVtx
        cutMap['PostSync'] = ttIsoInvert + ' && ' + ttDisc + ' && ' + extraVeto
    return cutMap

# Apply QCD estimation cuts one at a time
def getCutMapQuickQCD( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['qcd_pre'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && (' + e23m8 + ' || ' + m23e12 + ') && ' + emOS + ' && ' + extraVeto + ' && ' + emQCDPreIso
        cutMap['qcd_post'] = emIso + ' && ' + eID + ' && ' + mID
    if ch == 'tt':
        cutMap['qcd_pre'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && ' + ttVtx + ' && ' + ttOS + ' && ' + ttDisc + ' && ' + extraVeto + ' && ' + ttQCDPreIso
        cutMap['qcd_post'] = ttIso
    return cutMap

