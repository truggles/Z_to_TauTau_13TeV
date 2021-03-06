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
azhSamples = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'TT', 'WWW', 'WWZ', 'WZ3l1nu', 'WZZ', 'WZ', 'ZZ4l', 'ZZZ',] # May 31 samples, no ZZ->all, use ZZ4l

for mass in [110, 120, 125, 130, 140] :
    #azhSamples.append('ggHtoTauTau%i' % mass)
    #azhSamples.append('VBFHtoTauTau%i' % mass)
    #azhSamples.append('WMinusHTauTau%i' % mass)
    #azhSamples.append('WPlusHTauTau%i' % mass)
    azhSamples.append('ZHTauTau%i' % mass)
    #azhSamples.append('ttHTauTau%i' % mass)
for mass in [125,] :
    azhSamples.append('WMinusHTauTau%i' % mass)
    azhSamples.append('WPlusHTauTau%i' % mass)
    azhSamples.append('ZHWW%i' % mass)
    azhSamples.append('HZZ%i' % mass)

for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
    azhSamples.append('azh%i' % mass)

azhSamplesData = []
for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
    azhSamples.append('dataEE-%s' % era)
    azhSamples.append('dataMM-%s' % era)
    azhSamplesData.append('dataEE-%s' % era)
    azhSamplesData.append('dataMM-%s' % era)
    
#azhSamples = ['ZHWW125']
#azhSamples = ['dataEE-B']
#azhSamples = ['ZZ4l',]


iSamples = azhSamples
iSamplesData = azhSamplesData

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    #'debug' : 'true',
    'debug' : 'false',
    'numCores' : 10,
    'numFilesPerCycle' : 1,
    #'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'], # 8 Normal
    'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm','eeee','mmmm'], # 8 + eeee + mmmm
    'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'], # 8 + eeee + mmmm
    #'channels' : ['eeee','mmmm'], # 8 + eeee + mmmm
    #'channels' : ['eett',],
    'cutMapper' : 'Skim',
    'mid1' : '1June13svFitted',
    'mid2' : '2June13svFitted',
    'mid3' : '3June13svFitted',
    'additionalCut' : '',
    'svFitPost' : 'false',
    'svFitPrep' : 'false',
    'doFRMthd' : 'false',
    #'skimmed' : 'false',
    'skimmed' : 'true', # Use at uwlogin
    'skimHdfs' : 'false',
    #'skimHdfs' : 'true', # Use for initial skim
}

setUpDirs( iSamplesData, params, analysis ) # Print config file and set up dirs
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, iSamplesData )


#analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)
    
for LT in [20, 30, 40, 50, 60, 70, 80, 90, 100] :

    """ Get samples with map of attributes """
    setUpDirs( iSamples, params, analysis ) # Print config file and set up dirs
    import analysis3Plots
    from meta.sampleNames import returnSampleDetails
    samples = returnSampleDetails( analysis, iSamples )
    
    
    runPlots = True
    doMerge = True
    makeFinalPlots = True
    doDataCards = True
    
    
    #runPlots = False
    doMerge = False
    #makeFinalPlots = False
    #doDataCards = False
    
    
    doZH = True
    #doZH = False
    useRedBkg = True
    #useRedBkg = False
    
    if useRedBkg :
        params['doRedBkg'] = True
    else : params['doRedBkg'] = False

    redBkgList = ['TT', 'WZ', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'WWW']
    if useRedBkg :
        for sample in samples.keys() :
            if sample in redBkgList :
                del samples[ sample ]

    if runPlots :
        print params
        ''' Draw histos from TTrees '''
        params['additionalCut'] = '*(LT_higgs > %i)*ADD_CHANNEL_SPECIFIC_ISO_CUTS' % LT
        analysis1BaselineCuts.drawHistos( analysis, samples, **params )
    
    if useRedBkg :
        for sample in samples.keys() :
            if 'data' in sample :
                era = sample.split('-')[1]
                samples[ 'RedBkgYield-'+era ] = {'xsec' : 0.0, 'group' : 'redBkgYield'}
                samples[ 'RedBkgShape-'+era ] = {'xsec' : 0.0, 'group' : 'redBkg'}
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
    
    # Remove WZ sample, we have WZ3l1nu
    if 'WZ' in samples :
        del samples[ 'WZ' ]
    
    if makeFinalPlots :
        text=False
        #text=True
        kwargs = { 'text':text, 'blind':False, 'redBkg':useRedBkg }
        print params
    
        if useRedBkg : # Delete the yield sample from samples, will be loaded
            # in analysis3Plot.py
            for sample in samples :
                if 'RedBkgYield' in sample : del samples[ sample ]
    
        ''' Make the final plots
            and copy to viewing area '''
        analysis3Plots.makeLotsOfPlots( analysis, samples, params['channels'], params['mid3'], **kwargs  )
        cpDir = "/afs/cern.ch/user/t/truggles/www/AZH_%s_LT%i" % (params['mid2'].strip('2'), LT)
        checkDir( cpDir )
        subprocess.call( ["cp", "-r", "/afs/cern.ch/user/t/truggles/www/azhPlots/", cpDir] )
        
        
    if doDataCards :
    
        # Remove RedBkgYield samples from list to run over 
        for sample in  samples :
            if 'RedBkgYield' in sample : del samples[ sample ]
    
        # don't add eeee or mmmm
        if 'eeee' in params['channels'] : params['channels'].remove( 'eeee' ) 
        if 'mmmm' in params['channels'] : params['channels'].remove( 'mmmm' ) 
    
        doZH = True
        ROOT.gROOT.Reset()
        from analysisShapesROOT import makeDataCards
        var = 'm_sv'
        finalCat = 'inclusive'
        folderDetails = params['mid3']
        kwargs = {
        'doZH' : doZH,
        'category' : finalCat,
        'fitShape' : var,
        'allShapes' : False,
        'redBkg' : useRedBkg, 
        }
        makeDataCards( analysis, samples, params['channels'], folderDetails, **kwargs )
        extra = 'sm' if doZH else 'mssm'
        subprocess.call( ["mv", "shapes/azh/htt_zh.inputs-%s-13TeV_svFitMass.root" % extra, "shapes/azh/htt_zh.inputs-%s-13TeV_svFitMass_LT%i.root" % (extra, LT)] )
        print "moved to : shapes/azh/htt_zh.inputs-%s-13TeV_svFitMass_LT%i.root" % (extra, LT)
    
    
        doZH = False
        var = 'A_Mass'
        finalCat = 'inclusive'
        folderDetails = params['mid3']
        kwargs = {
        'doZH' : doZH,
        'category' : finalCat,
        'fitShape' : var,
        'allShapes' : False,
        'redBkg' : useRedBkg, 
        }
        makeDataCards( analysis, samples, params['channels'], folderDetails, **kwargs )
        extra = 'sm' if doZH else 'mssm'
        subprocess.call( ["mv", "shapes/azh/htt_zh.inputs-%s-13TeV_AMass.root" % extra, "shapes/azh/htt_zh.inputs-%s-13TeV_AMass_LT%i.root" % (extra, LT)] )
        print "moved to : shapes/azh/htt_zh.inputs-%s-13TeV_AMass_LT%i.root" % (extra, LT)
    
    
    
