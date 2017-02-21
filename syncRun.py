'''#################################################################
##     Analysis run file for Z or Higgs -> TauTau                 ##
##     Tyler Ruggles                                              ##
##     Oct 11, 2015                                               ##
#################################################################'''


import os
from time import gmtime, strftime
import ROOT
from ROOT import gPad, gROOT
import analysis1BaselineCuts
from util.helpers import setUpDirs 
ROOT.gROOT.Reset()



''' Set analysis (htt, Sync, azh) '''
analysis = 'Sync'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
print "zHome: ",zHome


''' Uncomment to make out starting JSON file of meta data! '''
from meta.makeMeta import makeMetaJSON
os.chdir('meta')
''' General samples.json file from /data/truggles files '''
#makeMetaJSON( analysis, channel='tt' )
''' samples.json for post /hdfs skim -> uwlogin samples '''
#makeMetaJSON( analysis, channel='tt', skimmed=True )
os.chdir('..')


''' Preset samples '''
SamplesSync = ['Sync-HtoTT','Sync-VBF125','Sync-DYJets4']
SamplesSync = ['Sync-VBF125',]
SamplesSync = ['Sync-data2016RunB',]
#SamplesSync = ['Sync-DYJets4',]
samples = SamplesSync

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    #'debug' : 'true',
    'debug' : 'false',
    'numCores' : 14,
    'numFilesPerCycle' : 1,
    'channels' : ['tt',],
    #'cutMapper' : 'syncCutsSMHTTNtuple', # Standard synchronization ntuple
    'cutMapper' : 'syncCutsDCqcdTES5040VL', # This is the same cut as applied for signal extraction, we choose the "best" version of an event after this cut, then perform additional cuts below if "makeSyncCategories" == True 
    'mid1' : '1Feb20_dataB_1evt4',
    'mid2' : '2Feb20_dataB_1evt4',
    'mid3' : '3Feb20_dataB_1evt4',
    'additionalCut' : '',
    #'svFitPost' : 'true',
    'svFitPost' : 'false',
    'svFitPrep' : 'false',
    #'svFitPrep' : 'true',
    'doFRMthd' : 'false',
    'skimHdfs' : 'false',
    #'skimHdfs' : 'true',
    'skimmed' : 'false',
    #'skimmed' : 'true',
}

""" Get samples with map of attributes """
setUpDirs( samples, params, analysis ) # Print config file and set up dirs
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )

#analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
#analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)



makeSyncCategories = True
makeSyncCategories = False
if makeSyncCategories :
    print "Making Sync Categories"
    print "\n\n  Make sure you have dealt with any svFit vs. non-svFit changes!!!!\n\n"
    print "cd folder"
    print "hadd Sync-data2016RunB_tt.root Sync-data2016RunB_*_tt.root"

    from util.ttreeWithCuts import ttreeWithCuts

    higgsPtVar = 'Higgs_PtCor'

    cutsMap = {
        'VBF' : '((jetVeto30>=2)*(%s>100)*(abs(jdeta)>2.5))' % higgsPtVar,
        'Boosted' : '(jetVeto30==1 || ((jetVeto30>=2)*!(abs(jdeta) > 2.5 && %s>100)))' % higgsPtVar,
        '0Jet' : '(jetVeto30==0)',
    }

    forAll = '(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && Z_SS==0 && ptCor_1 > 50 && ptCor_2 > 40)'

    oldFile = 'tmp.root'
    oldTreePath = 'Ntuple'

    for cat in ['VBF','Boosted','0Jet'] :
        print "Category!  %s" % cat
        cut = forAll + ' * ' + cutsMap[cat]
        
        fOutName = 'syncNtuple_DATA_NEW_%s.root' % cat
        ttreeWithCuts( oldFile, oldTreePath, fOutName, cut )
        



