import ROOT
import math
import util.cumulativeDist as CDF
ROOT.gROOT.SetBatch(True)

ssIsoPairs = [
    ('Loose','Medium'),
    #('Loose','Tight'),
    #('Loose','VTight'),
    ('Medium','Tight'),
    #('Medium','VTight'),
    ('Tight','VTight'),
    ('VTight','')
    ]
osIsoPairs = [
    ('Loose','Medium'),
    ('Medium','Tight'),
    ('Tight','VTight'),
    ]

def signalSamp( var, sign ) :
    print "\nSignal sample Var: %s    Sign: %s" % (var, sign)
    #f = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%sIsoCut.root' % sign,'r')
    f = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%sIsoCutBT.root' % sign,'r')
    t = f.Get('tt_Histos')
    h = t.Get( var )
    h.SetFillColor( 0 )
    h.SetDirectory( 0 )
    return h

def getShapes( var, sign, l1='', btag='' ) :
    histos = []
    if sign == 'SS' : isoPairs = ssIsoPairs
    if sign == 'OS' : isoPairs = osIsoPairs
    for i,pair in enumerate(isoPairs) :
        #f1 = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%s_%s_%s.root' % (sign, pair[1], pair[0]),'r')
        f1 = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%s%s_%s_%s%s.root' % (sign, l1, pair[1], pair[0], btag),'r')
        t1 = f1.Get('tt_Histos')
        h1 = t1.Get( var )
        h1.SetName( "%s%s" % (pair[0],pair[1]) )
        h1.SetDirectory( 0 )
        h1.SetFillColor( 0 )
        histos.append( h1 )
        f1.Close()
    return histos

def printStats( h ) :
    print " -- Mean: %3.2f +/- %3.2f  StdDev: %3.2f +/- %3.2f  Skew: %3.2f +/- %3.2f Kurtosis %3.2f +/- %3.2f\n" % (h.GetMean(), h.GetMeanError(), h.GetStdDev(), h.GetStdDevError(), h.GetSkewness(), h.GetSkewness(11), h.GetKurtosis(), h.GetKurtosis(11) )

def printYields( osHistos, ssHistos ) :
    isoPairs = osIsoPairs
    ssSigInt = ssHistos[-1].Integral()
    ssInts = []
    for h in ssHistos :
        ssInts.append( (h.Integral(),math.sqrt(h.Integral()),1./math.sqrt(h.Integral()) ) )
    osInts = []
    for h in osHistos :
        osInts.append( (h.Integral(),math.sqrt(h.Integral()),1./math.sqrt(h.Integral()) ) )
    for i,pair in enumerate(isoPairs) :
        ssWUncert = ssInts[i][1]
        print "SS %s %s yield = %3.2f +/- %3.2f" % (pair[0], pair[1], ssInts[i][0], ssWUncert)
        printStats( ssHistos[i] )
        osWUncert = osInts[i][1]
        print "OS %s %s yield = %3.2f +/- %3.2f" % (pair[0], pair[1], osInts[i][0], osWUncert)
        printStats( osHistos[i] )
    print "SS VTight yield = %3.2f +/- %3.2f" % (ssSigInt, math.sqrt(ssSigInt))
    printStats( ssHistos[-1] )
    print "\n"

    #tags = {0:'MT/LM',1:'TVT/MT',2:'VT/TVT'}
    tags = {(0,1):'MT/LM',(0,2):'TVT/LT',(1,2):'TVT/MT',len(osIsoPairs)-1:'VT/TVT'}
    #tags = {0:'LT/LM',1:'LVT/LT',2:'MT/LVT',3:'MVT/MT',4:'TVT/MVT'}
    print "              SS                       OS"
    for i in range( len(isoPairs) ) :
        for j in range(i+1, len(isoPairs) ) :
            if i < len(isoPairs)-1:
                ssr = ssInts[j][0]/ssInts[i][0]
                sse = math.sqrt( (1./ssInts[j][1])**2 + (1./ssInts[i][1])**2 )
                osr = osInts[j][0]/osInts[i][0]
                ose = math.sqrt( (1./osInts[j][1])**2 + (1./osInts[i][1])**2 )
                print "%8s   %3.2f+/-%3.2f        %3.2f+/-%3.2f" % (tags[(i,j)],ssr,sse,osr,ose)
        if i == len(isoPairs)-1 :
            ssr = ssSigInt/ssInts[i][0]
            sse = math.sqrt( (1./math.sqrt(ssSigInt))**2 + (1./ssInts[i][1])**2 )
            print "%8s   %3.2f+/-%3.2f" % (tags[i],ssr,sse)

    print "\n"
    for i,pair in enumerate(isoPairs) :
        uncert = math.sqrt( osInts[i][2]**2 + ssInts[i][2]**2 )
        ratio = ssInts[i][0]/osInts[i][0]
        print "%s %s   SS/OS   %3.2f +/- %3.3f" % ( pair[0], pair[1], ratio, ratio*uncert )
    print "\n"



