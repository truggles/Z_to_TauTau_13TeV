import os, glob, subprocess
from util.helpers import checkDir
import multiprocessing


def mergeSample( jobId, sample, channel, originalDir, targetDir ) :
    print "Checking here: "+originalDir+'%s%s_*_%s.root' % (jobId, sample, channel)
    files = glob.glob(originalDir+'%s%s_*_%s.root' % (jobId, sample, channel) )
    for file in files :
        print file
    checkDir( targetDir )

    rep = 0
    runningSize = 0
    toMerge = []
    ints = []
    for file_ in files :
        size = os.path.getsize( file_ )/1000 # in KB roughly
        print size, " KB ", file_
        runningSize += size
        toMerge.append( file_ )
        if runningSize > 15000 : # 7.5 MB is reasonal for doing duplicate removal later
            runningSize = 0
            mergeList = ["hadd", "-f", targetDir+"/%s_%i_%s.root" % (sample, rep, channel)]
            for f in toMerge :
                mergeList.append( f )
            subprocess.call( mergeList )
            ints = []
            toMerge = []
            rep += 1
    mergeList = ["hadd", "-f", targetDir+"/%s_%i_%s.root" % (sample, rep, channel)]
    for f in toMerge :
        mergeList.append( f )
    if len( mergeList ) > 3 : # greater than 3 means we actually have a file to merge (not empty)
        subprocess.call( mergeList )


#def removeFailed( jobId, sample, channel, originalDir ) :
#    files = glob.glob(originalDir+'/%s%s_*_%s.root' % (jobId, sample, channel) )
#
#    rep = 0
#    runningSize = 0
#    for file_ in files :
#        size = os.path.getsize( file_ )/1000. # in KB roughly
#        print size, " KB ", file_
#        if size < 10. : print "Small file



if __name__ == '__main__' :
    ''' Start multiprocessing tests '''
    pool = multiprocessing.Pool(processes = 6 )
    multiprocessingOutputs = []
    debug = False
    doAZH = True
    doHTT = False


    if doAZH :
        # AZH June 01 Wisconsin -> uwlogin
        azhSamples = ['ttZ', 'ttZ2', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'TT', 'WWW', 'WWZ', 'WZ3l1nu', 'WZZ', 'WZ', 'ZZ4l', 'ZZZ',] # May 31 samples, no ZZ->all, use ZZ4l
        
        for mass in [110, 120, 125, 130, 140] :
            azhSamples.append('ggHtoTauTau%i' % mass)
            azhSamples.append('VBFHtoTauTau%i' % mass)
            azhSamples.append('WMinusHTauTau%i' % mass)
            azhSamples.append('WPlusHTauTau%i' % mass)
            azhSamples.append('ZHTauTau%i' % mass)
            #azhSamples.append('ttHTauTau%i' % mass)
        for mass in [125,] :
            azhSamples.append('ZHWW%i' % mass)
            azhSamples.append('HZZ%i' % mass)
        
        for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
            azhSamples.append('azh%i' % mass)
        
        for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
            azhSamples.append('dataEE-%s' % era)
            azhSamples.append('dataMM-%s' % era)
            azhSamples.append('dataSingleE-%s' % era)
            azhSamples.append('dataSingleM-%s' % era)

        name = 'azhHalloweenSkim_svFitPrep'
        originalDir = '/data/truggles/'+name+'/'
        targetDir = '/data/truggles/'+name+'_Merged'
        checkDir( targetDir )
        jobId = 'TauTau_13*'
        jobId = ''
        channels = ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm','eeee','mmmm'] # 8 + eeee + mmmm + eemm
        for channel in channels :
            for sample in azhSamples :
                if debug:
                    mergeSample( jobId, sample, channel, originalDir, targetDir )
                else :
                    multiprocessingOutputs.append( pool.apply_async(mergeSample, args=(
                        jobId,
                        sample,
                        channel,
                        originalDir,
                        targetDir )))
        if not debug :
            mpResults = [p.get() for p in multiprocessingOutputs]
    


    if doHTT :
        # HTT Feb 21 hdfs -> UW
        SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJets1Low', 'DYJets2Low', 'EWKWMinus', 'EWKWPlus', 'EWKZ2l', 'EWKZ2nu', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'VV', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WWW', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZ3l1nu', 'ZZ2l2q', 'ZZ4l'] # Feb17 for Moriond17 
        
        for mass in [110, 120, 125, 130, 140] :
            SamplesDataCards.append('ggHtoTauTau%i' % mass)
            SamplesDataCards.append('VBFHtoTauTau%i' % mass)
            SamplesDataCards.append('VBFHtoWW2l2nu%i' % mass)
            SamplesDataCards.append('WMinusHTauTau%i' % mass)
            SamplesDataCards.append('WPlusHTauTau%i' % mass)
            SamplesDataCards.append('ZHTauTau%i' % mass)
            SamplesDataCards.append('HtoWW2l2nu%i' % mass)
            SamplesDataCards.append('ttHTauTau%i' % mass)
        
            
        for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
            SamplesDataCards.append('dataTT-%s' % era)

        originalDir = '/hdfs/store/user/truggles/svFitMay30_RivetSignals_SM-HTT/Recoil*/*'
        targetDir = '/nfs_scratch/truggles/svFitMay30_RivetSignals_SM-HTT_Merged'
        checkDir( targetDir )
        jobId = 'TauTau_13*'
        jobId = ''
        for sample in SamplesDataCards :
             if debug:
                 mergeSample( jobId, sample, 'tt', originalDir, targetDir )
             else :
                 multiprocessingOutputs.append( pool.apply_async(mergeSample, args=(
                     jobId,
                     sample,
                     'tt',
                     originalDir,
                     targetDir )))
        if not debug :
            mpResults = [p.get() for p in multiprocessingOutputs]





