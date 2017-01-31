import ROOT

def makeGenCut( inTree, cutString ) :
	#print "l1 %s, l2 %s" % (l1, l2)
	outTree = inTree.CopyTree( cutString )
	return outTree


#######################
### HTT-EM Baseline ###
#######################
emKin   = 'ePt > 13 && eAbsEta < 2.5 && mPt > 10 && mAbsEta < 2.4'
eID     = 'ePassesConversionVeto == 1 && eMissingHits <= 1 && eMVANonTrigWP80 == 1' #eCBIDMedium == 1
mID     = 'mPFIDMedium == 1'
emDR    = 'e_m_DR > 0.3'
emVtx   = 'abs(ePVDZ) < 0.2 && abs(ePVDXY) < 0.045 && abs(mPVDZ) < 0.2 && abs(mPVDXY) < 0.045'
#e23m8   = '(singleESingleMuPass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1 && eMu8Ele23Filter == 1 && mMu8Ele23Filter == 1 && ePt > 24)'
#m23e12  = '(singleMuSingleEPass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1 && eMu23Ele12Filter == 1 && mMu23Ele12Filter == 1 && mPt > 24)'
e23m8   = '(singleE23SingleMu8Pass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1  && ePt > 24)'
m23e12  = '(singleMu23SingleE12Pass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1  && mPt > 24)'
### I have MUCH better sync with IC without filters applied in EMu ###
#e17m8   = '(singleE17SingleMu8Pass > 0 && eMatchesMu8Ele17Path == 1 && mMatchesMu8Ele17Path == 1 && eMu8Ele23Filter > 0 && mMu8Ele23Filter > 0 && ePt > 18)'
#m17e12  = '(singleMu17SingleE12Pass > 0 && eMatchesMu17Ele12Path == 1 && mMatchesMu17Ele12Path == 1 && eMu17Ele12Filter > 0 && mMu17Ele12Filter > 0 && mPt > 18)'
e17m8   = '(singleE17SingleMu8Pass > 0 && eMatchesMu8Ele17Path == 1 && mMatchesMu8Ele17Path == 1 && ePt > 18)'
m17e12  = '(singleMu17SingleE12Pass > 0 && eMatchesMu17Ele12Path == 1 && mMatchesMu17Ele12Path == 1 && mPt > 18)'
emTrig = '('+e17m8+'||'+m17e12+')'
# EM PostSync
emOS    = 'e_m_SS == 0'
emSS    = 'e_m_SS == 1'
emIso   = 'eIsoDB03 < 0.15 && mIsoDB03 < 0.2'
extraVeto   = 'eVetoZTTp001dxyz == 0 && muVetoZTTp001dxyz == 0'


