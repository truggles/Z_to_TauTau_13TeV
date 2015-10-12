'''#################################################################
##     Analysis run file for Z or Higgs -> TauTau                 ##
##     Tyler Ruggles                                              ##
##     Oct 11, 2015                                               ##
#################################################################'''


import os
from time import gmtime, strftime
import ROOT
from ROOT import gPad, gROOT

# Set grouping (25ns or Sync)
grouping = '25ns'
os.environ['_GROUPING_'] = grouping


#sampPrefix = os.getenv('_GROUPING_', '25ns') # 25ns is default

''' Uncomment to make out starting JSON file of meta data! '''
#from meta.makeMeta import makeMetaJSON
#os.chdir('meta')
#makeMetaJSON( 'Sync' )
#os.chdir('..')


''' Preset samples '''
SamplesSync = ['Sync_HtoTT']
SamplesData = ['data_em', 'data_tt']
Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TTJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'WZ3l1nu', 'ZZ', 'ZZ4l', 'TT', 'TTPow'] # extra TT samples on stand by
Samples25nsFinal = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TT', 'WW', 'WZJets', 'ZZ'] # Intended good one

''' Uncomment to make pile up vertex templates! '''
#from util.pileUpVertexCorrections import buildAllPUTemplates
#buildAllPUTemplates( Samples25ns, numCores )

import analysis1BaselineCuts

ROOT.gROOT.Reset()

params = {
    'bkgs' : 'WJets',
    'numCores' : 18,
    'numFilesPerCycle' : 100,
    'cutMapper' : 'quickCutMapSingleCut',
    'cutName' : 'PostSync',
    'mid1' : '1oct12',
    'mid2' : '2oct12',
    'mid3' : '3oct12',
}

### option 2 = Signal level cuts
#cutMapper = 'QCDYieldOS'
#cutName = 'QCDYield'
samples = Samples25nsFinal

bkgMap = analysis1BaselineCuts.getBkgMap()
if params[ 'bkgs' ] != 'None' :
    params[ 'cutMapper' ] = bkgMap[ params[ 'bkgs' ] ][0]
    params[ 'cutName' ] = bkgMap[ params[ 'bkgs' ] ][0]
    samples = bkgMap[ params [ 'bkgs' ] ][1]

#samples = ['data_em', 'data_tt', 'Tbar-tW', 'T-tW',]
#analysis1BaselineCuts.drawHistos( grouping, Samples25nsFinal, bkgs, numFilesPerCycle, mid2, mid3 )
#analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, mid1, mid2, bkgs, cutMapper, cutName, numFilesPerCycle, numCores)
analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
analysis1BaselineCuts.drawHistos( grouping, samples, **params )
