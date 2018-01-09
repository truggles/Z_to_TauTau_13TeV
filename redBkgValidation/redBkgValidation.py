#!/usr/bin/env python

import ROOT
from ROOT import gPad
from array import array
from collections import OrderedDict
from util.helpers import returnSortedDict, getProdMap
from util.azhReducibleBackgroundHelpers import \
    getRedBkgCutsAndWeights, getChannelSpecificFinalCuts, \
    getRedBkgShape
import pyplotter.tdrstyle as tdr
from util.ratioPlot import ratioPlot

def makeRatioPlot( h1, h2, c1, sample, var, channel, saveName, decorateDoFinal=False ) :
    c1.Clear()
    smlPadSize = .25
    pads = ratioPlot( c1, 1-smlPadSize )
    pad1 = pads[0]
    ratioPad = pads[1]
    ratioPad.SetTopMargin(0.0)
    ratioPad.SetBottomMargin(0.3)
    pad1.SetBottomMargin(0.02)
    ratioPad.SetGridy()
    ratioHist = h1.Clone()
    ratioHist.Divide( h2 )
    ratioHist.SetLineColor( ROOT.kBlack )
    ratioHist.SetMarkerColor( ROOT.kBlack )
    ratioHist.GetYaxis().SetTitle( 'Ratio RB / Nom' )
    ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize() / (1-smlPadSize) )
    ratioHist.SetMaximum( 4. )
    ratioHist.SetMinimum( 0. )
    ratioHist.SetMarkerStyle( 21 )
    ratioHist.SetMarkerSize( 0.5 )
    ratioLine = ratioHist.Clone()
    for b in range( 1, ratioHist.GetNbinsX()+1 ) :
        ratioLine.SetBinContent( b, 1.0 )
        ratioLine.SetBinError( b, 0.0 )

    pad1.cd()
    prepForPlot( var, h1, h2 )
    h1.Draw('E1')
    h1.GetXaxis().SetLabelSize( 0.0 )
    h1.GetYaxis().SetLabelSize( h1.GetYaxis().GetLabelSize() / (1-smlPadSize) )
    h2.Draw('E1 SAME')
    #h1.Draw('E1')
    #hComp.Draw('E1 SAME')
    leg = buildLegend( [h1, h2], [sample+' RedBkg', sample+' MC'] ) 
    leg.Draw('SAME')
    decorate( pad1, channel, h1, h2, decorateDoFinal )


    #line = ROOT.TLine( info[1], 1, info[2], 1 )
    #line.SetLineColor(ROOT.kBlack)
    #line.SetLineWidth( 1 )
    #line.Draw()
    #ratioHist.Draw('esamex0')
    # X Axis!
    ratioHist.GetYaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
    ratioHist.GetYaxis().SetTitleOffset( smlPadSize*1.5 )
    ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize()*( 1/smlPadSize) )
    ratioHist.GetYaxis().SetNdivisions( 5, True )
    ratioHist.GetXaxis().SetLabelSize( ratioHist.GetXaxis().GetLabelSize()*( 1/smlPadSize) )
    ratioHist.GetXaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( 1/smlPadSize) )
    
    
    ratioPad.cd()
    ratioHist.Draw('same e1')
    ratioLine.Draw('SAME HIST')
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSFv2/lots/%s_%s_%s.png' % (sample, channel, var) )
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSFv2/'+saveName+'.png' )

    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSF_nov23_tauALLLinear/'+saveName+'.png' )
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSF_nov23_tauALLLandau/'+saveName+'.png' )
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSF_nov23_tauFSLinear/'+saveName+'.png' )
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSF_nov23_tauFSLandau/'+saveName+'.png' )
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSF_dec01_genJets/'+saveName+'.png' )
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSF_dec01_genJets_noBJets/'+saveName+'.png' )
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSF_dec01_genJetsX_noBJets/'+saveName+'.png' )

    c1.Clear()
    del pad1, ratioPad, ratioHist, ratioLine

