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
grouping = 'dataCards'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
print "zHome: ",zHome
os.environ['_GROUPING_'] = grouping
os.environ['_ZHOME_'] = zHome


''' Uncomment to make out starting JSON file of meta data! '''
from meta.makeMeta import makeMetaJSON
os.chdir('meta')
#makeMetaJSON( grouping )
os.chdir('..')


''' Uncomment to make pile up vertex templates! '''
''' Not needed with HTT provided pu templates '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate, makeDYJetsPUTemplate
#if not os.path.exists( 'meta/PileUpInfo' ) : 
#    os.makedirs( 'meta/PileUpInfo' )
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 
#makeDYJetsPUTemplate( grouping )


''' Fake Factors '''
SamplesDataCards = ['DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh', 'T-tchan', 'Tbar-tchan', 'Tbar-tW', 'T-tW', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # Fake Factor List, May 02 
#SamplesDataCards = ['data_tt',]
samples = SamplesDataCards

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    #'debug' : 'true',
    'debug' : 'false',
    'bkgs' : 'None',
    'numCores' : 10,
    'numFilesPerCycle' : 10,
    'channels' : ['tt',],
    #'cutMapper' : 'signalCutsNoIsoNoSign', #!
    #'cutMapper' : 'signalCutsNoSign', #!
    #'cutMapper' : 'signalCuts', #!
    #'cutMapper' : 'signalExtractionNoSign', #!
    #'cutName' : 'PostSync', #!
    #'cutMapper' : 'syncCutsDC',
    #'cutMapper' : 'syncCutsDCqcd',
#XXX    'cutMapper' : 'syncCutsDCqcdTES',
    #'cutMapper' : 'crazyCutsNtuple',
#XXX    'cutMapper' : 'svFitCuts',
    #'cutMapper' : 'syncCutsNtuple',
    'cutMapper' : 'signalCuts',
#XXX    'cutMapper' : 'fakeFactorCutsTT',
    'cutName' : 'BaseLine',
    'mid1' : '1May02_FakeFactors',
    'mid2' : '2May02_FakeFactors',
    'mid3' : '3May02_FakeFactors',
    'additionalCut' : '',
    #'svFitPost' : 'true',
    'svFitPost' : 'false',
    #'svFitPrep' : 'true',
    'svFitPrep' : 'false',
}

#samples = checkBkgs( samples, params, grouping )
analysis1BaselineCuts.doInitialCuts(grouping, samples, **params)
analysis1BaselineCuts.doInitialOrder(grouping, samples, **params)

SamplesDataCards = ['data_tt',]
samples = SamplesDataCards
samples = checkBkgs( samples, params, grouping )
params['cutMapper'] = 'fakeFactorCutsTT'
analysis1BaselineCuts.doInitialCuts(grouping, samples, **params)
analysis1BaselineCuts.doInitialOrder(grouping, samples, **params)




