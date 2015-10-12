from util.buildTChain import makeTChain
import ROOT
import json
from collections import OrderedDict
import pyplotter.plot_functions as pyplotter #import setTDRStyle, getCanvas
import pyplotter.tdrstyle as tdr
import argparse
from util.ratioPlot import ratioPlot
import analysisPlots

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='25ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--ratio', action='store', default=False, dest='ratio', help="Include ratio plots? Defaul = False")
p.add_argument('--log', action='store', default=False, dest='log', help="Plot Log Y?")
p.add_argument('--folder', action='store', default='2SingleIOAD', dest='folderDetails', help="What's our post-prefix folder name?")
p.add_argument('--qcd', action='store', default=True, dest='plotQCD', help="Plot QCD?")
options = p.parse_args()
pre_ = options.sampleName
ratio = options.ratio
folderDetails = options.folderDetails

print "Running over %s samples" % pre_

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

luminosity = 592.27 # (pb) 25ns - Sept 25th certification
#luminosity = 1000.0 # (pb) 25ns - Sept 25th certification
qcdTTScaleFactor = 1.00 # from running "python makeBaseSelections.py --invert=True" and checking ration of SS / OS
qcdEMScaleFactor = 1.0
qcdYieldTT = 2610.0 # From data - MC in OS region, see plots in ZtoTauTau/FinalPlots/[tt/em]_OS_mVis_QCD_Yield.png
qcdYieldEM = 114.9 # same as TT

with open('meta/NtupleInputs_%s/samples.json' % pre_) as sampFile :
    sampDict = json.load( sampFile )

prodMap = { 'em' : ('e', 'm'),
             'tt' : ('t1', 't2')
}
                # Sample : Color
samples = OrderedDict()
samples['DYJets']   = ('kOrange-4', 'dyj')
samples['TT']       = ('kBlue-8', 'top')
#samples['TTJets']       = ('kBlue-8', 'top')
#samples['TTPow']       = ('kBlue-8', 'top')
samples['QCD']        = ('kMagenta-10', 'qcd')
samples['Tbar-tW']  = ('kYellow-2', 'top')
samples['T-tW']     = ('kYellow+2', 'top')
samples['WJets']    = ('kAzure+2', 'wjets')
samples['WW']       = ('kAzure+10', 'dib')
#samples['WW2l2n']       = ('kAzure+8', 'dib')
#samples['WW4q']     = ('kAzure+6', 'dib')
#samples['WW1l1n2q']     = ('kAzure+4', 'dib')
samples['WZJets']   = ('kAzure-4', 'dib')
#samples['WZ1l1n2q'] = ('kAzure-6', 'dib')
#samples['WZ3l1nu'] = ('kAzure-6', 'dib')
samples['ZZ']   = ('kAzure-8', 'dib')
#samples['ZZ4l'] = ('kAzure-12', 'dib')
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


