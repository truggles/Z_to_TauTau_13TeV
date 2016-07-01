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

# EE for Z cand legs
eeTrig = '(doubleEPass > 0 && LEG1MatchesDoubleE > 0 && LEG2MAtchesDoubleE > 0)'
eePt = '(LEG1Pt > 20 && LEG2Pt > 15 && LEG1Pt > LEG2Pt) || (LEG2Pt > 20 && LEG1Pt > 15 && LEG2Pt > LEG1Pt)'
eeEta = 'abs(LEG1Eta) < 2.5 && abs(LEG2Eta) < 2.5'

# MM for Z cand legs
mmTrig = 'doubleMuPass > 0 && LEG1MatchesDoubleMu > 0 && LEG2MatchesDoubleMu > 0'
mmPt = '(LEG1Pt > 20 && LEG2Pt > 10 && LEG1Pt > LEG2Pt) || (LEG2Pt > 20 && LEG1Pt > 10 && LEG2Pt > LEG1Pt)'
mmEta = 'abs(LEG1Eta) < 2.4 && abs(LEG2Eta) < 2.4'

def getCut( analysis, channel, cutName, isData=False ) :
    
    triggers = [tt40, tt35, tt32]

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
        { 'eeet' : {
            'goodZ' : [ZMass, eeTrig, eePt, eeEta]
        } # end EEET
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

    cutString = ''
    for item in cuts1 :
        tmp = item.replace( 'LEG1', 'e1').replace( 'LEG2', 'e2' )
        if cutString != '' :
            cutString += ' && '
        cutString += tmp
    cutString = '('+cutString+')'
    return cutString



if __name__ == '__main__' :
    cut = getCut( 'htt', 'tt', 'syncCutsDCqcd', False )
    print cut + "\n\n"
    cut = getCut( 'htt', 'tt', 'syncCutsDCqcd', True )
    print cut + "\n\n"
    cut = getCut( 'azh', 'eeet', 'goodZ' )
    print cut + "\n\n"



