

# Calculate Fake Factors based on this work:
# https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauJet2TauFakes
# We start with applying QCD factors to each leg and sum for total



import ROOT
from util.fakeFactorQCD import fakeFactors
import os
from array import array
import math



def fillFakeFactorValues( analysis, mid2, sample, channel ) :

    # Create Fake Factor object for retrieving
    # FF values for data events
    cmssw_base = os.getenv('CMSSW_BASE')
    ffQCD = fakeFactors()
    #fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
    #    ffQCD.getInclusive(), 'Inc' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.get0Jet(), '0Jet' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.getBoosted(), 'Boosted' )
    fillFakeFactorValuesPerCat( analysis, mid2, sample, channel,
        ffQCD.getVBF(), 'VBF' )


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
    # Nominal
    FFWeight = array('f', [ 0 ] )
    branchMap['FFWeight'] = [FFWeight, 
        updateTree.Branch('FFWeight'+append, FFWeight, 'FFWeight/F')]
    # Statistical Shape Uncert
    FFWeight_0jet1prongStatUP = array('f', [ 0 ] )
    branchMap['FFWeight_0jet1prongStatUP'] = [FFWeight_0jet1prongStatUP,
        updateTree.Branch('FFWeight'+append+'_0jet1prongStatUP', FFWeight_0jet1prongStatUP, 'FFWeight_0jet1prongStatUP/F')]
    FFWeight_0jet1prongStatDOWN = array('f', [ 0 ] )
    branchMap['FFWeight_0jet1prongStatDOWN'] = [FFWeight_0jet1prongStatDOWN,
        updateTree.Branch('FFWeight'+append+'_0jet1prongStatDOWN', FFWeight_0jet1prongStatDOWN, 'FFWeight_0jet1prongStatDOWN/F')]

    FFWeight_0jet3prongStatUP = array('f', [ 0 ] )
    branchMap['FFWeight_0jet3prongStatUP'] = [FFWeight_0jet3prongStatUP,
        updateTree.Branch('FFWeight'+append+'_0jet3prongStatUP', FFWeight_0jet3prongStatUP, 'FFWeight_0jet3prongStatUP/F')]
    FFWeight_0jet3prongStatDOWN = array('f', [ 0 ] )
    branchMap['FFWeight_0jet3prongStatDOWN'] = [FFWeight_0jet3prongStatDOWN,
        updateTree.Branch('FFWeight'+append+'_0jet3prongStatDOWN', FFWeight_0jet3prongStatDOWN, 'FFWeight_0jet3prongStatDOWN/F')]

    FFWeight_1jet1prongStatUP = array('f', [ 0 ] )
    branchMap['FFWeight_1jet1prongStatUP'] = [FFWeight_1jet1prongStatUP,
        updateTree.Branch('FFWeight'+append+'_1jet1prongStatUP', FFWeight_1jet1prongStatUP, 'FFWeight_1jet1prongStatUP/F')]
    FFWeight_1jet1prongStatDOWN = array('f', [ 0 ] )
    branchMap['FFWeight_1jet1prongStatDOWN'] = [FFWeight_1jet1prongStatDOWN,
        updateTree.Branch('FFWeight'+append+'_1jet1prongStatDOWN', FFWeight_1jet1prongStatDOWN, 'FFWeight_1jet1prongStatDOWN/F')]

    FFWeight_1jet3prongStatUP = array('f', [ 0 ] )
    branchMap['FFWeight_1jet3prongStatUP'] = [FFWeight_1jet3prongStatUP,
        updateTree.Branch('FFWeight'+append+'_1jet3prongStatUP', FFWeight_1jet3prongStatUP, 'FFWeight_1jet3prongStatUP/F')]
    FFWeight_1jet3prongStatDOWN = array('f', [ 0 ] )
    branchMap['FFWeight_1jet3prongStatDOWN'] = [FFWeight_1jet3prongStatDOWN,
        updateTree.Branch('FFWeight'+append+'_1jet3prongStatDOWN', FFWeight_1jet3prongStatDOWN, 'FFWeight_1jet3prongStatDOWN/F')]

    # Systematic Shape Uncerts
    FFWeight_qcdSystUP = array('f', [ 0 ] )
    branchMap['FFWeight_qcdSystUP'] = [FFWeight_qcdSystUP,
        updateTree.Branch('FFWeight'+append+'_qcdSystUP', FFWeight_qcdSystUP, 'FFWeight_qcdSystUP/F')]
    FFWeight_qcdSystDOWN = array('f', [ 0 ] )
    branchMap['FFWeight_qcdSystDOWN'] = [FFWeight_qcdSystDOWN,
        updateTree.Branch('FFWeight'+append+'_qcdSystDOWN', FFWeight_qcdSystDOWN, 'FFWeight_qcdSystDOWN/F')]

    FFWeight_ttbarSystUP = array('f', [ 0 ] )
    branchMap['FFWeight_ttbarSystUP'] = [FFWeight_ttbarSystUP,
        updateTree.Branch('FFWeight'+append+'_ttbarSystUP', FFWeight_ttbarSystUP, 'FFWeight_ttbarSystUP/F')]
    FFWeight_ttbarSystDOWN = array('f', [ 0 ] )
    branchMap['FFWeight_ttbarSystDOWN'] = [FFWeight_ttbarSystDOWN,
        updateTree.Branch('FFWeight'+append+'_ttbarSystDOWN', FFWeight_ttbarSystDOWN, 'FFWeight_ttbarSystDOWN/F')]

    FFWeight_wjetsSystUP = array('f', [ 0 ] )
    branchMap['FFWeight_wjetsSystUP'] = [FFWeight_wjetsSystUP,
        updateTree.Branch('FFWeight'+append+'_wjetsSystUP', FFWeight_wjetsSystUP, 'FFWeight_wjetsSystUP/F')]
    FFWeight_wjetsSystDOWN = array('f', [ 0 ] )
    branchMap['FFWeight_wjetsSystDOWN'] = [FFWeight_wjetsSystDOWN,
        updateTree.Branch('FFWeight'+append+'_wjetsSystDOWN', FFWeight_wjetsSystDOWN, 'FFWeight_wjetsSystDOWN/F')]


    for row in updateTree :


        # Reset all values to 0.
        for key, val in branchMap.iteritems() :
            val[0][0] = 0.


        muon_iso = 0.0
        inputsqcd = []
        # First leg FR
        if row.byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5 and row.byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5 :
            pt = getattr(row, 'pt_1')
            pt2 = getattr(row, 'pt_2')
            decayMode = getattr(row, 'decayMode_1')
            nJets = getattr(row, 'jetVeto30')
            mVis = getattr(row, 'm_vis')
            inputsqcd = [pt, pt2, decayMode, nJets, mVis]
        # Second leg FR
        elif row.byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 and row.byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5 :
            pt = getattr(row, 'pt_2')
            pt2 = getattr(row, 'pt_1')
            decayMode = getattr(row, 'decayMode_2')
            nJets = getattr(row, 'jetVeto30')
            mVis = getattr(row, 'm_vis')
            inputsqcd = [pt, pt2, decayMode, nJets, mVis]

        if inputsqcd != [] :
            # The following notation is grabbing the first item in the value pair
            # (an array) of a map, then setting that single first value in 
            # the array to our FF value

            # Nominal
            branchMap['FFWeight'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd) )
            # Stat
            branchMap['FFWeight_0jet1prongStatUP'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd),   "ff_qcd_dm0_njet0_stat_up" )
            branchMap['FFWeight_0jet1prongStatDOWN'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_dm0_njet0_stat_down" )
            branchMap['FFWeight_0jet3prongStatUP'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd),   "ff_qcd_dm1_njet0_stat_up" )
            branchMap['FFWeight_0jet3prongStatDOWN'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_dm1_njet0_stat_down" )
            branchMap['FFWeight_1jet1prongStatUP'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd),   "ff_qcd_dm0_njet1_stat_up" )
            branchMap['FFWeight_1jet1prongStatDOWN'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_dm0_njet1_stat_down" )
            branchMap['FFWeight_1jet3prongStatUP'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd),   "ff_qcd_dm1_njet1_stat_up" )
            branchMap['FFWeight_1jet3prongStatDOWN'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_qcd_dm1_njet1_stat_down" )
            # Syst
            branchMap['FFWeight_qcdSystUP'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd),     "ff_qcd_syst_up" )
            branchMap['FFWeight_qcdSystDOWN'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd),   "ff_qcd_syst_down" )
            branchMap['FFWeight_ttbarSystUP'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd),   "ff_tt_syst_up" )
            branchMap['FFWeight_ttbarSystDOWN'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_tt_syst_down" )
            branchMap['FFWeight_wjetsSystUP'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd),   "ff_w_syst_up" )
            branchMap['FFWeight_wjetsSystDOWN'][0][0] = ffCat.value( len(inputsqcd),array('d',inputsqcd), "ff_w_syst_down" )



        # Fill all new values
        for key, val in branchMap.iteritems() :
            if math.isnan( val[0][0] ) :
                val[0][0] = branchMap['FFWeight'][0][0]
            val[1].Fill()


    f.cd()
    updateTree.Write('', ROOT.TObject.kOverwrite)
    f.Close()