for channel in prodMap.keys() :

    if channel == 'tt' : continue

    # Make an index file for web viewing
    htmlFile = open('%sPlots/%s/index.html' % (pre_, channel), 'w')
    htmlFile.write( '<html><head><STYLE type="text/css">img { border:0px; }</STYLE>\n' )
    htmlFile.write( '<title>Channel %s/</title></head>\n' % channel )
    htmlFile.write( '<body>\n' )


    print channel

    newVarMap = analysisPlots.getHistoDict( channel )
    plotDetails = analysisPlots.getPlotDetails( channel )

    for var, info in newVarMap.iteritems() :

        ttEvents = 0.0

        #if not (var == 'nbtag' or var == 'm_vis') : continue
        name = info[0]
        print "Var: %s      Name: %s" % (var, name)
        stack = ROOT.THStack("All Backgrounds stack", "%s, %s" % (channel, var) )
        dyj = ROOT.THStack("All Backgrounds dyj", "dyj" )
        dib = ROOT.THStack("All Backgrounds dib", "dib" )
        top = ROOT.THStack("All Backgrounds top", "top" )
        higgs = ROOT.THStack("All Backgrounds higgs", "higgs" )
        qcd = ROOT.THStack("All Backgrounds qcd", "qcd" )
        wjets = ROOT.THStack("All Backgrounds wjets", "wjets" )
        data = ROOT.THStack("All Backgrounds data", "data" )


        for sample in samples:
            print sample

            if channel == 'tt' and sample == 'data_em' : continue
            if channel == 'em' and sample == 'data_tt' : continue

            #print sample
            #print '%s2IsoOrderAndDups/%s_%s.root' % (pre_, sample, channel)

            if sample == 'data_em' :
                tFile = ROOT.TFile('%s%s/%s.root' % (pre_, folderDetails, sample), 'READ')
            elif sample == 'data_tt' :
                tFile = ROOT.TFile('%s%s/%s.root' % (pre_, folderDetails, sample), 'READ')
            elif sample == 'WJets' :
                tFile = ROOT.TFile('meta/%sBackgrounds/wJetsShape/shape/WJets_%s.root' % (pre_, channel), 'READ')
                tFileScale = ROOT.TFile('%s%s/%s_%s.root' % (pre_, folderDetails, sample, channel), 'READ')
                dicScale = tFileScale.Get("%s_Histos" % channel )
                histScale = dicScale.Get( "%s" % var )
                wJetsInt = histScale.Integral()
            elif sample == 'QCD' :
                tFile = ROOT.TFile('meta/%sBackgrounds/QCDShape/shape/data_%s.root' % (pre_, channel), 'READ')
            else :
                tFile = ROOT.TFile('%s%s/%s_%s.root' % (pre_, folderDetails, sample, channel), 'READ')


            dic = tFile.Get("%s_Histos" % channel )
            hist = dic.Get( "%s" % var )
            hist.SetDirectory( 0 )


            hist.Rebin( plotDetails[ var ][2] )
            if 'data' not in sample and samples[ sample ][1] != 'higgs' :
                color = "ROOT.%s" % sampColors[ samples[ sample ][1] ]
                hist.SetFillColor( eval( color ) )
                hist.SetLineColor( ROOT.kBlack )
                hist.SetLineWidth( 2 )
            elif samples[ sample ][1] == 'higgs' :
                hist.SetLineColor( ROOT.kBlue )
                hist.SetLineWidth( 4 )
                hist.SetLineStyle( 7 )
            else :
                hist.SetLineColor( ROOT.kBlack )
                hist.SetLineWidth( 2 )
                hist.SetMarkerStyle( 21 )
            #hist.SaveAs('plots/%s/%s.root' % (channel, sample) )

            ''' Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ),
            QCD gets special scaling from bkg estimation, see qcdYield[channel] above for details '''
            print "PRE Sample: %s      Int: %f" % (sample, hist.Integral() )
            if sample == 'QCD' and hist.Integral() != 0 :
                if channel == 'em' : hist.Scale( qcdYieldEM / hist.Integral() )
                if channel == 'tt' : hist.Scale( qcdYieldTT / hist.Integral() )
            elif sample == 'WJets' and hist.Integral() != 0 :
                scaler = luminosity * sampDict[ sample ]['Cross Section (pb)'] / ( sampDict[ sample ]['summedWeightsNorm'] )
                hist.Scale( scaler * wJetsInt / hist.Integral() )
            elif 'data' not in sample and hist.Integral() != 0:
                scaler = luminosity * sampDict[ sample ]['Cross Section (pb)'] / ( sampDict[ sample ]['summedWeightsNorm'] )
                hist.Scale( scaler )

            print " --- Sample: %s      Int: %f" % (sample, hist.Integral() )

            if samples[ sample ][1] == 'dyj' :
                hist.SetTitle('Z #rightarrow #tau#tau')
                dyj.Add( hist )
            if samples[ sample ][1] == 'qcd' :
                hist.SetTitle('QCD')
                qcd.Add( hist )
            if samples[ sample ][1] == 'top' :
                hist.SetTitle('Single & Double Top')
                top.Add( hist )
            if samples[ sample ][1] == 'dib' :
                hist.SetTitle('Di-Boson')
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


        if options.plotQCD == True :
            stack.Add( qcd.GetStack().Last() )
        stack.Add( top.GetStack().Last() )
        stack.Add( dib.GetStack().Last() )
        stack.Add( wjets.GetStack().Last() )
        stack.Add( dyj.GetStack().Last() )

        # Maybe make ratio hist
        c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 600, 600)

        if ratio == False :
            pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
            pad1.Draw()
            pad1.cd()
        if ratio == True :
            pads = ratioPlot( c1 )
            pad1 = pads[0]
            ratioPad = pads[1]
            pad1.cd()
            #varMin_ = dyj.GetStack().Last()
            #ratioHist = ROOT.TH1('ratio plot' + var, 'ratio',

        stack.Draw('hist')
        data.GetStack().Last().Draw('esamex0')

        # X Axis!
        stack.GetXaxis().SetTitle("%s" % plotDetails[ var ][ 3 ])

        # Set Y axis titles appropriately
        if hist.GetBinWidth(1) < .05 :
            binWidth = str( round( hist.GetBinWidth(1), 2) )
        elif hist.GetBinWidth(1) < .5 :
            binWidth = str( round( hist.GetBinWidth(1), 1) )
        else:
            binWidth = round( hist.GetBinWidth(1), 0)
        if plotDetails[ var ][ 4 ] == '' :
            stack.GetYaxis().SetTitle("Events")
        else :
            if hist.GetBinWidth(1) < .5 :
                stack.GetYaxis().SetTitle("Events / %s%s" % ( binWidth, plotDetails[ var ][ 4 ] ) )
            else :
                stack.GetYaxis().SetTitle("Events / %i%s" % ( binWidth, plotDetails[ var ][ 4 ] ) )

        stack.SetTitle( "CMS Preliminary        %f pb^{-1} ( 13 TeV )" % luminosity )

        # Set axis and viewing area
        #higgsMin = higgs.GetMaximum()
        #print "higgs max: %f" % higgsMin
        #stackMin = stack.GetStack().First().GetMaximum()
        #print "stack max: %f" % stackMin
        #stack.SetMinimum( min( higgsMin, stackMin) * 0.3 )
        stackMax = stack.GetStack().Last().GetMaximum()
        dataMax = data.GetStack().Last().GetMaximum()
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
        legend.AddEntry( data.GetStack().Last(), "Data", 'lep')
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

        lumi = ROOT.TText(.7,1.05,"%i pb^{-1} (13 TeV)" % luminosity)
        lumi.SetTextSize(0.03)
        lumi.DrawTextNDC(.7,.96,"%i / pb (13 TeV)" % luminosity)

        ''' Random print outs on plots '''
        #mean1 = ROOT.TText(.4,.6,"Data Integral: %f" % data.GetStack().Last().GetMean() )
        #mean1.SetTextSize(0.04)
        #mean1.DrawTextNDC(.65,.6,"Data Integral: %s" % str( round( data.GetStack().Last().Integral(), 1) ) )
        #mean2 = ROOT.TText(.4,.55,"Data Int: %s" % str( data.GetStack().Last().Integral() ) )
        #mean2.SetTextSize(0.04)
        #mean2.DrawTextNDC(.65,.55,"MC Integral: %s" % str( round( stack.GetStack().Last().Integral(), 1) ) )
        #mean3 = ROOT.TText(.4,.55,"Data Mean: %s" % str( data.GetStack().Last().GetMean() ) )
        #mean3.SetTextSize(0.04)
        #mean3.DrawTextNDC(.65,.50,"Diff = QCD: %s" % str( round( data.GetStack().Last().Integral() - stack.GetStack().Last().Integral(), 1) ) )
        #mean4 = ROOT.TText(.4,.55,"Data Int: %s" % str( data.GetStack().Last().Integral() ) )
        #mean4.SetTextSize(0.05)
        #mean4.DrawTextNDC(.65,.45,"SS Selection" )

        pad1.Update()
        stack.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )
        c1.SaveAs('%sPlots/%s/%s.png' % (pre_, channel, var ) )
        c1.SaveAs('%sPlotsList/%s/%s.png' % (pre_, channel, var ) )
        c1.Close()

        htmlFile.write( '<img src="%s.png">\n' % var )
        htmlFile.write( '<br>\n' )
    htmlFile.write( '</body></html>' )
    htmlFile.close()
