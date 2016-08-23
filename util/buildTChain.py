# Function to build TChains out of a list of input files and a TTree path

import ROOT
from ROOT import TTree, TFile

def makeTChain( sampleList, treePath, maxFiles=0, startFile=0, maxFile=9999 ) :
    #print "makeTChain: startFile: %i   maxFile: %i" % (startFile, maxFile)
    files = open( sampleList, 'r' )	
    tree = ROOT.TChain( treePath )
    startFile += 1
    maxFile += 1
    
    line = 1
    for file_ in files :
        #currentFile = ROOT.TFile( file_.strip(), 'r' )
        #fileTree =  currentFile.Get( treePath )
        if line >= startFile and line <= maxFile :
            #print " -- line %3i  %s" % (line, file_)
            tree.Add( file_.strip() )
        
        # Just in case we want to debug with a limited amount of files
        line += 1
        if line >= maxFiles and maxFiles != 0:
            #print "Loaded line %i --> line %i" % (startFile, maxFile)
            break
        if line > maxFile :
            #print "reached maxFile = %i" % maxFile
            break

    #print "File List: %s\n - Tree Path: %s\n - Loaded Files up to = %i" % (sampleList, treePath, line-1)
    files.close()
    return tree



def getEventCount( sampleList, channel, maxFiles=0, startFile=0, maxFile=9999 ) :
    #print "makeTChain: startFile: %i   maxFile: %i" % (startFile, maxFile)
    files = open( sampleList, 'r' )	
    startFile += 1
    maxFile += 1
    
    line = 1
    eventCount = 0
    for file_ in files :
        if line >= startFile and line <= maxFile :
            #print " -- line %3i  %s" % (line, file_)
	    f = ROOT.TFile( file_.strip(), 'r' )
	    eventCount += f.Get( channel+'/eventCount' ).Integral()
        
        # Just in case we want to debug with a limited amount of files
        line += 1
        if line >= maxFiles and maxFiles != 0:
            #print "Loaded line %i --> line %i" % (startFile, maxFile)
            break
        if line > maxFile :
            #print "reached maxFile = %i" % maxFile
            break

    files.close()
    return eventCount



def makeTChainFromGlob( sampleList, treePath, ) :
    #print "makeTChain: startFile: %i   maxFile: %i" % (startFile, maxFile)
    tree = ROOT.TChain( treePath )
    i = 0
    for file_ in sampleList :
        tree.Add( file_ )
        i += 1
        
    print "Loaded %i files" % i
    return tree



def getTree( sampleList, treePath, count ) :
    print "sampleList",sampleList
    print "path",treePath
    print "count",count
    files = open( sampleList, 'r' )	
    
    i = 0
    for file_ in files :
        print "i =",i
        #currentFile = ROOT.TFile( file_.strip(), 'r' )
        #fileTree =  currentFile.Get( treePath )
        if i == count :
            print "i ",i," == count",count
            #print "line %3i  %s" % (count, file_)
            f = ROOT.TFile( file_.strip() )
            tree = f.Get( treePath )
            print "tree entries",tree.GetEntries()
            files.close()
            return tree
        i += 1
    print "END OF FILE LIST AND NO FILE SELECTED"



