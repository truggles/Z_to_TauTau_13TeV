#!/usr/bin/env python

import ROOT
import os
from util.helpers import checkDir
import analysis1BaselineCuts
from meta.sampleNames import returnSampleDetails
from util.helpers import setUpDirs 
import pyplotter.tdrstyle as tdr
import subprocess
from array import array
from util.ratioPlot import ratioPlot



def scaleTTandWZ( obj, hist ) :
    if 'electron' in obj :
        hist.Scale( 1.-.17 )
    if 'muon' in obj :
        hist.Scale( 1.-.21 )



def plotDistributions( saveDir, saveName, dataHist, mcSamps, mcPromptHists, mcRedHists ) :
    c = ROOT.TCanvas("c","c", 550, 550)

    infoMap = {
        'obs' : [ROOT.kBlack, 'Data'],
        'ZZ4l' : [ROOT.kGreen-9, 'ZZ'],
        'ggZZ' : [ROOT.kGreen-9, 'ggZZ'],
        'ttZ' : [ROOT.kYellow-7, 'ttZ'],
        'WZ3l1nu' : [ROOT.kRed+1, 'WZ'],
        #'rare' : [ROOT.kOrange+7, 'Rare'],
        'DYJets' : [ROOT.TColor.GetColor(248,206,104), 'ZJets'],
        'DYJets4' : [ROOT.TColor.GetColor(248,206,104)+1, 'Z4Jets'],
        'TT' : [ROOT.kBlue-8, 't#bar{t}'],
        #'redBkg' : [ROOT.kCyan, 'Reducible Bkg.'],
        #'higgs' : [ROOT.kRed-4, 'SM HZZ (125)'],
        #'VH' : [ROOT.kGreen, 'SM VHiggs(125)'],
        #'azh' : [ROOT.kBlue, 'A#rightarrowZh M%s #sigma=%.3fpb' % (azhMass, azhSF)],
    }

    mcStack = ROOT.THStack( 'mc', 'mc' )
    for sample in mcSamps :
        mcPromptHists[ sample ].SetFillColor( infoMap[sample][0] )
        mcPromptHists[ sample ].SetLineColor( ROOT.kBlack )
        mcPromptHists[ sample ].SetLineWidth( 1 )
        mcPromptHists[ sample ].SetTitle( infoMap[sample][1]+' Prompt' )
        mcRedHists[ sample ].SetFillColor( infoMap[sample][0]+2 )
        mcRedHists[ sample ].SetLineColor( ROOT.kBlack )
        mcRedHists[ sample ].SetLineWidth( 1 )
        mcRedHists[ sample ].SetTitle( infoMap[sample][1]+' Fake' )
        mcStack.Add( mcPromptHists[ sample ] )
        mcStack.Add( mcRedHists[ sample ] )

    smlPadSize = .25
    pads = ratioPlot( c, 1-smlPadSize )
    pad1 = pads[0]
    ratioPad = pads[1]
    ratioPad.SetTopMargin(0.02)
    ratioPad.SetBottomMargin(0.3)
    pad1.SetBottomMargin(0.00)
    ratioPad.SetGridy()
    ratioHist = dataHist.Clone()
    ratioHist.Sumw2()
    #ratioHist.Add( dataHist )
    ratioHist.Divide( mcStack.GetStack().Last() )
    ratioHist.SetMaximum( 1.5 )
    ratioHist.SetMinimum( 0.5 )
    ratioHist.SetMarkerStyle( 21 )
    ratioPad.cd()
    #DATA ratioHist.Draw('ex0')

    # X Axis!
    ratioHist.GetXaxis().SetTitle( dataHist.GetXaxis().GetTitle() )
    ratioHist.GetYaxis().SetTitle("Data / MC")
    ratioHist.GetYaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
    ratioHist.GetYaxis().SetTitleOffset( smlPadSize*1.5 )
    ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize()*( 1/smlPadSize) )
    ratioHist.GetYaxis().SetNdivisions( 5, True )
    ratioHist.GetXaxis().SetLabelSize( ratioHist.GetXaxis().GetLabelSize()*( 1/smlPadSize) )
    ratioHist.GetXaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( 1/smlPadSize) )

    pad1.cd()

    #DATA dataHist.Draw('ex0')
    dataHist.SetMinimum( 1 )
    #DATA mcStack.Draw('hist same')
    mcStack.Draw('hist') #DATA
    #dataHist.SetMaximum( max( dataHist.GetMaximum(), mcStack.GetStack().Last().GetMaximum() ) * 1.3 )
    dataHist.SetMaximum( max( dataHist.GetMaximum(), mcStack.GetStack().Last().GetMaximum() ) * 2. )

    legend = ROOT.TLegend(0.65, 0.5, 0.95, 0.93)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    #DATA legend.AddEntry( dataHist, "Data", 'lep')
    for j in range(0, mcStack.GetStack().GetLast() + 1) :
        last = mcStack.GetStack().GetLast()
        name_str = mcStack.GetStack()[last - j ].GetTitle()
        legend.AddEntry( mcStack.GetStack()[ last - j ], name_str, 'f')
    legend.Draw()
    
    logo = ROOT.TText(.2, .88,"CMS Preliminary")
    logo.SetTextSize(0.04)
    logo.DrawTextNDC(.2, .89,"CMS Preliminary")

    print "saveName:",saveName
    if 'electron_denom' in saveName : regionName = 'Electron Denominator'
    elif 'electron_pass' in saveName : regionName = 'Electron Passing'
    elif 'muon_denom' in saveName : regionName = 'Muon Denominator'
    elif 'muon_pass' in saveName : regionName = 'Muon Passing'
    elif 'tau_denom' in saveName : regionName = 'Tau Denominator'
    elif 'tau_pass' in saveName : regionName = 'Tau Passing'
    elif 'tau-DM0_lltt_denom' in saveName : regionName = 'Tau DM0 LLTT Denominator'
    elif 'tau-DM0_lltt_pass' in saveName : regionName = 'Tau DM0 LLTT Passing'
    elif 'tau-DM1_lltt_denom' in saveName : regionName = 'Tau DM1 LLTT Denominator'
    elif 'tau-DM1_lltt_pass' in saveName : regionName = 'Tau DM1 LLTT Passing'
    elif 'tau-DM10_lltt_denom' in saveName : regionName = 'Tau DM10 LLTT Denominator'
    elif 'tau-DM10_lltt_pass' in saveName : regionName = 'Tau DM10 LLTT Passing'
    elif 'tau-DM0_lllt_denom' in saveName : regionName = 'Tau DM0 LLLT Denominator'
    elif 'tau-DM0_lllt_pass' in saveName : regionName = 'Tau DM0 LLLT Passing'
    elif 'tau-DM1_lllt_denom' in saveName : regionName = 'Tau DM1 LLLT Denominator'
    elif 'tau-DM1_lllt_pass' in saveName : regionName = 'Tau DM1 LLLT Passing'
    elif 'tau-DM10_lllt_denom' in saveName : regionName = 'Tau DM10 LLLT Denominator'
    elif 'tau-DM10_lllt_pass' in saveName : regionName = 'Tau DM10 LLLT Passing'
    elif 'tau-DM0_denom' in saveName : regionName = 'Tau DM0 Denominator'
    elif 'tau-DM0_pass' in saveName : regionName = 'Tau DM0 Passing'
    elif 'tau-DM1_denom' in saveName : regionName = 'Tau DM1 Denominator'
    elif 'tau-DM1_pass' in saveName : regionName = 'Tau DM1 Passing'
    elif 'tau-DM10_denom' in saveName : regionName = 'Tau DM10 Denominator'
    elif 'tau-DM10_pass' in saveName : regionName = 'Tau DM10 Passing'
    
    chan = ROOT.TLatex(.2, .80,"x")
    chan.SetTextSize(0.05)
    chan.DrawLatexNDC(.2, .84,"Region: %s" % regionName )
    
    cmsLumi = 35.9
    lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi.SetTextSize(0.035)
    lumi.DrawTextNDC(.7,.96,"%.1f / fb (13 TeV)" % cmsLumi )

    #DATA dataHist.Draw('esamex0')
    c.SaveAs( saveDir+'/'+saveName+'.png' )
    c.SaveAs( saveDir+'/'+saveName+'.pdf' )
    
    pad1.SetLogy()
    dataHist.SetMaximum( max( dataHist.GetMaximum(), mcStack.GetStack().Last().GetMaximum() ) * 150 )
    c.SaveAs( saveDir+'/'+saveName+'_log.png' )
    c.SaveAs( saveDir+'/'+saveName+'_log.pdf' )


