#!/usr/bin/env python

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
from util.helpers import checkDir
import copy
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
azhSamples = ['ttZ', 'ttZ2', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'TT', 'WWW', 'WWZ', 'WZ3l1nu', 'WZZ', 'WZ', 'ZZ4l', 'ZZZ',] # May 31 samples, no ZZ->all, use ZZ4l

for mass in [110, 120, 125, 130, 140] :
#for mass in [125,] :
    azhSamples.append('ggHtoTauTau%i' % mass)
    azhSamples.append('VBFHtoTauTau%i' % mass)
    azhSamples.append('WMinusHTauTau%i' % mass)
    azhSamples.append('WPlusHTauTau%i' % mass)
    azhSamples.append('ZHTauTau%i' % mass)
for mass in [125,] :
    azhSamples.append('ZHWW%i' % mass)
    azhSamples.append('HZZ%i' % mass)

azhSamples = []
for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
    azhSamples.append('dataEE-%s' % era)
    azhSamples.append('dataMM-%s' % era)
    azhSamples.append('dataSingleE-%s' % era)
    azhSamples.append('dataSingleM-%s' % era)

#azhSamples = []
#for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
#    azhSamples.append('azh%i' % mass)

    
#azhSamples = ['ZHWW125','HZZ125']
#azhSamples = ['dataEE-B']
#azhSamples = ['HZZ125',]
#azhSamples = ['azh300',]
#azhSamples = ['ZHTauTau125',]
#azhSamples = ['ttZ',]

samples = azhSamples

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    #'debug' : 'true',
    'debug' : 'false',
    'numCores' : 12,
    'numFilesPerCycle' : 1,
    'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'], # 8 Normal
    #'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm','eeee','mmmm'], # 8 + eeee + mmmm
    #'channels' : ['eeee','mmmm'],
    #'cutMapper' : 'Skim',
    #'cutMapper' : 'SkimNoTrig',
    'cutMapper' : 'SkimApplyNewTrig',
    'mid1' : '1Feb01svFitted',
    'mid2' : '2Feb01svFitted',
    'mid3' : '3Feb01svFitted',
    'additionalCut' : '',
    'svFitPost' : 'false',
    'svFitPrep' : 'false',
    'doFRMthd' : 'false',
    #'skimmed' : 'false',
    'skimmed' : 'true', # Use at uwlogin
    'skimHdfs' : 'false',
    #'skimHdfs' : 'true', # Use for initial skim

    ### Signal Sync
    ##'channels' : ['eemt','mmmt','emmt',],
    ##'channels' : ['eeet','eett','eeem','mmtt','emmm',],
    #'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm',], # 8
    ##'channels' : ['mmmt','mmtt'],
    ##'channels' : ['eett','mmtt'],
    ##'channels' : ['eeem','eeet',],
    ##'channels' : ['emmt','mmtt','mmmt','emmm'],
    ##'channels' : ['eeet','eeem','mmmt','emmm'],
    ##'channels' : ['mmmt',],
    ##'skimmed' : 'false',
    #'skimmed' : 'true',
    #'skimHdfs' : 'false',
    #'mid1' : '1Jan09NewTrigSync',
    #'mid2' : '2Jan09NewTrigSync',
    #'mid3' : '3Jan09NewTrigSync',
    #'cutMapper' : 'SkimApplyNewTrig',
    ##'cutMapper' : 'SkimNoTrig',
    ##'cutMapper' : 'SkimNoVeto',

    ## RedBkg Sync
    #'channels' : ['eeem',],
    #'mid1' : '1Aug09RBSync',
    #'mid2' : '2Aug09RBSync',
    #'mid3' : '3Aug09RBSync',
    #'skimmed' : 'true', # Use at uwlogin
    #'skimHdfs' : 'false',
    #'cutMapper' : 'Skim',
}

""" Get samples with map of attributes """
setUpDirs( samples, params, analysis ) # Print config file and set up dirs
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )


#analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
#analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)


runPlots = True
doMerge = True
makeFinalPlots = True
doDataCards = True


runPlots = False
doMerge = False
#makeFinalPlots = False
doDataCards = False


doZH = True
#doZH = False
useRedBkg = True
#useRedBkg = False

if useRedBkg :
    params['doRedBkg'] = True
else : params['doRedBkg'] = False

params[ 'debug' ] = 'true'

if runPlots :
    print params
    ''' Draw histos from TTrees '''
    params['additionalCut'] = '*ADD_CHANNEL_SPECIFIC_ISO_CUTS'
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )

samplesY = {}
if useRedBkg :
    for sample in samples.keys() :
        if 'dataSingle' in sample :
            era = sample.split('-')[1]
            samplesY[ 'RedBkgYieldSingleLep-'+era ] = {'xsec' : 0.0, 'group' : 'redBkgYield'}
            samplesY[ 'RedBkgShapeSingleLep-'+era ] = {'xsec' : 0.0, 'group' : 'redBkg'}
            samplesY[ sample ] = copy.deepcopy(samples[ sample ])
        elif 'data' in sample :
            era = sample.split('-')[1]
            samplesY[ 'RedBkgYieldDoubleLep-'+era ] = {'xsec' : 0.0, 'group' : 'redBkgYield'}
            samplesY[ 'RedBkgShapeDoubleLep-'+era ] = {'xsec' : 0.0, 'group' : 'redBkg'}
            samplesY[ sample ] = copy.deepcopy(samples[ sample ])
        elif sample in ['ttZ', 'ttZ2', 'DYJets', 'DYJets1', 'DYJets2',
                'DYJets3', 'DYJets4', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau',
                'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'TT', 'WWW', 'WWZ',
                'WZ3l1nu', 'WZZ', 'WZ', 'ZZ4l', 'ZZZ',] :
            samplesY[ sample+'-NONJET' ] = copy.deepcopy(samples[ sample ])
            #samples[ sample+'-JETFAKE' ] = samples[ sample ]
        else :
            samplesY[ sample ] = copy.deepcopy(samples[ sample ])
    #for sample in samplesY.keys() :
    #    print sample, samplesY[ sample ]
        #print sample
    #redBkgList = ['TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'WWW']
    #for sample in samples.keys() :
    #    if sample in redBkgList :
    #        del samples[ sample ]
