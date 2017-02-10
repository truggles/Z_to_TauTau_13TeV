import ROOT
from util.jetEnergyScale import getUncerts
from util.ratioPlot import ratioPlot



uncertNames = getUncerts()



c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
#p1 = ROOT.TPad('p1', 'p1', 0, 0, 1, 1)
#p1.Draw()
#p1.cd()
smlPadSize = .35
pads = ratioPlot( c1, 1-smlPadSize )
pad1 = pads[0]
ratioPad = pads[1]
ratioPad.SetTopMargin(0.00)
ratioPad.SetBottomMargin(0.3)
pad1.SetBottomMargin(0.00)
ratioPad.SetGridy()


ROOT.gROOT.SetBatch(True)

#for name in ['dyJets', ]:#'ggH125', 'qqH125'] :
for name in ['ggH125',]:# 'qqH125'] :
    f = ROOT.TFile('/data/truggles/JES_merge/%s.root' % name)
    t = f.Get('tt/final/Ntuple')

    # Closure test
    #h1 = ROOT.TH2D('h1', 'Closure Test', 25,0,300,25,-.01,.03)
    #t.Draw("((jet1PtJESClosure_Up-jet1PtJESTotal_Up)/(jet1Pt)):jet1Pt >> h1")
    #h1.Draw()
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/JES_Tests/%s_closure.png' % name)

    
    for shape in uncertNames : 
        pad1.cd()
        h1 = ROOT.TH1D('shape', 'mjj %s' % shape, 25,0,500)
        h2 = ROOT.TH1D('shapeUp', 'mjj %s' % shape, 25,0,500)
        h3 = ROOT.TH1D('shapeDown', 'mjj %s' % shape, 25,0,500)
        t.Draw('vbfMass >> shape')
        t.Draw('vbfMass_Jet%sUp >> shapeUp' % shape)
        t.Draw('vbfMass_Jet%sDown >> shapeDown' % shape)
        h1.SetLineColor(ROOT.kBlack)
        h2.SetLineColor(ROOT.kBlue)
        h3.SetLineColor(ROOT.kRed)
        h1.SetMaximum( h1.GetMaximum() * 1.2 )
        h1.Draw()
        h2.Draw('SAME')
        h3.Draw('SAME')
        leg = pad1.BuildLegend()
        leg.Draw()

        # Print integrals on png
        intNom = h1.Integral()
        intUp = h2.Integral()
        intDown = h3.Integral()
        #text1 = ROOT.TText(.4,.6,"" )
        text1 = ROOT.TText()
        text1.SetTextSize(0.035)
        text1.DrawTextNDC(.15,.85,"Up/Nom.=%.5f  Down/Nom.=%.5f" % (intUp/intNom, intDown/intNom) )

        # ratio
        ratioPad.cd()
        ratioHist1 = ROOT.TH1D('ratio %s Up' % shape, 'ratio', 25,0,500 )
        ratioHist1.Sumw2()
        ratioHist1.Add( h1 )
        ratioHist1.Divide( h2 )
        ratioHist1.SetMaximum( 1.05 )
        ratioHist1.SetMinimum( 0.95 )
        if 'Total' in shape or 'Closure' in shape :
            ratioHist1.SetMaximum( 1.2 )
            ratioHist1.SetMinimum( 0.80 )
        ratioHist1.SetLineColor( ROOT.kBlue )
        #ratioHist1.SetMarkerStyle( 21 )
        ratioHist1.GetYaxis().SetTitle('Nominal / Shift')
        #ratioHist1.GetYaxis().SetTitleSize( ratioHist1.GetYaxis().GetLabelSize() * 3. )
        ratioHist1.GetXaxis().SetTitle('di-jet Mass [GeV]')
        ratioHist1.GetYaxis().SetTitleSize( ratioHist1.GetYaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
        ratioHist1.GetYaxis().SetTitleOffset( smlPadSize*1.5 )
        ratioHist1.GetXaxis().SetTitleSize( ratioHist1.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )

        ratioHist1.Draw('hist')
        ratioHist2 = ROOT.TH1D('ratio %s Down' % shape, 'ratio', 25,0,500 )
        ratioHist2.Sumw2()
        ratioHist2.Add( h1 )
        ratioHist2.Divide( h3 )
        ratioHist2.SetLineColor( ROOT.kRed )
        #ratioHist2.SetMarkerStyle( 21 )
        ratioHist2.Draw('same hist')

        #p1.SetLogy()
        c1.SaveAs('/afs/cern.ch/user/t/truggles/www/JES_Tests2/%s_%s_mjj.png' % (name, shape))
        del h1,h2,h3









