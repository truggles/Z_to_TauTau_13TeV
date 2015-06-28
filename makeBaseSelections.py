from util.buildTChain import makeTChain
import ROOT
from array import array
from time import gmtime, strftime
import cutsBaseSelection as bc

# Configuration
skipMiddlePlots = True
#skipMiddlePlots = False

if skipMiddlePlots :
	maxFiles = 0
elif not skipMiddlePlots :
	maxFiles = 21

begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print begin

ROOT.gROOT.Reset()
channels = ['em', 'tt']
#samples = ['DYJets', 'TT', 'TTJets', 'QCD', 'Tbar_tW', 'T_tW', 'HtoTauTau', 'VBF_HtoTauTau', 'WJets', 'WW', 'WZJets']
samples = ['DYJets', 'QCD', 'Tbar_tW', 'T_tW', 'HtoTauTau', 'VBF_HtoTauTau', 'WJets', 'TT', 'TTJets', 'WW', 'WZJets']
#samples = ['HtoTauTau', 'WZJets']

for sample in samples :
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
			genVarMap = bc.getGeneralHistoDict()
			for cn, cv in genVarMap.iteritems() :
				hist = bc.makeHisto( chain, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
				hist.Write()
			if channel == 'em' :
				chanVarMap = bc.getEMHistoDict()
			if channel == 'tt' :
				chanVarMap = bc.getTTHistoDict()
			for cn, cv in chanVarMap.iteritems() :
				hist = bc.makeHisto( chain, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
				hist.Write()
		
		
		''' Get channel specific general cuts '''
		if skipMiddlePlots :
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
			if count % 2 == 1 :
				chainNew = bc.makeGenCut( chain, cutString )
				numEntries = chainNew.GetEntries()
			if count % 2 == 0 :
				chain = bc.makeGenCut( chainNew, cutString )
				numEntries = chain.GetEntries()
			print "%25s : %10i" % (cutName, numEntries)
	
			''' Making cut histos '''
			cutDir = outFile.mkdir( "%s_%s" % ( channel, cutName ) )
			cutDir.cd()
	
			''' Fill histos of general variables '''
			genVarMap = bc.getGeneralHistoDict()
			for cn, cv in genVarMap.iteritems() :
				if count % 2 == 1 :
					hist = bc.makeHisto( chainNew, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
				if count % 2 == 0 :
					hist = bc.makeHisto( chain, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
				hist.Write()
	
			''' Fill channel specific histos '''
			if channel == 'em' :
				chanVarMap = bc.getEMHistoDict()
			if channel == 'tt' :
				chanVarMap = bc.getTTHistoDict()
			for cn, cv in chanVarMap.iteritems() :
				if count % 2 == 1 :
					hist = bc.makeHisto( chainNew, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
				if count % 2 == 0 :
					hist = bc.makeHisto( chain, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
				hist.Write()
	
			if count == lenCutMap : continue
			elif count % 2 == 1 :
				chain.IsA().Destructor( chain )
			elif count % 2 == 0 :
				chainNew.IsA().Destructor( chainNew )
		
		treeOutDir.cd()
		if count % 2 == 1 :
			chain.Write()
		if count % 2 == 0 :
			chainNew.Write()
	
	outFile.Write()
	outFile.Close()

print "Start Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
