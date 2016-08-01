import ROOT

def makeGenCut( inTree, cutString ) :
	#print "l1 %s, l2 %s" % (l1, l2)
	outTree = inTree.CopyTree( cutString )
	return outTree


# TT Baseline
extraVetoTT   = 'eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 == 0'
#DecayMode = '(t1DecayMode != 5 && t1DecayMode != 6) && (t2DecayMode != 5 && t2DecayMode != 6)'
DecayMode = 't1DecayModeFinding == 1 && t2DecayModeFinding == 1'
ttKin   = 't1Pt > 37 && t1AbsEta < 2.1 && t2Pt > 37 && t2AbsEta < 2.1'
ttKinOld   = 't1Pt > 40 && t1AbsEta < 2.1 && t2Pt > 40 && t2AbsEta < 2.1'
ttKinTES   = '(t1Pt*1.03) > 40 && t1AbsEta < 2.1 && (t2Pt*1.03) > 40 && t2AbsEta < 2.1'
ttKinLoose   = 't1Pt > 35 && t1AbsEta < 2.1 && t2Pt > 35 && t2AbsEta < 2.1'
ttCharge    = 'abs( t1Charge ) == 1 && abs( t2Charge ) == 1'
ttDR    = 't1_t2_DR > 0.5'
ttVtx   = 'abs( t1PVDZ ) < 0.2 && abs( t2PVDZ ) < 0.2'
tt40    = 'doubleTau40Pass == 1 && t1MatchesDoubleTau40Path == 1 && t2MatchesDoubleTau40Path == 1 && t1MatchesDoubleTau40Filter > 0 && t2MatchesDoubleTau40Filter > 0'
tt35    = 'doubleTau35Pass > 0 && t1MatchesDoubleTau35Path > 0 && t2MatchesDoubleTau35Path > 0 && t1MatchesDoubleTau35Filter > 0 && t2MatchesDoubleTau35Filter > 0'
tt32    = 'doubleTau32Pass > 0 && t1MatchesDoubleTau32Path > 0 && t2MatchesDoubleTau32Path > 0 && t1MatchesDoubleTau32Filter > 0 && t2MatchesDoubleTau32Filter > 0'
# TT PostSync
ttL1IsoTaus = 't1L1IsoTauMatch > 0 && t2L1IsoTauMatch > 0 && doubleL1IsoTauMatch > 0' # Used in 2015 for double tau trigger screw up
ttOS    = 't1_t2_SS == 0'
ttSS    = 't1_t2_SS == 1'
#ttIso   = 't1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5'
ttIso   = 't1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5'
ttIsoTight   = 't1ByTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByTightIsolationMVArun2v1DBoldDMwLT > 0.5'
ttIsoLoose   = 't1ByIsolationMVArun2v1DBoldDMwLTraw > 0.0 && t2ByIsolationMVArun2v1DBoldDMwLTraw > 0.0'
ttIsoLooseMVA   = 't1ByLooseIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByLooseIsolationMVArun2v1DBoldDMwLT > 0.5'
ttIsoFakeFactor   = 't1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5'
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
eeTrig = '(doubleE_23_12Pass > 0 && LEG1MatchesDoubleE23_12Path > 0 && LEG2MatchesDoubleE23_12Path > 0)'
eePt = '((LEG1Pt > 28 && LEG2Pt > 20) || (LEG2Pt > 28 && LEG1Pt > 20))'
eeEta = 'abs(LEG1Eta) < 2.5 && abs(LEG2Eta) < 2.5'
eeIso = 'e1IsoDB03 < 0.3 && e2IsoDB03 < 0.3'
eeHits = 'e1PassesConversionVeto > 0 && e1MissingHits < 2 && e2PassesConversionVeto > 0 && e2MissingHits < 2'
eeIDL = 'LEG1MVANonTrigWP90 > 0 && LEG2MVANonTrigWP90 > 0'

# MM for Z cand legs
mmTrig = 'doubleMuPass > 0 && LEG1MatchesDoubleMu > 0 && LEG2MatchesDoubleMu > 0'
mmPt = '((LEG1Pt > 20 && LEG2Pt > 10) || (LEG2Pt > 20 && LEG1Pt > 10))'
mmEta = 'abs(LEG1Eta) < 2.4 && abs(LEG2Eta) < 2.4'
mmIso = 'm1IsoDB03 < 0.3 && m2IsoDB03 < 0.3'
mmIDL = 'LEG1IsTracker > 0 && LEG2IsTracker > 0 && LEG1IsGlobal > 0 && LEG2IsGlobal > 0 && LEG1PFIDLoose > 0 && LEG2PFIDLoose > 0'

