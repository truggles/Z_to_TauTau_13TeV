import os, glob, subprocess
from util.helpers import checkDir


def mergeSample( jobId, sample, channel, originalDir, targetDir ) :
    files = glob.glob(originalDir+'/%s%s_*_%s.root' % (jobId, sample, channel) )
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
        if runningSize > 50000 : # 7.5 MB is reasonal for doing duplicate removal later
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

    # AZH Jan 19 hdfs -> UW
    azhSamples = ['dataEE-B', 'dataEE-C', 'dataEE-D', 'dataEE-E', 'dataEE-F', 'dataEE-G', 'dataEE-H', 'dataMM-B', 'dataMM-C', 'dataMM-D', 'dataMM-E', 'dataMM-F', 'dataMM-G', 'dataMM-H', 'TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'ZZ4l', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'WWW', 'WWZ', 'WZ', 'WZZ', 'ZZ', 'ZZZ'] # Jan 14 samples
    azhSamples.append('WMinusHTauTau125')
    azhSamples.append('WPlusHTauTau125')
    #azhSamples = []
    for mass in [120, 125, 130] :
        #azhSamples.append('ggHtoTauTau%i' % mass)
        #azhSamples.append('VBFHtoTauTau%i' % mass)
        #azhSamples.append('WMinusHTauTau%i' % mass)
        #azhSamples.append('WPlusHTauTau%i' % mass)
        azhSamples.append('ZHTauTau%i' % mass)
        #azhSamples.append('ttHTauTau%i' % mass)
    for mass in [220, 240, 260, 280, 300, 320, 350, 400] :
        azhSamples.append('azh%i' % mass)
    originalDir = '/nfs_scratch/truggles/azhJan19newSkim'
    targetDir = '/nfs_scratch/truggles/azhJan19newSkimMerged'
    jobId = ''
    channels = ['eemm','eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm','eeee','mmmm'] # 8 + eeee + mmmm + eemm
    for channel in channels :
        for sample in azhSamples :
                mergeSample( jobId, sample, channel, originalDir, targetDir )
    




