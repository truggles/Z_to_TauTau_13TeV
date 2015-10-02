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

tauIso = {
    'Pt' : 'pt',
    'Eta' : 'eta',
    'Phi' : 'phi',
    'Mass' : 'm',
    'Charge' : 'q',
    'PVDXY' : 'd0',
    'PVDZ' : 'dZ',
    'MtToMET' : 'mt',
    'ByCombinedIsolationDeltaBetaCorrRaw3Hits' : 'iso',
    'AgainstElectronLooseMVA5' : 'againstElectronLooseMVA5',
    'AgainstElectronMediumMVA5' : 'againstElectronMediumMVA5',
    'AgainstElectronTightMVA5' : 'againstElectronTightMVA5',
    'AgainstElectronVLooseMVA5' : 'againstElectronVLooseMVA5',
    'AgainstElectronVTightMVA5' : 'againstElectronVTightMVA5',
    'AgainstMuonLoose3' : 'againstMuonLoose3',
    #'AgainstMuonLoose' : 'againstMuonLoose',
    'ChargedIsoPtSum' : 'chargedIsoPtSum',
    'DecayModeFindingNewDMs' : 'decayModeFindingOldDMs',
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
    'MtToPFMET' : '',
    'MtToPfMet_Ty1' : '',
    'MtToPfMet_jes' : '',
    'MtToPfMet_mes' : '',
    'MtToPfMet_tes' : '',
    'MtToPfMet_ues' : '',
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

def calcDR( eta1, phi1, eta2, phi2 ) :
    return float(math.sqrt( (eta1-eta2)*(eta1-eta2) + (phi1-phi2)*(phi1-phi2) ))

''' Functions for cleaning jets in DR = X around final state objs '''
jetVars = ['Pt', 'BJetCISV', 'PUMVA']

def jetCleaning( channel, row, DR ) :
    if channel == 'em' :
        l1 = 'e'
        l2 = 'm'
    if channel == 'tt' :
        l1 = 't1'
        l2 = 't2'

    l1Eta = getattr( row, '%sEta' % l1 )
    l1Phi = getattr( row, '%sPhi' % l1 )
    l2Eta = getattr( row, '%sEta' % l2 )
    l2Phi = getattr( row, '%sPhi' % l2 )

    jetDict = {} # Order this thing Eta, Phi, Pt, BJetCISV, PUMVA
    for i in range (1, 5) :
        jEta = getattr( row, 'jet%iEta' % i )
        jPhi = getattr( row, 'jet%iPhi' % i )
        jPt = getattr( row, 'jet%iPt' % i )
        jBJetCISV = getattr( row, 'jet%iBJetCISV' % i )
        jPUMVA = getattr( row, 'jet%iPUMVA' % i )
        jetDict['jet%i' % i] = ( jEta, jPhi, jPt, jBJetCISV, jPUMVA )

    jet1okay = False
    jet2okay = False

    while not jet1okay :
        # If jet1 overlaps at all remove it, shift other jets up, and give -999 to jet4
        if ( calcDR( l1Eta, l1Phi, jetDict['jet1'][0], jetDict['jet1'][1] ) < DR ) \
            or ( calcDR( l2Eta, l2Phi, jetDict['jet1'][0], jetDict['jet1'][1] ) < DR ) :
            jetDict['jet1'] = jetDict['jet2']
            jetDict['jet2'] = jetDict['jet3']
            jetDict['jet3'] = jetDict['jet4']
            jetDict['jet4'] = (-999, -999, -999, -999, -999)
        else : jet1okay = True

    while not jet2okay :
        # If jet2 overlaps at all remove it, shift other jets up, and give -999 to jet4
        if ( calcDR( l1Eta, l1Phi, jetDict['jet2'][0], jetDict['jet2'][1] ) < DR ) \
            or ( calcDR( l2Eta, l2Phi, jetDict['jet2'][0], jetDict['jet2'][1] ) < DR ) :
            jetDict['jet2'] = jetDict['jet3']
            jetDict['jet3'] = jetDict['jet4']
            jetDict['jet4'] = (-999, -999, -999, -999, -999)
        else : jet2okay = True

    for i in range (1, 5) :
        setattr( row, 'jet%iEta' % i, jetDict['jet%i' % i][0] )
        setattr( row, 'jet%iPhi' % i, jetDict['jet%i' % i][1] )
        setattr( row, 'jet%iPt' % i, jetDict['jet%i' % i][2] )
        setattr( row, 'jet%iBJetCISV' % i, jetDict['jet%i' % i][3] )
        setattr( row, 'jet%iPUMVA' % i, jetDict['jet%i' % i][4] )


def renameBranches( grouping, mid1, mid2, sample, channel ) :
    branchMappingEM = {
        'run' : 'run',
        'lumi' : 'lumi',
        'evt' : 'evt',
        'charge' : 'charge',
        'ePt' : 'pt_1', # rename ePt to pt_1
        'eEta' : 'eta_1',
        'ePhi' : 'phi_1',
        'eMass' : 'm_1',
        'eCharge' : 'q_1',
        'ePVDXY' : 'd0_1',
        'ePVDZ' : 'dZ_1',
        'eMtToMET' : 'mt_1',
        'eIsoDB03' : 'iso_1',
        'mPt' : 'pt_2',
        'mEta' : 'eta_2',
        'mPhi' : 'phi_2',
        'mMass' : 'm_2',
        'mCharge' : 'q_2',
        'mPVDXY' : 'd0_2',
        'mPVDZ' : 'dZ_2',
        'mMtToMET' : 'mt_2',
        'mIsoDB03' : 'iso_2',
        'jet1Pt' : 'jpt_1',
        'jet1Phi' : 'jphi_1',
        'jet1Eta' : 'jeta_1',
        'jet2Pt' : 'jpt_2',
        'jet2Phi' : 'jphi_2',
        'jet2Eta' : 'jeta_2',
        'muVetoZTT10new2' : 'extramuon_veto',
        'eVetoZTT10new2' : 'extraelec_veto',
        'e_m_Mass' : 'm_vis',
        'pfMetEt' : 'met',
        'pfMetPhi' : 'metphi',
        #'mvaMetEt' : 'mvamet',
        #'mvaMetPhi' : 'mvametphi',
        #'GenWeight' : 'weight',
        'bjetCISVVeto20MediumZTT' : 'nbtag',
        'jetVeto20ZTT' : 'njetspt20',
        }
    
    branchMappingTT = {
        'run' : 'run',
        'lumi' : 'lumi',
        'evt' : 'evt',
        'charge' : 'charge',
        't1Pt' : 'pt_1',
        't1Eta' : 'eta_1',
        't1Phi' : 'phi_1',
        't1Mass' : 'm_1',
        't1Charge' : 'q_1',
        't1PVDXY' : 'd0_1',
        't1PVDZ' : 'dZ_1',
        't1MtToMET' : 'mt_1',
        't1ByCombinedIsolationDeltaBetaCorrRaw3Hits' : 'iso_1',
        't1AgainstElectronLooseMVA5' : 'againstElectronLooseMVA5_1',
        't1AgainstElectronMediumMVA5' : 'againstElectronMediumMVA5_1',
        't1AgainstElectronTightMVA5' : 'againstElectronTightMVA5_1',
        't1AgainstElectronVLooseMVA5' : 'againstElectronVLooseMVA5_1',
        't1AgainstElectronVTightMVA5' : 'againstElectronVTightMVA5_1',
        't1AgainstMuonLoose3' : 'againstMuonLoose3_1',
        #'t1AgainstMuonLoose' : 'againstMuonLoose_1',
        't1ChargedIsoPtSum' : 'chargedIsoPtSum_1',
        't1DecayModeFindingNewDMs' : 'decayModeFindingOldDMs_1',
        't1NeutralIsoPtSum' : 'neutralIsoPtSum_1',
        't1PuCorrPtSum' : 'puCorrPtSum_1',
        #'t1ByIsolationMVA3newDMwLTraw' : 'byIsolationMVA3newDMwLTraw_1',
        #'t1ByIsolationMVA3newDMwoLTraw' : 'byIsolationMVA3newDMwoLTraw_1',
        #'t1ByIsolationMVA3oldDMwLTraw' : 'byIsolationMVA3oldDMwLTraw_1',
        #'t1ByIsolationMVA3oldDMwoLTraw' : 'byIsolationMVA3oldDMwoLTraw_1',
        't2Pt' : 'pt_2',
        't2Eta' : 'eta_2',
        't2Phi' : 'phi_2',
        't2Mass' : 'm_2',
        't2Charge' : 'q_2',
        't2PVDXY' : 'd0_2',
        't2PVDZ' : 'dZ_2',
        't2MtToMET' : 'mt_2',
        't2ByCombinedIsolationDeltaBetaCorrRaw3Hits' : 'iso_2',
        't2AgainstElectronLooseMVA5' : 'againstElectronLooseMVA5_2',
        't2AgainstElectronMediumMVA5' : 'againstElectronMediumMVA5_2',
        't2AgainstElectronTightMVA5' : 'againstElectronTightMVA5_2',
        't2AgainstElectronVLooseMVA5' : 'againstElectronVLooseMVA5_2',
        't2AgainstElectronVTightMVA5' : 'againstElectronVTightMVA5_2',
        't2AgainstMuonLoose3' : 'againstMuonLoose3_2',
        #'t2AgainstMuonLoose' : 'againstMuonLoose_2',
        't2ChargedIsoPtSum' : 'chargedIsoPtSum_2',
        't2DecayModeFindingNewDMs' : 'decayModeFindingOldDMs_2',
        't2NeutralIsoPtSum' : 'neutralIsoPtSum_2',
        't2PuCorrPtSum' : 'puCorrPtSum_2',
        #'t2ByIsolationMVA3newDMwLTraw' : 'byIsolationMVA3newDMwLTraw_2',
        #'t2ByIsolationMVA3newDMwoLTraw' : 'byIsolationMVA3newDMwoLTraw_2',
        #'t2ByIsolationMVA3oldDMwLTraw' : 'byIsolationMVA3oldDMwLTraw_2',
        #'t2ByIsolationMVA3oldDMwoLTraw' : 'byIsolationMVA3oldDMwoLTraw_2',
        'jet1Pt' : 'jpt_1',
        'jet1Phi' : 'jphi_1',
        'jet1Eta' : 'jeta_1',
        'jet2Pt' : 'jpt_2',
        'jet2Phi' : 'jphi_2',
        'jet2Eta' : 'jeta_2',
        'muVetoZTT10new2' : 'extramuon_veto',
        'eVetoZTT10new2' : 'extraelec_veto',
        't1_t2_Mass' : 'm_vis',
        'pfMetEt' : 'met',
        'pfMetPhi' : 'metphi',
        #'mvaMetEt' : 'mvamet',
        #'mvaMetPhi' : 'mvametphi',
        #'GenWeight' : 'weight',
        'bjetCISVVeto20MediumZTT' : 'nbtag',
        'jetVeto20ZTT' : 'njetspt20',
        }


    if channel == 'em' : branchMapping = branchMappingEM
    if channel == 'tt' : branchMapping = branchMappingTT

    oldFileName = '%s%s/%s.root' % (grouping, mid1, sample)
    newFileName = '%s%s/%s.root' % (grouping, mid2, sample)
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
        
        if channel == 'em' :
            leg1Iso = row.eRelPFIsoDB
            leg1Pt = row.ePt
            leg2Iso = row.mRelPFIsoDBDefault
            leg2Pt = row.mPt
            currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)

        if channel == 'tt' :
            ''' Get our Iso ordering for TT right for the get go '''
            leg1Iso = row.t1ByCombinedIsolationDeltaBetaCorrRaw3Hits
            leg1Pt = row.t1Pt
            leg2Iso = row.t2ByCombinedIsolationDeltaBetaCorrRaw3Hits
            leg2Pt = row.t2Pt
            if leg1Iso < leg2Iso :
                currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)
            elif leg1Iso > leg2Iso :
                currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt)
            elif leg1Pt > leg2Pt :
                currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)
            elif leg1Pt < leg2Pt :
                currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt)
            else : print "XXXX"


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
    


    ''' Now actually fill that instance of an evt '''
    count2 = 0
    for row in told:
        run = int( row.run )
        lumi = int( row.lumi )
        evt = int( row.evt )
        
        if channel == 'em' :
            leg1Iso = row.eRelPFIsoDB
            leg1Pt = row.ePt
            leg2Iso = row.mRelPFIsoDBDefault
            leg2Pt = row.mPt
            currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)

        if channel == 'tt' :
            leg1Iso = row.t1ByCombinedIsolationDeltaBetaCorrRaw3Hits
            leg1Pt = row.t1Pt
            leg2Iso = row.t2ByCombinedIsolationDeltaBetaCorrRaw3Hits
            leg2Pt = row.t2Pt
            if leg1Iso < leg2Iso :
                currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)
            elif leg1Iso > leg2Iso :
                currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt)
            elif leg1Pt > leg2Pt :
                currentEvt = (leg1Iso, leg1Pt, leg2Iso, leg2Pt)
            elif leg1Pt < leg2Pt :
                currentEvt = (leg2Iso, leg2Pt, leg1Iso, leg1Pt)
            else : print "XXXX"

        currentRunLumiEvt = (run, lumi, evt)
        
        if currentRunLumiEvt in toFillMap.keys() and currentEvt == toFillMap[ currentRunLumiEvt ] :
            #print "Fill choice:",currentRunLumiEvt, currentEvt
            isoOrder( channel, row )
            jetCleaning( channel, row, 0.5 )
            tnew.Fill()
            count2 += 1


    #print "Count: %i count2: %i" % (count, count2)
    print "%25s : %10i" % ('Iso Selected', count2)
    # write to disk
    tnew.write()
    fnew.close()

