from util.buildTChain import makeTChain
import ROOT
import json
from collections import OrderedDict
import pyplotter.plot_functions as pyplotter #import setTDRStyle, getCanvas
import pyplotter.tdrstyle as tdr
import argparse
from util.ratioPlot import ratioPlot
import analysisPlots
from util.splitCanvas import fixFontSize
import os
from array import array

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='dataCards', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--ratio', action='store', default=False, dest='ratio', help="Include ratio plots? Defaul = False")
p.add_argument('--log', action='store', default=False, dest='log', help="Plot Log Y?")
p.add_argument('--folder', action='store', default='2SingleIOAD', dest='folderDetails', help="What's our post-prefix folder name?")
p.add_argument('--qcd', action='store', default=True, dest='plotQCD', help="Plot QCD?")
p.add_argument('--text', action='store', default=False, dest='text', help="Add text?")
p.add_argument('--www', action='store', default=True, dest='www', help="Save to Tyler's public 'www' space?")
p.add_argument('--qcdShape', action='store', default='Sync', dest='qcdShape', help="Which QCD shape to use? Sync or Loose triggers")
p.add_argument('--qcdMake', action='store', default=False, dest='qcdMake', help="Make a data - MC qcd shape?")
p.add_argument('--useQCDMake', action='store', default=False, dest='useQCDMake', help="Make a data - MC qcd shape?")
p.add_argument('--QCDYield', action='store', default=False, dest='QCDYield', help="Define a QCD yield even when using a shape file?")
options = p.parse_args()
grouping = options.sampleName
ratio = options.ratio
folderDetails = options.folderDetails

xBins = array('d', [0,20,40,60,80,100,150,200,250,350,600])
xNum = len( xBins ) - 1

print "Running over %s samples" % grouping

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

luminosity = 2090.0 # / fb 25ns - Final 2015 25ns Golden JSON
#qcdTTScaleFactor = 1.07 # see http://truggles.web.cern.ch/truggles/Oct29/
qcdTTScaleFactor = 1.06 # see http://truggles.web.cern.ch/truggles/Oct29/
#qcdTTScaleFactor = 1.23 # http://truggles.web.cern.ch/truggles/qcdScale/dec02_singleBinnedQCD/OSvsSS-ddQCD.png
#qcdTTScaleFactor = 1.27 # dm0
#qcdTTScaleFactor = 1.26 # dm1
#qcdTTScaleFactor = 1.18 # dm10
#qcdTTScaleFactor = 1.38 # http://truggles.web.cern.ch/truggles/qcdScale/dec02_singleBinnedQCD/OSvsSS-ddQCD.png
qcdEMScaleFactor = 1.06
#bkgsTTScaleFactor = (1.11 + 0.99) / 2 # see pZeta_TT_Control.xlsx 
#bkgsTTScaleFactor = 1.14 # see pZeta_TT_Control.xlsx 
bkgsTTScaleFactor = 1.0
#bkgsTTScaleFactor = 0.96
qcdYieldTT = 35.7 * qcdTTScaleFactor
qcdYieldEM = 1586.0 *  qcdEMScaleFactor

with open('meta/NtupleInputs_%s/samples.json' % grouping) as sampFile :
    sampDict = json.load( sampFile )

                # Sample : Color
samples = OrderedDict()
samples['DYJets']   = ('kOrange-4', 'dyj')
samples['DYJetsLow']   = ('kOrange-4', 'dyj')
samples['T-tW']     = ('kYellow+2', 'dib')
samples['T-tchan']     = ('kYellow+2', 'dib')
samples['TT']       = ('kBlue-8', 'top')
samples['Tbar-tW']  = ('kYellow-2', 'dib')
samples['Tbar-tchan']  = ('kYellow-2', 'dib')
samples['WJets']    = ('kAzure+2', 'wjets')
samples['WW1l1nu2q']       = ('kAzure+8', 'dib')
samples['WW2l2nu']       = ('kAzure+8', 'dib')
samples['WZ1l1nu2q'] = ('kAzure-6', 'dib')
samples['WZ1l3nu'] = ('kAzure-6', 'dib')
samples['WZ2l2q'] = ('kAzure-6', 'dib')
samples['WZ3l1nu'] = ('kAzure-6', 'dib')
samples['ZZ2l2nu'] = ('kAzure-12', 'dib')
samples['ZZ2l2q'] = ('kAzure-12', 'dib')
samples['ZZ4l'] = ('kAzure-12', 'dib')
samples['QCD']        = ('kMagenta-10', 'qcd')
samples['data_tt']  = ('kBlack', 'data')
samples['data_em']  = ('kBlack', 'data')

