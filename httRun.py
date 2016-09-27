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
import copy
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
SamplesData = ['dataTT-B', 'dataTT-C', 'dataTT-D', 'dataTT-E', 'dataTT-F', ]
SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'EWKWPlus', 'EWKWMinus', 'EWKZ2l', 'EWKZ2nu', 'WWW', 'WWZ', 'WZZ', 'ZZZ', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'ZZ2l2q', 'VV', 'dataTT-B', 'dataTT-C', 'dataTT-D', 'dataTT-E', 'dataTT-F',  'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # Adding EWK and tri-boson, sept 25
#SamplesDataCards = ['dataTT',] 
#SamplesDataCards = ['VBFHtoTauTau125',]
#SamplesDataCards = ['DYJets', 'VBFHtoTauTau125', 'ggHtoTauTau125',] # NO ZZ2L2Q FIXME No data E/F
samples = SamplesDataCards

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
    'channels' : ['tt',],
    #'cutMapper' : 'syncCutsDC',
    #'cutMapper' : 'signalCuts',
    #'cutMapper' : 'fakeFactorCutsTT',
    #'cutMapper' : 'syncCutsDCqcdTES',
    'cutMapper' : 'syncCutsDCqcdTES5040',
    'mid1' : '1Sept26a',
    'mid2' : '2Sept26a',
    'mid3' : '3Sept26a',
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
makeFinalPlots = False
text=True
text=False
makeDataCards = True
#makeDataCards = False
#isoVals = ['VTight', 'Tight', 'Medium',]
isoVals = ['Tight',]

cats = ['inclusive', 'vbf', '1jet_low', '1jet_high', '0jet', '1jet', '2jet',]
cats = ['inclusive', 'vbf', '1jet_low', '1jet_high', '0jet',]
cats = ['inclusive', 'vbf_low', 'vbf_high', '1jet_low', '1jet_high', '0jet','1jet','2jet']
cats = ['inclusive', 'vbf_low', 'vbf_high', '1jet_low', '1jet_high', '0jet']
#cats = ['1jet',]
pt = '5040'
#sync = True
sync = False

for isoVal in isoVals :
    samplesX = copy.deepcopy(samples)
    if runPlots :
        skipSSQCDDetails=True
        process = ["python", "makeFinalCutsAndPlots.py", "--folder=%s" % params['mid2'],\
            "--isoVal=%s" % isoVal, "--skimmed=%s" % params['skimmed'],\
            "--skipSSQCDDetails=%r" % skipSSQCDDetails, "--samples"]
        for sample in samplesX.keys() :
            process.append( sample )
        """ Make our folders with directories of histos for each bkg """
        subprocess.call( process )
    
       
    if makeQCDBkg :    
        qcdYields = {}
        for sign in ['SS', 'OS'] :
            for name in [isoVal+'_Loose', isoVal+'_'] :
                for cat in cats :
                    if sign == 'SS' : skipSSQCDDetails = True
                    else : skipSSQCDDetails = False
                    ROOT.gROOT.Reset()
                    kwargs = { 'qcdMakeDM':sign+'l1ml2_'+name+'ZTT'+cat, 
                        'isSSQCD':skipSSQCDDetails,'sync':sync}
                    folder = params['mid2']+'_'+sign+'l1ml2_'+name+'ZTT'+cat
                    qcdYield = analysis3Plots.makeLotsOfPlots( analysis, samplesX, ['tt',], folder, **kwargs  )
                    qcdYields[ sign+name+cat ] = qcdYield
        
        print qcdYields
        qcdFile = open('httQCDYields_%s%s_%s.txt' % (pt, isoVal, params['mid2']),'w')
        for cat in cats :
            qcdSF = qcdYields['SS'+isoVal+'_'+cat] / qcdYields['SS'+isoVal+'_Loose'+cat]
            qcdFile.write( cat+":"+str(qcdSF)+"\n" )
        for key in qcdYields :
            qcdFile.write( "%s : %.2f\n" % (key, qcdYields[key]) )
        qcdFile.close()
        
    
    
    
    if makeFinalPlots :
        from util.helpers import getQCDSF
        for cat in cats :
            ROOT.gROOT.Reset()
            qcdSF = getQCDSF( 'httQCDYields_%s%s_%s.txt' % (pt, isoVal, params['mid2']), cat )
            tDir = cat
            blind = True
            if cat in ['inclusive', '0jet', '1jet'] :
                blind = False
            
            kwargs = { 'text':text, 'useQCDMake':True, 'blind':blind, 
                'useQCDMakeName':'OSl1ml2_'+isoVal+'_LooseZTT'+cat, 'qcdSF':qcdSF,
                'targetDir':'/'+tDir,'sync':sync }
            analysis3Plots.makeLotsOfPlots( analysis, samplesX, ['tt',], 
                params['mid2']+'_OSl1ml2_'+isoVal+'_ZTT'+cat, **kwargs  )
        subprocess.call( ["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlots/", "/afs/cern.ch/user/t/truggles/www/HTT_Sept08/%s" % isoVal] )
        
        
    if makeDataCards :
        ROOT.gROOT.Reset()
        from util.helpers import getQCDSF
        from analysisShapesROOT import makeDataCards
        #for var in ['m_vis', 'm_sv', 'mt_sv', 'mt_tot', 'm_coll',] :
        for var in ['m_sv',] :
        #for var in ['m_vis','m_sv'] :
            for cat in cats :
                qcdSF = getQCDSF( 'httQCDYields_%s%s_%s.txt' % (pt, isoVal, params['mid2']), cat )
                finalCat = cat
                folderDetails = params['mid2']+'_OSl1ml2_'+isoVal+'_ZTT'+cat
                kwargs = {
                'useQCDMakeName' : params['mid2']+'_OSl1ml2_'+isoVal+'_LooseZTT'+cat,
                'qcdSF' : qcdSF,
                'category' : finalCat,
                #'fitShape' : 'm_vis',
                'fitShape' : var,
                'allShapes' : True,
                'sync' : sync,
                }
                makeDataCards( analysis, samplesX, ['tt',], folderDetails, **kwargs )
        subprocess.call( ["mv", "httShapes/htt/htt_tt.inputs-sm-13TeV_svFitMass.root", "httShapes/htt/htt_tt.inputs-sm-13TeV_svFitMass-%s-%s.root" % (pt, isoVal)] )
        #subprocess.call( ["mv", "httShapes/htt/htt_tt.inputs-sm-13TeV_visMass.root", "httShapes/htt/htt_tt.inputs-sm-13TeV_visMass-%s-%s.root" % (pt, isoVal)] )
    
    ''' Remove the .pngs used to build the QCD Bkg
    from the web directory so we can view easitly '''
    cleanPlots = True
    if cleanPlots :
        print "\nTrying to remove pngs used to build QCD Bkg\n"
        subprocess.call(["bash", "util/cleanDirs.sh"])
    










    
