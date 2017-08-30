import ROOT
import copy

def makeGenCut( inTree, cutString ) :
	#print "l1 %s, l2 %s" % (l1, l2)
	outTree = inTree.CopyTree( cutString )
	return outTree


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
tt35_all    = '((doubleTau35Pass > 0 && t1MatchesDoubleTau35Path > 0 && t2MatchesDoubleTau35Path > 0 && t1MatchesDoubleTau35Filter > 0 && t2MatchesDoubleTau35Filter > 0) || (doubleTauCmbIso35RegPass > 0 && t1MatchesDoubleTauCmbIso35RegPath > 0 && t2MatchesDoubleTauCmbIso35RegPath > 0 && t1MatchesDoubleTauCmbIso35RegFilter > 0 && t2MatchesDoubleTauCmbIso35RegFilter > 0))'
tt35mc    = '(doubleTau35Pass > 0 && t1MatchesDoubleTau35Path > 0 && t2MatchesDoubleTau35Path > 0 && t1MatchesDoubleTau35Filter > 0 && t2MatchesDoubleTau35Filter > 0)'
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
ttIsoVLooseMVA_all   = '((t1ByVLooseIsolationMVArun2v1DBoldDMwLT > 0.5 || t1RerunMVArun2v1DBoldDMwLTVLoose > 0.5) && (t2ByVLooseIsolationMVArun2v1DBoldDMwLT > 0.5 || t2RerunMVArun2v1DBoldDMwLTVLoose > 0.5))'
ttIsoVVLooseMVA   = 't1ByIsolationMVArun2v1DBoldDMwLTraw > 0. && t2ByIsolationMVArun2v1DBoldDMwLTraw > 0.' # This corresponds to the loosest mva cut at high pt for VVLoose. The actual VVLoose variable is added after our initial cuts in step 2
ttDisc  = 't1AgainstElectronVLooseMVA6 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA6 > 0.5 && t2AgainstMuonLoose3 > 0.5'
# TT Studies
ttIsoInvert = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits > 3.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits > 3.0'
ttQCDPreIso = 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0 && t2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 5.0'

###########################
### AZh and ZH Baseline ###
###########################
ZMass = 'LEG1_LEG2_Mass > 60 && LEG1_LEG2_Mass < 120'
ZOS = 'LEG1_LEG2_SS == 0'
HOS = 'LEG3_LEG4_SS == 0'
HSS = 'LEG3_LEG4_SS == 1'

eeTrig = 'doubleE_23_12Pass > 0'
mmTrig = 'doubleMuPass > 0'

eeetVetos = 'eVetoAZHdR0 <= 3 && muVetoAZHdR0 == 0'
mmetVetos = 'eVetoAZHdR0 <= 1 && muVetoAZHdR0 <= 2'
eemtVetos = 'eVetoAZHdR0 <= 2 && muVetoAZHdR0 <= 1'
mmmtVetos = 'eVetoAZHdR0 == 0 && muVetoAZHdR0 <= 3'
eettVetos = 'eVetoAZHdR0 <= 2 && muVetoAZHdR0 == 0'
mmttVetos = 'eVetoAZHdR0 == 0 && muVetoAZHdR0 <= 2'
eeemVetos = 'eVetoAZHdR0 <= 3 && muVetoAZHdR0 <= 1'
mmemVetos = 'eVetoAZHdR0 <= 1 && muVetoAZHdR0 <= 3'
eeeeVetos = 'eVetoAZHdR0 <= 4 && muVetoAZHdR0 == 0'
mmmmVetos = 'eVetoAZHdR0 == 0 && muVetoAZHdR0 <= 4'
eemmVetos = 'eVetoAZHdR0 <= 2 && muVetoAZHdR0 <= 2'

#eeetVetos = 'eVetoZTTp001dxyzR0 <= 3 && muVetoZTTp001dxyzR0 == 0'
#mmetVetos = 'eVetoZTTp001dxyzR0 <= 1 && muVetoZTTp001dxyzR0 <= 2'
#eemtVetos = 'eVetoZTTp001dxyzR0 <= 2 && muVetoZTTp001dxyzR0 <= 1'
#mmmtVetos = 'eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 <= 3'
#eettVetos = 'eVetoZTTp001dxyzR0 <= 2 && muVetoZTTp001dxyzR0 == 0'
#mmttVetos = 'eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 <= 2'
#eeemVetos = 'eVetoZTTp001dxyzR0 <= 3 && muVetoZTTp001dxyzR0 <= 1'
#mmemVetos = 'eVetoZTTp001dxyzR0 <= 1 && muVetoZTTp001dxyzR0 <= 3'
#eeeeVetos = 'eVetoZTTp001dxyzR0 <= 4 && muVetoZTTp001dxyzR0 == 0'
#mmmmVetos = 'eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 <= 4'
#eemmVetos = 'eVetoZTTp001dxyzR0 <= 2 && muVetoZTTp001dxyzR0 <= 2'

