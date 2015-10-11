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
import multiprocessing
import math
from ROOT import gPad, gROOT

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='25ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--bkgs', action='store', default='None', dest='bkgs', help="Run a specific background with specific cuts?")
results = p.parse_args()
grouping = results.sampleName
bkgs = results.bkgs

numFilesPerCycle = 100
print "Running over %s samples" % grouping

''' Configuration '''
maxFiles = 0

#begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#print begin

channels = ['em', 'tt']

''' Preset samples '''
SamplesSync = ['Sync_HtoTT']
SamplesData = ['data_em', 'data_tt']
#Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TTJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'WZ3l1nu', 'ZZ', 'ZZ4l', 'TTPow', 'TT']
Samples25nsQCD = ['QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']

Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'TT', 'WW', 'WZJets', 'ZZ'] # Intended good one

bkgMap = {
            # cutMapper       samples
    'WJets' : ['wJetsShape', ['WJets',]],
    'QCD'   : ['QCDShape', ['data_em', 'data_tt',]],
    'None'  : ['', '', '', '']
    }

if grouping == 'Sync' : samples = SamplesSync
if grouping == '25ns' : samples = Samples25ns
if grouping == 'data' :
    samples = SamplesData
    grouping = '25ns'
if bkgs != 'None' : samples = bkgMap[ bkgs ][1]


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
    #print "###   %s  ###" % sample
    #print "Channel:  %s" % channel
    sampleList = 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample)
    # This should allow us to run over sections of files
    chain = makeTChain( sampleList, path, maxFiles, fileMin, fileMax )
    numEntries = chain.GetEntries()
    #print "%25s : %10i" % ('Initial', numEntries)
    initialQty = "%25s : %10i" % ('Initial', numEntries)
    
    
    ''' Get channel specific general cuts '''
    exec 'cutMap = analysisCuts.%s( channel )' % cutMapper
    	
    ''' Copy and make some cuts while doing it '''
    ROOT.gROOT.cd() # This makes copied TTrees get written to general ROOT, not our TFile
    
    cutString = cutMap[ cutName ]
    chainNew = analysisCuts.makeGenCut( chain, cutString )
    numEntries = chainNew.GetEntries()
    #print "%25s : %10i" % (cutName, numEntries)
    postCutQty = "%25s : %10i" % (cutName, numEntries)
    
    #treeOutDir.cd()
    #chainNew.Write()
    return (outFile, chainNew, initialQty, postCutQty)



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

    
    ''' Scale the histo taking into account events which are 1) out of range and 2) GenWeights '''
    # Parameters to track the number of positive and negative GenWeight events
    # so that we  can reweight the histo at the end
    # Order is : pos, neg
    scalingDict = {}
    for var in histos.keys() :
        scalingDict[ var ] = [0, 0]

    for i in range( chain.GetEntries() ):
        chain.GetEntry( i )
        
        # Apply Generator weights, speficially for DY Jets
        if chain.GenWeight >= 0 : genWeight = 1
        if chain.GenWeight < 0 : genWeight = -1

        # Apply PU correction reweighting
        puWeight = 1
        if 'data' not in sample and grouping != 'Sync':
            puWeight = puDict[ chain.nvtx ]
        
        w = chain.GenWeight
        for var, histo in histos.iteritems() :
            num = getattr( chain, newVarMap[ var ][0] )
            ret = histo.Fill( num, (genWeight * puWeight) )
            if ret > 0 and not 'data' in sample :
                if w > 0 : scalingDict[ var ][0] += 1
                elif w < 0 : scalingDict[ var ][1] += 1
    #print scalingDict

    for var, histo in histos.iteritems() :
        # Add in scaling for GenWeight!
        #print "Var: %s    Integral Pre: %f" % (var, histo.Integral() )
        if not 'data' in sample and histo.Integral() > 0 :
            histo.Scale( ( scalingDict[ var ][0] - scalingDict[ var ][1] ) / histo.Integral() )
        #print "Var: %s    Integral Pre: %f" % (var, histo.Integral() )
    	histo.Write()

    return outFile

def runCode(grouping, sample, channel, count, num) :

    if 'data' in sample : save = 'data_%i_%s' % (count, channel)
    else : save = '%s_%i_%s' % (sample, count, channel)
    #print "save",save
    print "%5i %20s %10s %3i: ====>>> START <<<====" % (num, sample, channel, count)

    ''' 1. Make cuts and save '''
    if doCuts :
        print "%5i %20s %10s %3i: Started Cuts" % (num, sample, channel, count)
        if bkgs != 'None' :
            outFile1 = ROOT.TFile('meta/%sBackgrounds/%s/cut/%s.root' % (grouping, bkgMap[ bkgs ][0], save), 'RECREATE')
        else :
            outFile1 = makeFile( grouping, mid1, save)
        cutOut = initialCut( outFile1, grouping, sample, channel, cutMapper, cutName, count * numFilesPerCycle, (count + 1) * numFilesPerCycle-1 )
        dir1 = cutOut[0].mkdir( channel )
        dir1.cd()
        cutOut[1].Write()
        outFile1.Close()
        initialQty = cutOut[2]
        postCutQty = cutOut[3]
        print "%5i %20s %10s %3i: Finished Cuts" % (num, sample, channel, count)

    ''' 2. Rename branches, Tau and Iso order legs '''
    if doOrdering :
        print "%5i %20s %10s %3i: Started Iso Ordering" % (num, sample, channel, count)
        isoQty = renameBranches( grouping, mid1, mid2, save, channel, bkgMap[ bkgs ][0])
        #print '%s%s/%s.root' % (grouping, mid2, save)
        #output.put( '%s%s/%s.root' % (grouping, mid2, save) )
        print "%5i %20s %10s %3i: Finished Iso Ordering" % (num, sample, channel, count)

    #output.put((num, sample, channel, count, initialQty, postCutQty, isoQty ))
    print "%5i %20s %10s %3i: ====>>> DONE <<<====" % (num, sample, channel, count)
    return (num, sample, channel, count, initialQty, postCutQty, isoQty )

begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print begin
ROOT.gROOT.Reset()

#grouping = '25ns'


#samples = ['data_em', 'data_tt', 'DYJets', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l']
#samples = ['data_em', 'data_tt', 'T-tW', 'Tbar-tW']# 'TT']
#samples = ['T-tW',]# 'Tbar-tW']# 'TT']
#samples = ['TT',]
#samples = ['data_em', 'data_tt', 'DYJets', 'Tbar-tW', 'T-tW', 'WJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l']
#samples = ['WJets',]
#samples = ['Tbar-tW',]
#samples = ['TTPow']
#samples = ['WZ3l1nu',]
#samples = ['DYJets',]

''' Cut configuration and location to save files: '''
### option 1 = Sync level cuts
#cutMapper = 'quickCutMapSync'
#cutName = 'BaseLine'

### option 2 = Signal level cuts
cutMapper = 'quickCutMapSingleCut'
cutName = 'PostSync'
#cutMapper = 'QCDYieldOS'
#cutName = 'QCDYield'
mid1 = '1oct12' 
mid2 = '2oct12'
mid3= '3oct12'
#mid3 = '3oct08QCD'

if bkgs != 'None' :
    cutMapper = bkgMap[ bkgs ][0]
    cutName = bkgMap[ bkgs ][0]


doCuts = True
doOrdering = True
#doPlots = True
#doCuts = False
#doOrdering = False
doPlots = False
numCores = 20

def doMP() :
    ''' Start multiprocessing tests '''
    #output = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes= numCores )
    multiprocessingOutputs = []
    
    num = 0
    for sample in samples :
    
        fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample) )
        go = True
        count = 0
        while go :
            for channel in channels :
    
                if channel == 'em' and sample == 'data_tt' : continue
                if channel == 'tt' and sample == 'data_em' : continue
                print " ====>  Adding %s_%s_%i_%s  <==== " % (grouping, sample, count, channel)
    
                multiprocessingOutputs.append( pool.apply_async(runCode, args=(grouping, sample, channel, count, num)) )
                num +=  1
    
            count += 1
            
            # Make sure we look over large samples to get all files
            if count * numFilesPerCycle >= fileLen : go = False
    
    
    mpResults = [p.get() for p in multiprocessingOutputs]
    
    #print(mpResults)
    print "#################################################################"
    print "###               Finished, summary below                     ###"
    print "#################################################################"
    
    print "\nStart Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
    print "\n"
    
    print " --- CutTable used: %s" % cutMapper
    print " --- Cut used: %s" % cutName
    print " --- Grouping: %s" % grouping
    print " --- Cut folder: %s%s" % (grouping, mid1)
    print " --- Iso folder: %s%s" % (grouping, mid2)
    print " --- Hist folder: %s%s" % (grouping, mid3)
    print " --- do Cuts? %s" % doCuts
    print " --- do Iso/Ordering? %s" % doOrdering
    print " --- do Histos? %s" % doPlots
    print "\n"
    
    mpResults.sort()
    for item in mpResults :
        print "%5s %10s %5s count %s:" % (item[0], item[1], item[2], item[3])
        print item[4]
        print item[5]
        print item[6]
    
    print "Start Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )

def drawHistos() : 
    ''' Start PROOF multiprocessing Draw '''
    ROOT.TProof.Open('workers=%s' % str(numCores/2) )
    gROOT.SetBatch(True)
    
    for sample in samples :
    
        fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample) )
        print "File len: %i" % fileLen
        numIters = int( math.ceil( fileLen / numFilesPerCycle ) )
        print "Num Iters: %i" % numIters
    
        for channel in channels :
    
            if channel == 'em' and sample == 'data_tt' : continue
            if channel == 'tt' and sample == 'data_em' : continue
            print " ====>  Starting Plots For %s_%s_%s  <==== " % (grouping, sample, channel)
    
            chain = ROOT.TChain('Ntuple')
            if bkgs != 'None' :
                outFile = ROOT.TFile('meta/%sBackgrounds/%s/shape/%s_%s.root' % (grouping, bkgMap[ bkgs ][0], sample.split('_')[0], channel), 'RECREATE')
                for i in range( numIters+1 ) :
                    print "%s_%i" % ( sample, i)
                    chain.Add('meta/%sBackgrounds/%s/iso/%s_%i_%s.root' % (grouping, bkgMap[ bkgs ][0], sample.split('_')[0], i, channel) )
            else :
                outFile = ROOT.TFile('%s%s/%s_%s.root' % (grouping, mid3, sample.split('_')[0], channel), 'RECREATE')
                for i in range( numIters+1 ) :
                    print "%s_%i" % ( sample, i)
                    chain.Add('%s%s/%s_%i_%s.root' % (grouping, mid2, sample.split('_')[0], i, channel) )
            analysisPlots.plotHistosProof( outFile, chain, channel )
            outFile.Close()
        
#drawHistos()
doMP()
