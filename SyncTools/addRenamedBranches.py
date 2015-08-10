
############################################################################
#   Rename my branches for the HTT 2015 Sync                               #
############################################################################

import ROOT
from array import array

def makeNewTree( dir_, sample, channel ) :
    ifile = ROOT.TFile('%s.root' % sample, 'r')
    d1 = ifile.Get( channel )
    inTree = d1.Get( 'Ntuple' )
    
    ofile = ROOT.TFile('%s/SYNCFILE_SUSYGluGluToHToTauTau_M-160_%s_spring15.root' % (dir_, channel), 'RECREATE')
    directory = ofile.mkdir( channel )
    directory.cd()
    
    outTree = inTree.CopyTree( '' )
    ofile.Write()

legMap = {
    'e' : '_1',
    'm' : '_2',
    't1' : '_1',
    't2' : '_2'}

def addBranches( dir_, sample, channel, leg ) :
    lep = leg
    if channel == 'em': zProd = ['e', 'm']
    if channel == 'tt': zProd = ['t1', 't2']
    treeFile = ROOT.TFile('%s/SYNCFILE_SUSYGluGluToHToTauTau_M-160_%s_spring15.root' % (dir_, channel), 'update')
    d1 = treeFile.Get( '%s' % channel )	
    tree = d1.Get( 'Ntuple' )
    
    pt = array('f', [ 0 ] )
    ptB = tree.Branch('pt%s' % legMap[ lep ], pt, 'pt/F')
    eta = array('f', [ 0 ] )
    etaB = tree.Branch('eta%s' % legMap[ lep ], eta, 'eta/F')
    phi = array('f', [ 0 ] )
    phiB = tree.Branch('phi%s' % legMap[ lep ], phi, 'phi/F')
    m = array('f', [ 0 ] )
    mB = tree.Branch('m%s' % legMap[ lep ], m, 'm/F')
    q = array('f', [ 0 ] )
    qB = tree.Branch('q%s' % legMap[ lep ], q, 'q/F')
    mt = array('f', [ 0 ] )
    mtB = tree.Branch('mt%s' % legMap[ lep ], mt, 'mt/F')
    d0 = array('f', [ 0 ] )
    d0B = tree.Branch('d0%s' % legMap[ lep ], d0, 'd0/F')

    if channel == 'em' :
        dZ = array('f', [ 0 ] )
        dZB = tree.Branch('dZ%s' % legMap[ lep ], dZ, 'dZ/F')

    if channel == 'tt' :
        dZ = array('f', [ 0 ] )
        dZB = tree.Branch('dZ%s' % legMap[ lep ], dZ, 'dZ/F')
        iso = array('f', [ 0 ] )
        isoB = tree.Branch('iso%s' % legMap[ lep ], iso, 'iso/F')
        againstElectronVLooseMVA5 = array('f', [ 0 ] )
        againstElectronVLooseMVA5B = tree.Branch('againstElectronVLooseMVA5%s' % legMap[ lep ], againstElectronVLooseMVA5, 'againstElectronVLooseMVA5/F')
        againstElectronLooseMVA5 = array('f', [ 0 ] )
        againstElectronLooseMVA5B = tree.Branch('againstElectronLooseMVA5%s' % legMap[ lep ], againstElectronLooseMVA5, 'againstElectronLooseMVA5/F')
        againstElectronMediumMVA5 = array('f', [ 0 ] )
        againstElectronMediumMVA5B = tree.Branch('againstElectronMediumMVA5%s' % legMap[ lep ], againstElectronMediumMVA5, 'againstElectronMediumMVA5/F')
        againstElectronTightMVA5 = array('f', [ 0 ] )
        againstElectronTightMVA5B = tree.Branch('againstElectronTightMVA5%s' % legMap[ lep ], againstElectronTightMVA5, 'againstElectronTightMVA5/F')
        againstElectronVTightMVA5 = array('f', [ 0 ] )
        againstElectronVTightMVA5B = tree.Branch('againstElectronVTightMVA5%s' % legMap[ lep ], againstElectronVTightMVA5, 'againstElectronVTightMVA5/F')
        againstMuonLoose3 = array('f', [ 0 ] )
        againstMuonLoose3B = tree.Branch('againstMuonLoose3%s' % legMap[ lep ], againstMuonLoose3, 'againstMuonLoose3/F')
        againstMuonLoose = array('f', [ 0 ] )
        againstMuonLooseB = tree.Branch('againstMuonLoose%s' % legMap[ lep ], againstMuonLoose, 'againstMuonLoose/F')
        chargedIsoPtSum = array('f', [ 0 ] )
        chargedIsoPtSumB = tree.Branch('chargedIsoPtSum%s' % legMap[ lep ], chargedIsoPtSum, 'chargedIsoPtSum/F')
        neutralIsoPtSum = array('f', [ 0 ] )
        neutralIsoPtSumB = tree.Branch('neutralIsoPtSum%s' % legMap[ lep ], neutralIsoPtSum, 'neutralIsoPtSum/F')
        puCorrPtSum = array('f', [ 0 ] )
        puCorrPtSumB = tree.Branch('puCorrPtSum%s' % legMap[ lep ], puCorrPtSum, 'puCorrPtSum/F')
        decayModeFindingOldDMs = array('f', [ 0 ] )
        decayModeFindingOldDMsB = tree.Branch('decayModeFindingOldDMs%s' % legMap[ lep ], decayModeFindingOldDMs, 'decayModeFindingOldDMs/F')
        byIsolationMVA3newDMwoLTraw = array('f', [ 0 ] )
        byIsolationMVA3newDMwoLTrawB = tree.Branch('byIsolationMVA3newDMwoLTraw%s' % legMap[ lep ], byIsolationMVA3newDMwoLTraw, 'byIsolationMVA3newDMwoLTraw/F')
        byIsolationMVA3newDMwLTraw = array('f', [ 0 ] )
        byIsolationMVA3newDMwLTrawB = tree.Branch('byIsolationMVA3newDMwLTraw%s' % legMap[ lep ], byIsolationMVA3newDMwLTraw, 'byIsolationMVA3newDMwLTraw/F')
        byIsolationMVA3oldDMwoLTraw = array('f', [ 0 ] )
        byIsolationMVA3oldDMwoLTrawB = tree.Branch('byIsolationMVA3oldDMwoLTraw%s' % legMap[ lep ], byIsolationMVA3oldDMwoLTraw, 'byIsolationMVA3oldDMwoLTraw/F')
        byIsolationMVA3oldDMwLTraw = array('f', [ 0 ] )
        byIsolationMVA3oldDMwLTrawB = tree.Branch('byIsolationMVA3oldDMwLTraw%s' % legMap[ lep ], byIsolationMVA3oldDMwLTraw, 'byIsolationMVA3oldDMwLTraw/F')
    
    treeFile.cd( '%s' % channel )
    for i in range( tree.GetEntries() ):
        tree.GetEntry( i )
        pt[0] = getattr(tree, '%sPt' % lep)
        ptB.Fill()
        eta[0] = getattr(tree, '%sEta' % lep)
        etaB.Fill()
        phi[0] = getattr(tree, '%sPhi' % lep)
        phiB.Fill()
        m[0] = getattr(tree, '%sMass' % lep)
        mB.Fill()
        q[0] = getattr(tree, '%sCharge' % lep)
        qB.Fill()
        mt[0] = getattr(tree, '%sMtToMET' % lep)
        mtB.Fill()
        d0[0] = getattr(tree, '%sPVDXY' % lep)
        d0B.Fill()
        if channel == 'em' :
            dZ[0] = getattr(tree, '%sPVDZ' % lep)
            dZB.Fill()
        if channel == 'tt' :
            dZ[0] = getattr(tree, '%sVZ' % lep)
            dZB.Fill()
            iso[0] = getattr(tree, '%sByCombinedIsolationDeltaBetaCorrRaw3Hits' % lep)
            isoB.Fill()
            againstElectronVLooseMVA5[0] = getattr(tree, '%sAgainstElectronVLooseMVA5' % lep)
            againstElectronVLooseMVA5B.Fill()
            againstElectronLooseMVA5[0] = getattr(tree, '%sAgainstElectronLooseMVA5' % lep)
            againstElectronLooseMVA5B.Fill()
            againstElectronMediumMVA5[0] = getattr(tree, '%sAgainstElectronMediumMVA5' % lep)
            againstElectronMediumMVA5B.Fill()
            againstElectronTightMVA5[0] = getattr(tree, '%sAgainstElectronTightMVA5' % lep)
            againstElectronTightMVA5B.Fill()
            againstElectronVTightMVA5[0] = getattr(tree, '%sAgainstElectronVTightMVA5' % lep)
            againstElectronVTightMVA5B.Fill()
            againstMuonLoose3[0] = getattr(tree, '%sAgainstMuonLoose3' % lep)
            againstMuonLoose3B.Fill()
            againstMuonLoose[0] = getattr(tree, '%sAgainstMuonLoose' % lep)
            againstMuonLooseB.Fill()
            chargedIsoPtSum[0] = getattr(tree, '%sChargedIsoPtSum' % lep)
            chargedIsoPtSumB.Fill()
            neutralIsoPtSum[0] = getattr(tree, '%sNeutralIsoPtSum' % lep)
            neutralIsoPtSumB.Fill()
            puCorrPtSum[0] = getattr(tree, '%sPuCorrPtSum' % lep)
            puCorrPtSumB.Fill()
            decayModeFindingOldDMs[0] = getattr(tree, '%sDecayModeFindingNewDMs' % lep)
            decayModeFindingOldDMsB.Fill()
            byIsolationMVA3newDMwoLTraw[0] = getattr(tree, '%sByIsolationMVA3newDMwoLTraw' % lep)
            byIsolationMVA3newDMwoLTrawB.Fill()
            byIsolationMVA3newDMwLTraw[0] = getattr(tree, '%sByIsolationMVA3newDMwLTraw' % lep)
            byIsolationMVA3newDMwLTrawB.Fill()
            byIsolationMVA3oldDMwoLTraw[0] = getattr(tree, '%sByIsolationMVA3oldDMwoLTraw' % lep)
            byIsolationMVA3oldDMwoLTrawB.Fill()
            byIsolationMVA3oldDMwLTraw[0] = getattr(tree, '%sByIsolationMVA3oldDMwLTraw' % lep)
            byIsolationMVA3oldDMwLTrawB.Fill()


    tree.Write('', ROOT.TObject.kOverwrite)


