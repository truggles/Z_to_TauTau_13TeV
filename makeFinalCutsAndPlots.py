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
from smart_getenv import getenv


p = argparse.ArgumentParser(description="A script to apply additional cuts and plot.")
p.add_argument('--folder', action='store', default='xxx', dest='folder', help="What is the full folder name for extracting root files?")
p.add_argument('--isoVal', action='store', default='Tight', dest='isoVal', help="What is the signal selection tau MVA isolation? Tight? VTight?")
p.add_argument('--skimmed', action='store', default='false', dest='skimmed', help="Using skimmed samples?")
p.add_argument('--skipSSQCDDetails', action='store', default=False, dest='skipSSQCDDetails', type=bool, help="Using skimmed samples?")
p.add_argument('--samples', action='store', dest='samples', nargs='+', type=str, help="Pass in a list of space separated samples")
options = p.parse_args()
folder = options.folder
skimmed = options.skimmed
skipSSQCDDetails = options.skipSSQCDDetails
isoVal = options.isoVal
samples = options.samples
print "Options Skimmed:",skimmed
print "samples: ",samples

def testQCDCuts( folder, samples, isoVal, isoL, isoT, sign, doFF=False ) :
    if folder == 'xxx' :
        print "ERROR: Folder was not choosen"
        return
    
    ''' Set analysis (25ns or Sync) '''
    analysis = 'htt'
    zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
    print "zHome: ",zHome
    
    
    
    if sign == 'OS' :
        skipSSQCDDetailsX = False
    else : 
        skipSSQCDDetailsX = True


    ''' Preset samples '''
    
    params = {
        'numCores' : 8,
        'numFilesPerCycle' : 1,
        'channels' : ['tt',],
        'mid1' : '1Feb24a',
        'mid2' : folder,
        'additionalCut' : '',
        'svFitPost' : 'false',
        'doFRMthd' : 'false',
        'skimmed' : skimmed,
        'skipSSQCDDetails' : skipSSQCDDetailsX,
        'debug' : 'true'
        #'debug' : 'false'
    }

    isoCutter = '((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)\
            || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_1 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_1 > 0.5))' % (isoT, isoL, isoT, isoL)

    if isoL == '' :
        isoCutter = '(by%sIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)' % (isoVal, isoVal)

    # If doing Fake Factors, we will add isolation cuts later
    # for convenience
    if doFF : isoCutter = '(1)'

    if sign == 'OS' :
        Zsign = 0
    else : 
        Zsign = 1
        
    print "\n\nIsoL1ML2Loose: %s\n\n" % isoCutter
    print "skipSSQCDDetails:", skipSSQCDDetailsX

    """
    Double Hardonic baseline with good QCD estimation
        Inclusive
    """
    ### FINAL SELECTIONS MSSM ###
    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_%sl1ml2_%s_%sBTL' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtagLoose>0)*(njets<=1)' % (Zsign, isoCutter)
    #samples = setUpDirs( samples, params, analysis )
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    #params['channels'] = ['tt',]
    #params['mid3'] = folder+'_%sl1ml2_%s_%sNoBTL' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*%s*(nbtagLoose==0)' % (Zsign, isoCutter)
    #samples = setUpDirs( samples, params, analysis )
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    ### FINAL SELECTIONS ZTT && HIG-15-007 ZTT ###
    params['channels'] = ['tt',]
    params['mid3'] = folder+'_%sl1ml2_%s_%sZTTinclusive' % (sign, isoT, isoL)
    params['additionalCut'] = '*(Z_SS==%i)*%s' % (Zsign, isoCutter)
    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    import analysis3Plots
    from meta.sampleNames import returnSampleDetails
    samples = returnSampleDetails( analysis, samples )
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    #### LEGACY HTT CATEGORIES ###
    higgsPtVar = 'Higgs_PtCor'
    #higgsPtVar = 'pt_sv'
