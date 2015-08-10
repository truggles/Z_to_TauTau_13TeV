
############################################################################
#   Creates flag variables for whether or not an event passes a signal cut #
############################################################################

import ROOT
from array import array



def dZCut( sample, channel ) :
	if channel == 'em': zProd = ['e', 'm']
	if channel == 'tt': zProd = ['t1', 't2']
	#treeFile = ROOT.TFile('baseSelectionRoot/%s.root' % sample, 'update')
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
