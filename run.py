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
os.environ['_GROUPING_'] = analysis
os.environ['_ZHOME_'] = zHome


''' Uncomment to make out starting JSON file of meta data! '''
from meta.makeMeta import makeMetaJSON
os.chdir('meta')
#makeMetaJSON( analysis )
os.chdir('..')


''' Uncomment to make pile up vertex templates! '''
''' Not needed with HTT provided pu templates '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate, makeDYJetsPUTemplate
#if not os.path.exists( 'meta/PileUpInfo' ) : 
#    os.makedirs( 'meta/PileUpInfo' )
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 
#makeDYJetsPUTemplate( analysis )


''' Preset samples '''
SamplesSync = ['Sync-HtoTT']
SamplesData = ['data_em', 'data_tt']
SamplesDataCards = ['DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh', 'DYJetsLow', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'data_em', 'data_tt', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # As of April23, removed DYJets LO small sample

#SamplesDataCards = []
masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
for mass in masses :
       SamplesDataCards.append( 'ggH%i' % mass )
       SamplesDataCards.append( 'bbH%i' % mass )

#SamplesDataCards = ['data_tt','data_em']
#SamplesDataCards = ['DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh'] # LO DYJets
#SamplesDataCards = ['DYJetsLow',]
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
    'numFilesPerCycle' : 1,
    #'channels' : ['em', 'tt'],
    #'channels' : ['em', 'tt', 'et', 'mt'],
    #'channels' : ['em',],
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
    'mid1' : '1May01',
    'mid2' : '2May01',
    'mid3' : '3May01',
    'additionalCut' : '',
    'svFitPost' : 'true',
    #'svFitPost' : 'false',
    #'svFitPrep' : 'true',
    'svFitPrep' : 'false',
    'doFRMthd' : 'false',
}

samples = setUpDirs( samples, params, analysis )
analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)
#analysis1BaselineCuts.drawHistos( analysis, samples, **params )





