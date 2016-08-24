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
from util.helpers import setUpDirs 
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
    
    ''' Set analysis (25ns or Sync) '''
    analysis = 'htt'
    zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
    print "zHome: ",zHome
    
    
    
    ''' Preset samples '''
    SamplesDataCards = ['data_em', 'data_tt', 'DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # As of April24, removed LO DYJets small sample and DYJets m-150
    SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'ZZ2l2q', 'VV', 'data_tt'] # As of April23, removed DYJets LO small sample
    
    #masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
    #for mass in masses :
    #       SamplesDataCards.append( 'ggH%i' % mass )
    #       SamplesDataCards.append( 'bbH%i' % mass )
    #SamplesDataCards = ['DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh',] # As of April03
    #SamplesDataCards = ['DYJetsLow',] # As of April03
    #SamplesDataCards = ['WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4'] # As of April03
    samples = SamplesDataCards
    params = {
        'numCores' : 5,
        'numFilesPerCycle' : 10,
        'channels' : ['tt',],
        'mid1' : '1Feb24a',
        'mid2' : folder,
        'additionalCut' : '',
        'svFitPost' : 'false',
        'doFRMthd' : 'false',
    }

    isoL2loose = '(byVTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoL1TL2loose = '(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoL1ML2loose = '(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoL1LL2loose = '(byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoL1VTL2loose = '(byVTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoPt1GtrL1TL2loose = '(pt_1 > pt_2)*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoPt2GtrL1TL2loose = '(pt_1 < pt_2)*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoPt1GtrL1ML2loose = '(pt_1 > pt_2)*(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoPt2GtrL1ML2loose = '(pt_1 < pt_2)*(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)

    if isoL == '' :
        isoL2loose = '(byVTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)'
        isoL1TL2loose = isoL2loose
        isoL1ML2loose = isoL2loose
        isoL1LL2loose = isoL2loose
        isoL1VTL2loose = isoL2loose
    if sign == 'OS' :
        Zsign = 0
    else : 
        Zsign = 1
        
    print "IsoL2Loose: %s" % isoL2loose

    """
    Double Hardonic baseline with good QCD estimation
        Inclusive
    """
    ''' FINAL SELECTIONS MSSM '''
    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_%sl1ml2_%s_%sBTL' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtagLoose>0)*(njets<=1)' % (Zsign, isoL1ML2loose)
    #samples = setUpDirs( samples, params, analysis )
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_%sl1ml2_%s_%sNoBTL' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtagLoose==0)' % (Zsign, isoL1ML2loose)
    #samples = setUpDirs( samples, params, analysis )
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    ''' FINAL SELECTIONS ZTT && HIG-15-007 ZTT '''
    params['channels'] = ['tt',]
    params['mid3'] = folder+'_%sl1ml2_%s_%sZTT' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*%s*(pt_1 > 60 && pt_2 > 60)' % (Zsign, isoL1ML2loose)
    params['additionalCut'] = '*(Z_SS==%i)*%s' % (Zsign, isoL1ML2loose)
    samples = setUpDirs( samples, params, analysis )
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )
    
    return










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

    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlots", "/afs/cern.ch/user/t/truggles/www/%s/%s%s" % (folder[1:], channel, sufix1)])
    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlotsList", "/afs/cern.ch/user/t/truggles/www/%s/%s%s" % (folder[1:], channel, sufix1)])


    if not os.path.exists( '/afs/cern.ch/user/t/truggles/www/%s/%s%s' % (folder[1:], channel, sufix2) ) :
        os.makedirs( '/afs/cern.ch/user/t/truggles/www/%s/%s%s' % (folder[1:], channel, sufix2) )

    #subprocess.call(["python", "analysis3Plots.py", "--folder=%s_%s_%s"%(folder,channel,sufix2), "--useQCDMake=True", "--text=True", "--ratio=True", "--channels=%s"%channel, "--useQCDMakeName=%s"%sufix1])
    subprocess.call(["python", "analysis3Plots.py", "--folder=%s_%s_%s"%(folder,channel,sufix2), "--useQCDMake=True", "--ratio=True", "--channels=%s"%channel, "--useQCDMakeName=%s"%sufix1])

    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlots", "/afs/cern.ch/user/t/truggles/www/%s/%s%s" % (folder[1:], channel, sufix2)])
    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlotsList", "/afs/cern.ch/user/t/truggles/www/%s/%s%s" % (folder[1:], channel, sufix2)])


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

    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlots", "/afs/cern.ch/user/t/truggles/www/%s/%s%s%s" % (folder, channel, sufix1, btag)])
    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlotsList", "/afs/cern.ch/user/t/truggles/www/%s/%s%s%s" % (folder, channel, sufix1, btag)])


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

    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlots", "/afs/cern.ch/user/t/truggles/www/%s/%s" % (folder, folder2)])
    subprocess.call(["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlotsList", "/afs/cern.ch/user/t/truggles/www/%s/%s" % (folder, folder2)])



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




