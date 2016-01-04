import ROOT
from collections import OrderedDict

def makeGenCut( inTree, cutString ) :
	#print "l1 %s, l2 %s" % (l1, l2)
	outTree = inTree.CopyTree( cutString )
	return outTree

# EM Baseline
emKin   = 'ePt > 13 && eAbsEta < 2.5 && mPt > 10 && mAbsEta < 2.4'
eID     = 'ePassesConversionVeto == 1 && eMissingHits <= 1 && eMVANonTrigWP80 == 1' #eCBIDMedium == 1
eIDLoose     = 'eMVANonTrigWP90 == 1'
mID     = 'mPFIDMedium == 1'
mIDLoose     = 'mPFIDLoose == 1'
emDR    = 'e_m_DR > 0.3'
emVtx   = 'abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045'
#e23m8   = '(singleESingleMuPass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1 && eMu8Ele23Filter == 1 && mMu8Ele23Filter == 1 && ePt > 24)'
#m23e12  = '(singleMuSingleEPass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1 && eMu23Ele12Filter == 1 && mMu23Ele12Filter == 1 && mPt > 24)'
e23m8   = '(singleE23SingleMu8Pass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1  && ePt > 24)'
m23e12  = '(singleMu23SingleE12Pass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1  && mPt > 24)'
e17m8   = '(singleE17SingleMu8Pass > 0 && eMatchesMu8Ele17Path == 1 && mMatchesMu8Ele17Path == 1 && ePt > 18)'
m17e12  = '(singleMu17SingleE12Pass > 0 && eMatchesMu17Ele12Path == 1 && mMatchesMu17Ele12Path == 1 && mPt > 18)'
# EM PostSync
emOS    = 'e_m_SS == 0'
emSS    = 'e_m_SS == 1'
emIso   = 'eIsoDB03 < 0.15 && mIsoDB03 < 0.15'
emIsoLoose   = 'eIsoDB03 < 0.3 && mIsoDB03 < 0.3'
extraVeto   = 'eVetoZTT10new2 == 0 && muVetoZTT10new2 == 0'
emMTFix = '( (type1_pfMetEt > 1) || ( eMtToPfMet_Raw > 5 && mMtToPfMet_Raw > 5 ) )'
# EM Studies
emQCDPreIso = 'eIsoDB03 < 0.2 && mIsoDB03 < 1.0'
emIsoInvertM    = 'eIsoDB03 < 0.15 && mIsoDB03 > 0.15'
emIsoInvert    = 'eIsoDB03 > 0.5 && mIsoDB03 > 0.25'

# TT Baseline
DecayMode = '(t1DecayMode != 5 && t1DecayMode != 6) && (t2DecayMode != 5 && t2DecayMode != 6)'
ttKin   = 't1Pt > 45 && t1AbsEta < 2.1 && t2Pt > 45 && t2AbsEta < 2.1'
ttCharge    = 'abs( t1Charge ) == 1 && abs( t2Charge ) == 1'
ttDR    = 't1_t2_DR > 0.5'
ttVtx   = 'abs( t1PVDZ ) < 0.2 && abs( t2PVDZ ) < 0.2'
tt40    = 'doubleTau40Pass == 1 && t1MatchesDoubleTau40Path == 1 && t2MatchesDoubleTau40Path == 1 && t1DoubleTau40Filter > 0 && t2DoubleTau40Filter > 0'
tt35    = 'doubleTau35Pass == 1 && t1MatchesDoubleTau35Path == 1 && t2MatchesDoubleTau35Path == 1 && t1DoubleTau35Filter > 0 && t2DoubleTau35Filter > 0'
# TT PostSync
ttOS    = 't1_t2_SS == 0'
ttSS    = 't1_t2_SS == 1'
ttIso   = 't1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5'
ttIsoLoose   = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0'
ttDisc  = 't1AgainstElectronVLooseMVA5 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA5 > 0.5 && t2AgainstMuonLoose3 > 0.5'
ttMTFix = '( (type1_pfMetEt > 1) || ( t1MtToPfMet_Raw > 5 && t2MtToPfMet_Raw > 5 ) )'
# TT Studies
ttIsoInvert = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits > 3.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits > 3.0'
ttQCDPreIso = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0'


# A version which applies all cuts at once RunII - NO SIGN SO WE CAN DO QCD
def signalCutsNoSign( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['PostSync'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e17m8 + ' || ' + m17e12 + ') && ' + emIso + ' && ' + extraVeto + ' && ' + emMTFix
    if ch == 'tt':
        cutMap['PostSync'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && ' + ttVtx + ' && ' + ttIso + ' && ' + ttDisc + ' && ' + extraVeto + ' && ' + tt40 + ' && ' + DecayMode + ' && ' + ttMTFix
    return cutMap


# A version which applies all cuts at once RunII
def signalCuts( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['PostSync'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e17m8 + ' || ' + m17e12 + ') && ' + emOS + ' && ' + emIso + ' && ' + extraVeto + ' && ' + emMTFix
    if ch == 'tt':
        cutMap['PostSync'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && ' + ttVtx + ' && ' + ttOS + ' && ' + ttIso + ' && ' + ttDisc + ' && ' + extraVeto + ' && ' + tt40 + ' && ' + DecayMode + ' && ' + ttMTFix
    return cutMap


# Data card sync, no Decay Mode cut 
def signalCutsNoIsoNoSign( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['PostSync'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e17m8 + ' || ' + m17e12 + ') && ' + extraVeto + ' && ' + emMTFix
    if ch == 'tt':
        cutMap['PostSync'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && ' + ttVtx + ' && ' + ttDisc + ' && ' + extraVeto + ' && ' + tt40 + ' && ' + DecayMode + ' && ' + ttMTFix
    return cutMap

    
# Selection which only does baseline for sync data cards, NO SIGN for QCD
def syncCutsDC( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['BaseLine'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e17m8 + ' || ' + m17e12 + ') && ' + emIso + ' && ' + extraVeto
    if ch == 'tt':
        cutMap['BaseLine'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && ' + ttVtx + ' && ' + ttIso + ' && ' + ttDisc + ' && ' + extraVeto + ' && ' + tt40
    return cutMap
    

# Selection which only does baseline for sync sample
def syncCutsNtuple( ch ) :
    cutMap = OrderedDict()
    if ch == 'em':
        cutMap['BaseLine'] = emKin + ' && ' + emDR + ' && ' + emVtx + ' && ' + eID + ' && ' + mID + ' && (' + e17m8 + ' || ' + m17e12 + ')'
    if ch == 'tt':
        cutMap['BaseLine'] = ttKin + ' && ' + ttCharge + ' && ' + ttDR + ' && '  + ttVtx + ' && ' + tt40
    return cutMap
    





