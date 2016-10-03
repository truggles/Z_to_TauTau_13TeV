

# Calculate Fake Factors based on this work:
# https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauJet2TauFakes
# We start with applying QCD factors to each leg and sum for total



import ROOT
from util.fakeFactorQCD import fakeFactors
import os
from array import array



def fillFakeFactorValues( analysis, mid2, sample, channel ) :

    # Create Fake Factor object for retrieving
    # FF values for data events
    cmssw_base = os.getenv('CMSSW_BASE')
    ffQCD = fakeFactors()
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.getInclusive(), 'Inc' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.get0Jet(), '0Jet' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.get1Jet(), '1Jet' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.get1JetLow(), '1JetLow' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.get1JetMed(), '1JetMed' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.get1JetHigh(), '1JetHigh' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.get2Jet(), '2Jet' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.getVBF(), 'VBF' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.getBTagged(), 'BTagged' )


    del ffQCD


def fillFakeFactorValuesPerCat( analysis, mid2, sample, channel, ffCat, append ) :
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
        updateTree.Branch('FFWeightQCD'+append, FFWeightQCD, 'FFWeightQCD/F')]
    FFWeightQCD_StatUP = array('f', [ 0 ] )
    branchMap['FFWeightQCD_StatUP'] = [FFWeightQCD_StatUP,
        updateTree.Branch('FFWeightQCD'+append+'_StatUP', FFWeightQCD_StatUP, 'FFWeightQCD_StatUP/F')]
    FFWeightQCD_StatDOWN = array('f', [ 0 ] )
    branchMap['FFWeightQCD_StatDOWN'] = [FFWeightQCD_StatDOWN,
        updateTree.Branch('FFWeightQCD'+append+'_StatDOWN', FFWeightQCD_StatDOWN, 'FFWeightQCD_StatDOWN/F')]
    FFWeightQCD_SystUP = array('f', [ 0 ] )
    branchMap['FFWeightQCD_SystUP'] = [FFWeightQCD_SystUP,
        updateTree.Branch('FFWeightQCD'+append+'_SystUP', FFWeightQCD_SystUP, 'FFWeightQCD_SystUP/F')]
    FFWeightQCD_SystDOWN = array('f', [ 0 ] )
    branchMap['FFWeightQCD_SystDOWN'] = [FFWeightQCD_SystDOWN,
        updateTree.Branch('FFWeightQCD'+append+'_SystDOWN', FFWeightQCD_SystDOWN, 'FFWeightQCD_SystDOWN/F')]


    for row in updateTree :


        # Reset all values to 0.
        for key, val in branchMap.iteritems() :
            val[0][0] = 0.


        muon_iso = 0.0
        # First leg FR
        if row.byVTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5 and row.byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5 :
            pt = getattr(row, 'pt_1')
            decayMode = getattr(row, 'decayMode_1')
            nJets = getattr(row, 'jetVeto30')
            mVis = getattr(row, 'm_vis')
            transMass = getattr(row, 'mt_2')
        # Second leg FR
        elif row.byVTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 and row.byVTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5 :
            pt = getattr(row, 'pt_2')
            decayMode = getattr(row, 'decayMode_2')
            nJets = getattr(row, 'jetVeto30')
            mVis = getattr(row, 'm_vis')
            transMass = getattr(row, 'mt_1')
        else : continue

        inputsqcd = [pt, decayMode, nJets, mVis, transMass, muon_iso]

        # The following notation is grabbing the first item in the value pair
        # (an array) of a map, then setting that single first value in 
        # the array to our FF value
        branchMap['FFWeightQCD'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd) )
        branchMap['FFWeightQCD_StatUP'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_stat_up" )
        branchMap['FFWeightQCD_StatDOWN'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_stat_down" )
        branchMap['FFWeightQCD_SystUP'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_syst_up" )
        branchMap['FFWeightQCD_SystDOWN'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_syst_down" )


        # Fill all new values
        for key, val in branchMap.iteritems() :
            val[1].Fill()


    f.cd()
    updateTree.Write('', ROOT.TObject.kOverwrite)
    f.Close()




