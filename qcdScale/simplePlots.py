import ROOT

h1 = ROOT.TH1F('h1', 'Tau 1 Iso > 3 && SS', 3, 0, 2)
h2 = ROOT.TH1F('h2', 'Tau 1 Iso > 3 && OS', 3, 0, 2)
h3 = ROOT.TH1F('h3', 'Tau 1 Iso < 1 && SS', 3, 0, 2)
h4 = ROOT.TH1F('h4', 'Tau 1 Iso < 1 && OS', 3, 0, 2)

h1.SetBinContent( 1, 3442)
h1.SetBinContent( 2, 11124)
h1.SetBinContent( 3, 58842)
h1.SetLineColor( ROOT.kRed )
h1.Scale( 1 / h1.Integral() )
h1.SetLineWidth( 2 )
h1.SetStats( 0 )

h2.SetBinContent( 1, 4016)
h2.SetBinContent( 2, 12676)
h2.SetBinContent( 3, 62543)
h2.SetLineColor( ROOT.kBlue )
h2.Scale( 1 / h2.Integral() )
h2.SetLineWidth( 2 )

h3.SetBinContent( 1, 472.5)
h3.SetBinContent( 2, 1905.4)
h3.SetBinContent( 3, 287.8)
h3.SetLineColor( ROOT.kMagenta )
h3.Scale( 1 / h3.Integral() )
h3.SetLineWidth( 2 )

h4.SetBinContent( 1, 679.6)
h4.SetBinContent( 2, 2773.8)
h4.SetBinContent( 3, 361.3)
h4.SetLineColor( ROOT.kYellow )
h4.Scale( 1 / h4.Integral() )
h4.SetLineWidth( 2 )

c1 = ROOT.TCanvas('c1','c1',600,600)
p1 = ROOT.TPad('p1','p1',0,0,1,1)
p1.Draw()
p1.cd()
h1.Draw('hist')
h2.Draw('same')
h3.Draw('same')
h4.Draw('same')

#p1.BuildLegend()
#p1.Update()
c1.SaveAs('/afs/cern.ch/user/t/truggles/www/qcdScale/test.png')


#h1 = ROOT.TH1F('Tau 1 Iso > 3 && SS', 'h1', 3, 0, 2)
#h2 = ROOT.TH1F('Tau 1 Iso > 3 && OS', 'h2', 3, 0, 2)
#h3 = ROOT.TH1F('Tau 1 Iso < 1 && SS', 'h3', 3, 0, 2)
#h4 = ROOT.TH1F('Tau 1 Iso < 1 && SS', 'h4', 3, 0, 2)
#
#h1.SetBinContent( 1, 3442)
#h1.SetBinContent( 2, 11124)
#h1.SetBinContent( 3, 58842)
#
#h2.SetBinContent( 1, )
#h2.SetBinContent( 2, )
#h2.SetBinContent( 3, )
#
#h3.SetBinContent( 1, )
#h3.SetBinContent( 2, )
#h3.SetBinContent( 3, )
#
#h4.SetBinContent( 1, )
#h4.SetBinContent( 2, )
#h4.SetBinContent( 3, )
