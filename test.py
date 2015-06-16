from util.buildTChain import makeTChain
import ROOT
from array import array

ROOT.gROOT.Reset()

def dZCut( sample, channel ) :
	if channel == 'em': zProd = ['e', 'm']
	if channel == 'tt': zProd = ['t1', 't2']
	treeFile = ROOT.TFile('%s.root' % sample, 'update')
	dir_ = treeFile.Get( '%s' % channel )	
	tree = dir_.Get( 'Ntuple' )

	# Make a channel specific directory and cd() to it for future writting
	dzCutTight = array('i', [ 0 ] )
	dzCutB = tree.Branch('dzCutTight', dzCutTight, 'dzCutTight/I')

	treeFile.cd( '%s' % channel )
#	for row in outTree :
	for i in range( tree.GetEntries() ):
		tree.GetEntry( i )
		if abs( getattr(tree, '%s_%s_Mass' % (zProd[0], zProd[1]) ) - 90 ) < 10:
			dzCutTight[0] = 1
		else:
			dzCutTight[0] = 0
		dzCutB.Fill()
	tree.Write('', ROOT.TObject.kOverwrite)

channels = {'em' : ( ['e', 'm'],
					 ['abs(e_m_Mass-90) < 30', 'e_m_SS == 0', 'ePt > 20', 'abs(eEta) < 2.3', 'mPt > 10', 'abs(mEta) < 2.1', 'ePVDZ < 0.2', 'ePVDXY < 0.045', 'mPVDZ < 0.2', 'mPVDXY < 0.045', 'eRelPFIsoDB < 0.15', 'mRelPFIsoDBDefault < 0.15', 'mIsGlobal == 1', 'mNormTrkChi2 < 3.0' ] ),
		    'tt' : ( ['t1', 't2'],
					 ['abs(t1_t2_Mass-90) < 30', 't1_t2_SS == 0', 't1Pt > 40', 'abs(t1Eta) < 2.1', 't2Pt > 40', 'abs(t2Eta) < 2.1', 't1AgainstElectronVLooseMVA5 > 0.5', 't1AgainstMuonLoose3 > 0.5', 't1ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0', 't2AgainstElectronVLooseMVA5 > 0.5', 't2AgainstMuonLoose3 > 0.5', 't2ByCombinedIsolationDeltaBetaCorrRaw3Hits < 1.0' ] )
}
#channels = {'em' : ['abs(e_m_Mass-90) < 30'],
#		    'tt' : ['abs(t1_t2_Mass-90) < 30']
#}

sample = 'DYJets'

outFile = ROOT.TFile('%s.root' % sample, 'RECREATE')
# Try adding a branch
#file2 = ROOT.TFile('%s_fr.root' % sample, 'RECREATE')

for channel in channels.keys() :
	if channel == 'em': zProd = ['e', 'm']
	if channel == 'tt': zProd = ['t1', 't2']
	path = '%s/final/Ntuple' % channel
	sampleList = 'meta/NtupleInputs/%s.txt' % sample
	
	chain = makeTChain( sampleList, path )
	numEntries = chain.GetEntries('1')
	print numEntries
	
	# Copy and make some cuts while doing it
	#print ROOT.TString("&&".join( channels[ channel ][1] ) )
	outTree = chain.CopyTree("&&".join( channels[ channel ][1] ) )
	numEntries = outTree.GetEntries('1')
	print numEntries

	# Make a channel specific directory and write the tree to it
	outDir = outFile.mkdir( path.split('/')[0] )
	outDir.cd()
	outTree.Write()
outFile.Write()
outFile.Close()

#dZCut( sample, 'em' )

