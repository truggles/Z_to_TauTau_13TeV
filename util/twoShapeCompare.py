import ROOT
from array import array
from analysisPlots import getHistoDict
from ROOT import gPad, gStyle
from ratioPlot import ratioPlot
import os
import pyplotter.tdrstyle as tdr
from util.helpers import checkDir
from util.helpers import getQCDSF

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

#f1name = 'htt2Oct03bFFshapeSyst_OSl1ml2_VTight_ZTT1jet/QCD_tt.root'
#f = ROOT.TFile(f1name,'r')
#d = f.Get('tt_Histos')
#c = ROOT.TCanvas('c', 'c', 600, 600)
#p = ROOT.TPad('p','p',0,0,1,1)
#p.Draw()
#ha = d.Get('m_sv')
#hb = d.Get('m_sv_ffStatUp')
#hc = d.Get('m_sv_ffStatDown')
#hd = d.Get('m_sv_ffSystUp')
#he = d.Get('m_sv_ffSystDown')
#count = 0
#ROOT.gStyle.SetOptStat(0)
#colors = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,ROOT.kGreen+2,ROOT.kCyan+1]
#for hist in [ha, hb ,hc ,hd ,he] :
#    hist.Rebin(10)
#    hist.SetLineWidth(2)
#    hist.SetLineColor(colors[count])
#    count += 1
#ha.Draw()
#ha.SetMaximum(15)
#logo = ROOT.TText(.2, .88,"CMS Preliminary")
#logo.SetTextSize(0.04)
#logo.DrawTextNDC(.2, .89,"CMS Preliminary")
#lumi = ROOT.TText(.7,1.05,"%.1f fb^{-1} (13 TeV)" % cmsLumi )
#lumi.SetTextSize(0.04)
#lumi.DrawTextNDC(.7,.96,"2.3 / fb (13 TeV)" )
#for hist in [hb ,hc ,hd ,he] :
#    hist.Draw('SAME')
#ha.Draw('SAME')
##c.BuildLegend()
#c.SaveAs('/afs/cern.ch/user/t/truggles/www/fakeFactor/overlapPlots/syst.png')





cats = ['inclusive', '0jet', '1jet', '2jet', '1jet_low', '1jet_medium', '1jet_high', '2jet_vbf', '1bjet', '2bjet']
folder = '2Oct05oldMthd'
for cat in cats :
    qcdSF = getQCDSF( 'httQCDYields_4040VTight_%s.txt' % folder, cat )
    print cat,"  with qcdSF = ",qcdSF

    useQCDMakeName = folder+'_OSl1ml2_VTight_LooseZTT'+cat
    f2name = 'meta/httBackgrounds/tt_qcdShape_%s.root' % useQCDMakeName
    f1name = 'htt2Oct03bFFshapeSyst_OSl1ml2_VTight_ZTT'+cat+'/QCD_tt.root'
    dname = 'tt_Histos'
    pdet = getHistoDict( 'htt', 'tt' )
    shapeSyst = ['_ffStat', '_ffSyst', '_energyScale']
    for shape in shapeSyst :
        for dir in ['Up', 'Down'] :
            pdet['m_sv'+shape+dir] = pdet['m_sv']
            pdet['m_vis'+shape+dir] = pdet['m_vis']
    
    f1 = ROOT.TFile(f1name, 'r')
    f2 = ROOT.TFile(f2name, 'r')
    
    vars1 = f1.Get('tt_Histos').GetListOfKeys()
    #print f1
    #print vars1
    vars2 = f2.Get('tt_Histos').GetListOfKeys()
    #print f2
    #print vars2
    v1s = [] 
    v2s = [] 
    for v in vars1 :
        #print "Vars1:",v.GetName()
        v1s.append(v.GetName())
    for v in vars1 :
        #print "Vars2:",v.GetName()
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
    
    pdir = '/afs/cern.ch/user/t/truggles/www/fakeFactor/overlapPlots/'+cat+'/'
    checkDir( pdir )
    for v in v1s :
        print v
        if '_ff' in v or '_energyScale' in v : continue
        varBin = False
        if v in v2s :
            print v," in both roots"
            # 1 = un-rebinned, range not set, 2 = post work

            # Check if this var is rebinned
            #if 'm_sv' in v or 'm_vis' in v :
            #    h1_ = f1.Get('tt_Histos/'+v)
            #    print h1_.GetNbinsX()
            #    varBin = True
            #    
            #    if cat in ['2jet', '1jet_low', '1jet_medium', '1jet_high'] :
            #        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
            #    elif cat in ['2jet_vbf', '1bjet', '2bjet'] :
            #        xBins = array( 'd', [0,40,60,80,100,120,150,200,250] )
            #    else :
            #        xBins = array( 'd', [i*10 for i in range( 31 )] )
            #    h1 = h1_.Rebin( len(xBins)-1, "Re"+v, xBins)
            #else :
            #    h1 = f1.Get('tt_Histos/'+v)
            #    h1.Rebin( pdet[v][3] )
            #    h1.GetXaxis().SetRangeUser( pdet[v][1], pdet[v][2] )
            h1 = f1.Get('tt_Histos/'+v)
            h1.Rebin( pdet[v][3] )
            h1.GetXaxis().SetRangeUser( pdet[v][1], pdet[v][2] )
            h1.GetXaxis().SetTitle( v + ' [GeV]')
            h1.GetYaxis().SetTitle( 'Events' )
            h1.SetLineColor( ROOT.kRed )
            h1.SetLineWidth( 2 )
            h1.SetMarkerStyle( 0 )
            h1.SetName('FF QCD Mthd.')
            h1.SetTitle('')
            h1.Draw('e1p')
            p1.Update()
            l1 = h1.GetListOfFunctions()
            s1 = l1.FindObject("stats")
            #print s1
            s1.SetName('s1')
            s1.SetX1NDC(.75)
            s1.SetY1NDC(.65)
            s1.SetY2NDC(.9)
            s1.SetTextColor(ROOT.kRed)
    
    
    
            #drawCMSString('CMS Preliminary, 2.3/fb, 13 TeV')
            h2 = f2.Get('tt_Histos/'+v)
            h2.SetStats(1)
            h2.Scale( qcdSF )
            h2.SetLineColor( ROOT.kBlue )
            h2.SetLineWidth( 2 )
            h2.SetMarkerStyle( 0 )
            h2.SetName('Standard QCD Mthd.')
            h2.Draw('SAMES')
            
            p1.Update()
            l2 = h2.GetListOfFunctions()
            s2 = l2.FindObject("stats")
            #print s2
            s2.SetName('s2')
            s2.SetX1NDC(.75)
            s2.SetY1NDC(.4)
            s2.SetY2NDC(.65)
            s2.SetTextColor(ROOT.kBlue)
            p1.Update()
            
            ratioPad.cd()
            #ratioHist = ROOT.TH1F('ratio %s' % v, 'ratio', pdet[v][0], pdet[v][1] )
            ratioHist = h1.Clone()
            ratioHist.SetStats(0)
            if varBin :
                ratioHist.GetXaxis().SetRangeUser( xBins[0], xBins[-1] )
            else :
                ratioHist.GetXaxis().SetRangeUser( pdet[v][1], pdet[v][2] )
            #ratioHist.Sumw2()
            #ratioHist.Add( h1 )
            ratioHist.Divide( h2 )
            ratioHist.SetMaximum( 2. )
            ratioHist.SetMinimum( 0. )
            ratioHist.SetMarkerStyle( 21 )
            ratioHist.SetMarkerSize( 0.5 )
            ratioHist.SetLineColor(ROOT.kBlack)
            ratioHist.Draw('ex0')
            line = ROOT.TLine( pdet[v][1], 1, pdet[v][2], 1 )
            line.SetLineColor(ROOT.kBlack)
            line.SetLineWidth( 1 )
            line.Draw()
            ratioHist.Draw('esamex0')
            # X Axis!
            ratioHist.GetXaxis().SetTitle("%s" % pdet[v][4])
            ratioHist.GetYaxis().SetTitle("FF/Standard")
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
    
    