# ET Higgs
eeetE = 'e3Pt > 15 && abs(e3Eta) < 2.5 && e3IsoDB03 < 0.15 && e3MVANonTrigWP90 > 0'
mmetE = 'ePt > 15 && abs(eEta) < 2.5 && eIsoDB03 < 0.15 && eMVANonTrigWP90 > 0'
xxetT = 'tPt > 20 && abs(tEta) < 2.1 && tByLooseIsolationMVArun2v1DBoldDMwLT > 0 && tDecayModeFinding == 1'
# MT Higgs
eemtM = 'mPt > 10 && abs(mEta) < 2.4 && mIsoDB03 < 0.15 && mIsTracker > 0 && mIsGlobal > 0 && mPFIDLoose > 0'
mmmtM = 'm3Pt > 10 && abs(m3Eta) < 2.4 && m3IsoDB03 < 0.15 && m3IsTracker > 0 && m3IsGlobal > 0 && m3PFIDLoose > 0'
xxmtT = 'tPt > 20 && abs(tEta) < 2.1 && tByLooseIsolationMVArun2v1DBoldDMwLT > 0 && tDecayModeFinding == 1'
# TT Higgs
xxttTT = 't1Pt > 20 && abs(t1Eta) < 2.5 && t2Pt > 20 && abs(t2Eta) < 2.5 && t1ByLooseIsolationMVArun2v1DBoldDMwLT > 0 && t2ByLooseIsolationMVArun2v1DBoldDMwLT > 0 && t1DecayModeFinding == 1 && t2DecayModeFinding == 1'
# EM Higgs
eeemE = 'e3Pt > 15 && abs(e3Eta) < 2.5 && e3IsoDB03 < 0.3 && e3MVANonTrigWP90 > 0'
mmemE = 'ePt > 15 && abs(eEta) < 2.5 && eIsoDB03 < 0.3 && eMVANonTrigWP90 > 0'
eeemM = 'mPt > 10 && abs(mEta) < 2.4 && mIsoDB03 < 0.3 && mIsTracker > 0 && mIsGlobal > 0 && mPFIDLoose > 0'
mmemM = 'm3Pt > 10 && abs(m3Eta) < 2.4 && m3IsoDB03 < 0.3 && m3IsTracker > 0 && m3IsGlobal > 0 && m3PFIDLoose > 0'
# EE & MM Higgs (ZZ control region)
eeee = 'e3Pt > 15 && abs(e3Eta) < 2.5 && e3IsoDB03 < 0.3 && e3MVANonTrigWP90 > 0 && e4Pt > 15 && abs(e4Eta) < 2.5 && e4IsoDB03 < 0.3 && e4MVANonTrigWP90 > 0'
mmmm = 'm3Pt > 10 && abs(m3Eta) < 2.4 && m3IsoDB03 < 0.3 && m3IsTracker > 0 && m3IsGlobal > 0 && m3PFIDLoose> 0 && m4Pt > 10 && abs(m4Eta) < 2.4 && m4IsoDB03 < 0.3 && m4IsTracker > 0 && m4IsGlobal > 0 && m4PFIDLoose > 0'
eemm = 'm1Pt > 10 && abs(m1Eta) < 2.4 && m1IsoDB03 < 0.3 && m1IsTracker > 0 && m1IsGlobal > 0 m1PFIDLoose > 0 && m2Pt > 10 && abs(m2Eta) < 2.4 && m2IsoDB03 < 0.3 && m2IsTracker > 0 && m2IsGlobal > 0 && m2PFIDLoose > 0'

