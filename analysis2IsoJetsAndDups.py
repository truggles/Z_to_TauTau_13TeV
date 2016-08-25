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

cmsLumi = float(os.getenv('LUMI'))
print "Lumi = %i" % cmsLumi

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

#XXX XXX XXX FIXME so that this does N Jet binned correct once we have ReHLT
def getXSec( analysis, shortName, sampDict, numGenJets=0 ) :
    #print "Short Name: ",shortName," mini Name: ",shortName[:6]#shortName[:-7]
    if 'data' in shortName : return 1.0 #XXX#
    jetBins = ['1', '2', '3', '4']
    try :
        if shortName in ['DYJets', 'DYJets'] or shortName[:6] == 'DYJets' :
        #if 'DYJets' in shortName :
            scalar1 = cmsLumi * sampDict[ 'DYJets' ]['Cross Section (pb)'] / sampDict[ 'DYJets' ]['summedWeightsNorm'] # removing LO small DYJets
            return scalar1 # FIXME
            #print "DYJets in shortName, scalar1 =",scalar1
        elif 'WJets' in shortName :
            scalar1 = cmsLumi * ( sampDict[ 'WJets' ]['Cross Section (pb)'] / sampDict[ 'WJets' ]['summedWeightsNorm'] )
            return scalar1 # FIXME
        else :
            scalar1 = cmsLumi * sampDict[ shortName ]['Cross Section (pb)'] / ( sampDict[ shortName ]['summedWeightsNorm'] )
            #print "DYJets not in shortName, scalar1 =",scalar1

    except KeyError :
        print "Sample not found in meta/Ntuples_xxx/samples.json"
        return
    #return scalar1 #XXX#
    
    """
    Commented out for HT bin samples, we're switching to
    jet binned samples
    """
    # If inclusive sample
    if shortName in ['DYJets', 'DYJetsBig', 'WJets'] :
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

        if shortName in ['DYJetsBig','DYJets'] :
            scalar2 = cmsLumi * sampDict[ 'DYJets'+binPartner ]['Cross Section (pb)'] / ( sampDict[ 'DYJets'+binPartner ]['summedWeightsNorm'] )
        elif shortName == 'WJets' :
            scalar2 = cmsLumi * sampDict[ 'WJets'+binPartner ]['Cross Section (pb)'] / ( sampDict[ 'WJets'+binPartner ]['summedWeightsNorm'] )
        return (1.0/( (1./scalar1) + (1./scalar2) ))

    # If exclusive sample
    if (('DYJets' in shortName) or ('WJets' in shortName)) and shortName[-1:] in jetBins :
        scalar2 = cmsLumi * sampDict[ shortName ]['Cross Section (pb)'] / ( sampDict[ shortName ]['summedWeightsNorm'] )
        #print "Scalar2 ",scalar2
        return (1.0/( (1./scalar1) + (1./scalar2) ))
        
        
    if 'QCD' in shortName or 'toTauTau' in shortName : return scalar1
    if 'data' in shortName : return 1.0
    return scalar1


def getTauPtWeight( sample, channel, row, ptScaler ) :
    if channel != 'tt' : return 1
    if not ('ggH' in sample or 'bbH' in sample or 'DYJets' in sample or 'VBF' in sample or 'Sync' in sample) :
        return 1
    l1weight = 0. 
    l2weight = 0.
    if row.t1ZTTGenMatching == 5 and row.t1GenJetPt >= 0 :
        l1weight = row.t1GenJetPt * ptScaler / 1000.
    if row.t2ZTTGenMatching == 5 and row.t2GenJetPt >= 0 :
        l2weight = row.t2GenJetPt * ptScaler / 1000.
    return 1 + l1weight + l2weight




def mVisTES( cand1, cand2, row, TES ) :
    pt1 = (1 + TES) * getattr( row, cand1+'Pt' )
    eta1 = getattr( row, cand1+'Eta' )
    phi1 = getattr( row, cand1+'Phi' )
    m1 = getattr( row, cand1+'Mass' )
    pt2 = (1 + TES) * getattr( row, cand2+'Pt' )
    eta2 = getattr( row, cand2+'Eta' )
    phi2 = getattr( row, cand2+'Phi' )
    m2 = getattr( row, cand2+'Mass' )
    lorentz1 = ROOT.TLorentzVector( 0,0,0,0 )
    lorentz1.SetPtEtaPhiM( pt1, eta1, phi1, m1 )
    lorentz2 = ROOT.TLorentzVector( 0,0,0,0 )
    lorentz2.SetPtEtaPhiM( pt2, eta2, phi2, m2 )
    shifted = lorentz1 + lorentz2
    return shifted.M()


