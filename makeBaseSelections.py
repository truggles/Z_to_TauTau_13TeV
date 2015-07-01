from util.buildTChain import makeTChain
import ROOT
from array import array
from time import gmtime, strftime
import cutsBaseSelection as bc

# Configuration
#skipMiddlePlots = True
skipMiddlePlots = False
#justShape = True
justShape = False
#qcd = True
qcd = False

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
#samples = ['DYJets', 'TT', 'TTJets', 'QCD', 'Tbar_tW', 'T_tW', 'HtoTauTau', 'VBF_HtoTauTau', 'WJets', 'WW', 'WZJets', 'ZZ']
samples = ['DYJets', 'QCD', 'Tbar_tW', 'T_tW', 'HtoTauTau', 'VBF_HtoTauTau', 'WJets', 'TTJets', 'WW', 'WZJets', 'ZZ']#, 'TT']
#samples = ['DYJets', 'QCD', 'Tbar_tW', 'T_tW', 'WJets', 'TTJets', 'WW', 'WZJets', 'ZZ']#, 'TT']
samples = ['HtoTauTau', 'VBF_HtoTauTau']
#samples = ['HtoTauTau', 'T_tW']

for sample in samples :
#	if skipMiddlePlots == False and sample != 'QCD' : continue
#sample = 'HtoTauTau'
	print "###   %s   ###" % sample
	if skipMiddlePlots :
		outFile = ROOT.TFile('baseSelectionRootQuick/%s.root' % sample, 'RECREATE')
	elif not skipMiddlePlots :
		outFile = ROOT.TFile('baseSelectionRoot/%s.root' % sample, 'RECREATE')
	
	for channel in channels :
		print "Channel:  %s" % channel
		if channel == 'em': zProd = ['e', 'm']
		if channel == 'tt': zProd = ['t1', 't2']
		l1 = zProd[0]
		l2 = zProd[1]
		
		if channel == 'em': varMap = bc.getEMHistoDict()
		if channel == 'tt': varMap = bc.getTTHistoDict()
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
		sampleList = 'meta/NtupleInputs/%s.txt' % sample
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
				eventTup = ( chain.run, chain.lumi, chain.evt )
				if eventTup not in eventSet :
					for var, histo in histos.iteritems() :
						num = getattr( chain, newVarMap[ var ][0] )
						histo.Fill( num )
					eventSet.add( eventTup )
				if evtNum == maxEvents :
					break
			for var, histo in histos.iteritems() :
				histo.Write()
			
		
		
		''' Get channel specific general cuts '''
		if qcd and skipMiddlePlots :
			cutMap = bc.getCutMapQuickQCD( channel ) 
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
					eventTup = ( chain.run, chain.lumi, chain.evt )
					if eventTup not in eventSet :
						for var, histo in histos.iteritems() :
							num = getattr( chain, newVarMap[ var ][0] )
							histo.Fill( num )
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
					eventTup = ( chainNew.run, chainNew.lumi, chainNew.evt )
					if eventTup not in eventSet :
						for var, histo in histos.iteritems() :
							num = getattr( chainNew, newVarMap[ var ][0] )
							histo.Fill( num )
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
