import ROOT
import math
import util.cumulativeDist as CDF
ROOT.gROOT.SetBatch(True)

isoPairs = [
    ('Loose','Medium'),
    #('Loose','Tight'),
    #('Loose','VTight'),
    ('Medium','Tight'),
    #('Medium','VTight'),
    ('Tight','VTight'),
    ('VTight','')
    ]

def signalSamp( var, sign ) :
    print "\nSignal sample Var: %s    Sign: %s" % (var, sign)
    f = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%sIsoCut.root' % sign,'r')
    t = f.Get('tt_Histos')
    h = t.Get( var )
    h.SetFillColor( 0 )
    h.SetDirectory( 0 )
    return h

def getShapes( var, sign ) :
    histos = []
    for i,pair in enumerate(isoPairs) :
        f1 = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%s_%s_%s.root' % (sign, pair[1], pair[0]),'r')
        t1 = f1.Get('tt_Histos')
        h1 = t1.Get( var )
        h1.SetName( "%s%s" % (pair[0],pair[1]) )
        h1.SetDirectory( 0 )
        h1.SetFillColor( 0 )
        histos.append( h1 )
        f1.Close()
    return histos


def printYields( osHistos, ssh, ssHistos ) :
    ssSigInt = ssh.Integral()
    ssInts = []
    for h in ssHistos :
        ssInts.append( (h.Integral(),math.sqrt(h.Integral()),1./math.sqrt(h.Integral()) ) )
    osInts = []
    for h in osHistos :
        osInts.append( (h.Integral(),math.sqrt(h.Integral()),1./math.sqrt(h.Integral()) ) )
    for i,pair in enumerate(isoPairs) :
        ssWUncert = ssInts[i][1]
        print "SS %s %s yield = %3.2f +/- %3.2f" % (pair[0], pair[1], ssInts[i][0], ssWUncert)
        osWUncert = osInts[i][1]
        print "OS %s %s yield = %3.2f +/- %3.2f" % (pair[0], pair[1], osInts[i][0], osWUncert)
        #ssWUncert = ssInts[i][1]/ssInts[i][0]
        #print "SS %s %s yield = %3.2f +/- %3.2fper" % (pair[0], pair[1], ssInts[i][0], ssWUncert)
        #osWUncert = ssInts[i][1]/ssInts[i][0]
        #print "SS %s %s yield = %3.2f +/- %3.2fper" % (pair[0], pair[1], osInts[i][0], osWUncert)
    print "SS VTight yield = %3.2f +/- %3.2f\n" % (ssSigInt, math.sqrt(ssSigInt))

    #tags = {0:'MT/LM',1:'TVT/MT',2:'VT/TVT'}
    tags = {(0,1):'MT/LM',(0,2):'TVT/LT',(1,2):'TVT/MT',len(isoPairs)-1:'VT/TVT'}
    #tags = {0:'LT/LM',1:'LVT/LT',2:'MT/LVT',3:'MVT/MT',4:'TVT/MVT'}
    print "              SS                       OS"
    for i in range( len(isoPairs) ) :
        for j in range(i+1, len(isoPairs) ) :
            #if i == j : continue
            #if i+j > len(isoPairs) : continue
            #print "i:",i,"j:",j
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



def compareYield( osHistos, osh, ssh, ssHistos ) :
    ssSigInt = ssh.Integral()
    osSigInt = osh.Integral()
    ints = []
    for h in ssHistos :
        ints.append( (h.Integral(),math.sqrt(h.Integral()) ) )
    #print "OS Signal yield = %3.2f +/- %3.2f" % (osSigInt, math.sqrt(osSigInt))
    print "SS Signal yield = %3.2f +/- %3.2f" % (ssSigInt, math.sqrt(ssSigInt))
    for i,pair in enumerate(isoPairs) :
        sf = math.sqrt( (math.sqrt(ssSigInt)/ssSigInt)**2 + (ints[i][1]/ints[i][0])**2 )
        wUncert = ints[i][1]/ints[i][0]
        print "\n%s %s yield = %3.2f +/- %3.2fper" % (pair[0], pair[1], ints[i][0], wUncert)
        print " --- SF = %3.2f +/- %3.2fper" % (ssSigInt/ints[i][0], sf)
        fYield = (osHistos[i].Integral())*ssSigInt/ints[i][0]
        print " --- SF applied yield << %f +/- %3.2f>>" % (fYield, fYield*sf)


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
    print "%s: KS Prop = %f" % (n0, ksProb )
    c1 = ROOT.TCanvas( 'c1%s' % n0, 'c1', 600, 600 )
    p1 = ROOT.TPad('p1%s' % n0, 'p1', 0, 0, 1, 1 )
    p1.Draw()
    p1.SetGrid()
    p1.cd()
    
    h1.SetLineColor( ROOT.kRed )
    h1.SetTitle( '%s %s %s KS Prob = %f' % (n0, shape, zeroed, ksProb ) )
    h2.SetLineColor( ROOT.kBlue )
    h1.SetStats(0)
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
        
