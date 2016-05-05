import ROOT
from ROOT import gPad

ROOT.gROOT.SetBatch(True)

osFile = ROOT.TFile('qcdOS.root','r')
osT = osFile.Get('tt_Histos')


#osT.Draw('qcdm_vistt')
#h1 = ROOT.TH1F('h1', 'h1', 35, 0, 350)
##h1 = ROOT.TH1()
#osT.Draw('m_vis>>h1')#(35,0,350)')
#h1 = gPad.GetPrimitive( 'h1' )
#h1.Draw()
h1 = osT.Get('m_vis')
for i in range( h1.GetNbinsX()+1 ):
    if h1.GetBinContent( i ) < 0 :
        h1.SetBinContent( i, 0 )
h1.SetLineWidth( 4 )
h1.SetLineColor( ROOT.kRed )
h1.Scale( 1 / h1.Integral() )


toPlot = {
    'h2' : 'Z_SS==1 && iso_1<.8 && iso_2<.8',
    'h3' : 'Z_SS==1 && iso_1<.8 && iso_2<3',
    'h4' : 'Z_SS==1 && iso_1<.8 && iso_2<3 && iso_2>.8',
    'h5' : 'Z_SS==1 && iso_1<.8 && iso_2<10 && iso_2>.8',
    'h6' : 'Z_SS==1 && iso_1<2 && iso_2<10 && iso_2>.8',
    'h7' : 'Z_SS==1 && iso_1<10 && iso_2<10',
    }
histos = {}
colors = [ROOT.kCyan,ROOT.kBlue,ROOT.kGreen,ROOT.kGreen-3,ROOT.kYellow,ROOT.kBlack]

dFile = ROOT.TFile('dataTT.root','r')
dT = dFile.Get('Ntuple')

count = 0
for key in toPlot.keys() :
    dT.Draw('m_vis>>%s(35,0,350)' % key, '%s' % toPlot[key])
    histos[ key ] = gPad.GetPrimitive( key )
    histos[ key ].Scale( 1 / histos[key].Integral() )
    histos[ key ].Draw('same')
    histos[ key ].SetLineColor( colors[count] )
    histos[ key ].SetLineWidth( 2 )
    count += 1


c1 = ROOT.TCanvas( 'c1', 'c1', 600, 600 )
p1 = ROOT.TPad('p1', 'p1', 0, 0, 1, 1 )
p1.Draw()
p1.cd()

h1.Draw('hist')
for key in histos.keys() :
    histos[key].Draw('same')

p1.BuildLegend()

c1.SaveAs('/afs/cern.ch/user/t/truggles/www/qcdScale/qcdShapes.png')


