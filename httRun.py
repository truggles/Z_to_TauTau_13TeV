'''#################################################################
##     Analysis run file for Z or Higgs -> TauTau                 ##
##     Tyler Ruggles                                              ##
##     Oct 11, 2015                                               ##
#################################################################'''


import os
from time import gmtime, strftime
import ROOT
from ROOT import gPad, gROOT
import analysis1BaselineCuts
from util.helpers import setUpDirs 
import subprocess
ROOT.gROOT.Reset()



''' Set analysis (25ns or Sync) '''
analysis = 'htt'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
print "zHome: ",zHome
os.environ['_GROUPING_'] = analysis
os.environ['_ZHOME_'] = zHome


''' Uncomment to make out starting JSON file of meta data! '''
#from meta.makeMeta import makeMetaJSON
#os.chdir('meta')
#makeMetaJSON( analysis )
#os.chdir('..')


''' Uncomment to make pile up vertex templates! '''
''' Not needed with HTT provided pu templates '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate, makeDYJetsPUTemplate
#if not os.path.exists( 'meta/PileUpInfo' ) : 
#    os.makedirs( 'meta/PileUpInfo' )
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 
#makeDYJetsPUTemplate( analysis )


''' Preset samples '''
SamplesData = ['data_tt',]
#SamplesDataCards = ['DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh', 'DYJetsLow', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'ZZ2l2q', 'VV', 'data_tt', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # As of April23, removed DYJets LO small sample
SamplesDataCards = ['data_tt', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'ZZ2l2q', 'VV'] # As of June28
#SamplesDataCards = ['DYJetsHigh', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'ZZ2l2q', 'VV', 'data_tt', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # As of April23, removed DYJets LO small sample


#SamplesDataCards = ['data_tt','data_em']
#SamplesDataCards = ['DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh'] # LO DYJets
#SamplesDataCards = ['DYJets4',]
samples = SamplesDataCards

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    #'debug' : 'true',
    'debug' : 'false',
    'numCores' : 15,
    'numFilesPerCycle' : 10,
    'channels' : ['tt',],
    #'cutMapper' : 'syncCutsDC',
    #'cutMapper' : 'syncCutsDCqcd',
    'cutMapper' : 'syncCutsNtupleBuilding',
    #'cutMapper' : 'signalCuts',
    #'cutMapper' : 'fakeFactorCutsTT',
    'mid1' : '1June26c',
    'mid2' : '2June29a',
    'mid3' : '3June29a',
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
#analysis1BaselineCuts.drawHistos( analysis, samples, **params )

runPlots = True
if runPlots :
    """ Make our folders with directories of histos for each bkg """
    subprocess.call(["python", "makeFinalCutsAndPlots.py", "--folder=%s" % params['mid2']])
    
    
    """ Get samples with map of attributes """
    import analysis3Plots
    from meta.sampleNames import returnSampleDetails
    samples = returnSampleDetails( analysis, samples )
    
    qcdYields = {}
    for sign in ['SS', 'OS'] :
        for name in ['VTight_Loose', 'VTight_'] :
            kwargs = { 'qcdMakeDM':sign+'l1ml2_'+name+'ZTT', }
            folder = params['mid2']+'_'+sign+'l1ml2_'+name+'ZTT'
            qcdYield = analysis3Plots.makeLotsOfPlots( analysis, samples, ['tt',], folder, **kwargs  )
            qcdYields[ sign+name ] = qcdYield
    
    print qcdYields
    looseToTightRatio = qcdYields['SSVTight_'] / qcdYields['SSVTight_Loose']
    qcdFile = open('httQCDYields.txt','w')
    qcdFile.write( str(looseToTightRatio)+"\n" )
    for key in qcdYields :
        qcdFile.write( "%s : %.2f" % (key, qcdYields[key]) )
    qcdFile.close()
    
    """ Final plots """
    qcdSF = 1.0
    with open('httQCDYields.txt') as qcdFile :
        cnt = 0
        for line in qcdFile :
            qcdSF = float(line)
            break
    print qcdSF
    
    kwargs = { 'text':True, 'useQCDMake':True, 'useQCDMakeName':'OSl1ml2_VTight_LooseZTT', 'qcdSF':qcdSF }
    analysis3Plots.makeLotsOfPlots( analysis, samples, ['tt',], '%s_OSl1ml2_VTight_ZTT' % params['mid2'], **kwargs  )
    
    
    
