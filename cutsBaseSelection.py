import ROOT
#from array import array

def makeZCut( chain, l1, l2 ) :
	print "l1 %s, l2 %s" % (l1, l2)
	outTree = chain.CopyTree( "abs( %s_%s_Mass - 90 ) < 30" % (l1, l2) )
	return outTree

def makeHisto( tree, sample, channel, cutName, var, varBins, varMin, varMax ) :
	name = "%s%s%s" % ( sample, channel, cutName )
	hist = ROOT.TH1F( var, var, varBins, varMin, varMax )

	for i in range( tree.GetEntries() ):
		tree.GetEntry( i )
		num = getattr( tree, var )
		hist.Fill( num )
	return hist
			
#def getGeneralHistoDict()
		
