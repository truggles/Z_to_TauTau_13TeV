import ROOT
import math
import util.cumulativeDist as CDF

isoPairs = [
    ('Loose','Medium'),
    ('Loose','Tight'),
    ('Loose','VTight'),
    ('Medium','Tight'),
    ('Medium','VTight'),
    ('Tight','VTight')]

def signalSamp( var, sign ) :
    print "\nSignal sample Var: %s    Sign: %s" % (var, sign)
    f = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_%sIsoCut.root' % sign,'r')
    t = f.Get('tt_Histos')
    h = t.Get( var )
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
        histos.append( h1 )
        f1.Close()
    return histos


def compareYield( osHistos, ssh, histos ) :
    sigInt = ssh.Integral()
    ints = []
    for h in histos :
        ints.append( (h.Integral(),math.sqrt(h.Integral()) ) )
    print "Signal yield = %3.2f +/- %3.2f" % (sigInt, math.sqrt(sigInt))
    for i,pair in enumerate(isoPairs) :
        sf = math.sqrt( (math.sqrt(sigInt)/sigInt)**2 + (ints[i][1]/ints[i][0])**2 )
        wUncert = ints[i][1]/ints[i][0]
        print "\n%s %s yield = %3.2f +/- %3.2fper" % (pair[0], pair[1], ints[i][0], wUncert)
        print " --- SF = %3.2f +/- %3.2fper" % (sigInt/ints[i][0], sf)
        print " --- SF applied yield << %f >>" % ((osHistos[i].Integral())*sigInt/ints[i][0])


def makeCDFs( histos, sign ) :
    cdfs = []
    for hist in histos :
        cdfs.append( CDF.CDF( hist, False, sign ) )
    return cdfs


def KSTests( cdf1, cdfs, histos ) :
    for i,cdf in enumerate(cdfs) :
        maxDiff = 0
        for k in range( 1, cdf.GetXaxis().GetNbins() + 2 ) :
            diff = abs(cdf.GetBinContent( k ) - cdf1.GetBinContent( k ))
            if diff > maxDiff : maxDiff = diff
        print "cdf %i: KS max diff %f" % (i, maxDiff)
        print " --- Crit Val: %f" % (maxDiff * histos[i].Integral())
        
if __name__ == '__main__' :
    ssh = signalSamp( 'm_sv', 'SS' )
    ssHistos = getShapes( 'm_sv', 'SS' )
    osh = signalSamp( 'm_sv', 'OS' )
    print "\n ###   OS QCD Yield %f +/- %3.2f   ###" % (osh.Integral(), math.sqrt(osh.Integral()))
    osHistos = getShapes( 'm_sv', 'OS' )
    #compareYield( osHistos, ssh, ssHistos )
    ssCDFs = makeCDFs( ssHistos, 'SS' )
    osCDFs = makeCDFs( osHistos, 'OS' )
    ssSigCDF = CDF.CDF( ssh, False, 'SS' )
    osSigCDF = CDF.CDF( osh, False, 'OS' )
    #KSTests( ssSigCDF, ssCDFs, ssHistos )
    KSTests( osSigCDF, osCDFs, osHistos )

    
    c1 = ROOT.TCanvas( 'c1', 'c1', 600, 600 )
    p1 = ROOT.TPad('p1', 'p1', 0, 0, 1, 1 )
    p1.Draw()
    p1.cd()
    osSigCDF.SetStats( 0 )
    osSigCDF.SetLineWidth( 2 )
    osSigCDF.Draw('hist')
    for i,h in enumerate(osCDFs) :
        h.SetLineColor( i )
        h.Draw('hist same')
    p1.BuildLegend()
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/moreQCD/osCDFs.png')








