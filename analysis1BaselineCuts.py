from util.buildTChain import makeTChain
from util.fileLength import file_len
import util.pileUpVertexCorrections
from analysis2IsoJetsAndDups import renameBranches
import ROOT
from array import array
from time import gmtime, strftime
import analysisCuts
import analysisPlots
import argparse

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='25ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
results = p.parse_args()
grouping = results.sampleName

maxTTfiles = 100
print "Running over %s samples" % grouping

''' Configuration '''
maxFiles = 0

#begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#print begin

channels = ['em', 'tt']

''' Preset samples '''
SamplesSync = ['Sync_HtoTT']
SamplesData = ['data_em', 'data_tt']
Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar_tW', 'T_tW', 'WJets', 'TT', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l']
Samples25nsQCD = ['QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']
#Samples25ns = ['Tbar_tW',]# 'T_tW']#, 'WJets', 'TT', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l', 'QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']

if grouping == 'Sync' : samples = SamplesSync
if grouping == '25ns' : samples = Samples25ns

def makeFile( grouping, mid, save) :
    outFile = ROOT.TFile('%s%s/%s.root' % (grouping, mid, save), 'RECREATE')
    return outFile

def closeFile( outFile ) :
    outFile.Close()
    

#for sample in samples :
def initialCut( outFile, grouping, sample, channel, cutMapper, cutName, fileMin=0, fileMax=9999 ) :
    path = '%s/final/Ntuple' % channel
    #treeOutDir = outFile.mkdir( path.split('/')[0] )

    ''' Get initial chain '''
    print "###   %s  ###" % sample
    print "Channel:  %s" % channel
    sampleList = 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample)
    # This should allow us to run over sections of files
    chain = makeTChain( sampleList, path, maxFiles, fileMin, fileMax )
    numEntries = chain.GetEntries()
    print "%25s : %10i" % ('Initial', numEntries)
    
    
    ''' Get channel specific general cuts '''
    exec 'cutMap = analysisCuts.%s( channel )' % cutMapper
    	
    ''' Copy and make some cuts while doing it '''
    ROOT.gROOT.cd() # This makes copied TTrees get written to general ROOT, not our TFile
    
    cutString = cutMap[ cutName ]
    chainNew = analysisCuts.makeGenCut( chain, cutString )
    numEntries = chainNew.GetEntries()
    print "%25s : %10i" % (cutName, numEntries)
    
    #treeOutDir.cd()
    #chainNew.Write()
    return (outFile, chainNew)



def plotHistos( outFile, chain, channel ) :
    ''' Make a channel specific selection of desired histos and fill them '''
    newVarMap = analysisPlots.getHistoDict( channel )

    histosDir = outFile.mkdir( "%s_Histos" % channel )
    histosDir.cd()
    ''' Combine Gen and Chan specific into one fill section '''
    histos = {}
    for var, cv in newVarMap.iteritems() :
    	histos[ var ] = analysisPlots.makeHisto( var, cv[1], cv[2], cv[3])
    #print "Initial:"
    #print histos

    # Get Pile Up reweight Dictionary
    if 'data' not in sample and grouping != 'Sync':
        puDict = util.pileUpVertexCorrections.PUreweight( grouping, sample, channel ) 
        #print puDict
        histosDir.cd()

    # Skip the EvtSet approach for now, as it takes too long
    # And FSA events are USUALLY never out of order
    # Does it actually take longer?!
    #eventSet = set()
    #previousEvt = (0, 0, 0)
    #evtNum = 0
    #fillCount = 0
    for i in range( chain.GetEntries() ):
        #evtNum += 1
        chain.GetEntry( i )
        
        # Apply Generator weights, speficially for DY Jets
        weight = 1
        if chain.GenWeight >= 0 : genWeight = 1
        if chain.GenWeight < 0 : genWeight = -1

        # Apply PU correction reweighting
        puWeight = 1
        if 'data' not in sample and grouping != 'Sync':
            puWeight = puDict[ chain.nvtx ]
        
        #eventTup = ( chain.run, chain.lumi, chain.evt )
        #currentEvt = ( chain.run, chain.lumi, chain.evt )
        #if eventTup not in eventSet :
        #if currentEvt != previousEvt :
        #    fillCount += 1
        for var, histo in histos.iteritems() :
            num = getattr( chain, newVarMap[ var ][0] )
            histo.Fill( num, (genWeight * puWeight) )
        #    previousEvt = currentEvt
            #eventSet.add( eventTup )
        #else : print "Skipped Dup"
    for var, histo in histos.iteritems() :
    	histo.Write()
    #print "%25s : %10i" % ('Events Plotted', fillCount)

    outFile.Write()
    return outFile



begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print begin
ROOT.gROOT.Reset()

#grouping = '25ns'

#samples = ['data_em', 'data_tt', 'DYJets', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l']
#samples = ['data_em', 'data_tt',]# 'T_tW', 'Tbar_tW']# 'TT']
#samples = ['T_tW',]# 'Tbar_tW']# 'TT']
#samples = ['TT',]
#samples = ['data_em', 'data_tt', 'DYJets', 'Tbar_tW', 'T_tW', 'WJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l']
samples = ['WJets',]

''' Cut configuration and location to save files: '''
### option 1 = Sync level cuts
cutMapper = 'quickCutMapSync'
cutName = 'BaseLine'
mid1 = '1BaseCut'
mid2 = '2IsoOrderAndDups'

### option 2 = Signal level cuts
#cutMapper = 'quickCutMapSingleCut'
#cutName = 'PostSync'
#mid1 = '1Single'
#mid2 = '2SingleIOAD'
#mid1 = '1PUTest'
#mid2 = '2PUTest'
#mid1 = '1noPU'
#mid2 = '2noPU'

for sample in samples :
    #if sample == 'TT' : continue
    fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample) )
    go = True
    count = 0
    while go :
        print " ====>  Loop Count %i  <==== " % count
        for channel in channels :

            if channel == 'em' and sample == 'data_tt' : continue
            if channel == 'tt' and sample == 'data_em' : continue

            if sample == 'TT' : save = '%s_%i_%s' % (sample, count, channel)
            elif 'data' in sample : save = sample
            else : save = '%s_%s' % (sample, channel)
            print "save",save

            ''' 1. Make cuts and save '''
            outFile1 = makeFile( grouping, mid1, save)
            outputs = initialCut( outFile1, grouping, sample, channel, cutMapper, cutName, count * maxTTfiles, (count + 1) * maxTTfiles-1 )
            dir1 = outputs[0].mkdir( channel )
            dir1.cd()
            outputs[1].Write()
            outFile1.Close()

            ''' 2. Rename branches, Tau and Iso order legs '''
            renameBranches( grouping, mid1, mid2, save, channel)

            ''' 3. Make the histos '''
            outFile2 = ROOT.TFile('%s%s/%s.root' % (grouping, mid2, save), 'UPDATE')
            #ifile = ROOT.TFile('%s%s/%s.root' % (grouping, mid2, save), 'r')
            print '%s%s/%s.root' % (grouping, mid2, save)
            #tree = ifile.Get('Ntuple')
            tree = outFile2.Get('Ntuple')
            plotHistos( outFile2, tree, channel )

            #''' 4. If this is data, make the PU template '''
            #if (sample == 'data_em' and channel == 'em') or (sample == 'data_tt' and channel == 'tt') :
            #    print "making PU template",sample,channel
            #    util.pileUpVertexCorrections.makeDataPUTemplate( grouping, tree, channel ) 

            # Close
            outFile2.Close()

        count += 1
        if sample != 'TT' : go = False
        elif count * maxTTfiles >= fileLen : go = False

print "Start Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
