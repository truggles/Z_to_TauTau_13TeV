import ROOT
from ROOT import gROOT

def qcdFit() :
    f = ROOT.TFile('roots/OSvsSS.root','r')
    h = f.Get('OSvsSS')
    
    func = ROOT.TF2( 'func', '[0] + (x * [1]) +(y *[2])' )
    f1 = gROOT.GetFunction('func' )
    f1.SetParName( 0, 'Intercept' )
    f1.SetParName( 1, 'x-slope' )
    f1.SetParName( 2, 'y-slope' )
    f1.SetParameter( 0, 99 )
    f1.SetParameter( 1, 99 )
    f1.SetParameter( 2, 99 )
    h.Fit('func', 'R' )
    

qcdFit()
