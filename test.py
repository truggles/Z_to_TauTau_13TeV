from util.buildTChain import makeTChain

path = 'em/final/Ntuple'
sampleList = 'meta/NtupleInputs/QCD.txt'

tree1 = makeTChain( sampleList, path )
print tree1.GetEntries('1')
path = 'tt/final/Ntuple'
tree2 = makeTChain( sampleList, path )
print tree2.GetEntries('1')

tree2.SaveAs('tt.root')
