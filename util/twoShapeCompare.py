import ROOT
from analysisPlots import getPlotDetails
from ROOT import gPad, gStyle
from ratioPlot import ratioPlot
import os
import pyplotter.tdrstyle as tdr
from util.helpers import checkDir

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()
ROOT.gStyle.SetOptStat(1111)
cmsLumi = float(os.getenv('LUMI'))
print "Lumi = %i" % cmsLumi

def drawCMSString( title ) :
    cmsString = ROOT.TLatex(
        gPad.GetAbsXlowNDC()+gPad.GetAbsWNDC()-gPad.GetLeftMargin(),
        gPad.GetAbsYlowNDC()+gPad.GetAbsHNDC()-gPad.GetTopMargin()+0.005,
        title )
    cmsString.SetTextFont(42)
    cmsString.SetTextSize(0.03)
    cmsString.SetNDC(1)
    cmsString.SetTextAlign(31)
    cmsString.Draw()
    return cmsString


qcdSF = 519./3169. # loose to tight QCD SF

f1name = 'dataCards3May02_FakeFactors/QCD_tt.root'
f2name = 'meta/dataCardsBackgrounds/tt_qcdShape_OSl1m_VTight_LooseZTT.root'
dname = 'tt_Histos'
pdet = getPlotDetails( 'tt' )

f1 = ROOT.TFile(f1name, 'r')
f2 = ROOT.TFile(f2name, 'r')

vars1 = f1.Get('tt_Histos').GetListOfKeys()
vars2 = f2.Get('tt_Histos').GetListOfKeys()
v1s = [] 
v2s = [] 
for v in vars1 :
     v1s.append(v.GetName())
for v in vars1 :
     v2s.append(v.GetName())

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
smlPadSize = .25
pads = ratioPlot( c1, 1-smlPadSize )
p1 = pads[0]
ratioPad = pads[1]
ratioPad.SetTopMargin(0.00)
ratioPad.SetBottomMargin(0.3)
p1.SetBottomMargin(0.00)
ratioPad.SetGridy()
#p1 = ROOT.TPad('p1', 'p1', 0, 0, 1, 1)
#p1.Draw()
#p1.cd()

pdir = '/afs/cern.ch/user/t/truggles/www/fakeFactor/overlapPlots/'
checkDir(pdir)
for v in v1s :
    if v in v2s :
        # 1 = un-rebinned, range not set, 2 = post work
        h1 = f1.Get('tt_Histos/'+v)
        h1.Rebin( pdet[v][2] )
        h1.GetXaxis().SetRangeUser( pdet[v][0], pdet[v][1] )
        h1.GetXaxis().SetTitle( v + ' [GeV]')
        h1.GetYaxis().SetTitle( 'Events' )
        h1.SetLineColor( ROOT.kRed )
        h1.SetLineWidth( 1 )
        h1.SetMarkerStyle( 0 )
        h1.SetName('Current QCD Mthd.')
        h1.SetTitle('')
        h1.Draw('e1p')
        p1.Update()
        l1 = h1.GetListOfFunctions()
        s1 = l1.FindObject("stats")
        #print s1
        s1.SetName('s1')
        s1.SetY1NDC(.7)
        s1.SetY2NDC(.9)
        s1.SetTextColor(ROOT.kRed)



        #drawCMSString('CMS Preliminary, 2.3/fb, 13 TeV')
        h2 = f2.Get('tt_Histos/'+v)
        h2.SetStats(1)
        h2.Scale( qcdSF )
        h2.SetLineColor( ROOT.kBlue )
        h2.SetLineWidth( 1 )
        h2.SetMarkerStyle( 0 )
        h2.SetName('FF QCD Mthd.')
        h2.Draw('SAMES')
        
        p1.Update()
        l2 = h2.GetListOfFunctions()
        s2 = l2.FindObject("stats")
        #print s2
        s2.SetName('s2')
        s2.SetY1NDC(.5)
        s2.SetY2NDC(.7)
        s2.SetTextColor(ROOT.kBlue)
        p1.Update()
        
        ratioPad.cd()
        #ratioHist = ROOT.TH1F('ratio %s' % v, 'ratio', pdet[v][0], pdet[v][1] )
        ratioHist = h1.Clone()
        ratioHist.SetStats(0)
        ratioHist.GetXaxis().SetRangeUser( pdet[v][0], pdet[v][1] )
        #ratioHist.Sumw2()
        #ratioHist.Add( h1 )
        ratioHist.Divide( h2 )
        ratioHist.SetMaximum( 2. )
        ratioHist.SetMinimum( 0. )
        ratioHist.SetMarkerStyle( 21 )
        ratioHist.SetMarkerSize( 0.5 )
        ratioHist.SetLineColor(ROOT.kBlack)
        ratioHist.Draw('ex0')
        line = ROOT.TLine( pdet[v][0], 1, pdet[v][1], 1 )
        line.SetLineColor(ROOT.kBlack)
        line.SetLineWidth( 1 )
        line.Draw()
        ratioHist.Draw('esamex0')
        # X Axis!
        ratioHist.GetXaxis().SetTitle("%s" % pdet[v][3])
        ratioHist.GetYaxis().SetTitle("Current/FF")
        ratioHist.GetYaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
        ratioHist.GetYaxis().SetTitleOffset( smlPadSize*1.5 )
        ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize()*( 1/smlPadSize) )
        ratioHist.GetYaxis().SetNdivisions( 5, True )
        ratioHist.GetXaxis().SetLabelSize( ratioHist.GetXaxis().GetLabelSize()*( 1/smlPadSize) )
        ratioHist.GetXaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( 1/smlPadSize) )
        
        p1.cd() 
        h1.SetMaximum( max( h1.GetMaximum(), h2.GetMaximum())*1.3 )
        h1.Draw('SAMES')
        h2.Draw('SAMES')
        p1.Update()
        logo = ROOT.TText(.2, .88,"CMS Preliminary")
        logo.SetTextSize(0.04)
        logo.DrawTextNDC(.2, .89,"CMS Preliminary")
        lumi = ROOT.TText(.7,1.05,"%.1f fb^{-1} (13 TeV)" % cmsLumi )
        lumi.SetTextSize(0.04)
        lumi.DrawTextNDC(.7,.96,"2.3 / fb (13 TeV)" )

        c1.Print(pdir+'compare_'+v+'.png')


