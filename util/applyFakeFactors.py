

# Calculate Fake Factors based on this work:
# https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauJet2TauFakes
# We start with applying QCD factors to each leg and sum for total



import ROOT
from util.fakeFactorQCD import fakeFactors
import random
import os
from array import array



def fillFakeFactorValues( analysis, mid2, sample, channel ) :
    fileName = '%s%s/%s.root' % (analysis, mid2, sample)
    f = ROOT.TFile(fileName, 'UPDATE' )
    updateTree = f.Get('Ntuple')


    # Create Fake Factor object for retrieving
    # FF values for data events
    cmssw_base = os.getenv('CMSSW_BASE')
    ffQCD = fakeFactors()


    branchMap = {}
    FFWeightQCD = array('f', [ 0 ] )
    branchMap['FFWeightQCD'] = [FFWeightQCD, 
        updateTree.Branch('FFWeightQCD', FFWeightQCD, 'FFWeightQCD/F')]
    FFWeightQCD_StatUP = array('f', [ 0 ] )
    branchMap['FFWeightQCD_StatUP'] = [FFWeightQCD_StatUP,
        updateTree.Branch('FFWeightQCD_StatUP', FFWeightQCD_StatUP, 'FFWeightQCD_StatUP/F')]
    FFWeightQCD_StatDOWN = array('f', [ 0 ] )
    branchMap['FFWeightQCD_StatDOWN'] = [FFWeightQCD_StatDOWN,
        updateTree.Branch('FFWeightQCD_StatDOWN', FFWeightQCD_StatDOWN, 'FFWeightQCD_StatDOWN/F')]
    FFWeightQCD_SystUP = array('f', [ 0 ] )
    branchMap['FFWeightQCD_SystUP'] = [FFWeightQCD_SystUP,
        updateTree.Branch('FFWeightQCD_SystUP', FFWeightQCD_SystUP, 'FFWeightQCD_SystUP/F')]
    FFWeightQCD_SystDOWN = array('f', [ 0 ] )
    branchMap['FFWeightQCD_SystDOWN'] = [FFWeightQCD_SystDOWN,
        updateTree.Branch('FFWeightQCD_SystDOWN', FFWeightQCD_SystDOWN, 'FFWeightQCD_SystDOWN/F')]


    for row in updateTree :


        # Reset all values to 0.
        for key, val in branchMap.iteritems() :
            val[0][0] = 0.


        # First leg FR
        if row.byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5 and row.byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5 :
            pt = getattr(row, 'pt_1')
            decayMode = getattr(row, 'decayMode_1')
            nJets = getattr(row, 'jetVeto30')
            mVis = getattr(row, 'm_vis')
            print "mvis",mVis
            transMass = getattr(row, 'mt_1')
            print transMass
            muon_iso = 0.0
            inputsqcd = [pt, decayMode, nJets, mVis, transMass, muon_iso]

            # The following notation is grabbing the first item in the value pair
            # (an array) of a map, then setting that single first value in 
            # the array to our FF value
            branchMap['FFWeightQCD'][0][0] = ffQCD.getInclusive().value( len(inputsqcd),array('d',inputsqcd) )
            branchMap['FFWeightQCD_StatUP'][0][0] = ffQCD.getInclusive().value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_stat_up" )
            branchMap['FFWeightQCD_StatDOWN'][0][0] = ffQCD.getInclusive().value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_stat_down" )
            branchMap['FFWeightQCD_SystUP'][0][0] = ffQCD.getInclusive().value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_syst_up" )
            branchMap['FFWeightQCD_SystDOWN'][0][0] = ffQCD.getInclusive().value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_syst_down" )


        # Fill all new values
        for key, val in branchMap.iteritems() :
            val[1].Fill()

    del ffQCD

    f.cd()
    updateTree.Write('', ROOT.TObject.kOverwrite)
    f.Close()





