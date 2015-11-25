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

''' Set grouping (25ns or Sync) '''
#grouping = '25ns'
#grouping = 'Sync'
grouping = 'dataCards'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
print "zHome: ",zHome
os.environ['_GROUPING_'] = grouping
os.environ['_ZHOME_'] = zHome
lumiCert = 'Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt' # 2.11/fb - all of 2015 25ns golden
puJson = 'pileup_latest.txt' # Symlinked to newest pile_JSON_xxxxx.txt


''' Uncomment to make out starting JSON file of meta data! '''
#from meta.makeMeta import makeMetaJSON
#os.chdir('meta')
#makeMetaJSON( grouping )
#os.chdir('..')


''' Uncomment to make pile up vertex templates! '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate
#if not os.path.exists( 'meta/PileUpInfo' ) : 
#    os.makedirs( 'meta/PileUpInfo' )
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 


''' Preset samples '''
SamplesSync = ['Sync-HtoTT']
SamplesData = ['data_em', 'data_tt']
Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TTJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'WZ3l1nu', 'ZZ', 'ZZ4l', 'TT', 'TTPow', 'ggHtoTauTau', 'VBFHtoTauTau'] # extra TT samples on stand by
Samples25nsFinal = ['data_em', 'data_tt', 'QCD', 'TTJets', 'DYJets', 'DYJetsLow', 'Tbar-tW', 'T-tW', 'WJets', 'WW', 'WZJets', 'ZZ', 'ggHtoTauTau', 'VBFHtoTauTau'] # Intended good one
SamplesDataCards = ['data_em', 'data_tt', 'DYJets', 'DYJetsLow', 'T-tW', 'T-tchan', 'TT', 'Tbar-tW', 'Tbar-tchan', 'WJets', 'WW1l1nu2q', 'WW2l2nu', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZ3l1nu', 'ZZ2l2nu', 'ZZ2l2q', 'ZZ4l'] # Set list for Data Card Sync (less DYJetsLow)
#samples = Samples25nsFinal
#samples = SamplesSync
#samples = SamplesData
samples = SamplesDataCards

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'bkgs' : 'None',
    'numCores' : 20,
    'numFilesPerCycle' : 25,
    'cutMapper' : 'signalCutsX', #!
    'cutName' : 'PostSync', #!
    #'cutMapper' : 'tmp',
    #'cutMapper' : 'syncCuts',
    #'cutName' : 'BaseLine',
    #'cutMapper' : 'QCDYieldSS',
    #'cutName' : 'QCDYield',
    #'cutMapper' : 'qcdShapeScale', #!
    #'cutName' : 'PostSync', #!
    #'mid1' : '1nov24isoOrderReweightMTfixNoSignNoIso',
    #'mid2' : '2nov24isoOrderReweightMTfixNoSignNoIso',
    'mid1' : '1nov22noSignNoIso',
    'mid2' : '2nov22noSignNoIso',
    'mid3' : '3nov24OS3to10',
    #'additionalCut' : '',
    #'additionalCut' : '*(Z_SS==0)',
    'additionalCut' : '*(Z_SS==0)*(iso_1 > 3)*(iso_2 >3)*(iso_1 < 10)*(iso_2 < 10)',
    #'additionalCut' : '*( (t1DecayMode < 3 || t1DecayMode == 10) && (t2DecayMode < 3 || t2DecayMode == 10) )',
}

samples = checkBkgs( samples, params, bkgMap )
#analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
analysis1BaselineCuts.drawHistos( grouping, samples, **params )



''' for WJets and QCD shapes 
uncomment and run each time you change cuts '''
#params[ 'bkgs' ] = 'WJets'
#samples = checkBkgs( samples, params, bkgMap )
##analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#params[ 'bkgs' ] = 'QCDSync'
#samples = checkBkgs( samples, params, bkgMap )
#analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#params[ 'bkgs' ] = 'QCDLoose'
#samples = checkBkgs( samples, params, bkgMap )
#analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