def buildRedBkgFakeFunctions( inSamples, **params ) :
    analysis = 'azh'
    params['doRedBkg'] = True
    params['mid1'] = params['mid1']+'RedBkg'
    params['mid2'] = params['mid2']+'RedBkg'
    params['mid3'] = params['mid3']+'RedBkg'
    dir2 = 'azh'+params['mid2']

    setUpDirs( inSamples, params, analysis ) # Print config file and set up dirs
    inSamples = returnSampleDetails( analysis, inSamples )

    # Only do Red Bkg method on data
    samples = {}
    for samp, val in inSamples.iteritems() :
        #if 'data' in samp : samples[samp] = val
        samples[samp] = val
    #print samples

#    # Apply initial Reducible Bkg Cuts for inclusive selection
#    analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
#    # Order events and choose best interpretation
#    analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)
#
#    # HADD each channel together so we can avoid different data runs
#    # and pool all MC backgrounds together
#    for channel in params['channels'] :
#        print "HADD for",channel
#        subprocess.call(["bash","./util/haddRedBkg.sh",dir2,channel])

    # Next try without drawHistos
    # Red Bkg Obj : Channels providing stats
    redBkgMap = {
#        'tau' : ['eeet', 'eett', 'eemt', 'emmt', 'mmtt', 'mmmt'],
        'tau-DM0' : ['eeet', 'eett', 'eemt', 'emmt', 'mmtt', 'mmmt'],
        'tau-DM1' : ['eeet', 'eett', 'eemt', 'emmt', 'mmtt', 'mmmt'],
        'tau-DM10' : ['eeet', 'eett', 'eemt', 'emmt', 'mmtt', 'mmmt'],
##        'tau-lltt' : ['eett', 'mmtt'],
        'tau-DM0_lltt' : ['eett', 'mmtt'],
        'tau-DM1_lltt' : ['eett', 'mmtt'],
        'tau-DM10_lltt' : ['eett', 'mmtt'],
#        'tau-lllt' : ['eeet', 'eemt', 'emmt', 'mmmt'],
        'tau-DM0_lllt' : ['eeet', 'eemt', 'emmt', 'mmmt'],
        'tau-DM1_lllt' : ['eeet', 'eemt', 'emmt', 'mmmt'],
        'tau-DM10_lllt' : ['eeet', 'eemt', 'emmt', 'mmmt'],
###        'electron' : ['eeet', 'emmt','eeem','emmm'],
        'electron' : ['eeet', 'emmt'],
        'muon' : ['eemt', 'mmmt'],
    }

    fakeRateMap = {}
    app = 'leptonPt'
    for obj, chans in redBkgMap.iteritems() :
        tmpMap = doRedBkgPlots( obj, chans, dir2 )
        for name, info in tmpMap.iteritems() :
            fakeRateMap[name+'_'+app] = info

    # Save fits to out file
    outFile = ROOT.TFile('data/azhFakeRateFits.root', 'RECREATE')
    for name, info in fakeRateMap.iteritems() :
        func = info[0]
        func.SetName( name+'_fit' )
        func.SetTitle( 'Fake Rate Fit: '+name )
        func.Write()
        graph = info[1]
        graph.SetName( name+'_graph' )
        graph.SetTitle( 'Fake Rate Fit: '+name )
        graph.Write()
    outFile.Close()


