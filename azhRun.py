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


''' Uncomment to make pile up vertex templates! '''
''' Not needed with HTT provided pu templates '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate, makeDYJetsPUTemplate
#if not os.path.exists( 'meta/PileUpInfo' ) : 
#    os.makedirs( 'meta/PileUpInfo' )
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 
#makeDYJetsPUTemplate( analysis )


''' Preset samples '''
#azhSamples = ['data_ee', 'data_mm', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'ggZZ4e', 'ggZZ4m', 'ggZZ2m2t', 'TTJ', 'TTZ', 'TTTT', 'WZ3l1nu', 'WminusHtoTauTau', 'WplusHtoTauTau', 'ZHtoTauTau', 'ZZ2l2q', 'ZZ4l']
azhSamples = []
for mass in [220, 240, 300, 320, 350, 400] :
    azhSamples.append('azh%i' % mass)

azhSamples=['azh350',]
samples = azhSamples

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    'debug' : 'true',
    #'debug' : 'false',
    'numCores' : 1,
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
analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)


""" Get samples with map of attributes """
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )
    

runPlots = True
runPlots = False
if runPlots :
    """ Make our folders with directories of histos for each bkg """
    subprocess.call(["python", "makeFinalCutsAndPlots.py", "--folder=%s" % params['mid2']])
    
    qcdYields = {}
    sign = 'NoSign'
    name = 'NoQCD'
    kwargs = { 'qcdMakeDM':sign+'l1ml2_'+name+'ZTT', }
    folder = params['mid2']+'_'+sign+'l1ml2_'+name+'ZTT'
    qcdYield = analysis3Plots.makeLotsOfPlots( analysis, samples, ['eeet',], folder, **kwargs  )
    qcdYields[ sign+name ] = qcdYield
    
    print qcdYields
    looseToTightRatio = qcdYields['SSVTight_'] / qcdYields['SSVTight_Loose']
    qcdFile = open('httQCDYields_%s.txt' % params['mid2'],'w')
    qcdFile.write( str(looseToTightRatio)+"\n" )
    for key in qcdYields :
        qcdFile.write( "%s : %.2f\n" % (key, qcdYields[key]) )
    qcdFile.close()
    
    """ Final plots """
    qcdSF = 1.0
    with open('httQCDYields_%s.txt' % params['mid2']) as qcdFile :
        cnt = 0
        for line in qcdFile :
            qcdSF = float(line)
            break
    print qcdSF
    
    text=False
    #text=True
    kwargs = { 'text':text, 'useQCDMake':True, 'useQCDMakeName':'OSl1ml2_VTight_LooseZTT', 'qcdSF':qcdSF }
    analysis3Plots.makeLotsOfPlots( analysis, samples, ['tt',], '%s_OSl1ml2_VTight_ZTT' % params['mid2'], **kwargs  )
    
    
    


