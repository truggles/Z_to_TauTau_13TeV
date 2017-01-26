'''#################################################################
##     Analysis run file for A -> Z + sm-Higgs -> ll TauTau       ##
##     Tyler Ruggles                                              ##
##     June 27, 2016                                              ##
#################################################################'''


import os
from time import gmtime, strftime
import ROOT
from ROOT import gROOT
import analysis1BaselineCuts
from util.helpers import setUpDirs, mergeChannels
import subprocess
ROOT.gROOT.Reset()



''' Set analysis (25ns or Sync) '''
analysis = 'azh'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
print "zHome: ",zHome


''' Uncomment to make out starting JSON file of meta data! '''
from meta.makeMeta import makeMetaJSON
os.chdir('meta')
### General samples.json file from /data/truggles files
#makeMetaJSON( analysis, 'eeet' )
### samples.json for post /hdfs skim -> uwlogin samples
#makeMetaJSON( analysis, 'eeet', skimmed=True )
os.chdir('..')


''' Preset samples '''
azhSamples = ['dataEE-B', 'dataEE-C', 'dataEE-D', 'dataEE-E', 'dataEE-F', 'dataMM-B', 'dataMM-C', 'dataMM-D', 'dataMM-E', 'dataMM-F', 'TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'WWW', 'ZZ4l', 'ZZ4lAMCNLO', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau',]
azhSamples = ['dataEE-B', 'dataEE-C', 'dataEE-D', 'dataEE-E', 'dataEE-F', 'dataEE-G', 'dataEE-H', 'dataMM-B', 'dataMM-C', 'dataMM-D', 'dataMM-E', 'dataMM-F', 'dataMM-G', 'dataMM-H', 'TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'ZZ4l', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'WWW', 'WWZ', 'WZ', 'WZZ', 'ZZ', 'ZZZ'] # Jan 14 samples

for mass in [120, 125, 130] :
    #azhSamples.append('ggHtoTauTau%i' % mass)
    #azhSamples.append('VBFHtoTauTau%i' % mass)
    #azhSamples.append('WMinusHTauTau%i' % mass)
    #azhSamples.append('WPlusHTauTau%i' % mass)
    azhSamples.append('ZHTauTau%i' % mass)
    #azhSamples.append('ttHTauTau%i' % mass)
for mass in [125,] :
    azhSamples.append('WMinusHTauTau%i' % mass)
    azhSamples.append('WPlusHTauTau%i' % mass)

#azhSamples = []
for mass in [220, 240, 260, 280, 300, 320, 350, 400] :
    azhSamples.append('azh%i' % mass)

#azhSamples = ['dataEE-B', 'dataEE-C', 'dataEE-D', 'dataEE-E', 'dataEE-F', 'dataMM-B', 'dataMM-C', 'dataMM-D', 'dataMM-E', 'dataMM-F',]
#azhSamples=['ZZ4lAMCNLO',]
#azhSamples=['dataEE-D',]
#azhSamples=['azh300',]
azhSamples=['ZHTauTau125',]
#azhSamples=['ggZZ4m','ggZZ2m2tau']
samples = azhSamples

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    #'debug' : 'true',
    'debug' : 'false',
    'numCores' : 16,
    'numFilesPerCycle' : 1,
    #'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'], # 8 Normal
    'channels' : ['eemm','eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm','eeee','mmmm'], # 8 + eeee + mmmm + eemm
    #'channels' : ['eeet','eett','eemt','eeem'],
    #'channels' : ['eeee','mmmm','eemm'],
    'channels' : ['eemt',],
    #'channels' : ['emmt',],
    #'channels' : ['eeee','eeet','eett','eemt'],
    #'cutMapper' : 'HSS',
    'cutMapper' : 'Skim',
    'cutMapper' : 'Sync2',
    #'mid1' : '1Jan12redBkgOS',
    #'mid2' : '2Jan12redBkgOSnewFR',
    #'mid3' : '3Jan12redBkgOSnewFR',
    'mid1' : '1Jan20sync',
    'mid2' : '2Jan20sync',
    'mid3' : '3Jan20sync',
    'additionalCut' : '',
    'svFitPost' : 'false',
    'svFitPrep' : 'false',
    'doFRMthd' : 'false',
    'skimmed' : 'false',
    #'skimmed' : 'true',
    'skimHdfs' : 'false',
    #'skimHdfs' : 'true',
}

