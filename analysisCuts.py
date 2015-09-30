import ROOT
from collections import OrderedDict

def makeGenCut( inTree, cutString ) :
	#print "l1 %s, l2 %s" % (l1, l2)
	outTree = inTree.CopyTree( cutString )
	return outTree

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
emIso   = 'eIsoDB03 < 0.15 && mIsoDB03 < 0.15'
extraVeto   = 'eVetoZTT10 == 0 && muVetoZTT10 == 0'
# EM Studies
emQCDPreIso = 'eIsoDB03 < 0.2 && mIsoDB03 < 1.0'
emIsoInvertM    = 'eIsoDB03 < 0.15 && mIsoDB03 > 0.15'

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