def decorate( p, channel, h1, h2, doFinal=False ) :

    cmsLumi = 35.9
    # Set CMS Styles Stuff
    logo = ROOT.TText(.2, .88,"CMS Preliminary")
    logo.SetTextSize(0.03)
    logo.DrawTextNDC(.2, .89,"CMS Preliminary")
    
    chan = ROOT.TLatex(.2, .80,"x")
    chan.SetTextSize(0.05)
    chan.DrawLatexNDC(.2, .84,"Channel: %s" % channelNames[channel] )
    
    lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi.SetTextSize(0.03)
    lumi.DrawTextNDC(.7,.96,"%.1f / fb (13 TeV)" % cmsLumi )

    err3 = ROOT.Double(0)
    err4 = ROOT.Double(0)
    h1.IntegralAndError( 0, h1.GetNbinsX(), err3 )
    h2.IntegralAndError( 0, h2.GetNbinsX(), err4 )
    str1 = "RB - Int: %3.2f+/-%3.2f" % (h1.Integral(), err3)
    str2 = "MC - Int: %3.2f+/-%3.2f" % (h2.Integral(), err4)
    str1c = "     evts %i" % (h1.GetEntries())
    str2c = "     evts %i" % (h2.GetEntries())

    str1b = ""
    str2b = ""
    ksNoNorm = -99
    ksNorm = -99
    if h1.Integral() > 0 and h2.Integral() > 0 and doFinal :
        for b in range( 0, h1.GetNbinsX()+1 ) :
            print "bin %i h1 %2.2f" % (b, h1.GetBinContent( b ) )
            print "bin %i h2 %2.2f" % (b, h2.GetBinContent( b ) )
            if h1.GetBinContent( b ) < 0 : h1.SetBinContent( b, 0. )
            if h2.GetBinContent( b ) < 0 : h2.SetBinContent( b, 0. )
        ksNoNorm = h1.KolmogorovTest( h2, 'X' )
        ksNorm = h1.KolmogorovTest( h2, 'XN' )
    elif h1.Integral() > 0 and h2.Integral() > 0 :
        str1b = "     Int: %3.2f+/-%1.3f pct" % (h1.Integral(), err3/h1.Integral()*100)
        str2b = "     Int: %3.2f+/-%1.3f pct" % (h2.Integral(), err4/h2.Integral()*100)
        ksNoNorm = h1.KolmogorovTest( h2, 'X' )
        ksNorm = h1.KolmogorovTest( h2, 'XN' )
   
    t1 = ROOT.TText(.2, .88,"x")
    t1.SetTextSize(0.025)
    xPos = .71
    yPos = .71
    yGap = .045
    t1.DrawTextNDC(xPos, yPos, str1)
    t1.DrawTextNDC(xPos, yPos-yGap, str1b)
    t1.DrawTextNDC(xPos, yPos-2*yGap, str1c)
    t1.DrawTextNDC(xPos, yPos-3*yGap, str2)
    t1.DrawTextNDC(xPos, yPos-4*yGap, str2b)
    t1.DrawTextNDC(xPos, yPos-5*yGap, str2c)
    t1.DrawTextNDC(xPos, yPos-6*yGap, "KS no norm: %2.3f" % ksNoNorm)
    t1.DrawTextNDC(xPos, yPos-7*yGap, "KS inc. norm: %2.3f" % ksNorm)

# Provides a list of histos to create for both channels
def getHistoDict( analysis ) :
    genVarMap = {
        #'Z_Pt' : [10, 0, 400, 40, 'Z p_{T} [GeV]', ' GeV'],
        ##'m_vis' : [7, 55, 125, 10, 'Z Mass [GeV]', ' GeV'],
        #'m_sv' : [15, 0, 300, 20, 'M_{#tau#tau} [GeV]', ' GeV'],
        #'met' : [15, 0, 300, 20, 'pfMet [GeV]', ' GeV'],
        ##'pt_1' : [10, 0, 200, 5, 'Leg1 p_{T} [GeV]', ' GeV'],
        ##'pt_2' : [10, 0, 200, 5, 'Leg2 p_{T} [GeV]', ' GeV'],
        #'pt_3' : [10, 0, 200, 5, 'Leg3 p_{T} [GeV]', ' GeV'],
        'pt_4' : [10, 0, 200, 5, 'Leg4 p_{T} [GeV]', ' GeV'],
        #'gen_match_3' : [7, -0.5, 6.5, 1, 'Gen Match Leg 3', ''],
        #'gen_match_4' : [7, -0.5, 6.5, 1, 'Gen Match Leg 4', ''],
        #'bjetCISVVeto20MediumZTT' : [5, -0.5, 4.5, 1, 'nBTag_20Medium', ''],
    }
    return genVarMap

def buildLegend( hists, names ) :
    ''' Build the legend explicitly so we can specify marker styles '''
    legend = ROOT.TLegend(0.60, 0.75, 0.95, 0.93)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for hist, name in zip( hists, names ) :
        legend.AddEntry( hist, name, 'lep')
    return legend


def prepForPlot( var, h1, h2 ) :
    maxi = h1.GetMaximum()
    if h2.GetMaximum() > maxi : maxi = h2.GetMaximum()
    h1.SetMaximum( 1.6 * maxi )
    h1.GetXaxis().SetTitle("%s" % plotVars[var][ 4 ])
    h1.GetYaxis().SetTitle("Events / Bin Width")
    h1.SetLineColor( ROOT.kRed )
    h1.SetMarkerColor( ROOT.kRed )
    h1.SetMarkerStyle( 22 )
    h2.SetLineColor( ROOT.kBlue )
    h2.SetMarkerColor( ROOT.kBlue )
    h2.SetMarkerStyle( 21 )


