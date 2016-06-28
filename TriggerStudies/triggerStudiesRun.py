'''#################################################################
##     Trigger run file for Z or Higgs -> TauTau                  ##
##     Tyler Ruggles                                              ##
##     Jan 13, 2016                                               ##
#################################################################'''


import os
from time import gmtime, strftime
import ROOT
from ROOT import gPad, gROOT
from util.helpers import setUpDirs 
import analysis1BaselineCuts
ROOT.gROOT.Reset()

os.chdir('..')

''' Set analysis for Trigger Studies '''
analysis = 'Trigger'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
cmsLumi = '2200.0'
print "zHome: ",zHome
os.environ['_GROUPING_'] = analysis
os.environ['_ZHOME_'] = zHome
os.environ['_LUMI_'] = cmsLumi
lumiCert = 'Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt' # 2.11/fb - all of 2015 25ns golden
puJson = 'pileup_latest.txt' # Symlinked to newest pile_JSON_xxxxx.txt


''' Uncomment to make out starting JSON file of meta data! '''
#from meta.makeMeta import makeMetaJSON
#os.chdir('meta')
#makeMetaJSON( analysis, 'mt' )
#os.chdir('..')


''' Uncomment to make pile up vertex templates! '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate, makeDYJetsPUTemplate
#if not os.path.exists( 'meta/PileUpInfo' ) : 
#    os.makedirs( 'meta/PileUpInfo' )
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 
#makeDYJetsPUTemplate( analysis )


''' Preset samples '''
SamplesTrigger = ['ggHtoTauTau', 'data_mt']
samples = SamplesTrigger

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'numCores' : 20,
    'numFilesPerCycle' : 25,
    'channels' : ['mt'],
    'cutMapper' : 'trigCuts',
    'mid1' : '1Jan13_denom',
    'mid2' : '2Jan13_denom',
    'mid3' : '3Jan13_denom',
    'additionalCut' : '',
}

samples = setUpDirs( samples, params, analysis )
analysis1BaselineCuts.doInitialCutsAndOrder(analysis, samples, **params)




os.chdir('TriggerStudies')

