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
from util.helpers import setUpDirs 
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
#azhSamples = ['data_ee', 'data_mm', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'ggZZ4e', 'ggZZ4m', 'ggZZ2m2t', 'TTJ', 'TTZ', 'TTTT', 'WZ3l1nu', 'WminusHtoTauTau', 'WplusHtoTauTau', 'ZHtoTauTau', 'ZZ2l2q', 'ZZ4l']
azhSamples = ['data_ee', 'data_mm', 'WZ3l1nu', 'ZZ4l']
#azhSamples = []
for mass in [220, 240, 300, 320, 350, 400] :
    azhSamples.append('azh%i' % mass)

#azhSamples=['azh350',]
samples = azhSamples

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    #'debug' : 'true',
    'debug' : 'false',
    'numCores' : 25,
    'numFilesPerCycle' : 20,
    'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'],
    #'channels' : ['eeet',],
    'cutMapper' : 'goodZ',
    'mid1' : '1July20a',
    'mid2' : '2July20a',
    'mid3' : '3July20a',
    'additionalCut' : '',
    #'svFitPost' : 'true',
    'svFitPost' : 'false',
    #'svFitPrep' : 'true',
    'svFitPrep' : 'false',
    'doFRMthd' : 'false',
}

samples = setUpDirs( samples, params, analysis )
#analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
#analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)


""" Get samples with map of attributes """
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )
    

runPlots = True
#runPlots = False
if runPlots :
    analysis1BaselineCuts.drawHistos( analysis, samples, **params )
    text=False
    #text=True
    kwargs = { 'text':text, }
    analysis3Plots.makeLotsOfPlots( analysis, samples, ['eeet',], params['mid3'], **kwargs  )
    
    
    