def makePlots( sample ) :
    channels = ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm']
    #channels = ['eeet',]#'eett','eemt','eeem','emmt','mmtt','mmmt','emmm']

    err1 = ROOT.Double(0)
    err2 = ROOT.Double(0)

    shapeOnly = True
    shapeOnly = False
    print sample
    combMapHists = {
        'LLET' : {},
        'LLMT' : {},
        'LLTT' : {},
        'LLEM' : {},
        'ZXX' : {},
    }
    c = ROOT.TCanvas('c','c',600,600)
    p = ROOT.TPad('p','p',0,0,1,1)
    p.Draw()
    p.cd()
    for var in plotVars :
        for group in combMapHists.keys() :
            combMapHists[group] = {}
            combMapHists[group][var+' '+group+' MC']  = ROOT.TH1D(var+' '+group+' MC', var+' '+group+' MC', plotVars[var][0], plotVars[var][1], plotVars[var][2])
            combMapHists[group][var+' '+group+' RB'] = ROOT.TH1D(var+' '+group+' RB', var+' '+group+' RB', plotVars[var][0], plotVars[var][1], plotVars[var][2])

    print combMapHists
    for channel in channels :
        print channel
        iDir = 'root_files_tauFinalStatesLandau'
        iDir = 'root_files_tauFinalStatesLinear'
        iDir = 'root_files_tauAllLandau'
        iDir = 'root_files_tauAllLinear'
        iDir = 'root_files'
        ifile = ROOT.TFile(iDir+'/%s_%s.root' % (sample, channel), 'r' )
        itree = ifile.Get('Ntuple')
        #compfile = ROOT.TFile('../azh3Sept05OSLooseForRBVal/%s_%s.root' % (sample, channel), 'r' )
        #compfile = ROOT.TFile('../azh3Nov13RedBkgMC_allFakes/%s_%s.root' % (sample, channel), 'r' )
        compfile = ROOT.TFile('../azh3Nov13RedBkgMC/%s_%s.root' % (sample, channel), 'r' )
        print ifile, itree.GetEntries()
        print compfile
    
        var = 'pt_3'
        var = 'pt_4'
        #var = 'm_sv'
        #var = 'met'
        #var = 'gen_match_3'
        #var = 'gen_match_4'
        #var = 'bjetCISVVeto20MediumZTT'
    
        h1 = ROOT.TH1D(var+'_'+channel, var+'_'+channel, plotVars[var][0], plotVars[var][1], plotVars[var][2])
        hComp = compfile.Get('%s_Histos/%s' % (channel, var))
    
        cut = '(ADD_CHANNEL_SPECIFIC_ISO_CUTS)'
        cutString = getRedBkgCutsAndWeights( 'azh', channel, cut, prodMap ).strip('*')
        cutString = '(GenWeight/abs( GenWeight ))*'+cutString.replace(')(',')*(')
        #cutString += '(zhFR1 + zhFR2 - zhFR0)'
        cutString += '*(puweight*azhWeight)' 
        cutString += '*(XSecLumiWeight)'
        cutString += '*(bjetCISVVeto20MediumZTT==0)'
        if channel in ['eeet','emmt'] :
            #cutString += '*(LT_higgs > 30)'
            cutString += '*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)'
        elif channel in ['eemt','mmmt'] :
            #cutString += '*(LT_higgs > 40)'
            cutString += '*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)'
        elif channel in ['eeem','emmm'] :
            cutString += '*(LT_higgs > 20)'
        elif channel in ['eett','mmtt'] :
            #cutString += '*(LT_higgs > 80)' # > 80 GeV is 10% better than 60,
            cutString += '*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)'
            cutString += '*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)'

        print '\n'+cutString+'\n'
        
        itree.Draw( var+'>>'+var+'_'+channel, cutString )
        h1.IntegralAndError( 0, h1.GetNbinsX(), err1 )
        hComp.IntegralAndError( 0, hComp.GetNbinsX(), err2 )
        print "h1 - int: %3.3f +/- %3.3f  nEntries %i" % (h1.Integral(), err1, h1.GetEntries())
        print "hComp - int: %3.3f +/- %3.3f  nEntries %i" % (hComp.Integral(), err2, hComp.GetEntries())

        if shapeOnly :
            if h1.Integral() > 0. :
                h1.Scale( 1. / h1.Integral() )
            if hComp.Integral() > 0. :
                hComp.Scale( 1. / hComp.Integral() )

        prepForPlot( var, h1, hComp )

        saveName = 'lots/%s_%s_%s' % (sample, channel, var)
        makeRatioPlot( h1, hComp, c, sample, var, channel, saveName )
        h1.SetDirectory( 0 )
        hComp.SetDirectory( 0 )

        for group, chans in combMap.iteritems() :
            if channel in chans :
                print combMapHists[ group ]
                combMapHists[ group ][ var+' '+group+' MC' ].Add( hComp )
                combMapHists[ group ][ var+' '+group+' RB' ].Add( h1 )

        #break
    for group, hists in combMapHists.iteritems() :
        for var in plotVars.keys() :
            prepForPlot( var, hists[var+' '+group+' RB'], hists[var+' '+group+' MC'] )
            hists[var+' '+group+' RB'].Draw('E1')
            hists[var+' '+group+' MC'].Draw('E1 SAME')
            saveName = '%s/%s_%s_%s' % (group, sample, group, var)
            makeRatioPlot( hists[var+' '+group+' RB'], hists[var+' '+group+' MC'], c, sample, var, group, saveName )
            #leg = buildLegend( [hists[var+' '+group+' RB'], hists[var+' '+group+' MC']], [sample+' RedBkg', sample+' MC'] ) 
            #leg.Draw('SAME')
            #decorate( p, group, hists[var+' '+group+' RB'], hists[var+' '+group+' MC'] )
            #c.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSFv2/%s/%s_%s_%s.png' % (group, sample, group, var) )
    del c, p
    return combMapHists




