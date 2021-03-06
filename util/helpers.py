import os, glob, subprocess
import ROOT
from collections import OrderedDict
from array import array
from math import sqrt
import copy


# Check if directory exists, make it if not
def checkDir( dirName ) :
    if not os.path.exists( dirName ) : os.makedirs( dirName )


# Function to create TH1Fs from TGraphAsymmErrors
def getTH1FfromTGraphAsymmErrors( asym, name='new_asym' ) :

    # Holding vals for TH1F binning and y-vals
    xSpacing = array( 'd', [] )
    yVals = array( 'd', [] )
    yErrors = array( 'd', [] )

    nVals = asym.GetN()
    x, y = ROOT.Double(0.), ROOT.Double(0.)
    xEPlus, xEMin = 0., 0.
    yEPlus, yEMin = 0., 0.

    for n in range( nVals ) :
        asym.GetPoint( n, x, y )
        xEPlus = asym.GetErrorXhigh( n )
        xEMin = asym.GetErrorXlow( n )
        yEPlus = asym.GetErrorYhigh( n )
        yEMin = asym.GetErrorYlow( n )
        xSpacing.append( x-xEMin )
        yVals.append( y )
        # To simplify, take asymm errors and got to Gaussian
        # for TH1
        yErrors.append( sqrt(yEPlus**2 + yEMin**2) )

    # Don't forget to add the high end of last bin
    xSpacing.append( x+xEPlus )

    #print xSpacing
    #print yVals

    outH = ROOT.TH1F( name, name, len(xSpacing)-1, xSpacing )
    for bin in range( 1, outH.GetNbinsX()+1 ) :
        outH.SetBinContent( bin, yVals[bin-1] )
        outH.SetBinError( bin, yErrors[bin-1] )
    return outH



# A function to set up our directories and check if we are running
# certain bkg methods
def setUpDirs( samples, params, analysis ) :
    
    host = os.getenv('HOSTNAME')
    if 'uwlogin' in host :
        if not os.path.exists( '/data/truggles/%s%s' % (analysis, params['mid1']) ) : os.makedirs( '/data/truggles/%s%s' % (analysis, params['mid1']) )
        if not os.path.exists( '/data/truggles/%s%s' % (analysis, params['mid2']) ) : os.makedirs( '/data/truggles/%s%s' % (analysis, params['mid2']) )
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
        if final == 'ZEE' and ('dataMM' in sample or 'dataSingleM' in sample ): continue
        if final == 'ZMM' and ('dataEE' in sample or 'dataSingleE' in sample ): continue

        if final == 'ZEE' : getChan = 'eeet' 
        elif final == 'ZMM' : getChan = 'emmt' 
        elif final == 'LLET' :
            getChan = 'eeet' 
            if ('dataMM' in sample or 'dataSingleM' in sample) :
                getChan = 'emmt' 
        elif final == 'LLMT' :
            getChan = 'eemt' 
            if ('dataMM' in sample or 'dataSingleM' in sample) :
                getChan = 'mmmt' 
        elif final == 'LLTT' :
            getChan = 'eett' 
            if ('dataMM' in sample or 'dataSingleM' in sample) :
                getChan = 'mmtt' 
        elif final == 'LLEM' :
            getChan = 'eeem' 
            if ('dataMM' in sample or 'dataSingleM' in sample) :
                getChan = 'emmm' 
        elif final == 'ZXX' : 
            getChan = 'eeet' 
            if ('dataMM' in sample or 'dataSingleM' in sample) :
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
            if channel in ['eeet', 'eemt', 'eett', 'eeem', 'eeee', 'eemm'] and ('dataMM' in sample or 'dataSingleM' in sample) :
                continue
            if channel in ['emmt', 'mmmt', 'mmtt', 'emmm', 'mmmm'] and ('dataEE' in sample or 'dataSingleE' in sample) :
                continue
            print channel," considered"

            f = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folder, sample, channel), 'r' )
            d = f.Get( channel+'_Histos' )
            for h in hists.keys() :
                #print h
                htmp = d.Get( h )
                if htmp == None :
                    print "\n\n\nIn Merge HTMP == None\n%s %s %s" % ( channel, f, h )
                    continue
                if h not in allChannelVarMap.keys() :
                    #print "Not in all chan var map ",h.GetName()
                    print "Not in all chan var map ",h
                    continue
                #hists[h] += htmp
                hists[h].Add( htmp )
        # Write final output
        for h in hists.keys() :
            outDir.cd()
            hists[h].Write()


def getQCDSF( fileName, category ) :

    with open( fileName ) as qcdFile :
        for line in qcdFile :
            info = line.strip().split(':')
            if info[0] == category :
                print info
                return float(info[1])


