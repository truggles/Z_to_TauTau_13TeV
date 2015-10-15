'''#################################################################
##     Analysis run file for Z or Higgs -> TauTau                 ##
##     Tyler Ruggles                                              ##
##     Oct 11, 2015                                               ##
#################################################################'''


import os
from time import gmtime, strftime
import ROOT
from ROOT import gPad, gROOT
ROOT.gROOT.Reset()

''' Set grouping (25ns or Sync) '''
grouping = '25ns'
os.environ['_GROUPING_'] = grouping
#sampPrefix = os.getenv('_GROUPING_', '25ns') # 25ns is default

''' Preset samples '''
SamplesSync = ['Sync_HtoTT']
SamplesData = ['data_em', 'data_tt']
Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TTJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'WZ3l1nu', 'ZZ', 'ZZ4l', 'TT', 'TTPow', 'ggHtoTauTau', 'VBFHtoTauTau'] # extra TT samples on stand by
Samples25nsFinal = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TTJets', 'WW', 'WZJets', 'ZZ', 'ggHtoTauTau', 'VBFHtoTauTau'] # Intended good one
#samples = ['data_em', 'data_tt', 'Tbar-tW', 'T-tW',]
#samples = ['DYJets',]# 'Tbar-tW', 'T-tW',]
#samples = ['ggHtoTauTau', 'VBFHtoTauTau']
#samples = ['WJets']

#samples = Samples25nsFinal
samples = SamplesData
params = {
    'bkgs' : 'None',
    'numCores' : 10,
    'numFilesPerCycle' : 100,
    #'cutMapper' : 'quickCutMapSingleCut',
    'cutMapper' : 'testLooserTriggers',
    'cutName' : 'PostSync',
    #'cutMapper' : 'QCDYieldOS',
    #'cutName' : 'QCDYield',
    'mid1' : '1oct15LooserTrig',
    #'mid2' : 'Oct12MCandData/25ns2oct12',
    #'mid3' : 'Oct12MCandData/25ns3oct12',
    'mid2' : '2oct15LooserTrig',
    'mid3' : '3oct15LooserTrig',
    'additionalCut' : '',
    #'additionalCut' : '*(nbtag<1)*(mt_2<80)',
}


''' Uncomment to make out starting JSON file of meta data! '''
#from meta.makeMeta import makeMetaJSON
#os.chdir('meta')
#makeMetaJSON( grouping )
#os.chdir('..')


''' Uncomment to make pile up vertex templates! '''
#from util.pileUpVertexCorrections import buildAllPUTemplates
#buildAllPUTemplates( samples, params['numCores'] )


import analysis1BaselineCuts
bkgMap = analysis1BaselineCuts.getBkgMap()
def checkBkgs( samples, params, bkgMap ) :
    if params[ 'bkgs' ] != 'None' :
        bkgs = params[ 'bkgs' ]
        params[ 'cutMapper' ] = bkgMap[ params[ 'bkgs' ] ][0]
        params[ 'cutName' ] = bkgMap[ params[ 'bkgs' ] ][0]
        samples = bkgMap[ params [ 'bkgs' ] ][1]
        if not os.path.exists( 'meta/%sBackgrounds/%s/cut' % (grouping, bkgMap[ bkgs ][0]) ) : 
            os.makedirs( 'meta/%sBackgrounds/%s/cut' % (grouping, bkgMap[ bkgs ][0]) )
            os.makedirs( 'meta/%sBackgrounds/%s/iso' % (grouping, bkgMap[ bkgs ][0]) )
            os.makedirs( 'meta/%sBackgrounds/%s/shape' % (grouping, bkgMap[ bkgs ][0]) )
    else :
        if not os.path.exists( '%s%s' % (grouping, params['mid1']) ) : os.makedirs( '%s%s' % (grouping, params['mid1']) )
        if not os.path.exists( '%s%s' % (grouping, params['mid2']) ) : os.makedirs( '%s%s' % (grouping, params['mid2']) )
        if not os.path.exists( '%s%s' % (grouping, params['mid3']) ) : os.makedirs( '%s%s' % (grouping, params['mid3']) )
    return samples

samples = checkBkgs( samples, params, bkgMap )
print samples
print params
analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
analysis1BaselineCuts.drawHistos( grouping, samples, **params )

''' for WJets and QCD shapes '''
#params[ 'bkgs' ] = 'WJets'
#samples = checkBkgs( samples, params, bkgMap )
#analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#params[ 'bkgs' ] = 'QCD'
#samples = checkBkgs( samples, params, bkgMap )
#analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