if __name__ == '__main__' :

    channelNames = {
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
        'LLET' : "ll'e#tau_{h}",
        'LLMT' : "ll'#mu#tau_{h}",
        'LLTT' : "ll'#tau_{h}#tau_{h}",
        'LLEM' : "ll'e#mu",
    }
    combMap = {
        'LLET' : ['eeet','emmt'],
        'LLMT' : ['eemt','mmmt',],
        'LLTT' : ['eett','mmtt'],
        'LLEM' : ['eeem','emmm'],
        'ZXX' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'],
    }
    ROOT.gROOT.SetBatch(True)
    tdr.setTDRStyle()
    analysis = 'azh'
    prodMap = getProdMap()
    plotVars = getHistoDict( analysis )
    azhSamples = ['WZ3l1nu', 'DYJets4', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets', 'TT'] # May 31 samples, no ZZ->all, use ZZ4l
    #azhSamples = ['DYJets4', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets',]
    sampMap = {}
    for sample in azhSamples :
        sampMap[ sample ] = makePlots( sample )

    print "\n\n Finished normals stuff \n\n"
    combMapHists = {
        'LLET' : {},
        'LLMT' : {},
        'LLTT' : {},
        'LLEM' : {},
        'ZXX' : {},
    }
    c = ROOT.TCanvas('c','c',600,600)
    p = ROOT.TPad('p','p',0,0,1,1)
    p.Draw()
    p.cd()
    for var in plotVars :
        for group in combMapHists.keys() :
            h1 = ROOT.TH1D(var+' Total RB', var+' Total RB', plotVars[var][0], plotVars[var][1], plotVars[var][2])
            h2 = ROOT.TH1D(var+' Total MC', var+' Total MC', plotVars[var][0], plotVars[var][1], plotVars[var][2])
            for sample in azhSamples :
                h1.Add( sampMap[ sample ][ group ][var+' '+group+' RB'] )
                h2.Add( sampMap[ sample ][ group ][var+' '+group+' MC'] )

            err1 = ROOT.Double(0)
            err2 = ROOT.Double(0)
            h1.IntegralAndError( 0, h1.GetNbinsX(), err1 )
            h2.IntegralAndError( 0, h2.GetNbinsX(), err2 )
            print "h1 - int: %3.3f +/- %3.3f  nEntries %i" % (h1.Integral(), err1, h1.GetEntries())
            print "h2 - int: %3.3f +/- %3.3f  nEntries %i" % (h2.Integral(), err2, h2.GetEntries())

            prepForPlot( var, h1, h2 )
            saveName = '%s/Total_%s_%s' % (group, group, var)
            makeRatioPlot( h1, h2, c, 'Total', var, group, saveName, True )
            #h1.Draw('')
            #h2.Draw('SAME')
            #leg = buildLegend( [h1, h2], ['Total RedBkg', 'Total MC'] ) 
            #leg.Draw('SAME')
            #decorate( p, group, h1, h2, True )
            #c.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgVal_mcSFv2/%s/Total_%s_%s.png' % (group, group, var) )
            