def getCut( analysis, channel, cutName, isData=False ) :
    
    triggers = [tt40, tt35, tt32, eeTrig, mmTrig]

    cutMap = { 
        'htt' : # analysis
        { 'tt' : {
            # A version which applies all cuts at once RunII - NO SIGN SO WE CAN DO QCD
            'signalCutsNoSign' : [ttKin, ttCharge, ttDR, ttVtx, ttIso, ttDisc, extraVetoTT, tt32, DecayMode],
            # A version which applies all cuts at once RunII
            'signalCuts' : [ttKin, ttCharge, ttDR, ttVtx, ttOS, ttIso, ttDisc, extraVetoTT, tt32, DecayMode],
            # Data card sync, no Decay Mode cut 
            'signalCutsNoIsoNoSign' : [ttKin, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt32, DecayMode],
            # Baseline inclusive cuts with Sign applied
            # Not isolation for full QCD estimation
            'fakeFactorCutsTT' : [ttKin, ttCharge, ttDR, ttVtx, ttOS, ttDisc, extraVetoTT, tt32, DecayMode],
            # Selection which only does baseline for sync data cards, NO SIGN for QCD
            'syncCutsDC' : [ttKin, ttCharge, ttDR, ttVtx, ttIso, ttDisc, extraVetoTT, tt32, DecayMode],
            # Selection which only does baseline for sync data cards, NO SIGN for QCD and Loose Iso for TT QCD
            'syncCutsDCqcd' : [ttKin, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt32, DecayMode, ttIsoLooseMVA],
            # Selection which only does baseline for sync data cards, NO SIGN for QCD and Loose Iso for TT QCD
            'syncCutsDCqcdTES' : [ttKinTES, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt32, DecayMode, ttIsoLooseMVA],
            # Selection which only does baseline for sync sample
            'syncCutsNtuple' : [ttKin, ttCharge, ttDR, ttVtx, tt32, DecayMode],
            #'syncCutsNtupleTmp' : [ttKinOld, ttCharge, ttDR, ttVtx, DecayMode],
            'syncCutsNtupleTmp' : [ttKinOld, ttCharge, ttDR, ttVtx, DecayMode],
            'syncCutsNtupleBuilding' : [ttKinOld, ttCharge, ttDR, ttVtx, DecayMode, extraVetoTT, ttDisc, ttIsoTight, tt35],
            'syncCutsNtupleLoose' : [ttKinOld, ttCharge, ttDR, ttVtx, DecayMode, extraVetoTT, ttDisc, ttIsoLooseMVA, tt35],
            # Selection which only does a loose version of the sync Ntuple cuts
            # incase we need to do tau energy scaling later
            'svFitCuts' : [ttKinLoose, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt32, DecayMode, ttIsoLooseMVA],
            # Selection which only does baseline for sync sample
            'crazyCutsNtuple' : [ttKin, ttCharge, ttDR, ttVtx, tt32, DecayMode, 't1Pt>150&&t2Pt>150'],
        }, # end tt channel
        }, # end HTT analysis cuts
        'azh' : # analysis
        { 'eeee' : {
            'goodZ' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eeee],
            'HSS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eeee],
        }, # end EEEE
         'eeet' : {
            'goodZ' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eeetE, xxetT],
            'HSS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eeetE, xxetT],
        }, # end EEET
         'eett' : {
            'goodZ' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, xxttTT],
            'HSS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, xxttTT],
        }, # end EETT
         'eemt' : {
            'goodZ' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eemtM, xxmtT],
            'HSS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eemtM, xxmtT],
        }, # end EEMT
         'eeem' : {
            'goodZ' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eeemE, eeemM],
            'HSS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eeemE, eeemM],
        }, # end EEEM
         'eemm' : {
            'goodZ' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HOS, HDXYZ, eemm],
            'HSS' : [ZOS, ZMass, eeTrig, eeHits, eeIso, eeIDL, eePt, eeEta, ZDXYZ, HSS, HDXYZ, eemm],
        }, # end EEMM
         'mmmm' : {
            'goodZ' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, mmmm],
            'HSS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmmm],
        }, # end MMMM
         'emmt' : {
            'goodZ' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, mmetE, xxetT],
            'HSS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmetE, xxetT],
        }, # end MMET
         'mmtt' : {
            'goodZ' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, xxttTT],
            'HSS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, xxttTT],
        }, # end MMTT
         'mmmt' : {
            'goodZ' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, mmmtM, xxmtT],
            'HSS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmmtM, xxmtT],
        }, # end MMMT
         'emmm' : {
            'goodZ' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HOS, HDXYZ, mmemE, mmemM],
            'HSS' : [ZOS, ZMass, mmTrig, mmIso, mmIDL, mmPt, mmEta, ZDXYZ, HSS, HDXYZ, mmemE, mmemM],
        } # end MMEM
        } # end AZH analysis cuts
    } # end cutMap
    
    # Add a copy of the 'htt' analysis cuts under 'Sync'
    cutMap[ 'Sync' ] = cutMap[ 'htt' ]

    cuts1 = cutMap[ analysis ][ channel ][ cutName ]

    # Remove trigger requirements if MC
    if not isData :
        for trig in triggers :
            if trig in cuts1 :
                cuts1.remove( trig )

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
    cut = getCut( 'htt', 'tt', 'syncCutsDCqcd', False )
    print cut + "\n\n"
    cut = getCut( 'htt', 'tt', 'syncCutsDCqcd', True )
    print cut + "\n\n"
    cut = getCut( 'azh', 'eeet', 'goodZ' )
    print cut + "\n\n"