def makeCDFs( histos, sign, zeroNeg ) :
    cdfs = []
    for hist in histos :
        cdfs.append( CDF.CDF( hist, zeroNeg, sign ) )
    return cdfs


def KSTests( cdf1, eCDF1, cdfs, histos ) :
    ksVals = []
    for i,cdf in enumerate(cdfs) :
        maxDiff = 0
        for k in range( 1, cdf.GetXaxis().GetNbins() + 2 ) :
            diff = abs(cdf.GetBinContent( k ) - cdf1.GetBinContent( k ))
            if diff > maxDiff : maxDiff = diff
        #print "cdf %i: KS max diff %f" % (i, maxDiff)
        e2 =  histos[i].GetEntries()
        #ksVals.append( maxDiff * histos[i].Integral() )
        ksVals.append( maxDiff * math.sqrt((eCDF1*e2)/(eCDF1+e2)))
        #print " --- Crit Val: %f" % ( ksVals[i] )
    return ksVals

def ksTest( shape, h1, h2, n0, n1, n2, zeroed='' ) :
    ksProb = h1.KolmogorovTest( h2 )
    #print "%s: KS Prop = %3.2f" % (n0, ksProb )
    c1 = ROOT.TCanvas( 'c1%s' % n0, 'c1', 600, 600 )
    p1 = ROOT.TPad('p1%s' % n0, 'p1', 0, 0, 1, 1 )
    p1.Draw()
    p1.SetGrid()
    p1.cd()
    
    h1.SetLineColor( ROOT.kRed )
    h1.SetTitle( '%s  %s KS Prob = %3.3f' % (n0, zeroed, ksProb ) )
    h2.SetLineColor( ROOT.kBlue )
    h1.SetStats(0)
    if shape == 'm_sv' : title = 'svFit M_{#tau#tau}'
    if shape == 'm_vis' : title = 'Visible M_{#tau#tau}'
    h1.GetXaxis().SetTitle('%s (GeV)' % title)
    h1.GetYaxis().SetTitle('A.U.')
    #h1.Draw('')
    #h2.Draw('same')
    h1.Draw('HIST e1')
    h2.Draw('same HIST e1')

    h1.SetMaximum( max(h1.GetMaximum(), h2.GetMaximum()) * 1.1 )
    h1.SetMinimum( min(h1.GetMinimum(), h2.GetMinimum()) * 1.2 )
    
    
    ''' Build the legend explicitly so we can specify marker styles '''
    legend = ROOT.TLegend(0.60, 0.75, 0.90, 0.9)
    legend.SetMargin(0.3)
    #legend.SetBorderSize(0)
    legend.AddEntry( h1, n1, 'l')
    legend.AddEntry( h2, n2, 'l')
    legend.Draw()
    
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/moreQCD/%s_%s_%s%s%s.png' % (shape, n, n0,n1,n2))
    return ksProb
        
