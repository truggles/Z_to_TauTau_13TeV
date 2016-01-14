import ROOT
from ROOT import gPad
from util.CDF import makeCDF

#ROOT.gROOT.SetBatch(True)
dataF = ROOT.TFile('dataTT.root','r')
data = dataF.Get('Ntuple')
mcF = ROOT.TFile('mcTT.root','r')
mc = mcF.Get('Ntuple')

if __name__ == '__main__' :

    h1 = makeCDF( data, 'iso_1', 70, 3, 10 )
    print h1.GetBinContent( 70 )
    print h1.GetBinContent( 10 )
    print h1.GetBinContent( 30 )

    h2 = makeCDF( data, 'iso_2', 70, 3, 10 )
    print h2.GetBinContent( 70 )
    print h2.GetBinContent( 15 )
    print h2.GetBinContent( 40 )
