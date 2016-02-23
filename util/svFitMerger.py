


import os, glob, subprocess


def mergeSample( jobId, sample, channel ) :
        files = glob.glob('/hdfs/store/user/truggles/feb22_svFitFeb21SkimX/test/%s-%s_*_%s.root' % (jobId, sample, channel) )

        rep = 0
        runningSize = 0
        toMerge = []
        ints = []
        for file_ in files :
                size = os.path.getsize( file_ )/1000 # in KB roughly
                print size, " KB ", file_
                runningSize += size
                toMerge.append( file_ )
                if runningSize > 25000 :
                        runningSize = 0
                        mergeList = ["hadd", "-f", "/nfs_scratch/truggles/svFitComplete/feb23_fromFeb21SkimX/%s_%i_%s.root" % (sample, rep, channel)]
                        for f in toMerge :
                                mergeList.append( f )
                        subprocess.call( mergeList )
                        ints = []
                        toMerge = []
                        rep += 1
        mergeList = ["hadd", "-f", "/nfs_scratch/truggles/svFitComplete/feb23_fromFeb21SkimX/%s_%i_%s.root" % (sample, rep, channel)]
        for f in toMerge :
                mergeList.append( f )
        subprocess.call( mergeList )


#hadd -f /nfs_scratch/truggles/svFitComplete/feb23_fromFeb21SkimX/data_tt.root /hdfs/store/user/truggles/feb22_svFitFeb21SkimX/test/TauTau_13_test-data_*_tt.root
#for SAMPLE in DYJets  DYJets1 DYJets2  DYJets3  DYJets4  DYJetsFXFX  DYJetsLow  T-tchan  Tbar-tchan  Tbar-tW  T-tW  TT  WJets  WW1l1nu2q; do #  WZJets  WZ1l1nu2q  WZ1l3nu  WZ2l2q  ZZ2l2q  ZZ4l VBFHtoTauTau120 VBFHtoTauTau125 VBFHtoTauTau130 ggHtoTauTau125 ggHtoTauTau130; do
#for MASS in 80 90 100 110 120 130 140 160 180 450 500 600 700 800 900 1000 1200 1400 1500 1600 1800 2000 2600 2900 3200; do



if __name__ == '__main__' :

        samples = ['data', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau125', 'ggHtoTauTau130', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJetsFXFX', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZJets',]# 'ZZ2l2q', 'ZZ4l']
        masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2600, 2900, 3200]
        for mass in masses :
                samples.append( 'ggH%i' % mass )
                samples.append( 'bbH%i' % mass )

        jobId = 'TauTau_13_test'
        channels = ['em', 'tt']

        for sample in samples :
                for channel in channels :
                        mergeSample( jobId, sample, channel )




