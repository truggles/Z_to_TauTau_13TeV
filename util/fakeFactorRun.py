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



''' Set analysis (25ns or Sync) '''
analysis = 'dataCards'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
print "zHome: ",zHome


''' Uncomment to make out starting JSON file of meta data! '''
from meta.makeMeta import makeMetaJSON
os.chdir('meta')
#makeMetaJSON( analysis )
os.chdir('..')


''' Uncomment to make pile up vertex templates! '''
''' Not needed with HTT provided pu templates '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate, makeDYJetsPUTemplate
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 
#makeDYJetsPUTemplate( analysis )


''' Fake Factors '''
SamplesDataCards = ['TT', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'DYJetsLow', 'DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh', 'T-tchan', 'Tbar-tchan', 'Tbar-tW', 'T-tW', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # Fake Factor List, May 02 
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
    'numCores' : 10,
    'numFilesPerCycle' : 10,
    'channels' : ['tt',],
    #'cutMapper' : 'signalCutsNoIsoNoSign', #!
    #'cutMapper' : 'signalCutsNoSign', #!
    #'cutMapper' : 'signalCuts', #!
    #'cutMapper' : 'signalExtractionNoSign', #!
    #'cutMapper' : 'syncCutsDC',
    #'cutMapper' : 'syncCutsDCqcd',
#XXX    'cutMapper' : 'syncCutsDCqcdTES',
    #'cutMapper' : 'crazyCutsNtuple',
#XXX    'cutMapper' : 'svFitCuts',
    #'cutMapper' : 'syncCutsNtuple',
    'cutMapper' : 'signalCuts',
#XXX    'cutMapper' : 'fakeFactorCutsTT',
    'mid1' : '1May02_FakeFactors',
    'mid2' : '2May02_FakeFactors',
    'mid3' : '3May02_FakeFactors',
    'additionalCut' : '',
    #'svFitPost' : 'true',
    'svFitPost' : 'false',
    #'svFitPrep' : 'true',
    'svFitPrep' : 'false',
    'doFRMthd' : 'true',
}

#samples = setUpDirs( samples, params, analysis )
#analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
#analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)
analysis1BaselineCuts.drawHistos( analysis, samples, **params)

SamplesDataCards = ['data_tt',]
samples = SamplesDataCards
samples = setUpDirs( samples, params, analysis )
params['cutMapper'] = 'fakeFactorCutsTT'
#analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
#analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)
analysis1BaselineCuts.drawHistos( analysis, samples, **params)



SamplesDataCards = ['data_tt',]
params['doFRMthd'] = 'false'
params['additionalCut'] = '*(t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 && t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5)'
samples = SamplesDataCards
samples = setUpDirs( samples, params, analysis )
params['cutMapper'] = 'fakeFactorCutsTT'
analysis1BaselineCuts.drawHistos( analysis, samples, **params)

