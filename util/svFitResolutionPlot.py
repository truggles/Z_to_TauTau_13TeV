import ROOT
ROOT.gROOT.SetBatch(True)

f1 = ROOT.TFile('DYInc_Tight.root','r')
t1 = f1.Get('Ntuple')
f2 = ROOT.TFile('ggHInc_Tight.root','r')
t2 = f2.Get('Ntuple')

mini = 0
maxi = 300
nBins=75
h1 = ROOT.TH1F('ztt_m_vis','ztt_m_vis',nBins,mini,maxi)
h2 = ROOT.TH1F('ztt_m_sv','ztt_m_sv',nBins,mini,maxi)
t1.Draw('m_visCor >> ztt_m_vis','XSecLumiWeight')
t1.Draw('m_sv >> ztt_m_sv','XSecLumiWeight')
# XSecLumiWeight

h3 = ROOT.TH1F('ggH_m_vis','ggH_m_vis',nBins,mini,maxi)
h4 = ROOT.TH1F('ggH_m_sv','ggH_m_sv',nBins,mini,maxi)
t2.Draw('m_visCor >> ggH_m_vis','XSecLumiWeight')
t2.Draw('m_sv >> ggH_m_sv','XSecLumiWeight')


c = ROOT.TCanvas('c1','c1',400,400)
c.cd()
p = ROOT.TPad('p1','p1',0,0,1,1)
p.Draw()
p.cd()

h1.Scale( 1. / h1.Integral() )
h2.Scale( 1. / h2.Integral() )
h3.Scale( 1. / h3.Integral() )
h4.Scale( 1. / h4.Integral() )


maxi = max( h1.GetMaximum(), h3.GetMaximum() )
h1.SetMaximum( maxi * 1.2 )
h1.Draw('HIST')
h3.SetLineColor(ROOT.kRed)
h3.Draw('HIST SAME')
#l = p.BuildLegend()
#l.Draw()
c.SaveAs('/afs/cern.ch/user/t/truggles/www/SM-HTT_May04/m_vis.png')

c.Clear()
p = ROOT.TPad('p1','p1',0,0,1,1)
p.Draw()
p.cd()
maxi = max( h2.GetMaximum(), h4.GetMaximum() )
h2.SetMaximum( maxi * 1.2 )
h2.Draw('HIST')
h4.SetLineColor(ROOT.kRed)
h4.Draw('HIST SAME')
#l = p.BuildLegend()
#l.Draw()
c.SaveAs('/afs/cern.ch/user/t/truggles/www/SM-HTT_May04/m_sv.png')
