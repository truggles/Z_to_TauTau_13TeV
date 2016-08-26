'''#################################################################
##     Analysis run file for Z or Higgs -> TauTau                 ##
##     Tyler Ruggles                                              ##
##     Oct 11, 2015                                               ##
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
analysis = 'htt'
zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
print "zHome: ",zHome


''' Uncomment to make out starting JSON file of meta data! '''
from meta.makeMeta import makeMetaJSON
os.chdir('meta')
### General samples.json file from /data/truggles files
#makeMetaJSON( analysis, channel='tt' )
### samples.json for post /hdfs skim -> uwlogin samples
#makeMetaJSON( analysis, channel='tt', skimmed=True )
os.chdir('..')


''' Uncomment to make pile up vertex templates! '''
''' Not needed with HTT provided pu templates '''
#from util.pileUpVertexCorrections import makeDataPUTemplate, makeMCPUTemplate, makeDYJetsPUTemplate
#makeMCPUTemplate()
#makeDataPUTemplate( lumiCert, puJson ) 
#makeDYJetsPUTemplate( analysis )


''' Preset samples '''
SamplesData = ['dataTT',]
#SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'ZZ2l2q', 'VV', 'dataTT', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # Aug 24 samples from /hdfs @cecile
#SamplesDataCards = ['DYJets', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'ZZ2l2q', 'VV', 'dataTT', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # Aug 24 samples from /hdfs @cecile
SamplesDataCards = ['DYJets', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'ZZ2l2q', 'VV', 'dataTT', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # Aug 24 samples from /hdfs @cecile


#SamplesDataCards = ['dataTT','dataEM','DYJets']
#SamplesDataCards = ['DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh'] # LO DYJets
#SamplesDataCards = ['DYJets4',]
#SamplesDataCards = ['VBFHtoTauTau125',]
samples = SamplesDataCards

''' These parameters are fed into the 2 main function calls.
They adjust the cuts you make, number of cores you run in
multiprocessing, and the 'mid' params define the save location
of your output files.  additionCut can be specified to further
cut on any 'preselection' made in the initial stages '''
params = {
    #'debug' : 'true',
    'debug' : 'false',
    'numCores' : 8,
    'numFilesPerCycle' : 1,
    'channels' : ['tt',],
    #'cutMapper' : 'syncCutsDC',
    'cutMapper' : 'syncCutsDCqcdTES',
    #'cutMapper' : 'signalCuts',
    #'cutMapper' : 'fakeFactorCutsTT',
    'mid1' : '1Aug25x5pt45b',
    'mid2' : '2Aug25x5pt45b',
    'mid3' : '3Aug25x5pt45b',
    'additionalCut' : '',
    #'svFitPost' : 'true',
    'svFitPost' : 'false',
    #'svFitPrep' : 'true',
    'svFitPrep' : 'false',
    'doFRMthd' : 'false',
    'skimHdfs' : 'false',
    #'skimHdfs' : 'true',
    #'skimmed' : 'false',
    'skimmed' : 'true',
}
""" Get samples with map of attributes """
setUpDirs( samples, params, analysis ) # Print config file and set up dirs
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )


#analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
#analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)


""" Get samples with map of attributes """
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )
    

runPlots = True
runPlots = False
makeQCDBkg = True
makeQCDBkg = False
makeFinalPlots = True
#makeFinalPlots = False
text=True
text=False
makeDataCards = True
makeDataCards = False

cats = ['', '0Jet', '1Jet', 'VBF',]

if runPlots :
    process = ["python", "makeFinalCutsAndPlots.py", "--folder=%s" % params['mid2'], "--skimmed=%s" % params['skimmed'], "--samples"]
    for sample in samples.keys() :
        process.append( sample )
    """ Make our folders with directories of histos for each bkg """
    subprocess.call( process )

   
if makeQCDBkg :    
    qcdYields = {}
    for sign in ['SS', 'OS'] :
        #XXX for name in ['VTight_Loose', 'VTight_'] :
        for name in ['Tight_Loose', 'Tight_'] :
            for cat in cats :
                ROOT.gROOT.Reset()
                kwargs = { 'qcdMakeDM':sign+'l1ml2_'+name+'ZTT'+cat, }
                folder = params['mid2']+'_'+sign+'l1ml2_'+name+'ZTT'+cat
                qcdYield = analysis3Plots.makeLotsOfPlots( analysis, samples, ['tt',], folder, **kwargs  )
                qcdYields[ sign+name+cat ] = qcdYield
    
    print qcdYields
    qcdFile = open('httQCDYields_%s.txt' % params['mid2'],'w')
    for cat in cats :
        qcdSF = qcdYields['SSTight_'+cat] / qcdYields['SSTight_Loose'+cat]
        qcdFile.write( cat+":"+str(qcdSF)+"\n" )
    for key in qcdYields :
        qcdFile.write( "%s : %.2f\n" % (key, qcdYields[key]) )
    qcdFile.close()
    



if makeFinalPlots :
    from util.helpers import getQCDSF
    for cat in cats :
        ROOT.gROOT.Reset()
        qcdSF = getQCDSF( 'httQCDYields_%s.txt' % params['mid2'], cat )
        tDir = cat
        if cat == '' : tDir = 'inclusive'
        kwargs = { 'text':text, 'useQCDMake':True, 
            'useQCDMakeName':'OSl1ml2_Tight_LooseZTT'+cat, 'qcdSF':qcdSF,
            'targetDir':'/'+tDir }
        analysis3Plots.makeLotsOfPlots( analysis, samples, ['tt',], 
            params['mid2']+'_OSl1ml2_Tight_ZTT'+cat, **kwargs  )
    
    
if makeDataCards :
    ROOT.gROOT.Reset()
    from util.helpers import getQCDSF
    from analysisShapesROOT import makeDataCards
    for cat in cats :
        qcdSF = getQCDSF( 'httQCDYields_%s.txt' % params['mid2'], cat )
        fitShape = cat
        if cat == '' : fitShape = 'inclusive'
        folderDetails = params['mid2']+'_OSl1ml2_Tight_ZTT'+cat
        kwargs = {
        'useQCDMakeName' : params['mid2']+'_OSl1ml2_Tight_LooseZTT'+cat,
        'qcdSF' : qcdSF,
        'category' : fitShape,
        'fitShape' : 'm_vis',
        'ES' : True,
        }
        makeDataCards( analysis, samples, ['tt',], folderDetails, **kwargs )











    
