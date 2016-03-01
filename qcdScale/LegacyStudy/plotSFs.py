import ROOT
import math
import util.cumulativeDist as CDF

def isoLeg( var ) :
    f = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_SSIsoCut.root','r')
    t = f.Get('tt_Histos')
    h = t.Get( var )
    ssInt = h.Integral()

    ints = []
    
    isoPairs = [
        ('Loose','Medium'),
        ('Loose','Tight'),
        ('Loose','VTight'),
        ('Medium','Tight'),
        ('Medium','VTight'),
        ('Tight','VTight')]
    
    histos = []
    for i,pair in enumerate(isoPairs) :
        f1 = ROOT.TFile('../../meta/dataCardsBackgrounds/tt_qcdShape_SS_%s_%s.root' % (pair[1], pair[0]),'r')
        t1 = f1.Get('tt_Histos')
        h1 = t1.Get( var )
        h1.SetName( "%s%s" % (pair[0],pair[1]) )
        h1.SetDirectory( 0 )
        histos.append( h1 )
        #print "%s->%s KS Test: %f" % (pair[0],pair[1],h1.KolmogorovTest(h))
        int_ = histos[i].Integral()
        ints.append( (int_, math.sqrt( int_ ) ) )
        f1.Close()

    print "\n   Results for ",var
    print "Signal yield = %3.2f +/- %3.2f" % (ssInt, math.sqrt(ssInt))
    for i,pair in enumerate(isoPairs) :
        sf = math.sqrt( (math.sqrt(ssInt)/ssInt)**2 + (ints[i][1]/ints[i][0])**2 )
        print "pair %8s %8s yield = %3.2f +/- %3.2fpercent .... SF = %3.2f +/- %3.2fpercent" % (pair[0], pair[1], ints[i][0], ints[i][1]/ints[i][0], ssInt/ints[i][0], sf)

    sigCDF = CDF.CDF( h )
    cdfs = []
    for hist in histos :
        cdfs.append( CDF.CDF( hist ) )

    for i,cdf in enumerate(cdfs) :
        maxDiff = 0
        for k in range( 1, cdf.GetXaxis().GetNbins() + 2 ) :
            diff = cdf.GetBinContent( k ) - sigCDF.GetBinContent( k )
            if diff > maxDiff : maxDiff = diff
        print "cdf %i: KS max diff %f" % (i, maxDiff)


if __name__ == '__main__' :

    isoLeg( 'iso_1' )






