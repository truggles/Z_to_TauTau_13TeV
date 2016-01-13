'''#################################################################
##     Analysis run file for Z or Higgs -> TauTau                 ##
##     Tyler Ruggles                                              ##
##     Oct 11, 2015                                               ##
#################################################################'''


import os
from time import gmtime, strftime
import ROOT
from ROOT import gPad, gROOT
from util.helpers import checkBkgs 
import analysis1BaselineCuts
ROOT.gROOT.Reset()


''' Set grouping for Trigger Studies '''
grouping = 'Trigger'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
cmsLumi = '220.0'
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


''' Uncomment to make pile up vertex templates! '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate, makeDYJetsPUTemplate
#if not os.path.exists( 'meta/PileUpInfo' ) : 
#    os.makedirs( 'meta/PileUpInfo' )
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 
#makeDYJetsPUTemplate( grouping )


''' Preset samples '''
SamplesTrigger = ['ggH', 'data_trig']
samples = SamplesTrigger

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'bkgs' : 'None',
    'numCores' : 20,
    'numFilesPerCycle' : 25,
    'channels' : ['mt'],
    'cutMapper' : 'trigCuts',
    'cutName' : 'BaseLine',
    'mid1' : '1Jan13_denom',
    'mid2' : '2Jan13_denom',
    'mid3' : '3Jan13_denom',
    'additionalCut' : '',
}

samples = checkBkgs( samples, params )
analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)

params['mid3'] = '3jan13_numerLIsoTau20'
params['additionalCut'] = '*(mMatchesIsoMu17LooseIsoTau20Path > 0.5)' # && L1_trigObj_pt > 0
samples = checkBkgs( samples, params )
analysis1BaselineCuts.drawHistos( grouping, samples, **params )


params['mid3'] = '3jan13_numerMIsoTau35'
params['additionalCut'] = '*(mMatchesIsoMu17MedIsoTau35Path > 0.5)' # && L1_trigObj_pt > 0
samples = checkBkgs( samples, params )
analysis1BaselineCuts.drawHistos( grouping, samples, **params )






