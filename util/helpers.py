import os, glob, subprocess
import ROOT




# A function to set up our directories and check if we are running
# certain bkg methods
def setUpDirs( samples, params, analysis ) :
    if not os.path.exists( '%s%s' % (analysis, params['mid1']) ) : os.makedirs( '%s%s' % (analysis, params['mid1']) )
    if not os.path.exists( '%s%s' % (analysis, params['mid2']) ) : os.makedirs( '%s%s' % (analysis, params['mid2']) )
    if not os.path.exists( '%s%s' % (analysis, params['mid3']) ) : os.makedirs( '%s%s' % (analysis, params['mid3']) )
    ofile = open('%s%s/config.txt' % (analysis, params['mid3']), "w")
    for sample in samples :
        ofile.write( "%s " % sample )
    ofile.write( "\n" )
    for key in params :
        ofile.write( "%s : %s\n" % (key, params[key]) )
    ofile.close() 


# Can use to return all hists in a dir
def getKeysOfClass( file_, dir_, class_ ) :
    keys = []
    d = file_.Get( dir_ )
    allKeys = d.GetListOfKeys()

    #print "keys of class"
    for k in allKeys :
        if k.GetClassName() == class_ :
            keys.append( k )

    return keys

# Merge some files for useful channel combinations
def mergeChannels( analysis, folder, samples, channels, final ) :
    # Check if we have data files in samples
    hasData = False
    toRemove = []
    for sample in samples :
        if 'data' in sample :
            hasData = True
            toRemove.append( sample )
    if hasData == True :
        for rmv in toRemove :
            samples.remove( rmv )
        samples.append( 'data' )

    for sample in samples :
        # Make new file to hold combined histos
        nfile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folder, sample, final), 'RECREATE')
        outDir = nfile.mkdir( final+'_Histos' )
        outDir.cd()

        firstChan = channels[0]
        ifile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folder, sample, firstChan), 'r' )
        histKeys = getKeysOfClass( ifile, channels[0]+'_Histos', 'TH1F' )
        print histKeys
        iDir = ifile.Get( channels[0] )

        # Make a map of our hists to add
        hists = {}
        for h in histKeys :
            print h.GetName()
            hists[h.GetName()] =  h.ReadObj()
        # Skip channels[0] as we already used it
        for i in range( 1, len( channels ) ) :
            f = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folder, sample, channels[i]), 'r' )
            print f
            d = f.Get( channels[i]+'_Histos' )
            for h in histKeys :
                htmp = d.Get( h.GetName() )
                hists[h.GetName()] += htmp
        # Write final output
        for h in histKeys :
            outDir.cd()
            hists[h.GetName()].Write()
        
            
        
            

if __name__ == '__main__' :
    mergeChannels( 'azh', '3July27d', ['data_ee',], ['eeet','eemt'], 'ZEE' )