def getMTTotal( pt1, phi1, pt2, phi2, row, channel, esUP=True ) :
    if channel == 'tt' :
        es = 0.03
    if channel == 'em' :
        if abs( row.eEta ) < 1.479 : # BarrelEndcap transition at eta = 1.479
            es = 0.01
        else :
            es = 0.025

    shift = 1.
    if esUP : shift += es
    else : shift -= es

    # Get ES corrected mva met
    dx1_UP = pt1 * math.cos( phi1 ) * (( 1. / (shift) ) - 1.)
    dy1_UP = pt1 * math.sin( phi1 ) * (( 1. / (shift) ) - 1.)
    if hasattr( row, "mvametcorr_ex" ) :
        mvametcorr_ex_UP = row.mvametcorr_ex + dx1_UP
        mvametcorr_ey_UP = row.mvametcorr_ey + dy1_UP
    else : return -10
    mvametcorr = math.sqrt( mvametcorr_ex_UP**2 + mvametcorr_ey_UP**2 )
    mvametcorrphi = ROOT.TMath.ATan2( mvametcorr_ey_UP, mvametcorr_ex_UP )

    mt_1_UP = getTransMass( mvametcorr, mvametcorrphi, pt1*shift, phi1 )
    mt_2_UP = getTransMass( mvametcorr, mvametcorrphi, pt2*shift, phi2 )
    return calcMTTotal( pt1*shift, phi1, pt2*shift, phi2, mt_1_UP, mt_2_UP )


def calcMTTotal( pt1, phi1, pt2, phi2, mt1, mt2 ) :
    mt_diTau = getTransMass( pt1, phi1, pt2, phi2 )
    return math.sqrt( mt_diTau**2 + mt1**2 + mt2**2 )


def getTransMass( met, metphi, l1pt, l1phi ) :
    return math.sqrt( 2 * l1pt * met * (1 - math.cos( l1phi - metphi)))


def getIso( cand, row ) :
    if 'e' in cand :
        return getattr(row, cand+'RelPFIsoDB')
    if 'm' in cand :
        return getattr(row, cand+'RelPFIsoDBDefault')
    if 't' in cand :
        #return getattr(row, cand+'ByCombinedIsolationDeltaBetaCorrRaw3Hits')
        return getattr(row, cand+'ByIsolationMVArun2v1DBoldDMwLTraw' )
        
        
def getCurrentEvt( channel, row ) :
    l1 = prodMap[channel][0]
    l2 = prodMap[channel][1]
    leg1Iso = getIso( l1, row )
    leg2Iso = getIso( l2, row )
    leg1Pt = getattr(row, l1+'Pt')
    leg2Pt = getattr(row, l2+'Pt')
    sign = ''
    if getattr(row, '%s_%s_SS' % (l1,l2)) == 1 : sign = 'SS'
    if getattr(row, '%s_%s_SS' % (l1,l2)) == 0 : sign = 'OS'

    if channel == 'tt' :
        if leg1Iso > leg2Iso :
            currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt, sign)
        elif leg1Iso < leg2Iso :
            currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt, sign)
        elif leg1Pt > leg2Pt :
            currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt, sign)
        elif leg1Pt < leg2Pt :
            currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt, sign)
        else : print "Iso1 == Iso2 & Pt1 == Pt2", row.evt
    else : currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt, sign)
    return currentEvt


tauIso = {
    'Pt' : 'pt',
    'Eta' : 'eta',
    'Phi' : 'phi',
    'Mass' : 'm',
    'Charge' : 'q',
    'PVDXY' : 'd0',
    'PVDZ' : 'dZ',
    'MtToPfMet_Raw' : '',
    'MtToPfMet_type1' : '',
    'ByCombinedIsolationDeltaBetaCorrRaw3Hits' : 'iso',
    'ByIsolationMVArun2v1DBnewDMwLTraw' : '',
    'ByIsolationMVArun2v1DBoldDMwLTraw' : '',
    'ByLooseIsolationMVArun2v1DBoldDMwLT' : '',
    'ByMediumIsolationMVArun2v1DBoldDMwLT' : '',
    'ByTightIsolationMVArun2v1DBoldDMwLT' : '',
    'ByVTightIsolationMVArun2v1DBoldDMwLT' : '',
    'ByIsolationMVA3newDMwLTraw' : '',
    'ByIsolationMVA3oldDMwLTraw' : '',
    'AgainstElectronLooseMVA6' : 'againstElectronLooseMVA6',
    'AgainstElectronMediumMVA6' : 'againstElectronMediumMVA6',
    'AgainstElectronTightMVA6' : 'againstElectronTightMVA6',
    'AgainstElectronVLooseMVA6' : 'againstElectronVLooseMVA6',
    'AgainstElectronVTightMVA6' : 'againstElectronVTightMVA6',
    'AgainstMuonLoose3' : 'againstMuonLoose3',
    'AgainstMuonTight3' : 'againstMuonTight3',
    'ChargedIsoPtSum' : 'chargedIsoPtSum',
    'NeutralIsoPtSum' : 'neutralIsoPtSum',
    'PuCorrPtSum' : 'puCorrPtSum',
    'AbsEta' : '',
    'DecayMode' : '',
    'DecayModeFinding' : '',
    'DoubleTau40Filter' : '',
    'ElecOverlap' : '',
    'GenDecayMode' : '',
    'ZTTGenMatching' : 'gen_match',
    'GlobalMuonVtxOverlap' : '',
    'JetArea' : '',
    'JetBtag' : '',
    'JetEtaEtaMoment' : '',
    'JetEtaPhiMoment' : '',
    'JetPFCISVBtag' : '',
    'JetPartonFlavour' : '',
    'JetPhiPhiMoment' : '',
    'JetPt' : '',
    'GenJetPt' : '',
    'LeadTrackPt' : '',
    'LowestMll' : '',
    'MatchesDoubleTau40Path' : '',
    'MatchesDoubleTau35Path' : '',
    'MuOverlap' : '',
    'MuonIdIsoStdVtxOverlap' : '',
    'MuonIdIsoVtxOverlap' : '',
    'MuonIdVtxOverlap' : '',
    'NearestZMass' : '',
    'Rank' : '',
    'VZ' : '',
}

