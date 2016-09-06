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
p.add_argument('--isoVal', action='store', default='Tight', dest='isoVal', help="What is the signal selection tau MVA isolation? Tight? VTight?")
p.add_argument('--skimmed', action='store', default='false', dest='skimmed', help="Using skimmed samples?")
p.add_argument('--samples', action='store', dest='samples', nargs='+', type=str, help="Pass in a list of space separated samples")
options = p.parse_args()
folder = options.folder
skimmed = options.skimmed
isoVal = options.isoVal
samples = options.samples
print "Options Skimmed:",skimmed
print "samples: ",samples

def testQCDCuts( folder, samples, isoVal, isoL, isoT, sign ) :
    if folder == 'xxx' :
        print "ERROR: Folder was not choosen"
        return
    
    ''' Set analysis (25ns or Sync) '''
    analysis = 'htt'
    zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
    print "zHome: ",zHome
    
    
    
    ''' Preset samples '''
    
    params = {
        'numCores' : 5,
        'numFilesPerCycle' : 1,
        'channels' : ['tt',],
        'mid1' : '1Feb24a',
        'mid2' : folder,
        'additionalCut' : '',
        'svFitPost' : 'false',
        'doFRMthd' : 'false',
        'skimmed' : skimmed,
    }

    isoL2loose = '(by%sIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoVal, isoT, isoL)
    isoL1TL2loose = '(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoL1ML2loose = '(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoL1LL2loose = '(byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoL1VTL2loose = '(byVTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoPt1GtrL1TL2loose = '(pt_1 > pt_2)*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoPt2GtrL1TL2loose = '(pt_1 < pt_2)*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoPt1GtrL1ML2loose = '(pt_1 > pt_2)*(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)
    isoPt2GtrL1ML2loose = '(pt_1 < pt_2)*(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoT, isoL)

    if isoL == '' :
        isoL2loose = '(by%sIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoVal, isoVal)
        isoL1TL2loose = isoL2loose
        isoL1ML2loose = isoL2loose
        isoL1LL2loose = isoL2loose
        isoL1VTL2loose = isoL2loose
    if sign == 'OS' :
        Zsign = 0
    else : 
        Zsign = 1
        
    print "\n\nIsoL2Loose: %s\n\n" % isoL2loose

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
    params['additionalCut'] = '*(Z_SS==%i)*%s' % (Zsign, isoL1ML2loose)
    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    import analysis3Plots
    from meta.sampleNames import returnSampleDetails
    samples = returnSampleDetails( analysis, samples )
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    ''' PRELIMINARY SELECTIONS FROM LAURA FOR SM-HIGGS -> TAUTAU 2016 '''
    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_%sl1ml2_%s_%sZTT0Jet' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==0)*%s' % (Zsign, isoL1ML2loose)
    #setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )
    #
    #params['mid3'] = folder+'_%sl1ml2_%s_%sZTT1Jet' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==1 && bjetCISVVeto30Medium == 0)*%s' % (Zsign, isoL1ML2loose)
    #setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )
    #
    #params['mid3'] = folder+'_%sl1ml2_%s_%sZTTVBF' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==2 && mjj > 400 && abs(jdeta) > 3.5 && bjetCISVVeto30Medium == 0)*%s' % (Zsign, isoL1ML2loose)
    #setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    #''' CUTS TO MATCH ISOBEL'S '''
    params['mid3'] = folder+'_%sl1ml2_%s_%sZTT1jet_low' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==1 && Higgs_Pt>100 && bjetCISVVeto30MediumZTT == 0)*%s' % (Zsign, isoL1ML2loose)
    params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==1 && Higgs_Pt>100 )*%s' % (Zsign, isoL1ML2loose)
    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    params['mid3'] = folder+'_%sl1ml2_%s_%sZTT1jet_high' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==1 && Higgs_Pt>170 && bjetCISVVeto30MediumZTT == 0)*%s' % (Zsign, isoL1ML2loose)
    params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==1 && Higgs_Pt>170 )*%s' % (Zsign, isoL1ML2loose)
    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    params['mid3'] = folder+'_%sl1ml2_%s_%sZTTvbf' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==2 && Higgs_Pt>100 && bjetCISVVeto30MediumZTT == 0 && mjj>500 && abs(jdeta) > 3.5 && njetingap20 < 1)*%s' % (Zsign, isoL1ML2loose)
    params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==2 && Higgs_Pt>100 && mjj>500 && abs(jdeta) > 3.5 && njetingap20 < 1)*%s' % (Zsign, isoL1ML2loose)
    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
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
        ('Loose',isoVal),
        #XXX('Loose','Tight'),
#        ('Medium','Tight'),
        #('Medium','VTight'),
#        ('Tight','VTight'),
        ('',isoVal),
        #XXX('','Tight'),
    ]

    for pair in isoPairs :
        for sign in ['OS', 'SS']:
            testQCDCuts( folder, samples, isoVal, pair[0], pair[1], sign )

#XXX    testQCDCuts( folder, '', 'VTight', 'OS' )




