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
lumiCert = 'Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt' # 2.11/fb - all of 2015 25ns golden
puJson = 'pileup_latest.txt' # Symlinked to newest pile_JSON_xxxxx.txt


''' Uncomment to make out starting JSON file of meta data! '''
from meta.makeMeta import makeMetaJSON
os.chdir('meta')
makeMetaJSON( grouping )
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
    'numCores' : 10,
    'numFilesPerCycle' : 25,
    'channels' : ['em', 'tt'],
    #'channels' : ['em', 'tt', 'et', 'mt'],
    'cutMapper' : 'syncCutsNtuple',
    'cutName' : 'BaseLine',
    'mid1' : '1Feb08Sync',
    'mid2' : '2Feb08Sync',
    'mid3' : '3Feb08Sync',
    'additionalCut' : '',
}

samples = checkBkgs( samples, params, grouping )
analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)





