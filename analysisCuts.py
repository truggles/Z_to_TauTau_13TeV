import ROOT

def makeGenCut( inTree, cutString ) :
	#print "l1 %s, l2 %s" % (l1, l2)
	outTree = inTree.CopyTree( cutString )
	return outTree


# TT Baseline
extraVetoTT   = 'eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 == 0'
#DecayMode = '(t1DecayMode != 5 && t1DecayMode != 6) && (t2DecayMode != 5 && t2DecayMode != 6)'
DecayMode = 't1DecayModeFinding == 1 && t2DecayModeFinding == 1'
ttKin   = 't1Pt > 40 && t1AbsEta < 2.1 && t2Pt > 40 && t2AbsEta < 2.1'
ttKinTES   = '(t1Pt*1.03) > 40 && t1AbsEta < 2.1 && (t2Pt*1.03) > 40 && t2AbsEta < 2.1'
ttKinLoose   = 't1Pt > 35 && t1AbsEta < 2.1 && t2Pt > 35 && t2AbsEta < 2.1'
#ttKin   = 't1Pt > 45 && t1AbsEta < 2.1 && t2Pt > 45 && t2AbsEta < 2.1'
ttCharge    = 'abs( t1Charge ) == 1 && abs( t2Charge ) == 1'
ttDR    = 't1_t2_DR > 0.5'
ttVtx   = 'abs( t1PVDZ ) < 0.2 && abs( t2PVDZ ) < 0.2'
tt40    = 'doubleTau40Pass == 1 && t1MatchesDoubleTau40Path == 1 && t2MatchesDoubleTau40Path == 1 && t1DoubleTau40Filter > 0 && t2DoubleTau40Filter > 0'
#XXX tt35    = 'doubleTau35Pass > 0 && t1MatchesDoubleTau35Path > 0 && t2MatchesDoubleTau35Path > 0 && t1DoubleTau35Filter > 0 && t2DoubleTau35Filter > 0'
tt35    = '(1)'
# TT PostSync
#XXX ttL1IsoTaus = 't1L1IsoTauMatch > 0 && t2L1IsoTauMatch > 0 && doubleL1IsoTauMatch > 0'
ttL1IsoTaus = '(1)'
#ttL1IsoTaus = 't1L1IsoTauMatch > 0 && t2L1IsoTauMatch > 0'
ttOS    = 't1_t2_SS == 0'
ttSS    = 't1_t2_SS == 1'
#ttIso   = 't1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5'
ttIso   = 't1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5'
ttIsoLoose   = 't1ByIsolationMVArun2v1DBoldDMwLTraw > 0.0 && t2ByIsolationMVArun2v1DBoldDMwLTraw > 0.0'
ttIsoLooseMVA   = 't1ByLooseIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByLooseIsolationMVArun2v1DBoldDMwLT > 0.5'
ttIsoFakeFactor   = 't1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5'
ttDisc  = 't1AgainstElectronVLooseMVA6 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA6 > 0.5 && t2AgainstMuonLoose3 > 0.5'
# TT Studies
ttIsoInvert = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits > 3.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits > 3.0'
ttQCDPreIso = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0'

# AtoZh
# eeet
ZMass = 'LEG1_LEG2_Mass > 60 && LEG1_LEG2_Mass < 120'

def getCut( analysis, channel, cutName ) :

    cutMap = { 
        'htt' : # analysis
        { 'tt' : {
            # A version which applies all cuts at once RunII - NO SIGN SO WE CAN DO QCD
            'signalExtractionNoSign' : [ttKin, ttCharge, ttDR, ttVtx, ttIso, ttDisc, extraVetoTT, tt35, DecayMode, ttL1IsoTaus, 't1_t2_Pt > 100'],
            # A version which applies all cuts at once RunII - NO SIGN SO WE CAN DO QCD
            'signalCutsNoSign' : [ttKin, ttCharge, ttDR, ttVtx, ttIso, ttDisc, extraVetoTT, tt35, DecayMode, ttL1IsoTaus],
            # A version which applies all cuts at once RunII
            'signalCuts' : [ttKin, ttCharge, ttDR, ttVtx, ttOS, ttIso, ttDisc, extraVetoTT, tt35, DecayMode, ttL1IsoTaus],
            # Data card sync, no Decay Mode cut 
            'signalCutsNoIsoNoSign' : [ttKin, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode, ttL1IsoTaus],
            # Baseline inclusive cuts with Sign applied
            # Not isolation for full QCD estimation
            'fakeFactorCutsTT' : [ttKin, ttCharge, ttDR, ttVtx, ttOS, ttDisc, extraVetoTT, tt35, DecayMode, ttL1IsoTaus],
            # Selection which only does baseline for sync data cards, NO SIGN for QCD
            'syncCutsDC' : [ttKin, ttCharge, ttDR, ttVtx, ttIso, ttDisc, extraVetoTT, tt35, DecayMode, ttL1IsoTaus],
            # Selection which only does baseline for sync data cards, NO SIGN for QCD and Loose Iso for TT QCD
            'syncCutsDCqcd' : [ttKin, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode, ttL1IsoTaus, ttIsoLooseMVA],
            # Selection which only does baseline for sync data cards, NO SIGN for QCD and Loose Iso for TT QCD
            'syncCutsDCqcdTES' : [ttKinTES, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode, ttL1IsoTaus, ttIsoLooseMVA],
            # Selection which only does baseline for sync sample
            'syncCutsNtuple' : [ttKin, ttCharge, ttDR, ttVtx, tt35, DecayMode, ttL1IsoTaus],
            # Selection which only does a loose version of the sync Ntuple cuts
            # incase we need to do tau energy scaling later
            'svFitCuts' : [ttKinLoose, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode, ttL1IsoTaus, ttIsoLooseMVA],
            # Selection which only does baseline for sync sample
            'crazyCutsNtuple' : [ttKin, ttCharge, ttDR, ttVtx, tt35, DecayMode, ttL1IsoTaus, 't1Pt>150&&t2Pt>150'],
        }, # end tt channel
        }, # end HTT analysis cuts
        'azh' : # analysis
        { 'eeet' : {
            'goodZ' : [ZMass]
        } # end EEET
        } # end AZH analysis cuts
    } # end cutMap
    
    # Add a copy of the 'htt' analysis cuts under 'Sync'
    cutMap[ 'Sync' ] = cutMap[ 'htt' ]

    cuts1 = cutMap[ analysis ][ channel ][ cutName ]
    cutString = ''
    for item in cuts1 :
        tmp = item.replace( 'LEG1', 'e1').replace( 'LEG2', 'e2' )
        if cutString != '' :
            cutString += ' && '
        cutString += tmp
    cutString = '('+cutString+')'
    return cutString



if __name__ == '__main__' :
    cut = getCut( 'htt', 'tt', 'syncCutsDCqcdTES' )
    print cut
    cut = getCut( 'azh', 'eeet', 'goodZ' )
    print cut



