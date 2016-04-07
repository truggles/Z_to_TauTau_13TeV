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
}


def getXSec( shortName, sampDict, numGenJets=0 ) :
    #print "Short Name: ",shortName," mini Name: ",shortName[:6]#shortName[:-7]
    #if 'data' in shortName : return 1.0 #XXX#
    jetBins = ['1', '2', '3', '4']
    try :
        if shortName in ['DYJets', 'DYJetsBig'] or shortName[:6] == 'DYJets' :
        #if 'DYJets' in shortName :
            scalar1 = cmsLumi * sampDict[ 'DYJets' ]['Cross Section (pb)'] / ( sampDict[ 'DYJets' ]['summedWeightsNorm'] + sampDict[ 'DYJetsBig' ]['summedWeightsNorm'] )
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



def renameBranches( grouping, mid1, mid2, sample, channel, bkgFlag, count ) :
    with open('meta/NtupleInputs_%s/samples.json' % grouping) as sampFile :
        sampDict = json.load( sampFile )

    shortName = sample.split('_')[0]
    if shortName == 'data' : shortName = 'data_%s' % channel

    xsec = getXSec( shortName, sampDict )
    print "\n Sampe: %s    shortName: %s    xsec: %f" % (sample, shortName, xsec)

    l1 = prodMap[channel][0]
    l2 = prodMap[channel][1]

    from util.lepSF import LepWeights
    from util.doubleTauSF import doubleTauTriggerEff
    lepWeights = LepWeights( channel, count )

    branchMapping = {
        'run' : 'run',
        'lumi' : 'lumi',
        'evt' : 'evt',
        'nvtx' : 'npv',
        'nTruePU' : 'npu',
        'charge' : 'charge',
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
        'NBTagPDM_idL_jVeto' : 'nbtag',
        'NBTagPDL_idL_jVeto' : 'nbtagLoose',
        'jetVeto20ZTT' : 'njetspt20',
        'jetVeto30RecoilZTT' : 'njets',
        #'jetVeto30ZTT' : 'njets',
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
        'cand_DecayModeFinding' : 'decayModeFindingOldDMs',
        'cand_NeutralIsoPtSum' : 'neutralIsoPtSum',
        'cand_PuCorrPtSum' : 'puCorrPtSum',
        'cand_ByIsolationMVA3newDMwLTraw' : 'byIsolationMVA3newDMwLTraw',
        #'cand_ByIsolationMVA3newDMwoLTraw' : 'byIsolationMVA3newDMwoLTraw',
        'cand_ByIsolationMVA3oldDMwLTraw' : 'byIsolationMVA3oldDMwLTraw',
        #'cand_ByIsolationMVA3oldDMwoLTraw' : 'byIsolationMVA3oldDMwoLTraw',
        'cand_MtToPfMet_Raw' : 'pfmt',
        }

    # Generate our mapping for double candidate variables
    for key in doubleProds :
        branchMapping[ l1+'_'+l2+'_'+key ] = doubleProds[ key ]
    # Map all of the variables based on their FSA names to Sync names leg by leg
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
    for key in l1Map.keys() :
        branchMapping[ key.replace('cand_', l1) ] = l1Map[ key ]+'_1'
    for key in l2Map.keys() :
        branchMapping[ key.replace('cand_', l2) ] = l2Map[ key ]+'_2'

    if bkgFlag == '' :
        oldFileName = '%s%s/%s.root' % (grouping, mid1, sample)
        newFileName = '%s%s/%s.root' % (grouping, mid2, sample)
    else :
        oldFileName = 'meta/%sBackgrounds/%s/cut/%s.root' % (grouping, bkgFlag, sample)
        newFileName = 'meta/%sBackgrounds/%s/iso/%s.root' % (grouping, bkgFlag, sample)

    dirName = channel
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
        ###if old in branchMapping.keys() :
        ###    name = branchMapping[old]
        ###    branchType = IntCol() if old in intBranches else FloatCol()
        ###    newBranches[name] = branchType
    
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
        if count == 0 : prevRunLumiEvt = currentRunLumiEvt

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

        #print currentRunLumiEvt, currentEvt
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
                if currentEvt[ 1 ] < prevEvt[ 1 ] :
                    prevEvt = currentEvt
                # pt_1 equal
                elif currentEvt[ 1 ] == prevEvt[ 1 ] :
                    # lowest iso_2
                    if currentEvt[ 2 ] < prevEvt[ 2 ] :
                        prevEvt = currentEvt
                    # iso_2 equal
                    elif currentEvt[ 2 ] == prevEvt[ 2 ] :
                        # highest pt_2
                        if currentEvt[ 3 ] < prevEvt[ 3 ] :
                            prevEvt = currentEvt
        

        # Make sure we get the last event
        if count == numRows :
            #print "LastRow:",prevRunLumiEvt, prevEvt
            prevRunLumiEvt = currentRunLumiEvt
            prevEvt = currentEvt
            toFillMap[ prevRunLumiEvt ] = prevEvt
    
    ''' Add a nvtx Pile UP weighting variable to the new tree
    see util.pileUpVertexCorrections.addNvtxWeight for inspiration '''
    from util.pZeta import compZeta
    from util.pileUpVertexCorrections import PUreweight
    from array import array
    puDict = PUreweight( channel )

    ''' We are calculating and adding these below variables to our new tree
    PU Weighting '''
    weight = array('f', [ 0 ] )
    weightB = tnew.Branch('weight', weight, 'weight/F')
    puweight = array('f', [ 0 ] )
    puweightB = tnew.Branch('puweight', puweight, 'puweight/F')
    pzetamiss = array('f', [ 0 ] )
    pzetamissB = tnew.Branch('pzetamiss', pzetamiss, 'pzetamiss/F')
    m_vis_UP = array('f', [ 0 ] )
    m_vis_UPB = tnew.Branch('m_vis_UP', m_vis_UP, 'm_vis_UP/F')
    m_vis_DOWN = array('f', [ 0 ] )
    m_vis_DOWNB = tnew.Branch('m_vis_DOWN', m_vis_DOWN, 'm_vis_DOWN/F')
    mt_1 = array('f', [ 0 ] )
    mt_1B = tnew.Branch('mt_1', mt_1, 'mt_1/F')
    mt_2 = array('f', [ 0 ] )
    mt_2B = tnew.Branch('mt_2', mt_2, 'mt_2/F')
    XSecLumiWeight = array('f', [ 0 ] )
    XSecLumiWeightB = tnew.Branch('XSecLumiWeight', XSecLumiWeight, 'XSecLumiWeight/F')
    trigweight_1 = array('f', [ 0 ] )
    trigweight_1B = tnew.Branch('trigweight_1', trigweight_1, 'trigweight_1/F')
    effweight = array('f', [ 0 ] )
    effweightB = tnew.Branch('effweight', effweight, 'effweight/F')
    idisoweight_1 = array('f', [ 0 ] )
    idisoweight_1B = tnew.Branch('idisoweight_1', idisoweight_1, 'idisoweight_1/F')
    idisoweight_2 = array('f', [ 0 ] )
    idisoweight_2B = tnew.Branch('idisoweight_2', idisoweight_2, 'idisoweight_2/F')
    UniqueID = array('f', [ 0 ] )
    UniqueIDB = tnew.Branch('UniqueID', UniqueID, 'UniqueID/F')
    BkgGroup = array('f', [ 0 ] )
    BkgGroupB = tnew.Branch('BkgGroup', BkgGroup, 'BkgGroup/F')
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
    isZtt = array('f', [ 0 ] )
    isZttB = tnew.Branch('isZtt', isZtt, 'isZtt/F')
    isZmt = array('f', [ 0 ] )
    isZmtB = tnew.Branch('isZmt', isZmt, 'isZmt/F')
    isZet = array('f', [ 0 ] )
    isZetB = tnew.Branch('isZet', isZet, 'isZet/F')
    isZee = array('f', [ 0 ] )
    isZeeB = tnew.Branch('isZee', isZee, 'isZee/F')
    isZmm = array('f', [ 0 ] )
    isZmmB = tnew.Branch('isZmm', isZmm, 'isZmm/F')
    isZem = array('f', [ 0 ] )
    isZemB = tnew.Branch('isZem', isZem, 'isZem/F')
    isZEE = array('f', [ 0 ] )
    isZEEB = tnew.Branch('isZEE', isZEE, 'isZEE/F')
    isZMM = array('f', [ 0 ] )
    isZMMB = tnew.Branch('isZMM', isZMM, 'isZMM/F')
    isZTT = array('f', [ 0 ] )
    isZTTB = tnew.Branch('isZTT', isZTT, 'isZTT/F')
    isZLL = array('f', [ 0 ] )
    isZLLB = tnew.Branch('isZLL', isZLL, 'isZLL/F')


    # add dummy decaymode vars in to EMu channel for cut strings later
    if channel != 'tt' :
        t1DecayMode = array('f', [ 0 ] )
        t1DecayModeB = tnew.Branch('t1DecayMode', t1DecayMode, 't1DecayMode/F')
        t2DecayMode = array('f', [ 0 ] )
        t2DecayModeB = tnew.Branch('t2DecayMode', t2DecayMode, 't2DecayMode/F')
    if channel == 'em' or channel == 'tt' :
        tDecayMode = array('f', [ 0 ] )
        tDecayModeB = tnew.Branch('tDecayMode', tDecayMode, 'tDecayMode/F')

    ''' Now actually fill that instance of an evtFake'''
    count2 = 0
    for row in told:
        run = int( row.run )
        lumi = int( row.lumi )
        evt = int( row.evt )
        
        currentEvt = getCurrentEvt( channel, row )
        currentRunLumiEvt = (run, lumi, evt)

        
        if currentRunLumiEvt in toFillMap.keys() and currentEvt == toFillMap[ currentRunLumiEvt ] :
            #print "Fill choice:",currentRunLumiEvt, currentEvt

            if channel == 'tt' and 'Sync-HtoTT' in sample : 
                #print "### Iso Ordering %s ###" % sample
                isoOrder( channel, row )
            vbfClean( row )


            isZtt[0] = 0
            isZmt[0] = 0
            isZet[0] = 0
            isZee[0] = 0
            isZmm[0] = 0
            isZem[0] = 0
            isZEE[0] = 0
            isZMM[0] = 0
            isZTT[0] = 0
            isZLL[0] = 0

            # Decay final states
            if channel == 'tt' :
                isZtt[0] = 1
            if channel == 'et' :
                isZet[0] = 1
            if channel == 'mt' :
                isZmt[0] = 1
            if channel == 'em' :
                isZem[0] = 1
            # Generator states, combine Z & sm-H into 1 var
            if row.isZee == 1 :#or row.isHee == 1 : 
                isZEE[0] = 1
            if row.isZmumu == 1 :#or row.isHmumu == 1 : 
                isZMM[0] = 1
            if row.isZtautau == 1 :#or row.isHtautau == 1 : 
                isZTT[0] = 1
            if isZEE[0] == 1 or isZMM[0] == 1 : isZLL[0] = 1
            UniqueID[0] = sampDict[ shortName ]['UniqueID']
            BkgGroup[0] = sampDict[ shortName ]['BkgGroup']

            # TES Shifted M_Vis
            if 'DYJets' in sample or 'ggH' in sample or 'bbH' in sample or 'VBH' in sample :
                m_vis_UP[0] = mVisTES( l1, l2, row, 0.03 )
                m_vis_DOWN[0] = mVisTES( l1, l2, row, -0.03 )
            else :
                m_vis_UP[0] = getattr( row, '%s_%s_Mass' % (l1, l2) )
                m_vis_DOWN[0] = getattr( row, '%s_%s_Mass' % (l1, l2) )
                if hasattr( row, 'm_sv_UP' ) :
                    setattr( row, 'm_sv_UP', getattr( row, 'm_sv' ) )
                    setattr( row, 'm_sv_DOWN', getattr( row, 'm_sv' ) )
                    setattr( row, 'mt_sv_UP', getattr( row, 'mt_sv' ) )
                    setattr( row, 'mt_sv_DOWN', getattr( row, 'mt_sv' ) )


            # Channel specific vetoes
            if channel == 'tt' :
                extramuon_veto[0] = getattr( row, "muVetoZTTp001dxyzR0" )
                extraelec_veto[0] = getattr( row, "eVetoZTTp001dxyzR0" )
            if channel == 'em' :
                extramuon_veto[0] = getattr( row, "muVetoZTTp001dxyz" )
                extraelec_veto[0] = getattr( row, "eVetoZTTp001dxyz" )
            if channel == 'et' :
                extramuon_veto[0] = getattr( row, "muVetoZTTp001dxyzR0" )
                extraelec_veto[0] = getattr( row, "eVetoZTTp001dxyz" )
            if channel == 'mt' :
                extramuon_veto[0] = getattr( row, "muVetoZTTp001dxyz" )
                extraelec_veto[0] = getattr( row, "eVetoZTTp001dxyzR0" )
            
            mvacov00[0] = getattr( row, "%s_%s_MvaMetCovMatrix00" % (l1, l2) )
            mvacov01[0] = getattr( row, "%s_%s_MvaMetCovMatrix01" % (l1, l2) )
            mvacov10[0] = getattr( row, "%s_%s_MvaMetCovMatrix10" % (l1, l2) )
            mvacov11[0] = getattr( row, "%s_%s_MvaMetCovMatrix11" % (l1, l2) )

            # Channel specific pairwise mvaMet
            if channel == 'tt' :
                if hasattr( row, "mvamet" ) and hasattr( row, "mvametphi" ) :
                    pzetamiss[0] = compZeta(row.t1Pt, row.t1Phi, row.t2Pt, row.t2Phi, row.mvamet, row.mvametphi)[1]
                    mt_1[0] = getTransMass( row.mvamet, row.mvametphi, row.t1Pt, row.t1Phi )
                    mt_2[0] = getTransMass( row.mvamet, row.mvametphi, row.t2Pt, row.t2Phi )
                else :
                    pzetamiss[0] = -9999
                    mt_1[0] = -9999
                    mt_2[0] = -9999
            if channel == 'em' :
                if hasattr( row, "mvamet" ) and hasattr( row, "mvametphi" ) :
                    pzetamiss[0] = compZeta(row.ePt, row.ePhi, row.mPt, row.mPhi, row.mvamet, row.mvametphi)[1]
                    mt_1[0] = getTransMass( row.mvamet, row.mvametphi, row.ePt, row.ePhi )
                    mt_2[0] = getTransMass( row.mvamet, row.mvametphi, row.mPt, row.mPhi )
                else :
                    pzetamiss[0] = -9999
                    mt_1[0] = -9999
                    mt_2[0] = -9999

            # Data specific vars
            if 'data' in sample :
                puweight[0] = 1
                trigweight_1[0] = 1
                idisoweight_1[0] = 1
                idisoweight_2[0] = 1
                XSecLumiWeight[0] = 1
                isZEE[0] = -1
                isZMM[0] = -1
                isZLL[0] = -1
            else :
                nTrPu = ( math.floor(row.nTruePU * 10))/10
                puweight[0] = puDict[ nTrPu ]
                l1Pt = getattr( row, '%sPt' % l1 )
                l1Eta = getattr( row, '%sEta' % l1 )
                l2Pt = getattr( row, '%sPt' % l2 )
                l2Eta = getattr( row, '%sEta' % l2 )

                # Isolation / ID weights
                if 't' in l1 : idisoweight_1[0] = 1
                else : idisoweight_1[0] = lepWeights.getWeight( l1, 'IdIso', l1Pt, l1Eta )
                if 't' in l2 : idisoweight_2[0] = 1
                else : idisoweight_2[0] = lepWeights.getWeight( l2, 'IdIso', l2Pt, l2Eta )

                # Trigger Weights
                effweight[0] = 1
                if channel == 'et' : trigweight_1[0] = lepWeights.getWeight( l1, 'Trig', l1Pt, l1Eta )
                elif channel == 'mt' : trigweight_1[0] = lepWeights.getWeight( l1, 'Trig', l1Pt, l1Eta )
                elif channel == 'em' : trigweight_1[0] = lepWeights.getEMTrigWeight( l1Pt, l1Eta, l2Pt, l2Eta )
                elif channel == 'tt' :
                    trigweight_1[0] = 1
                    effweight[0] = doubleTauTriggerEff( l1Pt ) * doubleTauTriggerEff( l2Pt )
                else : trigweight_1[0] = 1

                weight[0] = puweight[0] * idisoweight_1[0] * idisoweight_2[0]
                weight[0] *= trigweight_1[0] * effweight[0]

                # Special weighting for WJets and DYJets
                if shortName in ['DYJets', 'DYJetsBig', 'WJets'] :
                    xsec = getXSec( shortName, sampDict, row.numGenJets )
                    #print "\n Sampe: %s    ShortNAme: %s    xsec: %f     numGenJets %i" % (sample, shortName, xsec, row.numGenJets)
                # If not WJets or DYJets fill from xsec defined before
                XSecLumiWeight[0] = xsec
 

            tnew.Fill()
            count2 += 1


    #print "Count: %i count2: %i" % (count, count2)
    #print "%25s : %10i" % ('Iso Selected', count2)
    isoQty = "%25s : %10i" % ('Iso Selected', count2)
    # write to disk
    tnew.write()
    fnew.close()
    return isoQty

