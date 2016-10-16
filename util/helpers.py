import os, glob, subprocess
import ROOT


# Check if directory exists, make it if not
def checkDir( dirName ) :
    if not os.path.exists( dirName ) : os.makedirs( dirName )


# Function to create TH1Fs from TGraphAsymmErrors
def getTH1FfromTGraphAsymmErrors( asym, name ) :
    from array import array

    # Holding vals for TH1F binning and y-vals
    xSpacing = array( 'd', [] )
    yVals = array( 'd', [] )

    nVals = asym.GetN()
    x, y = ROOT.Double(0.), ROOT.Double(0.)
    xEPlus, xEMin = 0., 0.

    for n in range( nVals ) :
        asym.GetPoint( n, x, y )
        xEPlus = asym.GetErrorXhigh( n )
        xEMin = asym.GetErrorXlow( n )
        xSpacing.append( x-xEMin )
        yVals.append( y )

    # Don't forget to add the high end of last bin
    xSpacing.append( x+xEPlus )

    #print xSpacing
    #print yVals

    outH = ROOT.TH1F( name, name, len(xSpacing)-1, xSpacing )
    for bin in range( 1, outH.GetNbinsX()+1 ) :
        outH.SetBinContent( bin, yVals[bin-1] )
    return outH



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
    from analysisPlots import getHistoDict

    # We only want to merge histos that correspond to all channels
    allChannelVarMap = getHistoDict( analysis, 'xxxx' )
    #print allChannelVarMap

    # Check if we have data files in samples
    # and remove them to correspond to the final state combo
    for sample in samples :
        if final == 'ZEE' and 'dataMM' in sample : continue
        if final == 'ZMM' and 'dataEE' in sample : continue

        if final == 'ZEE' : getChan = 'eeet' 
        if final == 'ZMM' : getChan = 'emmt' 
        if final == 'ZXX' : 
            getChan = 'eeet' 
            if 'dataMM' in sample :
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
        histKeys = getKeysOfClass( ifile, getChan+'_Histos', 'TH1D' )
        #print histKeys

        # Make a map of our hists to add
        hists = {}
        for h in histKeys :
            if h.GetName() not in allChannelVarMap.keys() :
                print "Not in all chan var map ",h.GetName()
                histKeys.remove( h )
                continue
            hists[h.GetName()] =  h.ReadObj()
        # Skip channels[0] as we already used it
        for channel in channels :
            print channel," for consideration"

            # These are for the Z->EE/MM inclusive
            if channel == getChan : 
                print "Included as initial file"
                continue
            if channel in ['eeet', 'eemt', 'eett', 'eeem', 'eeee', 'eemm'] and 'dataMM' in sample :
                continue
            if channel in ['emmt', 'mmmt', 'mmtt', 'emmm', 'mmmm'] and 'dataEE' in sample :
                continue
            print channel," considered"

            f = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folder, sample, channel), 'r' )
            d = f.Get( channel+'_Histos' )
            for h in hists.keys() :
                #print h
                htmp = d.Get( h )
                if h not in allChannelVarMap.keys() :
                    #print "Not in all chan var map ",h.GetName()
                    print "Not in all chan var map ",h
                    continue
                hists[h] += htmp
        # Write final output
        for h in hists.keys() :
            outDir.cd()
            hists[h].Write()
        
            
## Merge files from a file list into a new directory
## this is to keep root from having to open thousands
## of tiny files        
#def mergeFiles( analysis, fileList, outDir ) :
#    
#    # Check if outbound directory exists
#    # Make outbound directory
#    if not os.path.exists( outDir ) :
#        os.makedirs( outDir )
#    print "Output Dir: ",outDir
#    
#    # Build list of files
#    files = []
#    with open( 'meta/NtupleInputs_%s/%s' % (analysis, fileList) ) as fList :
#        for file in fList :
#            f = file.strip()
#            files.append( f )
#    print files
#    info = fileList.split('/')
#    sample = info[-1].strip('.txt')
#    print sample
#    
#
#    rep = 0
#    runningSize = 0
#    toMerge = []
#    for file_ in files :
#        size = os.path.getsize( file_ )/1000 # in KB roughly
#        print size, " KB ", file_
#        runningSize += size
#        print "Running size",runningSize
#        toMerge.append( file_ )
#        if runningSize > 500000 : # Target 1 GB files
#            runningSize = 0
#            mergeList = ["hadd", "-f", outDir+"/%s_%i.root" % (sample, rep)]
#            for f in toMerge :
#            	mergeList.append( f )
#            subprocess.call( mergeList )
#            print mergeList
#            toMerge = []
#            rep += 1
#
#    # Make sure to get the others who didn't total over 1 GB
#    mergeList = ["hadd", "-f", outDir+"/%s_%i.root" % (sample, rep)]
#    for f in toMerge :
#    	mergeList.append( f )
#    if len( mergeList ) > 3 : # greater than 3 means we actually have a file to merge (not empty)
#    	subprocess.call( mergeList )
            

#if __name__ == '__main__' :
    #mergeChannels( 'azh', '3July27d', ['data_ee',], ['eeet','eemt'], 'ZEE' )
    #analysis = 'azh'
    #fileList = 'WZ3l1nu.txt'
    #outDir = '/data/truggles/tmpFun'    
    #mergeFiles( analysis, fileList, outDir )


def getQCDSF( fileName, category ) :

    with open( fileName ) as qcdFile :
        for line in qcdFile :
            info = line.strip().split(':')
            if info[0] == category :
                print info
                return float(info[1])


def unroll2D( hist ) :
    nBinsX = hist.GetNbinsX()
    nBinsY = hist.GetNbinsY()
    nBins = nBinsX * nBinsY
    #print "bin info: ",nBinsX, nBinsY, nBins
    hNew = ROOT.TH1D( hist.GetName(), hist.GetTitle(), nBins, 0, nBins )
    for i in range(1, nBinsY+1) :
        for j in range(1, nBinsX+1) :
            #print "i %i j %i set bin %i" % (i, j, j+(i-1)*nBinsX)
            #print "Bin content:",hist.GetBinContent( j, i )
            hNew.SetBinContent( j+(i-1)*nBinsX, hist.GetBinContent( j, i ) )
            hNew.SetBinError( j+(i-1)*nBinsX, hist.GetBinError( j, i ) )
    return hNew


if __name__ == '__main__' :
    #print getQCDSF( 'httQCDYields_2Aug25x5pt45b.txt', '1Jet' )
    #f = ROOT.TFile('meta/httBackgrounds/tt_qcdShape_2Oct11b2DRoll_OSl1ml2_Tight_LooseZTT1jet2D.root','r')
    #f = ROOT.TFile('htt2Oct11b2DRoll_OSl1ml2_Tight_LooseZTT1jet2D/ggHtoTauTau125_tt.root','r')
    #hist = f.Get('tt_Histos/Higgs_Pt:m_sv')
    #h1 = unroll2D( hist )
    #h1.SaveAs('ggh125.root')
    print "Hello"