def unroll2D( hist, name='' ) :
    nBinsX = hist.GetNbinsX()
    nBinsY = hist.GetNbinsY()
    nBins = nBinsX * nBinsY
    #print "bin info: ",nBinsX, nBinsY, nBins

    # Because we use the array method to construct our datacards
    # if we use arrays here, we avoid unnecessary warning messages
    # later on
    # ROOT warning: "Attempt to add histograms with different bin limits"
    binArray = array( 'd', [i for i in range( nBins+1 )] )
    numBins = len( binArray ) - 1
    hNew = ROOT.TH1D( hist.GetName()+name, hist.GetTitle()+name, numBins, binArray )
    hNew.Sumw2()
    for i in range(1, nBinsY+1) :
        for j in range(1, nBinsX+1) :
            #print "i %i j %i set bin %i" % (i, j, j+(i-1)*nBinsX)
            #print "Bin content:",hist.GetBinContent( j, i )
            hNew.SetBinContent( j+(i-1)*nBinsX, hist.GetBinContent( j, i ) )
            hNew.SetBinError( j+(i-1)*nBinsX, hist.GetBinError( j, i ) )
    return hNew


# Returns a sorted ordered dict
# The values must be stored in a list, not tuple
def returnSortedDict( dict ) :
    alist = dict.keys()
    alist.sort()
    rtnDict = OrderedDict()
    for var in alist :
        rtnDict[ var ] = list(dict[ var ])
    return rtnDict

def getProdMap() :
    prodMap = {
        'em' : ('e', 'm'),
        'et' : ('e', 't'),
        'mt' : ('m', 't'),
        'tt' : ('t1', 't2'),
        'eeem' : ('e1', 'e2', 'e3', 'm'),
        'eeet' : ('e1', 'e2', 'e3', 't'),
        'eemt' : ('e1', 'e2', 'm', 't'),
        'eett' : ('e1', 'e2', 't1', 't2'),
        'emmm' : ('m1', 'm2', 'e', 'm3'),
        'emmt' : ('m1', 'm2', 'e', 't'),
        'mmmt' : ('m1', 'm2', 'm3', 't'),
        'mmtt' : ('m1', 'm2', 't1', 't2'),
        'eeee' : ('e1', 'e2', 'e3', 'e4'),
        'eemm' : ('e1', 'e2', 'm1', 'm2'),
        'mmmm' : ('m1', 'm2', 'm3', 'm4'),
    }
    return prodMap


