from util.buildTChain import makeTChain
import ROOT
from array import array
#from ROOT import TProof
from time import gmtime, strftime
import cutsBaseSelection as bc # "Base Cuts"

begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print begin

ROOT.gROOT.Reset()


#channels = {'em' : ( ['e', 'm'],
#					 ['abs(e_m_Mass-90) < 30', 'e_m_SS == 0', 'ePt > 20', 'abs(eEta) < 2.3', 'mPt > 10', 'abs(mEta) < 2.1', 'ePVDZ < 0.2', 'ePVDXY < 0.045', 'mPVDZ < 0.2', 'mPVDXY < 0.045', 'eRelPFIsoDB < 0.15', 'mRelPFIsoDBDefault < 0.15', 'mIsGlobal == 1', 'mNormTrkChi2 < 3.0' ] ),
#		    'tt' : ( ['t1', 't2'],
#					 ['abs(t1_t2_Mass-90) < 30', 't1_t2_SS == 0', 't1Pt > 40', 'abs(t1Eta) < 2.1', 't2Pt > 40', 'abs(t2Eta) < 2.1', 't1AgainstElectronVLooseMVA5 > 0.5', 't1AgainstMuonLoose3 > 0.5', 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0', 't2AgainstElectronVLooseMVA5 > 0.5', 't2AgainstMuonLoose3 > 0.5', 't2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0' ] )
#}
channels = {'em' : (['e', 'm'], ['abs(e_m_Mass-90) < 30']),
		    'tt' : (['t1', 't2'], ['abs(t1_t2_Mass-90) < 30'])
}

#samples = ['DYJets', 'TT', 'TTJets', 'QCD', 'Tbar_tW', 'T_tW', 'HtoTauTau', 'VBF_HtoTauTau', 'WJets', 'WW', 'WZJets']
samples = ['HtoTauTau', 'WZJets']

#ROOT.TProof.Open('workers=6')
#for sample in samples :
sample = 'HtoTauTau'
print "###   %s   ###" % sample

# Start fresh ROOT session with Proof
#ROOT.gROOT.Reset()
#proof = ROOT.gProof

outFile = ROOT.TFile('baseSelectionRoot/%s.root' % sample, 'RECREATE')
# Try adding a branch
#file2 = ROOT.TFile('%s_fr.root' % sample, 'RECREATE')

for channel in channels.keys() :
	print "Channel:  %s" % channel
	if channel == 'em': zProd = ['e', 'm']
	if channel == 'tt': zProd = ['t1', 't2']
	path = '%s/final/Ntuple' % channel
	sampleList = 'meta/NtupleInputs/%s.txt' % sample
	
	#chain = ROOT.TChain( path )
	#chain.SetProof(True)
	#files = open( sampleList, 'r' )	


	chain = makeTChain( sampleList, path )
	#chain.SetProof( True )

	numEntries = chain.GetEntries()
	print numEntries
	
	''' Copy and make some cuts while doing it '''
	#print ROOT.TString("&&".join( channels[ channel ][1] ) )
	#outTree = chain.CopyTree("&&".join( channels[ channel ][1] ) )
	treeOutDir = outFile.mkdir( path.split('/')[0] )
	tree1 = bc.makeZCut( chain, channels[ channel ][0][0], channels[ channel ][0][1] )
	treeOutDir.cd()
	tree1.Write()
	numEntries = tree1.GetEntries()
	print numEntries

	# Making cut histos
	cutName = "ZMass"
	cutDir = outFile.mkdir( "%s_%s" % ( channel, cutName ) )
	cutDir.cd()

	varMap = {
		'Z_Pt' : ('%s_%s_Pt' % (channels[ channel ][0][0], channels[ channel ][0][1]), 500, 0, 500),
		'Z_Mass' : ('%s_%s_Mass' % (channels[ channel ][0][0], channels[ channel ][0][1]), 80, 50, 130),
		'Z_SS' : ('%s_%s_SS' % (channels[ channel ][0][0], channels[ channel ][0][1]), 21, -1, 1),
		'LT' : ('LT', 500, 0, 500),
		'Mt' : ('Mt', 500, 0, 500),
		'pfMetEt' : ('pfMetEt', 500, 0, 500),
		'bjetCISVVeto20' : ('bjetCISVVeto20', 60, 0, 5),
		'jetVeto30' : ('jetVeto30', 100, 0, 10),
		'l1_Pt' : ('%sPt' % channels[ channel ][0][0], 500, 0, 500),
		'l1_Eta' : ('%sEta' % channels[ channel ][0][0], 101, -5, 5),
		#'l1_RelPFIsoDB' : ('%sRelPFIsoDB' % channels[ channel ][0][0], 100, 0, 100),
		'l2_Pt' : ('%sPt' % channels[ channel ][0][1], 500, 0, 500),
		'l2_Eta' : ('%sEta' % channels[ channel ][0][1], 101, -5, 5),
		#'l2_RelPFIsoDB' : ('%sRelPFIsoDB' % channels[ channel ][0][2], 100, 0, 100),
}

	for cn, cv in varMap.iteritems() :
		#print cn
		#print cv
		hist = bc.makeHisto( tree1, sample, channel, cn, cv[0], cv[1], cv[2], cv[3] )
		hist.Write()
	
	# New
	#chain.SetProof(0)

	# Make a channel specific directory and write the tree to it
outFile.Write()
outFile.Close()

#dZCut( sample, 'em' )
print "Start Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
