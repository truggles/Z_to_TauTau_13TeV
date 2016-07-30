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
#makeMetaJSON( analysis, 'eeet' )
os.chdir('..')


''' Preset samples '''
azhSamples = ['dataEE', 'dataMM', 'WZ3l1nu', 'ZZ4l', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'TT']
for mass in [220, 240, 300, 320, 350, 400] :
    azhSamples.append('azh%i' % mass)

#azhSamples=['azh350',]
#azhSamples=['dataEE', 'dataMM']
samples = azhSamples

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    #'debug' : 'true',
    'debug' : 'false',
    'numCores' : 15,
    'numFilesPerCycle' : 20,
    'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'],
    #'channels' : ['eeet','eett','eemt','eeem'],
    #'channels' : ['eett',],
    'cutMapper' : 'goodZ',
    'mid1' : '1July29a',
    'mid2' : '2July29a',
    'mid3' : '3July29a',
    'additionalCut' : '',
    #'svFitPost' : 'true',
    'svFitPost' : 'false',
    #'svFitPrep' : 'true',
    'svFitPrep' : 'false',
    'doFRMthd' : 'false',
}

""" Get samples with map of attributes """
setUpDirs( samples, params, analysis ) # Print config file and set up dirs
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )


#analysis1BaselineCuts.doInitialCuts(analysis, samples.keys(), **params)
#analysis1BaselineCuts.doInitialOrder(analysis, samples.keys(), **params)


runPlots = True
#runPlots = False
if runPlots :
    print params
    ''' Draw histos from TTrees '''
    #analysis1BaselineCuts.drawHistos( analysis, samples, **params )

    ''' merge channels '''
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
            mergeChannels( analysis, params['mid3'], samples.keys(), ['eeet','eett','eemt','eeem'], 'ZEE' )
        if 'ZMM' in merge :
            mergeChannels( analysis, params['mid3'], samples.keys(), ['emmt','mmtt','mmmt','emmm'], 'ZMM' )
        if 'ZXX' in merge :
            mergeChannels( analysis, params['mid3'], samples.keys(), ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'], 'ZXX' )
        for m in merge :
            params['channels'].append( m )

    #text=False
    text=True
    kwargs = { 'text':text, }
    print params

    ''' Make the final plots '''
    analysis3Plots.makeLotsOfPlots( analysis, samples, params['channels'], params['mid3'], **kwargs  )
    
    
    

