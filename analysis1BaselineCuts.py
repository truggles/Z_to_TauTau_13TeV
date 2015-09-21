from util.buildTChain import makeTChain
from util.fileLength import file_len
from util.isoOrder import isoOrder, getTauIsoDic
from analysis2IsoJetsAndDups import renameBranches
import ROOT
from array import array
from time import gmtime, strftime
import cutsBaseSelection as bc
import argparse

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='25ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
results = p.parse_args()
grouping = results.sampleName

maxTTfiles = 100
print "Running over %s samples" % grouping

''' Configuration '''
weight = 1
maxFiles = 0

#begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#print begin

channels = ['em', 'tt']

''' Preset samples '''
SamplesSync = ['Sync_HtoTT']
SamplesData = ['data_em', 'data_tt']
Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar_tW', 'T_tW', 'WJets', 'TT', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l', 'QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']
#Samples25ns = ['Tbar_tW',]# 'T_tW']#, 'WJets', 'TT', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l', 'QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']

if grouping == 'Sync' : samples = SamplesSync
if grouping == '25ns' : samples = Samples25ns

def makeFile( grouping, save) :
    outFile = ROOT.TFile('%s1BaseCut/%s.root' % (grouping, save), 'RECREATE')
    return outFile

def closeFile( outFile ) :
    outFile.Close()
    

#for sample in samples :
def initialCut( outFile, grouping, sample, channel, count=0, maxTTfiles=999 ) :
    path = '%s/final/Ntuple' % channel
    #treeOutDir = outFile.mkdir( path.split('/')[0] )

    ''' Get initial chain '''
    print "###   %s  ###" % sample
    print "Channel:  %s" % channel
    sampleList = 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample)
    # This should allow us to run over sections of files
    chain = makeTChain( sampleList, path, maxFiles, count * maxTTfiles, (count + 1) * maxTTfiles )
    numEntries = chain.GetEntries()
    print "%25s : %10i" % ('Initial', numEntries)
    
    
    ''' Get channel specific general cuts '''
    cutMap = bc.quickCutMapSync( channel )
    
    	
    ''' Copy and make some cuts while doing it '''
    ROOT.gROOT.cd() # This makes copied TTrees get written to general ROOT, not our TFile
    
    cutName = 'BaseLine'
    cutString = cutMap[ cutName ]
    chainNew = bc.makeGenCut( chain, cutString )
    numEntries = chainNew.GetEntries()
    print "%25s : %10i" % (cutName, numEntries)
    
    #treeOutDir.cd()
    #chainNew.Write()
    return (outFile, chainNew)



def plotHistos( outFile, chain, channel ) :
    ''' Make a channel specific selection of desired histos and fill them '''
    if channel == 'em' : varMap = bc.getEMHistoDict()
    if channel == 'tt' : varMap = bc.getTTHistoDict()
    
    genVar = bc.getGeneralHistoDict()
    newVarMap = genVar
    for var, details in varMap.iteritems() :
    	newVarMap[ var ] = details

    histosDir = outFile.mkdir( "%s_Histos" % channel )
    histosDir.cd()
    ''' Combine Gen and Chan specific into one fill section '''
    histos = {}
    for var, cv in newVarMap.iteritems() :
    	histos[ var ] = bc.makeHisto( var, cv[1], cv[2], cv[3])
    #print "Initial:"
    #print histos
    
    # Skip the EvtSet approach for now, as it takes too long
    # And FSA events are USUALLY never out of order
    # Does it actually take longer?!
    #eventSet = set()
    previousEvt = (0, 0, 0)
    evtNum = 0
    fillCount = 0
    for i in range( chain.GetEntries() ):
        evtNum += 1
        chain.GetEntry( i )
        
        # Apply Generator weights, speficially for DY Jets
        if chain.GenWeight >= 0 : weight = 1
        if chain.GenWeight < 0 : weight = -1
        
        #eventTup = ( chain.run, chain.lumi, chain.evt )
        currentEvt = ( chain.run, chain.lumi, chain.evt )
        #if eventTup not in eventSet :
        if currentEvt != previousEvt :
            fillCount += 1
            for var, histo in histos.iteritems() :
                num = getattr( chain, newVarMap[ var ][0] )
                histo.Fill( num, weight )
            previousEvt = currentEvt
            #eventSet.add( eventTup )
        #else : print "Skipped Dup"
    for var, histo in histos.iteritems() :
    	histo.Write()
    print "%25s : %10i" % ('Event Selection', fillCount)

    outFile.Write()
    return outFile



begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print begin
ROOT.gROOT.Reset()

grouping = '25ns'

#samples = ['data_em', 'ZZ']
#samples = ['TT',]
#save = 'T_tWTester4'

for sample in samples :
    if sample == 'TT' : continue
    fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample) )
    go = True
    count = 0
    #while go :
    #    print " ====>  Loop Count %i  <==== " % count
    #    save = '%s_%i' % (sample, count)
    #    outFile = makeFile( grouping, save)
    #    outputs = initialCut( outFile, grouping, sample, 'em', count * maxTTfiles, (count + 1) * maxTTfiles )
    #    dir1 = outputs[0].mkdir( 'em' )
    #    dir1.cd()
    #    outputs[1].Write()
    #    #outFile = plotHistos( outputs[0], outputs[1], 'em' )
    #    outputs = initialCut( outFile, grouping, sample, 'tt', count * maxTTfiles, (count + 1) * maxTTfiles )
    #    dir1 = outputs[0].mkdir( 'tt' )
    #    dir1.cd()
    #    outputs[1].Write()
    #    #outFile = plotHistos( outputs[0], outputs[1], 'tt' )
    #    closeFile( outFile )
    #    
    #    renameBranches( grouping, save, 'tt')
    #    renameBranches( grouping, save, 'em')
    #    count += 1
    #    if count * maxTTfiles >= fileLen : go = False

    #else :
    save = sample
    outFile = makeFile( grouping, save)
    outputs = initialCut( outFile, grouping, sample, 'em', count=0, maxTTfiles=999 )
    dir1 = outputs[0].mkdir( 'em' )
    dir1.cd()
    outputs[1].Write()
    #outFile = plotHistos( outputs[0], outputs[1], 'em' )
    outputs = initialCut( outFile, grouping, sample, 'tt', count=0, maxTTfiles=999 )
    dir1 = outputs[0].mkdir( 'tt' )
    dir1.cd()
    outputs[1].Write()
    #outFile = plotHistos( outputs[0], outputs[1], 'tt' )
    closeFile( outFile )
    
    renameBranches( grouping, save, 'tt')
    renameBranches( grouping, save, 'em')
    #renameBranches( 'Sync', 'tmp', 'tt')
    #renameBranches( 'Sync', 'tmp', 'em')

print "Start Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