def doRedBkgPlots( obj, channels, inputDir ) :

    cmsLumi = float(os.getenv('LUMI'))/1000
    print "Lumi = %.1f / fb" % cmsLumi
    print "doing Red Bkg Plots for",obj
    print channels


    xAxis = 'Lepton p_{T} [GeV]'
    #xAxis = 'M_{T}( MET, Lepton) [GeV]'
    app = 'leptonPt'
    saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Jan16_mcSub_'+app
    checkDir( saveDir )

    #c1 = ROOT.TCanvas("c1","c1", 550, 550)
    #pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
    #pad1.Draw()
    #pad1.cd()


    yAxis2 = 'Fake Rate'
    binInfo = [20, 0, 200]
    yAxis1 = 'Events / %i GeV' % ( (binInfo[2] - binInfo[1]) / binInfo[0] )
    useVariableBinning = True
    if not useVariableBinning :
        denomAll = ROOT.TH1D( obj+'_denom', obj+'_denom;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
        passAll = ROOT.TH1D( obj+'_pass', obj+'_pass;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
        denomPlotAll = ROOT.TH1D( obj+'_denomPlot', obj+'_denomPlot;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
        passPlotAll = ROOT.TH1D( obj+'_passPlot', obj+'_passPlot;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
    else :
        if 'tau' in obj :
            xBins = array('d', [0,10,15,20,25,30,40,50,70,100])
        else :
            xBins = array('d', [0,10,15,20,30,40,100])
        print xBins
        binInfo = ['x', xBins[0], xBins[-1]]
        yAxis1 = 'Events'
        denomAll = ROOT.TH1D( obj+'_denom', obj+'_denom;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )
        passAll = ROOT.TH1D( obj+'_pass', obj+'_pass;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )
        denomPlotAll = ROOT.TH1D( obj+'_denomPlot', obj+'_denomPlot;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )
        passPlotAll = ROOT.TH1D( obj+'_passPlot', obj+'_passPlot;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )

    denomAll.Sumw2()
    passAll.Sumw2()
    denomPlotAll.Sumw2()
    passPlotAll.Sumw2()

    # Channel leg map
    prodMap = {
        'eeem' : ('e3', 'm'),
        'eeet' : ('e3', 't'),
        'eemt' : ('m', 't'),
        'eett' : ('t1', 't2'),
        'emmm' : ('e', 'm3'),
        'emmt' : ('e', 't'),
        'mmmt' : ('m3', 't'),
        'mmtt' : ('t1', 't2'),
        'eeee' : ('e3', 'e4'),
        'eemm' : ('m1', 'm2'),
        'mmmm' : ('m3', 'm4'),
    }

    cuts = {
        'tau' : {
            'denom' : ['byVVLooseIsolationMVArun2v1DBoldDMwLT_Num > 0.5',],
            'pass' : ['byMediumIsolationMVArun2v1DBoldDMwLT_Num > 0.5',],
        },
        'electron' : {
            'denom' : ['pfmt_3 < 40',], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 40 && pt_3 > 40',], # to suppress real leptons from WZ and ZZ
            'pass' : ['iso_Num < 0.15', 'id_e_mva_nt_tight_Num > 0.5'],
        },
        'muon' : {
            'denom' : ['pfmt_3 < 40',], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 40 && pt_3 > 40',], # to suppress real leptons from WZ and ZZ
            'pass' : ['iso_Num < 0.15', 'cand_PFIDLoose > 0.5'],
        },
    } 

    etaCuts = {
        'tau' : {
            #'Barrel' : 'abs( eta_Num ) <= 1.4',
            #'Endcap' : 'abs( eta_Num ) > 1.4',
            'AllEta' : '(1)',
        },
        'electron' : {
            #'Barrel' : 'abs( eta_Num ) <= 1.4',
            #'Endcap' : 'abs( eta_Num ) > 1.4',
            'AllEta' : '(1)',
        },
        'muon' :{
            #'Barrel' : 'abs( eta_Num ) <= 1.4',
            #'Endcap' : 'abs( eta_Num ) > 1.4',
            'AllEta' : '(1)',
        },
    }

    frMap = {}

    etaCode = 'tau' if 'tau' in obj else obj.split('-')[0]
    for etaRegion, etaCut in etaCuts[etaCode].iteritems() :
    # obj.split('-')[0] is to get the same cuts and mapping for
    # tau, tau-lltt, tau-lllt

        denomCut = ' && '.join( cuts[obj.split('-')[0]]['denom'] )
        denomCut += ' && '+etaCut
        denomCut += ' && bjetCISVVeto20MediumZTT == 0'

        # If using tau decay modes:
        if 'tau-DM10' in obj : denomCut += ' && decayMode_Num == 10'
        elif 'tau-DM0' in obj : denomCut += ' && decayMode_Num == 0'
        elif 'tau-DM1' in obj : denomCut += ' && decayMode_Num == 1'

        passCut = ' && '.join( cuts[obj.split('-')[0]]['pass'] )
        passCut = denomCut+' && '+passCut

        totalDenomAll = 0.
        totalPassingAll = 0.

        mcSamps = ['DYJets', 'DYJets4', 'TT', 'WZ3l1nu', 'ZZ4l', 'ggZZ', 'ttZ']
        mcDenomPromptTots = {}
        mcDenomRedTots = {}
        mcPassingPromptTots = {}
        mcPassingRedTots = {}
        for sample in mcSamps :
            mcDenomPromptTots[ sample ] = 0.0
            mcDenomRedTots[ sample ] = 0.0
            mcPassingPromptTots[ sample ] = 0.0
            mcPassingRedTots[ sample ] = 0.0


        # Total Data and MC distributions
        hDenomMCPrompt = {}
        hDenomMCRed = {}
        hPassingMCPrompt = {}
        hPassingMCRed = {}
        if not useVariableBinning :
            for sample in mcSamps :
                hDenomMCPrompt[ sample ] = ROOT.TH1D( sample+'_denomTot', sample+'_denomTot;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
                hDenomMCRed[ sample ] = ROOT.TH1D( sample+'_denomRedTot', sample+'_denomRedTot;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
                hPassingMCPrompt[ sample ] = ROOT.TH1D( sample+'_passTot', sample+'_passTot;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
                hPassingMCRed[ sample ] = ROOT.TH1D( sample+'_passRedTot', sample+'_passRedTot;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
        else :
            for sample in mcSamps :
                hDenomMCPrompt[ sample ] = ROOT.TH1D( sample+'_denomTot', sample+'_denomTot;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )
                hDenomMCRed[ sample ] = ROOT.TH1D( sample+'_denomRedTot', sample+'_denomRedTot;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )
                hPassingMCPrompt[ sample ] = ROOT.TH1D( sample+'_passTot', sample+'_passTot;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )
                hPassingMCRed[ sample ] = ROOT.TH1D( sample+'_passRedTot', sample+'_passRedTot;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )



        for channel in channels :
            print channel

            # Apply loosened LT_higgs cuts for LLTT channels and
            # make sure to apply it for LLMT
            # LLET and LLEM essentially have no LT_higgs cut
            passCut2 = passCut
            denomCut2 = denomCut
            if channel in ['eett', 'mmtt'] :
                passCut2 += ' && LT_higgs > 50'
                denomCut2 += ' && LT_higgs > 50'
            elif channel in ['eemt','mmmt'] :
                passCut2 += ' && LT_higgs > 40'
                denomCut2 += ' && LT_higgs > 40'

            f = ROOT.TFile( '/data/truggles/'+inputDir+'/dataRedBkg_'+channel+'.root', 'r' )
            t = f.Get('Ntuple')
            mcFiles = {}
            mcTrees = {}
            for sample in mcSamps :
                mcFiles[ sample ] = ROOT.TFile( '/data/truggles/'+inputDir+'/mc_'+sample+'_'+channel+'.root', 'r' )
                mcTrees[ sample ] = mcFiles[ sample ].Get('Ntuple')
                

            # check if first letter of 'obj' in leg3 then leg4 and draw if so
            for i, leg in enumerate(prodMap[channel]) :

                if not obj[0] in leg : continue

                # Replace vals in the passCut to match leg
                denomCutX = denomCut2.replace( '_Num', '_%i' % (i+3) ) # i begins at 0, we being with leg3
                denomCutX = denomCutX.replace( 'cand_', leg ) # For vars we didn't use in sync ntuple
                passCutX = passCut2.replace( '_Num', '_%i' % (i+3) ) # i begins at 0, we being with leg3
                passCutX = passCutX.replace( 'cand_', leg ) # For vars we didn't use in sync ntuple
                mcCutPrompt = 'gen_match_'+str(i+3)+' != 6)*(puweight*azhWeight*XSecLumiWeight*GenWeight/abs(GenWeight))' # prompt sub
                mcCutRed = 'gen_match_'+str(i+3)+' == 6)*(puweight*azhWeight*XSecLumiWeight*GenWeight/abs(GenWeight))' # prompt sub
                print "Denom Cut:",denomCutX
                print "Passing Cut:",passCutX
                print "MC Cut Prompt:",mcCutPrompt
                print "MC Cut Red:",mcCutRed

                # Denominator selection
                denomMCPrompt = {}
                denomMCRed = {}
                if not useVariableBinning :
                    hTmp = ROOT.TH1D( 'hTmp', 'hTmp', binInfo[0], binInfo[1], binInfo[2] )
                    for sample in mcSamps :
                        denomMCPrompt[ sample ] = ROOT.TH1D( sample, sample, binInfo[0], binInfo[1], binInfo[2] )
                        denomMCRed[ sample ] = ROOT.TH1D( sample+'_red', sample+'_red', binInfo[0], binInfo[1], binInfo[2] )
                else :
                    hTmp = ROOT.TH1D( 'hTmp', 'hTmp', len(xBins)-1, xBins )
                    for sample in mcSamps :
                        denomMCPrompt[ sample ] = ROOT.TH1D( sample, sample, len(xBins)-1, xBins )
                        denomMCRed[ sample ] = ROOT.TH1D( sample+'_red', sample+'_red', len(xBins)-1, xBins )

                t.Draw( 'pt_'+str(i+3)+' >> hTmp', denomCutX )
                for sample in mcSamps :
                    mcTrees[ sample ].Draw( 'pt_'+str(i+3)+' >> '+sample, '('+denomCutX+' && '+mcCutPrompt )
                    mcTrees[ sample ].Draw( 'pt_'+str(i+3)+' >> '+sample+'_red', '('+denomCutX+' && '+mcCutRed )
                        

                denomAll.Add( hTmp )
                denomPlotAll.Add( hTmp )
                #DATA print " -- denomAll Int:",denomAll.Integral()

                #DATA print "Denom Data: ",hTmp.Integral()
                for sample in mcSamps :
                    #print "Denom MC ",sample,": ",denomMCPrompt[ sample ].Integral()
                    if sample in ['TT','WZ3l1nu'] :
                        scaleTTandWZ( obj, denomMCPrompt[ sample ] )
                        scaleTTandWZ( obj, denomMCRed[ sample ] )
                    denomAll.Add( denomMCPrompt[ sample ] * -1. )
                    mcDenomPromptTots[ sample ] += denomMCPrompt[ sample ].Integral()
                    mcDenomRedTots[ sample ] += denomMCRed[ sample ].Integral()
                    hDenomMCPrompt[ sample ].Add( denomMCPrompt[ sample ] )
                    hDenomMCRed[ sample ].Add( denomMCRed[ sample ] )

                #print " -- denomAll Int MC sub:",denomAll.Integral()
                totalDenomAll += hTmp.Integral()

                # Passing selection
                passingMCPrompt = {}
                passingMCRed = {}
                if not useVariableBinning :
                    hTmpPass = ROOT.TH1D( 'hTmpPass', 'hTmpPass', binInfo[0], binInfo[1], binInfo[2] )
                    for sample in mcSamps :
                        passingMCPrompt[ sample ] = ROOT.TH1D( sample+'_pass', sample+'_pass', binInfo[0], binInfo[1], binInfo[2] )
                        passingMCRed[ sample ] = ROOT.TH1D( sample+'_passRed', sample+'_passRed', binInfo[0], binInfo[1], binInfo[2] )
                else :
                    hTmpPass = ROOT.TH1D( 'hTmpPass', 'hTmpPass', len(xBins)-1, xBins )
                    for sample in mcSamps :
                        passingMCPrompt[ sample ] = ROOT.TH1D( sample+'_pass', sample+'_pass', len(xBins)-1, xBins )
                        passingMCRed[ sample ] = ROOT.TH1D( sample+'_passRed', sample+'_passRed', len(xBins)-1, xBins )

                t.Draw( 'pt_'+str(i+3)+' >> hTmpPass', passCutX )
                for sample in mcSamps :
                    mcTrees[ sample ].Draw( 'pt_'+str(i+3)+' >> '+sample+'_pass', '('+passCutX+' && '+mcCutPrompt )
                    mcTrees[ sample ].Draw( 'pt_'+str(i+3)+' >> '+sample+'_passRed', '('+passCutX+' && '+mcCutRed )

                #DATA print "Passing Data: ",hTmpPass.Integral()
                passAll.Add( hTmpPass )
                passPlotAll.Add( hTmpPass )
                #DATA print " -- passAll Int:",passAll.Integral()
                for sample in mcSamps :
                    #print "Passing MC ",sample,": ",passingMCPrompt[ sample ].Integral()
                    if sample in ['TT','WZ3l1nu'] :
                        scaleTTandWZ( obj, passingMCPrompt[ sample ] )
                        scaleTTandWZ( obj, passingMCRed[ sample ] )
                    passAll.Add( passingMCPrompt[ sample ] * -1. )
                    mcPassingPromptTots[ sample ] += passingMCPrompt[ sample ].Integral()
                    mcPassingRedTots[ sample ] += passingMCRed[ sample ].Integral()
                    hPassingMCPrompt[ sample ].Add( passingMCPrompt[ sample ] )
                    hPassingMCRed[ sample ].Add( passingMCRed[ sample ] )

                #DATA print " -- passAll Int MC sub:",passAll.Integral()
                totalPassingAll += hTmpPass.Integral()
                del hTmp, hTmpPass, denomMCPrompt, passingMCPrompt, denomMCRed, passingMCRed


        # Print totals for each plot
        #print ' ---- '+obj+' '+etaRegion+'   denom: '+str(totalDenomAll)+'    passing: '+str(totalPassingAll)
        #DATA print ' ---- '+obj+' '+etaRegion+'   denom: %.2f passing: %.2f' % (totalDenomAll, totalPassingAll)
        promptMCTotalDenom = 0.0
        promptMCTotalPassing = 0.0
        redMCTotalDenom = 0.0
        redMCTotalPassing = 0.0
        for sample in mcSamps :
            print ' - -       %10s    denom: %.2f    passing: %.2f' % (sample, mcDenomPromptTots[ sample ], mcPassingPromptTots[ sample ])
            promptMCTotalDenom += mcDenomPromptTots[ sample ]
            promptMCTotalPassing += mcPassingPromptTots[ sample ]
        for sample in mcSamps :
            print ' - -       %10s    denom: %.2f    passing: %.2f' % (sample, mcDenomRedTots[ sample ], mcPassingRedTots[ sample ])
            redMCTotalDenom += mcDenomRedTots[ sample ]
            redMCTotalPassing += mcPassingRedTots[ sample ]

        print '\n - - '+obj+' '+etaRegion
        #DATA print ' - - Data Denom: %.2f        passing: %.2f' % (totalDenomAll, totalPassingAll)
        print ' - - MC Prompt Denom: %.2f    Prompt passing: %.2f' % (promptMCTotalDenom, promptMCTotalPassing)
        print ' - - MC Red Denom: %.2f    Red passing: %.2f' % (redMCTotalDenom, redMCTotalPassing)
        #DATA print ' - - Denom (Data - MC total) / Data = %.3f' % ((totalDenomAll - promptMCTotalDenom - redMCTotalDenom) / totalDenomAll)
        #DATA print ' - - Passing (Data - MC total) / Data = %.3f\n' % ((totalPassingAll - promptMCTotalPassing - redMCTotalPassing) / totalPassingAll)


        plotDistributions( saveDir, 'lepPtScaledMTLs40_'+obj+'_pass', passPlotAll, mcSamps, hPassingMCPrompt, hPassingMCRed )
        plotDistributions( saveDir, 'lepPtScaledMTLs40_'+obj+'_denom', denomPlotAll, mcSamps, hDenomMCPrompt, hDenomMCRed )
        #plotDistributions( saveDir, obj+'_pass', passAll, mcSamps, hPassingMCPrompt, hPassingMCRed )
        #plotDistributions( saveDir, obj+'_denom', denomAll, mcSamps, hDenomMCPrompt, hDenomMCRed )

        c1 = ROOT.TCanvas("c1","c1", 550, 550)
        pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
        pad1.Draw()
        pad1.cd()



        #denomAll.SetMaximum( denomAll.GetMaximum() * 1.3 )
        #denomAll.Draw()
        #setText( obj+" Denominator", cmsLumi )
        #c1.SaveAs( saveDir+'/'+obj+'_'+etaRegion+'_Denominator.png' )
        #passAll.SetMaximum( passAll.GetMaximum() * 1.3 )
        #passAll.Draw()
        #setText( obj+" Passing", cmsLumi )
        #c1.SaveAs( saveDir+'/'+obj+'_'+etaRegion+'_Pass.png' )

        # Make Fake Rate plot
        graph = ROOT.TGraphAsymmErrors(passAll, denomAll)
        graph.GetXaxis().SetTitle(xAxis)
        graph.GetYaxis().SetTitle(yAxis2)
        graph.GetYaxis().SetTitle("Fake Rate")
        graph.SetName( graph.GetName()+' '+app )
        pad1.SetGrid()

        # For Log
        doLinear = True
        #doLinear = False
        if not doLinear :
            pad1.SetLogy()
            graph.SetMaximum( 10 )
            if 'DM10' in obj :
                graph.SetMinimum( 0.00005 )
            elif 'DM1' in obj or 'DM0' in obj :
                graph.SetMinimum( 0.005 )
            else :
                graph.SetMinimum( 0.0005 )
        if doLinear :
            if obj == 'muon' :
                graph.SetMaximum( .05 )
            #else :
            #    graph.SetMaximum( .15 )
            elif obj == 'electron' :
                graph.SetMaximum( .05 )
            else :
                graph.SetMaximum( .5 )
            graph.SetMinimum( 0 )

        graph.Draw("AP")

        # do fit
        doFit = True
        useExp = True
        useExp = False
        # Set fit min for different objects
        if 'tau' in obj : fitMin = 20
        if obj == 'electron' : fitMin = 10
        if obj == 'muon' : fitMin = 10
        if doFit :
            #fitMin = binInfo[1] if binInfo[1] != 0 else 10


            #if useExp :
            #    f1 = ROOT.TF1( 'f1', '([0] + [1]*TMath::Exp(-[2]*x))', fitMin, binInfo[2]) # default one used on 2012 data
            #    f1.SetParName( 2, "decay" )
            #    if obj == 'electron' or obj == 'muon' :
            #        f1.SetParameter( 0, 0. )
            #        f1.SetParameter( 1, 1 )
            #        f1.SetParameter( 2, .05 )
            #    else : # is tau
            #        f1.SetParameter( 0, 0. )
            #        f1.SetParameter( 1, 1 )
            #        f1.SetParameter( 2, .05 )
            #else : # No Exponential
            #    f1 = ROOT.TF1( 'f1', '([0] + [1]*(TMath::Landau(x,[2],[3],0)) )', fitMin, binInfo[2])
            #    f1.SetParName( 2, "approx. max" )
            #    f1.SetParName( 3, "sigma param" )
            #    f1.SetParameter( 0, 0. )
            #    f1.SetParameter( 1, 1 )
            #    if obj == 'electron' :
            #        f1.SetParameter( 2, 25. )
            #        f1.SetParameter( 3, 2.5 )
            #    elif obj == 'muon' :
            #        f1.SetParameter( 2, 15. )
            #        f1.SetParameter( 3, 2.5 )
            #    else : # is tau
            #        f1.SetParameter( 2, 45. )
            #        f1.SetParameter( 3, 15. )
            #f1.SetParName( 0, "y rise" )
            #f1.SetParName( 1, "scale" )

            f1 = ROOT.TF1( 'f1', '([0] + [1]*x)', fitMin, binInfo[2])
            f1.SetParameter( 0, 0.1 )
            f1.SetParameter( 1, 0.0 )
            f1.SetParName( 0, "y rise" )
            f1.SetParName( 1, "slope" )

            graph.Fit('f1', 'SR' )
            #graph.Fit('f1', 'SRN' ) # N skips drawing

        if useExp :
            f2 = ROOT.TF1( 'f2 '+app, '([0] + [1]*TMath::Exp(-[2]*x))', fitMin, binInfo[2]) # default one used on 2012 data
        else :
            f2 = ROOT.TF1( 'f2 '+app, '([0] + [1]*(TMath::Landau(x,[2],[3],0)) )', fitMin, binInfo[2])
            f2 = ROOT.TF1( 'f2', '([0] + [1]*x)', fitMin, binInfo[2])
        if doFit :
            #f2.SetParameter( 3, f1.GetParameter( 3 ) )
            f2.SetParameter( 0, f1.GetParameter( 0 ) )
            f2.SetParameter( 1, f1.GetParameter( 1 ) )
            #f2.SetParameter( 2, f1.GetParameter( 2 ) )
            f2.Draw('SAME R')

        ROOT.gStyle.SetStatX(.95)
        ROOT.gStyle.SetStatY(0.8)
        ROOT.gStyle.SetStatH(.2)
        ROOT.gStyle.SetStatW(.2)
        setText( "Fake Rate: %s %s" % (obj, etaRegion), cmsLumi )
        c1.SaveAs( saveDir+'/'+obj+'_'+etaRegion+'_FakeRate.png' )
        #c1.SaveAs( saveDir+'/'+obj+'_'+etaRegion+'_FakeRate.pdf' )
        pad1.SetLogy(0)

        # Add FR fit to map
        frMap[obj+'_'+etaRegion] = [f2, graph]

        del mcDenomPromptTots, mcDenomRedTots, mcPassingPromptTots, mcPassingRedTots
        for sample in mcSamps :
            del hDenomMCPrompt[ sample ]
            del hDenomMCRed[ sample ]
            del hPassingMCPrompt[ sample ]
            del hPassingMCRed[ sample ]

    # Return map
    return frMap



def setText( text, cmsLumi ) :
    # Set CMS Styles Stuff
    logo = ROOT.TText(.2, .88,"CMS Preliminary")
    logo.SetTextSize(0.03)
    logo.DrawTextNDC(.2, .89,"CMS Preliminary")
    
    chan = ROOT.TLatex(.2, .80,"x")
    chan.SetTextSize(0.05)
    chan.DrawLatexNDC(.2, .84,"%s" % text )
    
    lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi.SetTextSize(0.03)
    lumi.DrawTextNDC(.7,.96,"%.1f / fb (13 TeV)" % cmsLumi )



if '__main__' in __name__ :
    
    ROOT.gROOT.SetBatch(True)
    tdr.setTDRStyle()
    
    dataSamples = ['ttZ', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'TT', 'WWW', 'WZ3l1nu', 'ZZ4l'] # removed tri-boson samples 
    for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
        dataSamples.append('dataEE-%s' % era)
        dataSamples.append('dataMM-%s' % era)

    params = {
        #'debug' : 'true',
        'debug' : 'false',
        'numCores' : 15,
        'numFilesPerCycle' : 1,
        'channels' : ['eeet','eett','eemt','emmt','mmtt','mmmt',], # no eeem or mmme
        #'channels' : ['eeem','emmm',],
        'cutMapper' : 'RedBkg',
        'mid1' : '1Jan09rb',
        'mid2' : '2Jan09rb',
        'mid3' : '3Jan09rb',
        #'cutMapper' : 'SignalRegion',
        #'mid1' : '1Jan13rbOS',
        #'mid2' : '2Jan13rbOS',
        #'mid3' : '3Jan13rbOS',
        'additionalCut' : '',
        'svFitPost' : 'false',
        'svFitPrep' : 'false',
        'doFRMthd' : 'false',
        #'skimmed' : 'false',
        'skimmed' : 'true',
        'skimHdfs' : 'false',
        #'skimHdfs' : 'true',
    }
    buildRedBkgFakeFunctions( dataSamples, **params )

