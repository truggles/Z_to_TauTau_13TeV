# Function to build TChains out of a list of input files and a TTree path

import ROOT
from ROOT import TTree, TFile

def makeTChain( sampleList, treePath, maxFiles=0 ) :
	files = open( sampleList, 'r' )	
	tree = ROOT.TChain( treePath )
	count = 0
	
	for file_ in files :
		#currentFile = ROOT.TFile( file_.strip(), 'r' )
		#fileTree =  currentFile.Get( treePath )
		tree.Add( file_.strip() )
		
		# Just in case we want to debug with a limited amount of files
		count += 1
		if count >= maxFiles and maxFiles != 0:
			print "Loaded %i Files" % count
			break
			
	files.close()
	return tree