if __name__ == '__main__' :

    for shape in ['m_sv',]:# 'm_vis']:
        for zero in [False,]:# True] :
            if zero : n = 'zeroed'
            else : n = 'incNeg'

            ssh = signalSamp( shape, 'SS' )
            ssHistos = getShapes( shape, 'SS' )
            osh = signalSamp( shape, 'OS' )
            #print "\n ###   OS QCD Yield %f +/- %3.2f   ###" % (osh.Integral(), math.sqrt(osh.Integral()))
            osHistos = getShapes( shape, 'OS' )
            #compareYield( osHistos, osh, ssh, ssHistos )
            printYields( osHistos, ssh, ssHistos )
            ssCDFs = makeCDFs( ssHistos, 'SS', zero )
            osCDFs = makeCDFs( osHistos, 'OS', zero )
            ssSigCDF = CDF.CDF( ssh, zero, 'SS' )
            osSigCDF = CDF.CDF( osh, zero, 'OS' )
            #KSTests( ssSigCDF, ssCDFs, ssHistos )
            ksVals = KSTests( osSigCDF, osh.GetEntries(), osCDFs, osHistos )

            ''' rebin! '''
            ks = True
            if ks:
                rBin = 40
                for i in range( len( isoPairs ) ) :
                    osCDFs[i].Sumw2()
                    ssCDFs[i].Sumw2()
                    osCDFs[i].Rebin(rBin)
                    osCDFs[i].Scale(1./rBin)
                    ssCDFs[i].Rebin(rBin)
                    ssCDFs[i].Scale(1./rBin)
                    #osHistos[i].Sumw2()
                    #ssHistos[i].Sumw2()
                    osHistos[i].Rebin(rBin)
                    osHistos[i].Scale(1./osHistos[i].Integral())
                    ssHistos[i].Rebin(rBin)
                    ssHistos[i].Scale(1./ssHistos[i].Integral())
                ssSigCDF.Sumw2()
                osSigCDF.Sumw2()
                ssSigCDF.Rebin(rBin)
                ssSigCDF.Scale(1./rBin)
                osSigCDF.Rebin(rBin)
                osSigCDF.Scale(1./rBin)
                #ssh.Sumw2()
                #osh.Sumw2()
                ssh.Rebin(rBin)
                ssh.Scale(1./ssh.Integral())
                osh.Rebin(rBin)
                osh.Scale(1./osh.Integral())
    
                
                

                print "\nROOT KS Tests"
                ''' SS vs OS '''
                for i in range( len( isoPairs ) ) :
                    for j in range( len( isoPairs ) ) :
                        n0 = "SSvsOS"
                        n1 = "SS_%s->%s" % (isoPairs[i][0], isoPairs[i][1] )
                        n2 = "OS_%s->%s" % (isoPairs[j][0], isoPairs[j][1] )
                        ksTest( shape, ssHistos[i], osHistos[j], n0, n1, n2 )

                ''' iso Binning '''
                for i in range( len( isoPairs )-1 ) :
                    for j in range(i+1, len( isoPairs ) ) :
                        n0 = "SS"
                        n1 = "%s->%s" % (isoPairs[i][0], isoPairs[i][1] )
                        n2 = "%s->%s" % (isoPairs[j][0], isoPairs[j][1] )
                        ksTest( shape, ssHistos[i], ssHistos[j], n0, n1, n2 )
                for i in range( len( isoPairs )-1 ) :
                    for j in range(i+1, len( isoPairs ) ) :
                        n0 = "OS"
                        n1 = "%s->%s" % (isoPairs[i][0], isoPairs[i][1] )
                        n2 = "%s->%s" % (isoPairs[j][0], isoPairs[j][1] )
                        ksTest( shape, osHistos[i], osHistos[j], n0, n1, n2 )
                ksTest( shape, ssHistos[-1], ssh, 'SS', 'Tight->VTight', 'VTight' )
                print "T->VT vs Sig in SS %f" % ssh.KolmogorovTest( ssHistos[-1] ) 
                print "\n\n"   







