import ROOT
ROOT.gROOT.SetBatch(True)


def get_and_fit( c, f, name ) :
    hist = f.Get('mmmt_Histos/'+name)
    print hist.Integral()
    hist.Scale( 1. / hist.Integral() )
    hist.SetMinimum( 0. )
    hist.GetXaxis().SetTitle('m_{A} (GeV)')
    hist.GetYaxis().SetTitle('A.U.')
    fitResults = []
    fitResults.append( ROOT.TLatex(.2, .7, "Gaussian Fit:" ))

    # Fit +/- 70 GeV around max
    dist = 70
    hist_max = hist.GetBinCenter( hist.GetMaximumBin() )
    shape = ROOT.TF1("shape", "gaus(0)", hist_max - dist, hist_max + dist )
    shape.SetParameters(hist_max, 10, 10)

    hist.Fit(shape, "R")
    hist.GetFunction("shape").SetLineColor(ROOT.kRed)
    hist.GetFunction("shape").SetLineWidth(hist.GetLineWidth()*2)

    fitResult = hist.GetFunction("shape")
    i = 0
    fitResults.append( ROOT.TLatex(.2, .66-i*.13, "#mu: "+format(fitResult.GetParameter(1), '.3g')))
    #fitResults.append( ROOT.TLatex(.2, .62-i*.13, "#sigma: "+format(ROOT.TMath.Sqrt(.5*abs(fitResult.GetParameter(2))), '.3g')))
    fitResults.append( ROOT.TLatex(.2, .62-i*.13, "#sigma: "+format(fitResult.GetParameter(2), '.3g')))
    fitResults.append( ROOT.TLatex(.2, .58-i*.13, "mean: "+format(hist.GetMean(1), '.3g')))
    for i in range( len(fitResults) ) :
        fitResults[i].SetTextSize(0.045)
        fitResults[i].SetTextFont(42)
        fitResults[i].SetNDC()
        fitResults[i].Draw()
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/aug11_resolution/%s.png' % name)



f = ROOT.TFile('azh3July08AZH/azh300_mmmt.root','r')

c = ROOT.TCanvas('c','c',600,400)
pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
pad1.Draw()
pad1.cd()

get_and_fit( c, f, 'Mass' )
get_and_fit( c, f, 'A_Mass' )
get_and_fit( c, f, 'AMassConst' )
