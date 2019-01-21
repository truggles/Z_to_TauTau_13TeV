import ROOT
ROOT.gROOT.SetBatch(True)


def get_and_fit( c, d, var, app ) :
    hist = d.Get(var)
    print hist.Integral()
    hist.Scale( 1. / hist.Integral() )
    hist.SetMinimum( 0. )
    hist.GetXaxis().SetTitle('m_{A} (GeV)')
    hist.GetYaxis().SetTitle('A.U.')
    fitResults = []

    # Fit +/- 70 GeV around max
    dist =70
    #hist_max = hist.GetBinCenter( hist.GetMaximumBin() )
    hist_max = 300
    hist_top = 450
    hist_bottom = 50
    #if var == 'AMassConst' :
    #    hist_max = 295
    #    dist = 15
    #    dist = 20
    #if var == 'A_Mass' :
    #    hist_max = 285
    #    dist = 50
    #if var == 'Mass' :
    #    hist_max = 220
    #    dist = 60
    #    hist_top = 350
    hist_max = hist.GetMean(1)
    if var == 'AMassConst' :
        dist = 20
    if var == 'A_Mass' :
        dist = 50
    if var == 'Mass' :
        dist = 60
        hist_top = 350
    hist.GetXaxis().SetRangeUser( hist_bottom, hist_top )
    shape = ROOT.TF1("shape", "gaus(0)", hist_max - dist, hist_max + dist )
    shape.SetParameters(hist_max, 10, 10)
    

    hist.Fit(shape, "R")
    new_fit = ROOT.TF1("shape", "gaus(0)", hist_bottom, hist_top )
    new_fit.SetParameters( shape.GetParameter(0), shape.GetParameter(1), shape.GetParameter(2) )
    new_fit.SetLineColor( ROOT.kBlue )
    new_fit.SetLineWidth( 2 )
    new_fit.Draw("same")
    hist.GetFunction("shape").SetLineColor(ROOT.kRed)
    hist.GetFunction("shape").SetLineWidth(hist.GetLineWidth()*2)

    fitResult = hist.GetFunction("shape")
    i = 0
    fitResults.append( ROOT.TLatex(.15, .7, "Gaussian Fit:" ))
    fitResults.append( ROOT.TLatex(.15, .66-i*.13, "#mu: "+format(fitResult.GetParameter(1), '.3g')))
    fitResults.append( ROOT.TLatex(.15, .62-i*.13, "#sigma: "+format(fitResult.GetParameter(2), '.3g')))
    fitResults.append( ROOT.TLatex(.15, .58-i*.13, "mean: "+format(hist.GetMean(1), '.3g')))
    fitResults.append( ROOT.TLatex(.15, .54-i*.13, "fit range: [%i, %i]" % (hist_max - dist, hist_max + dist)))
    res = fitResult.GetParameter(2) / hist.GetMean(1)
    fitResults.append( ROOT.TLatex(.15, .48-i*.13, "#sigma/#mu: "+format( res, '.3g')))
    for i in range( len(fitResults) ) :
        fitResults[i].SetTextSize(0.045)
        fitResults[i].SetTextFont(42)
        fitResults[i].SetNDC()
        fitResults[i].Draw()
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/Jan21_resolution/%s_%s.png' % (app, var))
    return res


#fBase = '/afs/cern.ch/user/j/jheikkil/public/ForTyler/resolution/'
fBase = 'mass_resolution/'
#for name in ['Aconstr', 'AsvFit', 'Avis'] :
res_map = {}
for var in ['Mass', 'A_Mass', 'AMassConst'] :
    res_map[ var ] = [0., 0., 999.]
    for channel in ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'] :
        f = ROOT.TFile(fBase+'azh300_'+channel+'.root', 'r')
        d = f.Get( channel+'_Histos' )
        c = ROOT.TCanvas('c','c',600,400)
        pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
        pad1.Draw()
        pad1.cd()
    
        res = get_and_fit( c, d, var, channel )
        res_map[ var ][0] +=  res
        if res_map[ var ][1] < res : res_map[ var ][1] = res
        if res_map[ var ][2] > res : res_map[ var ][2] = res

for k, v in res_map.iteritems() :
    print "Var: %15s  avg: %.3f   max: %.3f   min %.3f" % ( k, v[0]/8., v[1], v[2])
