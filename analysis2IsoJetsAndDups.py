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

cmsLumi = float( os.getenv('_LUMI_', '2170.0') )

prodMap = {
    'em' : ('e', 'm'),
    'et' : ('e', 't'),
    'mt' : ('m', 't'),
    'tt' : ('t1', 't2'),
}

def getXSec( shortName, sampDict ) :
    htts = ['100-200', '200-400', '400-600', '600-Inf']
    scaler1 = cmsLumi * sampDict[ shortName ]['Cross Section (pb)'] / ( sampDict[ shortName ]['summedWeightsNorm'] )
    if 'QCD' in shortName : return scaler1
    if 'data' in shortName : return 1.0
    for htt in htts :
        if htt in shortName :
            scaler2 = cmsLumi * sampDict[ shortName[:-7] ]['Cross Section (pb)'] / ( sampDict[ shortName[:-7] ]['summedWeightsNorm'] )
            return 1/( (1/scalar1) + (1/scalar2) )
    return scalar1

def leptonWeights( idMap, isoMap ) :
    print 'Hi'

def getIso( cand, row ) :
    if 'e' in cand :
        return getattr(row, cand+'RelPFIsoDB')
    if 'm' in cand :
        return getattr(row, cand+'RelPFIsoDBDefault')
    if 't' in cand :
        return getattr(row, cand+'ByCombinedIsolationDeltaBetaCorrRaw3Hits')
        
        
def getCurrentEvt( channel, row ) :
    l1 = prodMap[channel][0]
    l2 = prodMap[channel][1]
    leg1Iso = getIso( l1, row )
    leg2Iso = getIso( l2, row )
    leg1Pt = getattr(row, l1+'Pt')
    leg2Pt = getattr(row, l2+'Pt')

    if channel == 'tt' :
        if leg1Iso < leg2Iso :
            currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)
        elif leg1Iso > leg2Iso :
            currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt)
        elif leg1Pt > leg2Pt :
            currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)
        elif leg1Pt < leg2Pt :
            currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt)
        else : print "Iso1 == Iso2 & Pt1 == Pt2", row.evt
    else : currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)
    return currentEvt


tauIso = {
    'Pt' : 'pt',
    'Eta' : 'eta',
    'Phi' : 'phi',
    'Mass' : 'm',
    'Charge' : 'q',
    'PVDXY' : 'd0',
    'PVDZ' : 'dZ',
    'MtToPfMet_Raw' : 'mt',
    'MtToPfMet_type1' : '',
    'ByCombinedIsolationDeltaBetaCorrRaw3Hits' : 'iso',
    'AgainstElectronLooseMVA5' : 'againstElectronLooseMVA5',
    'AgainstElectronMediumMVA5' : 'againstElectronMediumMVA5',
    'AgainstElectronTightMVA5' : 'againstElectronTightMVA5',
    'AgainstElectronVLooseMVA5' : 'againstElectronVLooseMVA5',
    'AgainstElectronVTightMVA5' : 'againstElectronVTightMVA5',
    'AgainstMuonLoose3' : 'againstMuonLoose3',
    #'AgainstMuonLoose' : 'againstMuonLoose',
    'ChargedIsoPtSum' : 'chargedIsoPtSum',
    #'DecayModeFindingNewDMs' : 'decayModeFindingOldDMs',
    'NeutralIsoPtSum' : 'neutralIsoPtSum',
    'PuCorrPtSum' : 'puCorrPtSum',
    #'ByIsolationMVA3newDMwLTraw' : 'byIsolationMVA3newDMwLTraw',
    #'ByIsolationMVA3newDMwoLTraw' : 'byIsolationMVA3newDMwoLTraw',
    #'ByIsolationMVA3oldDMwLTraw' : 'byIsolationMVA3oldDMwLTraw',
    #'ByIsolationMVA3oldDMwoLTraw' : 'byIsolationMVA3oldDMwoLTraw',
    'AbsEta' : '',
    #'AgainstElectronLoose' : '',
    'AgainstElectronMVA5category' : '',
    'AgainstElectronMVA5raw' : '',
    #'AgainstElectronMedium' : '',
    #'AgainstElectronTight' : '',
    #'AgainstMuonLoose2' : '',
    'DecayMode' : '',
    'DecayModeFinding' : '',
    'DoubleTau40Filter' : '',
    'ElecOverlap' : '',
    'ElectronPt10IdIsoVtxOverlap' : '',
    'ElectronPt10IdVtxOverlap' : '',
    'ElectronPt15IdIsoVtxOverlap' : '',
    'ElectronPt15IdVtxOverlap' : '',
    'GenDecayMode' : '',
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
    'MuOverlap' : '',
    'MuonIdIsoStdVtxOverlap' : '',
    'MuonIdIsoVtxOverlap' : '',
    'MuonIdVtxOverlap' : '',
    'NearestZMass' : '',
    'Rank' : '',
    'TNPId' : '',
    'ToMETDPhi' : '',
    'VZ' : '',
}

