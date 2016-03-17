import ROOT
import math
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
    #('Loose','Tight'),
    #('Loose','VTight'),
    ('Medium','Tight'),
    #('Medium','VTight'),
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

def getShapes( var, sign, isoPairs, l1='', btag='' ) :
    histos = []
    #if sign == 'SS' : isoPairs = ssIsoPairs
    #if sign == 'OS' : isoPairs = osIsoPairs
    for i,pair in enumerate(isoPairs) :
        #f1 = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%s_%s_%s.root' % (sign, pair[1], pair[0]),'r')
        if pair != ('VTight','') :
            f1 = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%s%s_%s_%s%s.root' % (sign, l1, pair[1], pair[0], btag),'r')
        else :
            f1 = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%s%s_%s_%s.root' % (sign, l1, pair[0], btag),'r')
        #    print "File name: '../../meta/dataCardsBackgrounds/tt_qcdShape_%s%s_%s_%s%s.root'" %     (sign, '', pair[1], pair[0], btag)
        #    f1 = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%s%s_%s_%s%s.root' % (sign, '', pair[1], pair[0], btag),'r')
        t1 = f1.Get('tt_Histos')
        h1 = t1.Get( var )
        h1.SetName( "%s%s" % (pair[0],pair[1]) )
        h1.SetDirectory( 0 )
        h1.SetFillColor( 0 )
        histos.append( h1 )
        f1.Close()
    return histos

def printStats( h ) :
    print " -- Mean: %3.2f+/-%3.2f  StdDev: %3.2f+/-%3.2f  Skew: %3.2f+/-%3.2f Kurtosis %3.2f+/-%3.2f\n" % (h.GetMean(), h.GetMeanError(), h.GetStdDev(), h.GetStdDevError(), h.GetSkewness(), h.GetSkewness(11), h.GetKurtosis(), h.GetKurtosis(11) )

def printYields( osHistos, ssHistos, l1='', btag='', ssIsoPairs=['',] ) :
    isoPairs = osIsoPairs
    ssInts = []
    for h in ssHistos :
        ssInts.append( (h.Integral(),math.sqrt(h.Integral()),1./math.sqrt(h.Integral()) ) )
    osInts = []
    for h in osHistos :
        osInts.append( (h.Integral(),math.sqrt(h.Integral()),1./math.sqrt(h.Integral()) ) )
    for i,pair in enumerate(isoPairs) :
        ssWUncert = ssInts[i][1]
        print "SS %s %s yield = %3.2f+/-%3.2f" % (pair[0], pair[1], ssInts[i][0], ssWUncert)
        printStats( ssHistos[i] )
        osWUncert = osInts[i][1]
        print "OS %s %s yield = %3.2f+/-%3.2f" % (pair[0], pair[1], osInts[i][0], osWUncert)
        printStats( osHistos[i] )
    if ('VTight','') in ssIsoPairs :
        ssSigInt = ssHistos[-1].Integral()
        print "SS VTight yield = %3.2f+/-%3.2f" % (ssSigInt, math.sqrt(ssSigInt))
        printStats( ssHistos[-1] )
    print "\n"

    #if l1 == '' :
    #tags = {0:'MT/LM',1:'TVT/MT',2:'VT/TVT'}
    tags = {(0,1):'MT/LM',(0,2):'TVT/LT',(1,2):'TVT/MT',len(osIsoPairs)-1:'VT/TVT'}
    #tags = {0:'LT/LM',1:'LVT/LT',2:'MT/LVT',3:'MVT/MT',4:'TVT/MVT'}
    print "%s %s          SS                       OS" % (l1, btag)
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
        print "%s %s   SS/OS   %3.2f+/-%3.3f" % ( pair[0], pair[1], ratio, ratio*uncert )
    print "\n"


def ksTest( shape, h1, h2, n0, n1, n2, l1, btag, zeroed='' ) :
    ksProb = h1.KolmogorovTest( h2 )
    #print "%s: KS Prop = %3.2f" % (n0, ksProb )
    c1 = ROOT.TCanvas( 'c1%s' % n0, 'c1', 600, 600 )
    p1 = ROOT.TPad('p1%s' % n0, 'p1', 0, 0, 1, 1 )
    p1.Draw()
    p1.SetGrid()
    p1.cd()
    
    h1.SetLineColor( ROOT.kRed )
    h1.SetTitle( '%s %s %s KS Prob = %3.3f' % (n0, l1, btag, ksProb ) )
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
    
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/moreQCD/%s_%s_%s_%s_%s_%s%s.png' % (shape, n, l1, btag, n0,n1,n2))
    return ksProb
        