else :
    samplesY = samples
    samplesY = copy.deepcopy(samples)

''' merge channels '''
useMerge = True
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
        merge.append( 'LLET' )
        merge.append( 'LLMT' )
        merge.append( 'LLTT' )
        merge.append( 'LLEM' )
    for m in merge :
        params['channels'].append( m )

if doMerge :
    if useMerge :        
        if 'ZEE' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samplesY.keys()], ['eeet','eett','eemt','eeem'], 'ZEE' )
        if 'ZMM' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samplesY.keys()], ['emmt','mmtt','mmmt','emmm'], 'ZMM' )
        if 'ZXX' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samplesY.keys()], ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'], 'ZXX' )
        if 'LLET' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samplesY.keys()], ['eeet','emmt'], 'LLET' )
        if 'LLMT' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samplesY.keys()], ['eemt','mmmt'], 'LLMT' )
        if 'LLTT' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samplesY.keys()], ['eett','mmtt'], 'LLTT' )
        if 'LLEM' in merge :
            mergeChannels( analysis, params['mid3'], [s for s in samplesY.keys()], ['eeem','emmm'], 'LLEM' )

# Remove WZ sample, we have WZ3l1nu
if 'WZ' in samplesY :
    del samplesY[ 'WZ' ]
if 'WZ-NONJET' in samplesY :
    del samplesY[ 'WZ-NONJET' ]

if makeFinalPlots :
    samplesX = copy.deepcopy(samplesY)
    text=False
    #text=True
    #blind = True
    blind = False
    kwargs = { 'text':text, 'blind':blind, 'redBkg':useRedBkg }
    print params

    if useRedBkg : # Delete the yield sample from samples, will be loaded
        # in analysis3Plot.py
        for sample in samplesY :
            if 'RedBkgYield' in sample : del samplesX[ sample ]

    ''' Make the final plots
        and copy to viewing area '''
    analysis3Plots.makeLotsOfPlots( analysis, samplesX, params['channels'], params['mid3'], **kwargs  )
    cpDir = "/afs/cern.ch/user/t/truggles/www/AZH_%s" % params['mid2'].strip('2')
    checkDir( cpDir )
    subprocess.call( ["cp", "-r", "/afs/cern.ch/user/t/truggles/www/azhPlots/", cpDir] )
    
    
if doDataCards :
    #samplesX = copy.deepcopy(samples)
    samplesX = copy.deepcopy(samplesY)

    # Remove RedBkgYield samples from list to run over 
    for sample in  samplesY :
        if 'RedBkgYield' in sample : del samplesX[ sample ]
        if '-NONJET' in sample :
            samplesX[ sample.replace('-NONJET','') ] = samplesX[ sample ]
            del samplesX[ sample ]

    # don't add eeee or mmmm
    #if 'eeee' in params['channels'] : params['channels'].remove( 'eeee' ) 
    #if 'mmmm' in params['channels'] : params['channels'].remove( 'mmmm' ) 

    ROOT.gROOT.Reset()
    from analysisShapesROOT import makeDataCards
    for var in ['m_sv', 'A_Mass', 'Mass'] :
        if var == 'A_Mass' : doZH = False
        if var == 'Mass' : doZH = False
        finalCat = 'inclusive'
        folderDetails = params['mid3']
        kwargs = {
        'doZH' : doZH,
        'category' : finalCat,
        'fitShape' : var,
        'allShapes' : True,
        'redBkg' : useRedBkg, 
        }
        makeDataCards( analysis, samplesX, params['channels'], folderDetails, **kwargs )
    extra = 'mssm'
    subprocess.call( ["mv", "shapes/azh/htt_zh.inputs-mssm-13TeV_4LMass.root", "shapes/azh/htt_zh.inputs-mssm-13TeV_4LMass_new.root"] )
    subprocess.call( ["mv", "shapes/azh/htt_zh.inputs-mssm-13TeV_AMass.root", "shapes/azh/htt_zh.inputs-mssm-13TeV_AMass_new.root"] )
    subprocess.call( ["mv", "shapes/azh/htt_zh.inputs-sm-13TeV_svFitMass.root", "shapes/azh/htt_zh.inputs-sm-13TeV_svFitMass_new.root"] )
    print "moved to : shapes/azh/htt_zh.inputs-mssm-13TeV_AMass_new.root"
    print "moved to : shapes/azh/htt_zh.inputs-mssm-13TeV_4LMass_new.root"
    print "moved to : shapes/azh/htt_zh.inputs-sm-13TeV_svFitMass_new.root"



