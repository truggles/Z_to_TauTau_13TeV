# Function to build TChains out of a list of input files and a TTree path

import ROOT
from ROOT import TTree, TFile

def makeTChain( sampleList, treePath, maxFiles=0, startFile=0, maxFile=9999 ) :
    files = open( sampleList, 'r' )	
    tree = ROOT.TChain( treePath )
    count = 1
    #print "startFile = %i" % startFile
    
    for file_ in files :
        #currentFile = ROOT.TFile( file_.strip(), 'r' )
        #fileTree =  currentFile.Get( treePath )
        if count >= startFile and count <= maxFile :
            #print "count %3i  %s" % (count, file_)
            tree.Add( file_.strip() )
        
        # Just in case we want to debug with a limited amount of files
        count += 1
        if count >= maxFiles and maxFiles != 0:
            print "Loaded %i Files" % count
            break
        if count > maxFile :
            print "reached maxFile = %i" % maxFile
            break

    print "File List: %s\n - Tree Path: %s\n - Loaded Files up to = %i" % (sampleList, treePath, count-1)
    files.close()
    return tree