def runAllKS( osIsoPairs, ssIsoPairs, osHistos, ssHistos, l1, btag, normalize=True ) :
    ''' rebin! '''
    ks = True
    if ks:
        rBin = 10
        for i in range( len( osIsoPairs ) ) :
            osHistos[i].Rebin(rBin)
            if normalize :
                osHistos[i].Scale(1./osHistos[i].Integral())
        for i in range( len( ssIsoPairs ) ) :
            ssHistos[i].Rebin(rBin)
            if normalize :
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
            log1.append( ksTest( shape, ssHistos[i], osHistos[j], n0, n1, n2, l1, btag ) )
            cnt += 1

    ''' iso Binning '''
    log2 = []
    cnt = 0
    for i in range( len( ssIsoPairs )-1 ) :
        for j in range(i+1, len( ssIsoPairs ) ) :
            n0 = "SS"
            n1 = "%s->%s" % (ssIsoPairs[i][0], ssIsoPairs[i][1] )
            n2 = "%s->%s" % (ssIsoPairs[j][0], ssIsoPairs[j][1] )
            log2.append( ksTest( shape, ssHistos[i], ssHistos[j], n0, n1, n2, l1, btag ) )
            cnt += 1
    log3 = []
    cnt = 0
    for i in range( len( osIsoPairs )-1 ) :
        for j in range(i+1, len( osIsoPairs ) ) :
            n0 = "OS"
            n1 = "%s->%s" % (osIsoPairs[i][0], osIsoPairs[i][1] )
            n2 = "%s->%s" % (osIsoPairs[j][0], osIsoPairs[j][1] )
            log3.append( ksTest( shape, osHistos[i], osHistos[j], n0, n1, n2, l1, btag ) )
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

    print "\n\n"


def runAllPtCompKS( isoPairs, HPt1, HPt2, l1, sign, btag, normalize=True ) :
    ''' rebin! '''
    ks = True
    if ks:
        rBin = 10
        for i in range( len( isoPairs ) ) :
            HPt2[i].Rebin(rBin)
            if normalize :
                HPt2[i].Scale(1./HPt2[i].Integral())
        for i in range( len( isoPairs ) ) :
            HPt1[i].Rebin(rBin)
            if normalize :
                HPt1[i].Scale(1./HPt1[i].Integral())
    print "\nROOT KS Tests"
    ''' SS vs OS '''
    log1 = []
    cnt = 0
    for i in range( len( isoPairs ) ) :
        n0 = sign+"_Pt1GtrvsPt2Gtr"
        n1 = "Pt1Gtr_%s->%s" % (isoPairs[i][0], isoPairs[i][1] )
        n2 = "Pt2Gtr_%s->%s" % (isoPairs[i][0], isoPairs[i][1] )
        log1.append( ksTest( shape, HPt1[i], HPt2[i], n0, n1, n2, l1, btag ) )
        cnt += 1

    print "\n\n"   

    cnt = 0
    for i in range( len( isoPairs ) ) :
        n0 = "Pt1GtrvsPt2Gtr"
        n1 = "Pt1Gtr_%s->%s" % (isoPairs[i][0], isoPairs[i][1] )
        n2 = "Pt2Gtr_%s->%s" % (isoPairs[i][0], isoPairs[i][1] )
        print "%20s %20s %20s KS: %3.4f" % (n0, n1, n2, log1[cnt])
        cnt += 1

    print "\n\n"


if __name__ == '__main__' :

    #for shape in ['m_sv',]:# 'm_vis']:
    #    for zero in [False,]:# True] :
    #        if zero : n = 'zeroed'
    #        else : n = 'incNeg'
    #shape = 'm_sv'
    shape = 'mt_sv'
    n = 'incNeg'

    #ssh = signalSamp( shape, 'SS' )
    #osh = signalSamp( shape, 'OS' )

    #for l1 in ['', 'l1t', 'l1m'] :
    for l1 in ['l1m',] :
        #for btag in ['', 'BT'] :
        for btag in ['BT','BTL'] :
            ssIsoPairs_ = ssIsoPairs
            osIsoPairs_ = osIsoPairs
            #if l1 != '' : ssIsoPairs_ = osIsoPairs
            print "################"
            print "### %s %s ###" % (l1, btag)
            print "################"
            ssHistos = getShapes( shape, 'SS', ssIsoPairs_, l1, btag )
            osHistos = getShapes( shape, 'OS', osIsoPairs_, l1, btag )
            printYields( osHistos, ssHistos, l1, btag, ssIsoPairs_ )
#            runAllKS( osIsoPairs_, ssIsoPairs_, osHistos, ssHistos, l1, btag )
                
                
    #for l1 in ['l1t', 'l1m'] :
    #    btag = ''
    #    ssIsoPairs_ = ssIsoPairs
    #    osIsoPairs_ = osIsoPairs
    #    if l1 != '' : ssIsoPairs_ = osIsoPairs

    #    ssHPt1 = getShapes( shape, 'SS', ssIsoPairs_, 'Pt1Gtr'+l1, btag )
    #    osHPt1 = getShapes( shape, 'OS', osIsoPairs_, 'Pt1Gtr'+l1, btag )
    #    ssHPt2 = getShapes( shape, 'SS', ssIsoPairs_, 'Pt2Gtr'+l1, btag )
    #    osHPt2 = getShapes( shape, 'OS', osIsoPairs_, 'Pt2Gtr'+l1, btag )
    #    #for pt in ['Pt1Gtr', 'Pt2Gtr'] :
    #    print "################"
    #    print "### %s %s ###" % (l1, btag)
    #    print "################"
    #    print "\n OS "
    #    printYields( osHPt1, osHPt2, l1, btag, osIsoPairs_ )
    #    print "\n SS "
    #    printYields( ssHPt1, ssHPt2, l1, btag, ssIsoPairs_ )
    #    normalize = True
    #    runAllPtCompKS( osIsoPairs_, osHPt1, osHPt2, 'OS', l1, btag, normalize )
    #    runAllPtCompKS( ssIsoPairs_, ssHPt1, ssHPt2, 'SS', l1, btag, normalize )







