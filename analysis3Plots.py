from util.buildTChain import makeTChain
import ROOT
import json
import pyplotter.plot_functions as pyplotter #import setTDRStyle, getCanvas
import pyplotter.tdrstyle as tdr
from util.ratioPlot import ratioPlot
import analysisPlots
from util.splitCanvas import fixFontSize
import os
from array import array
import math
from analysisPlots import skipSystShapeVar
from copy import deepcopy
from util.helpers import checkDir



def makeLotsOfPlots( analysis, samples, channels, folderDetails, **kwargs ) :

    ops = {
    'qcdMakeDM' : 'x',
    'useQCDMakeName' : 'x',
    'isSSQCD' : False,
    'addUncert' : True,
    'qcdMC' : False,
    'qcdSF' : 1.0,
    'ratio' : True,
    'blind' : True,
    'text' : False,
    'mssm' : False,
    'log' : False,
    'sync' : False,
    'targetDir' : ''}

    '''python analysis3Plots.py --folder=2June26_OSl1ml2_VTight_ZTT --channel=tt --text=True --useQCDMake=True --useQCDMakeName=OSl1ml2_VTight_LooseZTT --qcdSF=0.147 --btag=False'''

    for key in kwargs :
        #print "another keyword arg: %s: %s" % (key, kwargs[key])
        if key in ops.keys() :
             ops[key] = kwargs[key]
    print ops


    """ Add in the gen matched DY catagorization """
    if analysis == 'htt' :
        genList = ['ZTT', 'ZLL', 'ZL', 'ZJ']
        dyJets = ['DYJetsAMCNLO', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4']
        newSamples = {}
        for sample in samples.keys() :
            #print sample
            if sample in dyJets :
                for gen in genList :
                    #print gen, sample+'-'+gen
                    samples[ sample+'-'+gen ] = deepcopy(samples[ sample ])
                    genApp = gen.lower()
                    samples[ sample+'-'+gen ]['group'] = genApp

        # Clean the samples list
        for dyJet in dyJets :
            if dyJet in samples.keys() :
                del samples[ dyJet ]
        samples[ 'QCD' ] = {'xsec' : 0.0, 'group' : 'qcd' }
                
        # Don't plot sm higgs 120, 130
        smHiggs = ['ggHtoTauTau120', 'ggHtoTauTau130', 'VBFHtoTauTau120', 'VBFHtoTauTau130']
        for higgs in smHiggs :
            if higgs in samples : del samples[ higgs ]

    for sample in samples :
        print sample


    print "Running over %s samples" % analysis
    
    ROOT.gROOT.SetBatch(True)
    tdr.setTDRStyle()
    
    cmsLumi = float(os.getenv('LUMI'))/1000
    print "Lumi = %.1f / fb" % cmsLumi
    
    mssmMass = 250
    azhMass = 350
    mssmSF = 100
    higgsSF = 10
    azhSF = .025
    

    with open('meta/NtupleInputs_%s/samples.json' % analysis) as sampFile :
        sampDict = json.load( sampFile )
    
    chans = {
        'tt' : '#tau_{h}#tau_{h}',
        'em' : 'e#mu',
        'eeet' : 'eee#tau_{h}',
        'eemt' : 'ee#mu#tau_{h}',
        'eett' : 'ee#tau_{h}#tau_{h}',
        'eeem' : 'eee#mu',
        'eeee' : 'eeee',
        'eemm' : 'ee#mu#mu',
        'emmt' : '#mu#mue#tau_{h}',
        'mmmt' : '#mu#mu#mu#tau_{h}',
        'mmtt' : '#mu#mu#tau_{h}#tau_{h}',
        'emmm' : '#mu#mue#mu',
        'mmmm' : '#mu#mu#mu#mu',
        'ZEE' : 'Z#rightarrowee',
        'ZMM' : 'Z#rightarrow#mu#mu',
        'ZXX' : 'Z#rightarrowee/#mu#mu',
    }
    
    
    sampInfo = { 'htt' : {
        'dib' : [ROOT.kRed+2, 'VV'],
        'top' : [ROOT.kBlue-8, 't#bar{t}'],
        'qcd' : [ROOT.TColor.GetColor(250,202,255), 'QCD'], #kMagenta-10
        'ztt' : [ROOT.TColor.GetColor(248,206,104), 'Z#rightarrow#tau#tau'], #kOrange-4,
        'zl' : [ROOT.kAzure+2, 'Z#rightarrowee (lepton)'],
        'zj' : [ROOT.kGreen+2, 'Z#rightarrowee (jet)'],
        'zll' : [ROOT.TColor.GetColor(100,182,232), 'Z#rightarrowee'],
        'wjets' : [ROOT.kAzure+6, 'WJets'],
        'higgs' : [ROOT.kBlue, 'SM Higgs(125)'],
        #'mssm' : [ROOT.kPink, 'MSSM(%i) x %i' % (mssmMass, mssmSF)],
        'obs' : [ROOT.kBlack, 'Data'],
        }, # htt
            'azh' : {
        'obs' : [ROOT.kBlack, 'Data'],
        'zz' : [ROOT.kGreen-9, 'ZZ'],
        'wz' : [ROOT.kRed-4, 'WZ'],
        'dyj' : [ROOT.TColor.GetColor(248,206,104), 'ZJets'],
        'top' : [ROOT.kBlue-8, 't#bar{t}'],
        'sm' : [ROOT.kGreen, 'SM Higgs (125)'],
        'azh' : [ROOT.kBlue, 'A#rightarrowZh M%s #sigma=%.3fpb' % (azhMass, azhSF)],
        } # azh
    } # sampInfo
    if not ops['mssm'] : sampInfo['htt']['higgs'][1] = "SM Higgs(125) x %i" % higgsSF

    # Make signal variable for later easy mapping
    signal = ''
    if analysis == 'htt' : 
        signal = 'higgs'
        signalSF = higgsSF
    if analysis == 'azh' : 
        signal = 'azh'
        signalSF = azhSF
    
    
    for channel in channels :
        print channel
    
        # Make an index file for web viewing
        checkDir( '%sPlots/em' % analysis )
        checkDir( '%sPlots/tt' % analysis )
        checkDir( '%sPlotsList/em' % analysis )
        checkDir( '%sPlotsList/tt' % analysis )
        checkDir( '/afs/cern.ch/user/t/truggles/www/%sPlots/%s%s/' % (analysis, channel, ops['targetDir']))
        checkDir( '/afs/cern.ch/user/t/truggles/www/%sPlotsList/%s%s/' % (analysis, channel, ops['targetDir']))
        htmlFile = open('/afs/cern.ch/user/t/truggles/www/%sPlots/%s%s/index.html' % (analysis, channel, ops['targetDir']), 'w')
        htmlFile.write( '<html><head><STYLE type="text/css">img { border:0px; }</STYLE>\n' )
        htmlFile.write( '<title>Channel %s/</title></head>\n' % channel )
        htmlFile.write( '<body>\n' )
    

        newVarMap = analysisPlots.getHistoDict( analysis, channel )
    
        finalQCDYield = 0.0
        finalDataYield = 0.0
        qcdMake = False
        if ops['qcdMakeDM'] != 'x' :
            qcdMake = True
            finalQCDYield = 0.0
            finalDataYield = 0.0
            checkDir('meta/%sBackgrounds' % analysis)
            print "qcdMakeDM called: ",ops['qcdMakeDM']
            qcdMaker = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s_%s.root' % (analysis, channel, folderDetails.split('_')[0], ops['qcdMakeDM']), 'RECREATE')
            qcdDir = qcdMaker.mkdir('%s_Histos' % channel)
    
        #print newVarMap
        for var, info in newVarMap.iteritems() :
    
            # This is to speed up the Data Card making process by 2x and not
            # create all the plots for SS when all we need it the yield from eta_1
            if ops['isSSQCD'] and not (var == 'eta_1' or var == 'm_vis') : continue
            #if 'mt_sv' in var : continue
            print "Var:",var
    
    
            """
            Handle variable binning and longer ranges for visible mass
            """
            isVBFCat = False
            is1JetCat = False
            if 'm_sv' in var :
                if ('1jet_low' in ops['useQCDMakeName'] or '1jet_high' in ops['useQCDMakeName']\
                        or '1jet_low' in ops['qcdMakeDM'] or '1jet_high' in ops['qcdMakeDM']) :
                    is1JetCat = True
                if ('vbf' in ops['useQCDMakeName'] or 'vbf' in ops['qcdMakeDM']) :
                    isVBFCat = True


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
    
            elif var == 'mt_tot' :
                varBinned = True
                xBins = array( 'd', [0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,\
                        80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,\
                        170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,\
                        350.0,400.0,500.0,700.0,900.0, 1100.0,1300.0,1500.0,\
                        1700.0,1900.0,2100.0,2300.0,2500.0,2700.0,2900.0,3100.0,\
                        3300.0,3500.0,3700.0,3900.0] )
            elif var == 'm_vis_mssm' :
                varBinned = True
                #xBins = array( 'd', [0,20,40,60,80,100,150,200,250,350,600,1000,1500,2000,2500,3500] )
                xBins = array( 'd', [] )
                for i in range(0, 351 ) :
                    xBins.append( i * 10 )
            elif ops['sync'] and 'm_vis' in var :
                varBinned = True
                xBins = array( 'd', [] )
                for i in range( 21 ) :
                    xBins.append( i * 17.5 )
            elif 'm_sv' in var :
                if is1JetCat :
                    varBinned = True
                    xBins = array( 'd', [0,60,70,80,90,100,110,120,130,150,200,350] )
                #elif isVBFCat :
                else :
                    varBinned = True
                    xBins = array( 'd', [0,60,80,100,120,150,200,350] )
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
            sampHistos = {}
            for samp in sampInfo[analysis].keys() :
                # Skip some DY gen based combos
                if analysis == 'htt' and channel == 'em' :
                    if samp in ['zl', 'zj'] : continue
                if analysis == 'htt' and channel == 'tt' :
                    if samp == 'zll' : continue
                sampHistos[samp] = ROOT.TH1D("All Backgrounds %s %s" % (samp, append), samp, xNum, xBins )
                sampHistos[samp].Sumw2()
                sampHistos[samp].SetFillColor( sampInfo[analysis][samp][0] )
                sampHistos[samp].SetLineColor( ROOT.kBlack )
                sampHistos[samp].SetLineWidth( 2 )
                sampHistos[samp].SetTitle( sampInfo[analysis][samp][1] )
            sampHistos[ signal ].SetLineColor( ROOT.kPink )
            sampHistos[ signal ].SetLineWidth( 4 )
            sampHistos[ signal ].SetLineStyle( 7 )
            sampHistos[ signal ].SetMarkerStyle( 0 )
                
    
            for sample in samples.keys() :
                #print sample
                #print samples[sample]
    
                ''' Shape systematics are plotted with their 
                    unshifted counterparts '''
                getVar = var
                if skipSystShapeVar( var, sample, channel ) :
                    breakUp = var.split('_')
                    breakUp.pop()
                    getVar = '_'.join(breakUp)
    
                # Remember data samples are called 'dataEE' and 'dataMM'
                if channel in ['eeet', 'eemt', 'eett', 'eeem', 'eeee', 'eemm'] and sample == 'dataMM' : continue
                if channel in ['emmt', 'mmmt', 'mmtt', 'emmm', 'mmmm'] and sample == 'dataEE' : continue
                if channel in ['ZEE',] and sample == 'dataMM' : continue
                if channel in ['ZMM',] and sample == 'dataEE' : continue
            
                if channel == 'tt' and sample == 'dataEM' : continue
                if channel == 'tt' and '-ZLL' in sample : continue
                if channel == 'em' and sample == 'dataTT' : continue
                if channel == 'em' and '-ZJ' in sample : continue
                if channel == 'em' and '-ZL' in sample and not '-ZLL' in sample : continue
                if ops['qcdMC'] and sample == 'QCD' : continue
                if not ops['qcdMC'] and 'QCD' in sample and '-' in sample : continue
    
                #if var == 'm_vis' : print sample
                #print '%s2IsoOrderAndDups/%s_%s.root' % (analysis, sample, channel)
    
                if 'QCD' in sample :
                    print "qcd in sample",sample
                    if ops['useQCDMakeName'] != 'x'  :
                        fName = 'meta/%sBackgrounds/%s_qcdShape_%s_%s.root' % (analysis, channel, folderDetails.split('_')[0], ops['useQCDMakeName'])
                        print fName 
                        tFile = ROOT.TFile(fName, 'READ')
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
                #print tFile
    
    
                dic = tFile.Get("%s_Histos" % channel )

                # Require var to be in file or print note and skip
                keys = dic.GetListOfKeys()
                inVars = []
                for key in keys :
                    inVars.append( key.GetName() )
                if getVar not in inVars :
                    print "\n\n"+getVar+" not in your root files!  Skipping...\n\n"
                    continue

                preHist = dic.Get( getVar )
                preHist.SetDirectory( 0 )
    
                if sample == 'QCD' and ops['useQCDMakeName'] != 'x' :
                    print "Using QCD SCALE FACTOR <<<< NEW >>>>"
                    preHist.Scale( ops['qcdSF'] )
                    #print "QCD yield: %f" % preHist.Integral()
                    hist = ROOT.TH1D( preHist )
                else :
                    hist = preHist.Rebin( xNum, "rebinned", xBins )
    
    
                if var == 'm_vis' :
                    if 'data' in sample and qcdMake : finalDataYield = hist.Integral()
                if var == 'eta_1' and finalDataYield == 0. :
                    if 'data' in sample and qcdMake : finalDataYield = hist.Integral()
    
                ''' Good Debugging stuff '''
                #nBins = hist.GetNbinsX()
                #print "sample %s    # bins, %i   range %i %i" % (sample, nBins, hist.GetBinLowEdge( 0 ), hist.GetBinLowEdge( nBins+1 ))
    
    
                #if samples[ sample ]['group'] == 'qcd' :
                #    print "qcd Stack yield: %f" % hist.Integral()
                sampHistos[ samples[ sample ]['group'] ].Add( hist )
                tFile.Close()
    

            for samp in sampHistos.keys() :
                if var == 'm_vis' :
                    print "%s --- yield %f" % ( samp, sampHistos[samp].Integral() )
                # With Variable binning, need to set bin content appropriately
                if not varBinned : continue
                if samp == "qcd" : continue
                for bin_ in range( 1, 11 ) :
                    sampHistos[samp].SetBinContent( bin_, sampHistos[samp].GetBinContent( bin_ ) * ( sampHistos[samp].GetBinWidth(1) / sampHistos[samp].GetBinWidth( bin_ ) ) )
    
    
            # Some specific HTT stuff
            if analysis == 'htt' :
                if not qcdMake :
                    #print "Adding QCD: ",sampHistos['qcd'].Integral()
                    stack.Add( sampHistos['qcd'] )
                stack.Add( sampHistos['top'] )
                stack.Add( sampHistos['dib'] )
                stack.Add( sampHistos['wjets'] )
                if channel != 'em' :
                    stack.Add( sampHistos['zl'] )
                    stack.Add( sampHistos['zj'] )
                if channel == 'em' :
                    stack.Add( sampHistos['zll'] )
                stack.Add( sampHistos['ztt'] )

            # A to Zh stuff
            if analysis == 'azh' :
                stack.Add( sampHistos['top'] )
                stack.Add( sampHistos['dyj'] )
                stack.Add( sampHistos['wz'] )
                stack.Add( sampHistos['zz'] )
    
            # Scale signal samples for viewing
            sampHistos[ signal ].Scale( signalSF )
    
            ''' Print out yields for a given distribution '''
            if var == "Higgs_Pt" or var == "pt_1" or var == "pt_2" :
                print "\n\n Stack yields"
                totBkgVar = 0.
                totSig = 0.
                top = stack.GetStack().Last().GetNbinsX()+1
                for bin in range( 1, top ) :
                    totBkgVar += stack.GetStack().Last().GetBinContent( top-bin )
                    totSig += sampHistos[signal].GetBinContent( top-bin )
                    if totBkgVar > 0. :
                        sensitivity = totSig / math.sqrt( totBkgVar )
                    else : sensitivity = 0.
                    edge = stack.GetStack().Last().GetBinLowEdge( top-bin )
                    print "Bin: %i     sensitivity: %.2f     signal %.2f    bkg: %.2f" % (edge, sensitivity, totSig, totBkgVar)
    
            """
            Calculate rough bin-by-bin uncertainties
            """
            uncertNormMap = { 'htt' : {
            'qcd' : .20,
            'top' : .15,
            'dib' : .10,
            'wjets' : .10,
            'ztt' : .05,
            'zl' : .30,
            'zj' : .30,
            'higgs' : .0,
            'obs' : .0,},
            'azh' : {
            'top' : .15,
            'dyj' : .10,
            'wz' : .15,
            'zz' : .25,
            'azh' : .0,
            'obs' : .0,}
            }
            binErrors = []
            for k in range( stack.GetStack().Last().GetNbinsX()+1 ) :
                toRoot = 0.
                for samp in sampHistos.keys() :
                    toRoot += (sampHistos[samp].GetBinContent(k)*\
                        uncertNormMap[analysis][samp])**2
                    toRoot += sampHistos[samp].GetBinError(k)**2

                binErrors.append( math.sqrt(toRoot) )
    
    
            if qcdMake :
                qcdVar = ROOT.TH1D( var, 'qcd%s%s' % (append,var), xNum, xBins )
                qcdVar.Sumw2()
                qcdVar.Add( sampHistos['obs'] )
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
                sampHistos[signal].Draw('same')
                sampHistos['obs'].Draw('esamex0')
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
                ratioHist = ROOT.TH1D('ratio %s' % append, 'ratio', xNum, xBins )
                ratioHist.Sumw2()
                ratioHist.Add( sampHistos['obs'] )
                ratioHist.Divide( stack.GetStack().Last() )
                ratioHist.SetMaximum( 2. )
                ratioHist.SetMinimum( 0. )
                if channel == 'tt' :
                    ratioHist.SetMaximum( 1.5 )
                    ratioHist.SetMinimum( 0.5 )
                ratioHist.SetMarkerStyle( 21 )
                ratioPad.cd()
                ratioHist.Draw('ex0')

                """ Add uncertainty bands on ratio """
                er = ROOT.TH1D("er %s" % append, "er", xNum, xBins )
                er.Sumw2()
                er.GetXaxis().SetRangeUser( info[1], info[2] )
                for k in range( er.GetNbinsX()+1 ) :
                    er.SetBinContent( k, 1. )
                    if stack.GetStack().Last().GetBinContent(k) > 0. : 
                        er.SetBinError(k, binErrors[k]/stack.GetStack().Last().GetBinContent(k) )
                    #print "Qcd Error:",qcd.GetBinError(k)
                er.SetLineColor( 0 )
                er.SetLineWidth( 0 )
                er.SetMarkerSize( 0 )
                er.SetFillStyle( 3002 )
                er.SetFillColor( 15 )
                er.Draw('same e2')
                ratioHist.Draw('esamex0')

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
                sampHistos[signal].Draw('same')
                sampHistos['obs'].Draw('esamex0')
    
    
            # Set labels appropriately
            if info[ 5 ] == '' :
                stack.GetYaxis().SetTitle("Events")
            else :
                stack.GetYaxis().SetTitle("Events / %s%s" % (str(round(stack.GetStack().Last().GetBinWidth(1),1)), info[ 5 ])  )
    

            # Set axis and viewing area
            stackMax = stack.GetStack().Last().GetMaximum()
            dataMax = sampHistos['obs'].GetMaximum()
            stack.SetMaximum( max(dataMax, stackMax) * 1.5 )
            if ops['log'] :
                pad1.SetLogy()
                stack.SetMaximum( max(dataMax, stackMax) * 10 )
                stack.SetMinimum( min(dataMax, stackMax) * .005 )
    

            ''' Build the legend explicitly so we can specify marker styles '''
            legend = ROOT.TLegend(0.60, 0.65, 0.95, 0.93)
            legend.SetMargin(0.3)
            legend.SetBorderSize(0)
            legend.AddEntry( sampHistos['obs'], "Data", 'lep')
            legend.AddEntry( sampHistos[signal], sampHistos[signal].GetTitle(), 'l')
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
    
            lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
            lumi.SetTextSize(0.03)
            lumi.DrawTextNDC(.7,.96,"%.1f / fb (13 TeV)" % cmsLumi )
    

            ''' Random print outs on plots '''
            if ops['text'] and not varBinned :
                text1 = ROOT.TText(.4,.6,"Data Integral: %f" % sampHistos['obs'].GetMean() )
                text1.SetTextSize(0.04)
                text1.DrawTextNDC(.6,.6,"Data Integral: %s" % str( round( sampHistos['obs'].Integral(), 1) ) )
                text2 = ROOT.TText(.4,.55,"Data Int: %s" % str( sampHistos['obs'].Integral() ) )
                text2.SetTextSize(0.04)
                text2.DrawTextNDC(.6,.55,"MC Integral: %s" % str( round( stack.GetStack().Last().Integral(), 1) ) )
                text3 = ROOT.TText(.4,.55,"Data Mean: %s" % str( sampHistos['obs'].GetMean() ) )
                text3.SetTextSize(0.04)
                text3.DrawTextNDC(.6,.50,"Diff: %s" % str( round( sampHistos['obs'].Integral() - stack.GetStack().Last().Integral(), 1) ) )
    
    
            pad1.Update()
            stack.GetXaxis().SetRangeUser( info[1], info[2] )
            if ops['ratio'] :
                ratioHist.GetXaxis().SetRangeUser( info[1], info[2] )
    
    
            """
            Add uncertainty bands on background stack
            """
            if ops['addUncert'] :
                e1 = ROOT.TH1D("e1 %s" % append, "e1", xNum, xBins )
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
            if ops['blind'] :
                if (analysis == 'htt' and ('m_vis' in var or 'm_sv' in var or 'mt_sv' in var\
                         or 'mt_tot' in var or 'm_coll' in var) ) or\
                         (analysis=='azh' and ('H_vis' in var or 'Mass' in var) ) :
                    if ops['mssm'] :
                        targetMass = 170
                        targetMassUp = 9999
                    else :
                        targetMassLow = 60
                        targetMassUp = 160
                    nBins = stack.GetStack().Last().GetXaxis().GetNbins()
                    for k in range( nBins+1 ) :
                        if sampHistos['obs'].GetXaxis().GetBinLowEdge(k+1)>targetMassLow and \
                        sampHistos['obs'].GetXaxis().GetBinLowEdge(k+1)<targetMassUp :
                            sampHistos['obs'].SetBinContent(k, 0.)
                            sampHistos['obs'].SetBinError(k, 0.)
                            if ops['ratio'] :
                                ratioHist.SetBinContent(k, 0.)
                                ratioHist.SetBinError(k, 0.)
                    if ops['ratio'] : 
                        ratioPad.cd()
                        ratioHist.Draw('esamex0')
                    pad1.cd()
            sampHistos['obs'].Draw('esamex0')
                
    
    
            c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlots/%s%s/%s.png' % (analysis, channel, ops['targetDir'], var ) )
            c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlotsList/%s%s/%s.png' % (analysis, channel, ops['targetDir'], var ) )
    
    
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
    
    return finalQCDYield



