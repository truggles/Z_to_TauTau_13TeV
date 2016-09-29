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
		if runningSize > 75000 : # 7.5 MB is reasonal for doing duplicate removal later
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




if __name__ == '__main__' :

    targetDir = '/data/truggles/2016-ZTT-April11Merged'
    
    # Recoil2, TES1, WJets0
    samples = ['DYJetsBig', 'DYJetsLow', 'DYJetsHigh', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130']
    originalDir = '/data/truggles/2015-ZTT-svFit/april11_svFit_2/Recoil2_TESType1_isWJ0'
    jobId = 'TauTau_13_Recoil2_TESType1_isWJ0-'
    channel = 'tt'
    for sample in samples :
        mergeSample( jobId, sample, channel, originalDir, targetDir )
    
    
    # Recoil0 TES0 WJets0
    originalDir = '/data/truggles/2015-ZTT-svFit/april11_svFit/Recoil0_TESType0_isWJ0'
    jobId = 'TauTau_13_Recoil0_TESType0_isWJ0-'
    samples = ['T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZ3l1nu', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV',]
    for sample in samples :
        mergeSample( jobId, sample, channel, originalDir, targetDir )
    
    
    # Recoil0 TES0 WJets0
    originalDir = '/data/truggles/2015-ZTT-svFit/april11_svFit/Recoil2_TESType0_isWJ1/'
    jobId = 'TauTau_13_Recoil2_TESType0_isWJ1-'
    samples = ['WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4',]
    for sample in samples :
        mergeSample( jobId, sample, channel, originalDir, targetDir )
    
    
    
