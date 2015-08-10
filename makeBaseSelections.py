from util.buildTChain import makeTChain
import ROOT
from array import array
from time import gmtime, strftime
import cutsBaseSelection as bc
import argparse

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='50ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--qcd', action='store', default=False, dest='qcd', help="Should we only run over QCD and Data?")
p.add_argument('--invert', action='store', default=False, dest='invert', help="Invert data Isolation values to model QCD?")
p.add_argument('--weight', action='store', default=True, dest='applyWeights', help="Apply GenWeight to mc samples?")
p.add_argument('--singleCut', action='store', default=True, dest='cuts', help="Single cut?")
results = p.parse_args()
pre_ = results.sampleName
qcd = results.qcd
invert = results.invert
applyWeights = results.applyWeights
singleCut = results.cuts

print "Single Cut == %s" % singleCut
print "Running over %s samples" % pre_

''' Configuration '''
weight = 1
skipMiddlePlots = True
#skipMiddlePlots = False
#justShape = True
justShape = False

if justShape :
	maxEvents = 100000
elif not justShape :
	maxEvents = 0

if skipMiddlePlots :
	maxFiles = 0
elif not skipMiddlePlots :
#	maxFiles = 21
	maxFiles = 0

begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print begin

ROOT.gROOT.Reset()
channels = ['em', 'tt']

''' Preset samples '''
SamplesSync = ['Sync_HtoTT']
Samples50ns = ['data_em', 'data_tt', 'DYJets', 'Tbar_tW', 'T_tW', 'WJets', 'TTJets', 'WW', 'WW2l2n', 'WW4q', 'WW1l1n2q', 'WZJets', 'WZ1l1n2q', 'ZZ', 'ZZ4l', 'TT', 'QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']
#Samples50ns = ['data_em', 'data_tt', 'DYJets', 'Tbar_tW', 'T_tW', 'WJets', 'TTJets', 'WW', 'WZJets', 'ZZ', 'TT', 'QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']
SamplesQCDData = ['data_em', 'data_tt', 'QCD15-20', 'QCD20-30', 'QCD30-50', 'QCD50-80', 'QCD80-120', 'QCD120-170', 'QCD170-300', 'QCD300-Inf']
SamplesData = ['data_em', 'data_tt']
#Samples25ns = ['DYJets', 'QCD', 'Tbar_tW', 'T_tW', 'HtoTauTau', 'VBF_HtoTauTau', 'WJets', 'TTJets', 'WW', 'WZJets', 'ZZ']
Samples25ns = ['HtoTauTau', 'VBF_HtoTauTau']

if pre_ == 'Sync' : samples = SamplesSync
if pre_ == '50ns' :
    if qcd : samples = SamplesQCDData
    elif invert : samples = SamplesData
    else : samples = Samples50ns
if pre_ == '25ns' : samples = Samples25ns



