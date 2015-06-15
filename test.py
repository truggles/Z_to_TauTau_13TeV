from util.buildTChain import makeTChain
import ROOT

ROOT.gROOT.Reset()

maxT = ROOT.TTree().GetMaxTreeSize()
#print "max tree size: %i" % maxT
#ROOT.TTree().SetMaxTreeSize( 1000000000000 )
#maxT = ROOT.TTree().GetMaxTreeSize()
#print "max tree size: %i" % maxT

#channel = 'em'
channels = {'em' : ['ePt > 20', 'abs(eEta) < 2.3', 'mPt > 10', 'abs(mEta) < 2.1', 'abs(e_m_Mass-90) < 30'],
		    'tt' : ['t1Pt > 45', 'abs(t1Eta) < 2.1', 't2Pt > 45', 'abs(t2Eta) < 2.1', 'abs(t1_t2_Mass-90) < 30']
}

sample = 'QCD'


outFile = ROOT.TFile('%s.root' % sample, 'RECREATE')

for channel in channels.keys() :
	path = '%s/final/Ntuple' % channel
	sampleList = 'meta/NtupleInputs/%s.txt' % sample
	
	chain = makeTChain( sampleList, path )
	numEntries = chain.GetEntries('1')
	
	print numEntries
	#tree1.ls()
	
	outDir = outFile.mkdir( path.split('/')[0] )
	outDir.cd()
	outTree = chain.CopyTree("&&".join( channels[ channel ] ) )
	print outTree.GetEntries('1')

outFile.Write()
outFile.Close()