def runAllKS( osIsoPairs, ssIsoPairs, osHistos, ssHistos ) :
    ''' rebin! '''
    ks = True
    if ks:
        rBin = 10
        for i in range( len( osIsoPairs ) ) :
            osHistos[i].Rebin(rBin)
            osHistos[i].Scale(1./osHistos[i].Integral())
        for i in range( len( ssIsoPairs ) ) :
            ssHistos[i].Rebin(rBin)
            ssHistos[i].Scale(1./ssHistos[i].Integral())
    print "\nROOT KS Tests"
    ''' SS vs OS '''
    log1 = []
    cnt = 0
    for i in range( len( ssIsoPairs ) ) :
        for j in range( len( osIsoPairs ) ) :
            n0 = "SSvsOS"
            n1 = "SS_%s->%s" % (ssIsoPairs[i][0], ssIsoPairs[i][1] )
            n2 = "OS_%s->%s" % (osIsoPairs[j][0], osIsoPairs[j][1] )
            log1.append( ksTest( shape, ssHistos[i], osHistos[j], n0, n1, n2 ) )
            cnt += 1

    ''' iso Binning '''
    log2 = []
    cnt = 0
    for i in range( len( ssIsoPairs )-1 ) :
        for j in range(i+1, len( ssIsoPairs ) ) :
            n0 = "SS"
            n1 = "%s->%s" % (ssIsoPairs[i][0], ssIsoPairs[i][1] )
            n2 = "%s->%s" % (ssIsoPairs[j][0], ssIsoPairs[j][1] )
            log2.append( ksTest( shape, ssHistos[i], ssHistos[j], n0, n1, n2 ) )
            cnt += 1
    log3 = []
    cnt = 0
    for i in range( len( osIsoPairs )-1 ) :
        for j in range(i+1, len( osIsoPairs ) ) :
            n0 = "OS"
            n1 = "%s->%s" % (osIsoPairs[i][0], osIsoPairs[i][1] )
            n2 = "%s->%s" % (osIsoPairs[j][0], osIsoPairs[j][1] )
            log3.append( ksTest( shape, osHistos[i], osHistos[j], n0, n1, n2 ) )
            cnt += 1
    print "\n\n"   

    cnt = 0
    for i in range( len( ssIsoPairs ) ) :
        for j in range( len( osIsoPairs ) ) :
            n0 = "SSvsOS"
            n1 = "SS_%s->%s" % (ssIsoPairs[i][0], ssIsoPairs[i][1] )
            n2 = "OS_%s->%s" % (osIsoPairs[j][0], osIsoPairs[j][1] )
            print "%20s %20s %20s KS: %3.4f" % (n0, n1, n2, log1[cnt])
            cnt += 1
    cnt = 0
    for i in range( len( ssIsoPairs )-1 ) :
        for j in range(i+1, len( ssIsoPairs ) ) :
            n0 = "SS"
            n1 = "%s->%s" % (ssIsoPairs[i][0], ssIsoPairs[i][1] )
            n2 = "%s->%s" % (ssIsoPairs[j][0], ssIsoPairs[j][1] )
            print "%20s %20s %20s KS: %3.4f" % (n0, n1, n2, log2[cnt])
            cnt += 1
    cnt = 0
    for i in range( len( osIsoPairs )-1 ) :
        for j in range(i+1, len( osIsoPairs ) ) :
            n0 = "OS"
            n1 = "%s->%s" % (osIsoPairs[i][0], osIsoPairs[i][1] )
            n2 = "%s->%s" % (osIsoPairs[j][0], osIsoPairs[j][1] )
            print "%20s %20s %20s KS: %3.4f" % (n0, n1, n2, log3[cnt])
            cnt += 1



if __name__ == '__main__' :

    #for shape in ['m_sv',]:# 'm_vis']:
    #    for zero in [False,]:# True] :
    #        if zero : n = 'zeroed'
    #        else : n = 'incNeg'
    shape = 'm_sv'
    n = 'incNeg'

    ssh = signalSamp( shape, 'SS' )
    ssHistos = getShapes( shape, 'SS', '', '' )
    osh = signalSamp( shape, 'OS' )
    osHistos = getShapes( shape, 'OS', '', '' )
    printYields( osHistos, ssHistos )

    
    runAllKS( osIsoPairs, ssIsoPairs, osHistos, ssHistos )
                
                







