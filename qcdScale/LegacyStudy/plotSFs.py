import ROOT
import math
import util.cumulativeDist as CDF
ROOT.gROOT.SetBatch(True)

isoPairs = [
    ('Loose','Medium'),
    ('Loose','Tight'),
    ('Loose','VTight'),
    ('Medium','Tight'),
    ('Medium','VTight'),
    ('Tight','VTight')
    ]

def signalSamp( var, sign ) :
    print "\nSignal sample Var: %s    Sign: %s" % (var, sign)
    f = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%sIsoCutBT.root' % sign,'r')
    t = f.Get('tt_Histos')
    h = t.Get( var )
    h.SetDirectory( 0 )
    return h

def getShapes( var, sign ) :
    histos = []
    for i,pair in enumerate(isoPairs) :
        f1 = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%s_%s_%sBT.root' % (sign, pair[1], pair[0]),'r')
        t1 = f1.Get('tt_Histos')
        h1 = t1.Get( var )
        h1.SetName( "%s%s" % (pair[0],pair[1]) )
        h1.SetDirectory( 0 )
        histos.append( h1 )
        f1.Close()
    return histos


def compareYield( osHistos, osh, ssh, histos ) :
    ssSigInt = ssh.Integral()
    osSigInt = osh.Integral()
    ints = []
    for h in histos :
        ints.append( (h.Integral(),math.sqrt(h.Integral()) ) )
    print "OS Signal yield = %3.2f +/- %3.2f" % (osSigInt, math.sqrt(osSigInt))
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
        
if __name__ == '__main__' :

    for shape in ['m_sv', 'm_vis']:
        for zero in [True,]:# False] :
            if zero : n = 'zeroed'
            else : n = 'incNeg'

            ssh = signalSamp( shape, 'SS' )
            ssHistos = getShapes( shape, 'SS' )
            osh = signalSamp( shape, 'OS' )
            print "\n ###   OS QCD Yield %f +/- %3.2f   ###" % (osh.Integral(), math.sqrt(osh.Integral()))
            osHistos = getShapes( shape, 'OS' )
            compareYield( osHistos, osh, ssh, ssHistos )
            ssCDFs = makeCDFs( ssHistos, 'SS', zero )
            osCDFs = makeCDFs( osHistos, 'OS', zero )
            ssSigCDF = CDF.CDF( ssh, zero, 'SS' )
            osSigCDF = CDF.CDF( osh, zero, 'OS' )
            #KSTests( ssSigCDF, ssCDFs, ssHistos )
            ksVals = KSTests( osSigCDF, osh.GetEntries(), osCDFs, osHistos )
        
            
            c1 = ROOT.TCanvas( 'c1', 'c1', 1000, 1200 )
            p1 = ROOT.TPad('p1', 'p1', 0, 0, 1, 1 )
            p1.Draw()
            p1.cd()
            osSigCDF.SetStats( 0 )
            osSigCDF.SetLineWidth( 2 )
            osSigCDF.SetLineColor( ROOT.kBlack )
            osSigCDF.SetTitle( "%s %s" % (shape, n))
            osSigCDF.Draw('hist')
            for i,h in enumerate(osCDFs) :
                h.SetLineColor( i+1 )
                h.Draw('hist same')
        
            ''' Build the legend explicitly so we can specify marker styles '''
            legend = ROOT.TLegend(0.50, 0.15, 0.90, 0.5)
            legend.SetMargin(0.3)
            #legend.SetBorderSize(0)
            legend.AddEntry( osSigCDF, "OS Signal", 'l')
            for i,cdf in enumerate(osCDFs) :
                legend.AddEntry( cdf, "%s-%s KS=%f" % (isoPairs[i][0],isoPairs[i][1],ksVals[i]), 'l')
            legend.Draw()
        
            c1.SaveAs('/afs/cern.ch/user/t/truggles/www/moreQCD/osCDFs_%s_%s.png' % (shape, n))