# Provides a gen matched expanded list of samples
# with the key, val being name = data card name
def dataCardGenMatchedSamples( analysis, inSamples ) :
    assert( type(inSamples) == type(OrderedDict())
        or type(inSamples) == type({}) ), "Provide a samples list which \
        is a dict or OrderedDict"

    # Eras of 2016 data
    eras =  ['B', 'C', 'D', 'E', 'F', 'G', 'H']

    samples = OrderedDict()
    if analysis == 'htt' :
        genMapDYJ = ['ZTT', 'ZLL', 'ZL', 'ZJ']
        dyJets = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4',]# 'DYJetsLow']
        for dyj in dyJets :
            if dyj in inSamples :
                for gen in genMapDYJ : samples[dyj+'-'+gen] = gen

        genMapTT = ['TTT', 'TTJ']
        if 'TT' in inSamples :
            for gen in genMapTT : samples['TT-'+gen] = gen
        
        genMapVV = ['VVT', 'VVJ']
        vvs = ['WW1l1nu2q', 'WW2l2nu', 'WZ1l1nu2q', 'WZ1l3nu', 
             'WZ2l2q', 'WZ3l1nu', 'ZZ2l2nu', 'ZZ2l2q', 'ZZ4l', 
             'VV', 'WWW', 'ZZZ', 'T-tW', 'T-tchan', 'Tbar-tW', 'Tbar-tchan']
        for vv in vvs :
            if vv in inSamples :
                for gen in genMapVV : samples[vv+'-'+gen] = gen

        WJets = ['WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'EWKWPlus', 'EWKWMinus']
        for wjet in WJets :
            if wjet in inSamples : samples[wjet] = 'W'

        ewkZs = ['EWKZ2l', 'EWKZ2nu']
        for ewkZ in ewkZs :
            if ewkZ in inSamples : samples[ewkZ] = 'EWKZ'

        samples['QCD'] = 'QCD'

    if analysis == 'azh' :

        useRedBkg = False
        # Check for reducible bkg samples
        # if RedBkg present, skim DYJ and WZ later
        for era in eras :
            if 'RedBkgYieldSingleLep-%s' % era in inSamples :
                useRedBkg = True
                samples['RedBkgYieldSingleLep-%s' % era]  = 'allFakes'
            elif 'RedBkgShapeSingleLep-%s' % era in inSamples :
                useRedBkg = True
                samples['RedBkgShapeSingleLep-%s' % era]  = 'allFakes'
            elif 'RedBkgYieldDoubleLep-%s' % era in inSamples :
                useRedBkg = True
                samples['RedBkgYieldDoubleLep-%s' % era]  = 'allFakes'
            elif 'RedBkgShapeDoubleLep-%s' % era in inSamples :
                useRedBkg = True
                samples['RedBkgShapeDoubleLep-%s' % era]  = 'allFakes'
        if not useRedBkg :
            redBkgList = ['TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'WWW']
            for rb in redBkgList :
                if rb in inSamples :
                    if rb == 'TT' : samples['TT']  = 'TT'
                    elif rb == 'WZ3l1nu' : samples['WZ3l1nu']  = 'WZ'
                    elif rb == 'WWW' : samples['WWW']  = 'TriBoson'
                    else : samples[rb]  = 'DY'
        if useRedBkg :
            redBkgList = ['TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'WWW']
            for rb in redBkgList :
                if rb in inSamples :
                    if rb == 'TT' : samples['TT-NONJET']  = 'TT'
                    elif rb == 'WZ3l1nu' : samples['WZ3l1nu-NONJET']  = 'WZ'
                    elif rb == 'WWW' : samples['WWW-NONJET']  = 'TriBoson'
                    else : samples['%s-NONJET' % rb]  = 'DY'

        triBosons = ['WWZ', 'WZZ', 'ZZZ',] # WWW is reducible
        for tri in triBosons :
            if tri in inSamples :
                samples['%s-NONJET' % tri]  = 'TriBoson'
        ggZZs = ['ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau']
        for zz in ggZZs :
            if zz in inSamples :
                samples['%s-NONJET' % zz]  = 'ggZZ'
        if 'ZZ4l' in inSamples : samples['ZZ4l-NONJET'] = 'ZZ'
        if 'ttZ' in inSamples : samples['ttZ-NONJET'] = 'ttZ'

        for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
            if 'azh%i' % mass in inSamples :
                samples['azh%i' % mass] = 'azh%i' % mass

    # Common to all
    for era in eras :
        if 'dataTT-%s' % era in inSamples :
            samples['dataTT-%s' % era]  = 'data_obs'
        if 'dataEE-%s' % era in inSamples :
            samples['dataEE-%s' % era]  = 'data_obs'
        if 'dataMM-%s' % era in inSamples :
            samples['dataMM-%s' % era]  = 'data_obs'
        if 'dataSingleE-%s' % era in inSamples :
            samples['dataSingleE-%s' % era]  = 'data_obs'
        if 'dataSingleM-%s' % era in inSamples :
            samples['dataSingleM-%s' % era]  = 'data_obs'

    for mass in ['110', '120', '125', '130', '140'] :
        # *_htt
        if 'VBFHtoTauTau%s' % mass in inSamples :
            samples['VBFHtoTauTau%s' % mass] = 'qqH_htt%s' % mass
        if 'ggHtoTauTau%s' % mass in inSamples :
            samples['ggHtoTauTau%s' % mass] = 'ggH_htt%s' % mass
        if 'WMinusHTauTau%s' % mass in inSamples :
            samples['WMinusHTauTau%s' % mass] = 'WH_htt%s' % mass
        if 'WPlusHTauTau%s' % mass in inSamples :
            samples['WPlusHTauTau%s' % mass] = 'WH_htt%s' % mass
        if 'ZHTauTau%s' % mass in inSamples :
            samples['ZHTauTau%s' % mass] = 'ZH_htt%s' % mass

        # *_hww
        if 'ZHWW%s' % mass in inSamples :
            samples['ZHWW%s' % mass] = 'ZH_hww%s' % mass
        if 'WPlusHHWW%s' % mass in inSamples :
            samples['WPlusHHWW%s' % mass] = 'WH_hww%s' % mass
        if 'WMinusHHWW%s' % mass in inSamples :
            samples['WMinusHHWW%s' % mass] = 'WH_hww%s' % mass
        if 'VBFHtoWW2l2nu%s' % mass in inSamples :
            samples['VBFHtoWW2l2nu%s' % mass] = 'qqH_hww%s' % mass
        if 'HtoWW2l2nu%s' % mass in inSamples :
            samples['HtoWW2l2nu%s' % mass] = 'ggH_hww%s' % mass

        # *_hzz
        if 'HZZ%s' % mass in inSamples :
            samples['HZZ%s' % mass] = 'ggH_hzz%s' % mass

        # ttH production
        if 'ttHTauTau%s' % mass in inSamples :
            samples['ttHTauTau%s' % mass] = 'ttH_htt%s' % mass
        if 'ttHNonBB%s' % mass in inSamples :
            samples['ttHNonBB%s' % mass] = 'ttH_other%s' % mass
        if 'ttHJNonBB%s' % mass in inSamples :
            samples['ttHJNonBB%s' % mass] = 'ttH_otherJ%s' % mass


    return samples


if __name__ == '__main__' :
    #print getQCDSF( 'httQCDYields_2Aug25x5pt45b.txt', '1Jet' )
    #f = ROOT.TFile('meta/httBackgrounds/tt_qcdShape_2Oct11b2DRoll_OSl1ml2_Tight_LooseZTT1jet2D.root','r')
    #f = ROOT.TFile('htt2Oct11b2DRoll_OSl1ml2_Tight_LooseZTT1jet2D/ggHtoTauTau125_tt.root','r')
    #hist = f.Get('tt_Histos/Higgs_Pt:m_sv')
    #h1 = unroll2D( hist )
    #h1.SaveAs('ggh125.root')
    print "Hello"





