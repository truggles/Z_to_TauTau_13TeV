from util.buildTChain import makeTChain
import ROOT

ROOT.gROOT.Reset()

maxT = ROOT.TTree().GetMaxTreeSize()
#print "max tree size: %i" % maxT
#ROOT.TTree().SetMaxTreeSize( 1000000000000 )
#maxT = ROOT.TTree().GetMaxTreeSize()
#print "max tree size: %i" % maxT

#channel = 'em'
channel = 'em'
sample = 'QCD'

path = '%s/final/Ntuple' % channel
sampleList = 'meta/NtupleInputs/%s.txt' % sample

chain = makeTChain( sampleList, path )
numEntries = chain.GetEntries('1')

print numEntries
#tree1.ls()

outFile = ROOT.TFile('%s.root' % sample, 'RECREATE')
outDir = outFile.mkdir( path.split('/')[0] )
outDir.cd()
outTree = chain.CopyTree(" Eta > 3 ")
print outTree.GetEntries('1')

outFile.Write()
outFile.Close()


