#############################################################################
#                                                                           #
# renameBranches.py                                                         #
#                                                                           #
# takes a tree in a file, creates a new file with a new tree that is an     #
# exact copy, but with selected branches renamed.                           #
#                                                                           #
# Nate Woods, U. Wisconsin, mods Tyler Ruggles                              #
#                                                                           #
#############################################################################

import math
import json
import os
import ROOT
import copy
from util.helpers import getProdMap

cmsLumi = float(os.getenv('LUMI'))
print "Lumi = %i" % cmsLumi

prodMap = getProdMap()

#XXX XXX XXX FIXME so that this does N Jet binned correct once we have ReHLT
def getXSec( analysis, shortName, sampDict, numGenJets=0 ) :
    #print "Short Name: ",shortName," mini Name: ",shortName[:6]#shortName[:-7]
    assert( shortName in sampDict.keys() ), "Sample %s not in your meta samples.json" % shortName
    if shortName in ['DYJetsAMCNLO', 'DYJetsAMCNLOReHLT', 'DYJetsOld', 'DYJetsLow'] : # or shortName == 'DYJets' : # Uncomment last part to study relations between all 4
        return cmsLumi * sampDict[ shortName ]['Cross Section (pb)'] / ( sampDict[ shortName ]['summedWeightsNorm'] )
    if 'data' in shortName : return 1.0 #XXX#
    jetBins = ['1', '2', '3', '4']
    try :
        if 'DYJets' == shortName or shortName[:6] == 'DYJets' :
        #if 'DYJets' in shortName :
            scalar1 = cmsLumi * sampDict[ 'DYJets' ]['Cross Section (pb)'] / sampDict[ 'DYJets' ]['summedWeightsNorm'] # removing LO small DYJets
            #return scalar1 # FIXME
            #print "DYJets in shortName, scalar1 =",scalar1
        elif 'WJets' in shortName :
            scalar1 = cmsLumi * ( sampDict[ 'WJets' ]['Cross Section (pb)'] / sampDict[ 'WJets' ]['summedWeightsNorm'] )
        else :
            scalar1 = cmsLumi * sampDict[ shortName ]['Cross Section (pb)'] / ( sampDict[ shortName ]['summedWeightsNorm'] )
            #print "DYJets not in shortName, scalar1 =",scalar1

    except KeyError :
        print "Sample not found in meta/Ntuples_xxx/samples.json"
        return
    #return scalar1 #XXX#
    
    """
    Using jet binned samples
    """
    # If inclusive sample
    if shortName in ['DYJets', 'WJets'] :
        binPartner = ''
        if numGenJets == 0 :
            return scalar1
        elif numGenJets == 1 :
            binPartner = '1'
        elif numGenJets == 2 :
            binPartner = '2'
        elif numGenJets == 3 :
            binPartner = '3'
        elif numGenJets == 4 :
            binPartner = '4'
        else :
            return scalar1

        scalar2 = cmsLumi * sampDict[ shortName+binPartner ]['Cross Section (pb)'] / ( sampDict[ shortName+binPartner ]['summedWeightsNorm'] )
        return (1.0/( (1./scalar1) + (1./scalar2) ))

    # If exclusive sample
    if (('DYJets' in shortName) or ('WJets' in shortName)) and shortName[-1:] in jetBins :
        scalar2 = cmsLumi * sampDict[ shortName ]['Cross Section (pb)'] / ( sampDict[ shortName ]['summedWeightsNorm'] )
        #print "Scalar2 ",scalar2
        return (1.0/( (1./scalar1) + (1./scalar2) ))
        
        
    if 'QCD' in shortName or 'toTauTau' in shortName : return scalar1
    if 'data' in shortName : return 1.0
    return scalar1


# Apply Tau Energy Scale corrections to a corrected PT variable
def correctTauPt( pt, gen_match, decayMode ) :
    # only correct good decay modes
    if decayMode not in [0, 1, 10] : return pt
    # only correct real taus
    if gen_match != 5 : return pt

    # Values from my reposting for Alex Nehrkorn's slides
    # https://indico.cern.ch/event/607882/contributions/2450164/attachments/1412727/2161541/nehrkorn_tau_es_summer16.pdf
    if decayMode == 0  : return pt * 0.982
    if decayMode == 1  : return pt * 1.010
    if decayMode == 10 : return pt * 1.004    



# make a var which fills with the tighest iso WP passed
def setIsoCode( row, lep, VVTight, VVLoose ) :
    # None = 0, VVL = 1, VL = 2, L = 3, M = 4, T = 5, VT = 6, VVT = 7
    if not VVLoose : return 0
    if not getattr( row, lep+'ByVLooseIsolationMVArun2v1DBoldDMwLT' ) : return 1
    if not getattr( row, lep+'ByLooseIsolationMVArun2v1DBoldDMwLT' ) : return 2
    if not getattr( row, lep+'ByMediumIsolationMVArun2v1DBoldDMwLT' ) : return 3
    if not getattr( row, lep+'ByTightIsolationMVArun2v1DBoldDMwLT' ) : return 4
    if not getattr( row, lep+'ByVTightIsolationMVArun2v1DBoldDMwLT' ) : return 5
    if not VVTight : return 6
    if VVTight : return 7
    else : return -1


def getTauPtWeight( sample, channel, t1GenID, t2GenID, row, ptScaler ) :
    if channel != 'tt' : return 1
    if not ('ggH' in sample or 'bbH' in sample or 'DYJets' in sample or 'VBF' in sample or 'Sync' in sample) :
        return 1
    l1weight = 0. 
    l2weight = 0.
    if t1GenID == 5 and row.t1GenJetPt >= 0 :
        l1weight = row.t1GenJetPt * ptScaler / 1000.
    if t2GenID == 5 and row.t2GenJetPt >= 0 :
        l2weight = row.t2GenJetPt * ptScaler / 1000.
    return 1 + l1weight + l2weight



def getHiggsPt( pt1, eta1, phi1, m1, pt2, eta2, phi2, m2, met, metphi) :
    lorentz1 = ROOT.TLorentzVector( 0.,0.,0.,0. )
    lorentz1.SetPtEtaPhiM( pt1, eta1, phi1, m1 )
    lorentz2 = ROOT.TLorentzVector( 0.,0.,0.,0. )
    lorentz2.SetPtEtaPhiM( pt2, eta2, phi2, m2 )
    lorentz3 = ROOT.TLorentzVector( 0.,0.,0.,0. )
    lorentz3.SetPtEtaPhiM( met, 0., metphi, 0. )
    higgs = lorentz1 + lorentz2 + lorentz3
    return higgs.Pt()
    


def mVisTES( cand1, cand2, row, TES ) :
    pt1 = (1 + TES) * getattr( row, cand1+'Pt' )
    eta1 = getattr( row, cand1+'Eta' )
    phi1 = getattr( row, cand1+'Phi' )
    m1 = getattr( row, cand1+'Mass' )
    pt2 = (1 + TES) * getattr( row, cand2+'Pt' )
    eta2 = getattr( row, cand2+'Eta' )
    phi2 = getattr( row, cand2+'Phi' )
    m2 = getattr( row, cand2+'Mass' )
    lorentz1 = ROOT.TLorentzVector( 0.,0.,0.,0. )
    lorentz1.SetPtEtaPhiM( pt1, eta1, phi1, m1 )
    lorentz2 = ROOT.TLorentzVector( 0.,0.,0.,0. )
    lorentz2.SetPtEtaPhiM( pt2, eta2, phi2, m2 )
    shifted = lorentz1 + lorentz2
    return shifted.M()


def mVisTESCor( cand1, cand2, row, pt1, pt2 ) :
    eta1 = getattr( row, cand1+'Eta' )
    phi1 = getattr( row, cand1+'Phi' )
    m1 = getattr( row, cand1+'Mass' )
    eta2 = getattr( row, cand2+'Eta' )
    phi2 = getattr( row, cand2+'Phi' )
    m2 = getattr( row, cand2+'Mass' )
    lorentz1 = ROOT.TLorentzVector( 0.,0.,0.,0. )
    lorentz1.SetPtEtaPhiM( pt1, eta1, phi1, m1 )
    lorentz2 = ROOT.TLorentzVector( 0.,0.,0.,0. )
    lorentz2.SetPtEtaPhiM( pt2, eta2, phi2, m2 )
    corrected = lorentz1 + lorentz2
    return corrected.M()


#def getMTTotal( pt1, phi1, pt2, phi2, row, channel, esUP=True ) :
#    if channel == 'tt' :
#        es = 0.03
#    elif channel == 'em' :
#        if abs( row.eEta ) < 1.479 : # BarrelEndcap transition at eta = 1.479
#            es = 0.01
#        else :
#            es = 0.025
#    else : es = 0.0
#
#    shift = 1.
#    if esUP : shift += es
#    else : shift -= es
#
#    # Get ES corrected mva met
#    dx1_UP = pt1 * math.cos( phi1 ) * (( 1. / (shift) ) - 1.)
#    dy1_UP = pt1 * math.sin( phi1 ) * (( 1. / (shift) ) - 1.)
#    if hasattr( row, "mvametcorr_ex" ) :
#        mvametcorr_ex_UP = row.mvametcorr_ex + dx1_UP
#        mvametcorr_ey_UP = row.mvametcorr_ey + dy1_UP
#    else : return -10
#    mvametcorr = math.sqrt( mvametcorr_ex_UP**2 + mvametcorr_ey_UP**2 )
#    mvametcorrphi = ROOT.TMath.ATan2( mvametcorr_ey_UP, mvametcorr_ex_UP )
#
#    mt_1_UP = getTransMass( mvametcorr, mvametcorrphi, pt1*shift, phi1 )
#    mt_2_UP = getTransMass( mvametcorr, mvametcorrphi, pt2*shift, phi2 )
#    return calcMTTotal( pt1*shift, phi1, pt2*shift, phi2, mt_1_UP, mt_2_UP )
#
#
#def calcMTTotal( pt1, phi1, pt2, phi2, mt1, mt2 ) :
#    mt_diTau = getTransMass( pt1, phi1, pt2, phi2 )
#    return math.sqrt( mt_diTau**2 + mt1**2 + mt2**2 )


def getTransMass( met, metphi, l1pt, l1phi ) :
    if met < 0. : metTmp = 0.
    else : metTmp = met
    return math.sqrt( 2 * l1pt * metTmp * (1 - math.cos( l1phi - metphi)))


def getIso( cand, row ) :
    if 'e' in cand :
        return getattr(row, cand+'RelPFIsoDB')
    if 'm' in cand :
        return getattr(row, cand+'RelPFIsoDBDefault')
    if 't' in cand :
        #return getattr(row, cand+'ByCombinedIsolationDeltaBetaCorrRaw3Hits')
        return getattr(row, cand+'ByIsolationMVArun2v1DBoldDMwLTraw' )
                    

def getCurrentEvt( analysis, channel, row ) :
    l1 = prodMap[channel][0]
    l2 = prodMap[channel][1]
    leg1Iso = getIso( l1, row )
    leg2Iso = getIso( l2, row )
    leg1Pt = getattr(row, l1+'Pt')
    leg2Pt = getattr(row, l2+'Pt')
    if (analysis == 'htt' or analysis == 'Sync') and channel == 'tt' :
        if leg1Iso > leg2Iso :
            currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)
        elif leg1Iso < leg2Iso :
            currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt)
        elif leg1Pt > leg2Pt :
            currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)
        elif leg1Pt < leg2Pt :
            currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt)
        else : print "Iso1 == Iso2 & Pt1 == Pt2", row.evt
    elif analysis == 'azh' :
        l3 = prodMap[channel][2]
        l4 = prodMap[channel][3]
        leg3Pt = getattr(row, l3+'Pt')
        leg4Pt = getattr(row, l4+'Pt')
        closeZ = abs( getattr(row, l1+'_'+l2+'_Mass') - 91.2 )
        LT = leg3Pt + leg4Pt # LT here is just Higgs_LT
        currentEvt = (closeZ, LT)
    else : currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)

    return currentEvt


tauIsoList = [
'Pt', 'Eta', 'Phi', 'Mass', 'Charge', 'PVDXY', 'PVDZ', 'MtToPfMet_type1',
'ByCombinedIsolationDeltaBetaCorrRaw3Hits', 'ByIsolationMVArun2v1DBnewDMwLTraw',
'ByIsolationMVArun2v1DBoldDMwLTraw', 'ByLooseIsolationMVArun2v1DBoldDMwLT',
'ByMediumIsolationMVArun2v1DBoldDMwLT', 'ByTightIsolationMVArun2v1DBoldDMwLT',
'ByVTightIsolationMVArun2v1DBoldDMwLT', 'ByIsolationMVA3newDMwLTraw',
'ByIsolationMVA3oldDMwLTraw', 'AgainstElectronLooseMVA6', 'AgainstElectronMediumMVA6',
'AgainstElectronTightMVA6', 'AgainstElectronVLooseMVA6', 'AgainstElectronVTightMVA6',
'AgainstMuonLoose3', 'AgainstMuonTight3', 'ChargedIsoPtSum', 'NeutralIsoPtSum',
'PuCorrPtSum', 'AbsEta', 'DecayMode', 'DecayModeFinding', 'DoubleTau40Filter',
'ElecOverlap', 'GenDecayMode', 'ZTTGenMatching', 'ZTTGenMatching2', 'GlobalMuonVtxOverlap',
'JetArea', 'JetBtag', 'JetEtaEtaMoment', 'JetEtaPhiMoment', 'JetPFCISVBtag',
'JetPartonFlavour', 'JetPhiPhiMoment', 'JetPt', 'GenJetPt', 'LeadTrackPt', 'LowestMll',
'ZTTGenPt', 'ZTTGenEta', 'ZTTGenPhi', 'ZTTGenDR',
'MatchesDoubleTau40Path', 'MatchesDoubleTau35Path', 'MuOverlap', 'MuonIdIsoStdVtxOverlap',
'MuonIdIsoVtxOverlap', 'MuonIdVtxOverlap', 'NearestZMass', 'Rank', 'VZ',]

def isoOrder( channel, row ) :
    if channel != 'tt' : return
    iso1 = getattr( row, 't1ByIsolationMVArun2v1DBoldDMwLTraw' )
    iso2 = getattr( row, 't2ByIsolationMVArun2v1DBoldDMwLTraw' )
        
    #iso1 = getattr( row, 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits')
    #iso2 = getattr( row, 't2ByCombinedIsolationDeltaBetaCorrRaw3Hits')
    pt1 = getattr( row, 't1Pt' )
    pt2 = getattr( row, 't2Pt' )
    if iso2 > iso1 :
        for uw in tauIsoList :
            if not hasattr( row, 't1%s' % uw ) : continue
            if not hasattr( row, 't2%s' % uw ) : continue
            tmp1 = getattr( row, 't1%s' % uw )
            tmp2 = getattr( row, 't2%s' % uw )
            setattr( row, 't1%s' % uw, tmp2 )
            setattr( row, 't2%s' % uw, tmp1 )

