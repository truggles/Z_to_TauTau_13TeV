
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

    #dzCutTight = array('i', [ 0 ] )
    #dzCutB = tree.Branch('dzCutTight', dzCutTight, 'dzCutTight/I')
    pt = array('f', [ 0 ] )
    ptB = tree.Branch('pt%s' % legMap[ lep ], pt, 'pt/F')
    eta = array('f', [ 0 ] )
    etaB = tree.Branch('eta%s' % legMap[ lep ], eta, 'eta/F')
    phi = array('f', [ 0 ] )
    phiB = tree.Branch('phi%s' % legMap[ lep ], phi, 'phi/F')
    mass = array('f', [ 0 ] )
    massB = tree.Branch('mass%s' % legMap[ lep ], mass, 'mass/F')
    q = array('f', [ 0 ] )
    qB = tree.Branch('q%s' % legMap[ lep ], q, 'q/F')
    #d0 = array('f', [ 0 ] )
    #d0B = tree.Branch('d0%s' % legMap[ lep ], d0, 'd0/F')
    #dZ = array('f', [ 0 ] )
    #dZB = tree.Branch('dZ%s' % legMap[ lep ], dZ, 'dZ/F')
    mt = array('f', [ 0 ] )
    mtB = tree.Branch('mt%s' % legMap[ lep ], mt, 'mt/F')
    
    treeFile.cd( '%s' % channel )
    for i in range( tree.GetEntries() ):
        tree.GetEntry( i )
        pt[0] = getattr(tree, '%sPt' % lep)
        ptB.Fill()
        eta[0] = getattr(tree, '%sEta' % lep)
        etaB.Fill()
        phi[0] = getattr(tree, '%sPhi' % lep)
        phiB.Fill()
        mass[0] = getattr(tree, '%sMass' % lep)
        massB.Fill()
        q[0] = getattr(tree, '%sCharge' % lep)
        qB.Fill()
        #d0[0] = getattr(tree, '%sPVDXY' % lep)
        #d0B.Fill()
        #dZ[0] = getattr(tree, '%sPVDZ' % lep)
        #dZB.Fill()
        mt[0] = getattr(tree, '%sMtToMET' % lep)
        mtB.Fill()
    














    tree.Write('', ROOT.TObject.kOverwrite)

makeNewTree( 'tuples', 'Sync_HtoTT', 'tt' )
addBranches( 'tuples', 'Sync_HtoTT', 'tt', 't2' )
addBranches( 'tuples', 'Sync_HtoTT', 'tt', 't1' )
