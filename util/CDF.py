import ROOT
from ROOT import gPad


def makeCDF( tree, var, nBins, low, high ) :
    h1 = ROOT.TH1F('h1','h1',nBins,low,high)
    tree.Draw( '%s>>h2(%i,%i,%i)' % (var, nBins, low, high) )
    h2 = gPad.GetPrimitive( 'h2' )
    h2.SaveAs('%sRaw.root' % var)
    cdf = 0
    for bin_ in range(1, nBins+1) :
        cdf += h2.GetBinContent( bin_ )
        h1.SetBinContent( bin_, cdf )
    h1.SetMaximum( h1.GetMaximum() * 1.4 )
    h1.SaveAs('%sCDF.root' % var)
    return h1