def isoOrder( channel, row ) :
    if channel != 'tt' : return
    iso1 = getattr( row, 't1ByIsolationMVArun2v1DBoldDMwLTraw' )
    iso2 = getattr( row, 't2ByIsolationMVArun2v1DBoldDMwLTraw' )
        
    #iso1 = getattr( row, 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits')
    #iso2 = getattr( row, 't2ByCombinedIsolationDeltaBetaCorrRaw3Hits')
    pt1 = getattr( row, 't1Pt' )
    pt2 = getattr( row, 't2Pt' )
    if iso2 > iso1 :
        for uw in tauIso.keys() :
            if not hasattr( row, 't1%s' % uw ) : continue
            if not hasattr( row, 't2%s' % uw ) : continue
            tmp1 = getattr( row, 't1%s' % uw )
            tmp2 = getattr( row, 't2%s' % uw )
            setattr( row, 't1%s' % uw, tmp2 )
            setattr( row, 't2%s' % uw, tmp1 )

def vbfClean( row ) :
    if row.jetVeto20ZTT < 2 :
        setattr( row, 'vbfMassZTT', -10000 )
        setattr( row, 'vbfDetaZTT', -10 )
        setattr( row, 'vbfDphiZTT', -10 )
        setattr( row, 'vbfJetVeto30ZTT', -10 )
        setattr( row, 'vbfJetVeto20ZTT', -10 )

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

    #from util.zPtReweight import ZPtReweighter
    #zPtWeighter = ZPtReweighter()

    #cmssw_base = os.getenv('CMSSW_BASE')
    #ff_file = ROOT.TFile.Open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/fakeFactors_20160425.root')
    #ffqcd = ff_file.Get('ff_qcd_os') 

    sameNameVars = [
    'run','lumi','evt','GenWeight','LT','charge','jetVeto30','jetVeto40',
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
        #'bjetCISVVeto20MediumZTT' : 'nbtag',
        #XXX 'NBTagPDM_idL_jVeto' : 'nbtag',
        #XXX 'NBTagPDL_idL_jVeto' : 'nbtagLoose',
        'jetVeto20ZTT' : 'njetspt20',
        #'jetVeto30RecoilZTT' : 'njets',
        'jetVeto30ZTT' : 'njets',
        'type1_pfMetEt' : 'met',
        'type1_pfMetPhi' : 'metphi',
        #'GenWeight' : 'weight',
        'vbfMassZTT' : 'mjj',
        'vbfDetaZTT' : 'jdeta',
        'vbfDphiZTT' : 'jdphi',
        'vbfJetVeto30ZTT' : 'njetingap',
        'vbfJetVeto20ZTT' : 'njetingap20',
        }
    doubleProds = {
        'Mass' : 'm_vis',
        #'SVfitMass' : 'm_sv',
        'PZeta' : 'pfpzetamis',
        'PZetaVis' : 'pzetavis',
        'SS' : 'Z_SS',
        'Pt' : 'Z_Pt',
        'DR' : 'Z_DR',
        'DPhi' : 'Z_DPhi',
        #XXX#'pt_tt' : 'pp_tt',
        #XXX#'MtTotal' : 'mt_tot',
        }
    quadFSDoubleProds = {
        'Mass' : 'H_vis',
        #'SVfitMass' : 'm_sv',
        'SS' : 'H_SS',
        'Pt' : 'H_Pt',
        'DR' : 'H_DR',
        'DPhi' : 'H_DPhi',
        }
    branchMappingElec = {
        'cand_ZTTGenMatching' : 'gen_match',
        'cand_Pt' : 'pt', # rename ePt to pt_1
        'cand_Eta' : 'eta',
        'cand_Phi' : 'phi',
        'cand_Mass' : 'm',
        'cand_Charge' : 'q',
        'cand_PVDXY' : 'd0',
        'cand_PVDZ' : 'dZ',
        'cand_IsoDB03' : 'iso',
        'cand_MVANonTrigWP90' : 'id_e_mva_nt_loose',
        'cand_MtToPfMet_Raw' : 'pfmt',
        }
    branchMappingMuon = {
        'cand_ZTTGenMatching' : 'gen_match',
        'cand_Pt' : 'pt',
        'cand_Eta' : 'eta',
        'cand_Phi' : 'phi',
        'cand_Mass' : 'm',
        'cand_Charge' : 'q',
        'cand_PVDXY' : 'd0',
        'cand_PVDZ' : 'dZ',
        'cand_IsoDB03' : 'iso',
        'cand_MtToPfMet_Raw' : 'pfmt',
        }
    branchMappingTau = {
        'cand_ZTTGenMatching' : 'gen_match',
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
        'cand_MtToPfMet_Raw' : 'pfmt',
        'cand_ByVTightIsolationMVArun2v1DBoldDMwLT' : 'byVTightIsolationMVArun2v1DBoldDMwLT',
        'cand_ByTightIsolationMVArun2v1DBoldDMwLT' : 'byTightIsolationMVArun2v1DBoldDMwLT',
        'cand_ByMediumIsolationMVArun2v1DBoldDMwLT' : 'byMediumIsolationMVArun2v1DBoldDMwLT',
        'cand_ByLooseIsolationMVArun2v1DBoldDMwLT' : 'byLooseIsolationMVArun2v1DBoldDMwLT',
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
            l1Map = branchMappingElec
            l2Map = branchMappingMuon
        elif channel == 'et' :
            l1Map = branchMappingElec
            l2Map = branchMappingTau
        elif channel == 'mt' :
            l1Map = branchMappingMuon
            l2Map = branchMappingTau
        elif channel == 'tt' :
            l1Map = branchMappingTau
            l2Map = branchMappingTau
    if len( channel ) == 4 :
        # Channel naming gets confusing with FSA, e first, m second, t last
        if channel[:2] == 'ee' :
            l1Map = branchMappingElec
            l2Map = branchMappingElec
        elif channel[:2] == 'mm' or channel == 'emmt' or channel == 'emmm' :
            l1Map = branchMappingMuon
            l2Map = branchMappingMuon

        if channel[-2:] == 'ee' :
            l3Map = branchMappingElec
            l4Map = branchMappingElec
        if channel[-2:] == 'mm' :
            l3Map = branchMappingMuon
            l4Map = branchMappingMuon
        if channel[-2:] == 'tt' :
            l3Map = branchMappingTau
            l4Map = branchMappingTau
        elif channel[-2:] == 'mt' :
            l3Map = branchMappingMuon
            l4Map = branchMappingTau
        elif channel == 'eeet' or channel == 'emmt' :
            l3Map = branchMappingElec
            l4Map = branchMappingTau
        elif channel == 'eeem' or channel == 'emmm' :
            l3Map = branchMappingElec
            l4Map = branchMappingMuon

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
    #intBranches = set(['run', 'evt', 'lumi', 'isdata', 'pvIsValid', 'pvIsFake'])
    intBranches = set(['run', 'evt', 'lumi', 'isdata',])
    
    ##############################################################################
    # Shouldn't need to modify anything below here                               #
    ##############################################################################
    
    from rootpy.io import root_open
    from rootpy.tree import Tree, TreeModel, FloatCol, IntCol
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
        branchType = IntCol() if old in intBranches else FloatCol()
        if old in branchMapping.keys() :
            name = branchMapping[old]
            branchType = IntCol() if old in intBranches else FloatCol()
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
    prevEvt = (999, 0, 999, 0, '')
    prevRunLumiEvt = (0, 0, 0)
    toFillMap = {}
    count = 0
    for row in told:
        run = int( row.run )
        lumi = int( row.lumi )
        evt = int( row.evt )
        
        currentEvt = getCurrentEvt( channel, row )
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
        if channel == 'tt' :
            # OS has preference over SS regardless of iso and pt
            #if currentEvt[ 4 ] == 'OS' and prevEvt[ 4 ] == 'SS' :
            #    prevEvt = currentEvt
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
        else :
            # OS has preference over SS regardless of iso and pt
            #if currentEvt[ 4 ] == 'OS' and prevEvt[ 4 ] == 'SS' :
            #    prevEvt = currentEvt
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
        if count == numRows :
            #print "LastRowPrev:",prevRunLumiEvt, prevEvt
            #print "LastRowCur:",currentRunLumiEvt, currentEvt
            prevRunLumiEvt = currentRunLumiEvt
            prevEvt = currentEvt
            toFillMap[ prevRunLumiEvt ] = prevEvt
    
    ''' Add a nvtx Pile UP weighting variable to the new tree
    see util.pileUpVertexCorrections.addNvtxWeight for inspiration '''
    from util.pZeta import compZeta
    from util.pileUpVertexCorrections import PUreweight
    from array import array
    puDict = PUreweight()

    ''' We are calculating and adding these below variables to our new tree
    PU Weighting '''
    weight = array('f', [ 0 ] )
    weightB = tnew.Branch('weight', weight, 'weight/F')
    azhWeight = array('f', [ 0 ] )
    azhWeightB = tnew.Branch('azhWeight', azhWeight, 'azhWeight/F')
    puweight = array('f', [ 0 ] )
    puweightB = tnew.Branch('puweight', puweight, 'puweight/F')
    tauPtWeightUp = array('f', [ 0 ] )
    tauPtWeightUpB = tnew.Branch('tauPtWeightUp', tauPtWeightUp, 'tauPtWeightUp/F')
    tauPtWeightDown = array('f', [ 0 ] )
    tauPtWeightDownB = tnew.Branch('tauPtWeightDown', tauPtWeightDown, 'tauPtWeightDown/F')
    topWeight = array('f', [ 0 ] )
    topWeightB = tnew.Branch('topWeight', topWeight, 'topWeight/F')
    zPtWeight = array('f', [ 0 ] )
    zPtWeightB = tnew.Branch('zPtWeight', zPtWeight, 'zPtWeight/F')
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
    #FFWeightQCD = array('f', [ 0 ] )
    #FFWeightQCDB = tnew.Branch('FFWeightQCD', FFWeightQCD, 'FFWeightQCD/F')
    #FFWeightQCD_UP = array('f', [ 0 ] )
    #FFWeightQCD_UPB = tnew.Branch('FFWeightQCD_UP', FFWeightQCD_UP, 'FFWeightQCD_UP/F')
    #FFWeightQCD_DOWN = array('f', [ 0 ] )
    #FFWeightQCD_DOWNB = tnew.Branch('FFWeightQCD_DOWN', FFWeightQCD_DOWN, 'FFWeightQCD_DOWN/F')
    #FFWeightQCD1 = array('f', [ 0 ] )
    #FFWeightQCD1B = tnew.Branch('FFWeightQCD1', FFWeightQCD1, 'FFWeightQCD1/F')
    #FFWeightQCD1_UP = array('f', [ 0 ] )
    #FFWeightQCD1_UPB = tnew.Branch('FFWeightQCD1_UP', FFWeightQCD1_UP, 'FFWeightQCD1_UP/F')
    #FFWeightQCD1_DOWN = array('f', [ 0 ] )
    #FFWeightQCD1_DOWNB = tnew.Branch('FFWeightQCD1_DOWN', FFWeightQCD1_DOWN, 'FFWeightQCD1_DOWN/F')
    #FFWeightQCD2 = array('f', [ 0 ] )
    #FFWeightQCD2B = tnew.Branch('FFWeightQCD2', FFWeightQCD2, 'FFWeightQCD2/F')
    #FFWeightQCD2_UP = array('f', [ 0 ] )
    #FFWeightQCD2_UPB = tnew.Branch('FFWeightQCD2_UP', FFWeightQCD2_UP, 'FFWeightQCD2_UP/F')
    #FFWeightQCD2_DOWN = array('f', [ 0 ] )
    #FFWeightQCD2_DOWNB = tnew.Branch('FFWeightQCD2_DOWN', FFWeightQCD2_DOWN, 'FFWeightQCD2_DOWN/F')
    #pzetamiss = array('f', [ 0 ] )
    #pzetamissB = tnew.Branch('pzetamiss', pzetamiss, 'pzetamiss/F')
    #pzeta = array('f', [ 0 ] )
    #pzetaB = tnew.Branch('pzeta', pzeta, 'pzeta/F')
    Z_DEta = array('f', [ 0 ] )
    Z_DEtaB = tnew.Branch('Z_DEta', Z_DEta, 'Z_DEta/F')
    #m_vis_UP = array('f', [ 0 ] )
    #m_vis_UPB = tnew.Branch('m_vis_UP', m_vis_UP, 'm_vis_UP/F')
    #m_vis_DOWN = array('f', [ 0 ] )
    #m_vis_DOWNB = tnew.Branch('m_vis_DOWN', m_vis_DOWN, 'm_vis_DOWN/F')
    mt_tot = array('f', [ 0 ] )
    mt_totB = tnew.Branch('mt_tot', mt_tot, 'mt_tot/F')
    #mt_tot_UP = array('f', [ 0 ] )
    #mt_tot_UPB = tnew.Branch('mt_tot_UP', mt_tot_UP, 'mt_tot_UP/F')
    #mt_tot_DOWN = array('f', [ 0 ] )
    #mt_tot_DOWNB = tnew.Branch('mt_tot_DOWN', mt_tot_DOWN, 'mt_tot_DOWN/F')
    #mt_1 = array('f', [ 0 ] )
    #mt_1B = tnew.Branch('mt_1', mt_1, 'mt_1/F')
    #mt_2 = array('f', [ 0 ] )
    #mt_2B = tnew.Branch('mt_2', mt_2, 'mt_2/F')
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



    ''' Now actually fill that instance of an evtFake'''
    count2 = 0
    xsecList = []
    for row in told:
        run = int( row.run )
        lumi = int( row.lumi )
        evt = int( row.evt )
        if evt < 0 :
            print "\n\n\n BIG \n\n TROUBLE \n\n EVT: %i   Sample: %s \n\n\n\n" % (evt, sample)
        
        currentEvt = getCurrentEvt( channel, row )
        currentRunLumiEvt = (run, lumi, evt)

        
        if currentRunLumiEvt in toFillMap.keys() and currentEvt == toFillMap[ currentRunLumiEvt ] :
            #print "Fill choice:",currentRunLumiEvt, currentEvt

            #if channel == 'tt' and 'Sync-HtoTT' in sample : 
            #    #print "### Iso Ordering %s ###" % sample
            #    isoOrder( channel, row )
            vbfClean( row )


            #FFWeightQCD[0] = -1
            #FFWeightQCD_UP[0] = -1
            #FFWeightQCD_DOWN[0] = -1
            #FFWeightQCD1[0] = -1
            #FFWeightQCD1_UP[0] = -1
            #FFWeightQCD1_DOWN[0] = -1
            #FFWeightQCD2[0] = -1
            #FFWeightQCD2_UP[0] = -1
            #FFWeightQCD2_DOWN[0] = -1


            # For easy use later
            pt1 = getattr( row, l1+'Pt' )
            phi1 = getattr( row, l1+'Phi' )
            eta1 = getattr( row, l1+'Eta' )
            pt2 = getattr( row, l2+'Pt' )
            phi2 = getattr( row, l2+'Phi' )
            eta2 = getattr( row, l2+'Eta' )
            if len( channel ) > 2 :
                pt3 = getattr( row, l3+'Pt' )
                phi3 = getattr( row, l3+'Phi' )
                eta3 = getattr( row, l3+'Eta' )
            if len( channel ) > 3 :
                pt4 = getattr( row, l4+'Pt' )
                phi4 = getattr( row, l4+'Phi' )
                eta4 = getattr( row, l4+'Eta' )

            Z_DEta[0] = (eta1 - eta2)

            # TES Shifted M_Vis
            #if 'DYJets' in sample or 'ggH' in sample or 'bbH' in sample or 'VBH' in sample :
            #    m_vis_UP[0] = mVisTES( l1, l2, row, 0.03 )
            #    m_vis_DOWN[0] = mVisTES( l1, l2, row, -0.03 )
            #else :
            #    m_vis_UP[0] = getattr( row, '%s_%s_Mass' % (l1, l2) )
            #    m_vis_DOWN[0] = getattr( row, '%s_%s_Mass' % (l1, l2) )
            #    if hasattr( row, 'm_sv_UP' ) :
            #        setattr( row, 'm_sv_UP', getattr( row, 'm_sv' ) )
            #        setattr( row, 'm_sv_DOWN', getattr( row, 'm_sv' ) )
            #        setattr( row, 'mt_sv_UP', getattr( row, 'mt_sv' ) )
            #        setattr( row, 'mt_sv_DOWN', getattr( row, 'mt_sv' ) )


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
            
            if hasattr( row, "%s_%s_MvaMetCovMatrix00" % (l1, l2) ):
                mvacov00[0] = getattr( row, "%s_%s_MvaMetCovMatrix00" % (l1, l2) )
                mvacov01[0] = getattr( row, "%s_%s_MvaMetCovMatrix01" % (l1, l2) )
                mvacov10[0] = getattr( row, "%s_%s_MvaMetCovMatrix10" % (l1, l2) )
                mvacov11[0] = getattr( row, "%s_%s_MvaMetCovMatrix11" % (l1, l2) )

            # Channel specific pairwise mvaMet
            #if channel == 'tt' :
            #    if hasattr( row, "mvamet" ) and hasattr( row, "mvametphi" ) :
            #        pzetamiss[0] = compZeta(pt1, phi1, pt2, phi2, row.mvamet, row.mvametphi)[1]
            #        mt_1[0] = getTransMass( row.mvamet, row.mvametphi, pt1, phi1 )
            #        mt_2[0] = getTransMass( row.mvamet, row.mvametphi, pt2, phi2 )
            #    else :
            #        pzetamiss[0] = -9999
            #        mt_1[0] = -9999
            #        mt_2[0] = -9999
            #if channel == 'em' :
            #    if hasattr( row, "mvamet" ) and hasattr( row, "mvametphi" ) :
            #        pzetamiss[0] = compZeta(pt1, phi1, pt2, phi2, row.mvamet, row.mvametphi)[1]
            #        mt_1[0] = getTransMass( row.mvamet, row.mvametphi, pt1, phi1 )
            #        mt_2[0] = getTransMass( row.mvamet, row.mvametphi, pt2, phi2 )
            #    else :
            #        pzetamiss[0] = -9999
            #        mt_1[0] = -9999
            #        mt_2[0] = -9999
            #if hasattr( row, '%s_%s_PZetaVis' % (l1, l2) ) :
            #    pzeta[0] = pzetamiss[0] - 0.85 * getattr( row, '%s_%s_PZetaVis' % (l1, l2) )


            # With calculated transverse mass variables, do Mt_Total for mssm search
            mt_1 = getattr( row, l1+'MtToPfMet_Raw' )
            mt_2 = getattr( row, l2+'MtToPfMet_Raw' )
            mt_tot[0] = calcMTTotal( pt1, phi1, pt2, phi2, mt_1, mt_2 ) # Using wrong mt
            #XXX mt_tot[0] = calcMTTotal( pt1, phi1, pt2, phi2, mt_1[0], mt_2[0] )
            #if 'DYJets' in sample or 'ggH' in sample or 'bbH' in sample or 'VBH' in sample or 'Sync' in sample :
            #    mt_tot_UP[0] = getMTTotal( pt1, phi1, pt2, phi2, row, channel, True )
            #    mt_tot_DOWN[0] = getMTTotal( pt1, phi1, pt2, phi2, row, channel, False )
            #else :
            #    mt_tot_UP[0] = -10
            #    mt_tot_DOWN[0] = -10
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
            weight[0] = 1
            XSecLumiWeight[0] = 1

            # Data specific vars
            if 'data' in sample :
                # Have the btag numbers correspond to actual values not
                # Promote/Demote values
                if hasattr(row, 'NBTagPDM_idL_jVeto' ) :
                    setattr(row, 'NBTagPDM_idL_jVeto', getattr(row, 'bjetCISVVeto20MediumZTT'))
                if hasattr(row, 'NBTagPDL_idL_jVeto' ) :
                    setattr(row, 'NBTagPDL_idL_jVeto', getattr(row, 'bjetCISVVeto20LooseZTT'))

                # Calculate Fake Factors based on this work:
                # https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauJet2TauFakes
                # We start with applying QCD factors to each leg and sum for total
                #if channel == 'tt' :
                #    FFWeightQCD[0] = 0.
                #    FFWeightQCD_UP[0] = 0.
                #    FFWeightQCD_DOWN[0] = 0.
                #    FFWeightQCD1[0] = 0.
                #    FFWeightQCD1_UP[0] = 0.
                #    FFWeightQCD1_DOWN[0] = 0.
                #    FFWeightQCD2[0] = 0.
                #    FFWeightQCD2_UP[0] = 0.
                #    FFWeightQCD2_DOWN[0] = 0.
                #    muon_iso = 0.089 # this is an artifact of being based on MuTau channel
                #                    # 0.089 gives a correction value of 1.0
                #    # First leg FR
                #    if row.t1ByTightIsolationMVArun2v1DBoldDMwLT < 0.5 and row.t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 :
                #        inputsqcd = ffqcd.inputs()
                #        inputsqcd = [pt1, row.t1DecayMode, row.t1_t2_Mass, muon_iso]
                #        FFWeightQCD1[0] = ffqcd.value( len(inputsqcd),array('d',inputsqcd) )
                #        FFWeightQCD1_UP[0] = ffqcd.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_up" )
                #        FFWeightQCD1_DOWN[0] = ffqcd.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_down" )
                #    # Second leg FR
                #    if row.t2ByTightIsolationMVArun2v1DBoldDMwLT < 0.5 and row.t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 :
                #        inputsqcd = ffqcd.inputs()
                #        inputsqcd = [pt2, row.t2DecayMode, row.t1_t2_Mass, muon_iso]
                #        FFWeightQCD2[0] = ffqcd.value( len(inputsqcd),array('d',inputsqcd) )
                #        FFWeightQCD2_UP[0] = ffqcd.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_up" )
                #        FFWeightQCD2_DOWN[0] = ffqcd.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_down" )
                #    # Total
                #    FFWeightQCD[0] = FFWeightQCD1[0] + FFWeightQCD2[0] 
                #    FFWeightQCD_UP[0] = FFWeightQCD1_UP[0] + FFWeightQCD2_UP[0] 
                #    FFWeightQCD_DOWN[0] = FFWeightQCD1_DOWN[0] + FFWeightQCD2_DOWN[0]
                    
            ### Not Data
            else :
                nTrPu = ( math.floor(row.nTruePU * 10))/10
                puweight[0] = puDict[ nTrPu ]

                if analysis == 'azh' :
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
                    t1Gen = getattr( row, l1+'ZTTGenMatching' )
                    tauIso = 'NoIso'
                    if getattr( row, l1+'ByLooseIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'LooseIso'
                    if getattr( row, l1+'ByMediumIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'MediumIso'
                    if getattr( row, l1+'ByTightIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'TightIso'
                    if getattr( row, l1+'ByVTightIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'VTightIso'
                    trigweight_1[0] = doublTau35.doubleTauTriggerEff( pt1, tauIso, t1Gen )
                    t2Gen = getattr( row, l2+'ZTTGenMatching' )
                    tauIso = 'NoIso'
                    if getattr( row, l2+'ByLooseIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'LooseIso'
                    if getattr( row, l2+'ByMediumIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'MediumIso'
                    if getattr( row, l2+'ByTightIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'TightIso'
                    if getattr( row, l2+'ByVTightIsolationMVArun2v1DBoldDMwLT' ) > 0 :
                        tauIso = 'VTightIso'
                    trigweight_2[0] = doublTau35.doubleTauTriggerEff( pt2, tauIso, t2Gen )
                    tauIDweight_1[0] = 0.84
                    tauIDweight_2[0] = 0.84
                
                # top pt reweighting, only for ttbar events
                # https://twiki.cern.ch/twiki/bin/view/CMS/MSSMAHTauTauEarlyRun2#Top_quark_pT_reweighting
                #if 'TT' in sample and hasattr( row, 'topQuarkPt1' ) :
                #    top1Pt = row.topQuarkPt1
                #    if top1Pt > 400 : top1Pt = 400
                #    top2Pt = row.topQuarkPt2
                #    if top2Pt > 400 : top2Pt = 400
                #    topWeight[0] = math.sqrt(math.exp(0.156-0.00137*top1Pt)*math.exp(0.156-0.00137*top2Pt))
                #else : topWeight[0] = 1
                topWeight[0] = 1

                # Apply z Pt Reweighting to LO DYJets samples
                # https://twiki.cern.ch/twiki/bin/view/CMS/MSSMAHTauTauEarlyRun2#Z_reweighting

                #if 'DYJets' in sample and 'Low' not in sample :
                #    if hasattr( row, 'genM' ) and hasattr( row, 'genpT' ) :
                #        zPtWeight[0] = zPtWeighter.getZPtReweight( row.genM, row.genpT )
                weight[0] = puweight[0] * idisoweight_1[0] * idisoweight_2[0]
                weight[0] *= trigweight_1[0] * trigweight_2[0]
                weight[0] *= zPtWeight[0]* topWeight[0]
                # Below set to 1. for HTT
                azhWeight[0] *= muonSF1[0] * muonSF2[0] * muonSF3[0] * muonSF4[0]
                azhWeight[0] *= electronSF1[0] * electronSF2[0] * electronSF3[0] * electronSF4[0]



                # Special weighting for WJets and DYJets
                if shortName in ['DYJets', 'DYJetsBig', 'WJets'] :
                    xsec = getXSec( analysis, shortName, sampDict, row.numGenJets )
                    if xsec not in xsecList : xsecList.append( xsec )
                    #print "\n Sampe: %s    ShortNAme: %s    xsec: %f     numGenJets %i" % (sample, shortName, xsec, row.numGenJets)
                # If not WJets or DYJets fill from xsec defined before
                XSecLumiWeight[0] = xsec

            # Tau Pt Weighting
            if 'data' not in sample :
                if channel == 'em' :
                    tauPtWeightUp[0] = 1
                    tauPtWeightDown[0] = 1
                if channel == 'tt' :
                    tauPtWeightUp[0] = getTauPtWeight( sample, channel, row, 0.2 )
                    tauPtWeightDown[0] = getTauPtWeight( sample, channel, row, -0.2 )



            tnew.Fill()
            count2 += 1

    # For xsec debugging:
    #if shortName in ['DYJets', 'DYJetsBig', 'WJets'] :
        #print "Cross Sections in sample: ",xsecList


    #print "Count: %i count2: %i" % (count, count2)
    #print "%25s : %10i" % ('Iso Selected', count2)


    isoQty = "%25s : %10i" % ('Iso Selected', count2)
    # write to disk
    tnew.write()
    fnew.close()
    return isoQty

