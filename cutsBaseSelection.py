



import ROOT
from array import array

def makeZCut( chain, l1, l2 ) :
	print "l1 %s, l2 %s" % (l1, l2)
	outTree = chain.CopyTree( "abs( %s_%s_Mass - 90 ) < 30" % (l1, l2) )
	return outTree

def makeHistos( tree, sample, channel, cutName, var, varBins, varMin, varMax ) :
	name = "%s%s%s%s" % ( sample, channel, cutName, var )
	hist = ROOT.TH1F( name, name, varBins, varMin, varMax )

	for i in range( tree.GetEntries() ):
		tree.GetEntry( i )
		if channel == 'em': var = getattr( tree, 'ePt' )
		elif channel == 'tt': var = getattr( tree, 't1Pt' )
		else: 
			print "What channel are you giving me?!?" 
			return -1
		hist.Fill( var )
	return hist
			
