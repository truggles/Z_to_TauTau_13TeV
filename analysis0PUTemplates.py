from util.pileUpVertexCorrections import makePUTemplate
from util.buildTChain import makeTChain
import ROOT
from array import array
from time import gmtime, strftime
import argparse

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='25ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
results = p.parse_args()
grouping = results.sampleName

print "Running over %s samples" % grouping

''' Configuration '''
maxFiles = 20

channels = ['em', 'tt']

''' Preset samples '''
SamplesSync = ['Sync_HtoTT']
SamplesData = ['data_em', 'data_tt']
Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TTJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'WZ3l1nu', 'ZZ', 'ZZ4l', 'TT', 'TTPow'] # extra TT samples on stand by
#Samples25ns = ['DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TT', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l']


if grouping == 'Sync' : samples = SamplesSync
if grouping == '25ns' : samples = Samples25ns

#for sample in samples :
def makeAllPUTemplates( grouping, sample, channel, fileMin=0, fileMax=9999 ) :

    ''' Get initial chain '''
    print "###   %s PU Template   ###" % sample
    print "Channel:  %s" % channel
    sampleList = 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample)
    path = '%s/final/Ntuple' % channel
    # This should allow us to run over sections of files
    chain = makeTChain( sampleList, path, fileMax, fileMin, fileMax )
    numEntries = chain.GetEntries()
    print "%25s : %10i" % ('Initial', numEntries)

    makePUTemplate( grouping, sample, channel, chain )

for sample in samples :
    if 'data' in sample : tmpMax = 999
    else : tmpMax = maxFiles

    for channel in channels :
        if sample == 'data_em' and channel == 'tt' : continue
        if sample == 'data_tt' and channel == 'em' : continue

        makeAllPUTemplates( grouping, sample, channel, 0, tmpMax )
