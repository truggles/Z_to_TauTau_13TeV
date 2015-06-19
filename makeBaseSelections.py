from util.buildTChain import makeTChain
import ROOT
from array import array
#from ROOT import TProof
from time import gmtime, strftime
import cutsBaseSelection as bc # "Base Cuts"

begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print begin

ROOT.gROOT.Reset()
#channels = {'em' : (['e', 'm'], ['abs(e_m_Mass-90) < 30']),
#		    'tt' : (['t1', 't2'], ['abs(t1_t2_Mass-90) < 30'])
#}
channels = ['em', 'tt']
#samples = ['DYJets', 'TT', 'TTJets', 'QCD', 'Tbar_tW', 'T_tW', 'HtoTauTau', 'VBF_HtoTauTau', 'WJets', 'WW', 'WZJets']
samples = ['HtoTauTau', 'WZJets']

#ROOT.TProof.Open('workers=6')
#for sample in samples :
sample = 'HtoTauTau'
print "###   %s   ###" % sample
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
	chain = makeTChain( sampleList, path )
	numEntries = chain.GetEntries()
	print "%15s : %10i" % ('Initial', numEntries)
	
	''' Get channel specific general cuts '''
	cutMap = bc.getCutMap( channel, l1, l2 )
	#print cutMap
	treeOutDir = outFile.mkdir( path.split('/')[0] )

	lenCutMap = len( cutMap )
	count = 0
	for cutName, cutString in cutMap.items() :
			
		''' Copy and make some cuts while doing it '''
		ROOT.gROOT.cd()
		#treeOutDir.cd()

		''' This count thing is so we don't have to copy TTrees extra times '''
		count += 1
		#print "count: %i" % count
		if count % 2 == 1 :
			chainNew = bc.makeGenCut( chain, cutString )
			numEntries = chainNew.GetEntries()
		if count % 2 == 0 :
			chain = bc.makeGenCut( chainNew, cutString )
			numEntries = chain.GetEntries()
		print "%15s : %10i" % (cutName, numEntries)

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