#    params['mid3'] = folder+'_%sl1ml2_%s_%sZTT1jet_low' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*(%s>100 && %s<170)*(jetVeto30==1 ||\
#        (jetVeto30>=2 && !(mjj>300 && abs(jdeta) > 2.5 && njetingap < 1)))*%s' % (Zsign, higgsPtVar, higgsPtVar, isoCutter)
#    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
#    analysis1BaselineCuts.drawHistos( analysis, samples, **params )
#
#    params['mid3'] = folder+'_%sl1ml2_%s_%sZTT1jet_high' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*(%s>170)*(jetVeto30==1 ||\
#        (jetVeto30>=2 && !(mjj>300 && abs(jdeta) > 2.5 && njetingap < 1)))*%s' % (Zsign, higgsPtVar, isoCutter)
#    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
#    analysis1BaselineCuts.drawHistos( analysis, samples, **params )
#
#    params['mid3'] = folder+'_%sl1ml2_%s_%sZTTvbf_low' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30>=2 && abs(jdeta) > 2.5 && njetingap < 1)*((%s<100 && mjj>300) || (%s>100 && mjj>300 && mjj<500))*%s' % (Zsign, higgsPtVar, higgsPtVar, isoCutter)
#    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
#    analysis1BaselineCuts.drawHistos( analysis, samples, **params )
#
#    params['mid3'] = folder+'_%sl1ml2_%s_%sZTTvbf_high' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30>=2 && %s>100 && mjj>500 && abs(jdeta)>2.5 && njetingap<1)*%s' % (Zsign, higgsPtVar, isoCutter)
#    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
#    analysis1BaselineCuts.drawHistos( analysis, samples, **params )
#
#    params['mid3'] = folder+'_%sl1ml2_%s_%sZTT0jet' % (sign, isoT, isoL)
#    params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==0)*%s' % (Zsign, isoCutter)
#    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
#    analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    #### For checking distributions ###
    #params['mid3'] = folder+'_%sl1ml2_%s_%sZTT1jet' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==1)*%s' % (Zsign, isoCutter)
    #setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )
 
    #params['mid3'] = folder+'_%sl1ml2_%s_%sZTT2jet' % (sign, isoT, isoL)
    #params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==2)*%s' % (Zsign, isoCutter)
    #setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    ### 2D Distributions ###
    params['mid3'] = folder+'_%sl1ml2_%s_%sZTTboosted' % (sign, isoT, isoL)
    params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==1 || ((jetVeto30>=2)*!(abs(jdeta) > 2.5 && %s>100)))*%s' % (Zsign, higgsPtVar, isoCutter)
    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    params['mid3'] = folder+'_%sl1ml2_%s_%sZTTvbf' % (sign, isoT, isoL)
    params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30>=2)*(%s>100)*(abs(jdeta)>2.5)*%s' % (Zsign, higgsPtVar, isoCutter)
    setUpDirs( samples, params, analysis ) # Print config file and set up dirs
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    params['mid3'] = folder+'_%sl1ml2_%s_%sZTT0jet2D' % (sign, isoT, isoL)
    params['additionalCut'] = '*(Z_SS==%i)*(jetVeto30==0)*%s' % (Zsign, isoCutter)
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

    isoPairs = [
# QCD Syst Mthd Closure        ('VLoose','Loose'), # qcd Syst check
# QCD Syst Mthd Closure        ('Loose','Tight'), # qcd Syst check
# QCD Syst Mthd Closure        ('','Tight'), # qcd Syst check
# QCD Syst Mthd Closure        ('','Loose'), # qcd Syst check
        ('Loose',isoVal), # Normal running
        ('',isoVal), # Normal running
    ]

    ### Check if we intend to do Fake Factor based MC cuts
    ### These differ because of requiring a random choice
    ### of l1 and l2, then seeing if l1 is gen matched
    ### to anything besides a fake/jet
    ### This is only applied for DYJets, WJets, TT, and QCD MC
    doFF = getenv('doFF', type=bool)
    if doFF :
        # The '' in the following line gives us the signal region
        testQCDCuts( folder, samples, isoVal, '', isoVal, 'OS', doFF )
    else :
        for pair in isoPairs :
            for sign in ['OS', 'SS']:
                testQCDCuts( folder, samples, isoVal, pair[0], pair[1], sign )

#XXX    testQCDCuts( folder, '', 'VTight', 'OS' )




