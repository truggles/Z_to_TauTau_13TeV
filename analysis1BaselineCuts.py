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

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='25ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--bkgs', action='store', default='None', dest='bkgs', help="Run a specific background with specific cuts?")
results = p.parse_args()
grouping = results.sampleName
bkgs = results.bkgs

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
#Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar_tW', 'T_tW', 'WJets', 'TTJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'WZ3l1nu', 'ZZ', 'ZZ4l', 'TTPow', 'TT']
Samples25nsQCD = ['QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']

Samples25ns = ['data_em', 'data_tt', 'DYJets', 'Tbar_tW', 'T_tW', 'WJets', 'TT', 'WW', 'WZJets', 'ZZ'] # Intended good one

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

def runCode(grouping, sample, channel, count, output) :
    if channel == 'em' and sample == 'data_tt' : return
    if channel == 'tt' and sample == 'data_em' : return

    #if sample == 'TT' : save = '%s_%i_%s' % (sample, count, channel)
    #elif 'data' in sample : save = sample
    if 'data' in sample : save = 'data_%i_%s' % (count, channel)
    #else : save = '%s_%s' % (sample, channel)
    else : save = '%s_%i_%s' % (sample, count, channel)
    #print "save",save
    output.put("save %s" % save )

    ''' 1. Make cuts and save '''
    if doCuts :
        if bkgs != 'None' :
            outFile1 = ROOT.TFile('meta/%sBackgrounds/%s/cut/%s.root' % (grouping, bkgMap[ bkgs ][0], save), 'RECREATE')
        else :
            outFile1 = makeFile( grouping, mid1, save)
        outputs = initialCut( outFile1, grouping, sample, channel, cutMapper, cutName, count * maxTTfiles, (count + 1) * maxTTfiles-1 )
        dir1 = outputs[0].mkdir( channel )
        dir1.cd()
        outputs[1].Write()
        outFile1.Close()

    ''' 2. Rename branches, Tau and Iso order legs '''
    if doOrdering :
        renameBranches( grouping, mid1, mid2, save, channel, bkgMap[ bkgs ][0])
        #print '%s%s/%s.root' % (grouping, mid2, save)
        output.put( '%s%s/%s.root' % (grouping, mid2, save) )

    ''' 3. Make the histos '''
    if doPlots :
        if bkgs != 'None' :
            outFile2 = ROOT.TFile('meta/%sBackgrounds/%s/iso/%s.root' % (grouping, bkgMap[ bkgs ][0], save), 'READ')
            outFile3 = ROOT.TFile('meta/%sBackgrounds/%s/shape/%s.root' % (grouping, bkgMap[ bkgs ][0], save), 'RECREATE')
        else :
            outFile2 = ROOT.TFile('%s%s/%s.root' % (grouping, mid2, save), 'READ')
            outFile3 = makeFile( grouping, mid3, save)
        #ifile = ROOT.TFile('%s%s/%s.root' % (grouping, mid2, save), 'r')
        #tree = ifile.Get('Ntuple')
        tree = outFile2.Get('Ntuple')

        plotHistos( outFile3, tree, channel )
        outFile2.Close()
        outFile3.Close()

begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print begin
ROOT.gROOT.Reset()

#grouping = '25ns'


#samples = ['data_em', 'data_tt', 'DYJets', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l']
#samples = ['data_em', 'data_tt',]# 'T_tW', 'Tbar_tW']# 'TT']
#samples = ['T_tW',]# 'Tbar_tW']# 'TT']
#samples = ['TT',]
#samples = ['data_em', 'data_tt', 'DYJets', 'Tbar_tW', 'T_tW', 'WJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l']
#samples = ['WJets',]
#samples = ['Tbar_tW',]
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
mid1 = '1oct08mp' 
mid2 = '2oct08mp'
mid3= 'xxx'
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

''' Start multiprocessing tests '''
output = multiprocessing.Queue()

w = 0
processes = []
for sample in samples :
    #if sample == 'TT' : continue
    fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample) )
    go = True
    count = 0
    while go :
        print " ====>  Loop Count %i  <==== " % count
        for channel in channels :

            processes.append(multiprocessing.Process(target=runCode, args=(grouping, sample, channel, count, output)) )
            w +=  1
            #if j > 10 : break

        count += 1
        #if sample != 'TT' : go = False
        if count * maxTTfiles >= fileLen : go = False

for p in processes :
    p.start()

for p in processes :
    p.join()

mpResults = [output.get() for p in processes]

print(mpResults)

print "Start Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
