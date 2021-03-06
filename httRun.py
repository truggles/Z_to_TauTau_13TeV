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
from smart_getenv import getenv
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
SamplesData = ['dataTT-B', 'dataTT-C', 'dataTT-D', 'dataTT-E', 'dataTT-F', 'dataTT-G', 'dataTT-H']
SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJets1Low', 'DYJets2Low', 'EWKWMinus', 'EWKWPlus', 'EWKZ2l', 'EWKZ2nu', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'VV', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WWW', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZ3l1nu', 'ZZ2l2q', 'ZZ4l'] # Feb17 for Moriond17 

for mass in [110, 120, 125, 130, 140] :
    SamplesDataCards.append('ggHtoTauTau%i' % mass)
    SamplesDataCards.append('VBFHtoTauTau%i' % mass)
    SamplesDataCards.append('WMinusHTauTau%i' % mass)
    SamplesDataCards.append('WPlusHTauTau%i' % mass)
    SamplesDataCards.append('ZHTauTau%i' % mass)
SamplesDataCards.append('HtoWW2l2nu125')
SamplesDataCards.append('ttHTauTau125')
SamplesDataCards.append('VBFHtoWW2l2nu125')

    
for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
    SamplesDataCards.append('dataTT-%s' % era)
    
#SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'EWKZ2l', 'EWKZ2nu']
#SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4']
#SamplesDataCards = [ 'EWKZ2l', 'EWKZ2nu']
#SamplesDataCards = ['DYJets',] 
#SamplesDataCards = ['dataTT-C',] 
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
    'numCores' : 6,
    'numFilesPerCycle' : 1,
    'channels' : ['tt',],
    #'cutMapper' : 'syncCutsDC',
    #'cutMapper' : 'signalCuts',
    #'cutMapper' : 'fakeFactorCutsTT',
    #'cutMapper' : 'syncCutsDCqcdTES',
    #'cutMapper' : 'syncCutsDCqcdTES5040VVLoose', # For VVL study
    #'cutMapper' : 'syncCutsDCqcdTES5040', # For normal running
    'cutMapper' : 'syncCutsDCqcdTES5040VL', # For QCD Mthd Check
    #'cutMapper' : 'syncCutsDCqcdTES5040VL_HdfsSkim', # For svFit Skim keeping VLoose for new definition and both triggers
    'mid1' : '1March20withMetUnc',
    'mid2' : '2March23withMetUnc',
    'mid3' : '3March23withMetUnc',
    'mid2' : '2March28withMetUnc',
    'mid3' : '3March28withMetUnc',
    'additionalCut' : '',
    #'svFitPost' : 'true',
    'svFitPost' : 'false',
    #'svFitPrep' : 'true',
    'svFitPrep' : 'false',
    'doFRMthd' : 'false',
    'skimHdfs' : 'false',
    #'skimHdfs' : 'true', # This means "do the hdfs skim"
    #'skimmed' : 'false',
    'skimmed' : 'true',
}
""" Get samples with map of attributes """
setUpDirs( samples, params, analysis ) # Print config file and set up dirs
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )


#analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)


""" Get samples with map of attributes """
import analysis3Plots
from meta.sampleNames import returnSampleDetails
samples = returnSampleDetails( analysis, samples )
    

runPlots = True
#runPlots = False
makeQCDBkg = True
makeQCDBkg = False
makeFinalPlots = True
makeFinalPlots = False # Use this with FF
text=True
text=False
makeDataCards = True
#makeDataCards = False

cats = ['inclusive', 'vbf_low', 'vbf_high', '1jet_low', '1jet_high', '0jet','1jet','2jet']
cats = ['inclusive', '0jet2D', 'boosted','vbf',]
#cats = ['0jet2D', 'boosted','vbf',]
#cats = ['boosted',]
#cats = ['inclusive',]
pt = '5040'
#sync = True
sync = False
#cleanPlots = False
cleanPlots = True
#isoVals = ['Tight', 'Medium', 'Loose',]
#isoVals = ['Tight', 'Loose',]
isoVals = ['Tight',]
doFF = getenv('doFF', type=bool)

