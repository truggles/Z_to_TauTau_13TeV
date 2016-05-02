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
import math
from analysisPlots import skipSystShapeVar

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='dataCards', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--ratio', action='store', default=True, dest='ratio', help="Include ratio plots? Defaul = False")
p.add_argument('--log', action='store', default=False, dest='log', help="Plot Log Y?")
p.add_argument('--folder', action='store', default='2SingleIOAD', dest='folderDetails', help="What's our post-prefix folder name?")
p.add_argument('--text', action='store', default=False, dest='text', help="Add text?")
p.add_argument('--qcdShape', action='store', default='Sync', dest='qcdShape', help="Which QCD shape to use? Sync or Loose triggers")
p.add_argument('--qcdMake', action='store', default=False, dest='qcdMake', help="Make a data - MC qcd shape?")
p.add_argument('--qcdMakeDM', action='store', default='x', dest='qcdMakeDM', help="Make a data - MC qcd shape for a specific DM?")
p.add_argument('--useQCDMake', action='store', default=False, dest='useQCDMake', help="Use a data - MC qcd shape?")
p.add_argument('--useQCDMakeName', action='store', default='x', dest='useQCDMakeName', help="Use a specific qcd shape?")
p.add_argument('--useQCDMakeDM', action='store', default=False, dest='useQCDMakeDM', help="Use a data - MC qcd shape for DM 0, 1, 10?")
p.add_argument('--QCDYield', action='store', default=False, dest='QCDYield', help="Define a QCD yield even when using a shape file?")
p.add_argument('--qcdMC', action='store', default=False, dest='qcdMC', help="Use QCD from MC?")
p.add_argument('--mssm', action='store', default=False, dest='mssm', help="Plot MSSM?")
p.add_argument('--blind', action='store', default=True, dest='blind', help="Blind Data?")
p.add_argument('--channels', action='store', default='em,tt', dest='channels', help="What channels?")
p.add_argument('--addUncert', action='store', default=True, dest='addUncert', help="What channels?")
p.add_argument('--qcdSF', action='store', default='1.9/1.0', dest='qcdSF', help="Choose QCD SF, default is 1.9 for EMu, TT must be specified")
p.add_argument('--btag', action='store', default=False, dest='btag', help="BTagging has specific binning")
options = p.parse_args()
grouping = options.sampleName
ratio = options.ratio
folderDetails = options.folderDetails


print "Running over %s samples" % grouping

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

cmsLumi = float(os.getenv('LUMI'))
print "Lumi = %i" % cmsLumi

mssmMass = 250
mssmSF = 100
higgsSF = 10
qcdTTScaleFactor = 1.06
qcdTTScaleFactor = 504.5 / 676.6 # Feb24, no2p, Medium -> VTight
#qcdEMScaleFactor = 1.06
qcdEMScaleFactor = 1.9
#qcdTTScaleFactor = 1.25
#qcdTTScaleFactorNew = 499.075601 / 684.737359 
#qcdTTScaleFactorNew = 0.49 # no 2 prong, baseline
#qcdTTScaleFactorNew = 430./628. # no 2 prong, boosted Z, pt > 100
#qcdTTScaleFactorNew = 430./978. # no 2 prong, boosted Z, pt > 100, rlx iso2 to 5
#qcdEMScaleFactor = 1.5
#qcdEMScaleFactor = 1.9
bkgsTTScaleFactor = 1.0

# DM specific scaling
dm0sf = 1.27
dm1sf = 1.21
dm10sf = 1.14

qcdYieldTT = 35.7 * qcdTTScaleFactor
qcdYieldEM = 1586.0 *  qcdEMScaleFactor

with open('meta/NtupleInputs_%s/samples.json' % grouping) as sampFile :
    sampDict = json.load( sampFile )

chans = {
    'tt' : '#tau_{h}#tau_{h}',
    'em' : 'e#mu',
}


                # Sample : Color
