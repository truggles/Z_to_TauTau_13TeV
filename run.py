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
#SamplesDataCards = ['data_em', 'data_tt', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'DYJets', 'DYJetsLow', 'T-tW', 'T-tchan', 'TT', 'Tbar-tW', 'Tbar-tchan', 'WJets', 'WW1l1nu2q', 'WW2l2nu', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZ3l1nu', 'ZZ2l2nu', 'ZZ2l2q', 'ZZ4l']#, 'QCD15-20', 'QCD20-30', 'QCD30-80', 'QCD80-170', 'QCD170-250', 'QCD250-Inf'] # Set list for Data Card Sync (less DYJetsLow)
#SamplesDataCards = ['data_em', 'data_tt', 'ggHtoTauTau125', 'ggHtoTauTau130', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'DYJets', 'DYJets100-200', 'DYJets200-400', 'DYJets400-600', 'DYJets600-Inf', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'WJets', 'WJets100-200', 'WJets200-400', 'WJets400-600', 'WJets600-Inf', 'WW1l1nu2q', 'WZ1l3nu', 'ZZ4l'] # As we wait for all samples 76x to come in, this is our complete list
SamplesDataCards = ['data_em', 'data_tt', 'ggHtoTauTau125', 'VBFHtoTauTau125', 'DYJets', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WW1l1nu2q', 'WZ1l3nu', 'WZ1l1nu2q', 'ZZ2l2q', 'ZZ4l'] # As of Feb11

#SamplesDataCards = []
masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 600, 900, 1000, 1200, 1500, 2900, 3200]
for mass in masses :
       SamplesDataCards.append( 'ggH%i' % mass )
       SamplesDataCards.append( 'bbH%i' % mass )

#samples = SamplesData
samples = SamplesDataCards

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'bkgs' : 'None',
    'numCores' : 10,
    'numFilesPerCycle' : 2,
    #'channels' : ['em', 'tt'],
    #'channels' : ['em', 'tt', 'et', 'mt'],
    #'channels' : ['em',],
    'channels' : ['tt',],
    #'cutMapper' : 'signalCutsNoIsoNoSign', #!
    #'cutMapper' : 'signalCutsNoSign', #!
    #'cutMapper' : 'signalExtractionNoSign', #!
    #'cutName' : 'PostSync', #!
    'cutMapper' : 'syncCutsDC',
    #'cutMapper' : 'syncCutsNtuple',
    'cutName' : 'BaseLine',
    'mid1' : '1Feb11a',
    'mid2' : '2Feb11a',
    'mid3' : '3Feb11a',
    'additionalCut' : '',
}

samples = checkBkgs( samples, params, grouping )
analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)

#params['mid3'] = '3Feb02sDC_SS'
#params['additionalCut'] = '*(Z_SS==1)'
#samples = checkBkgs( samples, params, grouping )
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#
#params['mid3'] = '3Feb02sDC_OS'
#params['additionalCut'] = '*(Z_SS==0)'
#samples = checkBkgs( samples, params, grouping )
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )


''' for WJets and QCD shapes 
uncomment and run each time you change cuts '''
#params[ 'bkgs' ] = 'WJets'
#samples = checkBkgs( samples, params, grouping )
##analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#params[ 'bkgs' ] = 'QCDSync'
#samples = checkBkgs( samples, params, grouping )
#analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