#######################
### HTT-TT Baseline ###
#######################
extraVetoTT   = 'eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 == 0'
#DecayMode = '(t1DecayMode != 5 && t1DecayMode != 6) && (t2DecayMode != 5 && t2DecayMode != 6)'
DecayMode = 't1DecayModeFinding == 1 && t2DecayModeFinding == 1'
ttKin37   = 't1Pt > 37 && t1AbsEta < 2.1 && t2Pt > 37 && t2AbsEta < 2.1'
ttKin40   = 't1Pt > 40 && t1AbsEta < 2.1 && t2Pt > 40 && t2AbsEta < 2.1'
ttKin5040   = 't1Pt > 50 && t1AbsEta < 2.1 && t2Pt > 40 && t2AbsEta < 2.1'
ttKin40TES   = '(t1Pt*1.03) > 40 && t1AbsEta < 2.1 && (t2Pt*1.03) > 40 && t2AbsEta < 2.1'
ttKin5040TES   = '(t1Pt*1.03) > 50 && t1AbsEta < 2.1 && (t2Pt*1.03) > 40 && t2AbsEta < 2.1'
ttCharge    = 'abs( t1Charge ) == 1 && abs( t2Charge ) == 1'
ttDR    = 't1_t2_DR > 0.5'
ttVtx   = 'abs( t1PVDZ ) < 0.2 && abs( t2PVDZ ) < 0.2'
tt40    = 'doubleTau40Pass == 1 && t1MatchesDoubleTau40Path == 1 && t2MatchesDoubleTau40Path == 1 && t1MatchesDoubleTau40Filter > 0 && t2MatchesDoubleTau40Filter > 0'
tt35    = '((doubleTau35Pass > 0 && t1MatchesDoubleTau35Path > 0 && t2MatchesDoubleTau35Path > 0 && t1MatchesDoubleTau35Filter > 0 && t2MatchesDoubleTau35Filter > 0) || (doubleTauCmbIso35RegPass > 0 && t1MatchesDoubleTauCmbIso35RegPath > 0 && t2MatchesDoubleTauCmbIso35RegPath > 0 && t1MatchesDoubleTauCmbIso35RegFilter > 0 && t2MatchesDoubleTauCmbIso35RegFilter > 0))'
tt32    = 'doubleTau32Pass > 0 && t1MatchesDoubleTau32Path > 0 && t2MatchesDoubleTau32Path > 0 && t1MatchesDoubleTau32Filter > 0 && t2MatchesDoubleTau32Filter > 0'
# TT PostSync
ttL1IsoTaus = 't1L1IsoTauMatch > 0 && t2L1IsoTauMatch > 0 && doubleL1IsoTauMatch > 0' # Used in 2015 for double tau trigger screw up
ttOS    = 't1_t2_SS == 0'
ttSS    = 't1_t2_SS == 1'
#ttIso   = 't1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5'
ttIso   = 't1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5'
ttIsoTight   = 't1ByTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByTightIsolationMVArun2v1DBoldDMwLT > 0.5'
ttIsoLooseMVA   = 't1ByLooseIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByLooseIsolationMVArun2v1DBoldDMwLT > 0.5'
ttIsoVLooseMVA   = 't1ByVLooseIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVLooseIsolationMVArun2v1DBoldDMwLT > 0.5'
ttIsoVVLooseMVA   = 't1ByIsolationMVArun2v1DBoldDMwLTraw > 0. && t2ByIsolationMVArun2v1DBoldDMwLTraw > 0.' # This corresponds to the loosest mva cut at high pt for VVLoose. The actual VVLoose variable is added after our initial cuts in step 2
ttDisc  = 't1AgainstElectronVLooseMVA6 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA6 > 0.5 && t2AgainstMuonLoose3 > 0.5'
# TT Studies
ttIsoInvert = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits > 3.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits > 3.0'
ttQCDPreIso = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0'

# AtoZh
ZMass = 'LEG1_LEG2_Mass > 60 && LEG1_LEG2_Mass < 120'
ZDXYZ = 'LEG1PVDXY < 0.045 && LEG1PVDZ < 0.2 && LEG2PVDXY < 0.045 && LEG2PVDZ < 0.2'
HDXYZ = 'LEG3PVDXY < 0.045 && LEG3PVDZ < 0.2 && LEG4PVDXY < 0.045 && LEG4PVDZ < 0.2'
ZOS = 'LEG1_LEG2_SS == 0'
HOS = 'LEG3_LEG4_SS == 0'
HSS = 'LEG3_LEG4_SS == 1'

# EE for Z cand legs
# Preselection
eeTrig = 'doubleE_23_12Pass > 0'
#eePt = '((LEG1Pt > 24 && LEG2Pt > 13) || (LEG2Pt > 24 && LEG1Pt > 13))'
eePt = 'LEG1Pt > 10 && LEG2Pt > 10'
eeEta = 'abs(LEG1Eta) < 2.5 && abs(LEG2Eta) < 2.5'
eeIso = 'e1IsoDB03 < 0.3 && e2IsoDB03 < 0.3'
eeHits = 'e1PassesConversionVeto > 0 && e1MissingHits < 2 && e2PassesConversionVeto > 0 && e2MissingHits < 2'
eeIDL = 'LEG1MVANonTrigWP90 > 0 && LEG2MVANonTrigWP90 > 0'

