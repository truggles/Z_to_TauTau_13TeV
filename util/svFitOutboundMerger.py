import os, glob, subprocess
import ROOT


def mergeSample( jobId, recoilType, TESType, isWJets, sample, channel ) :
    
    # Check if outbound directory exists
    # Make outbound directory
    if not os.path.exists( '/data/truggles/svFitPrep/%s_out' % jobId ) :
        os.makedirs( '/data/truggles/svFitPrep/%s_out' % jobId )
    if not os.path.exists( '/data/truggles/svFitPrep/%s_out/Recoil%i_TESType%i_isWJ%i' % (jobId, recoilType, TESType, isWJets) ) :
        os.makedirs( '/data/truggles/svFitPrep/%s_out/Recoil%i_TESType%i_isWJ%i' % (jobId, recoilType, TESType, isWJets) )
    outDir = '/data/truggles/svFitPrep/%s_out/Recoil%i_TESType%i_isWJ%i' % (jobId, recoilType, TESType, isWJets)
    print "Output Dir: ",outDir
    
    # Get our per-merged filelist
    files = glob.glob('/data/truggles/svFitPrep/%s/%s_*_%s.root' % (jobId, sample, channel) )
    
    rep = 0
    runningEvtSize = 0
    toMerge = []
    ints = []
    for file_ in files :
    
        # Merge to ~ 1000 events per file
        f = ROOT.TFile(file_,'r')
        t = f.Get('%s/Ntuple' % channel)
        size = t.GetEntries()
        print size,"   ",file_
    
    	runningEvtSize += size
        print "running size: ",runningEvtSize
    	toMerge.append( file_ )
    	if runningEvtSize > 1000 :
    		runningEvtSize = 0
    		mergeList = ["hadd", "-f", "%s/%s_%i_%s.root" % (outDir, sample, rep, channel)]
    		for f in toMerge :
    			mergeList.append( f )
    		subprocess.call( mergeList )
    		ints = []
    		toMerge = []
    		rep += 1
    mergeList = ["hadd", "-f", "%s/%s_%i_%s.root" % (outDir, sample, rep, channel)]
    for f in toMerge :
    	mergeList.append( f )
    if len( mergeList ) > 3 : # greater than 3 means we actually have a file to merge (not empty)
    	subprocess.call( mergeList )





if __name__ == '__main__' :

    AllSamples = ['DYJets', 'DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJetsHigh', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'data', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'] # As of April03

    jobId = 'dataCards1April10a'
    channels = ['em', 'tt']
    #channels = ['em',]
    #channels = ['tt',]

    """ section 1, Need TES, Recoil type 2, no WJets """
    samples = ['DYJets', 'DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJetsHigh', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130']
    masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
    for mass in masses :
       samples.append( 'ggH%i' % mass )
       samples.append( 'bbH%i' % mass )

    recoilType = 2 # 0 = no recoil
        # 1 = aMC@NLO DY and W+Jets MC samples
        # 2 = MG5 DY and W+Jets MC samples or Higgs MC samples
    TESType = 1 # 0 = no TES
        # 1 = Apply TES
    isWJets = 0
    for sample in samples :
        for channel in channels :
            mergeSample( jobId, recoilType, TESType, isWJets, sample, channel )



    """ section 2, No TES, Recoil type 2, WJets """
    samples = ['WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4']
    recoilType = 2 # 0 = no recoil
        # 1 = aMC@NLO DY and W+Jets MC samples
        # 2 = MG5 DY and W+Jets MC samples or Higgs MC samples
    TESType = 0 # 0 = no TES
        # 1 = Apply TES
    isWJets = 1
    for sample in samples :
        for channel in channels :
            mergeSample( jobId, recoilType, TESType, isWJets, sample, channel )



    """ section 3, No TES, no recoil, no WJets """
    samples = ['T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'data'] 
    recoilType = 0 # 0 = no recoil
        # 1 = aMC@NLO DY and W+Jets MC samples
        # 2 = MG5 DY and W+Jets MC samples or Higgs MC samples
    TESType = 0 # 0 = no TES
        # 1 = Apply TES
    isWJets = 0
    for sample in samples :
        for channel in channels :
            mergeSample( jobId, recoilType, TESType, isWJets, sample, channel )