def addBranchesGen( dir_, sample, channel ) :
    treeFile = ROOT.TFile('%s/SYNCFILE_SYSYGluGluToHToTauTau_M-160_%s_spring15.root' % (dir_, channel), 'update')
    d1 = treeFile.Get( '%s' % channel )	
    tree = d1.Get( 'Ntuple' )
    
    # Common variables in all channels
    # Jets
    jpt_1 = array('f', [ 0 ] )
    jpt_1B = tree.Branch('jpt_1', jpt_1, 'jpt_1/F')
    jeta_1 = array('f', [ 0 ] )
    jeta_1B = tree.Branch('jeta_1', jeta_1, 'jeta_1/F')
    jphi_1 = array('f', [ 0 ] )
    jphi_1B = tree.Branch('jphi_1', jphi_1, 'jphi_1/F')
    jpt_2 = array('f', [ 0 ] )
    jpt_2B = tree.Branch('jpt_2', jpt_2, 'jpt_2/F')
    jeta_2 = array('f', [ 0 ] )
    jeta_2B = tree.Branch('jeta_2', jeta_2, 'jeta_2/F')
    jphi_2 = array('f', [ 0 ] )
    jphi_2B = tree.Branch('jphi_2', jphi_2, 'jphi_2/F')

    # Other vars
    extramuon_veto = array('i', [ 0 ] )
    extramuon_vetoB = tree.Branch('extramuon_veto', extramuon_veto, 'extramuon_veto/I')
    extraelec_veto = array('i', [ 0 ] )
    extraelec_vetoB = tree.Branch('extraelec_veto', extraelec_veto, 'extraelec_veto/I')
    m_vis = array('f', [ 0 ] )
    m_visB = tree.Branch('m_vis', m_vis, 'm_vis/F')
    met = array('f', [ 0 ] )
    metB = tree.Branch('met', met, 'met/F')
    metphi = array('f', [ 0 ] )
    metphiB = tree.Branch('metphi', metphi, 'metphi/F')
    weight = array('f', [ 0 ] )
    weightB = tree.Branch('weight', weight, 'weight/F')
    nbtag = array('i', [ 0 ] )
    nbtagB = tree.Branch('nbtag', nbtag, 'nbtag/I')
    njetspt20 = array('i', [ 0 ] )
    njetspt20B = tree.Branch('njetspt20', njetspt20, 'njetspt20/I')

    if channel == 'em' :
        iso_1 = array('f', [ 0 ] )
        iso_1B = tree.Branch('iso_1', iso_1, 'iso_1/F')
        iso_2 = array('f', [ 0 ] )
        iso_2B = tree.Branch('iso_2', iso_2, 'iso_2/F')

    treeFile.cd( '%s' % channel )

    # evt tracker [leg1iso,leg1pt,leg2iso,leg2pt,evtID,index]
    prevEvt = [999, 0, 999, 0, 0, 0]
    #for i in range( tree.GetEntries() ):
    for i in range( 1 ):
        tree.GetEntry( i )
        # Select 'best' Z candidates
        evtID = getattr( tree, 'evt' )
        if channel == 'em' :
            leg1Iso = getattr(tree, 'eRelPFIsoDB' )
            leg1Pt = getattr(tree, 'ePt' )
            leg2Iso = getattr(tree, 'mRelPFIsoDBDefault' )
            leg2Pt = getattr(tree, 'mPt' )
        if channel == 'tt' :
            leg1Iso = getattr(tree, 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits' )
            leg1Pt = getattr(tree, 't1Pt' )
            leg2Iso = getattr(tree, 't2ByCombinedIsolationDeltaBetaCorrRaw3Hits' )
            leg2Pt = getattr(tree, 't2Pt' )

        currentEvt = [ leg1Iso, leg1Pt, leg2Iso, leg2Pt, evtID, i ]

        # Fill once we've run through all versions of a single event
        #if currentEvt[4] != prevEvt[4] and i < 100 :
        if i < 100 :
            print "made it to fill, index %i" % i
            tree.GetEntry( prevEvt[ 5 ] )
            jpt_1[0] = getattr(tree, 'jet1Pt')
            jpt_1B.Fill()
            jphi_1[0] = getattr(tree, 'jet1Phi')
            jphi_1B.Fill()
            jeta_1[0] = getattr(tree, 'jet2Eta')
            jeta_1B.Fill()
            jpt_2[0] = getattr(tree, 'jet2Pt')
            jpt_2B.Fill()
            jphi_2[0] = getattr(tree, 'jet2Phi')
            jphi_2B.Fill()
            jeta_2[0] = getattr(tree, 'jet2Eta')
            jeta_2B.Fill()
            extramuon_veto[0] = int( getattr(tree, 'muVetoZTT10') )
            extramuon_vetoB.Fill()
            extraelec_veto[0] = int( getattr(tree, 'eVetoZTT10') )
            extraelec_vetoB.Fill()
            m_vis[0] = getattr(tree, 'Mass')
            m_visB.Fill()
            met[0] = getattr(tree, 'pfMetEt')
            metB.Fill()
            metphi[0] = getattr(tree, 'pfMetPhi')
            metphiB.Fill()
            weight[0] = getattr(tree, 'GenWeight')
            weightB.Fill()
            nbtag[0] = int( getattr(tree, 'bjetCISVVeto20Loose') )
            nbtagB.Fill()
            njetspt20[0] = int( getattr(tree, 'jetVeto20') )
            njetspt20B.Fill()
        
            if channel == 'em' :
                iso_1[0] = getattr(tree, 'eRelPFIsoDB')
                iso_1B.Fill()
                iso_2[0] = getattr(tree, 'mRelPFIsoDBDefault')
                iso_2B.Fill()

        elif currentEvt[ 0 ] < prevEvt[ 0 ] : prevEvt = currentEvt
        elif currentEvt[ 1 ] > prevEvt[ 1 ] : prevEvt = currentEvt
        elif currentEvt[ 2 ] < prevEvt[ 2 ] : prevEvt = currentEvt
        elif currentEvt[ 3 ] > prevEvt[ 3 ] : prevEvt = currentEvt

        #currentEvt = [ leg1Iso, leg1Pt, leg2Iso, leg2Pt, i ]
    tree.Write('', ROOT.TObject.kOverwrite)


chan = 'em'
if chan == 'em': zProd = ['e', 'm']
if chan == 'tt': zProd = ['t1', 't2']
makeNewTree( 'tuples', 'Sync_HtoTT', chan )
addBranchesGen( 'tuples', 'Sync_HtoTT', chan )
#addBranches( 'tuples', 'Sync_HtoTT', chan, zProd[0] )
#addBranches( 'tuples', 'Sync_HtoTT', chan, zProd[1] )