def vbfClean( row, analysis ) :
    if row.jetVeto20 < 2 :
        if analysis == 'Sync' : # This just makes sync ntuples prettier
            setattr( row, 'vbfMass', -10000 )
        setattr( row, 'vbfDeta', -10 )
        setattr( row, 'vbfDphi', -10 )
        setattr( row, 'vbfJetVeto30', -10 )
        setattr( row, 'vbfJetVeto20', -10 )

def calcDR( eta1, phi1, eta2, phi2 ) :
    return float(math.sqrt( (eta1-eta2)*(eta1-eta2) + (phi1-phi2)*(phi1-phi2) ))



def renameBranches( analysis, mid1, mid2, sample, channel, count ) :
    with open('meta/NtupleInputs_%s/samples.json' % analysis) as sampFile :
        sampDict = json.load( sampFile )

    shortName = sample.split('_')[0]

    xsec = getXSec( analysis, shortName, sampDict )
    print "\n Sampe: %s    shortName: %s    xsec: %f" % (sample, shortName, xsec)

    l1 = prodMap[channel][0]
    l2 = prodMap[channel][1]
    if len( channel ) == 4 :
        l3 = prodMap[channel][2]
        l4 = prodMap[channel][3]

    #from util.lepSF import LepWeights
    from util.doubleTauSF import DoubleTau35Efficiencies
    from util.muonSF import MuonSF
    from util.electronSF import ElectronSF
    #lepWeights = LepWeights( channel, count )
    doublTau35 = DoubleTau35Efficiencies( channel )
    muonSF = MuonSF()
    electronSF = ElectronSF()

    from util.zPtReweight import ZPtReweighter
    zPtWeighter = ZPtReweighter()
    from util.extraTauMVArun2v1IsoWPs import IsoWPAdder
    isoWPAdder = IsoWPAdder()

    from util.qqZZ4l_reweight import qqZZ4l_nnlo_weight

    if len(channel) > 3 : # either AZH or ZH analysis
        from util.applyReducibleBkg import ReducibleBkgWeights
        zhFRObj = ReducibleBkgWeights( channel )

    #cmssw_base = os.getenv('CMSSW_BASE')
    #ff_file = ROOT.TFile.Open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/fakeFactors_20160425.root')
    #ffqcd = ff_file.Get('ff_qcd_os') 

    sameNameVars = [
    'run','lumi','evt','GenWeight','LT','charge','jetVeto30',
    'bjetCISVVeto20Medium','Mt','bjetCISVVeto30Medium','bjetCISVVeto30Tight',]

    branchMapping = {
        'nvtx' : 'npv',
        'nTruePU' : 'npu',
        'j1pt' : 'jpt_1',
        'j1phi' : 'jphi_1',
        'j1eta' : 'jeta_1',
        #XXX'j1mva' : 'jmva_1',
        'j2pt' : 'jpt_2',
        'j2phi' : 'jphi_2',
        'j2eta' : 'jeta_2',
        #XXX'j2mva' : 'jmva_2',
        'jb1pt' : 'bpt_1',
        'jb1phi' : 'bphi_1',
        'jb1eta' : 'beta_1',
        #XXX'jb1mva' : 'bmva_1',
        'jb1csv' : 'bcsv_1',
        'jb2pt' : 'bpt_2',
        'jb2phi' : 'bphi_2',
        'jb2eta' : 'beta_2',
        #XXX'jb2mva' : 'bmva_2',
        'jb2csv' : 'bcsv_2',
        'bjetCISVVeto20Medium' : 'nbtag',
        'bjetCISVVeto20Loose' : 'nbtagloose',
        #XXX 'NBTagPDM_idL_jVeto' : 'nbtag',
        #XXX 'NBTagPDL_idL_jVeto' : 'nbtagLoose',
        'jetVeto20' : 'njetspt20',
        'jetVeto30' : 'njets',
        'type1_pfMetEt' : 'met',
        'type1_pfMetPhi' : 'metphi',
        #'GenWeight' : 'weight',
        'vbfMass' : 'mjj',
        'vbfDeta' : 'jdeta',
        'vbfDphi' : 'jdphi',
        'vbfJetVeto30' : 'njetingap',
        'vbfJetVeto20' : 'njetingap20',
        'puppiMetEt' : 'puppimet',
        'puppiMetPhi' : 'puppimetphi',
        }

    doubleProds = {
        'Mass' : 'm_vis',
        'PZeta' : 'pfpzetamis',
        'PZetaVis' : 'pzetavis',
        'SS' : 'Z_SS',
        'Pt' : 'Z_Pt',
        'DR' : 'Z_DR',
        'DPhi' : 'Z_DPhi',
        }
    quadFSDoubleProds = {
        'Mass' : 'H_vis',
        'SS' : 'H_SS',
        'Pt' : 'H_Pt',
        'DR' : 'H_DR',
        'DPhi' : 'H_DPhi',
        }
    branchMappingElec = {
        'cand_Pt' : 'pt', # rename ePt to pt_1
        'cand_Eta' : 'eta',
        'cand_Phi' : 'phi',
        'cand_Mass' : 'm',
        'cand_Charge' : 'q',
        'cand_PVDXY' : 'd0',
        'cand_PVDZ' : 'dZ',
        'cand_IsoDB03' : 'iso',
        'cand_MVANonTrigWP80' : 'id_e_mva_nt_tight',
        'cand_MVANonTrigWP90' : 'id_e_mva_nt_loose',
        'cand_MtToPfMet_type1' : 'pfmt',
        }
    branchMappingMuon = {
        'cand_Pt' : 'pt',
        'cand_Eta' : 'eta',
        'cand_Phi' : 'phi',
        'cand_Mass' : 'm',
        'cand_Charge' : 'q',
        'cand_PVDXY' : 'd0',
        'cand_PVDZ' : 'dZ',
        'cand_IsoDB04' : 'iso',
        'cand_MtToPfMet_type1' : 'pfmt',
        }
    branchMappingTau = {
        'cand_Pt' : 'pt',
        'cand_DecayMode' : 'decayMode',
        'cand_Eta' : 'eta',
        'cand_Phi' : 'phi',
        'cand_Mass' : 'm',
        'cand_Charge' : 'q',
        'cand_PVDXY' : 'd0',
        'cand_PVDZ' : 'dZ',
        'cand_ByCombinedIsolationDeltaBetaCorrRaw3Hits' : 'byCombinedIsolationDeltaBetaCorrRaw3Hits',
        #'cand_ByCombinedIsolationDeltaBetaCorrRaw3Hits' : 'iso',
        'cand_ByIsolationMVArun2v1DBnewDMwLTraw' : 'byIsolationMVArun2v1DBnewDMwLTraw',
        #'cand_ByIsolationMVArun2v1DBoldDMwLTraw' : 'byIsolationMVArun2v1DBoldDMwLTraw',
        'cand_ByIsolationMVArun2v1DBoldDMwLTraw' : 'iso',
        'cand_AgainstElectronLooseMVA6' : 'againstElectronLooseMVA6',
        'cand_AgainstElectronMediumMVA6' : 'againstElectronMediumMVA6',
        'cand_AgainstElectronTightMVA6' : 'againstElectronTightMVA6',
        'cand_AgainstElectronVLooseMVA6' : 'againstElectronVLooseMVA6',
        'cand_AgainstElectronVTightMVA6' : 'againstElectronVTightMVA6',
        'cand_AgainstMuonLoose3' : 'againstMuonLoose3',
        'cand_AgainstMuonTight3' : 'againstMuonTight3',
        'cand_ChargedIsoPtSum' : 'chargedIsoPtSum',
        'cand_ChargedIsoPtSumdR03' : 'chargedIsoPtSumdR03',
        'cand_DecayModeFinding' : 'decayModeFindingOldDMs',
        'cand_NeutralIsoPtSum' : 'neutralIsoPtSum',
        'cand_PuCorrPtSum' : 'puCorrPtSum',
        'cand_MtToPfMet_type1' : 'pfmt',
        'cand_ByVTightIsolationMVArun2v1DBoldDMwLT' : 'byVTightIsolationMVArun2v1DBoldDMwLT',
        'cand_ByTightIsolationMVArun2v1DBoldDMwLT' : 'byTightIsolationMVArun2v1DBoldDMwLT',
        'cand_ByMediumIsolationMVArun2v1DBoldDMwLT' : 'byMediumIsolationMVArun2v1DBoldDMwLT',
        'cand_ByLooseIsolationMVArun2v1DBoldDMwLT' : 'byLooseIsolationMVArun2v1DBoldDMwLT',
        'cand_ByVLooseIsolationMVArun2v1DBoldDMwLT' : 'byVLooseIsolationMVArun2v1DBoldDMwLT',
        }

    # Add in the vars which won't change names
    for var in sameNameVars :
        branchMapping[ var ] = var
    # Generate our mapping for double candidate variables
    for key in doubleProds :
        branchMapping[ l1+'_'+l2+'_'+key ] = doubleProds[ key ]
    if len( channel ) == 4 :
        for key in quadFSDoubleProds :
            branchMapping[ l3+'_'+l4+'_'+key ] = quadFSDoubleProds[ key ]
    # Map all of the variables based on their FSA names to Sync names leg by leg
    if len( channel ) == 2 :
        if channel == 'em' :
            l1Map = copy.deepcopy( branchMappingElec )
            l2Map = copy.deepcopy( branchMappingMuon )
        elif channel == 'et' :
            l1Map = copy.deepcopy( branchMappingElec )
            l2Map = copy.deepcopy( branchMappingTau )
        elif channel == 'mt' :
            l1Map = copy.deepcopy( branchMappingMuon )
            l2Map = copy.deepcopy( branchMappingTau )
        elif channel == 'tt' :
            l1Map = copy.deepcopy( branchMappingTau )
            l2Map = copy.deepcopy( branchMappingTau )
    if len( channel ) == 4 :
        # Channel naming gets confusing with FSA, e first, m second, t last
        if channel[:2] == 'ee' :
            l1Map = copy.deepcopy( branchMappingElec )
            l2Map = copy.deepcopy( branchMappingElec )
        elif channel[:2] == 'mm' or channel == 'emmt' or channel == 'emmm' :
            l1Map = copy.deepcopy( branchMappingMuon )
            l2Map = copy.deepcopy( branchMappingMuon )

        if channel == 'eeet' or channel == 'emmt' :
            l3Map = copy.deepcopy( branchMappingElec )
            l4Map = copy.deepcopy( branchMappingTau )
        elif channel == 'eeem' or channel == 'emmm' :
            l3Map = copy.deepcopy( branchMappingElec )
            l4Map = copy.deepcopy( branchMappingMuon )
        elif channel[-2:] == 'ee' :
            l3Map = copy.deepcopy( branchMappingElec )
            l4Map = copy.deepcopy( branchMappingElec )
        elif channel[-2:] == 'mm' :
            l3Map = copy.deepcopy( branchMappingMuon )
            l4Map = copy.deepcopy( branchMappingMuon )
        elif channel[-2:] == 'tt' :
            l3Map = copy.deepcopy( branchMappingTau )
            l4Map = copy.deepcopy( branchMappingTau )
        elif channel[-2:] == 'mt' :
            l3Map = copy.deepcopy( branchMappingMuon )
            l4Map = copy.deepcopy( branchMappingTau )

        for key in l3Map.keys() :
            branchMapping[ key.replace('cand_', l3) ] = l3Map[ key ]+'_3'
        for key in l4Map.keys() :
            branchMapping[ key.replace('cand_', l4) ] = l4Map[ key ]+'_4'
    # applies to all channels of len 2 and 4
    for key in l1Map.keys() :
        branchMapping[ key.replace('cand_', l1) ] = l1Map[ key ]+'_1'
    for key in l2Map.keys() :
        branchMapping[ key.replace('cand_', l2) ] = l2Map[ key ]+'_2'


    oldFileName = '%s%s/%s.root' % (analysis, mid1, sample)
    newFileName = '%s%s/%s.root' % (analysis, mid2, sample)

    dirName = channel+'/final'
    treeName = 'Ntuple'
    
    # A few branches are ints instead of floats and must be treated specially
    # I think these are all the ones in FSA ntuples, but add more if you find them
    intBranches = set(['run', 'lumi', 'isdata',])
    ulongBranches = set(['evt',])
    
    ##############################################################################
    # Shouldn't need to modify anything below here                               #
    ##############################################################################
    
    from rootpy.io import root_open
    from rootpy.tree import Tree, TreeModel, FloatCol, IntCol, ULongCol
    # don't give silly warning
    import logging
    from rootpy import log as rlog; rlog = rlog['/renameBranches']
    logging.basicConfig(level=logging.WARNING)
    rlog["/rootpy.tree"].setLevel(rlog.ERROR)
    
    # get old tree
    fold = root_open(oldFileName)
    dold = fold.Get(dirName)
    told = dold.Get(treeName)
    told.create_buffer()
    
    # get list of branches for new tree
    newBranches = {}
    for old in told.branchnames:
        name = branchMapping[old] if old in branchMapping else old

        #branchType = IntCol() if old in intBranches else FloatCol()
        if old in intBranches : branchType = IntCol()
        elif old in ulongBranches : branchType = ULongCol()
        else : branchType = FloatCol()

        if old in branchMapping.keys() :
            name = branchMapping[old]
            #branchType = IntCol() if old in intBranches else FloatCol()
            if old in intBranches : branchType = IntCol()
            elif old in ulongBranches : branchType = ULongCol()
            else : branchType = FloatCol()
            newBranches[name] = branchType
    
        newBranches[name] = branchType
    
    NewTreeModel = type("NewTreeModel", (TreeModel,), newBranches)
    
    # make new tree
    fnew = root_open(newFileName, "recreate")
    tnew = Tree(treeName, model=NewTreeModel)
    
    # set buffer to same memory locations as old tree for fast copying
    tnew.set_buffer(told._buffer, ignore_missing=True)
    for old, new in branchMapping.iteritems():
        tnew.SetBranchAddress(new, told._buffer[old])
        tnew._buffer[new] = told._buffer[old]
    

    ''' Select the version of each even we want to keep '''
    numRows = told.GetEntries()
    #print "Num rows %i" % numRows
    prevEvt = (999, 0, 999, 0)
    prevRunLumiEvt = (0, 0, 0)
    toFillMap = {}
    count = 0
    for row in told:
        run = int( row.run )
        lumi = int( row.lumi )
        evt = int( row.evt )
        
        currentEvt = getCurrentEvt( analysis, channel, row )
        currentRunLumiEvt = (run, lumi, evt)
        if count == 0 :
            prevRunLumiEvt = currentRunLumiEvt
            prevEvt = currentEvt

        count += 1

        
        if currentRunLumiEvt != prevRunLumiEvt :
            toFillMap[ prevRunLumiEvt ] = prevEvt
            prevRunLumiEvt = currentRunLumiEvt
            prevEvt = currentEvt

            # Make sure that the last event is filled!
            if count == numRows :
                #print "LastRow:",prevRunLumiEvt, prevEvt
                prevRunLumiEvt = currentRunLumiEvt
                prevEvt = currentEvt
                toFillMap[ prevRunLumiEvt ] = prevEvt
            continue

        #print "Current: ",currentRunLumiEvt, currentEvt
        """
        Iso sorting is channel specific b/c tt uses MVA iso
        where are high value == good isolation
        """
        if (analysis == 'htt' or analysis == 'Sync') and channel == 'tt' :
            # lowest iso_1
            if currentEvt[ 0 ] > prevEvt[ 0 ] :
                prevEvt = currentEvt
            # iso_1 equal
            elif currentEvt[ 0 ] == prevEvt[ 0 ] :
                # highest pt_1
                if currentEvt[ 1 ] > prevEvt[ 1 ] :
                    prevEvt = currentEvt
                # pt_1 equal
                elif currentEvt[ 1 ] == prevEvt[ 1 ] :
                    # lowest iso_2
                    if currentEvt[ 2 ] > prevEvt[ 2 ] :
                        prevEvt = currentEvt
                    # iso_2 equal
                    elif currentEvt[ 2 ] == prevEvt[ 2 ] :
                        # highest pt_2
                        if currentEvt[ 3 ] > prevEvt[ 3 ] :
                            prevEvt = currentEvt
        elif analysis == 'azh' :
            # closest Z to Z mass top priority, then highest Higgs LT
            if currentEvt[ 0 ] < prevEvt[ 0 ] :
                prevEvt = currentEvt
            elif currentEvt[ 0 ] == prevEvt[ 0 ] :
                if currentEvt[ 1 ] > prevEvt[ 1 ] :
                    prevEvt = currentEvt
        else :
            # lowest iso_1
            if currentEvt[ 0 ] < prevEvt[ 0 ] :
                prevEvt = currentEvt
            # iso_1 equal
            elif currentEvt[ 0 ] == prevEvt[ 0 ] :
                # highest pt_1
                if currentEvt[ 1 ] > prevEvt[ 1 ] :
                    prevEvt = currentEvt
                # pt_1 equal
                elif currentEvt[ 1 ] == prevEvt[ 1 ] :
                    # lowest iso_2
                    if currentEvt[ 2 ] < prevEvt[ 2 ] :
                        prevEvt = currentEvt
                    # iso_2 equal
                    elif currentEvt[ 2 ] == prevEvt[ 2 ] :
                        # highest pt_2
                        if currentEvt[ 3 ] > prevEvt[ 3 ] :
                            prevEvt = currentEvt
        

        # Make sure we get the last event
        # A previous check covered this situation
        # if prevRunLumiEvt != currentRunLumiEvt
        # so just fill here with the best version
        # of an event we have
        if count == numRows :
            #print "LastRowPrev:",prevRunLumiEvt, prevEvt
            #print "LastRowCur:",currentRunLumiEvt, currentEvt
            toFillMap[ prevRunLumiEvt ] = prevEvt
    
    ''' Add a nvtx Pile UP weighting variable to the new tree
    see util.pileUpVertexCorrections.addNvtxWeight for inspiration '''
    from util.pZeta import compZeta
    from util.pileUpVertexCorrections import PUreweight
    from array import array
    puDict = PUreweight()

    ''' We are calculating and adding these below variables to our new tree
    PU Weighting '''
    byVVTightIsolationMVArun2v1DBoldDMwLT_1 = array('f', [ 0 ] )
    byVVTightIsolationMVArun2v1DBoldDMwLT_1B = tnew.Branch('byVVTightIsolationMVArun2v1DBoldDMwLT_1', byVVTightIsolationMVArun2v1DBoldDMwLT_1, 'byVVTightIsolationMVArun2v1DBoldDMwLT_1/F')
    byVVTightIsolationMVArun2v1DBoldDMwLT_2 = array('f', [ 0 ] )
    byVVTightIsolationMVArun2v1DBoldDMwLT_2B = tnew.Branch('byVVTightIsolationMVArun2v1DBoldDMwLT_2', byVVTightIsolationMVArun2v1DBoldDMwLT_2, 'byVVTightIsolationMVArun2v1DBoldDMwLT_2/F')
    byVVLooseIsolationMVArun2v1DBoldDMwLT_1 = array('f', [ 0 ] )
    byVVLooseIsolationMVArun2v1DBoldDMwLT_1B = tnew.Branch('byVVLooseIsolationMVArun2v1DBoldDMwLT_1', byVVLooseIsolationMVArun2v1DBoldDMwLT_1, 'byVVLooseIsolationMVArun2v1DBoldDMwLT_1/F')
    byVVLooseIsolationMVArun2v1DBoldDMwLT_2 = array('f', [ 0 ] )
    byVVLooseIsolationMVArun2v1DBoldDMwLT_2B = tnew.Branch('byVVLooseIsolationMVArun2v1DBoldDMwLT_2', byVVLooseIsolationMVArun2v1DBoldDMwLT_2, 'byVVLooseIsolationMVArun2v1DBoldDMwLT_2/F')
    byVVLooseIsolationMVArun2v1DBoldDMwLT_3 = array('f', [ 0 ] )
    byVVLooseIsolationMVArun2v1DBoldDMwLT_3B = tnew.Branch('byVVLooseIsolationMVArun2v1DBoldDMwLT_3', byVVLooseIsolationMVArun2v1DBoldDMwLT_3, 'byVVLooseIsolationMVArun2v1DBoldDMwLT_3/F')
    byVVLooseIsolationMVArun2v1DBoldDMwLT_4 = array('f', [ 0 ] )
    byVVLooseIsolationMVArun2v1DBoldDMwLT_4B = tnew.Branch('byVVLooseIsolationMVArun2v1DBoldDMwLT_4', byVVLooseIsolationMVArun2v1DBoldDMwLT_4, 'byVVLooseIsolationMVArun2v1DBoldDMwLT_4/F')
    isoCode1 = array('f', [ 0 ] )
    isoCode1B = tnew.Branch('isoCode1', isoCode1, 'isoCode1/F')
    isoCode2 = array('f', [ 0 ] )
    isoCode2B = tnew.Branch('isoCode2', isoCode2, 'isoCode2/F')
    weight = array('f', [ 0 ] )
    weightB = tnew.Branch('weight', weight, 'weight/F')
    azhWeight = array('f', [ 0 ] )
    azhWeightB = tnew.Branch('azhWeight', azhWeight, 'azhWeight/F')
    puweight = array('f', [ 0 ] )
    puweightB = tnew.Branch('puweight', puweight, 'puweight/F')
    qqZZ4lWeight = array('f', [ 0 ] )
    qqZZ4lWeightB = tnew.Branch('qqZZ4lWeight', qqZZ4lWeight, 'qqZZ4lWeight/F')
    tauPtWeightUp = array('f', [ 0 ] )
    tauPtWeightUpB = tnew.Branch('tauPtWeightUp', tauPtWeightUp, 'tauPtWeightUp/F')
    tauPtWeightDown = array('f', [ 0 ] )
    tauPtWeightDownB = tnew.Branch('tauPtWeightDown', tauPtWeightDown, 'tauPtWeightDown/F')
    topWeight = array('f', [ 0 ] )
    topWeightB = tnew.Branch('topWeight', topWeight, 'topWeight/F')
    zPtWeight = array('f', [ 0 ] )
    zPtWeightB = tnew.Branch('zPtWeight', zPtWeight, 'zPtWeight/F')
    zmumuVBFWeight = array('f', [ 0 ] )
    zmumuVBFWeightB = tnew.Branch('zmumuVBFWeight', zmumuVBFWeight, 'zmumuVBFWeight/F')
    ggHWeight0Jet = array('f', [ 0 ] )
    ggHWeight0JetB = tnew.Branch('ggHWeight0Jet', ggHWeight0Jet, 'ggHWeight0Jet/F')
    ggHWeightBoost = array('f', [ 0 ] )
    ggHWeightBoostB = tnew.Branch('ggHWeightBoost', ggHWeightBoost, 'ggHWeightBoost/F')
    ggHWeightVBF = array('f', [ 0 ] )
    ggHWeightVBFB = tnew.Branch('ggHWeightVBF', ggHWeightVBF, 'ggHWeightVBF/F')
    jetToTauFakeWeight = array('f', [ 0 ] )
    jetToTauFakeWeightB = tnew.Branch('jetToTauFakeWeight', jetToTauFakeWeight, 'jetToTauFakeWeight/F')
    pzetamiss = array('f', [ 0 ] )
    pzetamissB = tnew.Branch('pzetamiss', pzetamiss, 'pzetamiss/F')
    pzeta = array('f', [ 0 ] )
    pzetaB = tnew.Branch('pzeta', pzeta, 'pzeta/F')
    Higgs_Pt = array('f', [ 0 ] )
    Higgs_PtB = tnew.Branch('Higgs_Pt', Higgs_Pt, 'Higgs_Pt/F')
    Z_DEta = array('f', [ 0 ] )
    Z_DEtaB = tnew.Branch('Z_DEta', Z_DEta, 'Z_DEta/F')
    m_vis_UP = array('f', [ 0 ] )
    m_vis_UPB = tnew.Branch('m_vis_UP', m_vis_UP, 'm_vis_UP/F')
    m_vis_DOWN = array('f', [ 0 ] )
    m_vis_DOWNB = tnew.Branch('m_vis_DOWN', m_vis_DOWN, 'm_vis_DOWN/F')
    #mt_tot = array('f', [ 0 ] )
    #mt_totB = tnew.Branch('mt_tot', mt_tot, 'mt_tot/F')
    #mt_tot_UP = array('f', [ 0 ] )
    #mt_tot_UPB = tnew.Branch('mt_tot_UP', mt_tot_UP, 'mt_tot_UP/F')
    #mt_tot_DOWN = array('f', [ 0 ] )
    #mt_tot_DOWNB = tnew.Branch('mt_tot_DOWN', mt_tot_DOWN, 'mt_tot_DOWN/F')
    mt_1 = array('f', [ 0 ] )
    mt_1B = tnew.Branch('mt_1', mt_1, 'mt_1/F')
    mt_2 = array('f', [ 0 ] )
    mt_2B = tnew.Branch('mt_2', mt_2, 'mt_2/F')
    XSecLumiWeight = array('f', [ 0 ] )
    XSecLumiWeightB = tnew.Branch('XSecLumiWeight', XSecLumiWeight, 'XSecLumiWeight/F')
    trigweight_1 = array('f', [ 0 ] )
    trigweight_1B = tnew.Branch('trigweight_1', trigweight_1, 'trigweight_1/F')
    trigweight_2 = array('f', [ 0 ] )
    trigweight_2B = tnew.Branch('trigweight_2', trigweight_2, 'trigweight_2/F')
    tauIDweight_1 = array('f', [ 0 ] )
    tauIDweight_1B = tnew.Branch('tauIDweight_1', tauIDweight_1, 'tauIDweight_1/F')
    tauIDweight_2 = array('f', [ 0 ] )
    tauIDweight_2B = tnew.Branch('tauIDweight_2', tauIDweight_2, 'tauIDweight_2/F')
    idisoweight_1 = array('f', [ 0 ] )
    idisoweight_1B = tnew.Branch('idisoweight_1', idisoweight_1, 'idisoweight_1/F')
    idisoweight_2 = array('f', [ 0 ] )
    idisoweight_2B = tnew.Branch('idisoweight_2', idisoweight_2, 'idisoweight_2/F')
    extramuon_veto = array('f', [ 0 ] )
    extramuon_vetoB = tnew.Branch('extramuon_veto', extramuon_veto, 'extramuon_veto/F')
    extraelec_veto = array('f', [ 0 ] )
    extraelec_vetoB = tnew.Branch('extraelec_veto', extraelec_veto, 'extraelec_veto/F')
    mvacov00 = array('f', [ 0 ] )
    mvacov00B = tnew.Branch('mvacov00', mvacov00, 'mvacov00/F')
    mvacov01 = array('f', [ 0 ] )
    mvacov01B = tnew.Branch('mvacov01', mvacov01, 'mvacov01/F')
    mvacov10 = array('f', [ 0 ] )
    mvacov10B = tnew.Branch('mvacov10', mvacov10, 'mvacov10/F')
    mvacov11 = array('f', [ 0 ] )
    mvacov11B = tnew.Branch('mvacov11', mvacov11, 'mvacov11/F')
    mvamet = array('f', [ 0 ] )
    mvametB = tnew.Branch('mvamet', mvamet, 'mvamet/F')
    mvametphi = array('f', [ 0 ] )
    mvametphiB = tnew.Branch('mvametphi', mvametphi, 'mvametphi/F')
    gen_match_1 = array('f', [ 0 ] )
    gen_match_1B = tnew.Branch('gen_match_1', gen_match_1, 'gen_match_1/F')
    gen_match_2 = array('f', [ 0 ] )
    gen_match_2B = tnew.Branch('gen_match_2', gen_match_2, 'gen_match_2/F')
    gen_match_3 = array('f', [ 0 ] )
    gen_match_3B = tnew.Branch('gen_match_3', gen_match_3, 'gen_match_3/F')
    gen_match_4 = array('f', [ 0 ] )
    gen_match_4B = tnew.Branch('gen_match_4', gen_match_4, 'gen_match_4/F')
    muonSF1 = array('f', [ 0 ] )
    muonSF1B = tnew.Branch('muonSF1', muonSF1, 'muonSF1/F')
    muonSF2 = array('f', [ 0 ] )
    muonSF2B = tnew.Branch('muonSF2', muonSF2, 'muonSF2/F')
    muonSF3 = array('f', [ 0 ] )
    muonSF3B = tnew.Branch('muonSF3', muonSF3, 'muonSF3/F')
    muonSF4 = array('f', [ 0 ] )
    muonSF4B = tnew.Branch('muonSF4', muonSF4, 'muonSF4/F')
    electronSF1 = array('f', [ 0 ] )
    electronSF1B = tnew.Branch('electronSF1', electronSF1, 'electronSF1/F')
    electronSF2 = array('f', [ 0 ] )
    electronSF2B = tnew.Branch('electronSF2', electronSF2, 'electronSF2/F')
    electronSF3 = array('f', [ 0 ] )
    electronSF3B = tnew.Branch('electronSF3', electronSF3, 'electronSF3/F')
    electronSF4 = array('f', [ 0 ] )
    electronSF4B = tnew.Branch('electronSF4', electronSF4, 'electronSF4/F')
    zhFR0 = array('f', [ 0 ] )
    zhFR0B = tnew.Branch('zhFR0', zhFR0, 'zhFR0/F')
    zhFR1 = array('f', [ 0 ] )
    zhFR1B = tnew.Branch('zhFR1', zhFR1, 'zhFR1/F')
    zhFR2 = array('f', [ 0 ] )
    zhFR2B = tnew.Branch('zhFR2', zhFR2, 'zhFR2/F')
    LT_higgs = array('f', [ 0 ] )
    LT_higgsB = tnew.Branch('LT_higgs', LT_higgs, 'LT_higgs/F')
    ptCor_1 = array('f', [ 0 ] )
    ptCor_1B = tnew.Branch('ptCor_1', ptCor_1, 'ptCor_1/F')
    ptCor_2 = array('f', [ 0 ] )
    ptCor_2B = tnew.Branch('ptCor_2', ptCor_2, 'ptCor_2/F')
    pt_1_UP = array('f', [ 0 ] )
    pt_1_UPB = tnew.Branch('pt_1_UP', pt_1_UP, 'pt_1_UP/F')
    pt_1_DOWN = array('f', [ 0 ] )
    pt_1_DOWNB = tnew.Branch('pt_1_DOWN', pt_1_DOWN, 'pt_1_DOWN/F')
    pt_1_DM0_UP = array('f', [ 0 ] )
    pt_1_DM0_UPB = tnew.Branch('pt_1_DM0_UP', pt_1_DM0_UP, 'pt_1_DM0_UP/F')
    pt_1_DM0_DOWN = array('f', [ 0 ] )
    pt_1_DM0_DOWNB = tnew.Branch('pt_1_DM0_DOWN', pt_1_DM0_DOWN, 'pt_1_DM0_DOWN/F')
    pt_1_DM1_UP = array('f', [ 0 ] )
    pt_1_DM1_UPB = tnew.Branch('pt_1_DM1_UP', pt_1_DM1_UP, 'pt_1_DM1_UP/F')
    pt_1_DM1_DOWN = array('f', [ 0 ] )
    pt_1_DM1_DOWNB = tnew.Branch('pt_1_DM1_DOWN', pt_1_DM1_DOWN, 'pt_1_DM1_DOWN/F')
    pt_1_DM10_UP = array('f', [ 0 ] )
    pt_1_DM10_UPB = tnew.Branch('pt_1_DM10_UP', pt_1_DM10_UP, 'pt_1_DM10_UP/F')
    pt_1_DM10_DOWN = array('f', [ 0 ] )
    pt_1_DM10_DOWNB = tnew.Branch('pt_1_DM10_DOWN', pt_1_DM10_DOWN, 'pt_1_DM10_DOWN/F')
    pt_2_UP = array('f', [ 0 ] )
    pt_2_UPB = tnew.Branch('pt_2_UP', pt_2_UP, 'pt_2_UP/F')
    pt_2_DOWN = array('f', [ 0 ] )
    pt_2_DOWNB = tnew.Branch('pt_2_DOWN', pt_2_DOWN, 'pt_2_DOWN/F')
    pt_2_DM0_UP = array('f', [ 0 ] )
    pt_2_DM0_UPB = tnew.Branch('pt_2_DM0_UP', pt_2_DM0_UP, 'pt_2_DM0_UP/F')
    pt_2_DM0_DOWN = array('f', [ 0 ] )
    pt_2_DM0_DOWNB = tnew.Branch('pt_2_DM0_DOWN', pt_2_DM0_DOWN, 'pt_2_DM0_DOWN/F')
    pt_2_DM1_UP = array('f', [ 0 ] )
    pt_2_DM1_UPB = tnew.Branch('pt_2_DM1_UP', pt_2_DM1_UP, 'pt_2_DM1_UP/F')
    pt_2_DM1_DOWN = array('f', [ 0 ] )
    pt_2_DM1_DOWNB = tnew.Branch('pt_2_DM1_DOWN', pt_2_DM1_DOWN, 'pt_2_DM1_DOWN/F')
    pt_2_DM10_UP = array('f', [ 0 ] )
    pt_2_DM10_UPB = tnew.Branch('pt_2_DM10_UP', pt_2_DM10_UP, 'pt_2_DM10_UP/F')
    pt_2_DM10_DOWN = array('f', [ 0 ] )
    pt_2_DM10_DOWNB = tnew.Branch('pt_2_DM10_DOWN', pt_2_DM10_DOWN, 'pt_2_DM10_DOWN/F')
    Higgs_PtCor = array('f', [ 0 ] )
    Higgs_PtCorB = tnew.Branch('Higgs_PtCor', Higgs_PtCor, 'Higgs_PtCor/F')
    Higgs_PtCor_UP = array('f', [ 0 ] )
    Higgs_PtCor_UPB = tnew.Branch('Higgs_PtCor_UP', Higgs_PtCor_UP, 'Higgs_PtCor_UP/F')
    Higgs_PtCor_DOWN = array('f', [ 0 ] )
    Higgs_PtCor_DOWNB = tnew.Branch('Higgs_PtCor_DOWN', Higgs_PtCor_DOWN, 'Higgs_PtCor_DOWN/F')
    Higgs_PtCor_DM0_UP = array('f', [ 0 ] )
    Higgs_PtCor_DM0_UPB = tnew.Branch('Higgs_PtCor_DM0_UP', Higgs_PtCor_DM0_UP, 'Higgs_PtCor_DM0_UP/F')
    Higgs_PtCor_DM0_DOWN = array('f', [ 0 ] )
    Higgs_PtCor_DM0_DOWNB = tnew.Branch('Higgs_PtCor_DM0_DOWN', Higgs_PtCor_DM0_DOWN, 'Higgs_PtCor_DM0_DOWN/F')
    Higgs_PtCor_DM1_UP = array('f', [ 0 ] )
    Higgs_PtCor_DM1_UPB = tnew.Branch('Higgs_PtCor_DM1_UP', Higgs_PtCor_DM1_UP, 'Higgs_PtCor_DM1_UP/F')
    Higgs_PtCor_DM1_DOWN = array('f', [ 0 ] )
    Higgs_PtCor_DM1_DOWNB = tnew.Branch('Higgs_PtCor_DM1_DOWN', Higgs_PtCor_DM1_DOWN, 'Higgs_PtCor_DM1_DOWN/F')
    Higgs_PtCor_DM10_UP = array('f', [ 0 ] )
    Higgs_PtCor_DM10_UPB = tnew.Branch('Higgs_PtCor_DM10_UP', Higgs_PtCor_DM10_UP, 'Higgs_PtCor_DM10_UP/F')
    Higgs_PtCor_DM10_DOWN = array('f', [ 0 ] )
    Higgs_PtCor_DM10_DOWNB = tnew.Branch('Higgs_PtCor_DM10_DOWN', Higgs_PtCor_DM10_DOWN, 'Higgs_PtCor_DM10_DOWN/F')
    Higgs_PtCor_UncMet_UP = array('f', [ 0 ] )
    Higgs_PtCor_UncMet_UPB = tnew.Branch('Higgs_PtCor_UncMet_UP', Higgs_PtCor_UncMet_UP, 'Higgs_PtCor_UncMet_UP/F')
    Higgs_PtCor_UncMet_DOWN = array('f', [ 0 ] )
    Higgs_PtCor_UncMet_DOWNB = tnew.Branch('Higgs_PtCor_UncMet_DOWN', Higgs_PtCor_UncMet_DOWN, 'Higgs_PtCor_UncMet_DOWN/F')
    Higgs_PtCor_ClusteredMet_UP = array('f', [ 0 ] )
    Higgs_PtCor_ClusteredMet_UPB = tnew.Branch('Higgs_PtCor_ClusteredMet_UP', Higgs_PtCor_ClusteredMet_UP, 'Higgs_PtCor_ClusteredMet_UP/F')
    Higgs_PtCor_ClusteredMet_DOWN = array('f', [ 0 ] )
    Higgs_PtCor_ClusteredMet_DOWNB = tnew.Branch('Higgs_PtCor_ClusteredMet_DOWN', Higgs_PtCor_ClusteredMet_DOWN, 'Higgs_PtCor_ClusteredMet_DOWN/F')
    m_visCor = array('f', [ 0 ] )
    m_visCorB = tnew.Branch('m_visCor', m_visCor, 'm_visCor/F')
    m_visCor_UP = array('f', [ 0 ] )
    m_visCor_UPB = tnew.Branch('m_visCor_UP', m_visCor_UP, 'm_visCor_UP/F')
    m_visCor_DM0_UP = array('f', [ 0 ] )
    m_visCor_DM0_UPB = tnew.Branch('m_visCor_DM0_UP', m_visCor_DM0_UP, 'm_visCor_DM0_UP/F')
    m_visCor_DM1_UP = array('f', [ 0 ] )
    m_visCor_DM1_UPB = tnew.Branch('m_visCor_DM1_UP', m_visCor_DM1_UP, 'm_visCor_DM1_UP/F')
    m_visCor_DM10_UP = array('f', [ 0 ] )
    m_visCor_DM10_UPB = tnew.Branch('m_visCor_DM10_UP', m_visCor_DM10_UP, 'm_visCor_DM10_UP/F')
    m_visCor_DOWN = array('f', [ 0 ] )
    m_visCor_DOWNB = tnew.Branch('m_visCor_DOWN', m_visCor_DOWN, 'm_visCor_DOWN/F')
    m_visCor_DM0_DOWN = array('f', [ 0 ] )
    m_visCor_DM0_DOWNB = tnew.Branch('m_visCor_DM0_DOWN', m_visCor_DM0_DOWN, 'm_visCor_DM0_DOWN/F')
    m_visCor_DM1_DOWN = array('f', [ 0 ] )
    m_visCor_DM1_DOWNB = tnew.Branch('m_visCor_DM1_DOWN', m_visCor_DM1_DOWN, 'm_visCor_DM1_DOWN/F')
    m_visCor_DM10_DOWN = array('f', [ 0 ] )
    m_visCor_DM10_DOWNB = tnew.Branch('m_visCor_DM10_DOWN', m_visCor_DM10_DOWN, 'm_visCor_DM10_DOWN/F')


    ''' Set MvaMet base vars defaults in case we didn't fill that value '''
    mvacov00[0] = -999
    mvacov10[0] = -999
    mvacov01[0] = -999
    mvacov11[0] = -999
    mvamet[0] = -999
    mvametphi[0] = -999
    mt_1[0] = -999
    mt_2[0] = -999
    pzeta[0] = -999
    pzetamiss[0] = -999

    ''' Now actually fill that instance of an evtFake'''
    count2 = 0
    xsecList = []
    counter = 0
    for row in told:
        if counter == 0 :
            counter += 1
            # FIXME ugly kludge to handle that some TTrees are missing some
            # branches.  This allows us to HADD the samples
            # REMOVE THIS IN THE FUTURE!
            try : print row[0].type1_pfMet_shiftedPt_UnclusteredEnUp
            except KeyError :
                type1_pfMet_shiftedPhi_ElectronEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_ElectronEnDownB = tnew.Branch('type1_pfMet_shiftedPhi_ElectronEnDown', type1_pfMet_shiftedPhi_ElectronEnDown, 'type1_pfMet_shiftedPhi_ElectronEnDown/F')
                type1_pfMet_shiftedPhi_ElectronEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_ElectronEnUpB = tnew.Branch('type1_pfMet_shiftedPhi_ElectronEnUp', type1_pfMet_shiftedPhi_ElectronEnUp, 'type1_pfMet_shiftedPhi_ElectronEnUp/F')
                type1_pfMet_shiftedPhi_JetEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_JetEnDownB = tnew.Branch('type1_pfMet_shiftedPhi_JetEnDown', type1_pfMet_shiftedPhi_JetEnDown, 'type1_pfMet_shiftedPhi_JetEnDown/F')
                type1_pfMet_shiftedPhi_JetEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_JetEnUpB = tnew.Branch('type1_pfMet_shiftedPhi_JetEnUp', type1_pfMet_shiftedPhi_JetEnUp, 'type1_pfMet_shiftedPhi_JetEnUp/F')
                type1_pfMet_shiftedPhi_JetResDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_JetResDownB = tnew.Branch('type1_pfMet_shiftedPhi_JetResDown', type1_pfMet_shiftedPhi_JetResDown, 'type1_pfMet_shiftedPhi_JetResDown/F')
                type1_pfMet_shiftedPhi_JetResUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_JetResUpB = tnew.Branch('type1_pfMet_shiftedPhi_JetResUp', type1_pfMet_shiftedPhi_JetResUp, 'type1_pfMet_shiftedPhi_JetResUp/F')
                type1_pfMet_shiftedPhi_MuonEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_MuonEnUpB = tnew.Branch('type1_pfMet_shiftedPhi_MuonEnUp', type1_pfMet_shiftedPhi_MuonEnUp, 'type1_pfMet_shiftedPhi_MuonEnUp/F')
                type1_pfMet_shiftedPhi_MuonEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_MuonEnDownB = tnew.Branch('type1_pfMet_shiftedPhi_MuonEnDown', type1_pfMet_shiftedPhi_MuonEnDown, 'type1_pfMet_shiftedPhi_MuonEnDown/F')
                type1_pfMet_shiftedPhi_PhotonEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_PhotonEnDownB = tnew.Branch('type1_pfMet_shiftedPhi_PhotonEnDown', type1_pfMet_shiftedPhi_PhotonEnDown, 'type1_pfMet_shiftedPhi_PhotonEnDown/F')
                type1_pfMet_shiftedPhi_PhotonEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_PhotonEnUpB = tnew.Branch('type1_pfMet_shiftedPhi_PhotonEnUp', type1_pfMet_shiftedPhi_PhotonEnUp, 'type1_pfMet_shiftedPhi_PhotonEnUp/F')
                type1_pfMet_shiftedPhi_TauEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_TauEnUpB = tnew.Branch('type1_pfMet_shiftedPhi_TauEnUp', type1_pfMet_shiftedPhi_TauEnUp, 'type1_pfMet_shiftedPhi_TauEnUp/F')
                type1_pfMet_shiftedPhi_TauEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_TauEnDownB = tnew.Branch('type1_pfMet_shiftedPhi_TauEnDown', type1_pfMet_shiftedPhi_TauEnDown, 'type1_pfMet_shiftedPhi_TauEnDown/F')
                type1_pfMet_shiftedPhi_UnclusteredEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_UnclusteredEnDownB = tnew.Branch('type1_pfMet_shiftedPhi_UnclusteredEnDown', type1_pfMet_shiftedPhi_UnclusteredEnDown, 'type1_pfMet_shiftedPhi_UnclusteredEnDown/F')
                type1_pfMet_shiftedPhi_UnclusteredEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPhi_UnclusteredEnUpB = tnew.Branch('type1_pfMet_shiftedPhi_UnclusteredEnUp', type1_pfMet_shiftedPhi_UnclusteredEnUp, 'type1_pfMet_shiftedPhi_UnclusteredEnUp/F')
                type1_pfMet_shiftedPt_ElectronEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_ElectronEnDownB = tnew.Branch('type1_pfMet_shiftedPt_ElectronEnDown', type1_pfMet_shiftedPt_ElectronEnDown, 'type1_pfMet_shiftedPt_ElectronEnDown/F')
                type1_pfMet_shiftedPt_ElectronEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_ElectronEnUpB = tnew.Branch('type1_pfMet_shiftedPt_ElectronEnUp', type1_pfMet_shiftedPt_ElectronEnUp, 'type1_pfMet_shiftedPt_ElectronEnUp/F')
                type1_pfMet_shiftedPt_JetEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_JetEnDownB = tnew.Branch('type1_pfMet_shiftedPt_JetEnDown', type1_pfMet_shiftedPt_JetEnDown, 'type1_pfMet_shiftedPt_JetEnDown/F')
                type1_pfMet_shiftedPt_JetEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_JetEnUpB = tnew.Branch('type1_pfMet_shiftedPt_JetEnUp', type1_pfMet_shiftedPt_JetEnUp, 'type1_pfMet_shiftedPt_JetEnUp/F')
                type1_pfMet_shiftedPt_JetResDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_JetResDownB = tnew.Branch('type1_pfMet_shiftedPt_JetResDown', type1_pfMet_shiftedPt_JetResDown, 'type1_pfMet_shiftedPt_JetResDown/F')
                type1_pfMet_shiftedPt_JetResUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_JetResUpB = tnew.Branch('type1_pfMet_shiftedPt_JetResUp', type1_pfMet_shiftedPt_JetResUp, 'type1_pfMet_shiftedPt_JetResUp/F')
                type1_pfMet_shiftedPt_MuonEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_MuonEnUpB = tnew.Branch('type1_pfMet_shiftedPt_MuonEnUp', type1_pfMet_shiftedPt_MuonEnUp, 'type1_pfMet_shiftedPt_MuonEnUp/F')
                type1_pfMet_shiftedPt_MuonEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_MuonEnDownB = tnew.Branch('type1_pfMet_shiftedPt_MuonEnDown', type1_pfMet_shiftedPt_MuonEnDown, 'type1_pfMet_shiftedPt_MuonEnDown/F')
                type1_pfMet_shiftedPt_PhotonEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_PhotonEnDownB = tnew.Branch('type1_pfMet_shiftedPt_PhotonEnDown', type1_pfMet_shiftedPt_PhotonEnDown, 'type1_pfMet_shiftedPt_PhotonEnDown/F')
                type1_pfMet_shiftedPt_PhotonEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_PhotonEnUpB = tnew.Branch('type1_pfMet_shiftedPt_PhotonEnUp', type1_pfMet_shiftedPt_PhotonEnUp, 'type1_pfMet_shiftedPt_PhotonEnUp/F')
                type1_pfMet_shiftedPt_TauEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_TauEnUpB = tnew.Branch('type1_pfMet_shiftedPt_TauEnUp', type1_pfMet_shiftedPt_TauEnUp, 'type1_pfMet_shiftedPt_TauEnUp/F')
                type1_pfMet_shiftedPt_TauEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_TauEnDownB = tnew.Branch('type1_pfMet_shiftedPt_TauEnDown', type1_pfMet_shiftedPt_TauEnDown, 'type1_pfMet_shiftedPt_TauEnDown/F')
                type1_pfMet_shiftedPt_UnclusteredEnDown = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_UnclusteredEnDownB = tnew.Branch('type1_pfMet_shiftedPt_UnclusteredEnDown', type1_pfMet_shiftedPt_UnclusteredEnDown, 'type1_pfMet_shiftedPt_UnclusteredEnDown/F')
                type1_pfMet_shiftedPt_UnclusteredEnUp = array('f', [ 0 ] )
                type1_pfMet_shiftedPt_UnclusteredEnUpB = tnew.Branch('type1_pfMet_shiftedPt_UnclusteredEnUp', type1_pfMet_shiftedPt_UnclusteredEnUp, 'type1_pfMet_shiftedPt_UnclusteredEnUp/F')
        
                t1DPhiToPfMet_ElectronEnDown = array('f', [ 0 ] )
                t1DPhiToPfMet_ElectronEnDownB = tnew.Branch('t1DPhiToPfMet_ElectronEnDown', t1DPhiToPfMet_ElectronEnDown, 't1DPhiToPfMet_ElectronEnDown/F')
                t1DPhiToPfMet_ElectronEnUp = array('f', [ 0 ] )
                t1DPhiToPfMet_ElectronEnUpB = tnew.Branch('t1DPhiToPfMet_ElectronEnUp', t1DPhiToPfMet_ElectronEnUp, 't1DPhiToPfMet_ElectronEnUp/F')
                t1DPhiToPfMet_JetEnDown = array('f', [ 0 ] )
                t1DPhiToPfMet_JetEnDownB = tnew.Branch('t1DPhiToPfMet_JetEnDown', t1DPhiToPfMet_JetEnDown, 't1DPhiToPfMet_JetEnDown/F')
                t1DPhiToPfMet_JetEnUp = array('f', [ 0 ] )
                t1DPhiToPfMet_JetEnUpB = tnew.Branch('t1DPhiToPfMet_JetEnUp', t1DPhiToPfMet_JetEnUp, 't1DPhiToPfMet_JetEnUp/F')
                t1DPhiToPfMet_JetResDown = array('f', [ 0 ] )
                t1DPhiToPfMet_JetResDownB = tnew.Branch('t1DPhiToPfMet_JetResDown', t1DPhiToPfMet_JetResDown, 't1DPhiToPfMet_JetResDown/F')
                t1DPhiToPfMet_JetResUp = array('f', [ 0 ] )
                t1DPhiToPfMet_JetResUpB = tnew.Branch('t1DPhiToPfMet_JetResUp', t1DPhiToPfMet_JetResUp, 't1DPhiToPfMet_JetResUp/F')
                t1DPhiToPfMet_MuonEnUp = array('f', [ 0 ] )
                t1DPhiToPfMet_MuonEnUpB = tnew.Branch('t1DPhiToPfMet_MuonEnUp', t1DPhiToPfMet_MuonEnUp, 't1DPhiToPfMet_MuonEnUp/F')
                t1DPhiToPfMet_MuonEnDown = array('f', [ 0 ] )
                t1DPhiToPfMet_MuonEnDownB = tnew.Branch('t1DPhiToPfMet_MuonEnDown', t1DPhiToPfMet_MuonEnDown, 't1DPhiToPfMet_MuonEnDown/F')
                t1DPhiToPfMet_PhotonEnDown = array('f', [ 0 ] )
                t1DPhiToPfMet_PhotonEnDownB = tnew.Branch('t1DPhiToPfMet_PhotonEnDown', t1DPhiToPfMet_PhotonEnDown, 't1DPhiToPfMet_PhotonEnDown/F')
                t1DPhiToPfMet_PhotonEnUp = array('f', [ 0 ] )
                t1DPhiToPfMet_PhotonEnUpB = tnew.Branch('t1DPhiToPfMet_PhotonEnUp', t1DPhiToPfMet_PhotonEnUp, 't1DPhiToPfMet_PhotonEnUp/F')
                t1DPhiToPfMet_TauEnUp = array('f', [ 0 ] )
                t1DPhiToPfMet_TauEnUpB = tnew.Branch('t1DPhiToPfMet_TauEnUp', t1DPhiToPfMet_TauEnUp, 't1DPhiToPfMet_TauEnUp/F')
                t1DPhiToPfMet_TauEnDown = array('f', [ 0 ] )
                t1DPhiToPfMet_TauEnDownB = tnew.Branch('t1DPhiToPfMet_TauEnDown', t1DPhiToPfMet_TauEnDown, 't1DPhiToPfMet_TauEnDown/F')
                t1DPhiToPfMet_UnclusteredEnDown = array('f', [ 0 ] )
                t1DPhiToPfMet_UnclusteredEnDownB = tnew.Branch('t1DPhiToPfMet_UnclusteredEnDown', t1DPhiToPfMet_UnclusteredEnDown, 't1DPhiToPfMet_UnclusteredEnDown/F')
                t1DPhiToPfMet_UnclusteredEnUp = array('f', [ 0 ] )
                t1DPhiToPfMet_UnclusteredEnUpB = tnew.Branch('t1DPhiToPfMet_UnclusteredEnUp', t1DPhiToPfMet_UnclusteredEnUp, 't1DPhiToPfMet_UnclusteredEnUp/F')
                t2DPhiToPfMet_ElectronEnDown = array('f', [ 0 ] )
                t2DPhiToPfMet_ElectronEnDownB = tnew.Branch('t2DPhiToPfMet_ElectronEnDown', t2DPhiToPfMet_ElectronEnDown, 't2DPhiToPfMet_ElectronEnDown/F')
                t2DPhiToPfMet_ElectronEnUp = array('f', [ 0 ] )
                t2DPhiToPfMet_ElectronEnUpB = tnew.Branch('t2DPhiToPfMet_ElectronEnUp', t2DPhiToPfMet_ElectronEnUp, 't2DPhiToPfMet_ElectronEnUp/F')
                t2DPhiToPfMet_JetEnDown = array('f', [ 0 ] )
                t2DPhiToPfMet_JetEnDownB = tnew.Branch('t2DPhiToPfMet_JetEnDown', t2DPhiToPfMet_JetEnDown, 't2DPhiToPfMet_JetEnDown/F')
                t2DPhiToPfMet_JetEnUp = array('f', [ 0 ] )
                t2DPhiToPfMet_JetEnUpB = tnew.Branch('t2DPhiToPfMet_JetEnUp', t2DPhiToPfMet_JetEnUp, 't2DPhiToPfMet_JetEnUp/F')
                t2DPhiToPfMet_JetResDown = array('f', [ 0 ] )
                t2DPhiToPfMet_JetResDownB = tnew.Branch('t2DPhiToPfMet_JetResDown', t2DPhiToPfMet_JetResDown, 't2DPhiToPfMet_JetResDown/F')
                t2DPhiToPfMet_JetResUp = array('f', [ 0 ] )
                t2DPhiToPfMet_JetResUpB = tnew.Branch('t2DPhiToPfMet_JetResUp', t2DPhiToPfMet_JetResUp, 't2DPhiToPfMet_JetResUp/F')
                t2DPhiToPfMet_MuonEnUp = array('f', [ 0 ] )
                t2DPhiToPfMet_MuonEnUpB = tnew.Branch('t2DPhiToPfMet_MuonEnUp', t2DPhiToPfMet_MuonEnUp, 't2DPhiToPfMet_MuonEnUp/F')
                t2DPhiToPfMet_MuonEnDown = array('f', [ 0 ] )
                t2DPhiToPfMet_MuonEnDownB = tnew.Branch('t2DPhiToPfMet_MuonEnDown', t2DPhiToPfMet_MuonEnDown, 't2DPhiToPfMet_MuonEnDown/F')
                t2DPhiToPfMet_PhotonEnDown = array('f', [ 0 ] )
                t2DPhiToPfMet_PhotonEnDownB = tnew.Branch('t2DPhiToPfMet_PhotonEnDown', t2DPhiToPfMet_PhotonEnDown, 't2DPhiToPfMet_PhotonEnDown/F')
                t2DPhiToPfMet_PhotonEnUp = array('f', [ 0 ] )
                t2DPhiToPfMet_PhotonEnUpB = tnew.Branch('t2DPhiToPfMet_PhotonEnUp', t2DPhiToPfMet_PhotonEnUp, 't2DPhiToPfMet_PhotonEnUp/F')
                t2DPhiToPfMet_TauEnUp = array('f', [ 0 ] )
                t2DPhiToPfMet_TauEnUpB = tnew.Branch('t2DPhiToPfMet_TauEnUp', t2DPhiToPfMet_TauEnUp, 't2DPhiToPfMet_TauEnUp/F')
                t2DPhiToPfMet_TauEnDown = array('f', [ 0 ] )
                t2DPhiToPfMet_TauEnDownB = tnew.Branch('t2DPhiToPfMet_TauEnDown', t2DPhiToPfMet_TauEnDown, 't2DPhiToPfMet_TauEnDown/F')
                t2DPhiToPfMet_UnclusteredEnDown = array('f', [ 0 ] )
                t2DPhiToPfMet_UnclusteredEnDownB = tnew.Branch('t2DPhiToPfMet_UnclusteredEnDown', t2DPhiToPfMet_UnclusteredEnDown, 't2DPhiToPfMet_UnclusteredEnDown/F')
                t2DPhiToPfMet_UnclusteredEnUp = array('f', [ 0 ] )
                t2DPhiToPfMet_UnclusteredEnUpB = tnew.Branch('t2DPhiToPfMet_UnclusteredEnUp', t2DPhiToPfMet_UnclusteredEnUp, 't2DPhiToPfMet_UnclusteredEnUp/F')
                t2DPhiToPfMet_Raw = array('f', [ 0 ] )
                t2DPhiToPfMet_RawB = tnew.Branch('t2DPhiToPfMet_Raw', t2DPhiToPfMet_Raw, 't2DPhiToPfMet_Raw/F')
                t1DPhiToPfMet_Raw = array('f', [ 0 ] )
                t1DPhiToPfMet_RawB = tnew.Branch('t1DPhiToPfMet_Raw', t1DPhiToPfMet_Raw, 't1DPhiToPfMet_Raw/F')
        
                t1MtToPfMet_ElectronEnDown = array('f', [ 0 ] )
                t1MtToPfMet_ElectronEnDownB = tnew.Branch('t1MtToPfMet_ElectronEnDown', t1MtToPfMet_ElectronEnDown, 't1MtToPfMet_ElectronEnDown/F')
                t1MtToPfMet_ElectronEnUp = array('f', [ 0 ] )
                t1MtToPfMet_ElectronEnUpB = tnew.Branch('t1MtToPfMet_ElectronEnUp', t1MtToPfMet_ElectronEnUp, 't1MtToPfMet_ElectronEnUp/F')
                t1MtToPfMet_JetEnDown = array('f', [ 0 ] )
                t1MtToPfMet_JetEnDownB = tnew.Branch('t1MtToPfMet_JetEnDown', t1MtToPfMet_JetEnDown, 't1MtToPfMet_JetEnDown/F')
                t1MtToPfMet_JetEnUp = array('f', [ 0 ] )
                t1MtToPfMet_JetEnUpB = tnew.Branch('t1MtToPfMet_JetEnUp', t1MtToPfMet_JetEnUp, 't1MtToPfMet_JetEnUp/F')
                t1MtToPfMet_JetResDown = array('f', [ 0 ] )
                t1MtToPfMet_JetResDownB = tnew.Branch('t1MtToPfMet_JetResDown', t1MtToPfMet_JetResDown, 't1MtToPfMet_JetResDown/F')
                t1MtToPfMet_JetResUp = array('f', [ 0 ] )
                t1MtToPfMet_JetResUpB = tnew.Branch('t1MtToPfMet_JetResUp', t1MtToPfMet_JetResUp, 't1MtToPfMet_JetResUp/F')
                t1MtToPfMet_MuonEnUp = array('f', [ 0 ] )
                t1MtToPfMet_MuonEnUpB = tnew.Branch('t1MtToPfMet_MuonEnUp', t1MtToPfMet_MuonEnUp, 't1MtToPfMet_MuonEnUp/F')
                t1MtToPfMet_MuonEnDown = array('f', [ 0 ] )
                t1MtToPfMet_MuonEnDownB = tnew.Branch('t1MtToPfMet_MuonEnDown', t1MtToPfMet_MuonEnDown, 't1MtToPfMet_MuonEnDown/F')
                t1MtToPfMet_PhotonEnDown = array('f', [ 0 ] )
                t1MtToPfMet_PhotonEnDownB = tnew.Branch('t1MtToPfMet_PhotonEnDown', t1MtToPfMet_PhotonEnDown, 't1MtToPfMet_PhotonEnDown/F')
                t1MtToPfMet_PhotonEnUp = array('f', [ 0 ] )
                t1MtToPfMet_PhotonEnUpB = tnew.Branch('t1MtToPfMet_PhotonEnUp', t1MtToPfMet_PhotonEnUp, 't1MtToPfMet_PhotonEnUp/F')
                t1MtToPfMet_TauEnUp = array('f', [ 0 ] )
                t1MtToPfMet_TauEnUpB = tnew.Branch('t1MtToPfMet_TauEnUp', t1MtToPfMet_TauEnUp, 't1MtToPfMet_TauEnUp/F')
                t1MtToPfMet_TauEnDown = array('f', [ 0 ] )
                t1MtToPfMet_TauEnDownB = tnew.Branch('t1MtToPfMet_TauEnDown', t1MtToPfMet_TauEnDown, 't1MtToPfMet_TauEnDown/F')
                t1MtToPfMet_UnclusteredEnDown = array('f', [ 0 ] )
                t1MtToPfMet_UnclusteredEnDownB = tnew.Branch('t1MtToPfMet_UnclusteredEnDown', t1MtToPfMet_UnclusteredEnDown, 't1MtToPfMet_UnclusteredEnDown/F')
                t1MtToPfMet_UnclusteredEnUp = array('f', [ 0 ] )
                t1MtToPfMet_UnclusteredEnUpB = tnew.Branch('t1MtToPfMet_UnclusteredEnUp', t1MtToPfMet_UnclusteredEnUp, 't1MtToPfMet_UnclusteredEnUp/F')
                t2MtToPfMet_ElectronEnDown = array('f', [ 0 ] )
                t2MtToPfMet_ElectronEnDownB = tnew.Branch('t2MtToPfMet_ElectronEnDown', t2MtToPfMet_ElectronEnDown, 't2MtToPfMet_ElectronEnDown/F')
                t2MtToPfMet_ElectronEnUp = array('f', [ 0 ] )
                t2MtToPfMet_ElectronEnUpB = tnew.Branch('t2MtToPfMet_ElectronEnUp', t2MtToPfMet_ElectronEnUp, 't2MtToPfMet_ElectronEnUp/F')
                t2MtToPfMet_JetEnDown = array('f', [ 0 ] )
                t2MtToPfMet_JetEnDownB = tnew.Branch('t2MtToPfMet_JetEnDown', t2MtToPfMet_JetEnDown, 't2MtToPfMet_JetEnDown/F')
                t2MtToPfMet_JetEnUp = array('f', [ 0 ] )
                t2MtToPfMet_JetEnUpB = tnew.Branch('t2MtToPfMet_JetEnUp', t2MtToPfMet_JetEnUp, 't2MtToPfMet_JetEnUp/F')
                t2MtToPfMet_JetResDown = array('f', [ 0 ] )
                t2MtToPfMet_JetResDownB = tnew.Branch('t2MtToPfMet_JetResDown', t2MtToPfMet_JetResDown, 't2MtToPfMet_JetResDown/F')
                t2MtToPfMet_JetResUp = array('f', [ 0 ] )
                t2MtToPfMet_JetResUpB = tnew.Branch('t2MtToPfMet_JetResUp', t2MtToPfMet_JetResUp, 't2MtToPfMet_JetResUp/F')
                t2MtToPfMet_MuonEnUp = array('f', [ 0 ] )
                t2MtToPfMet_MuonEnUpB = tnew.Branch('t2MtToPfMet_MuonEnUp', t2MtToPfMet_MuonEnUp, 't2MtToPfMet_MuonEnUp/F')
                t2MtToPfMet_MuonEnDown = array('f', [ 0 ] )
                t2MtToPfMet_MuonEnDownB = tnew.Branch('t2MtToPfMet_MuonEnDown', t2MtToPfMet_MuonEnDown, 't2MtToPfMet_MuonEnDown/F')
                t2MtToPfMet_PhotonEnDown = array('f', [ 0 ] )
                t2MtToPfMet_PhotonEnDownB = tnew.Branch('t2MtToPfMet_PhotonEnDown', t2MtToPfMet_PhotonEnDown, 't2MtToPfMet_PhotonEnDown/F')
                t2MtToPfMet_PhotonEnUp = array('f', [ 0 ] )
                t2MtToPfMet_PhotonEnUpB = tnew.Branch('t2MtToPfMet_PhotonEnUp', t2MtToPfMet_PhotonEnUp, 't2MtToPfMet_PhotonEnUp/F')
                t2MtToPfMet_TauEnUp = array('f', [ 0 ] )
                t2MtToPfMet_TauEnUpB = tnew.Branch('t2MtToPfMet_TauEnUp', t2MtToPfMet_TauEnUp, 't2MtToPfMet_TauEnUp/F')
                t2MtToPfMet_TauEnDown = array('f', [ 0 ] )
                t2MtToPfMet_TauEnDownB = tnew.Branch('t2MtToPfMet_TauEnDown', t2MtToPfMet_TauEnDown, 't2MtToPfMet_TauEnDown/F')
                t2MtToPfMet_UnclusteredEnDown = array('f', [ 0 ] )
                t2MtToPfMet_UnclusteredEnDownB = tnew.Branch('t2MtToPfMet_UnclusteredEnDown', t2MtToPfMet_UnclusteredEnDown, 't2MtToPfMet_UnclusteredEnDown/F')
                t2MtToPfMet_UnclusteredEnUp = array('f', [ 0 ] )
                t2MtToPfMet_UnclusteredEnUpB = tnew.Branch('t2MtToPfMet_UnclusteredEnUp', t2MtToPfMet_UnclusteredEnUp, 't2MtToPfMet_UnclusteredEnUp/F')
                t2MtToPfMet_type1 = array('f', [ 0 ] )
                t2MtToPfMet_type1B = tnew.Branch('t2MtToPfMet_type1', t2MtToPfMet_type1, 't2MtToPfMet_type1/F')
                t1MtToPfMet_type1 = array('f', [ 0 ] )
                t1MtToPfMet_type1B = tnew.Branch('t1MtToPfMet_type1', t1MtToPfMet_type1, 't1MtToPfMet_type1/F')
        
                t1MatchesEle24Tau20L1Filter = array('f', [ 0 ] )
                t1MatchesEle24Tau20L1FilterB = tnew.Branch('t1MatchesEle24Tau20L1Filter', t1MatchesEle24Tau20L1Filter, 't1MatchesEle24Tau20L1Filter/F')
                t2MatchesEle24Tau20L1Filter = array('f', [ 0 ] )
                t2MatchesEle24Tau20L1FilterB = tnew.Branch('t2MatchesEle24Tau20L1Filter', t2MatchesEle24Tau20L1Filter, 't2MatchesEle24Tau20L1Filter/F')
        
                
                raw_pfMetEt = array('f', [ 0 ] )
                raw_pfMetEtB = tnew.Branch('raw_pfMetEt', raw_pfMetEt, 'raw_pfMetEt/F')
                raw_pfMetPhi = array('f', [ 0 ] )
                raw_pfMetPhiB = tnew.Branch('raw_pfMetPhi', raw_pfMetPhi, 'raw_pfMetPhi/F')
        run = int( row.run )
        lumi = int( row.lumi )
        evt = int( row.evt )
        if evt < 0 :
            print "\n\n\n BIG \n\n TROUBLE \n\n EVT: %i   Sample: %s \n\n\n\n" % (evt, sample)
        
        currentEvt = getCurrentEvt( analysis, channel, row )
        currentRunLumiEvt = (run, lumi, evt)

        
        if currentRunLumiEvt in toFillMap.keys() and currentEvt == toFillMap[ currentRunLumiEvt ] :
            #print "Fill choice:",currentRunLumiEvt, currentEvt

            # This iso ordering is for the final selected permutation
            # of a given event, it just changes flips t1 vs t2
            # the actual permutation is selected elsewhere.
            # For SM-HTT 2016, we pt order the final selected taus.
            #if channel == 'tt' : #and 'Sync-' in sample : 
            #    #print "### Iso Ordering %s ###" % sample
            #    isoOrder( channel, row )
            vbfClean( row, analysis )


            # For easy use later
            pt1 = getattr( row, l1+'Pt' )
            phi1 = getattr( row, l1+'Phi' )
            eta1 = getattr( row, l1+'Eta' )
            m1 = getattr( row, l1+'Mass' )
            pt2 = getattr( row, l2+'Pt' )
            phi2 = getattr( row, l2+'Phi' )
            eta2 = getattr( row, l2+'Eta' )
            m2 = getattr( row, l2+'Mass' )
            if channel == 'tt' :
                dm1 = getattr( row, l1+'DecayMode' )
                dm2 = getattr( row, l2+'DecayMode' )
            if len( channel ) > 2 :
                pt3 = getattr( row, l3+'Pt' )
                phi3 = getattr( row, l3+'Phi' )
                eta3 = getattr( row, l3+'Eta' )
                m3 = getattr( row, l3+'Mass' )
            if len( channel ) > 3 :
                pt4 = getattr( row, l4+'Pt' )
                phi4 = getattr( row, l4+'Phi' )
                eta4 = getattr( row, l4+'Eta' )
                m4 = getattr( row, l4+'Mass' )

            Z_DEta[0] = (eta1 - eta2)


            # Channel specific vetoes
            if channel == 'tt' :
                extramuon_veto[0] = getattr( row, "muVetoZTTp001dxyzR0" )
                extraelec_veto[0] = getattr( row, "eVetoZTTp001dxyzR0" )
                if extramuon_veto[0] > 1 : extramuon_veto[0] = 1
                if extraelec_veto[0] > 1 : extraelec_veto[0] = 1
            if channel == 'em' :
                extramuon_veto[0] = getattr( row, "muVetoZTTp001dxyz" )
                extraelec_veto[0] = getattr( row, "eVetoZTTp001dxyz" )
                if extramuon_veto[0] > 1 : extramuon_veto[0] = 1
                if extraelec_veto[0] > 1 : extraelec_veto[0] = 1
            if channel == 'et' :
                extramuon_veto[0] = getattr( row, "muVetoZTTp001dxyzR0" )
                extraelec_veto[0] = getattr( row, "eVetoZTTp001dxyz" )
            if channel == 'mt' :
                extramuon_veto[0] = getattr( row, "muVetoZTTp001dxyz" )
                extraelec_veto[0] = getattr( row, "eVetoZTTp001dxyzR0" )


            
            #if hasattr( row, "%s_%s_MvaMet" % (l1, l2) ):
            #    mvacov00[0] = getattr( row, "%s_%s_MvaMetCovMatrix00" % (l1, l2) )
            #    mvacov01[0] = getattr( row, "%s_%s_MvaMetCovMatrix01" % (l1, l2) )
            #    mvacov10[0] = getattr( row, "%s_%s_MvaMetCovMatrix10" % (l1, l2) )
            #    mvacov11[0] = getattr( row, "%s_%s_MvaMetCovMatrix11" % (l1, l2) )
            #    mvamet[0] = getattr( row, "%s_%s_MvaMet" % (l1, l2) )
            #    mvametphi[0] = getattr( row, "%s_%s_MvaMetPhi" % (l1, l2) )
            #    mt_1[0]= getTransMass( mvamet[0], mvametphi[0], pt1, phi1 )
            #    mt_2[0]= getTransMass( mvamet[0], mvametphi[0], pt2, phi2 )
            #    pzetamiss[0] = compZeta(pt1, phi1, pt2, phi2, mvamet[0], mvametphi[0])[1]
            #    if hasattr( row, '%s_%s_PZetaVis' % (l1, l2) ) :
            #        pzeta[0] = pzetamiss[0] - 0.85 * getattr( row, '%s_%s_PZetaVis' % (l1, l2) )
            #    Higgs_Pt[0] = getHiggsPt( pt1, eta1, phi1, m1,\
            #             pt2, eta2, phi2, m2, mvamet[0], mvametphi[0])
            #else : # Not l1_l2_MvaMet
            #mt_1[0] = getattr( row, l1+'MtToPfMet_type1' )
            #mt_2[0] = getattr( row, l2+'MtToPfMet_type1' )
            Higgs_Pt[0] = getHiggsPt( pt1, eta1, phi1, m1,\
                    pt2, eta2, phi2, m2, row.type1_pfMetEt, row.type1_pfMetPhi)




            # With calculated transverse mass variables, do Mt_Total for mssm search
            #mt_tot[0] = calcMTTotal( pt1, phi1, pt2, phi2, mt_1[0], mt_2[0] )
            # TES Shifted
            if 'DYJets' in sample or 'ggH' in sample or 'bbH' in sample or 'VBH' in sample or 'Sync' in sample :
                m_vis_UP[0] = mVisTES( l1, l2, row, 0.03 )
                m_vis_DOWN[0] = mVisTES( l1, l2, row, -0.03 )
                #mt_tot_UP[0] = getMTTotal( pt1, phi1, pt2, phi2, row, channel, True )
                #mt_tot_DOWN[0] = getMTTotal( pt1, phi1, pt2, phi2, row, channel, False )
            else :
                m_vis_UP[0] = getattr( row, '%s_%s_Mass' % (l1, l2) )
                m_vis_DOWN[0] = getattr( row, '%s_%s_Mass' % (l1, l2) )
                if hasattr( row, 'm_sv_UP' ) :
                    setattr( row, 'm_sv_UP', getattr( row, 'm_sv' ) )
                    setattr( row, 'm_sv_DOWN', getattr( row, 'm_sv' ) )
                    setattr( row, 'mt_sv_UP', getattr( row, 'mt_sv' ) )
                    setattr( row, 'mt_sv_DOWN', getattr( row, 'mt_sv' ) )
                #mt_tot_UP[0] = mt_tot[0]
                #mt_tot_DOWN[0] = mt_tot[0]
            #print "Mt Tot: %f         Mt Tot Up: %f         Mt Tot Down: %f" % (mt_tot[0], mt_tot_UP[0], mt_tot_DOWN[0])




            muonSF1[0] = 1
            muonSF2[0] = 1
            muonSF3[0] = 1
            muonSF4[0] = 1
            electronSF1[0] = 1
            electronSF2[0] = 1
            electronSF3[0] = 1
            electronSF4[0] = 1
            azhWeight[0] = 1
            puweight[0] = 1
            qqZZ4lWeight[0] = 1
            tauPtWeightUp[0] = 1
            tauPtWeightDown[0] = 1
            trigweight_1[0] = 1
            trigweight_2[0] = 1
            idisoweight_1[0] = 1
            idisoweight_2[0] = 1
            tauIDweight_1[0] = 1
            tauIDweight_2[0] = 1
            topWeight[0] = 1
            zPtWeight[0] = 1
            zmumuVBFWeight[0] = 1
            ggHWeight0Jet[0] = 1
            ggHWeightBoost[0] = 1
            ggHWeightVBF[0] = 1
            jetToTauFakeWeight[0] = 1
            weight[0] = 1
            XSecLumiWeight[0] = 1
            gen_match_1[0] = -1
            gen_match_2[0] = -1
            gen_match_3[0] = -1
            gen_match_4[0] = -1
            byVVTightIsolationMVArun2v1DBoldDMwLT_1[0] = -1
            byVVTightIsolationMVArun2v1DBoldDMwLT_2[0] = -1
            byVVLooseIsolationMVArun2v1DBoldDMwLT_1[0] = -1
            byVVLooseIsolationMVArun2v1DBoldDMwLT_2[0] = -1
            byVVLooseIsolationMVArun2v1DBoldDMwLT_3[0] = -1
            byVVLooseIsolationMVArun2v1DBoldDMwLT_4[0] = -1
            isoCode1[0] = -1
            isoCode2[0] = -1
            pt_1_UP[0] = pt1
            pt_1_DOWN[0] = pt1
            pt_1_DM0_UP[0] = pt1
            pt_1_DM0_DOWN[0] = pt1
            pt_1_DM1_UP[0] = pt1
            pt_1_DM1_DOWN[0] = pt1
            pt_1_DM10_UP[0] = pt1
            pt_1_DM10_DOWN[0] = pt1
            pt_2_UP[0] = pt2
            pt_2_DOWN[0] = pt2
            pt_2_DM0_UP[0] = pt2
            pt_2_DM0_DOWN[0] = pt2
            pt_2_DM1_UP[0] = pt2
            pt_2_DM1_DOWN[0] = pt2
            pt_2_DM10_UP[0] = pt2
            pt_2_DM10_DOWN[0] = pt2
            ptCor_1[0] = pt1
            ptCor_2[0] = pt2
            Higgs_PtCor[0] = Higgs_Pt[0]
            Higgs_PtCor_UP[0] = Higgs_Pt[0]
            Higgs_PtCor_DM0_UP[0] = Higgs_Pt[0]
            Higgs_PtCor_DM1_UP[0] = Higgs_Pt[0]
            Higgs_PtCor_DM10_UP[0] = Higgs_Pt[0]
            Higgs_PtCor_UncMet_UP[0] = Higgs_Pt[0]
            Higgs_PtCor_ClusteredMet_UP[0] = Higgs_Pt[0]
            Higgs_PtCor_DOWN[0] = Higgs_Pt[0]
            Higgs_PtCor_DM0_DOWN[0] = Higgs_Pt[0]
            Higgs_PtCor_DM1_DOWN[0] = Higgs_Pt[0]
            Higgs_PtCor_DM10_DOWN[0] = Higgs_Pt[0]
            Higgs_PtCor_UncMet_DOWN[0] = Higgs_Pt[0]
            Higgs_PtCor_ClusteredMet_DOWN[0] = Higgs_Pt[0]
            m_visCor[0] = getattr( row, l1+'_'+l2+'_Mass' )
            m_visCor_UP[0] = m_visCor[0]
            m_visCor_DM0_UP[0] = m_visCor[0]
            m_visCor_DM1_UP[0] = m_visCor[0]
            m_visCor_DM10_UP[0] = m_visCor[0]
            m_visCor_DOWN[0] = m_visCor[0]
            m_visCor_DM0_DOWN[0] = m_visCor[0]
            m_visCor_DM1_DOWN[0] = m_visCor[0]
            m_visCor_DM10_DOWN[0] = m_visCor[0]
            zhFR0[0] = 0
            zhFR1[0] = 0
            zhFR2[0] = 0
            LT_higgs[0] = 0

            # Data specific vars
            if 'data' in sample :
                # Have the btag numbers correspond to actual values not
                # Promote/Demote values
                if hasattr(row, 'NBTagPDM_idL_jVeto' ) :
                    setattr(row, 'NBTagPDM_idL_jVeto', getattr(row, 'bjetCISVVeto20MediumZTT'))
                if hasattr(row, 'NBTagPDL_idL_jVeto' ) :
                    setattr(row, 'NBTagPDL_idL_jVeto', getattr(row, 'bjetCISVVeto20LooseZTT'))


                    
            ### Not Data
            else :
                nTrPu = ( math.floor(row.nTruePU * 10))/10
                puweight[0] = puDict[ nTrPu ]

                if hasattr( row, l1+'ZTTGenMatching2' ) : # GenMatching2 is best var
                    gen_match_1[0] = getattr( row, l1+'ZTTGenMatching2' )
                elif hasattr( row, l1+'ZTTGenMatching' ) :
                    gen_match_1[0] = getattr( row, l1+'ZTTGenMatching' )
                if hasattr( row, l2+'ZTTGenMatching2' ) : # GenMatching2 is best var
                    gen_match_2[0] = getattr( row, l2+'ZTTGenMatching2' )
                elif hasattr( row, l2+'ZTTGenMatching' ) :
                    gen_match_2[0] = getattr( row, l2+'ZTTGenMatching' )


                if analysis == 'azh' :

                    if 'ZZ4l' in sample :
                        qqZZ4lWeight[0] = qqZZ4l_nnlo_weight( row.genM, \
                                row.isZee, row.isZmumu, row.isZtautau )

                    if hasattr( row, l3+'ZTTGenMatching2' ) : # GenMatching2 is best var
                        gen_match_3[0] = getattr( row, l3+'ZTTGenMatching2' )
                    elif hasattr( row, l3+'ZTTGenMatching' ) :
                        gen_match_3[0] = getattr( row, l3+'ZTTGenMatching' )
                    if hasattr( row, l4+'ZTTGenMatching2' ) : # GenMatching2 is best var
                        gen_match_4[0] = getattr( row, l4+'ZTTGenMatching2' )
                    elif hasattr( row, l4+'ZTTGenMatching' ) :
                        gen_match_4[0] = getattr( row, l4+'ZTTGenMatching' )

                    nvtx = row.nvtx
                    # Currently using PFIDLoose and Loose RelIso for all muons
                    
                    if 'm' in l1 :
                        muonSF1[0] = muonSF.getIDScaleFactor( 'Loose', pt1, eta1, nvtx )
                        muonSF1[0] *= muonSF.getRelIsoScaleFactor( 'Loose', pt1, eta1, nvtx )
                        muonSF1[0] *= muonSF.getTkScaleFactor( eta1, nvtx )
                    if 'm' in l2 :
                        muonSF2[0] = muonSF.getIDScaleFactor( 'Loose', pt2, eta2, nvtx )
                        muonSF2[0] *= muonSF.getRelIsoScaleFactor( 'Loose', pt2, eta2, nvtx )
                        muonSF2[0] *= muonSF.getTkScaleFactor( eta2, nvtx )
                    if 'm' in l3 :
                        muonSF3[0] = muonSF.getIDScaleFactor( 'Loose', pt3, eta3, nvtx )
                        muonSF3[0] *= muonSF.getRelIsoScaleFactor( 'Loose', pt3, eta3, nvtx )
                        muonSF3[0] *= muonSF.getTkScaleFactor( eta3, nvtx )
                    if 'm' in l4 :
                        muonSF4[0] = muonSF.getIDScaleFactor( 'Loose', pt4, eta4, nvtx )
                        muonSF4[0] *= muonSF.getRelIsoScaleFactor( 'Loose', pt4, eta4, nvtx )
                        muonSF4[0] *= muonSF.getTkScaleFactor( eta4, nvtx )
                    # Currently using WP90 in all electrons
                    if 'e' in l1 :
                        electronSF1[0] = electronSF.getGSFAndWPScaleFactor( 'WP90', pt1, eta1 )
                    if 'e' in l2 :
                        electronSF2[0] = electronSF.getGSFAndWPScaleFactor( 'WP90', pt2, eta2 )
                    if 'e' in l3 :
                        electronSF3[0] = electronSF.getGSFAndWPScaleFactor( 'WP90', pt3, eta3 )
                    if 'e' in l4 :
                        electronSF4[0] = electronSF.getGSFAndWPScaleFactor( 'WP90', pt4, eta4 )


                # Isolation / ID weights
                if 't' in l1 : idisoweight_1[0] = 1
                #else : idisoweight_1[0] = lepWeights.getWeight( l1, 'IdIso', pt1, eta1 )
                if 't' in l2 : idisoweight_2[0] = 1
                #else : idisoweight_2[0] = lepWeights.getWeight( l2, 'IdIso', pt2, eta2 )

                # Trigger Weights
                #if channel == 'et' : trigweight_1[0] = lepWeights.getWeight( l1, 'Trig', pt1, eta1 )
                #elif channel == 'mt' : trigweight_1[0] = lepWeights.getWeight( l1, 'Trig', pt1, eta1 )
                #elif channel == 'em' : trigweight_1[0] = lepWeights.getEMTrigWeight( pt1, eta1, pt2, eta2 )
                #elif channel == 'tt' :
                if channel == 'tt' :

                    # L1 trigger efficiency is dependent on tau isolation
                    # and real / fake tau status
                    # find tau iso and pass string for mapping appropriately
                    tauIso = 'NoIso'
                    if getattr( row, l1+'ByVLooseIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'VLooseIso'
                    if getattr( row, l1+'ByLooseIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'LooseIso'
                    if getattr( row, l1+'ByMediumIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'MediumIso'
                    if getattr( row, l1+'ByTightIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'TightIso'
                    if getattr( row, l1+'ByVTightIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'VTightIso'
                    if analysis == 'Sync' and 'DYJets' not in sample : tauIso == 'TightIso'
                    trigweight_1[0] = doublTau35.doubleTauTriggerEff( pt1, tauIso, gen_match_1[0], dm1 )
                    tauIso = 'NoIso'
                    if getattr( row, l2+'ByVLooseIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'VLooseIso'
                    if getattr( row, l2+'ByLooseIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'LooseIso'
                    if getattr( row, l2+'ByMediumIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'MediumIso'
                    if getattr( row, l2+'ByTightIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'TightIso'
                    if getattr( row, l2+'ByVTightIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'VTightIso'
                    if analysis == 'Sync' and 'DYJets' not in sample : tauIso == 'TightIso'
                    trigweight_2[0] = doublTau35.doubleTauTriggerEff( pt2, tauIso, gen_match_2[0], dm2 )


                    # Tau Energy Correction
                    # also propagated to Higgs_Pt and m_vis
                    ptCor_1[0] = correctTauPt( pt1, gen_match_1[0], dm1 )
                    ptCor_2[0] = correctTauPt( pt2, gen_match_2[0], dm2 )
                    pt_1_UP[0] = ptCor_1[0]
                    pt_1_DOWN[0] = ptCor_1[0]
                    pt_1_DM0_UP[0] = ptCor_1[0]
                    pt_1_DM0_DOWN[0] = ptCor_1[0]
                    pt_1_DM1_UP[0] = ptCor_1[0]
                    pt_1_DM1_DOWN[0] = ptCor_1[0]
                    pt_1_DM10_UP[0] = ptCor_1[0]
                    pt_1_DM10_DOWN[0] = ptCor_1[0]
                    pt_2_UP[0] = ptCor_2[0]
                    pt_2_DOWN[0] = ptCor_2[0]
                    pt_2_DM0_UP[0] = ptCor_2[0]
                    pt_2_DM0_DOWN[0] = ptCor_2[0]
                    pt_2_DM1_UP[0] = ptCor_2[0]
                    pt_2_DM1_DOWN[0] = ptCor_2[0]
                    pt_2_DM10_UP[0] = ptCor_2[0]
                    pt_2_DM10_DOWN[0] = ptCor_2[0]
                    # Tau Energy Scale Saved
                    # 15 Feb 2017, TES uncertainty == 0.6%
                    # TES used to be 3% with no central shift
                    tesUp = 1.012
                    tesDown = 0.988
                    if gen_match_1[0] == 5 :
                        tauIDweight_1[0] = 0.95 # 06 Feb 2017
                        pt_1_UP[0] = ptCor_1[0] * tesUp
                        pt_1_DOWN[0] = ptCor_1[0] * tesDown
                        # For the combinatorics
                        if dm1 == 0 :
                            pt_1_DM0_UP[0] = ptCor_1[0] * tesUp
                            pt_1_DM0_DOWN[0] = ptCor_1[0] * tesDown
                        if dm1 == 1 :
                            pt_1_DM1_UP[0] = ptCor_1[0] * tesUp
                            pt_1_DM1_DOWN[0] = ptCor_1[0] * tesDown
                        if dm1 == 10 :
                            pt_1_DM10_UP[0] = ptCor_1[0] * tesUp
                            pt_1_DM10_DOWN[0] = ptCor_1[0] * tesDown
                    if gen_match_2[0] == 5 :
                        tauIDweight_2[0] = 0.95 # 06 Feb 2017
                        pt_2_UP[0] = ptCor_2[0] * tesUp
                        pt_2_DOWN[0] = ptCor_2[0] * tesDown
                        if dm2 == 0 :
                            pt_2_DM0_UP[0] = ptCor_2[0] * tesUp
                            pt_2_DM0_DOWN[0] = ptCor_2[0] * tesDown
                        if dm2 == 1 :
                            pt_2_DM1_UP[0] = ptCor_2[0] * tesUp
                            pt_2_DM1_DOWN[0] = ptCor_2[0] * tesDown
                        if dm2 == 10 :
                            pt_2_DM10_UP[0] = ptCor_2[0] * tesUp
                            pt_2_DM10_DOWN[0] = ptCor_2[0] * tesDown

                    # All shifts for Higgs_Pt with combinatorics
                    # This should use recoil corrected, TEC MET from svFit if available
                    if hasattr( row, 'metcor' ) : metTmp = row.metcor
                    else : metTmp = row.type1_pfMetEt
                    if hasattr( row, 'metcorphi' ) : metPhiTmp = row.metcorphi
                    else : metPhiTmp = row.type1_pfMetPhi
                    Higgs_PtCor[0] = getHiggsPt( ptCor_1[0], eta1, phi1, m1,\
                        ptCor_2[0], eta2, phi2, m2, metTmp, metPhiTmp)
                    Higgs_PtCor_UP[0] = getHiggsPt( pt_1_UP[0], eta1, phi1, m1,\
                        pt_2_UP[0], eta2, phi2, m2, metTmp, metPhiTmp)
                    Higgs_PtCor_DM0_UP[0] = getHiggsPt( pt_1_DM0_UP[0], eta1, phi1, m1,\
                        pt_2_DM0_UP[0], eta2, phi2, m2, metTmp, metPhiTmp)
                    Higgs_PtCor_DM1_UP[0] = getHiggsPt( pt_1_DM1_UP[0], eta1, phi1, m1,\
                        pt_2_DM1_UP[0], eta2, phi2, m2, metTmp, metPhiTmp)
                    Higgs_PtCor_DM10_UP[0] = getHiggsPt( pt_1_DM10_UP[0], eta1, phi1, m1,\
                        pt_2_DM10_UP[0], eta2, phi2, m2, metTmp, metPhiTmp)
                    Higgs_PtCor_DOWN[0] = getHiggsPt( pt_1_DOWN[0], eta1, phi1, m1,\
                        pt_2_DOWN[0], eta2, phi2, m2, metTmp, metPhiTmp)
                    Higgs_PtCor_DM0_DOWN[0] = getHiggsPt( pt_1_DM0_DOWN[0], eta1, phi1, m1,\
                        pt_2_DM0_DOWN[0], eta2, phi2, m2, metTmp, metPhiTmp)
                    Higgs_PtCor_DM1_DOWN[0] = getHiggsPt( pt_1_DM1_DOWN[0], eta1, phi1, m1,\
                        pt_2_DM1_DOWN[0], eta2, phi2, m2, metTmp, metPhiTmp)
                    Higgs_PtCor_DM10_DOWN[0] = getHiggsPt( pt_1_DM10_DOWN[0], eta1, phi1, m1,\
                        pt_2_DM10_DOWN[0], eta2, phi2, m2, metTmp, metPhiTmp)
                    # For the met shifted Higgs Pt, check 1 hasattr
                    if hasattr( row, 'metcorClusteredUp' ) :
                        Higgs_PtCor_UncMet_UP[0] = getHiggsPt( ptCor_1[0], eta1, phi1, m1,\
                            ptCor_2[0], eta2, phi2, m2, row.metcorUncUp, row.metcorphiUncUp)
                        Higgs_PtCor_UncMet_DOWN[0] = getHiggsPt( ptCor_1[0], eta1, phi1, m1,\
                            ptCor_2[0], eta2, phi2, m2, row.metcorUncDown, row.metcorphiUncDown)
                        Higgs_PtCor_ClusteredMet_UP[0] = getHiggsPt( ptCor_1[0], eta1, phi1, m1,\
                            ptCor_2[0], eta2, phi2, m2, row.metcorClusteredUp, row.metcorphiClusteredUp)
                        Higgs_PtCor_ClusteredMet_DOWN[0] = getHiggsPt( ptCor_1[0], eta1, phi1, m1,\
                            ptCor_2[0], eta2, phi2, m2, row.metcorClusteredDown, row.metcorphiClusteredDown)
                    

                    m_visCor[0] = mVisTESCor( l1, l2, row, ptCor_1[0], ptCor_2[0] )
                    m_visCor_UP[0] = mVisTESCor( l1, l2, row, pt_1_UP[0], pt_2_UP[0] )
                    m_visCor_DM0_UP[0] = mVisTESCor( l1, l2, row, pt_1_DM0_UP[0], pt_2_DM0_UP[0] )
                    m_visCor_DM1_UP[0] = mVisTESCor( l1, l2, row, pt_1_DM1_UP[0], pt_2_DM1_UP[0] )
                    m_visCor_DM10_UP[0] = mVisTESCor( l1, l2, row, pt_1_DM10_UP[0], pt_2_DM10_UP[0] )
                    m_visCor_DOWN[0] = mVisTESCor( l1, l2, row, pt_1_DOWN[0], pt_2_DOWN[0] )
                    m_visCor_DM0_DOWN[0] = mVisTESCor( l1, l2, row, pt_1_DM0_DOWN[0], pt_2_DM0_DOWN[0] )
                    m_visCor_DM1_DOWN[0] = mVisTESCor( l1, l2, row, pt_1_DM1_DOWN[0], pt_2_DM1_DOWN[0] )
                    m_visCor_DM10_DOWN[0] = mVisTESCor( l1, l2, row, pt_1_DM10_DOWN[0], pt_2_DM10_DOWN[0] )



                # ggH reweighting, only for ggH120,125,130
                # estimated by Cecile, Nov 15, 2016
                # See: https://indico.cern.ch/event/578552/contributions/2343738/attachments/1372271/2081852/systematics_SMH.pdf
                # Slide 10 for tautau
                if shortName in ['ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] :

                    ggHWeight0Jet[0] = 0.814 + 0.0027094 * row.t1Pt
                    # 2 options for boosted category in case we haven't run svFit
                    # prefer the svFit option
                    if hasattr( row, 'pt_sv' ) :
                        ggHWeightBoost[0] = 0.973 + 0.0008596 * row.pt_sv
                    elif Higgs_Pt[0] != 0.0 :
                        ggHWeightBoost[0] = 0.973 + 0.0008596 * Higgs_Pt[0]

                    if hasattr( row, 'vbfMass' ) :
                        ggHWeightVBF[0] = 1.094 + 0.0000545 * row.vbfMass

                
                # top pt reweighting, only for ttbar events
                # https://twiki.cern.ch/twiki/bin/view/CMS/MSSMAHTauTauEarlyRun2#Top_quark_pT_reweighting
                if shortName == 'TT' and hasattr( row, 'topQuarkPt1' ) :
                    top1Pt = row.topQuarkPt1 if row.topQuarkPt1 < 400 else 400
                    top2Pt = row.topQuarkPt2 if row.topQuarkPt2 < 400 else 400
                    topWeight[0] = math.sqrt(math.exp(0.156-0.00137*top1Pt)*math.exp(0.156-0.00137*top2Pt))
                else : topWeight[0] = 1
                #topWeight[0] = 1

                # genMass is a default from FSA, that doesn't conform to HTT genMass
                if hasattr( row, 'genMass' ) and hasattr( row, 'genM' ) :
                    setattr( row, 'genMass', getattr( row, 'genM' ))

                # Apply z Pt Reweighting to LO DYJets samples
                # https://twiki.cern.ch/twiki/bin/view/CMS/MSSMAHTauTauEarlyRun2#Z_reweighting
                if 'DYJets' in sample and 'Low' not in sample :
                    if hasattr( row, 'genM' ) and hasattr( row, 'genpT' ) :
                        zPtWeight[0] = zPtWeighter.getZPtReweight( row.genM, row.genpT )

                # Reweighting 2D distributions based on Zmumu CR
                if 'DYJets' in sample or 'EWKZ' in sample :

                    # VBF Category
                    # Change application method and add shape with nominal
                    # shift at 1/2 the initial value
                    # Update 2 Mar 2017, no more shape uncert, just weight correction
                    if row.vbfMass <= 300   : zmumuVBFWeight[0] = 0.0
                    elif row.vbfMass <= 500 : zmumuVBFWeight[0] = 0.02
                    elif row.vbfMass <= 800 : zmumuVBFWeight[0] = 0.06
                    else                    : zmumuVBFWeight[0] = 0.04 # > 800

                # Jet to Tau Fake weight
                if not 'date' in sample :
                    w1 = 0.
                    w2 = 0.
                    if gen_match_1[0] == 6 :
                        w1 = .2 * pt1 / 100.
                    if gen_match_2[0] == 6 :
                        w2 = .2 * pt2 / 100.
                    if w1 > .4 : w1 = .4
                    if w2 > .4 : w2 = .4
                    jetToTauFakeWeight[0] = 1. + w1 + w2
                    

                weight[0] = puweight[0] * idisoweight_1[0] * idisoweight_2[0]
                weight[0] *= trigweight_1[0] * trigweight_2[0]
                weight[0] *= zPtWeight[0] * topWeight[0]
                # Below set to 1. for HTT
                azhWeight[0] *= muonSF1[0] * muonSF2[0] * muonSF3[0] * muonSF4[0]
                azhWeight[0] *= electronSF1[0] * electronSF2[0] * electronSF3[0] * electronSF4[0]
                azhWeight[0] *= qqZZ4lWeight[0]



                # Special weighting for WJets and DYJets
                if shortName in ['DYJets', 'WJets'] :
                    xsec = getXSec( analysis, shortName, sampDict, row.numGenJets )
                    if xsec not in xsecList : xsecList.append( xsec )
                    #print "\n Sampe: %s    ShortNAme: %s    xsec: %f     numGenJets %i" % (sample, shortName, xsec, row.numGenJets)
                # If not WJets or DYJets fill from xsec defined before
                XSecLumiWeight[0] = xsec

            # Additional VVLoose and VVTight Iso WPs
            if channel == 'tt' :
                byVVTightIsolationMVArun2v1DBoldDMwLT_1[0] = isoWPAdder.getVVTight( row.t1ByIsolationMVArun2v1DBoldDMwLTraw, pt1 )
                byVVLooseIsolationMVArun2v1DBoldDMwLT_1[0] = isoWPAdder.getVVLoose( row.t1ByIsolationMVArun2v1DBoldDMwLTraw, pt1 )
                byVVTightIsolationMVArun2v1DBoldDMwLT_2[0] = isoWPAdder.getVVTight( row.t2ByIsolationMVArun2v1DBoldDMwLTraw, pt2 )
                byVVLooseIsolationMVArun2v1DBoldDMwLT_2[0] = isoWPAdder.getVVLoose( row.t2ByIsolationMVArun2v1DBoldDMwLTraw, pt2 )
                isoCode1[0] = setIsoCode( row, l1, byVVTightIsolationMVArun2v1DBoldDMwLT_1[0], byVVLooseIsolationMVArun2v1DBoldDMwLT_1[0]) 
                isoCode2[0] = setIsoCode( row, l2, byVVTightIsolationMVArun2v1DBoldDMwLT_2[0], byVVLooseIsolationMVArun2v1DBoldDMwLT_2[0]) 

            # Tau Pt Weighting
            if 'data' not in sample :
                if channel == 'em' :
                    tauPtWeightUp[0] = 1
                    tauPtWeightDown[0] = 1
                if channel == 'tt' :
                    tauPtWeightUp[0] = getTauPtWeight( sample, channel,
                        gen_match_1[0], gen_match_2[0], row, 0.2 )
                    tauPtWeightDown[0] = getTauPtWeight( sample, channel, 
                        gen_match_1[0], gen_match_2[0], row, -0.2 )

            if len(channel) > 3 :
                # Set LeptonJetPt to be equal to or greater than lepton Pt
                # b/c the lepton should be a subset of the overlapping jet
                # if jet pt < lepton pt, then we have the wrong jet
                for lep in [l1, l2, l3, l4] :
                    if getattr( row, lep+'Pt' ) > getattr( row, lep+'JetPt' ) :
                        setattr( row, lep+'JetPt', getattr( row, lep+'Pt' ))

                # Calculate our ZH fake rate values
                # This uses the 1+2-0 method detailed in AN2014/109
                if 'data' in sample :
                    zhFR1[0] = zhFRObj.getFRWeightL3( getattr( row, l3+'JetPt'), eta3, l3, row ) 
                    zhFR2[0] = zhFRObj.getFRWeightL4( getattr( row, l4+'JetPt'), eta4, l4, row ) 
                    zhFR0[0] = zhFR1[0] * zhFR2[0]
                
                # Define the LT varialbe we use in analysis (LT from FSA is all 4 objects)
                LT_higgs[0] = pt3 + pt4

                # Add VVL for leg3 and leg4
                if 't' in l3 :
                    byVVLooseIsolationMVArun2v1DBoldDMwLT_3[0] = isoWPAdder.getVVLoose(
                            getattr(row, l3+'ByIsolationMVArun2v1DBoldDMwLTraw'), pt3 )
                if 't' in l4 :
                    byVVLooseIsolationMVArun2v1DBoldDMwLT_4[0] = isoWPAdder.getVVLoose(
                            getattr(row, l4+'ByIsolationMVArun2v1DBoldDMwLTraw'), pt4 )



            tnew.Fill()
            count2 += 1

    # For xsec debugging:
    #if shortName in ['DYJets', 'WJets'] :
        #print "Cross Sections in sample: ",xsecList


    #print "Count: %i count2: %i" % (count, count2)
    #print "%25s : %10i" % ('Iso Selected', count2)


    isoQty = "%25s : %10i" % ('Iso Selected', count2)
    # write to disk
    tnew.write()
    fnew.close()
    return isoQty

