from util.buildTChain import makeTChain
import ROOT
from array import array

ROOT.gROOT.Reset()

maxT = ROOT.TTree().GetMaxTreeSize()

#channel = 'em'
channels = {'em' : ['ePt > 20', 'abs(eEta) < 2.3', 'mPt > 10', 'abs(mEta) < 2.1', 'abs(e_m_Mass-90) < 30'],
		    'tt' : ['t1Pt > 45', 'abs(t1Eta) < 2.1', 't2Pt > 45', 'abs(t2Eta) < 2.1', 'abs(t1_t2_Mass-90) < 30']
}

sample = 'QCD'


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
	outTree = chain.CopyTree("&&".join( channels[ channel ] ) )
	numEntries = outTree.GetEntries('1')
	print numEntries

	# Make a channel specific directory and write the tree to it
	outDir = outFile.mkdir( path.split('/')[0] )
	outDir.cd()
	outTree.Write()

	# Make a channel specific directory and cd() to it for future writting
#	outDir2 = file2.mkdir( path.split('/')[0] )
#	outDir2.cd()
#	tree2 = ROOT.TTree('treeFriend', 'a friend tree')
	dzCutTight = array('i', [ 0 ] )
	dzCutB = outTree.Branch('dzCutTight', dzCutTight, 'dzCutTight/I')

#	for row in outTree :
	for i in range( outTree.GetEntries() ):
		outTree.GetEntry( i )
		#if abs( getattr(i, '%s_%s_Mass' % (zProd[0], zProd[1]) ) - 90 ) < 10:
		dzCutTight[0] = 1
			#print "1 : %f" % row.Mass
		#else:
		#	dzCutTight[0] = 0
			#print "0 : %f" % row.Mass
		dzCutB.Fill()

#	count2 = 0
#	for row2 in tree2 :
#		setattr( row2, "dzCutTight", dzCutTight[ count2 ] )
#		count2 += 1

#	tree2.Fill()
#	tree2.Write()


outFile.Write()
outFile.Close()


