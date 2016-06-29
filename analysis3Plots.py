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
from copy import deepcopy



def makeLotsOfPlots( analysis, samples, channels, folderDetails, **kwargs ) :

    ops = {
    'qcdMakeDM' : 'x',
    'useQCDMakeName' : 'x',
    'addUncert' : True,
    'qcdMC' : False,
    'qcdSF' : 1.0,
    'ratio' : True,
    'blind' : False,
    'text' : False,
    'mssm' : False,
    'log' : False,}

    '''python analysis3Plots.py --folder=2June26_OSl1ml2_VTight_ZTT --channel=tt --text=True --useQCDMake=True --useQCDMakeName=OSl1ml2_VTight_LooseZTT --qcdSF=0.147 --btag=False'''

    for key in kwargs :
        #print "another keyword arg: %s: %s" % (key, kwargs[key])
        if key in ops.keys() :
             ops[key] = kwargs[key]

    print ops


    """ Add in the gen matched DY catagorization """
    genList = ['ZTT', 'ZLL', 'ZL', 'ZJ']
    dyJets = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4']
    newSamples = {}
    for sample in samples.keys() :
        #print sample
        if sample in dyJets :
            for gen in genList :
                #print gen, sample+'-'+gen
                samples[ sample+'-'+gen ] = deepcopy(samples[ sample ])
                genApp = gen.lower()
                samples[ sample+'-'+gen ]['group'] = genApp
                #print newSamples[ sample+'-'+gen ]
    #print newSamples

    # Clean the samples list
    for dyJet in dyJets :
        if dyJet in samples.keys() :
            del samples[ dyJet ]
    samples[ 'QCD' ] = {'xsec' : 0.0, 'group' : 'qcd' }
                



    print "Running over %s samples" % analysis
    
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
    
    with open('meta/NtupleInputs_%s/samples.json' % analysis) as sampFile :
        sampDict = json.load( sampFile )
    
    chans = {
        'tt' : '#tau_{h}#tau_{h}',
        'em' : 'e#mu',
    }
    
    
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
    
    
    for channel in channels :
    
        #if channel == 'tt' : continue
        #if channel == 'em' : continue
        if channel == 'tt' : mssmSF = int(mssmSF / 10)
    
        # Make an index file for web viewing
        if not os.path.exists( '%sPlots' % analysis ) :
            os.makedirs( '%sPlots/em' % analysis )
            os.makedirs( '%sPlots/tt' % analysis )
        if not os.path.exists( '%sPlotsList' % analysis ) :
            os.makedirs( '%sPlotsList/em' % analysis )
            os.makedirs( '%sPlotsList/tt' % analysis )
        htmlFile = open('/afs/cern.ch/user/t/truggles/www/%sPlots/%s/index.html' % (analysis, channel), 'w')
        htmlFile.write( '<html><head><STYLE type="text/css">img { border:0px; }</STYLE>\n' )
        htmlFile.write( '<title>Channel %s/</title></head>\n' % channel )
        htmlFile.write( '<body>\n' )
    
    
        print channel
    
        newVarMap = analysisPlots.getHistoDict( channel )
    
        finalQCDYield = 0.0
        finalDataYield = 0.0
        qcdMake = False
        if ops['qcdMakeDM'] != 'x' :
            qcdMake = True
            finalQCDYield = 0.0
            finalDataYield = 0.0
            if not os.path.exists('meta/%sBackgrounds' % analysis) :
                os.makedirs('meta/%sBackgrounds' % analysis)
            print "qcdMakeDM called: ",ops['qcdMakeDM']
            qcdMaker = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s.root' % (analysis, channel, ops['qcdMakeDM']), 'RECREATE')
            qcdDir = qcdMaker.mkdir('%s_Histos' % channel)
    
        #print newVarMap
        for var, info in newVarMap.iteritems() :
    
            #if 'mt_sv' in var : continue
            #if not (var == 'pZeta-0.85pZetaVis' or var == 'm_vis') : continue
            #if not 'm_vis_mssm' in var : continue
            #if not (var == 't1DecayMode' or var == 't2DecayMode') : continue
            print "Var:",var
    
    
            """
            Handle variable binning and longer ranges for visible mass
            """
            if '_mssm' in var :
                varBinned = True
                if 'ZTT' in folderDetails :
                    print "Inclusive"
                    xBins = array( 'd', [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900] )
                elif 'NoBTL' in folderDetails :
                    print "No-BTAGGING"
                    xBins = array( 'd', [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900] )
                elif 'NoBTL' not in folderDetails :
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
                first = info[1] * 1.
                last = info[2] * 1.
                totBins = ( info[0] / info[3] ) * 1.
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
            for sample in samples.keys() :
                print sample
                #print samples[sample]
    
                ''' Skip plotting unused shape systematics '''
                if skipSystShapeVar( var, sample, channel ) : continue
    
                if channel == 'tt' and sample == 'data_em' : continue
                if channel == 'tt' and '-ZLL' in sample : continue
                if channel == 'em' and sample == 'data_tt' : continue
                if channel == 'em' and '-ZJ' in sample : continue
                if channel == 'em' and '-ZL' in sample and not '-ZLL' in sample : continue
                if ops['qcdMC'] and sample == 'QCD' : continue
                if not ops['qcdMC'] and 'QCD' in sample and '-' in sample : continue
    
                #if var == 'm_vis' : print sample
                #print '%s2IsoOrderAndDups/%s_%s.root' % (analysis, sample, channel)
    
                if sample == 'data_em' :
                    tFile = ROOT.TFile('%s%s/%s.root' % (analysis, folderDetails, sample), 'READ')
                elif sample == 'data_tt' :
                    tFile = ROOT.TFile('%s%s/%s.root' % (analysis, folderDetails, sample), 'READ')
                elif 'QCD' in sample :
                    print "qcd in sample"
                    if ops['useQCDMakeName'] != 'x'  :
                        fName = 'meta/%sBackgrounds/%s_qcdShape_%s.root' % (analysis, channel, ops['useQCDMakeName'])
                        print fName 
                        tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s.root' % (analysis, channel, ops['useQCDMakeName']), 'READ')
                        print 1
                    elif ops['qcdMC'] :
                        print "Got QCD MC file", sample
                        tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                        print "QCD MC: %s Integral %f" % (sample, hxx.Integral() )
                    elif not ops['qcdMakeDM'] :
                        tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                    else :
                        continue
                else :
                    #print "File: '%s%s/%s_%s.root'" % (analysis, folderDetails, sample, channel)
                    tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
    
    
                #if 'QCD' not in sample :
                dic = tFile.Get("%s_Histos" % channel )
                preHist = dic.Get( var )
                #if 'm_vis' in var :
                #    if 'QCD' in sample and ops['useQCDMake'] :
                #        preHist = dic.Get( var )
                #    elif 'data' in sample :
                #        preHist = dic.Get( 'm_vis' )
                #    else :
                #        preHist = dic.Get( var )
    
                #else : preHist = dic.Get( var )
                preHist.SetDirectory( 0 )
    
                #if sample == 'QCD' and ops['useQCDMakeName'] != 'x' :
                #    if channel == 'em' :
                #        print "Skip rebin; Scale QCD shape by %f" % qcdEMScaleFactor
                #        preHist.Scale( qcdEMScaleFactor )
                #        print "QCD yield: %f" % preHist.Integral()
                #        hist = ROOT.TH1F( preHist )
                #    if channel == 'tt' :
                #        print "Skip rebin; Scale QCD shape by %f" % qcdTTScaleFactor
                #        preHist.Scale( qcdTTScaleFactor )
                #        print "QCD yield: %f" % preHist.Integral()
                #        hist = ROOT.TH1F( preHist )
                # If we use this option we specify a scaling factor
                #elif sample == 'QCD' and ops['useQCDMakeName'] != 'x' :
                if sample == 'QCD' and ops['useQCDMakeName'] != 'x' :
                    print "Using QCD SCALE FACTOR <<<< NEW >>>>"
                    #if channel == 'em' :
                    #    print "Skip rebin; Scale QCD shape by %f" % qcdEMScaleFactor
                    #    preHist.Scale( qcdEMScaleFactor )
                    #
                    #if channel == 'tt' :
                    #    print "Skip rebin; Scale QCD shape by %f" % qcdTTScaleFactor
                    #    preHist.Scale( qcdTTScaleFactor )
                    preHist.Scale( ops['qcdSF'] )
                    #print "Skip rebin; Scale QCD shape by %f" % qcdTTScaleFactorNew
                    #preHist.Scale( qcdTTScaleFactorNew )
                    print "QCD yield: %f" % preHist.Integral()
                    hist = ROOT.TH1F( preHist )
                else :
                    #preHist.Rebin( info[3] )
                    #print "Rebinning"
                    #print xNum
                    #print xBins
                    hist = preHist.Rebin( xNum, "rebinned", xBins )
                    #print "Done Rebinning"
    
    
    
                ''' Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ),
                QCD gets special scaling from bkg estimation, see qcdYield[channel] above for details '''
                #print "PRE Sample: %s      Int: %f" % (sample, hist.Integral() )
                #if sample == 'QCD' and hist.Integral() != 0 :
                #    if not useQCDMake or QCDYield :
                #        if channel == 'em' : hist.Scale( qcdYieldEM / hist.Integral() )
                #        if channel == 'tt' : hist.Scale( qcdYieldTT / hist.Integral() )
                #        print "Using QCD Yield numbers from this file, QCD Int: %f" % hist.Integral()
                #elif 'data' not in sample and hist.Integral() != 0:
                #    if 'TT' in sample :
                #        hist.Scale( bkgsTTScaleFactor )
                #    elif 'QCD' in sample :
                #        if channel == 'em' : hist.Scale( qcdEMScaleFactor )
    
    
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
                    if 'data' in sample and qcdMake : finalDataYield = hist.Integral()
                if var == 'eta_1' and finalDataYield == 0. :
                    if 'data' in sample and qcdMake : finalDataYield = hist.Integral()
    
                ''' Good Debugging stuff '''
                #nBins = hist.GetNbinsX()
                #print "sample %s    # bins, %i   range %i %i" % (sample, nBins, hist.GetBinLowEdge( 0 ), hist.GetBinLowEdge( nBins+1 ))
    
    
                #print "%s    ---    %f" % (sample, hist.Integral() )
                #if 'data' in sample :
                #    for b in range( 0, hist.GetNbinsX() ) :
                #        print "bin %f   qty %f" % (hist.GetXaxis().GetBinCenter(b), hist.GetBinContent(b))
                if samples[ sample ]['group'] == 'ztt' :
                    ztt.Add( hist )
                if samples[ sample ]['group'] == 'zl' :
                    zl.Add( hist )
                if samples[ sample ]['group'] == 'zj' :
                    zj.Add( hist )
                if samples[ sample ]['group'] == 'zll' :
                    zll.Add( hist )
                if samples[ sample ]['group'] == 'qcd' :
                    qcd.Add( hist )
                    #print "qcd Stack yield: %f" % qcd.GetStack().Last().Integral()
                    print "qcd Stack yield: %f" % qcd.Integral()
                if samples[ sample ]['group'] == 'top' :
                    top.Add( hist )
                if samples[ sample ]['group'] == 'dib' :
                    dib.Add( hist )
                if samples[ sample ]['group'] == 'wjets' :
                    wjets.Add( hist )
                if samples[ sample ]['group'] == 'mssm' :
                    mssm.Add( hist )
                if samples[ sample ]['group'] == 'higgs' :
                    higgs.Add( hist )
                if samples[ sample ]['group'] == 'obs' :
                    data.Add( hist )
                tFile.Close()
    
            Ary = { qcd : "qcd", top : "top", dib : "dib", wjets : "wjets", ztt : "ztt", zl :  "zl", zj : "zj", zll : "zll" }
            for h in Ary.keys() :
                h.SetFillColor( sampColors[ Ary[h] ] )
                h.SetLineColor( ROOT.kBlack )
                h.SetLineWidth( 2 )
                print "%s --- yield %f" % ( Ary[h], h.Integral() )
            data.SetLineColor( ROOT.kBlack )
            data.SetLineWidth( 2 )
            data.SetMarkerStyle( 21 )
            Ary[ data ] = "data"
            if not ops['mssm'] :
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
            if ops['mssm'] : Names["higgs"] = "SM Higgs(125)"
            else : Names["higgs"] = "SM Higgs(125) x %i" % higgsSF
            for h in Ary.keys() :
                h.SetTitle( Names[ Ary[h] ] )
                
    
            #if ops['mssm'] :
            #    stack.Add( higgs )
            if not qcdMake :
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
            if not ops['mssm'] :
                higgs.Scale( higgsSF )
            mssm.Scale( mssmSF )
    
                
            if qcdMake :
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
                    print "M_VIS_MSSM plot details: %f %f" % (info[1], info[2])
                qcdVar.GetXaxis().SetRangeUser( info[1], info[2] )
                print "qcdVar: %f   mean %f" % (qcdVar.Integral(), qcdVar.GetMean() )
                if var == 'mt_sv_mssm' :
                    #print "QCD Binning"
                    #print xBins
                    finalQCDYield = qcdVar.Integral()
                if var == 'eta_1' and finalQCDYield == 0.0 :
                    finalQCDYield = qcdVar.Integral()
                qcdDir.cd()
                qcdVar.Write()
    
    
            # Maybe make ratio hist
            c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 550, 550)
    
            if not ops['ratio'] :
                pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
                pad1.Draw()
                pad1.cd()
                stack.Draw('hist')
                if ops['mssm'] :
                    mssm.Draw('same')
                else :
                    higgs.Draw('same')
                data.Draw('esamex0')
                # X Axis!
                stack.GetXaxis().SetTitle("%s" % info[ 4 ])
    
            if ops['ratio'] :
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
                line = ROOT.TLine( info[1], 1, info[2], 1 )
                line.SetLineColor(ROOT.kBlack)
                line.SetLineWidth( 1 )
                line.Draw()
                ratioHist.Draw('esamex0')
                # X Axis!
                ratioHist.GetXaxis().SetTitle("%s" % info[ 4 ])
                ratioHist.GetYaxis().SetTitle("Data / MC")
                ratioHist.GetYaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
                ratioHist.GetYaxis().SetTitleOffset( smlPadSize*1.5 )
                ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize()*( 1/smlPadSize) )
                ratioHist.GetYaxis().SetNdivisions( 5, True )
                ratioHist.GetXaxis().SetLabelSize( ratioHist.GetXaxis().GetLabelSize()*( 1/smlPadSize) )
                ratioHist.GetXaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( 1/smlPadSize) )
    
    
                pad1.cd()
                stack.Draw('hist')
                if ops['mssm'] :
                    mssm.Draw('same')
                #else :
                #    higgs.Draw('same')
                data.Draw('esamex0')
    
    
            # Set Y axis titles appropriately
            #binWidth = str( round( hist.GetBinWidth(1), 0) )
            if info[ 5 ] == '' :
                stack.GetYaxis().SetTitle("Events")
            else :
                stack.GetYaxis().SetTitle("Events / %s%s" % (str(round(stack.GetStack().Last().GetBinWidth(1),1)), info[ 5 ])  )
            #    if hist.GetBinWidth(1) < .5 :
            #        stack.GetYaxis().SetTitle("Events / %s%s" % ( binWidth, info[ 5 ] ) )
            #    else :
            #        stack.GetYaxis().SetTitle("Events / %i%s" % ( binWidth, info[ 5 ] ) )
    
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
            if ops['log'] :
                pad1.SetLogy()
                stack.SetMaximum( max(dataMax, stackMax) * 10 )
                stack.SetMinimum( min(dataMax, stackMax) * .05 )
    
            ''' Build the legend explicitly so we can specify marker styles '''
            legend = ROOT.TLegend(0.60, 0.65, 0.95, 0.93)
            legend.SetMargin(0.3)
            legend.SetBorderSize(0)
            legend.AddEntry( data, "Data", 'lep')
            #if not ops['mssm'] :
            #    legend.AddEntry( higgs, "SM Higgs(125) x %i" % higgsSF, 'l')
            if ops['mssm'] :
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
            lumi.DrawTextNDC(.7,.96,"4.0 / fb (13 TeV)" )
    
            ''' Random print outs on plots '''
            if ops['text'] and not varBinned :
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
            stack.GetXaxis().SetRangeUser( info[1], info[2] )
            if ops['ratio'] :
                ratioHist.GetXaxis().SetRangeUser( info[1], info[2] )
    
    
            """
            Add uncertainty bands on background stack
            """
            if ops['addUncert'] :
                e1 = ROOT.TH1F("e1 %s" % append, "e1", xNum, xBins )
                e1.Sumw2()
                e1.GetXaxis().SetRangeUser( info[1], info[2] )
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
            if ops['blind'] and ('m_vis' in var or 'm_sv' in var or 'mt_sv' in var or 'mt_tot' in var) :
                nBins = stack.GetStack().Last().GetXaxis().GetNbins()
                for k in range( nBins+1 ) :
                    if data.GetXaxis().GetBinLowEdge(k+1)>170 :
                        data.SetBinContent(k, 0.)
                        data.SetBinError(k, 0.)
                        if ops['ratio'] :
                            ratioHist.SetBinContent(k, 0.)
                            ratioHist.SetBinError(k, 0.)
                if ops['ratio'] : 
                    ratioPad.cd()
                    ratioHist.Draw('esamex0')
                pad1.cd()
            data.Draw('esamex0')
                
    
    
            c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlots/%s/%s.png' % (analysis, channel, var ) )
            c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlotsList/%s/%s.png' % (analysis, channel, var ) )
    
    
            """ Additional views for Visible Mass """
            #if 'm_vis' in var :
            #    pad1.SetLogy()
            #    stack.SetMaximum( stack.GetMaximum() * 10 )
            #    stack.SetMinimum( higgs.GetMaximum() * .1 )
            #    if var == 'm_vis_mssm' :
            #        pad1.SetLogx()
            #        if ratio : ratioPad.SetLogx()
            #    pad1.Update()
            #    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlots/%s/%s_LogY.png' % (analysis, channel, var ) )
            #    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlotsList/%s/%s_LogY.png' % (analysis, channel, var ) )
            #    htmlFile.write( '<img src="%s_LogY.png">\n' % var )
            c1.Close()
    
            htmlFile.write( '<img src="%s.png">\n' % var )
            #htmlFile.write( '<br>\n' )
        htmlFile.write( '</body></html>' )
        htmlFile.close()
    
        if qcdMake :
            print "\n\n Final QCD and Data Info:\n -- QCD Name: %s\n -- Data Yield = %f\n -- QCD Yield = %f" % (ops['qcdMakeDM'], finalDataYield, finalQCDYield)
            dumpFile = open('plotsOut.txt', 'a')
            dumpFile.write("\nFinal QCD and Data Info:\n -- QCD Name: %s\n -- Data Yield = %f\n -- QCD Yield = %f" % (ops['qcdMakeDM'], finalDataYield, finalQCDYield))
            dumpFile.close()
    
        #if qcdVarIntegral :
        #    print "\n\n     QCD yield: %f           QCD Make: %s\n\n" % (qcdVarIntegral ,ops['qcdMakeDM'])
    return finalQCDYield