samples = OrderedDict()
#samples['ggHtoTauTau125'] = ('kBlue', 'higgs')
#samples['VBFHtoTauTau125'] = ('kBlue', 'higgs')
samples['DYJetsBig-ZTT']   = ('kOrange-4', 'ztt')
samples['DYJetsBig-ZL']   = ('kOrange-4', 'zl')
samples['DYJetsBig-ZJ']   = ('kOrange-4', 'zj')
samples['DYJetsBig-ZLL']   = ('kOrange-4', 'zll')
samples['DYJets1-ZTT']   = ('kOrange-4', 'ztt')
samples['DYJets1-ZL']   = ('kOrange-4', 'zl')
samples['DYJets1-ZJ']   = ('kOrange-4', 'zj')
samples['DYJets1-ZLL']   = ('kOrange-4', 'zll')
samples['DYJets2-ZTT']   = ('kOrange-4', 'ztt')
samples['DYJets2-ZL']   = ('kOrange-4', 'zl')
samples['DYJets2-ZJ']   = ('kOrange-4', 'zj')
samples['DYJets2-ZLL']   = ('kOrange-4', 'zll')
samples['DYJets3-ZTT']   = ('kOrange-4', 'ztt')
samples['DYJets3-ZL']   = ('kOrange-4', 'zl')
samples['DYJets3-ZJ']   = ('kOrange-4', 'zj')
samples['DYJets3-ZLL']   = ('kOrange-4', 'zll')
samples['DYJets4-ZTT']   = ('kOrange-4', 'ztt')
samples['DYJets4-ZL']   = ('kOrange-4', 'zl')
samples['DYJets4-ZJ']   = ('kOrange-4', 'zj')
samples['DYJets4-ZLL']   = ('kOrange-4', 'zll')
samples['DYJetsLow-ZTT']   = ('kOrange-4', 'ztt')
samples['DYJetsLow-ZL']   = ('kOrange-4', 'zl')
samples['DYJetsLow-ZJ']   = ('kOrange-4', 'zj')
samples['DYJetsLow-ZLL']   = ('kOrange-4', 'zll')
samples['T-tW']     = ('kYellow+2', 'dib')
samples['T-tchan']     = ('kYellow+2', 'dib')
samples['TT']       = ('kBlue-8', 'top')
samples['Tbar-tW']  = ('kYellow-2', 'dib')
samples['Tbar-tchan']  = ('kYellow-2', 'dib')
samples['WJets']    = ('kAzure+2', 'wjets')
samples['WJets1']    = ('kAzure+2', 'wjets')
samples['WJets2']    = ('kAzure+2', 'wjets')
samples['WJets3']    = ('kAzure+2', 'wjets')
samples['WJets4']    = ('kAzure+2', 'wjets')
samples['WW1l1nu2q']       = ('kAzure+8', 'dib')
#samples['WW2l2nu']       = ('kAzure+8', 'dib')
samples['WZ1l1nu2q'] = ('kAzure-6', 'dib')
samples['WZ1l3nu'] = ('kAzure-6', 'dib')
samples['WZ2l2q'] = ('kAzure-6', 'dib')
samples['WZ3l1nu'] = ('kAzure-6', 'dib')
#samples['ZZ2l2nu'] = ('kAzure-12', 'dib')
samples['ZZ2l2q'] = ('kAzure-12', 'dib')
samples['ZZ4l'] = ('kAzure-12', 'dib')
samples['VV'] = ('kAzure-12', 'dib')
samples['QCD']        = ('kMagenta-10', 'qcd')
samples['data_tt']  = ('kBlack', 'data')
samples['data_em']  = ('kBlack', 'data')
samples['ggH%i' % mssmMass] = ('kPink', 'mssm')
samples['bbH%i' % mssmMass] = ('kPink', 'mssm') 

sampColors = {
    'dib' : ROOT.kRed+2,
    'top' : ROOT.kBlue-8,
    'qcd' : ROOT.TColor.GetColor(250,202,255), #kMagenta-10
    'ztt' : ROOT.TColor.GetColor(248,206,104), #kOrange-4,
    'zl' : ROOT.kAzure+2,
    'zj' : ROOT.kGreen+2,
    'zll' : ROOT.TColor.GetColor(100,182,232),
    'wjets' : ROOT.kAzure+6,
    'higgs' : ROOT.kBlue,
    'mssm' : ROOT.kPink,
    'data' : ROOT.kBlack,
}