""" Get samples with map of attributes """
setUpDirs( samples, params, analysis ) # Print config file and set up dirs
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )


analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)


runPlots = True
doMerge = True
makeFinalPlots = True
doDataCards = True


doMerge = False
runPlots = False
makeFinalPlots = False
doDataCards = False


useRedBkg = True
#useRedBkg = False

if runPlots :
    from util.helpers import checkDir
    print params
    ''' Draw histos from TTrees '''
    params['additionalCut'] = '*ADD_CHANNEL_SPECIFIC_ISO_CUTS'
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )

if useRedBkg :
    for sample in samples.keys() :
        if 'data' in sample :
            era = sample.split('-')[1]
            samples[ 'RedBkgYield-'+era ] = {'xsec' : 0.0, 'group' : 'redBkgYield'}
            samples[ 'RedBkgShape-'+era ] = {'xsec' : 0.0, 'group' : 'redBkg'}
    redBkgList = ['TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu',]
    for sample in samples.keys() :
        if sample in redBkgList :
            del samples[ sample ]

''' merge channels '''
if doMerge :
    useMerge = False
    merge = []
    if len( params['channels'] ) > 3 :
        if 'eeet' in params['channels'] and 'eemt' in params['channels'] and 'eett' in params['channels'] and 'eeem' in params['channels'] :
            useMerge = True
            merge.append( 'ZEE' )
        if 'emmt' in params['channels'] and 'mmmt' in params['channels'] and 'mmtt' in params['channels'] and 'emmm' in params['channels'] :
            useMerge = True
            merge.append( 'ZMM' )
        ZXX = True
        for channel in ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'] :
            if channel not in params['channels'] : ZXX = False
        if ZXX == True :
            merge.append( 'ZXX' )
    if useMerge :
        
        if 'ZEE' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samples.keys()], ['eeet','eett','eemt','eeem'], 'ZEE' )
        if 'ZMM' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samples.keys()], ['emmt','mmtt','mmmt','emmm'], 'ZMM' )
        if 'ZXX' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samples.keys()], ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'], 'ZXX' )
        for m in merge :
            params['channels'].append( m )

if makeFinalPlots :
    #text=False
    text=True
    kwargs = { 'text':text, 'blind':False, 'redBkg':useRedBkg }
    print params
    if useRedBkg : # Delete the yield sample from samples, will be loaded
        # in analysis3Plot.py
        for sample in samples :
            if 'RedBkgYield' in sample : del samples[ sample ]

    ''' Make the final plots
        and copy to viewing area '''
    analysis3Plots.makeLotsOfPlots( analysis, samples, params['channels'], params['mid3'], **kwargs  )
    cpDir = "/afs/cern.ch/user/t/truggles/www/AZH_%s" % params['mid2'].strip('2')
    checkDir( cpDir )
    subprocess.call( ["cp", "-r", "/afs/cern.ch/user/t/truggles/www/azhPlots/", cpDir] )
    
    
if doDataCards :
    ROOT.gROOT.Reset()
    from analysisShapesROOT import makeDataCards
    var = 'Mass'
    finalCat = 'inclusive'
    folderDetails = params['mid3']
    kwargs = {
    'category' : finalCat,
    'fitShape' : var,
    'allShapes' : False,
    'redBkg' : useRedBkg, 
    }
    makeDataCards( analysis, samples, params['channels'], folderDetails, **kwargs )
    subprocess.call( ["mv", "azhShapes/azh/htt_zh.inputs-sm-13TeV_4LMass.root", "azhShapes/azh/htt_zh.inputs-sm-13TeV_4LMass_new.root"] )



