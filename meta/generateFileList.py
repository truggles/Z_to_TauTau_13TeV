
import os, glob, subprocess



def makeFileList( jobId, folder, sample, channel ) :
    files = glob.glob('/data/truggles/%s/%s_*_%s.root' % (jobId, sample, channel) )
    ofile = open('%s/sv_%s_%s.txt' % (folder, sample, channel), "w")

    for file_ in files :
        ofile.write( file_.strip() + "\n" )

    ofile.close()



if __name__ == '__main__' :

    folder = 'NtupleInputs_dataCards'
    samples = ['data', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau125', 'ggHtoTauTau130', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJetsFXFX', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l']
    masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2600, 2900, 3200]
    for mass in masses :
        samples.append( 'ggH%i' % mass )
        samples.append( 'bbH%i' % mass )
    
    jobId = 'svFitComplete/feb23_fromFeb21SkimX'
    channels = ['em', 'tt']
    
    for sample in samples :
        for channel in channels :
            print "Sample: %25s --- %s" % (sample, channel)
            makeFileList( jobId, folder, sample, channel )
    
    