# Basic lepton definitions for ZH analysis
def eBase( lep ) :
    return 'LEG_Pt > 10 && abs(LEG_Eta) < 2.5 && LEG_PassesConversionVeto > 0.5 && LEG_MissingHits < 2 && abs(LEG_PVDXY) < 0.045 && abs(LEG_PVDZ) < 0.2'.replace('LEG_',lep)
def eTight( lep ) :
    return 'LEG_Pt > 10 && abs(LEG_Eta) < 2.5 && LEG_PassesConversionVeto > 0.5 && LEG_MissingHits < 2 && abs(LEG_PVDXY) < 0.045 && abs(LEG_PVDZ) < 0.2 && LEG_MVANonTrigWP90 > 0.5'.replace('LEG_',lep)
def eTightWithIso( lep ) :
    return 'LEG_Pt > 10 && abs(LEG_Eta) < 2.5 && LEG_PassesConversionVeto > 0.5 && LEG_MissingHits < 2 && abs(LEG_PVDXY) < 0.045 && abs(LEG_PVDZ) < 0.2 && LEG_IsoDB03 < 0.3 && LEG_MVANonTrigWP90 > 0.5'.replace('LEG_',lep)

def mBase( lep ) :
    return 'LEG_Pt > 10 && abs(LEG_Eta) < 2.4 && abs(LEG_PVDXY) < 0.045 && abs(LEG_PVDZ) < 0.2'.replace('LEG_',lep)
def mTight( lep ) :
    return 'LEG_Pt > 10 && abs(LEG_Eta) < 2.4 && abs(LEG_PVDXY) < 0.045 && abs(LEG_PVDZ) < 0.2 && LEG_IsoDB04 < 0.25 && LEG_PFIDLoose > 0.5'.replace('LEG_',lep)

def tBase( lep ) :
    return 'LEG_Pt > 20 && abs(LEG_Eta) < 2.3 && LEG_DecayModeFinding == 1 && abs(LEG_PVDZ) < 0.2 && LEG_AgainstElectronVLooseMVA6 == 1 && LEG_AgainstMuonLoose3 == 1 && abs( LEG_Charge ) == 1'.replace('LEG_',lep)
def tTight( lep ) :
    return 'LEG_Pt > 20 && abs(LEG_Eta) < 2.3 && LEG_DecayModeFinding == 1 && abs(LEG_PVDZ) < 0.2 && LEG_AgainstElectronVLooseMVA6 == 1 && LEG_AgainstMuonLoose3 == 1 && abs( LEG_Charge ) == 1 && LEG_ByMediumIsolationMVArun2v1DBoldDMwLT > 0.5'.replace('LEG_',lep)
def tAntiEV ( lep ) :
    return 'LEG_AgainstElectronTightMVA6 == 1'.replace('LEG_',lep)
def tAntiMV ( lep ) :
    return 'LEG_AgainstMuonTight3 == 1'.replace('LEG_',lep)

def eeTrigPt(lep1='e1', lep2='e2') :
    #return '(((LEG1_Pt > 24 && LEG2_Pt > 13) || (LEG2_Pt > 24 && LEG1_Pt > 13)) && LEG1_MatchesDoubleE23_12Path > 0 && LEG2_MatchesDoubleE23_12Path > 0)'.replace('LEG1_',lep1).replace('LEG2_',lep2)
    return '(((LEG1_Pt > 24 && LEG2_Pt > 13) || (LEG2_Pt > 24 && LEG1_Pt > 13)) && LEG1_MatchesDoubleE23_12Path > 0 && LEG1_MatchesDoubleE23_12Filter > 0 && LEG2_MatchesDoubleE23_12Path > 0 && LEG2_MatchesDoubleE23_12Filter > 0)'.replace('LEG1_',lep1).replace('LEG2_',lep2)
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
    #return '((LEG1_Pt > 18 || LEG2_Pt > 18) && LEG1_MatchesDoubleMu > 0 && LEG2_MatchesDoubleMu > 0)'.replace('LEG1_',lep1).replace('LEG2_',lep2)
    return '((LEG1_Pt > 18 || LEG2_Pt > 18) && LEG1_MatchesDoubleMu > 0 && (LEG1_MatchesDoubleMuFilter1 > 0 || LEG1_MatchesDoubleMuFilter2 > 0) && LEG2_MatchesDoubleMu > 0 && (LEG2_MatchesDoubleMuFilter1 > 0 || LEG2_MatchesDoubleMuFilter2 > 0))'.replace('LEG1_',lep1).replace('LEG2_',lep2)
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