# MM for Z cand legs
mmTrig = 'doubleMuPass > 0'
#mmPt = '((LEG1Pt > 18 && LEG2Pt > 9) || (LEG2Pt > 18 && LEG1Pt > 9))'
mmPt = 'LEG1Pt > 10 && LEG2Pt > 10'
mmEta = 'abs(LEG1Eta) < 2.4 && abs(LEG2Eta) < 2.4'
mmIso = 'm1IsoDB04 < 0.25 && m2IsoDB04 < 0.25'
mmIDL = 'LEG1PFIDLoose > 0 && LEG2PFIDLoose > 0'

# ET Higgs
eeetE = 'e3Pt > 10 && abs(e3Eta) < 2.5 && e3IsoDB03 < 0.3 && e3MVANonTrigWP90 > 0'
eeetERed = 'e3Pt > 10 && abs(e3Eta) < 2.5'
mmetE = 'ePt > 10 && abs(eEta) < 2.5 && eIsoDB03 < 0.3 && eMVANonTrigWP90 > 0'
mmetERed = 'ePt > 10 && abs(eEta) < 2.5'
xxetT = 'tPt > 20 && abs(tEta) < 2.1 && tByLooseIsolationMVArun2v1DBoldDMwLT > 0 && tDecayModeFinding == 1 && tAgainstElectronVLooseMVA6 == 1'
xxetTRed = 'tPt > 20 && abs(tEta) < 2.1 && tDecayModeFinding == 1 && tAgainstElectronVLooseMVA6 == 1' 
eeetVetos = 'eVetoZTTp001dxyzR0 <= 3 && muVetoZTTp001dxyzR0 == 0'
mmetVetos = 'eVetoZTTp001dxyzR0 <= 1 && muVetoZTTp001dxyzR0 <= 2'
# MT Higgs
eemtM = 'mPt > 10 && abs(mEta) < 2.4 && mIsoDB04 < 0.25 && mPFIDLoose > 0'
eemtMRed = 'mPt > 10 && abs(mEta) < 2.4'
mmmtM = 'm3Pt > 10 && abs(m3Eta) < 2.4 && m3IsoDB04 < 0.25 && m3PFIDLoose > 0'
mmmtMRed = 'm3Pt > 10 && abs(m3Eta) < 2.4'
xxmtT = 'tPt > 20 && abs(tEta) < 2.1 && tByLooseIsolationMVArun2v1DBoldDMwLT > 0 && tDecayModeFinding == 1 && tAgainstMuonLoose3 == 1'
xxmtTRed = 'tPt > 20 && abs(tEta) < 2.1 && tDecayModeFinding == 1 && tAgainstMuonLoose3 == 1'
eemtVetos = 'eVetoZTTp001dxyzR0 <= 2 && muVetoZTTp001dxyzR0 <= 1'
mmmtVetos = 'eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 <= 3'
# TT Higgs
xxttTT = 't1Pt > 20 && abs(t1Eta) < 2.1 && t2Pt > 20 && abs(t2Eta) < 2.1 && t1ByLooseIsolationMVArun2v1DBoldDMwLT > 0 && t2ByLooseIsolationMVArun2v1DBoldDMwLT > 0 && t1DecayModeFinding == 1 && t2DecayModeFinding == 1 && t1AgainstElectronVLooseMVA6 == 1 && t1AgainstMuonLoose3 == 1 && t2AgainstElectronVLooseMVA6 == 1 && t2AgainstMuonLoose3 == 1'
xxttTTRed = 't1Pt > 20 && abs(t1Eta) < 2.1 && t2Pt > 20 && abs(t2Eta) < 2.1 && t1DecayModeFinding == 1 && t2DecayModeFinding == 1 && t1AgainstElectronVLooseMVA6 == 1 && t1AgainstMuonLoose3 == 1 && t2AgainstElectronVLooseMVA6 == 1 && t2AgainstMuonLoose3 == 1'
eettVetos = 'eVetoZTTp001dxyzR0 <= 2 && muVetoZTTp001dxyzR0 == 0'
mmttVetos = 'eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 <= 2'
# EM Higgs
eeemE = 'e3Pt > 10 && abs(e3Eta) < 2.5 && e3IsoDB03 < 0.3 && e3MVANonTrigWP90 > 0'
mmemE = 'ePt > 10 && abs(eEta) < 2.5 && eIsoDB03 < 0.3 && eMVANonTrigWP90 > 0'
eeemM = 'mPt > 10 && abs(mEta) < 2.4 && mIsoDB04 < 0.25 && mPFIDLoose > 0'
mmemM = 'm3Pt > 10 && abs(m3Eta) < 2.4 && m3IsoDB04 < 0.25 && m3PFIDLoose > 0'
eeemERed = 'e3Pt > 10 && abs(e3Eta) < 2.5'
mmemERed = 'ePt > 10 && abs(eEta) < 2.5'
eeemMRed = 'mPt > 10 && abs(mEta) < 2.4'
mmemMRed = 'm3Pt > 10 && abs(m3Eta) < 2.4'
eeemVetos = 'eVetoZTTp001dxyzR0 <= 3 && muVetoZTTp001dxyzR0 <= 1'
mmemVetos = 'eVetoZTTp001dxyzR0 <= 1 && muVetoZTTp001dxyzR0 <= 3'
# EE & MM Higgs (ZZ control region)
eeee = 'e3Pt > 10 && abs(e3Eta) < 2.5 && e3IsoDB03 < 0.3 && e3MVANonTrigWP90 > 0 && e4Pt > 10 && abs(e4Eta) < 2.5 && e4IsoDB03 < 0.3 && e4MVANonTrigWP90 > 0'
mmmm = 'm3Pt > 10 && abs(m3Eta) < 2.4 && m3IsoDB04 < 0.25 && m3PFIDLoose> 0 && m4Pt > 10 && abs(m4Eta) < 2.4 && m4IsoDB04 < 0.25 && m4PFIDLoose > 0'
eemm = 'm1Pt > 10 && abs(m1Eta) < 2.4 && m1IsoDB04 < 0.25 &&  m1PFIDLoose > 0 && m2Pt > 10 && abs(m2Eta) < 2.4 && m2IsoDB04 < 0.25 && m2PFIDLoose > 0'
eeeeRed = 'e3Pt > 10 && abs(e3Eta) < 2.5 && e4Pt > 10 && abs(e4Eta) < 2.5'
mmmmRed = 'm3Pt > 10 && abs(m3Eta) < 2.4 && m4Pt > 10 && abs(m4Eta) < 2.4'
eemmRed = 'm1Pt > 10 && abs(m1Eta) < 2.4 && m2Pt > 10 && abs(m2Eta) < 2.4'
eeeeVetos = 'eVetoZTTp001dxyzR0 <= 4 && muVetoZTTp001dxyzR0 == 0'
mmmmVetos = 'eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 <= 4'
eemmVetos = 'eVetoZTTp001dxyzR0 <= 2 && muVetoZTTp001dxyzR0 <= 2'

