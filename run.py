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
    ofile = open('%s%s/config.txt' % (grouping, params['mid3']), "w")
    for sample in samples :
        ofile.write( "%s " % sample )
    ofile.write( "\n" )
    for key in params :
        ofile.write( "%s : %s\n" % (key, params[key]) )
    ofile.close() 
    return samples

''' Set grouping (25ns or Sync) '''
#grouping = '25ns'
grouping = 'Sync'
#grouping = 'dataCards'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
cmsLumi = '2170.0'
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
SamplesSync = ['Sync-HtoTT']
SamplesData = ['data_em', 'data_tt']
Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TTJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'WZ3l1nu', 'ZZ', 'ZZ4l', 'TT', 'TTPow', 'ggHtoTauTau', 'VBFHtoTauTau'] # extra TT samples on stand by
Samples25nsFinal = ['data_em', 'data_tt', 'QCD', 'TTJets', 'DYJets', 'DYJetsLow', 'Tbar-tW', 'T-tW', 'WJets', 'WW', 'WZJets', 'ZZ', 'ggHtoTauTau', 'VBFHtoTauTau'] # Intended good one
SamplesDataCards = ['data_em', 'data_tt', 'DYJets', 'DYJetsLow', 'T-tW', 'T-tchan', 'TT', 'Tbar-tW', 'Tbar-tchan', 'WJets', 'WW1l1nu2q', 'WW2l2nu', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZ3l1nu', 'ZZ2l2nu', 'ZZ2l2q', 'ZZ4l', 'QCD15-20', 'QCD20-30', 'QCD30-80', 'QCD80-170', 'QCD170-250', 'QCD250-Inf'] # Set list for Data Card Sync (less DYJetsLow)
SamplesQCD = ['QCD15-20', 'QCD20-30', 'QCD30-80', 'QCD80-170', 'QCD170-250', 'QCD250-Inf']
#samples = Samples25nsFinal
samples = SamplesSync
#samples = SamplesData
#samples = SamplesDataCards
#samples = SamplesQCD

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'bkgs' : 'None',
    'numCores' : 20,
    'numFilesPerCycle' : 25,
    'channels' : ['em', 'tt'],
    #'channels' : ['em',],
    #'channels' : ['tt',],
    #'cutMapper' : 'signalCutsNoIsoNoSign', #!
    #'cutMapper' : 'signalCutsNoSign', #!
    #'cutName' : 'PostSync', #!
    #'cutMapper' : 'syncCutsDC',
    'cutMapper' : 'syncCutsNtuple',
    'cutName' : 'BaseLine',
    'mid1' : '1dec18',
    'mid2' : '2dec18',
    'mid3' : '3dec18',
    'additionalCut' : '',
    #'additionalCut' : '*(Z_SS==1)',
    #'additionalCut' : '*(Z_SS==0)*(pzetamis>-20)*(nbtag<1)',
    #'additionalCut' : '*(Z_SS==1)*(t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5)*(t1_t2_DR < 2.0)',
    #'additionalCut' : '*(Z_SS==0)*(iso_1 > 3)*(iso_2 >3)*(iso_1 < 10)*(iso_2 < 10)',
    #'additionalCut' : '*( (t1DecayMode < 3 || t1DecayMode == 10) && (t2DecayMode < 3 || t2DecayMode == 10) )',
}

samples = checkBkgs( samples, params, bkgMap )
analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )

#params['mid3'] = '3dec07_syncOS'
#params['additionalCut'] = '*(Z_SS==0)'
##params['additionalCut'] = '*(Z_SS==1)*(t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5)*(t1_t2_Pt > 100)'
##params['additionalCut'] = '*(Z_SS==1)*(t1ByMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5 && t2ByMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5)*(t1_t2_Pt > 100)'
#samples = checkBkgs( samples, params, bkgMap )
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )
#
#params['mid3'] = '3dec04_OS_ZPtGtr100vMed'
##params['additionalCut'] = '*(Z_SS==0)*(t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5)*(t1_t2_Pt > 100)'
#params['additionalCut'] = '*(Z_SS==0)*(t1ByMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5 && t2ByMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5)*(t1_t2_Pt > 100)'
#samples = checkBkgs( samples, params, bkgMap )
#analysis1BaselineCuts.drawHistos( grouping, samples, **params )


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