# Have default cut for all objects at dR > 0.3 in FSA
def llltDR( l1,l2,l3,l4 ) :
    dr = 'LEG1_LEG4_DR > 0.5 && LEG2_LEG4_DR > 0.5 && LEG3_LEG4_DR > 0.5'
    return dr.replace('LEG1',l1).replace('LEG2',l2).replace('LEG3',l3).replace('LEG4',l4)

def llttDR( l1,l2,l3,l4 ) :
    dr = 'LEG1_LEG3_DR > 0.5 && LEG1_LEG4_DR > 0.5 && LEG2_LEG3_DR > 0.5 && LEG2_LEG4_DR > 0.5 && LEG3_LEG4_DR > 0.5'
    return dr.replace('LEG1',l1).replace('LEG2',l2).replace('LEG3',l3).replace('LEG4',l4)


def getCut( analysis, channel, cutName, isData=False, hdfsSkim=False ) :
    
    triggers = [tt40, tt35,]

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
            'syncCutsDCqcdTES5040VL_HdfsSkim' : [ttKin5040TES, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35_all, DecayMode, ttIsoVLooseMVA_all],
            'syncCutsDCqcdTESNoIso' : [ttKin40TES, ttCharge, ttDR, ttVtx, ttDisc, extraVetoTT, tt35, DecayMode],
            # Selection which only does baseline for sync sample
            'syncCutsMSSMNtuple' : [ttKin40, ttCharge, ttDR, ttVtx, tt35, DecayMode],
            'syncCutsSMHTTNtuple' : [ttKin40, ttCharge, ttDR, ttVtx, tt35, DecayMode],
          }, # end tt channel
        }, # end HTT analysis cuts
        'azh' : # analysis
        { 'eeee' : {
            'Skim'   : [ZOS, ZMass, eeTrig, eeeeTrigPt(), eeeeVetos, eTight('e1'), eTight('e2'), eBase('e3'), eBase('e4')],
        }, # end EEEE
         'eeet' : {
            'Skim'   : [ZOS, ZMass, eeTrig, eeeTrigPt(), llltDR('e1','e2','e3','t'), eeetVetos, eTight('e1'), eTight('e2'), eBase('e3'), tBase('t'), tAntiEV('t')],
            'SkimAZH'   : [ZOS, ZMass, eeTrig, eeeTrigPt(), llltDR('e1','e2','e3','t'), eeetVetos, eTightWithIso('e1'), eTightWithIso('e2'), eBase('e3'), tBase('t'), tAntiEV('t')],
            'SkimNoTrig'   : [ZOS, ZMass, llltDR('e1','e2','e3','t'), eeetVetos, eTight('e1'), eTight('e2'), eBase('e3'), tBase('t'), tAntiEV('t')],
        }, # end EEET
         'eett' : {
            'Skim'   : [ZOS, ZMass, eeTrig, eeTrigPt(), llttDR('e1','e2','t1','t2'), eettVetos, eTight('e1'), eTight('e2'), tBase('t1'), tBase('t2')],
            'SkimAZH'   : [ZOS, ZMass, eeTrig, eeTrigPt(), llttDR('e1','e2','t1','t2'), eettVetos, eTightWithIso('e1'), eTightWithIso('e2'), tBase('t1'), tBase('t2')],
            'SkimNoTrig'   : [ZOS, ZMass, llttDR('e1','e2','t1','t2'), eettVetos, eTight('e1'), eTight('e2'), tBase('t1'), tBase('t2')],
        }, # end EETT
         'eemt' : {
            'Skim'   : [ZOS, ZMass, eeTrig, eeTrigPt(), llltDR('e1','e2','m','t'), eemtVetos, eTight('e1'), eTight('e2'), mBase('m'), tBase('t'), tAntiMV('t')],
            'SkimAZH'   : [ZOS, ZMass, eeTrig, eeTrigPt(), llltDR('e1','e2','m','t'), eemtVetos, eTightWithIso('e1'), eTightWithIso('e2'), mBase('m'), tBase('t'), tAntiMV('t')],
            'SkimNoTrig'   : [ZOS, ZMass, llltDR('e1','e2','m','t'), eemtVetos, eTight('e1'), eTight('e2'), mBase('m'), tBase('t'), tAntiMV('t')],
        }, # end EEMT
         'eeem' : {
            'Skim'   : [ZOS, ZMass, eeTrig, eeeTrigPt(), eeemVetos, eTight('e1'), eTight('e2'), eBase('e3'), mBase('m')],
            'SkimAZH'   : [ZOS, ZMass, eeTrig, eeeTrigPt(), eeemVetos, eTightWithIso('e1'), eTightWithIso('e2'), eBase('e3'), mBase('m')],
            'SkimNoTrig'   : [ZOS, ZMass, eeemVetos, eTight('e1'), eTight('e2'), eBase('e3'), mBase('m')],
        }, # end EEEM
         'eemm' : {
            'Skim'   : [ZOS, ZMass, eeTrig, eeTrigPt(), eemmVetos, eTight('e1'), eTight('e2'), mBase('m1'), mBase('m2')],
        }, # end EEMM
         'mmmm' : {
            'Skim'   : [ZOS, ZMass, mmTrig, mmmmTrigPt(), mmmmVetos, mTight('m1'), mTight('m2'), mBase('m3'), mBase('m4')],
        }, # end MMMM
         'emmt' : {
            'Skim'   : [ZOS, ZMass, mmTrig, mmTrigPt(), llltDR('m1','m2','e','t'), mmetVetos, mTight('m1'), mTight('m2'), eBase('e'), tBase('t'), tAntiEV('t')],
            'SkimNoTrig'   : [ZOS, ZMass, llltDR('m1','m2','e','t'), mmetVetos, mTight('m1'), mTight('m2'), eBase('e'), tBase('t'), tAntiEV('t')],
        }, # end MMET
         'mmtt' : {
            'Skim'   : [ZOS, ZMass, mmTrig, mmTrigPt(), llttDR('m1','m2','t1','t2'), mmttVetos, mTight('m1'), mTight('m2'), tBase('t1'), tBase('t2')],
            'SkimNoTrig'   : [ZOS, ZMass, llttDR('m1','m2','t1','t2'), mmttVetos, mTight('m1'), mTight('m2'), tBase('t1'), tBase('t2')],
        }, # end MMTT
         'mmmt' : {
            'Skim'   : [ZOS, ZMass, mmTrig, mmmTrigPt(), llltDR('m1','m2','m3','t'), mmmtVetos, mTight('m1'), mTight('m2'), mBase('m3'), tBase('t'), tAntiMV('t')],
            'SkimNoTrig'   : [ZOS, ZMass, llltDR('m1','m2','m3','t'), mmmtVetos, mTight('m1'), mTight('m2'), mBase('m3'), tBase('t'), tAntiMV('t')],
        }, # end MMMT
         'emmm' : {
            'Skim'   : [ZOS, ZMass, mmTrig, mmmTrigPt(), mmemVetos, mTight('m1'), mTight('m2'), mBase('m3'), eBase('e')],
            'SkimNoTrig'   : [ZOS, ZMass, mmemVetos, mTight('m1'), mTight('m2'), mBase('m3'), eBase('e')],
        } # end MMEM
        } # end AZH analysis cuts
    } # end cutMap

    # Add repetitive basic cuts to ZH/AZh cuts
    if analysis == 'azh' :
        chans = ['eeem', 'eeet', 'eemt', 'eett', 'emmm', 'emmt', 'mmmt', 'mmtt', 'eeee', 'eemm', 'mmmm']
        for chan in chans :
            l = copy.deepcopy(cutMap['azh'][chan]['Skim'])
            l.append( HSS )
            cutMap['azh'][chan]['RedBkg'] = l
            l = copy.deepcopy(cutMap['azh'][chan]['Skim'])
            l.append( HOS )
            cutMap['azh'][chan]['SignalRegion'] = l
            # Keep non-isolated electron passing ID using normal Skim
            if 'SkimAZH' not in cutMap['azh'][chan] :
                cutMap['azh'][chan]['SkimAZH'] = copy.deepcopy(cutMap['azh'][chan]['Skim'])
    
    
    # Add a copy of the 'htt' analysis cuts under 'Sync'
    cutMap[ 'Sync' ] = cutMap[ 'htt' ]

    cuts1 = cutMap[ analysis ][ channel ][ cutName ]

    # Remove trigger requirements if MC except reHLT samples
    #if not isData :
    #    #if not isReHLT : 
    #    for trig in triggers :
    #        if hdfsSkim : continue # We want to keep all versions of double Tau 35 trigger for svFitting
    #        if trig in cuts1 :
    #            cuts1.remove( trig )
    #            if analysis == 'htt' :
    #                cuts1.append( tt35mc )

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



