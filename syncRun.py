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
    #'numFilesPerCycle' : 2,
    'numFilesPerCycle' : 1,
    #'channels' : ['tt','em',],
    'channels' : ['tt',],
    #'channels' : ['em',],
    #'cutMapper' : 'syncCutsMSSMNtuple',
    'cutMapper' : 'syncCutsSMHTTNtuple',
    #'cutMapper' : 'crazyCutsNtuple',
    'mid1' : '1Jan30',
    'mid2' : '2Jan30',
    'mid3' : '3Jan30',
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

analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)





