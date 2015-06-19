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
	#for cName, cString in cutMap.items() :
		
	''' Copy and make some cuts while doing it '''
	treeOutDir = outFile.mkdir( path.split('/')[0] )
	#tree1 = bc.makeZCut( chain, l1, l2 )
	tree1 = bc.makeGenCut( chain, cutMap[ 'ZMass' ] )
	treeOutDir.cd()
	numEntries = tree1.GetEntries()
	print "Z Cut: %10i" % numEntries

	# Making cut histos
	cutName = "ZMass"
	cutDir = outFile.mkdir( "%s_%s" % ( channel, cutName ) )
	cutDir.cd()

	''' Fill histos of general variables '''
	genVarMap = bc.getGeneralHistoDict()
	for cn, cv in genVarMap.iteritems() :
		hist = bc.makeHisto( tree1, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
		hist.Write()

	''' Fill EM specific histos '''
	if channel == 'em' :
		chanVarMap = bc.getEMHistoDict()
	if channel == 'tt' :
		chanVarMap = bc.getTTHistoDict()
	for cn, cv in chanVarMap.iteritems() :
		hist = bc.makeHisto( tree1, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
		hist.Write()

	cutName = "L1Pt"
	if channel == 'em': cutString = 'ePt > 50'
	if channel == 'tt': cutString = 't1Pt > 75'
	treeOutDir.cd()
	tree2 = bc.makeGenCut( tree1, cutString )
	numEntries = tree2.GetEntries()
	print "%s: %10i" % (cutName, numEntries)
	cutDir2 = outFile.mkdir( "%s_%s" % ( channel, cutName ) )
	cutDir2.cd()

	''' Fill histos of general variables '''
	genVarMap = bc.getGeneralHistoDict()
	for cn, cv in genVarMap.iteritems() :
		hist = bc.makeHisto( tree2, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
		hist.Write()

	''' Fill EM specific histos '''
	if channel == 'em' :
		chanVarMap = bc.getEMHistoDict()
	if channel == 'tt' :
		chanVarMap = bc.getTTHistoDict()
	for cn, cv in chanVarMap.iteritems() :
		hist = bc.makeHisto( tree2, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
		hist.Write()

outFile.Write()
outFile.Close()

print "Start Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