# Basic lepton definitions for ZH analysis
def eBase( lep ) :
    return 'LEG_Pt > 10 && abs(LEG_Eta) < 2.5 && LEG_PassesConversionVeto > 0.5 && LEG_MissingHits < 2 && LEG_PVDXY < 0.045 && LEG_PVDZ < 0.2'.replace('LEG_',lep)
def eTight( lep ) :
    return 'LEG_Pt > 10 && abs(LEG_Eta) < 2.5 && LEG_PassesConversionVeto > 0.5 && LEG_MissingHits < 2 && LEG_PVDXY < 0.045 && LEG_PVDZ < 0.2 && LEG_IsoDB03 < 0.3 && LEG_MVANonTrigWP90 > 0.5'.replace('LEG_',lep)

def mBase( lep ) :
    return 'LEG_Pt > 10 && abs(LEG_Eta) < 2.4 && LEG_PVDXY < 0.045 && LEG_PVDZ < 0.2'.replace('LEG_',lep)
def mTight( lep ) :
    return 'LEG_Pt > 10 && abs(LEG_Eta) < 2.4 && LEG_PVDXY < 0.045 && LEG_PVDZ < 0.2 && LEG_IsoDB04 < 0.25 && LEG_PFIDLoose > 0.5'.replace('LEG_',lep)