def isoOrder( channel, row ) :
    if channel != 'tt' : return
    iso1 = getattr( row, 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits' )
    iso2 = getattr( row, 't2ByCombinedIsolationDeltaBetaCorrRaw3Hits' )
    pt1 = getattr( row, 't1Pt' )
    pt2 = getattr( row, 't2Pt' )
    if iso2 < iso1 :
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



def renameBranches( grouping, mid1, mid2, sample, channel, bkgFlag ) :
    with open('meta/NtupleInputs_%s/samples.json' % grouping) as sampFile :
        sampDict = json.load( sampFile )

    shortName = sample.split('_')[0]
    if shortName == 'data' : shortName = 'data_%s' % channel
    UniqueID[0] = sampDict[ shortName ]['UniqueID']
    BkgGroup[0] = sampDict[ shortName ]['BkgGroup']

    xsec = getXSec( shortName, sampDict )

    l1 = prodMap[channel][0]
    l2 = prodMap[channel][1]

    from util.lepSF import getSF, sfHistos
    elec12TrigMap = getSF( 'Electron_Ele12_eff' )
    elec12TrigSF = sfHistos( elec12TrigMap )
    elec17TrigMap = getSF( 'Electron_Ele17_eff' )
    elec17TrigSF = sfHistos( elec17TrigMap )
    elecIdIso0p10Map = getSF( 'Electron_IdIso0p10_eff' )
    elecIdIso0p10SF = sfHistos( elecIdIso0p10Map )
    elecIdIso0p15Map = getSF( 'Electron_IdIso0p15_eff' )
    elecIdIso0p15SF = sfHistos( elecIdIso0p15Map )
    elecSingleEffMap = getSF( 'Electron_SingleEle_eff' )
    elecSingleEffSF = sfHistos( elecSingleEffMap )
    muon8TrigMap = getSF( 'Muon_Mu8_eff' )
    muon8TrigSF = sfHistos( muon8TrigMap )
    muon17TrigMap = getSF( 'Muon_Mu17_eff' )
    muon17TrigSF = sfHistos( muon17TrigMap )
    muonIdIso0p10Map = getSF( 'Muon_IdIso0p10_eff' )
    muonIdIso0p10SF = sfHistos( muonIdIso0p10Map )
    muonIdIso0p15Map = getSF( 'Muon_IdIso0p15_eff' )
    muonIdIso0p15SF = sfHistos( muonIdIso0p15Map )
    muonSingleEffMap = getSF( 'Muon_SingleMu_eff' )
    muonSingleEffSF = sfHistos( muonSingleEffMap )

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
        'j1mva' : 'jmva_1',
        'j2pt' : 'jpt_2',
        'j2phi' : 'jphi_2',
        'j2eta' : 'jeta_2',
        'j2mva' : 'jmva_2',
        'jb1pt' : 'bpt_1',
        'jb1phi' : 'bphi_1',
        'jb1eta' : 'beta_1',
        'jb1mva' : 'bmva_1',
        'jb1csv' : 'bcsv_1',
        'jb2pt' : 'bpt_2',
        'jb2phi' : 'bphi_2',
        'jb2eta' : 'beta_2',
        'jb2mva' : 'bmva_2',
        'jb2csv' : 'bcsv_2',
        'muVetoZTT10new2' : 'extramuon_veto',
        'eVetoZTT10new2' : 'extraelec_veto',
        #'mvaMetEt' : 'mvamet',
        #'mvaMetPhi' : 'mvametphi',
        'bjetCISVVeto20MediumZTT' : 'nbtag',
        'jetVeto20ZTT' : 'njetspt20',
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
        'PZeta' : 'pzetamis',
        'PZetaVis' : 'pzetavis',
        'SS' : 'Z_SS',
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
        'cand_MtToPfMet_Raw' : 'mt',
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
        'cand_MtToPfMet_Raw' : 'mt',
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
        'cand_ByCombinedIsolationDeltaBetaCorrRaw3Hits' : 'iso',
        'cand_AgainstElectronLooseMVA5' : 'againstElectronLooseMVA5',
        'cand_AgainstElectronMediumMVA5' : 'againstElectronMediumMVA5',
        'cand_AgainstElectronTightMVA5' : 'againstElectronTightMVA5',
        'cand_AgainstElectronVLooseMVA5' : 'againstElectronVLooseMVA5',
        'cand_AgainstElectronVTightMVA5' : 'againstElectronVTightMVA5',
        'cand_AgainstMuonLoose3' : 'againstMuonLoose3',
        #cand_AgainstMuonLoose' : 'againstMuonLoose',
        'cand_ChargedIsoPtSum' : 'chargedIsoPtSum',
        'cand_DecayModeFinding' : 'decayModeFindingOldDMs',
        'cand_NeutralIsoPtSum' : 'neutralIsoPtSum',
        'cand_PuCorrPtSum' : 'puCorrPtSum',
        #cand_ByIsolationMVA3newDMwLTraw' : 'byIsolationMVA3newDMwLTraw',
        #cand_ByIsolationMVA3newDMwoLTraw' : 'byIsolationMVA3newDMwoLTraw',
        #cand_ByIsolationMVA3oldDMwLTraw' : 'byIsolationMVA3oldDMwLTraw',
        #cand_ByIsolationMVA3oldDMwoLTraw' : 'byIsolationMVA3oldDMwoLTraw',
        'cand_MtToPfMet_Raw' : 'mt',
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
    intBranches = set(['run', 'evt', 'lumi', 'isdata', 'pvIsValid', 'pvIsFake'])
    
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
    prevEvt = (999, 0, 999, 0)
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
        # lowest iso_1
        if currentEvt[ 0 ] < prevEvt[ 0 ] :
            prevEvt = currentEvt
        # iso_1 equal
        elif currentEvt[ 0 ] == prevEvt[ 0 ] :
            # highest pt_1
            if currentEvt[ 1 ] > prevEvt[ 1 ] :
                prevEvt = currentEvt
            # pt_1 equal
            if currentEvt[ 1 ] == prevEvt[ 1 ] :
                # lowest iso_2
                if currentEvt[ 2 ] < prevEvt[ 2 ] :
                    prevEvt = currentEvt
                # iso_2 equal
                if currentEvt[ 2 ] == prevEvt[ 2 ] :
                    # highest pt_2
                    if currentEvt[ 3 ] > prevEvt[ 3 ] :
                        prevEvt = currentEvt

        # Make sure we get the last event
        if count == numRows :
            #print "LastRow:",prevRunLumiEvt, prevEvt
            prevRunLumiEvt = currentRunLumiEvt
            prevEvt = currentEvt
            toFillMap[ prevRunLumiEvt ] = prevEvt
    
    ''' Add a nvtx Pile UP weighting variable to the new tree
    see util.pileUpVertexCorrections.addNvtxWeight for inspiration '''
    from util.pileUpVertexCorrections import PUreweight
    from array import array
    puDict = PUreweight( channel )

    ''' We are calculating and adding these below variables to our new tree
    PU Weighting '''
    puweight = array('f', [ 0 ] )
    puweightB = tnew.Branch('puweight', puweight, 'puweight/F')
    XSecLumiWeight = array('f', [ 0 ] )
    XSecLumiWeightB = tnew.Branch('XSecLumiWeight', XSecLumiWeight, 'XSecLumiWeight/F')
    l1TrigWeight = array('f', [ 0 ] )
    l1TrigWeightB = tnew.Branch('l1TrigWeight', l1TrigWeight, 'l1TrigWeight/F')
    l1IsoIDWeight = array('f', [ 0 ] )
    l1IsoIDWeightB = tnew.Branch('l1IsoIDWeight', l1IsoIDWeight, 'l1IsoIDWeight/F')
    l1EffWeight = array('f', [ 0 ] )
    l1EffWeightB = tnew.Branch('l1EffWeight', l1EffWeight, 'l1EffWeight/F')
    l2TrigWeight = array('f', [ 0 ] )
    l2TrigWeightB = tnew.Branch('l2TrigWeight', l2TrigWeight, 'l2TrigWeight/F')
    l2IsoIDWeight = array('f', [ 0 ] )
    l2IsoIDWeightB = tnew.Branch('l2IsoIDWeight', l2IsoIDWeight, 'l2IsoIDWeight/F')
    l2EffWeight = array('f', [ 0 ] )
    l2EffWeightB = tnew.Branch('l2EffWeight', l2EffWeight, 'l2EffWeight/F')
    UniqueID = array('f', [ 0 ] )
    UniqueIDB = tnew.Branch('UniqueID', UniqueID, 'UniqueID/F')
    BkgGroup = array('f', [ 0 ] )
    BkgGroupB = tnew.Branch('BkgGroup', BkgGroup, 'BkgGroup/F')
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

            if 'data' in sample :
                puweight[0] = 1
                l1TrigWeight[0] = 1
                l1IsoIDWeight[0] = 1
                l1EffWeight[0] = 1
                l2TrigWeight[0] = 1
                l2IsoIDWeight[0] = 1
                l2EffWeight[0] = 1
                XSecLumiWeight[0] = 1
                isZEE[0] = -1
                isZMM[0] = -1
                isZLL[0] = -1
            else :
                nTrPu = ( math.floor(row.nTruePU * 10))/10
                puweight[0] = puDict[ nTrPu ]
                l1TrigWeight[0] = 1
                l1IsoIDWeight[0] = 1
                l1EffWeight[0] = 1
                l2TrigWeight[0] = 1
                l2IsoIDWeight[0] = 1
                l2EffWeight[0] = 1
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