for channel in ['em', 'tt'] :

    #if channel == 'tt' : continue
    #if channel == 'em' : continue
    if 'tt' not in options.channels and channel == 'tt' : continue
    if 'em' not in options.channels and channel == 'em' : continue
    if channel == 'tt' : mssmSF = int(mssmSF / 10)

    # Make an index file for web viewing
    if not os.path.exists( '%sPlots' % grouping ) :
        os.makedirs( '%sPlots/em' % grouping )
        os.makedirs( '%sPlots/tt' % grouping )
    if not os.path.exists( '%sPlotsList' % grouping ) :
        os.makedirs( '%sPlotsList/em' % grouping )
        os.makedirs( '%sPlotsList/tt' % grouping )
    htmlFile = open('/afs/cern.ch/user/t/truggles/www/%sPlots/%s/index.html' % (grouping, channel), 'w')
    htmlFile.write( '<html><head><STYLE type="text/css">img { border:0px; }</STYLE>\n' )
    htmlFile.write( '<title>Channel %s/</title></head>\n' % channel )
    htmlFile.write( '<body>\n' )


    print channel

    newVarMap = analysisPlots.getHistoDict( channel )
    plotDetails = analysisPlots.getPlotDetails( channel )

    if options.qcdMake :
        finalQCDYield = 0.0
        finalDataYield = 0.0
        if not os.path.exists('meta/%sBackgrounds' % grouping) :
            os.makedirs('meta/%sBackgrounds' % grouping)
        if options.qcdMakeDM != 'x' :
            print "qcdMakeDM called: ",options.qcdMakeDM
            qcdMaker = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s.root' % (grouping, channel, options.qcdMakeDM), 'RECREATE')
        else :
            qcdMaker = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape.root' % (grouping, channel), 'RECREATE')
        qcdDir = qcdMaker.mkdir('%s_Histos' % channel)

    #print newVarMap
    for var, info in newVarMap.iteritems() :

        #if 'mt_sv' in var : continue
        #if not (var == 'pZeta-0.85pZetaVis' or var == 'm_vis') : continue
        #if not 'm_vis_mssm' in var : continue
        #if not (var == 't1DecayMode' or var == 't2DecayMode') : continue
        name = info[0]
        print "Var: %s      Name: %s" % (var, name)


        """
        Handle variable binning and longer ranges for visible mass
        """
        if '_mssm' in var :
            varBinned = True
            if 'ZTT' in options.folderDetails :
                print "Inclusive"
                xBins = array( 'd', [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900] )
            elif 'NoBTL' in options.folderDetails :
                print "No-BTAGGING"
                xBins = array( 'd', [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900] )
            elif 'NoBTL' not in options.folderDetails :
                print "BTAGGING"
                xBins = array( 'd', [0,20,40,60,80,100,120,140,160,180,200,250,300,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900] )

        elif var == 'm_vis_mssm' :
            varBinned = True
            #xBins = array( 'd', [0,20,40,60,80,100,150,200,250,350,600,1000,1500,2000,2500,3500] )
            xBins = array( 'd', [] )
            for i in range(0, 351 ) :
                xBins.append( i * 10 )
        elif var == 'm_vis_varB' :
            varBinned = True
            xBins = array('d', [0,20,40,60,80,100,150,200,250,350,600])
        else :
            varBinned = False
            first = info[2] * 1.
            last = info[3] * 1.
            totBins = ( info[1] / (plotDetails[ var ][2]) ) * 1.
            binWidth = (last - first)/totBins
            #print first, last, totBins, binWidth
            xBins = array('d', []) 
            for i in range( 0, int(totBins)+1 ) :
                if 'iso' in var :
                    xBins.append( round(i*binWidth+first,2) )
                else :
                    xBins.append( round(i*binWidth+first,1) )
        xNum = len( xBins ) - 1
        #print "Binning scheme: ",xBins
            


        append = var + channel
        stack = ROOT.THStack("All Backgrounds stack", "%s, %s" % (channel, var) )
        ztt = ROOT.TH1F("All Backgrounds ztt %s" % append, "ztt", xNum, xBins )
        zl = ROOT.TH1F("All Backgrounds zl %s" % append, "zl", xNum, xBins )
        zj = ROOT.TH1F("All Backgrounds zj %s" % append, "zj", xNum, xBins )
        zll = ROOT.TH1F("All Backgrounds zll %s" % append, "zll", xNum, xBins )
        dib = ROOT.TH1F("All Backgrounds dib %s" % append, "dib", xNum, xBins )
        top = ROOT.TH1F("All Backgrounds top %s" % append, "top", xNum, xBins )
        higgs = ROOT.TH1F("All Backgrounds higgs %s" % append, "higgs", xNum, xBins )
        mssm = ROOT.TH1F("All Backgrounds mssm %s" % append, "mssm", xNum, xBins )
        qcd = ROOT.TH1F("All Backgrounds qcd %s" % append, "qcd", xNum, xBins )
        wjets = ROOT.TH1F("All Backgrounds wjets %s" % append, "wjets", xNum, xBins )
        data = ROOT.TH1F("All Backgrounds data %s" % append, "data", xNum, xBins )
        ztt.Sumw2()
        zl.Sumw2()
        zj.Sumw2()
        zll.Sumw2()
        dib.Sumw2()
        top.Sumw2()
        higgs.Sumw2()
        mssm.Sumw2()
        qcd.Sumw2()
        wjets.Sumw2()
        data.Sumw2()


        pZetaTot = 0
        for sample in samples:

            ''' Skip plotting unused shape systematics '''
            if skipSystShapeVar( var, sample, channel ) : continue

            if channel == 'tt' and sample == 'data_em' : continue
            if channel == 'tt' and '-ZLL' in sample : continue
            if channel == 'em' and sample == 'data_tt' : continue
            if channel == 'em' and '-ZJ' in sample : continue
            if channel == 'em' and '-ZL' in sample and not '-ZLL' in sample : continue
            if options.qcdMC and sample == 'QCD' : continue
            if not options.qcdMC and 'QCD' in sample and '-' in sample : continue

            #if var == 'm_vis' : print sample
            #print '%s2IsoOrderAndDups/%s_%s.root' % (grouping, sample, channel)

            if sample == 'data_em' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif sample == 'data_tt' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif 'QCD' in sample :
                if options.useQCDMake :
                    if options.useQCDMakeName != 'x'  :
                        tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s.root' % (grouping, channel, options.useQCDMakeName), 'READ')
                    elif options.useQCDMakeDM  :
                        tFile1 = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_dm0.root' % (grouping, channel), 'READ')
                        tFile2 = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_dm1.root' % (grouping, channel), 'READ')
                        tFile3 = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_dm10.root' % (grouping, channel), 'READ')
                        print "Got QCD make file DM specific:", sample
                    else :
                        tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape.root' % (grouping, channel), 'READ')
                        print "Got QCD make file:", sample
                elif options.qcdMC :
                    print "Got QCD MC file", sample
                    tFile = ROOT.TFile('%s%s/%s_%s.root' % (grouping, folderDetails, sample, channel), 'READ')
                    hxx = tFile.Get('%s_Histos/metphi' % channel)
                    print "QCD MC: %s Integral %f" % (sample, hxx.Integral() )
                else :
                    continue
                    #tFile = ROOT.TFile('meta/%sBackgrounds/QCDShape%s/shape/data_%s.root' % (grouping, options.qcdShape, channel), 'READ')
            else :
                #print "File: '%s%s/%s_%s.root'" % (grouping, folderDetails, sample, channel)
                tFile = ROOT.TFile('%s%s/%s_%s.root' % (grouping, folderDetails, sample, channel), 'READ')


            if not options.useQCDMakeDM or 'QCD' not in sample :
                dic = tFile.Get("%s_Histos" % channel )
            if 'm_vis' in var :
                if 'QCD' in sample and options.useQCDMake :
                    if options.useQCDMakeDM :
                        print "multiple dics"
                        dic1 = tFile1.Get("%s_Histos" % channel )
                        dic2 = tFile2.Get("%s_Histos" % channel )
                        dic3 = tFile3.Get("%s_Histos" % channel )
                        preHist = dic1.Get( var )
                        preHist.Scale( dm0sf )
                        preHist.Add( dic2.Get( var ) * dm1sf )
                        preHist.Add( dic3.Get( var ) * dm10sf )
                        #preHist2 = dic2.Get( var )
                        #preHist3 = dic3.Get( var )
                        #preHist =
                    else :
                        preHist = dic.Get( var )
                elif 'data' in sample :
                    preHist = dic.Get( 'm_vis' )
                else :
                    preHist = dic.Get( var )
            elif 'QCD' in sample and options.useQCDMakeDM :
                print "multiple dics"
                dic1 = tFile1.Get("%s_Histos" % channel )
                dic2 = tFile2.Get("%s_Histos" % channel )
                dic3 = tFile3.Get("%s_Histos" % channel )
                preHist = dic1.Get( var )
                preHist.Scale( dm0sf )
                preHist.Add( dic2.Get( var ) * dm1sf )
                preHist.Add( dic3.Get( var ) * dm10sf )

            else : preHist = dic.Get( var )
            preHist.SetDirectory( 0 )

            if sample == 'QCD' and options.useQCDMake and not options.useQCDMakeDM and not options.useQCDMakeName :
                if channel == 'em' :
                    print "Skip rebin; Scale QCD shape by %f" % qcdEMScaleFactor
                    preHist.Scale( qcdEMScaleFactor )
                    print "QCD yield: %f" % preHist.Integral()
                    hist = ROOT.TH1F( preHist )
                if channel == 'tt' :
                    print "Skip rebin; Scale QCD shape by %f" % qcdTTScaleFactor
                    preHist.Scale( qcdTTScaleFactor )
                    print "QCD yield: %f" % preHist.Integral()
                    hist = ROOT.TH1F( preHist )
            # If we use this option we specify a scaling factor
            elif sample == 'QCD' and options.useQCDMakeName :
                print "Using QCD SCALE FACTOR <<<< NEW >>>>"
                #if channel == 'em' :
                #    print "Skip rebin; Scale QCD shape by %f" % qcdEMScaleFactor
                #    preHist.Scale( qcdEMScaleFactor )
                #
                #if channel == 'tt' :
                #    print "Skip rebin; Scale QCD shape by %f" % qcdTTScaleFactor
                #    preHist.Scale( qcdTTScaleFactor )
                qcdSF_s = options.qcdSF
                if '/' in qcdSF_s :
                    qcdSF = float(qcdSF_s.split('/')[0]) / float(qcdSF_s.split('/')[1])
                else : qcdSF = float(qcdSF_s)
                print "Using qcdSF from command line: %s" % qcdSF
                preHist.Scale( qcdSF )
                #print "Skip rebin; Scale QCD shape by %f" % qcdTTScaleFactorNew
                #preHist.Scale( qcdTTScaleFactorNew )
                print "QCD yield: %f" % preHist.Integral()
                hist = ROOT.TH1F( preHist )
            else :
                #preHist.Rebin( plotDetails[ var ][2] )
                #print "Rebinning"
                #print xNum
                #print xBins
                hist = preHist.Rebin( xNum, "rebinned", xBins )
                #print "Done Rebinning"



            ''' Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ),
            QCD gets special scaling from bkg estimation, see qcdYield[channel] above for details '''
            #print "PRE Sample: %s      Int: %f" % (sample, hist.Integral() )
            if sample == 'QCD' and hist.Integral() != 0 :
                if not options.useQCDMake or options.QCDYield :
                    if channel == 'em' : hist.Scale( qcdYieldEM / hist.Integral() )
                    if channel == 'tt' : hist.Scale( qcdYieldTT / hist.Integral() )
                    print "Using QCD Yield numbers from this file, QCD Int: %f" % hist.Integral()
            elif 'data' not in sample and hist.Integral() != 0:
                if 'TT' in sample :
                    hist.Scale( bkgsTTScaleFactor )
                elif 'QCD' in sample :
                    if channel == 'em' : hist.Scale( qcdEMScaleFactor )


            ''' For TT rescaling studies in pZeta distributions '''
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


            #if var == 'mt_sv' :
            if var == 'mt_sv_mssm' :
                if 'data' in sample and options.qcdMake : finalDataYield = hist.Integral()

            if samples[ sample ][1] == 'ztt' :
                ztt.Add( hist )
            if samples[ sample ][1] == 'zl' :
                zl.Add( hist )
            if samples[ sample ][1] == 'zj' :
                zj.Add( hist )
            if samples[ sample ][1] == 'zll' :
                zll.Add( hist )
            if samples[ sample ][1] == 'qcd' :
                qcd.Add( hist )
                #print "qcd Stack yield: %f" % qcd.GetStack().Last().Integral()
                print "qcd Stack yield: %f" % qcd.Integral()
            if samples[ sample ][1] == 'top' :
                top.Add( hist )
            if samples[ sample ][1] == 'dib' :
                dib.Add( hist )
            if samples[ sample ][1] == 'wjets' :
                wjets.Add( hist )
            if samples[ sample ][1] == 'mssm' :
                mssm.Add( hist )
            if samples[ sample ][1] == 'higgs' :
                higgs.Add( hist )
            if samples[ sample ][1] == 'data' :
                data.Add( hist )
            tFile.Close()

        Ary = { qcd : "qcd", top : "top", dib : "dib", wjets : "wjets", ztt : "ztt", zl :  "zl", zj : "zj", zll : "zll" }
        for h in Ary.keys() :
            h.SetFillColor( sampColors[ Ary[h] ] )
            h.SetLineColor( ROOT.kBlack )
            h.SetLineWidth( 2 )
        data.SetLineColor( ROOT.kBlack )
        data.SetLineWidth( 2 )
        data.SetMarkerStyle( 21 )
        Ary[ data ] = "data"
        if not options.mssm :
            higgs.SetLineColor( ROOT.kBlue )
            higgs.SetLineWidth( 4 )
            higgs.SetLineStyle( 7 )
            higgs.SetMarkerStyle( 0 )
        else :
            higgs.SetFillColor( ROOT.kGreen )
            higgs.SetLineColor( ROOT.kBlack )
            higgs.SetLineWidth( 2 )
        Ary[ higgs ] = "higgs"
        mssm.SetLineColor( ROOT.kPink )
        mssm.SetLineWidth( 4 )
        mssm.SetLineStyle( 7 )
        mssm.SetMarkerStyle( 0 )
        Ary[ mssm ] = "mssm"
        
        # With Variable binning, need to set bin content appropriately
        for h in Ary.keys() :
            if not varBinned : continue
            if Ary[h] == "qcd" : continue
            for bin_ in range( 1, 11 ) :
                h.SetBinContent( bin_, h.GetBinContent( bin_ ) * ( h.GetBinWidth(1) / h.GetBinWidth( bin_ ) ) )

        # Set hist Names
        Names = { "data" : "Data", "mssm" : "MSSM(%i) x %i" % (mssmMass, mssmSF), "qcd" : "QCD", "top" : "t#bar{t}", "dib" : "VV", "wjets" : "WJets", "ztt" : "Z#rightarrow#tau#tau", "zl" : "Z#rightarrowee (lepton)", "zj" : "Z#rightarrowee (jet)", "zll" : "Z#rightarrowee" }
        if options.mssm : Names["higgs"] = "SM Higgs(125)"
        else : Names["higgs"] = "SM Higgs(125) x %i" % higgsSF
        for h in Ary.keys() :
            h.SetTitle( Names[ Ary[h] ] )
            

        #if options.mssm :
        #    stack.Add( higgs )
        if not options.qcdMake :
            print "Adding QCD: ",qcd.Integral()
            stack.Add( qcd )
        stack.Add( top )
        stack.Add( dib )
        stack.Add( wjets )
        if channel != 'em' :
            stack.Add( zl )
            stack.Add( zj )
        if channel == 'em' :
            stack.Add( zll )
        stack.Add( ztt )


        """
        Calculate rough bin-by-bin uncertainties
        """
        binErrors = []
        for k in range( top.GetNbinsX()+1 ) :
            toRoot = (top.GetBinContent( k )*.1)**2
            toRoot += (dib.GetBinContent(k)*.1)**2
            toRoot += (wjets.GetBinContent(k)*.1)**2
            toRoot += (ztt.GetBinContent(k)*.1)**2
            toRoot += (qcd.GetBinContent(k)*.2)**2
            if channel != 'em' :
                toRoot += (zj.GetBinContent(k)*.1)**2
                toRoot += (zl.GetBinContent(k)*.1)**2
            if channel == 'em' :
                toRoot += (zll.GetBinContent(k)*.1)**2
            binErrors.append( math.sqrt(toRoot) )


        # Scale Higgs samples for viewing
        if not options.mssm :
            higgs.Scale( higgsSF )
        mssm.Scale( mssmSF )

            
        if options.qcdMake :
            qcdVar = ROOT.TH1F( var, 'qcd%s%s' % (append,var), xNum, xBins )
            qcdVar.Sumw2()
            qcdVar.Add( data )
            qcdVar.Add( -1 * stack.GetStack().Last() )
            qcdVar.SetFillColor( ROOT.kMagenta-10 )
            qcdVar.SetLineColor( ROOT.kBlack )
            qcdVar.SetLineWidth( 2 )
            # Add the shape estimated here to the stack pre-scaling!!!
            stack.Add( qcdVar ) 
            if var == 'm_vis_mssm' :
                print "M_VIS_MSSM plot details: %f %f" % (plotDetails[ var ][0], plotDetails[ var ][1])
            qcdVar.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )
            print "qcdVar: %f   mean %f" % (qcdVar.Integral(), qcdVar.GetMean() )
            if var == 'mt_sv_mssm' :
                #print "QCD Binning"
                #print xBins
                finalQCDYield = qcdVar.Integral()
            qcdDir.cd()
            qcdVar.Write()


        # Maybe make ratio hist
        c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 550, 550)

        if not options.ratio :
            pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
            pad1.Draw()
            pad1.cd()
            stack.Draw('hist')
            if options.mssm :
                mssm.Draw('same')
            else :
                higgs.Draw('same')
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
            ratioHist = ROOT.TH1F('ratio %s' % append, 'ratio', xNum, xBins )
            ratioHist.Sumw2()
            ratioHist.Add( data )
            ratioHist.Divide( stack.GetStack().Last() )
            if channel == 'em' :
                ratioHist.SetMaximum( 1.5 )
                ratioHist.SetMinimum( 0.5 )
            if channel == 'tt' :
                ratioHist.SetMaximum( 1.5 )
                ratioHist.SetMinimum( 0.5 )
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
            ratioHist.GetYaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
            ratioHist.GetYaxis().SetTitleOffset( smlPadSize*1.5 )
            ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize()*( 1/smlPadSize) )
            ratioHist.GetYaxis().SetNdivisions( 5, True )
            ratioHist.GetXaxis().SetLabelSize( ratioHist.GetXaxis().GetLabelSize()*( 1/smlPadSize) )
            ratioHist.GetXaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( 1/smlPadSize) )


            pad1.cd()
            stack.Draw('hist')
            if options.mssm :
                mssm.Draw('same')
            #else :
            #    higgs.Draw('same')
            data.Draw('esamex0')


        # Set Y axis titles appropriately
        #binWidth = str( round( hist.GetBinWidth(1), 0) )
        if plotDetails[ var ][ 4 ] == '' :
            stack.GetYaxis().SetTitle("Events")
        else :
            stack.GetYaxis().SetTitle("Events / %s%s" % (str(round(stack.GetStack().Last().GetBinWidth(1),1)), plotDetails[ var ][ 4 ])  )
        #    if hist.GetBinWidth(1) < .5 :
        #        stack.GetYaxis().SetTitle("Events / %s%s" % ( binWidth, plotDetails[ var ][ 4 ] ) )
        #    else :
        #        stack.GetYaxis().SetTitle("Events / %i%s" % ( binWidth, plotDetails[ var ][ 4 ] ) )

        stack.SetTitle( "CMS Preliminary        %f pb^{-1} ( 13 TeV )" % cmsLumi )

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
        #if not options.mssm :
        #    legend.AddEntry( higgs, "SM Higgs(125) x %i" % higgsSF, 'l')
        if options.mssm :
            legend.AddEntry( mssm, "MSSM(%i) x %i" % (mssmMass, mssmSF), 'l')
        for j in range(0, stack.GetStack().GetLast() + 1) :
            last = stack.GetStack().GetLast()
            legend.AddEntry( stack.GetStack()[ last - j ], stack.GetStack()[last - j ].GetTitle(), 'f')
        legend.Draw()

        # Set CMS Styles Stuff
        logo = ROOT.TText(.2, .88,"CMS Preliminary")
        logo.SetTextSize(0.03)
        logo.DrawTextNDC(.2, .89,"CMS Preliminary")

        chan = ROOT.TLatex(.2, .80,"x")
        chan.SetTextSize(0.05)
        chan.DrawLatexNDC(.2, .84,"Channel: %s" % chans[channel] )

        lumi = ROOT.TText(.7,1.05,"%f fb^{-1} (13 TeV)" % round(cmsLumi/1000,2) )
        lumi.SetTextSize(0.03)
        lumi.DrawTextNDC(.7,.96,"2.3 / fb (13 TeV)" )

        ''' Random print outs on plots '''
        if options.text and not varBinned :
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

        #if (var == 't1DecayMode' or var == 't2DecayMode') :
        #    print var + " DATA: 1p0pi0: %f   1p1pi0: %f   3p0pi0: %f" % ( data.GetBinContent( 1), data.GetBinContent( 2), data.GetBinContent( 11 ) )
        #    print var + " MC: 1p0pi0: %f   1p1pi0: %f   3p0pi0: %f" % ( stack.GetStack().Last().GetBinContent( 1), stack.GetStack().Last().GetBinContent( 2), stack.GetStack().Last().GetBinContent( 11 ) )


        pad1.Update()
        stack.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )
        if options.ratio :
            ratioHist.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )


        """
        Add uncertainty bands on background stack
        """
        if options.addUncert :
            e1 = ROOT.TH1F("e1 %s" % append, "e1", xNum, xBins )
            e1.Sumw2()
            e1.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )
            for k in range( e1.GetNbinsX()+1 ) :
                e1.SetBinContent( k, stack.GetStack().Last().GetBinContent( k ) )
                e1.SetBinError(k, binErrors[k] )
                #print "Qcd Error:",qcd.GetBinError(k)
            e1.SetLineColor( 0 )
            e1.SetLineWidth( 0 )
            e1.SetMarkerSize( 0 )
            e1.SetFillStyle( 3002 )
            #e1.SetFillStyle( 3244 )
            e1.SetFillColor( 15 )
            e1.Draw('same e2')


        """ Blinding Data """
        if options.blind and ('m_vis' in var or 'm_sv' in var or 'mt_sv' in var or 'mt_tot' in var) :
            nBins = stack.GetStack().Last().GetXaxis().GetNbins()
            for k in range( nBins+1 ) :
                if data.GetXaxis().GetBinLowEdge(k+1)>170 :
                    data.SetBinContent(k, 0.)
                    data.SetBinError(k, 0.)
                    if options.ratio :
                        ratioHist.SetBinContent(k, 0.)
                        ratioHist.SetBinError(k, 0.)
            if options.ratio : 
                ratioPad.cd()
                ratioHist.Draw('esamex0')
            pad1.cd()
        data.Draw('esamex0')
            


        c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlots/%s/%s.png' % (grouping, channel, var ) )
        c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlotsList/%s/%s.png' % (grouping, channel, var ) )


        """ Additional views for Visible Mass """
        #if 'm_vis' in var :
        #    pad1.SetLogy()
        #    stack.SetMaximum( stack.GetMaximum() * 10 )
        #    stack.SetMinimum( higgs.GetMaximum() * .1 )
        #    if var == 'm_vis_mssm' :
        #        pad1.SetLogx()
        #        if options.ratio : ratioPad.SetLogx()
        #    pad1.Update()
        #    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlots/%s/%s_LogY.png' % (grouping, channel, var ) )
        #    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlotsList/%s/%s_LogY.png' % (grouping, channel, var ) )
        #    htmlFile.write( '<img src="%s_LogY.png">\n' % var )
        c1.Close()

        htmlFile.write( '<img src="%s.png">\n' % var )
        #htmlFile.write( '<br>\n' )
    htmlFile.write( '</body></html>' )
    htmlFile.close()

    if options.qcdMake :
        print "\n\n Final QCD and Data Info:\n -- QCD Name: %s\n -- Data Yield = %f\n -- QCD Yield = %f" % (options.qcdMakeDM, finalDataYield, finalQCDYield)
        dumpFile = open('plotsOut.txt', 'a')
        dumpFile.write("\nFinal QCD and Data Info:\n -- QCD Name: %s\n -- Data Yield = %f\n -- QCD Yield = %f" % (options.qcdMakeDM, finalDataYield, finalQCDYield))
        dumpFile.close()

    #if qcdVarIntegral :
    #    print "\n\n     QCD yield: %f           QCD Make: %s\n\n" % (qcdVarIntegral ,options.qcdMakeDM)