# Make CR plots for AN
#plotAntiIso = True
plotAntiIso = False
higgsPt = 'pt_sv'
#higgsPt = 'Higgs_PtCor'


toRemove = ['DYJets1Low', 'DYJets2Low', 'VBFHtoWW2l2nu125' ,'HtoWW2l2nu125',]
for remove in toRemove :
    if remove in samples.keys() : del samples[remove]

for isoVal in isoVals :
    if isoVal == 'Tight' : lIso = 'Loose'
    #if isoVal == 'Medium' : lIso = 'Loose'
    #if isoVal == 'Loose' : lIso = 'VLoose'
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
    
    if doFF :
        for sample in samples.keys() :
            if 'data' in sample :
                era = sample.split('-')[1]
                samples[ 'QCD-'+era ] = {'group' : 'jetFakes'}
    samplesX = copy.deepcopy(samples)
       
    if makeQCDBkg :    
        qcdYields = {}
        for sign in ['SS', 'OS'] :
            for name in [isoVal+'_'+lIso, isoVal+'_'] :
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
            qcdSF = qcdYields['SS'+isoVal+'_'+cat] / qcdYields['SS'+isoVal+'_'+lIso+cat]
            if qcdYields['SS'+isoVal+'_'+lIso+cat] > 0 :
                qcdSF = qcdYields['SS'+isoVal+'_'+cat] / qcdYields['SS'+isoVal+'_'+lIso+cat]
            else : qcdSF = 9999 # Obviously a problem
            qcdFile.write( cat+":"+str(qcdSF)+"\n" )
        for key in qcdYields :
            qcdFile.write( "%s : %.2f\n" % (key, qcdYields[key]) )
        qcdFile.close()
        
    
    
    
    if makeFinalPlots :
        from util.helpers import getQCDSF, checkDir
        for cat in cats :
            for isoRegion in [isoVal+'_'+lIso, isoVal+'_'] :
                if not plotAntiIso and isoRegion == isoVal+'_'+lIso : continue
                if doFF and isoRegion == isoVal+'_'+lIso : continue
                ROOT.gROOT.Reset()
                tDir = cat if isoRegion == isoVal+'_' else cat+'_'+isoVal+'_'+lIso
                blind = True
                #if cat in ['inclusive', '0jet', '1jet', '0jet2D'] :
                #    blind = False
                
                if doFF :
                    kwargs = { 'text':text, 'blind':blind, 'targetDir':'/'+tDir,'sync':sync }
                else :
                    kwargs = { 'text':text, 'blind':blind, 
                        'targetDir':'/'+tDir,'sync':sync }
                    if isoRegion == isoVal+'_'+lIso :
                        kwargs['qcdMakeDM'] = cat+'_plotMe'
                        kwargs['qcdSF'] = 1.0
                    else :
                        kwargs['useQCDMakeName'] = str('OSl1ml2_'+isoVal+'_'+lIso+'ZTT'+cat).replace('dyShapeNew_','')
                        #str(.replace('dyShapeNew_',''),
                        kwargs['qcdSF'] = getQCDSF( 'httQCDYields_%s%s_%s.txt' % (pt, isoVal, params['mid2']), cat )
                        kwargs['useQCDMake'] = True
                analysis3Plots.makeLotsOfPlots( analysis, samplesX, ['tt',], 
                    params['mid2']+'_OSl1ml2_'+isoRegion+'ZTT'+cat, **kwargs  )
                cpDir = "/afs/cern.ch/user/t/truggles/www/HTT_%s" % params['mid2'].strip('2')
                checkDir( cpDir )
                subprocess.call( ["cp", "-r", "/afs/cern.ch/user/t/truggles/www/httPlots/tt/"+cat, cpDir] )
        
        
    if makeDataCards :
        ROOT.gROOT.Reset()
        from util.helpers import getQCDSF
        from analysisShapesROOT import makeDataCards
        #for var in ['m_visCor','m_sv'] :
        for var in ['m_sv',] :
        #for var in ['m_visCor',] :
            for cat in cats :
                #if var == 'm_visCor' and cat in ['boosted', 'vbf'] : continue
                #if var == 'm_visCor' and cat in ['boosted','vbf','0jet2D'] : continue
                if 'm_sv' in var :
                    if cat == 'boosted' : var = '%s:m_sv' % higgsPt
                    if cat == 'vbf' : var = 'mjj:m_sv'
                #if cat == 'boosted' : var = 'Higgs_PtCor:m_visCor'
                #if cat == 'vbf' : var = 'mjj:m_visCor'
                finalCat = cat
                if doFF :
                    folderDetails = params['mid2']+'_OSl1ml2_'+isoVal+'_ZTT'+cat
                    kwargs = {
                    'category' : finalCat,
                    'fitShape' : var,
                    'allShapes' : True,
                    'sync' : sync,
                    }
                    makeDataCards( analysis, samplesX, ['tt',], folderDetails, **kwargs )
                else :
                    qcdSF = getQCDSF( 'httQCDYields_%s%s_%s.txt' % (pt, isoVal, params['mid2']), cat )
                    folderDetails = params['mid2']+'_OSl1ml2_'+isoVal+'_ZTT'+cat
                    kwargs = {
                    'useQCDMakeName' : str(params['mid2']+'_OSl1ml2_'+isoVal+'_'+lIso+'ZTT'+cat).replace('dyShapeNew_',''),
                    'qcdSF' : qcdSF,
                    'category' : finalCat,
                    #'fitShape' : 'm_visCor',
                    'fitShape' : var,
                    'allShapes' : True,
                    'sync' : sync,
                    }
                    makeDataCards( analysis, samplesX, ['tt',], folderDetails, **kwargs )

                    # Make OS Loose QCD CR
                    folderDetails = params['mid2']+'_OSl1ml2_'+isoVal+'_'+lIso+'ZTT'+cat
                    kwargs = {
                    'useQCDMakeName' : str(params['mid2']+'_OSl1ml2_'+isoVal+'_'+lIso+'ZTT'+cat).replace('dyShapeNew_',''),
                    'qcdSF' : 1.0,
                    'category' : finalCat+'_qcd_cr',
                    #'fitShape' : 'm_visCor',
                    'fitShape' : var,
                    'allShapes' : True,
                    'sync' : sync,
                    }
                    makeDataCards( analysis, samplesX, ['tt',], folderDetails, **kwargs )

        app = '-FF' if doFF else '-StdMthd'
        #subprocess.call( ["mv", "shapes/htt/htt_tt.inputs-sm-13TeV_svFitMass.root", "shapes/htt/htt_tt.inputs-sm-13TeV_svFitMass-%s-%s.root" % (pt, isoVal)] )
        subprocess.call( ["mv", "shapes/htt/htt_tt.inputs-sm-13TeV_svFitMass2D.root", "shapes/htt/htt_tt.inputs-sm-13TeV_svFitMass2D-%s-%s.root" % (pt, isoVal)] )
        #subprocess.call( ["mv", "shapes/htt/htt_tt.inputs-sm-13TeV_svFitMass.root", "shapes/htt/htt_tt.inputs-sm-13TeV_svFitMass-%s-%s.root" % (pt, isoVal)] )
        #subprocess.call( ["mv", "shapes/htt/htt_tt.inputs-sm-13TeV_visMass2D.root", "shapes/htt/htt_tt.inputs-sm-13TeV_visMass2D-%s-%s%s.root" % (pt, isoVal, app)] )
    
    ''' Remove the .pngs used to build the QCD Bkg
    from the web directory so we can view easitly '''
    if cleanPlots :
        print "\nTrying to remove pngs used to build QCD Bkg\n"
        subprocess.call(["bash", "util/cleanDirs.sh"])
    










    
