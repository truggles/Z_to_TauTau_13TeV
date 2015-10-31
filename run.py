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
grouping = '25ns'
#grouping = 'Sync'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
print "zHome: ",zHome
os.environ['_GROUPING_'] = grouping
os.environ['_ZHOME_'] = zHome
lumiCert = 'Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
puJson = 'pileup_JSON_10-23-2015.txt'

''' Preset samples '''
SamplesSync = ['Sync-HtoTT']
SamplesData = ['data_em', 'data_tt']
Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TTJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'WZ3l1nu', 'ZZ', 'ZZ4l', 'TT', 'TTPow', 'ggHtoTauTau', 'VBFHtoTauTau'] # extra TT samples on stand by
#Samples25nsFinal = ['data_em', 'data_tt', 'TTJets', 'DYJets', 'DYJetsLow', 'Tbar-tW', 'T-tW', 'WJets', 'WW', 'WZJets', 'ZZ', 'ggHtoTauTau', 'VBFHtoTauTau'] # Intended good one
Samples25nsFinalNew = ['data_em', 'data_tt', 'WJets',]
Samples25nsFinalOld = ['TTJets', 'DYJets', 'DYJetsLow', 'Tbar-tW', 'T-tW', 'WW', 'WZJets', 'ZZ', 'ggHtoTauTau', 'VBFHtoTauTau']
#Samples25nsFinal = [ 'DYJets', 'DYJetsLow', 'Tbar-tW', 'T-tW', 'WJets', 'WW', 'WZJets', 'ZZ', 'ggHtoTauTau', 'VBFHtoTauTau'] # Intended good one
#samples = ['data_em', 'data_tt', 'Tbar-tW', 'T-tW',]
#samples = ['DYJets',]# 'Tbar-tW', 'T-tW',]
#samples = ['ggHtoTauTau', 'VBFHtoTauTau']
#samples = ['WJets',]
samples = Samples25nsFinalNew
#samples = SamplesSync
#samples = SamplesData
#samples = ['DYJetsLow', 'data_em']
#samples = ['Tbar-tW',]
#samples = ['WW',]
#samples = ['WJets',]
#samples = ['TTJets',]

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'bkgs' : 'None',
    'numCores' : 30,
    'numFilesPerCycle' : 50,
    #'cutMapper' : 'quickCutMapSingleCut',
    #'cutName' : 'PostSync',
    #'cutMapper' : 'quickCutMapSync',
    #'cutName' : 'BaseLine',
    #'cutMapper' : 'testLooserTriggers',
    #'cutMapper' : 'QCDYieldOS',
    #'cutMapper' : 'QCDYieldOSTrigLoose',
    #'cutName' : 'QCDYield',
    #'cutMapper' : 'qcdShapeScale', #!
    #'cutName' : 'PostSync', #!
    'mid1' : '1oct29baseline',
    'mid2' : '2oct29baseline',
    'mid3' : '3oct30baseline',
    #'mid3' : '3oct21LooseE17M8',
    #'mid1' : '1oct21Sync',
    #'mid2' : '2oct21Sync',
    #'mid3' : '3oct21Synce12m23',
    #'mid1' : '1oct29QCDScale',
    #'mid2' : '2oct29QCDScale',
    #'mid3' : '3oct29QCDScale_OS',
    #'mid1' : '1phys15run34',
    #'mid2' : '2phys15run34',
    #'mid3' : '3phys15run34',
    #'additionalCut' : '',
    #'additionalCut' : '*(t1_t2_SS==0)*(iso_1 > 5)*(iso_2 > 5)',
    'additionalCut' : '*( (t1DecayMode < 3 || t1DecayMode == 10) && (t2DecayMode < 3 || t2DecayMode == 10) )',
    #'additionalCut' : '*(nbtag<1)*(mt_2<80)',
    #'additionalCut' : '*(pt_2<20)',
    #'additionalCut' : '*(singleE23SingleMu8Pass > 0 && eMatchesMu8Ele23Path == 1 && mMatchesMu8Ele23Path == 1)',
    #'additionalCut' : '*(singleMu23SingleE12Pass > 0 && eMatchesMu23Ele12Path == 1 && mMatchesMu23Ele12Path == 1)'
    #'additionalCut' : '*(singleE17SingleMu8Pass > 0 && eMatchesMu8Ele17Path == 1 && mMatchesMu8Ele17Path == 1)',
    #'additionalCut' : '*(singleMu17SingleE12Pass > 0 && eMatchesMu17Ele12Path == 1 && mMatchesMu17Ele12Path == 1)'
}


''' Uncomment to make out starting JSON file of meta data! '''
#from meta.makeMeta import makeMetaJSON
#os.chdir('meta')
#makeMetaJSON( grouping )
#os.chdir('..')


''' Uncomment to make pile up vertex templates! '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 



samples = checkBkgs( samples, params, bkgMap )
#analysis1BaselineCuts.doInitialCutsAndOrder(grouping, samples, **params)
analysis1BaselineCuts.drawHistos( grouping, samples, **params )

samples = Samples25nsFinalOld
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
