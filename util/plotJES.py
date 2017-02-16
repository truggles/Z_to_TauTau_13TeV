import ROOT
from util.jetEnergyScale import getUncerts
from util.ratioPlot import ratioPlot
import pyplotter.plot_functions as pyplotter
import pyplotter.tdrstyle as tdr
from util.cecilesHelpers import add_lumi, add_CMS, add_Preliminary, \
        make_legend


ROOT.gROOT.SetBatch(True)
#ROOT.gStyle.SetFrameLineWidth(3)
#ROOT.gStyle.SetLineWidth(3)
ROOT.gStyle.SetOptStat(0)

#uncertNames = getUncerts()
uncertNames = [
    'RelativeBal', 'Total' ]


c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
#p1 = ROOT.TPad('p1', 'p1', 0, 0, 1, 1)
#p1.Draw()
#p1.cd()
smlPadSize = .35



#tdr.setTDRStyle()

def getCut( region ) :
    cut = ''
    if region == 'boosted' :
        cut = '(GenWeight/abs( GenWeight ))*(Z_SS==0)*(jetVeto30==1 || ((jetVeto30>=2)*!(abs(jdeta) > 2.5 && Higgs_Pt>100)))*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(weight)*(tauIDweight_1 * tauIDweight_2)*(XSecLumiWeight)*(ptCor_1 > 50.0 && ptCor_2 > 40.0)'
    if region == 'vbf' :
        cut = '(GenWeight/abs( GenWeight ))*(Z_SS==0)*(jetVeto30>=2)*(Higgs_Pt>100)*(abs(jdeta)>2.5)*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(weight)*(tauIDweight_1 * tauIDweight_2)*(XSecLumiWeight)*(ptCor_1 > 50.0 && ptCor_2 > 40.0)'
    if region == 'inc' :
        cut = '(GenWeight/abs( GenWeight ))*(Z_SS==0)*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(weight)*(tauIDweight_1 * tauIDweight_2)*(XSecLumiWeight)*(ptCor_1 > 50.0 && ptCor_2 > 40.0)'
    return cut


