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
from util.helpers import checkBkgs 
ROOT.gROOT.Reset()



''' Set grouping (25ns or Sync) '''
grouping = 'Sync'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
cmsLumi = '2260.0'
print "zHome: ",zHome
os.environ['_GROUPING_'] = grouping
os.environ['_ZHOME_'] = zHome
os.environ['_LUMI_'] = cmsLumi


''' Uncomment to make out starting JSON file of meta data! '''
from meta.makeMeta import makeMetaJSON
os.chdir('meta')
#makeMetaJSON( grouping )
os.chdir('..')


''' Preset samples '''
SamplesSync = ['Sync-HtoTT']
samples = SamplesSync

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'bkgs' : 'None',
    'numCores' : 16,
    'numFilesPerCycle' : 2,
    'channels' : ['em', 'tt'],
    #'channels' : ['tt'],
    #'channels' : ['em'],
    #'channels' : ['em', 'tt', 'et', 'mt'],
    'cutMapper' : 'syncCutsNtuple',
    #'cutMapper' : 'crazyCutsNtuple',
    'cutName' : 'BaseLine',
    'mid1' : '1Feb17a',
    'mid2' : '2Feb17a',
    'mid3' : '3Feb17a',
    'additionalCut' : '',
    'svf' : 'true',
    'svfName' : '/data/truggles/Sync_feb16_svFitted2/TauTau_13_Sync1Feb12d-',
    #'svfName' : '/hdfs/store/user/truggles/SyncTry1/Sync1Feb12d/TauTau_13_Sync1Feb12d-',
    #'svf' : 'false',
}

samples = checkBkgs( samples, params, grouping )
#analysis1BaselineCuts.doInitialCuts(grouping, samples, **params)
analysis1BaselineCuts.doInitialOrder(grouping, samples, **params)





