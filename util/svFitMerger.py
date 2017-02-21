import os, glob, subprocess
from util.helpers import checkDir


def mergeSample( jobId, sample, channel, originalDir, targetDir ) :
    files = glob.glob(originalDir+'/%s%s_*_%s.root' % (jobId, sample, channel) )
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

#    # AZH Jan 19 hdfs -> UW
#    azhSamples = ['dataEE-B', 'dataEE-C', 'dataEE-D', 'dataEE-E', 'dataEE-F', 'dataEE-G', 'dataEE-H', 'dataMM-B', 'dataMM-C', 'dataMM-D', 'dataMM-E', 'dataMM-F', 'dataMM-G', 'dataMM-H', 'TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'ZZ4l', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'WWW', 'WWZ', 'WZ', 'WZZ', 'ZZ', 'ZZZ'] # Jan 14 samples
#    azhSamples.append('WMinusHTauTau125')
#    azhSamples.append('WPlusHTauTau125')
#    #azhSamples = []
#    for mass in [120, 125, 130] :
#        #azhSamples.append('ggHtoTauTau%i' % mass)
#        #azhSamples.append('VBFHtoTauTau%i' % mass)
#        #azhSamples.append('WMinusHTauTau%i' % mass)
#        #azhSamples.append('WPlusHTauTau%i' % mass)
#        azhSamples.append('ZHTauTau%i' % mass)
#        #azhSamples.append('ttHTauTau%i' % mass)
#    for mass in [220, 240, 260, 280, 300, 320, 350, 400] :
#        azhSamples.append('azh%i' % mass)
#    originalDir = '/nfs_scratch/truggles/azhJan19newSkim'
#    targetDir = '/nfs_scratch/truggles/azhJan19newSkimMerged'
#    jobId = ''
#    channels = ['eemm','eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm','eeee','mmmm'] # 8 + eeee + mmmm + eemm
#    for channel in channels :
#        for sample in azhSamples :
#                mergeSample( jobId, sample, channel, originalDir, targetDir )
    

    # HTT Feb 21 hdfs -> UW
    SamplesDataCards = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJets1Low', 'DYJets2Low', 'EWKWMinus', 'EWKWPlus', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'VV', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WWW', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZ3l1nu', 'ZZ2l2q', 'ZZ4l'] # Feb17 for Moriond17 
    
    #for mass in [120, 125, 130] :
    for mass in [125,] :
        SamplesDataCards.append('ggHtoTauTau%i' % mass)
        SamplesDataCards.append('VBFHtoTauTau%i' % mass)
        SamplesDataCards.append('VBFHtoWW2l2nu%i' % mass)
        SamplesDataCards.append('WMinusHTauTau%i' % mass)
        SamplesDataCards.append('WPlusHTauTau%i' % mass)
        SamplesDataCards.append('ZHTauTau%i' % mass)
        SamplesDataCards.append('HtoWW2l2nu%i' % mass)
    
        
    for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
        SamplesDataCards.append('dataTT-%s' % era)
    SamplesDataCards = ['DYJets',] # Feb17 for Moriond17 

    originalDir = '/data/truggles/svFitFeb17_SM-HTT/*'
    targetDir = '/data/truggles/svFitFeb17_SM-HTT_Merged'
    jobId = 'TauTau_13*'
    for sample in SamplesDataCards :
            mergeSample( jobId, sample, 'tt', originalDir, targetDir )


