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

def renameBranches( sample, channel ) :
    branchMappingEM = {
        'ePt' : 'pt_1', # rename ePt to pt_1
        'eEta' : 'eta_1',
        'ePhi' : 'phi_1',
        'eMass' : 'm_1',
        'eCharge' : 'q_1',
        'ePVDXY' : 'd0_1',
        'ePVDZ' : 'dZ_1',
        'eMtToMET' : 'mt_1',
        'eRelPFIsoDB' : 'iso_1',
        'mPt' : 'pt_2',
        'mEta' : 'eta_2',
        'mPhi' : 'phi_2',
        'mMass' : 'm_2',
        'mCharge' : 'q_2',
        'mPVDXY' : 'd0_2',
        'mPVDZ' : 'dZ_2',
        'mMtToMET' : 'mt_2',
        'mRelPFIsoDBDefault' : 'iso_2',
        'jet1Pt' : 'jpt_1',
        'jet1Phi' : 'jphi_1',
        'jet1Eta' : 'jeta_1',
        'jet2Pt' : 'jpt_2',
        'jet2Phi' : 'jphi_2',
        'jet2Eta' : 'jeta_2',
        'muVetoZTT10' : 'extramuon_veto',
        'eVetoZTT10' : 'extraelec_veto',
        'e_m_Mass' : 'm_vis',
        'pfMetEt' : 'met',
        'pfMetPhi' : 'metphi',
        'GenWeight' : 'weight',
        'bjetCISVVeto20Loose' : 'nbtag',
        'jetVeto20' : 'njetspt20',
        }
    
    branchMappingTT = {
        'jet1Pt' : 'jpt_1',
        'jet1Phi' : 'jphi_1',
        'jet1Eta' : 'jeta_1',
        'jet2Pt' : 'jpt_2',
        'jet2Phi' : 'jphi_2',
        'jet2Eta' : 'jeta_2',
        'muVetoZTT10' : 'extramuon_veto',
        'eVetoZTT10' : 'extraelec_veto',
        't1_t2_Mass' : 'm_vis',
        'pfMetEt' : 'met',
        'pfMetPhi' : 'metphi',
        'GenWeight' : 'weight',
        'bjetCISVVeto20Loose' : 'nbtag',
        'jetVeto20' : 'njetspt20',
        }
    if channel == 'em' : branchMapping = branchMappingEM

    oldFileName = '%s.root' % sample
    if sample == 'Sync_HtoTT' :
        newFileName = 'tuples/SYNCFILE_SUSYGluGluToHToTauTau_M-160_%s_spring15.root' % channel
    else : newFileName = 'tuples/%s_%s.root' % (sample, channel)
    dirName = channel
    treeName = 'Ntuple'
    
    # A few branches are ints instead of floats and must be treated specially
    # I think these are all the ones in FSA ntuples, but add more if you find them
    intBranches = set(['run', 'evt', 'lumi', 'isdata', 'pvIsValid', 'pvIsFake', 'muVetoZTT10',
        'eVetoZTT10', 'GenWeight', 'bjetCISVVeto20Loose', 'jetVeto20'])
    
    
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
    
    # fill new tree
    # evt tracker [leg1iso,leg1pt,leg2iso,leg2pt,evtID,index]
    prevEvt = [999, 0, 999, 0, 0, 0]
    prevRow = 0
    count = 0
    for row in told:
        evtID = row.evt
        print "EvtID: %i" % evtID
        if channel == 'em' :
            leg1Iso = row.eRelPFIsoDB
            leg1Pt = row.ePt
            leg2Iso = row.mRelPFIsoDBDefault
            leg2Pt = row.mPt
        if channel == 'tt' :
            leg1Iso = row.t1ByCombinedIsolationDeltaBetaCorrRaw3Hits
            leg1Pt = row.t1Pt
            leg2Iso = row.t2ByCombinedIsolationDeltaBetaCorrRaw3Hits
            leg2Pt = row.t2Pt

        currentEvt = [ leg1Iso, leg1Pt, leg2Iso, leg2Pt, evtID, count ]
        print "Current: "
        print currentEvt
        print "Previous: "
        print prevEvt

        if currentEvt[4] != prevEvt[4] and count != 0 :
            row = prevRow
            tnew.Fill()
            prevEvt = currentEvt

        elif currentEvt[ 0 ] < prevEvt[ 0 ] :
            prevEvt = currentEvt
            prevRow = row
        elif currentEvt[ 1 ] > prevEvt[ 1 ] :
            prevEvt = currentEvt
            prevRow = row
        elif currentEvt[ 2 ] < prevEvt[ 2 ] :
            prevEvt = currentEvt
            prevRow = row
        elif currentEvt[ 3 ] > prevEvt[ 3 ] :
            prevEvt = currentEvt
            prevRow = row
        count += 1
        # Make sure we get the last event!
        if count == told.GetEntries() :
            tnew.Fill()
            print row
    
    # write to disk
    tnew.write()
    fnew.close()

WW = 'WW'
Sync = 'Sync_HtoTT'
renameBranches( Sync, 'tt' )