sampColors = {
    'dib' : 'kRed+2',
    'top' : 'kBlue-8',
    'qcd' : 'kMagenta-10',
    'dyj' : 'kOrange-4',
    'wjets' : 'kAzure+2',
    'data' : 'kBlack',
}


for channel in ['em', 'tt'] :

    #if channel == 'tt' : continue
    if channel == 'em' : continue

    # Make an index file for web viewing
    if not os.path.exists( '%sPlots' % grouping ) :
        os.makedirs( '%sPlots/em' % grouping )
        os.makedirs( '%sPlots/tt' % grouping )
    if not os.path.exists( '%sPlotsList' % grouping ) :
        os.makedirs( '%sPlotsList/em' % grouping )
        os.makedirs( '%sPlotsList/tt' % grouping )
    if options.www :
        htmlFile = open('/afs/cern.ch/user/t/truggles/www/%sPlots/%s/index.html' % (grouping, channel), 'w')
    else :
        htmlFile = open('%sPlots/%s/index.html' % (grouping, channel), 'w')
    htmlFile.write( '<html><head><STYLE type="text/css">img { border:0px; }</STYLE>\n' )
    htmlFile.write( '<title>Channel %s/</title></head>\n' % channel )
    htmlFile.write( '<body>\n' )


    print channel

    newVarMap = analysisPlots.getHistoDict( channel )
    plotDetails = analysisPlots.getPlotDetails( channel )

    if options.qcdMake :
        qcdMaker = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape.root' % (grouping, channel), 'RECREATE')
        qcdDir = qcdMaker.mkdir('%s_Histos' % channel)

    for var, info in newVarMap.iteritems() :

        #if not (var == 'pZeta-0.85pZetaVis' or var == 'm_vis') : continue
        if not var == 'm_vis' : continue
        #if not (var == 't1DecayMode' or var == 't2DecayMode') : continue
        name = info[0]
        print "Var: %s      Name: %s" % (var, name)
        stack = ROOT.THStack("All Backgrounds stack", "%s, %s" % (channel, var) )
        dyj = ROOT.TH1F("All Backgrounds dyj", "dyj", xNum, xBins )
        dib = ROOT.TH1F("All Backgrounds dib", "dib", xNum, xBins )
        top = ROOT.TH1F("All Backgrounds top", "top", xNum, xBins )
        higgs = ROOT.TH1F("All Backgrounds higgs", "higgs", xNum, xBins )
        qcd = ROOT.TH1F("All Backgrounds qcd", "qcd", xNum, xBins )
        wjets = ROOT.TH1F("All Backgrounds wjets", "wjets", xNum, xBins )
        data = ROOT.TH1F("All Backgrounds data", "data", xNum, xBins )

        #stack = ROOT.THStack("All Backgrounds stack", "%s, %s" % (channel, var) )
        #dyj = ROOT.THStack("All Backgrounds dyj", "dyj" )
        #dib = ROOT.THStack("All Backgrounds dib", "dib" )
        #top = ROOT.THStack("All Backgrounds top", "top" )
        #higgs = ROOT.THStack("All Backgrounds higgs", "higgs" )
        #qcd = ROOT.THStack("All Backgrounds qcd", "qcd" )
        #wjets = ROOT.THStack("All Backgrounds wjets", "wjets" )
        #data = ROOT.THStack("All Backgrounds data", "data" )

        pZetaTot = 0
        for sample in samples:
            print sample

            if channel == 'tt' and sample == 'data_em' : continue
            if channel == 'em' and sample == 'data_tt' : continue

            #print sample
            #print '%s2IsoOrderAndDups/%s_%s.root' % (grouping, sample, channel)

            if sample == 'data_em' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif sample == 'data_tt' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif sample == 'QCD' :
                if options.useQCDMake :
                    tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape.root' % (grouping, channel), 'READ')
                    print "Got QCD make file"
                else :
                    tFile = ROOT.TFile('meta/%sBackgrounds/QCDShape%s/shape/data_%s.root' % (grouping, options.qcdShape, channel), 'READ')
            else :
                tFile = ROOT.TFile('%s%s/%s_%s.root' % (grouping, folderDetails, sample, channel), 'READ')


            dic = tFile.Get("%s_Histos" % channel )
            preHist = dic.Get( "%s" % var )
            preHist.SetDirectory( 0 )

            if sample == 'QCD' and options.useQCDMake :
                if channel == 'em' :
                    print "Skip rebin; Scale QCD shape by %f" % qcdEMScaleFactor
                    preHist.Scale( qcdEMScaleFactor )
                if channel == 'tt' :
                    print "Skip rebin; Scale QCD shape by %f" % qcdTTScaleFactor
                    preHist.Scale( qcdTTScaleFactor )
                    print "QCD yield: %f" % preHist.Integral()
                    hist = ROOT.TH1F( preHist )
            else :
                #preHist.Rebin( plotDetails[ var ][2] )
                hist = preHist.Rebin( xNum, "rebinned", xBins )

            #if 'data' not in sample and samples[ sample ][1] != 'higgs' :
            #    color = "ROOT.%s" % sampColors[ samples[ sample ][1] ]
            #    hist.SetFillColor( eval( color ) )
            #    hist.SetLineColor( ROOT.kBlack )
            #    hist.SetLineWidth( 2 )
            #elif samples[ sample ][1] == 'higgs' :
            #    hist.SetLineColor( ROOT.kBlue )
            #    hist.SetLineWidth( 4 )
            #    hist.SetLineStyle( 7 )
            #else :
            #    hist.SetLineColor( ROOT.kBlack )
            #    hist.SetLineWidth( 2 )
            #    hist.SetMarkerStyle( 21 )
            #hist.SaveAs('plots/%s/%s.root' % (channel, sample) )

            ''' Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ),
            QCD gets special scaling from bkg estimation, see qcdYield[channel] above for details '''
            #print "PRE Sample: %s      Int: %f" % (sample, hist.Integral() )
            if sample == 'QCD' and hist.Integral() != 0 :
                if not options.useQCDMake or options.QCDYield :
                    if channel == 'em' : hist.Scale( qcdYieldEM / hist.Integral() )
                    if channel == 'tt' : hist.Scale( qcdYieldTT / hist.Integral() )
                    print "Using QCD Yield numbers from this file, QCD Int: %f" % hist.Integral()
            elif 'data' not in sample and hist.Integral() != 0:
                scaler = luminosity * sampDict[ sample ]['Cross Section (pb)'] / ( sampDict[ sample ]['summedWeightsNorm'] )
                if 'TT' in sample :
                    hist.Scale( scaler * bkgsTTScaleFactor )
                else :
                    hist.Scale( scaler )

            #if var == 'pZeta-0.85pZetaVis' :
            #    #print " --- Sample %s Int %f" % ( sample, hist.Integral() )
            #    lower = hist.GetXaxis().FindBin( -300. )
            #    upper = hist.GetXaxis().FindBin( -50. )
            #    #print " --- Sample: %s      Int: %f" % (sample, hist.Integral() )
            #    integral = hist.Integral( lower, upper)
            #    print " --- Sample: %s     Int below -50: %f" % (sample, integral )
            #    #hist.GetXaxis().SetRangeUser( 11, upper )
            #    pZetaTot += integral
            #    print " --- pZeta running total = ",pZetaTot

            #print "Hist int: %s %f" % (sample, hist.Integral() )
            if samples[ sample ][1] == 'dyj' :
                hist.SetTitle('Z #rightarrow #tau#tau')
                dyj.Add( hist )
            if samples[ sample ][1] == 'qcd' :
                hist.SetTitle('QCD')
                qcd.Add( hist )
                #print "qcd Stack yield: %f" % qcd.GetStack().Last().Integral()
                print "qcd Stack yield: %f" % qcd.Integral()
            if samples[ sample ][1] == 'top' :
                hist.SetTitle('TT')
                top.Add( hist )
            if samples[ sample ][1] == 'dib' :
                hist.SetTitle('VV')
                dib.Add( hist )
            if samples[ sample ][1] == 'wjets' :
                hist.SetTitle('WJets')
                wjets.Add( hist )
            if samples[ sample ][1] == 'higgs' :
                hist.SetTitle('SM Higgs(125)')
                higgs.Add( hist )
            if samples[ sample ][1] == 'data' :
                hist.SetTitle('Data')
                data.Add( hist )
            tFile.Close()

        Ary = { qcd : "qcd", top : "top", dib : "dib", wjets : "wjets", dyj : "dyj", }
        for h in Ary.keys() :
            color = "ROOT.%s" % sampColors[ Ary[h] ]
            h.SetFillColor( eval( color ) )
            h.SetLineColor( ROOT.kBlack )
            h.SetLineWidth( 2 )
        data.SetLineColor( ROOT.kBlack )
        data.SetLineWidth( 2 )
        data.SetMarkerStyle( 21 )
        Ary[ data ] = "data"
        
        # With Variable binning, need to set bin content appropriately
        for h in Ary.keys() :
            if Ary[h] == "qcd" : continue
            for bin_ in range( 1, 11 ) :
                h.SetBinContent( bin_, h.GetBinContent( bin_ ) * ( 20 / h.GetBinWidth( bin_ ) ) )

        # Set hist Names
        Names = { "data" : "Data", "qcd" : "QCD", "top" : "TT", "dib" : "VV", "wjets" : "WJets", "dyj" : "Z #rightarrow #tau#tau" }
        for h in Ary.keys() :
            h.SetTitle( Names[ Ary[h] ] )
            

        if options.plotQCD == True :
            print "Adding QCD"
            stack.Add( qcd )
        stack.Add( top )
        stack.Add( dib )
        stack.Add( wjets )
        stack.Add( dyj )

            
        if options.qcdMake :
            if var == 'm_vis' :
                qcdVar = ROOT.TH1F( var, 'qcd', xNum, xBins )
            else :
                qcdVar = ROOT.TH1F( var, 'qcd', ( info[1] / (plotDetails[ var ][2]) ), info[2], info[3])
            print "Pre ratio add"
            qcdVar.Add( data )
            qcdVar.Add( -1 * stack.GetStack().Last() )
            print "Post ratio add"
            qcdVar.SetFillColor( ROOT.kMagenta-10 )
            qcdVar.SetLineColor( ROOT.kBlack )
            qcdVar.SetLineWidth( 2 )
            # Add the shape estimated here to the stack pre-scaling!!!
            stack.Add( qcdVar ) 
            qcdVar.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )
            print "qcdVar: %f" % qcdVar.Integral()
            qcdDir.cd()
            qcdVar.Write()


        # Maybe make ratio hist
        c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 550, 550)

        if not options.ratio :
            pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
            pad1.Draw()
            pad1.cd()
            stack.Draw('hist')
            data.Draw('esamex0')
            # X Axis!
            stack.GetXaxis().SetTitle("%s" % plotDetails[ var ][ 3 ])

        if options.ratio :
            smlPadSize = .25
            pads = ratioPlot( c1, 1-smlPadSize )
            pad1 = pads[0]
            ratioPad = pads[1]
            ratioPad.SetTopMargin(0.00)
            ratioPad.SetBottomMargin(0.3)
            pad1.SetBottomMargin(0.00)
            ratioPad.SetGridy()
            if var == 'm_vis' :
                ratioHist = ROOT.TH1F('ratio %s' % info[0], 'ratio', xNum, xBins )
            else :
                ratioHist = ROOT.TH1F('ratio %s' % info[0], 'ratio', ( info[1] / (plotDetails[ var ][2]) ), info[2], info[3])
            ratioHist.Add( data )
            ratioHist.Sumw2()
            ratioHist.Divide( stack.GetStack().Last() )
            #lower = hist.GetXaxis().FindBin( 100. )
            #for bin_ in range( 0, (ratioHist.GetXaxis().GetNbins()+1) ) :
            #    if stack.GetStack().Last().GetBinContent( bin_ ) > 0 :
            #        num = data.GetStack().Last().GetBinContent( bin_ ) / stack.GetStack().Last().GetBinContent( bin_ )
            #        ratioHist.SetBinContent( bin_, num )
            if channel == 'em' :
                ratioHist.SetMaximum( 1.5 )
                ratioHist.SetMinimum( 0.5 )
            if channel == 'tt' :
                ratioHist.SetMaximum( 2. )
                ratioHist.SetMinimum( 0. )
            ratioHist.SetMarkerStyle( 21 )
            ratioPad.cd()
            ratioHist.Draw('ex0')
            line = ROOT.TLine( plotDetails[ var ][0], 1, plotDetails[ var ][1], 1 )
            line.SetLineColor(ROOT.kBlack)
            line.SetLineWidth( 1 )
            line.Draw()
            ratioHist.Draw('esamex0')
            # X Axis!
            ratioHist.GetXaxis().SetTitle("%s" % plotDetails[ var ][ 3 ])
            ratioHist.GetYaxis().SetTitle("Data / MC")
            #yAxis = ratioHist.GetYaxis()
            #xAxis = ratioHist.GetXaxis()
            #fixFontSize( yAxis, (1-.8))
            #fixFontSize( xAxis  (1-.8))
            ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize()*( 1/smlPadSize) )
            #ratioHist.GetYaxis().SetTextSize( ratioHist.GetYaxis().GetTextSize()*( 1/smlPadSize) )
            ratioHist.GetYaxis().SetNdivisions( 5, True )
            #ratioHist.GetYaxis().SetTitleSize( ratioHist.GetYaxis().GetTitleSize()*( 1/smlPadSize/2) )
            ratioHist.GetXaxis().SetLabelSize( ratioHist.GetXaxis().GetLabelSize()*( 1/smlPadSize) )
            ratioHist.GetXaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( 1/smlPadSize) )
            #ratioHist.GetXaxis().SetTitleOffset( ratioHist.GetXaxis().GetTitleOffset()*( 1/smlPadSize/2.5) )
            #ratioHist.GetYaxis().SetTickSize( .25 )
            #ratioHist.GetYaxis().SetTickLength( .03 )

            pad1.cd()
            stack.Draw('hist')
            data.Draw('esamex0')


        # Set Y axis titles appropriately
        #binWidth = str( round( hist.GetBinWidth(1), 0) )
        stack.GetYaxis().SetTitle("Events / 20 GeV")
        #if plotDetails[ var ][ 4 ] == '' :
        #    stack.GetYaxis().SetTitle("Events")
        #else :
        #    if hist.GetBinWidth(1) < .5 :
        #        stack.GetYaxis().SetTitle("Events / %s%s" % ( binWidth, plotDetails[ var ][ 4 ] ) )
        #    else :
        #        stack.GetYaxis().SetTitle("Events / %i%s" % ( binWidth, plotDetails[ var ][ 4 ] ) )

        stack.SetTitle( "CMS Preliminary        %f pb^{-1} ( 13 TeV )" % luminosity )

        # Set axis and viewing area
        #higgsMin = higgs.GetMaximum()
        #print "higgs max: %f" % higgsMin
        #stackMin = stack.GetStack().First().GetMaximum()
        #print "stack max: %f" % stackMin
        #stack.SetMinimum( min( higgsMin, stackMin) * 0.3 )
        stackMax = stack.GetStack().Last().GetMaximum()
        dataMax = data.GetMaximum()
        stack.SetMaximum( max(dataMax, stackMax) * 1.5 )
        #stack.SetMaximum( stackMax * 1.5 )
        if options.log :
            pad1.SetLogy()
            stack.SetMaximum( max(dataMax, stackMax) * 10 )
            stack.SetMinimum( min(dataMax, stackMax) * .05 )

        ''' Build the legend explicitly so we can specify marker styles '''
        legend = ROOT.TLegend(0.60, 0.65, 0.95, 0.93)
        legend.SetMargin(0.3)
        legend.SetBorderSize(0)
        legend.AddEntry( data, "Data", 'lep')
        for j in range(0, stack.GetStack().GetLast() + 1) :
            last = stack.GetStack().GetLast()
            legend.AddEntry( stack.GetStack()[ last - j ], stack.GetStack()[last - j ].GetTitle(), 'f')
        legend.Draw()

        # Set CMS Styles Stuff
        logo = ROOT.TText(.2, .88,"CMS Preliminary")
        logo.SetTextSize(0.03)
        logo.DrawTextNDC(.2, .89,"CMS Preliminary")

        chan = ROOT.TText(.2, .80,"x")
        chan.SetTextSize(0.05)
        chan.DrawTextNDC(.2, .84,"Channel: %s" % channel.upper() )

        lumi = ROOT.TText(.7,1.05,"%f fb^{-1} (13 TeV)" % round(luminosity/1000,2) )
        lumi.SetTextSize(0.03)
        lumi.DrawTextNDC(.7,.96,"%f / fb (13 TeV)" % round(luminosity/1000,2) )

        ''' Random print outs on plots '''
        if options.text :
            text1 = ROOT.TText(.4,.6,"Data Integral: %f" % data.GetMean() )
            text1.SetTextSize(0.04)
            text1.DrawTextNDC(.6,.6,"Data Integral: %s" % str( round( data.Integral(), 1) ) )
            text2 = ROOT.TText(.4,.55,"Data Int: %s" % str( data.Integral() ) )
            text2.SetTextSize(0.04)
            text2.DrawTextNDC(.6,.55,"MC Integral: %s" % str( round( stack.GetStack().Last().Integral(), 1) ) )
            text3 = ROOT.TText(.4,.55,"Data Mean: %s" % str( data.GetMean() ) )
            text3.SetTextSize(0.04)
            text3.DrawTextNDC(.6,.50,"Diff: %s" % str( round( data.Integral() - stack.GetStack().Last().Integral(), 1) ) )
            #text4 = ROOT.TText(.4,.55,"Data Int: %s" % str( data.Integral() ) )
            #text4.SetTextSize(0.05)
            #text4.DrawTextNDC(.65,.45,"SS Selection" )

        if (var == 't1DecayMode' or var == 't2DecayMode') :
            print var + " DATA: 1p0pi0: %f   1p1pi0: %f   3p0pi0: %f" % ( data.GetBinContent( 1), data.GetBinContent( 2), data.GetBinContent( 11 ) )
            print var + " MC: 1p0pi0: %f   1p1pi0: %f   3p0pi0: %f" % ( stack.GetStack().Last().GetBinContent( 1), stack.GetStack().Last().GetBinContent( 2), stack.GetStack().Last().GetBinContent( 11 ) )

        pad1.Update()
        stack.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )
        if options.ratio :
            ratioHist.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )
        if options.www :
            c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlots/%s/%s.png' % (grouping, channel, var ) )
            c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlotsList/%s/%s.png' % (grouping, channel, var ) )
        else :
            c1.SaveAs('%sPlots/%s/%s.png' % (grouping, channel, var ) )
            c1.SaveAs('%sPlotsList/%s/%s.png' % (grouping, channel, var ) )
        c1.Close()

        htmlFile.write( '<img src="%s.png">\n' % var )
        #htmlFile.write( '<br>\n' )
    htmlFile.write( '</body></html>' )
    htmlFile.close()