def tBase( lep ) :
    return 'LEG_Pt > 20 && abs(LEG_Eta) < 2.3 && LEG_DecayModeFinding == 1 && LEG_AgainstElectronVLooseMVA6 == 1 && LEG_AgainstMuonLoose3 == 1 && abs( LEG_Charge ) == 1'.replace('LEG_',lep)
def tTight( lep ) :
    return 'LEG_Pt > 20 && abs(LEG_Eta) < 2.3 && LEG_ByMediumIsolationMVArun2v1DBoldDMwLT > 0.5 && LEG_DecayModeFinding == 1 && LEG_AgainstElectronVLooseMVA6 == 1 && LEG_AgainstMuonLoose3 == 1 && abs( LEG_Charge ) == 1'.replace('LEG_',lep)
def tAntiEV ( lep ) :
    return 'LEG_AgainstElectronTightMVA6 == 1'.replace('LEG_',lep)
def tAntiMV ( lep ) :
    return 'LEG_AgainstMuonTight3 == 1'.replace('LEG_',lep)

def eeTrigPt(lep1='e1', lep2='e2') :
    return '(((LEG1_Pt > 24 && LEG2_Pt > 13) || (LEG2_Pt > 24 && LEG1_Pt > 13)) && LEG1_MatchesDoubleE23_12Path > 0 && LEG2_MatchesDoubleE23_12Path > 0)'.replace('LEG1_',lep1).replace('LEG2_',lep2)
def eeeTrigPt() :
    match1_2 = eeTrigPt('e1', 'e2')
    match1_3 = eeTrigPt('e1', 'e3')
    match2_3 = eeTrigPt('e2', 'e3')
    comb = ' || '.join( [match1_2, match1_3, match2_3] )
    return '('+comb+')'
def eeeeTrigPt() :
    match1_2 = eeTrigPt('e1', 'e2')
    match1_3 = eeTrigPt('e1', 'e3')
    match1_4 = eeTrigPt('e1', 'e4')
    match2_3 = eeTrigPt('e2', 'e3')
    match2_4 = eeTrigPt('e2', 'e4')
    match3_4 = eeTrigPt('e3', 'e4')
    comb = ' || '.join( [match1_2, match1_3, match1_4, match2_3, match2_4, match3_4] )
    return '('+comb+')'
def mmTrigPt(lep1='m1', lep2='m2') :
    return '((LEG1_Pt > 18 || LEG2_Pt > 18) && LEG1_MatchesDoubleMu > 0 && LEG2_MatchesDoubleMu > 0)'.replace('LEG1_',lep1).replace('LEG2_',lep2)
def mmmTrigPt() :
    match1_2 = mmTrigPt('m1', 'm2')
    match1_3 = mmTrigPt('m1', 'm3')
    match2_3 = mmTrigPt('m2', 'm3')
    comb = ' || '.join( [match1_2, match1_3, match2_3] )
    return '('+comb+')'
def mmmmTrigPt() :
    match1_2 = mmTrigPt('m1', 'm2')
    match1_3 = mmTrigPt('m1', 'm3')
    match1_4 = mmTrigPt('m1', 'm4')
    match2_3 = mmTrigPt('m2', 'm3')
    match2_4 = mmTrigPt('m2', 'm4')
    match3_4 = mmTrigPt('m3', 'm4')
    comb = ' || '.join( [match1_2, match1_3, match1_4, match2_3, match2_4, match3_4] )
    return '('+comb+')'

