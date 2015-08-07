
############################################################################
#   Rename my branches for the HTT 2015 Sync                               #
############################################################################

import ROOT
from array import array

def makeNewTree( dir_, sample, channel ) :
    ifile = ROOT.TFile('%s.root' % sample, 'r')
    d1 = ifile.Get( channel )
    inTree = d1.Get( 'Ntuple' )
    
    ofile = ROOT.TFile('%s/SYNCFILE_SYSYGluGluToHToTauTau_M-160_%s_spring15.root' % (dir_, channel), 'RECREATE')
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
    treeFile = ROOT.TFile('%s/SYNCFILE_SYSYGluGluToHToTauTau_M-160_%s_spring15.root' % (dir_, channel), 'update')
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
        d0 = array('f', [ 0 ] )
        d0B = tree.Branch('d0%s' % legMap[ lep ], d0, 'd0/F')
    
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
    for i in range( tree.GetEntries() ):
        tree.GetEntry( i )
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

    tree.Write('', ROOT.TObject.kOverwrite)


chan = 'em'
if chan == 'em': zProd = ['e', 'm']
if chan == 'tt': zProd = ['t1', 't2']
makeNewTree( 'tuples', 'Sync_HtoTT', chan )
addBranchesGen( 'tuples', 'Sync_HtoTT', chan )
addBranches( 'tuples', 'Sync_HtoTT', chan, zProd[0] )
addBranches( 'tuples', 'Sync_HtoTT', chan, zProd[1] )
