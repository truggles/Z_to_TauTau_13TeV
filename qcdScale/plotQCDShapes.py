import ROOT
from ROOT import gPad

ROOT.gROOT.SetBatch(True)


def getHisto( var, file_, folder, color ) :
    f = ROOT.TFile( file_ ,'r')
    d1 = f.Get( folder )
    h1 = d1.Get( var )
    print file_,color,h1.Integral()
    for i in range( h1.GetNbinsX()+1 ):
        if h1.GetBinContent( i ) < 0 :
            h1.SetBinContent( i, 0 )
    h1.SetLineWidth( 4 )
    h1.SetLineColor( color )
    h1.Scale( 1 / h1.Integral() )
    h1.SetDirectory( 0 )
    #print var,h1.Integral()
    return h1

    #osFile = ROOT.TFile('qcdOS.root','r')
    #osT = osFile.Get('tt_Histos')
    #h1 = osT.Get('m_vis')
    #for i in range( h1.GetNbinsX()+1 ):
    #    if h1.GetBinContent( i ) < 0 :
    #        h1.SetBinContent( i, 0 )
    #h1.SetLineWidth( 4 )
    #h1.SetLineColor( ROOT.kRed )
    #h1.Scale( 1 / h1.Integral() )

#toPlot = {
#    'h2' : 'Z_SS==0 && iso_1<1. && iso_2<1.',
#    'h3' : 'Z_SS==0 && iso_1<1. && iso_2<3',
#    'h4' : 'Z_SS==0 && iso_1<1. && iso_2<3 && iso_2>1.',
#    'h5' : 'Z_SS==0 && iso_1<1. && iso_2<10 && iso_2>1.',
#    'h6' : 'Z_SS==0 && iso_1<2 && iso_2<10 && iso_2>1.',
#    'h7' : 'Z_SS==0 && iso_1<10 && iso_2<10',
#    }
#histos = {}
#colors = [ROOT.kCyan,ROOT.kBlue,ROOT.kGreen,ROOT.kGreen-3,ROOT.kYellow,ROOT.kBlack]
#
#dFile = ROOT.TFile('dataTT.root','r')
#dT = dFile.Get('Ntuple')
#
#count = 0
#for key in toPlot.keys() :
#    dT.Draw('m_vis>>%s(35,0,350)' % key, '%s' % toPlot[key])
#    histos[ key ] = gPad.GetPrimitive( key )
#    histos[ key ].Scale( 1 / histos[key].Integral() )
#    histos[ key ].Draw('same')
#    histos[ key ].SetLineColor( colors[count] )
#    histos[ key ].SetLineWidth( 2 )
#    count += 1
vars_ = [
    ( 'qcdOS.root', ROOT.kRed ),
    ( '../meta/dataCardsBackgrounds/tt_qcdShape_SSsig.root', ROOT.kBlue ),
    ( '../meta/dataCardsBackgrounds/tt_qcdShape_OSsig.root', ROOT.kGreen ),
    ( '../meta/dataCardsBackgrounds/tt_qcdShape_SSl2loose.root', ROOT.kCyan ),
    ( '../meta/dataCardsBackgrounds/tt_qcdShape_OSl2loose.root', ROOT.kOrange ),
]


histos = []
for var in vars_ :
    histos.append( getHisto( 'm_vis', var[0], 'tt_Histos', var[1] ) )
    #print 'x',histos[-1].Integral()

c1 = ROOT.TCanvas( 'c1', 'c1', 600, 600 )
p1 = ROOT.TPad('p1', 'p1', 0, 0, 1, 1 )
p1.Draw()
p1.cd()

#h1.Draw('hist')
count = 0
for h in histos :
    #print "hi",h.Integral()
    if count == 0 : h.Draw('hist')
    else: h.Draw('same')
    count += 1

p1.BuildLegend()

c1.SaveAs('/afs/cern.ch/user/t/truggles/www/qcdScale/qcdShapesNew.png')


