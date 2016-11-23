import ROOT
from util.helpers import checkDir
import analysis1BaselineCuts
from meta.sampleNames import returnSampleDetails
from util.helpers import setUpDirs 



def buildRedBkgFakeFunctions( inSamples, **params ) :
    analysis = 'azh'
    params['doRedBkg'] = True
    params['mid1'] = params['mid1']+'RedBkg'
    params['mid2'] = params['mid2']+'RedBkg'
    params['mid3'] = params['mid3']+'RedBkg'

    setUpDirs( inSamples, params, analysis ) # Print config file and set up dirs
    inSamples = returnSampleDetails( analysis, inSamples )

    # Only do Red Bkg method on data
    samples = {}
    for samp, val in inSamples.iteritems() :
        if 'data' in samp : samples[samp] = val
    print samples

    # Apply initial Reducible Bkg Cuts for inclusive selection
    analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
    # Order events and choose best interpretation
#    analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)



    # This points back to doRedBkgPlots, but will load all data files 
    # into the chain which is passed in
#    analysis1BaselineCuts.drawHistos( analysis, samples, **params )




def doRedBkgPlots( analysis, chain, sample, channel ) :

    print "doing Red Bkg Plots",channel,sample




if '__main__' in __name__ :
    
    samples = ['dataEE-B', 'dataEE-C', 'dataEE-D', 'dataMM-B', 'dataMM-C', 'dataMM-D', 'TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'ZZ4lAMCNLO', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau',] # No WWW, data-E,F, ZZ4l MadGraph
    params = {
        #'debug' : 'true',
        'debug' : 'false',
        'numCores' : 20,
        'numFilesPerCycle' : 1,
        'channels' : ['eemm','eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm','eeee','mmmm'], # 8 + eeee + mmmm + eemm
        'cutMapper' : 'RedBkg',
        'mid1' : '1Nov23b',
        'mid2' : '2Nov23b',
        'mid3' : '3Nov23b',
        'additionalCut' : '',
        'svFitPost' : 'false',
        'svFitPrep' : 'false',
        'doFRMthd' : 'false',
        'skimmed' : 'false',
        #'skimmed' : 'true',
        'skimHdfs' : 'false',
        #'skimHdfs' : 'true',
    }
    buildRedBkgFakeFunctions( samples, **params )
