from util.buildTChain import makeTChain
from util.fileLength import file_len
import ROOT
from array import array
from time import gmtime, strftime
import cutsBaseSelection as bc
import argparse

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='Sync', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--qcd', action='store', default=False, dest='qcd', help="Should we only run over QCD and Data?")
p.add_argument('--invert', action='store', default=False, dest='invert', help="Invert data Isolation values to model QCD?")
p.add_argument('--weight', action='store', default=True, dest='applyWeights', help="Apply GenWeight to mc samples?")
p.add_argument('--singleCut', action='store', default=True, dest='cuts', help="Single cut?")
results = p.parse_args()
pre_ = results.sampleName

print "Running over %s samples" % pre_

''' Configuration '''
weight = 1
maxFiles = 0

begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print begin

channels = ['em', 'tt']

''' Preset samples '''
SamplesSync = ['Sync_HtoTT']
SamplesData = ['data_em', 'data_tt']
Samples25ns = ['DYJets', 'Tbar_tW', 'T_tW', 'WJets', 'TT', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l', 'QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']

if pre_ == 'Sync' : samples = SamplesSync
if pre_ == '25ns' : samples = Samples25ns



for sample in samples :
    sampleList = 'meta/NtupleInputs_%s/%s.txt' % (pre_, sample)
    # Get length of the txt file
    fileLen = file_len( sampleList )
    count = 0
    done = False
        
    while not done :
        ROOT.gROOT.Reset()
        if sample == 'TT' :
            outFile = ROOT.TFile('%s1BaseCut/%s_%i.root' % (pre_, sample, count), 'RECREATE')
        else :
            outFile = ROOT.TFile('%s1BaseCut/%s.root' % (pre_, sample), 'RECREATE')
        print "###   %s %i  ###" % (sample, count)
        for channel in channels :
            print "Channel:  %s" % channel
            
            ''' Get initial chain '''
            path = '%s/final/Ntuple' % channel
            # Break TT into groups of 250 files b/c it's so BIG
            if sample == 'TT' :
                chain = makeTChain( sampleList, path, maxFiles, count * 150, (count + 1) * 150 )
            else :
                chain = makeTChain( sampleList, path, maxFiles )
            numEntries = chain.GetEntries()
            print "%25s : %10i" % ('Initial', numEntries)
            treeOutDir = outFile.mkdir( path.split('/')[0] )
            
            
            ''' Get channel specific general cuts '''
            cutMap = bc.quickCutMapSync( channel )
            
            	
            ''' Copy and make some cuts while doing it '''
            ROOT.gROOT.cd() # This makes copied TTrees get written to general ROOT, not our TFile
        
            cutName = 'BaseLine'
            cutString = cutMap[ cutName ]
            chainNew = bc.makeGenCut( chain, cutString )
            numEntries = chainNew.GetEntries()
            print "%25s : %10i" % (cutName, numEntries)
            
            treeOutDir.cd()
            chainNew.Write()
        count += 1
        if sample != 'TT' :
            done = True
        elif sample == 'TT' and (count + 1) * 250 > fileLen :
            done = True
    

        outFile.Write()
        outFile.Close()

print "Start Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
