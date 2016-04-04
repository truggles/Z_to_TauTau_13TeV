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


''' Preset samples '''
SamplesSync = ['Sync-HtoTT']
SamplesData = ['data_em', 'data_tt']
SamplesDataCards = ['DYJets', 'DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJetsHigh', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'data_em', 'data_tt', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # As of April03

#SamplesDataCards = []
# gg->H missing 250, 300, 350, 400.  bb->H missing 200, 2300
masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
for mass in masses :
       SamplesDataCards.append( 'ggH%i' % mass )
       SamplesDataCards.append( 'bbH%i' % mass )

#SamplesDataCards = ['data_tt',]
samples = SamplesDataCards

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'bkgs' : 'None',
    'numCores' : 20,
    'numFilesPerCycle' : 1,
    #'channels' : ['em', 'tt'],
    #'channels' : ['em', 'tt', 'et', 'mt'],
    #'channels' : ['em',],
    'channels' : ['tt',],
#XXX    'cutMapper' : 'signalCutsNoIsoNoSign', #!
    #'cutMapper' : 'signalCutsNoSign', #!
    #'cutMapper' : 'signalExtractionNoSign', #!
#XXX    'cutName' : 'PostSync', #!
#XXX    'cutMapper' : 'syncCutsDC',
    #'cutMapper' : 'syncCutsDCqcd',
    #'cutMapper' : 'crazyCutsNtuple',
    'cutMapper' : 'svFitCuts',
    #'cutMapper' : 'syncCutsNtuple',
    'cutName' : 'BaseLine',
#XXX    'cutMapper' : 'signalCuts',
    'mid1' : '1April03a',
    'mid2' : '2April03a',
    'mid3' : '3April03a',
    'additionalCut' : '',
    #'svFitPost' : 'true',
    'svFitPost' : 'false',
    'svFitPrep' : 'true',
    #'svFitPrep' : 'false',
}

samples = checkBkgs( samples, params, grouping )
analysis1BaselineCuts.doInitialCuts(grouping, samples, **params)
#analysis1BaselineCuts.doInitialOrder(grouping, samples, **params)
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )

#params['mid3'] = '3Feb02sDC_SS'
#params['additionalCut'] = '*(Z_SS==1)'
#samples = checkBkgs( samples, params, grouping )
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#
#params['mid3'] = '3Feb02sDC_OS'
#params['additionalCut'] = '*(Z_SS==0)'
#samples = checkBkgs( samples, params, grouping )
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )





