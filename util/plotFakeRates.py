import ROOT
import os
from util.azhReducibleBackground import setText
from util.helpers import checkDir
import pyplotter.tdrstyle as tdr
from util.ratioPlot import ratioPlot

ROOT.gROOT.SetBatch(True)


def plotFRObj( name, inObjs, pad, ratioPad, smlPadSize, minMax, selector='XXX'  ) :
    
    print name

    # select out objects we want
    objs = []
    if selector == 'XXX' : objs = inObjs
    else :
        for obj in inObjs :
            if selector in obj.GetName() : objs.append( obj )

    back = ROOT.TH1F( name, name, (minMax[1]-minMax[0]),minMax[0],minMax[1] )
    back.Draw()
    pad.cd()
    pad.SetLogy()
    maxi = 0.
    hists = []
    for i, g in enumerate(objs) :
        print i, g
        h = makeH( g, minMax )
        h.SetDirectory(0)
        hists.append( h )
        if h.GetMaximum() > maxi : maxi = h.GetMaximum()
        h.SetLineColor( colors[i] )
        h.SetMarkerColor( colors[i] )
        h.SetMarkerSize( 0 )
        h.SetLineWidth( 2 )
        h.SetMaximum( 1. )
        h.SetMinimum( 0.001 )
        #h.GetXaxis().SetRangeUser( minMax[0], minMax[1] )
        if i == 0 :
            h.GetXaxis().SetLabelSize( 0.0 )
            h.GetYaxis().SetTitle("Fake Rate")
            h.GetYaxis().SetLabelSize( h.GetYaxis().GetLabelSize() / (1-smlPadSize) )
            #h.Draw('R')
            #h.Draw('HIST')
            h.Draw('hist')
        else : h.Draw('hist same')
    #objs[0].SetMaximum( maxi * 1.2 )
    #objs[0].SetMinimum( 0 )
    #back.SetMaximum( maxi * 5 )
    #back.SetMaximum( 5. )
    #back.SetMinimum( 0.01 )
    #objs[0].GetXaxis().SetRangeUser( minMax[0], minMax[1] )
    pad.Update()

    ''' Build the legend explicitly so we can specify marker styles '''
    legend = ROOT.TLegend(0.40, 0.5, 0.9, 0.8)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for i, h in enumerate(hists) :
        legend.AddEntry( h, h.GetTitle().replace("Fake Rate Fit: ","").replace('_fit',''), 'lep')
    legend.Draw()
        
    ratioPad.cd()
    ratios = []
    for i, g in enumerate(objs) :
        print 'orig ratio',i, g
        ratio = makeRatioH( g, objs[0], minMax )
        ratios.append( ratio )
        if 'muons' in name :
            ratio.SetMaximum( 1.15 )
            ratio.SetMinimum( 0.85 )
        elif name in ['taus-DM10_lllt','taus-DM1_lllt'] :
            ratio.SetMaximum( 1.15 )
            ratio.SetMinimum( 0.85 )
        elif name in ['taus-DM0_lllt',] :
            ratio.SetMaximum( 1.3 )
            ratio.SetMinimum( 0.7 )
        else :
            ratio.SetMaximum( 4 )
            ratio.SetMinimum( 0. )
        ratio.SetLineColor( colors[i] )
        ratio.SetMarkerColor( colors[i] )
        ratio.SetMarkerSize( 0 )
        ratio.SetLineWidth( 2 )
        ratio.SetLineWidth( 2 )
        if i == 0 : 
            print 'ratio',i, g
            ratio.Draw('hist')
        else :
            print 'ratio',i, g
            ratio.Draw('hist same')
    #ratioPad.BuildLegend()
    
    
    pad.cd()
    setText( "Fake Rate Comparison: %s" % name, cmsLumi )
    c1.SaveAs( saveDir+'/'+name+'_FakeRateComp.png' )

def loadKey( objs, key ) :
    l = []
    for obj in objs :
        print obj
        if key in obj.GetName() :
            l.append( obj )
    return l

def makeH( graph, minMax ) :
    hist = ROOT.TH1F(graph.GetName(),graph.GetName(),(minMax[1]-minMax[0]),minMax[0],minMax[1])
    hist.SetDirectory(0)
    for i in range( minMax[0]+1, minMax[1]+1 ) :
        fill = graph.Eval(i)
        hist.Fill( i, fill )
    return hist