for sample in samples :
#	if skipMiddlePlots == False and sample != 'QCD' : continue
    print "###   %s   ###" % sample
    if skipMiddlePlots :
        if qcd :
            outFile = ROOT.TFile('%sQCD/%s.root' % (pre_, sample), 'RECREATE')
        elif invert :
            outFile = ROOT.TFile('%sInvert/%s.root' % (pre_, sample), 'RECREATE')
        else :
            outFile = ROOT.TFile('%sBaseRootsQuick/%s.root' % (pre_, sample), 'RECREATE')
    elif not skipMiddlePlots :
    	outFile = ROOT.TFile('%sBaseRoots/%s.root' % (pre_, sample), 'RECREATE')
    
    for channel in channels :
        print "Channel:  %s" % channel
        if channel == 'em':
            zProd = ['e', 'm']
            varMap = bc.getEMHistoDict()
        if channel == 'tt':
            zProd = ['t1', 't2']
            varMap = bc.getTTHistoDict()
        l1 = zProd[0]
        l2 = zProd[1]
        
        genVar = bc.getGeneralHistoDict()
        if 'HtoTauTau' in sample :
        	genVar = bc.getGeneralHistoDictPhys14()
        newVarMap = genVar
        for var, details in varMap.iteritems() :
        	newVarMap[ var ] = details
        	#print var, details
        #for var, name in genVar.iteritems() :
        #	newVarMap[ var ] = details
        #	print var, details
        #print newVarMap
        
        
        ''' Get initial chain '''
        path = '%s/final/Ntuple' % channel
        sampleList = 'meta/NtupleInputs_%s/%s.txt' % (pre_, sample)
        chain = makeTChain( sampleList, path, maxFiles )
        numEntries = chain.GetEntries()
        print "%25s : %10i" % ('Initial', numEntries)
        treeOutDir = outFile.mkdir( path.split('/')[0] )
        
        
        ''' Make a set of Initial Conditions plots '''
        if not skipMiddlePlots :
            initialHistosDir = outFile.mkdir( "%s_Initial" % channel )
            initialHistosDir.cd()
            ''' Combine Gen and Chan specific into one fill section '''
            histos = {}
            for var, cv in newVarMap.iteritems() :
            	histos[ var ] = bc.makeHisto( var, cv[1], cv[2], cv[3])
            #print "Initial:"
            #print histos
            
            eventSet = set()
            evtNum = 0
            for i in range( chain.GetEntries() ):
                evtNum += 1
                chain.GetEntry( i )
                
                # Apply Generator weights, speficially for DY Jets
                if applyWeights : 
                    if chain.GenWeight >= 0 : weight = 1
                    if chain.GenWeight < 0 : weight = -1
                else : weight = 1
                
                eventTup = ( chain.run, chain.lumi, chain.evt )
                if eventTup not in eventSet :
                    for var, histo in histos.iteritems() :
                        num = getattr( chain, newVarMap[ var ][0] )
                        histo.Fill( num, weight )
                    eventSet.add( eventTup )
                if evtNum == maxEvents :
                	break
            for var, histo in histos.iteritems() :
            	histo.Write()
        
        
        
        ''' Get channel specific general cuts '''
        if qcd and skipMiddlePlots :
            cutMap = bc.getCutMapQuickQCD( channel ) 
            if 'data' in sample :
                cutMap = bc.quickCutMapDataSS( channel ) 
        elif invert == True :
            cutMap = bc.quickCutMapDataInversion( channel )
        elif pre_ == 'Sync' :
            cutMap = bc.quickCutMapSync( channel )
        elif singleCut == True :
            cutMap = bc.quickCutMapSingleCut( channel )
        elif 'HtoTauTau' in sample and skipMiddlePlots :
        	cutMap = bc.quickCutMapPhys14( channel )
        elif 'HtoTauTau' in sample and not skipMiddlePlots :
        	cutMap = bc.getCutMapPhys14( channel )
        elif skipMiddlePlots :
        	cutMap = bc.quickCutMap( channel )
        elif not skipMiddlePlots :
        	cutMap = bc.getCutMap( channel )
        #print cutMap
        
        lenCutMap = len( cutMap )
        count = 0
        for cutName, cutString in cutMap.items() :
            	
            ''' Copy and make some cuts while doing it '''
            ROOT.gROOT.cd() # This makes copied TTrees get written to general ROOT, not our TFile
            
            ''' This count thing is so we don't have to copy TTrees extra times '''
            count += 1
            #print "count: %i" % count
            #print "Starting Cut!"
            if count % 2 == 1 :
            	chainNew = bc.makeGenCut( chain, cutString )
            	numEntries = chainNew.GetEntries()
            if count % 2 == 0 :
            	chain = bc.makeGenCut( chainNew, cutString )
            	numEntries = chain.GetEntries()
            #print "Finishing Cut!"
            print "%25s : %10i" % (cutName, numEntries)
            
            ''' Making cut histos '''
            cutDir = outFile.mkdir( "%s_%s" % ( channel, cutName ) )
            cutDir.cd()
            
            ''' Combine Gen and Chan specific into one fill section '''
            histos = {}
            for var, cv in newVarMap.iteritems() :
            	histos[ var ] = bc.makeHisto( var, cv[1], cv[2], cv[3])
            #print "Combined Gen and Chan:"
            #print histos
            
            if count % 2 == 0 :
            	eventSet = set()
            	evtNum = 0
            	for i in range( chain.GetEntries() ):
                    evtNum += 1
                    chain.GetEntry( i )
            
                    # Apply Generator weights, speficially for DY Jets
                    if applyWeights : 
                        if chain.GenWeight >= 0 : weight = 1
                        if chain.GenWeight < 0 : weight = -1
                    else : weight = 1
            
                    eventTup = ( chain.run, chain.lumi, chain.evt )
                    if eventTup not in eventSet :
                    	for var, histo in histos.iteritems() :
                            num = getattr( chain, newVarMap[ var ][0] )
                            histo.Fill( num, weight )
                    	eventSet.add( eventTup )
                    if evtNum == maxEvents : 
                    	break
            	for var, histo in histos.iteritems() :
            		histo.Write()
            
            if count % 2 == 1 :
            	eventSet = set()
            	evtNum = 0
            	for i in range( chainNew.GetEntries() ):
                    evtNum += 1
                    chainNew.GetEntry( i )
            
                    # Apply Generator weights, speficially for DY Jets
                    if applyWeights : 
                        if chain.GenWeight >= 0 : weight = 1
                        if chain.GenWeight < 0 : weight = -1
                    else : weight = 1
            
                    eventTup = ( chainNew.run, chainNew.lumi, chainNew.evt )
                    if eventTup not in eventSet :
                        for var, histo in histos.iteritems() :
                            num = getattr( chainNew, newVarMap[ var ][0] )
                            histo.Fill( num, weight )
                        eventSet.add( eventTup )
                    if evtNum == maxEvents :
                    	break
            	for var, histo in histos.iteritems() :
            		histo.Write()
            
            if count == lenCutMap : continue
            elif count % 2 == 1 :
            	chain.IsA().Destructor( chain )
            elif count % 2 == 0 :
            	chainNew.IsA().Destructor( chainNew )
            #print "repeat!"
        
        treeOutDir.cd()
        if count % 2 == 1 :
        	chainNew.Write()
        if count % 2 == 0 :
        	chain.Write()

outFile.Write()
outFile.Close()

print "Start Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