def llltDR( l1,l2,l3,l4 ) :
    dr = 'LEG1_LEG4_DR > 0.5 && LEG2_LEG3_DR > 0.5 && LEG2_LEG4_DR > 0.5 && LEG3_LEG4_DR > 0.5'
    return dr.replace('LEG1',l1).replace('LEG2',l2).replace('LEG3',l3).replace('LEG4',l4)

def llttDR( l1,l2,l3,l4 ) :
    dr = 'LEG1_LEG3_DR > 0.5 && LEG1_LEG4_DR > 0.5 && LEG2_LEG3_DR > 0.5 && LEG2_LEG4_DR > 0.5 && LEG3_LEG4_DR > 0.5'
    return dr.replace('LEG1',l1).replace('LEG2',l2).replace('LEG3',l3).replace('LEG4',l4)


def getCut( analysis, channel, cutName, isData=False, isReHLT=False ) :
    
    #triggers = [tt40, tt35,]

    cutMap = { 
        'htt' : # analysis
        { 'tt' : {
            # A version which applies all cuts at once RunII
            'signalCuts' : [ttKin40, ttCharge, ttDR, ttVtx, ttOS, ttIsoTight, ttDisc, extraVetoTT, tt35, DecayMode],
            'signalCuts5040' : [ttKin5040, ttCharge, ttDR, ttVtx, ttOS, ttIsoTight, ttDisc, extraVetoTT, tt35, DecayMode],
            # Not isolation for full QCD estimation
            'fakeFactorCutsTT' : [ttKin40, ttCharge, ttDR, ttVtx, ttOS, ttDisc, extraVetoTT, tt35, DecayMode],
            # Selection which only does baseline for sync data cards, NO SIGN for QCD and Loose Iso for TT QCD
            'syncCutsDCqcdTES' : [ttKin40TES, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode, ttIsoVLooseMVA ],
            'syncCutsDCqcdTES5040VVLoose' : [ttKin5040TES, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode, ttIsoVVLooseMVA ],
            'syncCutsDCqcdTES5040' : [ttKin5040TES, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode, ttIsoLooseMVA],
            'syncCutsDCqcdTES5040VL' : [ttKin5040TES, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode, ttIsoVLooseMVA],
            'syncCutsDCqcdTESNoIso' : [ttKin40TES, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode],
            # Selection which only does baseline for sync sample
            'syncCutsMSSMNtuple' : [ttKin40, ttCharge, ttDR, ttVtx, tt35, DecayMode],
            'syncCutsSMHTTNtuple' : [ttKin40, ttCharge, ttDR, ttVtx, tt35, DecayMode],
        }, # end tt channel
          'em' : {
            'syncCutsNtuple' : [emKin, emDR, emVtx, emTrig,],#'('+e23m8+'||'+m23e12+')'],
        }, # end em channel
        }, # end HTT analysis cuts
        'azh' : # analysis
        { 'eeee' : {
            'goodZ'  : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eeee, eeeeVetos],
            'HSS'    : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eeee, eeeeVetos],
            'RedBkg' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eeeeRed, eeeeVetos],
            'Skim'   : [ZOS, ZMass, eeTrig, eeeeTrigPt(), eeeeVetos, eTight('e1'), eTight('e2'), eBase('e3'), eBase('e4')],
            'SkimOS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS,  HDXYZ, eeeeRed, eeeeVetos],
        }, # end EEEE
         'eeet' : {
            'goodZ'  : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eeetE, xxetT, eeetVetos],
            'HSS'    : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eeetE, xxetT, eeetVetos],
            'RedBkg' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eeetERed, xxetTRed, eeetVetos],
            'Skim'   : [ZOS, ZMass, eeTrig, eeeTrigPt(), llltDR('e1','e2','e3','t'), eeetVetos, eTight('e1'), eTight('e2'), eBase('e3'), tBase('t'), tAntiEV('t')],
            'SkimOS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS,  HDXYZ, eeetERed, xxetTRed, eeetVetos],
        }, # end EEET
         'eett' : {
            'goodZ'  : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, xxttTT, eettVetos],
            'HSS'    : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, xxttTT, eettVetos],
            'RedBkg' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, xxttTTRed, eettVetos],
            'Skim'   : [ZOS, ZMass, eeTrig, eeTrigPt(), llttDR('e1','e2','t1','t2'), eettVetos, eTight('e1'), eTight('e2'), tBase('t1'), tBase('t2')],
            'SkimOS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS,  HDXYZ, xxttTTRed, eettVetos],
        }, # end EETT
         'eemt' : {
            'goodZ'  : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eemtM, xxmtT, eemtVetos],
            'HSS'    : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eemtM, xxmtT, eemtVetos],
            'RedBkg' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eemtMRed, xxmtTRed, eemtVetos],
            'Skim'   : [ZOS, ZMass, eeTrig, eeTrigPt(), llltDR('e1','e2','m','t'), eemtVetos, eTight('e1'), eTight('e2'), mBase('m'), tBase('t'), tAntiMV('t')],
            'Sync'   : [ZOS, ZMass, eeTrig, eeTrigPt(), llltDR('e1','e2','m','t'), eTight('e1'), eTight('e2'), mBase('m'), tBase('t'), tAntiMV('t')],
            'Sync2'   : ['e1Pt > 5',],
            'SkimOS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS,  HDXYZ, eemtMRed, xxmtTRed, eemtVetos],
        }, # end EEMT
         'eeem' : {
            'goodZ'  : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eeemE, eeemM, eeemVetos],
            'HSS'    : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eeemE, eeemM, eeemVetos],
            'RedBkg' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eeemERed, eeemMRed, eeemVetos],
            'Skim'   : [ZOS, ZMass, eeTrig, eeeTrigPt(), eeemVetos, eTight('e1'), eTight('e2'), eBase('e3'), mBase('m')],
            'SkimOS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS,  HDXYZ, eeemERed, eeemMRed, eeemVetos],
        }, # end EEEM
         'eemm' : {
            'goodZ'  : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eemm, eemmVetos],
            'HSS'    : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eemm, eemmVetos],
            'RedBkg' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eemmRed, eemmVetos],
            'Skim'   : [ZOS, ZMass, eeTrig, eeTrigPt(), eemmVetos, eTight('e1'), eTight('e2'), mBase('m1'), mBase('m2')],
            'SkimOS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS,  HDXYZ, eemmRed, eemmVetos],
        }, # end EEMM
         'mmmm' : {
            'goodZ'  : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, mmmm, mmmmVetos],
            'HSS'    : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmmm, mmmmVetos],
            'RedBkg' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmmmRed, mmmmVetos],
            'Skim'   : [ZOS, ZMass, mmTrig, mmmmTrigPt(), mmmmVetos, mTight('m1'), mTight('m2'), mBase('m3'), mBase('m4')],
            'SkimOS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS,  HDXYZ, mmmmRed, mmmmVetos],
        }, # end MMMM
         'emmt' : {
            'goodZ'  : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, mmetE, xxetT, mmetVetos],
            'HSS'    : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmetE, xxetT, mmetVetos],
            'RedBkg' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmetERed, xxetTRed, mmetVetos],
            'Skim'   : [ZOS, ZMass, mmTrig, mmTrigPt(), llltDR('m1','m2','e','t'), mmetVetos, mTight('m1'), mTight('m2'), eBase('e'), tBase('t'), tAntiEV('t')],
            'SkimOS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS,  HDXYZ, mmetERed, xxetTRed, mmetVetos],
        }, # end MMET
         'mmtt' : {
            'goodZ'  : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, xxttTT, mmttVetos],
            'HSS'    : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, xxttTT, mmttVetos],
            'RedBkg' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, xxttTTRed, mmttVetos],
            'Skim'   : [ZOS, ZMass, mmTrig, mmTrigPt(), llttDR('m1','m2','t1','t2'), mmttVetos, mTight('m1'), mTight('m2'), tBase('t1'), tBase('t2')],
            'SkimOS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS,  HDXYZ, xxttTTRed, mmttVetos],
        }, # end MMTT
         'mmmt' : {
            'goodZ'  : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, mmmtM, xxmtT, mmmtVetos],
            'HSS'    : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmmtM, xxmtT, mmmtVetos],
            'RedBkg' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmmtMRed, xxmtTRed, mmmtVetos],
            'Skim'   : [ZOS, ZMass, mmTrig, mmmTrigPt(), llltDR('m1','m2','m','t'), mmmtVetos, mTight('m1'), mTight('m2'), mBase('m3'), tBase('t'), tAntiMV('t')],
            'SkimOS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS,  HDXYZ, mmmtMRed, xxmtTRed, mmmtVetos],
        }, # end MMMT
         'emmm' : {
            'goodZ'  : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, mmemE, mmemM, mmemVetos],
            'HSS'    : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmemE, mmemM, mmemVetos],
            'RedBkg' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmemERed, mmemMRed, mmemVetos],
            'Skim'   : [ZOS, ZMass, mmTrig, mmmTrigPt(), mmemVetos, mTight('m1'), mTight('m2'), mBase('m3'), eBase('e')],
            'SkimOS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS,  HDXYZ, mmemERed, mmemMRed, mmemVetos],
        } # end MMEM
        } # end AZH analysis cuts
    } # end cutMap
    
    # Add a copy of the 'htt' analysis cuts under 'Sync'
    cutMap[ 'Sync' ] = cutMap[ 'htt' ]

    cuts1 = cutMap[ analysis ][ channel ][ cutName ]

    # Remove trigger requirements if MC except reHLT samples
    #if not isData :
    #    #if not isReHLT : 
    #    for trig in triggers :
    #        if trig in cuts1 :
    #            cuts1.remove( trig )

    prodMap = {
        'em' : ('e', 'm'),
        'et' : ('e', 't'),
        'mt' : ('m', 't'),
        'tt' : ('t1', 't2'),
        'eeem' : ('e1', 'e2', 'e3', 'm'),
        'eeet' : ('e1', 'e2', 'e3', 't'),
        'eemt' : ('e1', 'e2', 'm', 't'),
        'eett' : ('e1', 'e2', 't1', 't2'),
        'emmm' : ('m1', 'm2', 'e', 'm3'),
        'emmt' : ('m1', 'm2', 'e', 't'),
        'mmmt' : ('m1', 'm2', 'm3', 't'),
        'mmtt' : ('m1', 'm2', 't1', 't2'),
        'eeee' : ('e1', 'e2', 'e3', 'e4'),
        'eemm' : ('e1', 'e2', 'm1', 'm2'),
        'mmmm' : ('m1', 'm2', 'm3', 'm4'),
    }

    cutString = ''
    for item in cuts1 :
        tmp = item.replace( 'LEG1', prodMap[channel][0] )
        tmp = tmp.replace( 'LEG2', prodMap[channel][1] )
        if analysis == 'azh' :
            tmp = tmp.replace( 'LEG3', prodMap[channel][2] )
            tmp = tmp.replace( 'LEG4', prodMap[channel][3] )

        if cutString != '' :
            cutString += ' && '
        cutString += tmp
    cutString = '('+cutString+')'
    #print cutString
    return cutString



if __name__ == '__main__' :
    isData=False
    isReHLT=True
    cut = getCut( 'htt', 'tt', 'syncCutsDCqcd', isData, isReHLT )
    print cut + "\n\n"
    cut = getCut( 'htt', 'tt', 'syncCutsDCqcd', isData, not isReHLT )
    print cut + "\n\n"
    cut = getCut( 'htt', 'tt', 'syncCutsDCqcd', True )
    print cut + "\n\n"
    cut = getCut( 'azh', 'eeet', 'goodZ' )
    print cut + "\n\n"