def makeRatioH( num, denom, minMax ) :
    print (minMax[1]-minMax[0]),minMax[0],minMax[1]
    ratioHist = ROOT.TH1F(num.GetName(),num.GetName(),(minMax[1]-minMax[0]),minMax[0],minMax[1])
    ratioHist.SetDirectory(0)
    for i in range( minMax[0]+1, minMax[1]+1 ) :
        if denom.Eval(i) > 0 :
            fill = num.Eval(i)/denom.Eval(i)
            #print i, num.Eval(i), denom.Eval(i), fill
            ratioHist.Fill( i, fill )
    ratioHist.GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
    ratioHist.GetYaxis().SetTitle("Ratio")
    ratioHist.GetYaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
    ratioHist.GetYaxis().SetTitleOffset( smlPadSize*1.5 )
    ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize()*( 1/smlPadSize) )
    ratioHist.GetYaxis().SetNdivisions( 5, True )
    ratioHist.GetXaxis().SetLabelSize( ratioHist.GetXaxis().GetLabelSize()*( 1/smlPadSize) )
    ratioHist.GetXaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( 1/smlPadSize) )
    return ratioHist


if '__main__' in __name__ :
    cmsLumi = float(os.getenv('LUMI'))/1000
    print "Lumi = %.1f / fb" % cmsLumi
    
    f = ROOT.TFile('data/azhFakeRateFits.root','r')
    
    #objs = ['tau-DM0','tau-DM1','tau-DM10','electron','muon',]
    objs = ['tau-DM0','tau-DM1','tau-DM10','muon',]
    
    newObjs = []
    for obj in objs :
        if 'tau' in obj :
            newObjs.append( obj )
            newObjs.append( obj+'_lllt' )
            newObjs.append( obj+'_lltt' )
        else : 
            newObjs.append( obj )
    
    newestObjs = []
    for obj in newObjs :
        newestObjs.append( obj+'_AllEta_jetMatch_fit' )
        newestObjs.append( obj+'_Barrel_jetMatch_fit' )
        newestObjs.append( obj+'_Endcap_jetMatch_fit' )
    
    graphs = []
    for obj in newestObjs :
        g = f.Get( obj )
        graphs.append( g )
    
    c1 = ROOT.TCanvas("c1","c1", 550, 550)
    smlPadSize = .25
    pads = ratioPlot( c1, 1-smlPadSize )
    pad1 = pads[0]
    ratioPad = pads[1]
    ratioPad.SetTopMargin(0.0)
    ratioPad.SetBottomMargin(0.3)
    pad1.SetBottomMargin(0.00)
    #pad1.SetTopMargin(0.18)
    pad1.SetTopMargin(0.12)
    pad1.SetGrid()
    ratioPad.SetGrid()
    
    saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Sept21_Final'
    checkDir( saveDir )
    
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kOrange, ROOT.kGray]
    
    tdr.setTDRStyle()

    #electrons = loadKey( graphs, 'electron' )
    #elecMinMax = [15, 100]
    #plotFRObj( 'electrons', electrons, pad1, ratioPad, smlPadSize, elecMinMax )
    print graphs
    muons = loadKey( graphs, 'muon' )
    muonMinMax = [12, 100]
    plotFRObj( 'muons', muons, pad1, ratioPad, smlPadSize, muonMinMax )

    taus = loadKey( graphs, 'tau-DM0_lllt' )
    tauMinMax = [20, 100]
    plotFRObj( 'taus-DM0_lllt', taus, pad1, ratioPad, smlPadSize, tauMinMax )
    taus = loadKey( graphs, 'tau-DM1_lllt' )
    tauMinMax = [20, 100]
    plotFRObj( 'taus-DM1_lllt', taus, pad1, ratioPad, smlPadSize, tauMinMax )
    taus = loadKey( graphs, 'tau-DM10_lllt' )
    tauMinMax = [20, 100]
    plotFRObj( 'taus-DM10_lllt', taus, pad1, ratioPad, smlPadSize, tauMinMax )

    taus = loadKey( graphs, 'tau-' )
    tauMinMax = [20, 100]
    plotFRObj( 'taus_lllt_AllEta', taus, pad1, ratioPad, smlPadSize, tauMinMax, 'lllt_AllEta' )
    taus = loadKey( graphs, 'tau-' )
    tauMinMax = [20, 100]
    plotFRObj( 'taus_lltt_AllEta', taus, pad1, ratioPad, smlPadSize, tauMinMax, 'lltt_AllEta' )
    taus = loadKey( graphs, 'tau-' )
    tauMinMax = [20, 100]
    plotFRObj( 'taus_lllt_Barrel', taus, pad1, ratioPad, smlPadSize, tauMinMax, 'lllt_Barrel' )
    taus = loadKey( graphs, 'tau-' )
    tauMinMax = [20, 100]
    plotFRObj( 'taus_lltt_Barrel', taus, pad1, ratioPad, smlPadSize, tauMinMax, 'lltt_Barrel' )
    taus = loadKey( graphs, 'tau-' )
    tauMinMax = [20, 100]
    plotFRObj( 'taus_lllt_Endcap', taus, pad1, ratioPad, smlPadSize, tauMinMax, 'lllt_Endcap' )
    taus = loadKey( graphs, 'tau-' )
    tauMinMax = [20, 100]
    plotFRObj( 'taus_lltt_Endcap', taus, pad1, ratioPad, smlPadSize, tauMinMax, 'lltt_Endcap' )

