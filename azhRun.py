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
analysis = 'azh'
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
azhSamples = ['data_ee', 'data_mm', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'ggZZ4e', 'ggZZ4m', 'ggZZ2m2t', 'TTJ', 'TTZ', 'TTTT', 'WZ3l1nu', 'WminusHtoTauTau', 'WplusHtoTauTau', 'ZHtoTauTau', 'ZZ2l2q', 'ZZ4l'],
samples = azhSamples

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'debug' : 'true',
    #'debug' : 'false',
    'numCores' : 10,
    'numFilesPerCycle' : 20,
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
    'mid1' : '1June26',
    'mid2' : '2June26',
    'mid3' : '3June26',
    'additionalCut' : '',
    #'svFitPost' : 'true',
    'svFitPost' : 'false',
    #'svFitPrep' : 'true',
    'svFitPrep' : 'false',
    'doFRMthd' : 'false',
}

samples = setUpDirs( samples, params, analysis )
#analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)
#analysis1BaselineCuts.drawHistos( analysis, samples, **params )





