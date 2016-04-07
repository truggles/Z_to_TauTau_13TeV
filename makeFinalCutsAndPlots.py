'''#################################################################
##     Based on 'run.py' file for Z or Higgs -> TauTau            ##
##     Tyler Ruggles                                              ##
##     Oct 11, 2015                                               ##
#################################################################'''


import os
from time import gmtime, strftime
import ROOT
from ROOT import gPad, gROOT
import analysis1BaselineCuts
from util.helpers import checkBkgs 
import argparse
import subprocess

p = argparse.ArgumentParser(description="A script to apply additional cuts and plot.")
p.add_argument('--folder', action='store', default='xxx', dest='folder', help="What is the full folder name for extracting root files?")
options = p.parse_args()
folder = options.folder


def testQCDCuts( folder, isoL, isoT, sign ) :
    if folder == 'xxx' :
        print "ERROR: Folder was not choosen"
        return
    
    ''' Set grouping (25ns or Sync) '''
    grouping = 'dataCards'
    zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
    print "zHome: ",zHome
    os.environ['_GROUPING_'] = grouping
    os.environ['_ZHOME_'] = zHome
    
    
    
    ''' Preset samples '''
    SamplesDataCards = ['DYJets', 'DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJetsHigh', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'data_em', 'data_tt', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # As of April03
    
    masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
    for mass in masses :
           SamplesDataCards.append( 'ggH%i' % mass )
           SamplesDataCards.append( 'bbH%i' % mass )
    #SamplesDataCards = ['DYJets', 'DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow',] # As of April03
    #SamplesDataCards = ['DYJets4',] # As of April03
    #SamplesDataCards = ['WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4'] # As of April03
    samples = SamplesDataCards
    params = {
        'bkgs' : 'None',
        'numCores' : 20,
        'numFilesPerCycle' : 1,
        'channels' : ['tt',],
        'mid1' : '1Feb24a',
        'mid2' : folder,
        'additionalCut' : '',
        'svFitPost' : 'true'
    }

    isoL2loose = '(t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)
    isoL1TL2loose = '(t1ByTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)
    isoL1ML2loose = '(t1ByMediumIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)
    isoL1LL2loose = '(t1ByLooseIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)
    isoL1VTL2loose = '(t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)
    isoPt1GtrL1TL2loose = '(pt_1 > pt_2)*(t1ByTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)
    isoPt2GtrL1TL2loose = '(pt_1 < pt_2)*(t1ByTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)
    isoPt1GtrL1ML2loose = '(pt_1 > pt_2)*(t1ByMediumIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)
    isoPt2GtrL1ML2loose = '(pt_1 < pt_2)*(t1ByMediumIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)

    if isoL == '' :
        isoL2loose = '(t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5)'
        isoL1TL2loose = isoL2loose
        isoL1ML2loose = isoL2loose
        isoL1LL2loose = isoL2loose
        isoL1VTL2loose = isoL2loose
    if sign == 'OS' :
        Zsign = 0
    else : 
        Zsign = 1
        
    print "IsoL2Loose: %s" % isoL2loose

    """ HIG-15-007 ZTT """
    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_%sl1ml2_%s_%sZTT' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*%s' % (Zsign, isoL1ML2loose)
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    """
    Double Hardonic baseline with good QCD estimation
        Inclusive
    """
    ''' FINAL SELECTIONS MSSM '''
    params['channels'] = ['tt',]
    params['mid3'] = folder+'_%sl1ml2_%s_%sBTL' % (sign, isoT, isoL)
    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtagLoose>0)*(njets<=1)' % (Zsign, isoL1ML2loose)
    samples = checkBkgs( samples, params, grouping )
    analysis1BaselineCuts.drawHistos( grouping, samples, **params )

    params['channels'] = ['tt',]
    params['mid3'] = folder+'_%sl1ml2_%s_%sNoBTL' % (sign, isoT, isoL)
    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtagLoose==0)' % (Zsign, isoL1ML2loose)
    samples = checkBkgs( samples, params, grouping )
    analysis1BaselineCuts.drawHistos( grouping, samples, **params )

    ''' FINAL SELECTIONS ZTT '''
    params['channels'] = ['tt',]
    params['mid3'] = folder+'_%sl1ml2_%s_%sZTT' % (sign, isoT, isoL)
    params['additionalCut'] = '*(Z_SS==%i)*%s' % (Zsign, isoL1ML2loose)
    samples = checkBkgs( samples, params, grouping )
    analysis1BaselineCuts.drawHistos( grouping, samples, **params )

    """ BTAG VS NO BTAG TEST WITH IMPERIAL medium """
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1ml2_%s_%sBTMjl1' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtag!=0)*(njets<=1)' % (Zsign, isoL1ML2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1ml2_%s_%sBTLjl1' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtagLoose!=0)*(njets<=1)' % (Zsign, isoL1ML2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1ml2_%s_%sNoBTM' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtag==0)' % (Zsign, isoL1ML2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    
    
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1ml2_%s_%sBTLallJ' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtagLoose!=0)' % (Zsign, isoL1ML2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1ml2_%s_%sNoBTM' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtag==0)' % (Zsign, isoL1ML2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    
    """ END BTAG TEST WITH IMPERIAL """
    ''' end l1 medium '''
#    """ BTAG VS NO BTAG TEST WITH IMPERIAL Loose """
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1ll2_%s_%sBTM' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtag!=0)*(njets<=2)' % (Zsign, isoL1LL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1ll2_%s_%sBTL' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(bjetCISVVeto20Loose!=0)*(njets<=2)' % (Zsign, isoL1LL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1ll2_%s_%sNoBTM' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtag==0)' % (Zsign, isoL1LL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1ll2_%s_%sNoBTL' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(bjetCISVVeto20Loose==0)' % (Zsign, isoL1LL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    """ END BTAG TEST WITH IMPERIAL """
#    ''' end l1 loose '''
#    """ BTAG VS NO BTAG TEST WITH IMPERIAL tight """
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1tl2_%s_%sBTM' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtag!=0)*(njets<=2)' % (Zsign, isoL1TL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1tl2_%s_%sBTL' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(bjetCISVVeto20Loose!=0)*(njets<=2)' % (Zsign, isoL1TL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1tl2_%s_%sNoBTM' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtag==0)' % (Zsign, isoL1TL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1tl2_%s_%sNoBTL' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(bjetCISVVeto20Loose==0)' % (Zsign, isoL1TL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    """ END BTAG TEST WITH IMPERIAL """
#    ''' end l1 tight '''
#    """ BTAG VS NO BTAG TEST WITH IMPERIAL vtight """
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1vtl2_%s_%sBTM' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtag!=0)*(njets<=2)' % (Zsign, isoL1VTL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1vtl2_%s_%sBTL' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(bjetCISVVeto20Loose!=0)*(njets<=2)' % (Zsign, isoL1VTL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1vtl2_%s_%sNoBTM' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtag==0)' % (Zsign, isoL1VTL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    
#    params['channels'] = ['tt',]
#    params['mid3'] = folder+'_%sl1vtl2_%s_%sNoBTL' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*%s*(bjetCISVVeto20Loose==0)' % (Zsign, isoL1VTL2loose)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    """ END BTAG TEST WITH IMPERIAL """
#    ''' end l1 vtight '''
    return






def makeCuts( folder ) :
    if folder == 'xxx' :
        print "ERROR: Folder was not choosen"
        return
    
    ''' Set grouping (25ns or Sync) '''
    grouping = 'dataCards'
    zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
    print "zHome: ",zHome
    os.environ['_GROUPING_'] = grouping
    os.environ['_ZHOME_'] = zHome
    
    
    
    ''' Preset samples '''
    #SamplesDataCards = ['data_em', 'data_tt', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'DYJets', 'DYJetsLow', 'T-tW', 'T-tchan', 'TT', 'Tbar-tW', 'Tbar-tchan', 'WJets', 'WW1l1nu2q', 'WW2l2nu', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZ3l1nu', 'ZZ2l2nu', 'ZZ2l2q', 'ZZ4l']#, 'QCD15-20', 'QCD20-30', 'QCD30-80', 'QCD80-170', 'QCD170-250', 'QCD250-Inf'] # Set list for Data Card Sync (less DYJetsLow)
    #SamplesDataCards = ['data_em', 'data_tt', 'ggHtoTauTau125', 'ggHtoTauTau130', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'DYJets', 'DYJets100-200', 'DYJets200-400', 'DYJets400-600', 'DYJets600-Inf', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'WJets', 'WJets100-200', 'WJets200-400', 'WJets400-600', 'WJets600-Inf', 'WW1l1nu2q', 'WZ1l3nu', 'ZZ4l'] # As we wait for all samples 76x to come in, this is our complete list
    #SamplesDataCards = ['DYJets', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WW1l1nu2q', 'WZ1l3nu', 'WZ1l1nu2q', 'ZZ2l2q', 'ZZ4l', 'data_em', 'data_tt', ] # As of Feb11
    SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'data_em', 'data_tt', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau125', 'ggHtoTauTau130'] # As of Feb22 XXX DYJetsFXFX not included
    
#XXX    SamplesDataCards = []
#XXX    masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2600, 2900, 3200]
#XXX    for mass in masses :
#XXX           SamplesDataCards.append( 'ggH%i' % mass )
#XXX           SamplesDataCards.append( 'bbH%i' % mass )
    
    #SamplesDataCards = ['DYJets',]
    samples = SamplesDataCards
    
    ''' These parameters are fed into the 2 main function calls.
    They adjust the cuts you make, number of cores you run in
    multiprocessing, and the 'mid' params define the save location
    of your output files.  additionCut can be specified to further
    cut on any 'preselection' made in the initial stages '''
    params = {
        'bkgs' : 'None',
        'numCores' : 5,
        'numFilesPerCycle' : 1,
        #'channels' : ['em', 'tt'],
        #'channels' : ['em', 'tt', 'et', 'mt'],
        #'channels' : ['em',],
        'channels' : ['tt',],
        #'cutMapper' : 'signalCutsNoIsoNoSign', #!
        #'cutMapper' : 'signalCutsNoSign', #!
        #'cutMapper' : 'signalExtractionNoSign', #!
        #'cutName' : 'PostSync', #!
        #'cutMapper' : 'syncCutsDC',
        #'cutMapper' : 'syncCutsNtuple',
        #'cutName' : 'BaseLine',
        'mid1' : '1Feb24a',
        'mid2' : folder,
        'additionalCut' : '',
        'svFitPost' : 'true'
    }
    
    """
    The below cuts will be based on a previous cut files from 'mid2'
    """

    # Experimental DM based shapes
    #for i in [0,1,10]:
    #    params['mid3'] = folder+'_tt_SStau%i'% i
    #    params['channels'] = ['tt',]
    #    params['additionalCut'] = '*(Z_SS==1)*((t1DecayMode == %i) && (t2DecayMode != 5 && t2DecayMode != 6))'% i
    #    samples = checkBkgs( samples, params, grouping )
    #    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    #    
    #    params['mid3'] = folder+'_tt_OStau%i'% i
    #    params['channels'] = ['tt',]
    #    params['additionalCut'] = '*(Z_SS==0)*((t1DecayMode == %i) && (t2DecayMode != 5 && t2DecayMode != 6))' % i
    #    samples = checkBkgs( samples, params, grouping )
    #    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    
    
    #params['mid3'] = folder+'_SStest'
    #params['channels'] = ['tt',]
    #params['additionalCut'] = '*(Z_SS==1)*(iso_1 < 1 && iso_2 > 1 && iso_2 < 3)'
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    
    #isoL2loose = '(iso_1<1. && iso_2>1. && iso_2 <3)'
    isoL2loose = '(t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVTightIsolationMVArun2v1DBoldDMwLT < 0.5 && t2ByMediumIsolationMVArun2v1DBoldDMwLT > 0.5)'
    no2p = '((t1DecayMode != 5 && t1DecayMode != 6) && (t2DecayMode != 5 && t2DecayMode != 6))'
    #isoSig = '(iso_1<1. && iso_2<1.)'
    isoSig = '(t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5)'
    #isoSig = '(1)'

    """
    Double Hardonic baseline with good QCD estimation
        Inclusive
    """
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_SSl2loose'
#XXX    params['additionalCut'] = '*(Z_SS==1)*%s' % (isoL2loose)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_OSl2loose'
#XXX    params['additionalCut'] = '*(Z_SS==0)*%s' % (isoL2loose)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_SSIsoCut'
#XXX    params['additionalCut'] = '*(Z_SS==1)*%s' % (isoSig)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_OSIsoCut'
#XXX    params['additionalCut'] = '*(Z_SS==0)*%s' % (isoSig)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
   
    """ No B Tag """
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_SSl2looseNoBT'
#XXX    params['additionalCut'] = '*(Z_SS==1)*(nbtag==0)*%s' % (isoL2loose)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_OSl2looseNoBT'
#XXX    params['additionalCut'] = '*(Z_SS==0)*(nbtag==0)*%s' % (isoL2loose)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_SSsigNoBT'
#XXX    params['additionalCut'] = '*(Z_SS==1)*(nbtag==0)*%s' % (isoSig)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_OSsigNoBT'
#XXX    params['additionalCut'] = '*(Z_SS==0)*(nbtag==0)*%s' % (isoSig)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX
#XXX    """ B Tag """
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_SSl2looseBT'
#XXX    params['additionalCut'] = '*(Z_SS==1)*(nbtag!=0)*%s' % (isoL2loose)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['channels'] = ['tt',]
#XXX    params['mid3'] = folder+'_OSl2looseBT'
#XXX    params['additionalCut'] = '*(Z_SS==0)*(nbtag!=0)*%s' % (isoL2loose)
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
    params['channels'] = ['tt',]
    params['mid3'] = folder+'_SSsigBT'
    params['additionalCut'] = '*(Z_SS==1)*(nbtag!=0)*%s' % (isoSig)
    samples = checkBkgs( samples, params, grouping )
    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    
    params['channels'] = ['tt',]
    params['mid3'] = folder+'_OSsigBT'
    params['additionalCut'] = '*(Z_SS==0)*(nbtag!=0)*%s' % (isoSig)
    samples = checkBkgs( samples, params, grouping )
    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    """
    EMu 'final' selection atm
    """
#XXX    params['mid3'] = folder+'_em_SSpZetaCut'
#XXX    params['channels'] = ['em',]
#XXX    params['additionalCut'] = '*(Z_SS==1)*(pzetamiss > -20)'
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['mid3'] = folder+'_em_OSpZetaCut'
#XXX    params['channels'] = ['em',]
#XXX    params['additionalCut'] = '*(Z_SS==0)*(pzetamiss > -20)'
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX
#XXX    """ No B Tag """
#XXX    params['mid3'] = folder+'_em_SSpZetaCutNoBT'
#XXX    params['channels'] = ['em',]
#XXX    params['additionalCut'] = '*(Z_SS==1)*(pzetamiss > -20)*(nbtag==0)'
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['mid3'] = folder+'_em_OSpZetaCutNoBT'
#XXX    params['channels'] = ['em',]
#XXX    params['additionalCut'] = '*(Z_SS==0)*(pzetamiss > -20)*(nbtag==0)'
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX
#XXX    """ B Tag """
#XXX    params['mid3'] = folder+'_em_SSpZetaCutBT'
#XXX    params['channels'] = ['em',]
#XXX    params['additionalCut'] = '*(Z_SS==1)*(pzetamiss > -20)*(nbtag!=0)'
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#XXX    
#XXX    params['mid3'] = folder+'_em_OSpZetaCutBT'
#XXX    params['channels'] = ['em',]
#XXX    params['additionalCut'] = '*(Z_SS==0)*(pzetamiss > -20)*(nbtag!=0)'
#XXX    samples = checkBkgs( samples, params, grouping )
#XXX    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    #"""
    #Double Hardonic boosted Z/higgs
    #"""
    #zPt = '(Z_Pt>100)'
    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_SSl2looseZPt2'
    #params['additionalCut'] = '*(Z_SS==1)*%s*%s*%s' % (no2p, isoL2loose, zPt)
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    #
    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_OSl2looseZPt2'
    #params['additionalCut'] = '*(Z_SS==0)*%s*%s*%s' % (no2p, isoL2loose, zPt)
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    #
    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_SSsigZPt2'
    #params['additionalCut'] = '*(Z_SS==1)*%s*%s*%s' % (no2p, isoSig, zPt)
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    #
    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_OSsigZPt2'
    #params['additionalCut'] = '*(Z_SS==0)*%s*%s*%s' % (no2p, isoSig, zPt)
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    
    #params['mid3'] = folder+'_tt_SSno2p'
    #params['channels'] = ['tt',]
    #params['additionalCut'] = '*(Z_SS==1)*((t1DecayMode != 5 && t1DecayMode != 6) && (t2DecayMode != 5 && t2DecayMode != 6))'
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    #
    #params['mid3'] = folder+'_tt_OSno2p'
    #params['channels'] = ['tt',]
    #params['additionalCut'] = '*(Z_SS==0)*((t1DecayMode != 5 && t1DecayMode != 6) && (t2DecayMode != 5 && t2DecayMode != 6))'
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    #
    #params['mid3'] = folder+'_tt_SSn2pZpt60'
    #params['channels'] = ['tt',]
    #params['additionalCut'] = '*(Z_SS==1)*((t1DecayMode != 5 && t1DecayMode != 6) && (t2DecayMode != 5 && t2DecayMode != 6))*(Z_Pt>60)'
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    #
    #params['mid3'] = folder+'_tt_OSn2pZpt60'
    #params['channels'] = ['tt',]
    #params['additionalCut'] = '*(Z_SS==0)*((t1DecayMode != 5 && t1DecayMode != 6) && (t2DecayMode != 5 && t2DecayMode != 6))*(Z_Pt>60)'
    #samples = checkBkgs( samples, params, grouping )
    #analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    #

    """
    Standard DC Sync cuts
    """
    ttIso   = '(t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5)'
    # EMu
#    params['mid3'] = folder+'_em_SS'
#    params['channels'] = ['em',]
#    params['additionalCut'] = '*(Z_SS==1)'
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    
#    params['mid3'] = folder+'_em_OS'
#    params['channels'] = ['em',]
#    params['additionalCut'] = '*(Z_SS==0)'
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#
#    # TT
#    params['mid3'] = folder+'_tt_SS'
#    params['channels'] = ['tt',]
#    params['additionalCut'] = '*(Z_SS==1)*%s*%s' % (ttIso, no2p)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    
#    params['mid3'] = folder+'_tt_OS'
#    params['channels'] = ['tt',]
#    params['additionalCut'] = '*(Z_SS==0)*%s*%s' % (ttIso, no2p)
#    samples = checkBkgs( samples, params, grouping )
#    analysis1BaselineCuts.drawHistos( grouping, samples, **params )
    return




def setUpForCuts() :
    ''' Set grouping (25ns or Sync) '''
    grouping = 'dataCards'
    zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
    print "zHome: ",zHome
    os.environ['_GROUPING_'] = grouping
    os.environ['_ZHOME_'] = zHome
    
    
    
    ''' Preset samples '''
    SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'data_em', 'data_tt', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau125', 'ggHtoTauTau130'] # As of Feb22 XXX DYJetsFXFX not included
    
    #SamplesDataCards = []
    masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2600, 2900, 3200]
    for mass in masses :
           SamplesDataCards.append( 'ggH%i' % mass )
           SamplesDataCards.append( 'bbH%i' % mass )
    samples = SamplesDataCards
    params = {
        'bkgs' : 'None',
        'numCores' : 20,
        'numFilesPerCycle' : 1,
        'channels' : ['tt',],
        'mid1' : '1Feb24a',
        'mid2' : 'xxx',
        'additionalCut' : '',
        'svFitPost' : 'true'
    }
    return (grouping, params, samples)






def plotThem( folder, sufix1, sufix2, channel, single=False ) :
    if folder == 'xxx' :
        print "ERROR: Folder was not choosen"
        return

    if not os.path.exists( '/afs/cern.ch/user/t/truggles/www/%s' % (folder) ) :
        os.makedirs( '/afs/cern.ch/user/t/truggles/www/%s' % (folder) )
    if not os.path.exists( '/afs/cern.ch/user/t/truggles/www/%s/%s%s' % (folder[1:], channel, sufix1) ) :
        os.makedirs( '/afs/cern.ch/user/t/truggles/www/%s/%s%s' % (folder[1:], channel, sufix1) )

    #subprocess.call(["python", "analysis3Plots.py", "--folder=%s_%s_%s"%(folder,channel,sufix1), "--qcdMake=True", "--text=True", "--ratio=True", "--channels=%s"%channel, "--qcdMakeDM=%s"%sufix1])
    subprocess.call(["python", "analysis3Plots.py", "--folder=%s_%s_%s"%(folder,channel,sufix1), "--qcdMake=True", "--ratio=True", "--channels=%s"%channel, "--qcdMakeDM=%s"%sufix1]) # Normal one that works for non QCD study

    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/dataCardsPlots", "/afs/cern.ch/user/t/truggles/www/%s/%s%s" % (folder[1:], channel, sufix1)])
    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/dataCardsPlotsList", "/afs/cern.ch/user/t/truggles/www/%s/%s%s" % (folder[1:], channel, sufix1)])


    if not os.path.exists( '/afs/cern.ch/user/t/truggles/www/%s/%s%s' % (folder[1:], channel, sufix2) ) :
        os.makedirs( '/afs/cern.ch/user/t/truggles/www/%s/%s%s' % (folder[1:], channel, sufix2) )

    #subprocess.call(["python", "analysis3Plots.py", "--folder=%s_%s_%s"%(folder,channel,sufix2), "--useQCDMake=True", "--text=True", "--ratio=True", "--channels=%s"%channel, "--useQCDMakeName=%s"%sufix1])
    subprocess.call(["python", "analysis3Plots.py", "--folder=%s_%s_%s"%(folder,channel,sufix2), "--useQCDMake=True", "--ratio=True", "--channels=%s"%channel, "--useQCDMakeName=%s"%sufix1])

    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/dataCardsPlots", "/afs/cern.ch/user/t/truggles/www/%s/%s%s" % (folder[1:], channel, sufix2)])
    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/dataCardsPlotsList", "/afs/cern.ch/user/t/truggles/www/%s/%s%s" % (folder[1:], channel, sufix2)])


def plotSingle( folder, sufix1, channel, btag ) :
    if folder == 'xxx' :
        print "ERROR: Folder was not choosen"
        return
    print folder,sufix1,channel

    if not os.path.exists( '/afs/cern.ch/user/t/truggles/www/%s' % (folder) ) :
        os.makedirs( '/afs/cern.ch/user/t/truggles/www/%s' % (folder) )
    if not os.path.exists( '/afs/cern.ch/user/t/truggles/www/%s/%s%s%s' % (folder, channel, sufix1, btag) ) :
        os.makedirs( '/afs/cern.ch/user/t/truggles/www/%s/%s%s%s' % (folder, channel, sufix1, btag) )

    #subprocess.call(["python", "analysis3Plots.py", "--folder=%s_%s%s"%(folder,sufix1,btag), "--qcdMake=True", "--ratio=True", "--channels=%s"%channel, "--qcdMakeDM=%s"%sufix1]) # Works for QCD study plotting
    subprocess.call(["python", "analysis3Plots.py", "--folder=%s_%s%s"%(folder,sufix1,btag), "--qcdMake=True", "--ratio=True", "--channels=%s"%channel, "--qcdMakeDM=xxx"]) # Works for QCD study plotting

    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/dataCardsPlots", "/afs/cern.ch/user/t/truggles/www/%s/%s%s%s" % (folder, channel, sufix1, btag)])
    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/dataCardsPlotsList", "/afs/cern.ch/user/t/truggles/www/%s/%s%s%s" % (folder, channel, sufix1, btag)])


def plotSingle2( folder, folder2 ) :
    if folder == 'xxx' :
        print "ERROR: Folder was not choosen"
        return
    print folder,folder2

    if not os.path.exists( '/afs/cern.ch/user/t/truggles/www/%s' % (folder) ) :
        os.makedirs( '/afs/cern.ch/user/t/truggles/www/%s' % (folder) )
    if not os.path.exists( '/afs/cern.ch/user/t/truggles/www/%s/%s' % (folder, folder2) ) :
        os.makedirs( '/afs/cern.ch/user/t/truggles/www/%s/%s' % (folder, folder2) )

    #subprocess.call(["python", "analysis3Plots.py", "--folder=%s_%s%s"%(folder,sufix1,btag), "--qcdMake=True", "--ratio=True", "--channels=%s"%channel, "--qcdMakeDM=%s"%sufix1]) # Works for QCD study plotting
    subprocess.call(["python", "analysis3Plots.py", "--folder=%s"%(folder2), "--qcdMake=True", "--ratio=True", "--channels=tt", "--qcdMakeDM=%s" % folder2]) # Works for QCD study plotting

    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/dataCardsPlots", "/afs/cern.ch/user/t/truggles/www/%s/%s" % (folder, folder2)])
    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/dataCardsPlotsList", "/afs/cern.ch/user/t/truggles/www/%s/%s" % (folder, folder2)])



if __name__ == '__main__' :

    tups = [
        #('SS', 'OS', 'em,tt'),
#        ('SS', 'OS', 'em'),
#        ('SS', 'OS', 'tt'),
        #('tt_SSno2p', 'tt_OSno2p', 'tt'),
        #('tt_SSno2pZpt60', 'tt_OSno2pZpt60', 'tt'),
        ('SSpZetaCut', 'OSpZetaCut', 'em'),
        ('SSpZetaCutNoBT', 'OSpZetaCutNoBT', 'em'),
        ('SSpZetaCutBT', 'OSpZetaCutBT', 'em'),
        #('tt_SStau0', 'tt_OStau0', 'tt', '0'),
        #('tt_SStau1', 'tt_OStau1', 'tt', '1'),
        #('tt_SStau10', 'tt_OStau10', 'tt', '10'),
    ]

    #folder = "2Feb02sDC"
#    for tup in tups :
#        plotThem( folder, tup[0], tup[1], tup[2] )
    
    isoPairs = [
#        ('Loose','Medium'),
        #('Loose','Tight'),
        ('Loose','VTight'),
#        ('Medium','Tight'),
        #('Medium','VTight'),
#        ('Tight','VTight'),
        ('','VTight'),
    ]

    for pair in isoPairs :
        for sign in ['OS', 'SS']:
            testQCDCuts( folder, pair[0], pair[1], sign )

#XXX    testQCDCuts( folder, '', 'VTight', 'OS' )

    #makeCuts( folder )
    #for pair in isoPairs :
    #    for sign in ['SS', 'OS'] :
    #        for l2 in ['l2', 'l1tl2', 'l1ml2'] :
    #            for bt in ['', 'BT'] :
    #                folder = '2Mar15a_'+sign+l2
    #                plotSingle( folder, pair[1]+'_'+pair[0], 'tt', bt )
    
#    stuff = setUpForCuts()
#    grouping = stuff[0]
#    params  = stuff[1]
#    samples = stuff[2]
#
#    info = {
#    'LBTagOSSig' : ['2Mar17g_osSig', 'OS', 'VTight', 'VTight', 'bjetCISVVeto20Loose'],
#    'LBTagOSt1mt2l' : ['2Mar17h_QCD', 'OS', 'VTight','Loose', 'bjetCISVVeto20Loose'],
#    'LBTagSSSig' : ['2Mar17h_QCD', 'SS', 'VTight', 'VTight', 'bjetCISVVeto20Loose'],
#    'LBTagSSt1mt2l' : ['2Mar17h_QCD', 'SS', 'VTight', 'Loose', 'bjetCISVVeto20Loose'],
#    'MBTagOSSig' : ['2Mar17g_osSig', 'OS', 'VTight', 'VTight', 'nbtag'],
#    'MBTagOSt1mt2l' : ['2Mar17h_QCD', 'OS', 'VTight','Loose', 'nbtag'],
#    'MBTagSSSig' : ['2Mar17h_QCD', 'SS', 'VTight', 'VTight', 'nbtag'],
#    'MBTagSSt1mt2l' : ['2Mar17h_QCD', 'SS', 'VTight', 'Loose', 'nbtag'],
#    'LBTagOSt1tt2l' : ['2Mar17h_QCD', 'OS', 'VTight','Loose', 'bjetCISVVeto20Loose'],
#    'LBTagSSt1tt2l' : ['2Mar17h_QCD', 'SS', 'VTight', 'Loose', 'bjetCISVVeto20Loose'],
#    'MBTagOSt1tt2l' : ['2Mar17h_QCD', 'OS', 'VTight','Loose', 'nbtag'],
#    'MBTagSSt1tt2l' : ['2Mar17h_QCD', 'SS', 'VTight', 'Loose', 'nbtag'],
#    }
#
#    for key,tup in info.iteritems() :
#        print key, tup
#        #isoL2loose = '(t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (isoT, isoL)
#        isoL1ML2loose = '(t1ByMediumIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (tup[2], tup[3])
#        isoL1TL2loose = '(t1ByTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT < 0.5 && t2By%sIsolationMVArun2v1DBoldDMwLT > 0.5)' % (tup[2], tup[3])
#        isoSig = '(t1ByMediumIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5)'
#        if 'Sig' in key : iso = isoSig
#        if 't1t' in key : iso = isoL1TL2loose
#        if 't1m' in key : iso = isoL1ML2loose
#
#        if tup[1] == 'OS' : sign = 0
#        else : sign = 1
#    
#        params['channels'] = ['tt',]
#        params['mid2'] = tup[0]
#        params['mid3'] = key
#        params['additionalCut'] = '*(Z_SS==%i)*%s*(%s>0)*(njets<=2)' % (sign, iso, tup[4])
#        samples = checkBkgs( samples, params, grouping )
#        analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#    for key,tup in info.iteritems() :
#        plotSingle2( 'Mar17BTagged', key)
