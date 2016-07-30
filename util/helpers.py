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
    # and remove them to correspond to the final state combo
    hasData = False
    toRemove = []
    for sample in samples :
        if 'data' in sample :
            hasData = True
            toRemove.append( sample )
    if hasData == True :
        for rmv in toRemove :
            samples.remove( rmv )
        if final == 'ZEE' : samples.append( 'dataEE' )
        if final == 'ZMM' : samples.append( 'dataMM' )
        if final == 'ZXX' : 
            samples.append( 'dataEE' )
            samples.append( 'dataMM' )

    for sample in samples :

        if final == 'ZEE' : getChan = 'eeet' 
        if final == 'ZMM' : getChan = 'emmt' 
        if final == 'ZXX' : 
            getChan = 'eeet' 
            if sample == 'dataMM' :
                getChan = 'emmt' 

        # Make new file to hold combined histos
        nfile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folder, sample, final), 'RECREATE')
        outDir = nfile.mkdir( final+'_Histos' )
        outDir.cd()

        ifile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folder, sample, getChan), 'r' )
        print sample
        print final
        print channels
        print ifile
        histKeys = getKeysOfClass( ifile, getChan+'_Histos', 'TH1F' )
        print histKeys

        # Make a map of our hists to add
        hists = {}
        for h in histKeys :
            #print h.GetName()
            hists[h.GetName()] =  h.ReadObj()
        # Skip channels[0] as we already used it
        for channel in channels :
            print channel," for consideration"

            # These are for the Z->EE/MM inclusive
            if channel == getChan : 
                print "Included as initial file"
                continue
            if channel in ['eeet', 'eemt', 'eett', 'eeem', 'eeee', 'eemm'] and sample == 'dataMM' :
                continue
            if channel in ['emmt', 'mmmt', 'mmtt', 'emmm', 'mmmm'] and sample == 'dataEE' :
                continue
            print channel," considered"

            f = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folder, sample, channel), 'r' )
            print f
            d = f.Get( channel+'_Histos' )
            for h in histKeys :
                htmp = d.Get( h.GetName() )
                hists[h.GetName()] += htmp
        # Write final output
        for h in histKeys :
            outDir.cd()
            hists[h.GetName()].Write()
        
            
        
            

if __name__ == '__main__' :
    mergeChannels( 'azh', '3July27d', ['data_ee',], ['eeet','eemt'], 'ZEE' )