def plotShifts( region, name, var ) :

    pads = ratioPlot( c1, 1-smlPadSize )
    pad1 = pads[0]
    ratioPad = pads[1]
    ratioPad.SetTopMargin(0.00)
    ratioPad.SetBottomMargin(0.3)
    pad1.SetBottomMargin(0.00)
    ratioPad.SetGridy()

    nameString = '/data/truggles/JES_merge2/%s.root' % name
    f = ROOT.TFile(nameString, 'r')
    t = f.Get('Ntuple')

    # Closure test
    #h1 = ROOT.TH2D('h1', 'Closure Test', 25,0,300,25,-.01,.03)
    #t.Draw("((jet1PtJESClosure_Up-jet1PtJESTotal_Up)/(jet1Pt)):jet1Pt >> h1")
    #h1.Draw()
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/JES_Tests2/%s_closure.png' % name)

    cut = getCut( region )
    
    for shape in uncertNames : 
        print shape
        pad1.cd()
        l1=add_lumi()
        l1.Draw()
        l2=add_CMS()
        l2.Draw("same")
        l3=add_Preliminary()
        l3.Draw("same")
        if var == 'mjj' :
            nBins = 15
            nMin = 0
            nMax = 750
            h1 = ROOT.TH1D('h1', 'mjj: %s %s' % (name, region), nBins,nMin,nMax)
            h2 = ROOT.TH1D('h2', 'mjj %s UP' % shape, nBins,nMin,nMax)
            h3 = ROOT.TH1D('h3', 'mjj %s DOWN' % shape, nBins,nMin,nMax)
            t.Draw('mjj >> h1', cut)
            t.Draw('vbfMass_Jet%sUp >> h2' % shape, cut)
            t.Draw('vbfMass_Jet%sDown >> h3' % shape, cut)
            xAxis = 'di-jet Mass [GeV]'
        if var == 'nJets' :
            nBins = 8
            nMin = -0.5
            nMax = 7.5
            h1 = ROOT.TH1D('h1', 'nJets: %s %s' % (name, region), nBins,nMin,nMax)
            h2 = ROOT.TH1D('h2', 'nJets %s UP' % shape, nBins,nMin,nMax)
            h3 = ROOT.TH1D('h3', 'nJets %s DOWN' % shape, nBins,nMin,nMax)
            t.Draw('jetVeto30 >> h1', cut)
            t.Draw('jetVeto30_Jet%sUp >> h2' % shape, cut)
            t.Draw('jetVeto30_Jet%sDown >> h3' % shape, cut)
            xAxis = 'nJets p_{T} > 30'
        h1.GetYaxis().SetTitle( 'Events' )
        h1.SetLineColor(ROOT.kBlack)
        h2.SetLineColor(ROOT.kBlue)
        h3.SetLineColor(ROOT.kRed)
        h1.SetMaximum( h1.GetMaximum() * 1.2 )
        h1.Draw()
        h2.Draw('SAME E1')
        h3.Draw('SAME E1')
        legend=make_legend()
        legend.AddEntry(h1,"Nominal","elp")
        legend.AddEntry(h2,shape+" Up","elp")
        legend.AddEntry(h3,shape+" Down","elp")
        legend.Draw()

        ## Print integrals on png
        #intNom = h1.Integral()
        #intUp = h2.Integral()
        #intDown = h3.Integral()
        ##text1 = ROOT.TText(.4,.6,"" )
        #text1 = ROOT.TText()
        #text1.SetTextSize(0.035)
        #text1.DrawTextNDC(.15,.85,"Up/Nom.=%.5f  Down/Nom.=%.5f" % (intUp/intNom, intDown/intNom) )

        # ratio
        ratioPad.cd()
        ratioHist1 = ROOT.TH1D('ratio %s Up' % shape, '', nBins,nMin,nMax )
        ratioHist1.Sumw2()
        #ratioHist1.Add( h1 )
        #ratioHist1.Divide( h2 )
        ratioHist1.SetMaximum( 1.05 )
        ratioHist1.SetMinimum( 0.95 )
        if 'Total' in shape or 'Closure' in shape or 'RelativeBal' in shape :
            ratioHist1.SetMaximum( 1.2 )
            ratioHist1.SetMinimum( 0.80 )
        ratioHist1.SetLineColor( ROOT.kBlack )
        ratioHist1.GetYaxis().SetTitle('Shift / Nominal')
        ratioHist1.GetXaxis().SetTitle( xAxis )
        ratioHist1.GetYaxis().SetTitleSize( ratioHist1.GetYaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
        ratioHist1.GetYaxis().SetTitleOffset( smlPadSize*2 )
        ratioHist1.GetXaxis().SetTitleSize( ratioHist1.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize)*1.5 )
        ratioHist1.GetXaxis().SetLabelSize( ratioHist1.GetXaxis().GetLabelSize()*2.5 )
        ratioHist1.GetYaxis().SetLabelSize( ratioHist1.GetYaxis().GetLabelSize()*2. )
        ratioHist1.Draw()

        ratioHist3 = ROOT.TH1D('ratio %s Up3' % shape, '', nBins,nMin,nMax )
        ratioHist3.Sumw2()
        ratioHist3.Add( h2 )
        ratioHist3.Divide( h1 )
        ratioHist3.SetLineColor( ROOT.kBlue )
        ratioHist3.Draw('SAME E1')

        ratioHist2 = ROOT.TH1D('ratio %s Down' % shape, 'ratio', nBins,nMin,nMax )
        ratioHist2.Sumw2()
        ratioHist2.Add( h3 )
        ratioHist2.Divide( h1 )
        ratioHist2.SetLineColor( ROOT.kRed )
        ratioHist2.Draw('SAME E1')

        c1.SaveAs('/afs/cern.ch/user/t/truggles/www/JES_Tests7/%s_%s_%s_%s.png' % (name, region, shape, var))
        del h1,h2,h3

    print "Met Resolution"
    c1.Clear()
    p3 = ROOT.TPad('p3','p3',0,0,1,1)
    p3.Draw()
    p3.SetRightMargin( 1.7 * p3.GetRightMargin() )
    p3.cd()
    h4 = ROOT.TH2D('h4', 'Met Resolution: %s %s selections' % (name, region), 20,0,500,100,0.,2.)
    t.Draw('type1_pfMet_shiftedPt_JetEnUp/met:met >> h4', cut)
    h4.GetXaxis().SetTitle('pfMet [GeV]')
    h4.GetYaxis().SetTitle('pfMet JES+ / pfMet')
    h4.Scale( 1. / h4.Integral() )
    h4.Draw('COLZ')
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/JES_Tests7/%s_%s_metResolutionJES.png' % (name, region))
    del h4
    h4 = ROOT.TH2D('h4', 'Met Resolution: %s %s selections' % (name, region), 20,0,500,100,0.,2.)
    t.Draw('type1_pfMet_shiftedPt_UnclusteredEnUp/met:met >> h4', cut)
    h4.GetXaxis().SetTitle('pfMet [GeV]')
    h4.GetYaxis().SetTitle('pfMet Unclustered Energy+ / pfMet')
    h4.Scale( 1. / h4.Integral() )
    h4.Draw('COLZ')
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/JES_Tests7/%s_%s_metResolutionUncEnergy.png' % (name, region))
    del h4
    
        


if '__main__' in __name__ :
    #for name in ['dyJets', ]:#'ggH125', 'qqH125'] :
    for name in ['qqH125','dyJets']:# 'qqH125'] :
        for region in ['vbf', 'boosted','inc',] :
            for var in ['mjj', 'nJets'] :
                plotShifts( region, name, var )






