import ROOT
from time import gmtime, strftime
from ROOT import gPad, gROOT, gStyle
import pyplotter.tdrstyle as tdr
import sys
sys.path.append( '/afs/cern.ch/work/t/truggles/Z_to_tautau/CMSSW_7_6_3_patch2/src/Z_to_TauTau_13TeV/util' )
from ratioPlot import ratioPlot
from array import array

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()
numT = 5
numJ = 7

def finishPlots( histos, plot, plotMap, runList, name, runColors ) :
    ratio = True

    c1 = ROOT.TCanvas(plot,plot,600,600)
    if ratio :
        xBins = array('d', []) 
        totBins = histos[ runList[0] ].GetXaxis().GetNbins()
        binWidth = histos[ runList[0] ].GetXaxis().GetBinWidth( 1 )
        first = histos[ runList[0] ].GetXaxis().GetBinLowEdge( 1 )
        for i in range( 0, int(totBins)+1 ) :
             xBins.append( round(i*binWidth+first,1) )
        xNum = len( xBins ) - 1
        smlPadSize = .25
        pads = ratioPlot( c1, 1-smlPadSize )
        p1 = pads[0]
        ratioPad = pads[1]
        ratioPad.SetTopMargin(0.00)
        ratioPad.SetBottomMargin(0.3)
        p1.SetBottomMargin(0.00)
        ratioPad.SetGridy()
        ratioHist = ROOT.TH1F('ratio %s' % runList[0], 'ratio', xNum, xBins )
        ratioHist.Sumw2()
        ratioHist.Add( histos[ runList[0] ] )
        ratioHist.Divide( histos[ runList[1] ] )
        #ratioHist.SetMaximum( ratioHist.GetMaximum() * 1.2 )
        #ratioHist.SetMinimum( ratioHist.GetMinimum() * 1.2 )
        ratioHist.SetMaximum( 1.5 )
        ratioHist.SetMinimum( 0.5 )
        ratioHist.SetMarkerStyle( 21 )
        ratioPad.cd()
        ratioHist.Draw('ex0')
        line = ROOT.TLine( xBins[0], 1, xBins[-1], 1 )
        line.SetLineColor(ROOT.kBlack)
        line.SetLineWidth( 1 )
        line.Draw()
        ratioHist.Draw('esamex0')
        # X Axis!
        ratioHist.GetXaxis().SetTitle('%s' % plotMap[plot][0])
        ratioHist.GetYaxis().SetTitle("80X / 76X")
        ratioHist.GetYaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
        ratioHist.GetYaxis().SetTitleOffset( smlPadSize*1.5 )
        ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize()*( 1/smlPadSize) )
        ratioHist.GetYaxis().SetNdivisions( 5, True )
        ratioHist.GetXaxis().SetLabelSize( ratioHist.GetXaxis().GetLabelSize()*( 1/smlPadSize) )
        ratioHist.GetXaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( 1/smlPadSize) )


    p1.cd()
    p1.cd()

    histos[ runList[0] ].Draw('e0')
    histos[ runList[1] ].Draw('same e0')

    maxi = 0
    for run in runList :
        #print histos[run].GetMaximum()
        histos[run].SetLineColor( runColors[ run ] )
        histos[run].SetLineWidth( 2 )
        if histos[run].GetMaximum() > maxi : maxi = histos[run].GetMaximum()
    histos[ runList[0] ].SetMaximum( maxi * 1.5 )
    histos[ runList[0] ].GetXaxis().SetTitle( '%s' % plotMap[plot][0] )
    #p1.SetTitle( '%s' % plot.replace('By',' vs. ') )
    #c1.SetTitle( '%s' % plot.replace('By',' vs. ') )
    if 'hreeProng' in name : yaxis = 'Taus / Event'
    elif 'taus' in name : yaxis = 'Taus / Jets Rate'
    elif 'jets' in name : yaxis = 'Jets / Event'
    else : yaxis = name
    if 'scale' in plotMap[plot][4] :
        yaxis = 'A.U.'
    histos[ runList[0] ].GetYaxis().SetTitle( yaxis )

    logo = ROOT.TText(.2, .88,"CMS Preliminary")
    logo.SetTextSize(0.04)
    logo.DrawTextNDC(.2, .89,"CMS Preliminary")

    lumi = ROOT.TText(.7,1.05,"(13 TeV)")
    lumi.SetTextSize(0.04)
    lumi.DrawTextNDC(.8,.96,"(13 TeV)" )
 
    Title = ROOT.TText(.7,1.05,"(13 TeV)")
    Title.SetTextSize(0.04)
    Title.DrawTextNDC(.15,.96,"%s" % plot.replace('By',' vs. ') )

    p1.BuildLegend( .65, .73, .95, .95 )
    p1.Update()
    if plotMap[ plot ][0]  == 'nvtx' :
        gStyle.SetOptFit(0000)
        funcs = {}
        fits = {}
        for run in runList :
            funcs[ run ] = ROOT.TF1( 'funx%s' % run, '[0] + (x * [1])', 5, 27 )
            f1 = gROOT.GetFunction('funx%s' % run )
            f1.SetParName( 0, 'Y-int' )
            f1.SetParName( 1, 'slope' )
            f1.SetParameter( 0, 99 )
            f1.SetParameter( 1, 99 ) 

            #histos[run].Fit('funx%s' % run, 'EMRIW')
            histos[run].Fit('funx%s' % run, 'R' )
            fits[ run ] = histos[run].GetFunction("funx%s" % run )
            fits[ run ].SetLineColor( runColors[ run ] )
            fits[ run ].SetLineWidth( 4 )
            fits[ run ].SetLineStyle( 1 )
            fits[ run ].Draw('same')

    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/%s/%s.png' % (runList[0].split('_')[0], name ) )

    if 'num' in name :
        p1.SetLogy()
        histos[ runList[0] ].SetMaximum( 2 )
        p1.Update()
        c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/%s/%s_log.png' % (runList[0].split('_')[0], name ) )

def getHist( histDict, key, tree, fill, weight, histName, run ) :
    tree.Draw( fill, weight )
    histDict[ key ] = gPad.GetPrimitive( histName )
    histDict[ key ].SetDirectory( 0 )
    histDict[ key ].SetTitle( str(run) )
    histDict[ key ].Sumw2()
    

def plotter( runList, runColors, plot ) :
    print "Starting: %s" % plot
#for plot in plotMap.keys() :
    numEventsPerRun = {}
    hists = {}
    #jhists = {}
    hists2 = {}
    #jhists2 = {}
    for run in runList :
        info = plotMap[plot][1].strip('(').strip(')').split(',')
        #print info
        numB = int(info[0])
        first = int(info[1])
        last = int(info[2])
        hists[ run ] = ROOT.TH1F( '%s' % run, '%s' % run, numB, first, last)
        #jhists[ run ] = ROOT.TH1F( 'j%s' % run, 'j%s' % run, numB, first, last)
        hists2[ run ] = ROOT.TH1F( '2_%s' % run, '2_%s' % run, numB, first, last)
        #jhists2[ run ] = ROOT.TH1F( 'j2_%s' % run, 'j2_%s' % run, numB, first, last)
        
    
    for run in runList :
        print "Run: %s" % run
        f = ROOT.TFile('%s/%s.root' % (run, run.split('_')[0]),'r')
        #f = ROOT.TFile('%s.root' % run,'r')
        tree = f.Get('tauEvents/Ntuple')
        weightedSum = 0
        for row in tree :
            weightedSum += row.PUWeight
        numEventsPerRun[ run ] = (tree.GetEntries(), weightedSum)
        #if (plotMap[plot][0] == 'nvtx') or (plotMap[plot][0] == 'bunchCrossing') or (plotMap[plot][0] == 'lumi') :
        getHist( hists, run, tree, '%s>>hist%s%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s' % plotMap[plot][2], 'hist%s' % run, run )
        getHist( hists2, run, tree, '%s>>hist2%s%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s' % plotMap[plot][3], 'hist2%s' % run, run )

        if 'div' in plotMap[plot][4] :
            hists[ run ].Divide( hists2[ run ] )
        if 'scale' in plotMap[plot][4] :
            hists[ run ].Scale( 1 / hists[ run ].Integral() )
        if 'x' in plotMap[plot][4] :
            print "Scaling by weighted sum: %f" % numEventsPerRun[ run ][1]
            hists[ run ].Scale( 1 / numEventsPerRun[ run ][1] )
            print "New Integral: %f" % hists[ run ].Integral()
        print "### Done first"

    print " <<< Plotting"
    name = plot
    finishPlots( hists, plot, plotMap, runList, name, runColors )
    return "Finished Plotting %s" % plot
        



plotMap = {

    #''' With Trigger Matching !!! '''
    'numTausThreeProng' : ( 'numTausThreeProng', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'numTausThreeProng30' : ( 'numTausThreeProng30', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'numTausThreeProngIsoPass' : ( 'numTausThreeProngIsoPass', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'numJets30Clean' : ( 'numJets30Clean', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'numLeadingTauMissingHits' : ( 't1MissingHits', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),

    'threeProngTaus30ByTauPt' : ( 't1Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTau2Pt' : ( 't2Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTauIso' : ( 't1Iso', '(20,0,200)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTauIso_' : ( 't1Iso', '(25,0,25)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTauIso__' : ( 't1Iso', '(10,0,5)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTau2Iso' : ( 't2Iso', '(20,0,200)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTauIsoChrg' : ( 't1IsoChrg', '(20,0,100)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTauIsoChrg_' : ( 't1IsoChrg', '(25,0,25)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'IsolatedThreeProngTaus30ByTauIsoChrg__' : ( 't1IsoChrg', '(10,0,2)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTau2IsoChrg' : ( 't2IsoChrg', '(20,0,100)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'jets30CleanByJetPt' : ( 'j1Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'jets30CleanByJet2Pt' : ( 'j2Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'jets30CleanByJet3Pt' : ( 'j3Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTauPhi' : ( 't1Phi', '(20,-4,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'jets30CleanByJetPhi' : ( 'j1Phi', '(20,-4,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'threeProngTaus30ByTauEta' : ( 't1Eta', '(30,-3,3)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'jets30CleanByJetEta' : ( 'j1Eta', '(30,-3,3)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'missingHitsPer3ProngTaus30ByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTauMissingHits', 'PUWeight*IsoMu20*numTausThreeProng30', 'div' ),
    'missingHitsPer3ProngTaus30ByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTauMissingHits', 'PUWeight*IsoMu20*numTausThreeProng30', 'div' ),

    'missingHitsPer3ProngTaus30ByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTauMissingHits', 'PUWeight*IsoMu20*numTausThreeProng30', 'div' ),
    'threeProngTaus30ByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20', 'div' ),
    'threeProngTaus30ByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20', 'div' ),
    'threeProngTaus30IsoPassByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20', 'div' ),
    'threeProngTaus30IsoChrgPassByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30IsoChrgPass', 'PUWeight*IsoMu20', 'div' ),
    'jets30CleanByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numJets30Clean', 'PUWeight*IsoMu20', 'div' ),
    'taus30PerJet30CleanByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    'taus30IsoPassPerJet30CleanByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    'taus30IsoChrgPassPerJet30CleanByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30IsoChrgPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),

    'jets30CleanByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numJets30Clean', 'PUWeight*IsoMu20', 'div' ),
    'threeProngTaus30ByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20', 'div' ),
    'threeProngTaus30IsoPassByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20', 'div' ),
    'threeProngTaus30IsoChrgPassByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20', 'div' ),
    'taus30IsoPassPerJet30CleanByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30IsoChrgPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    'taus30IsoChrgPassPerJet30CleanByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30IsoChrgPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    'taus30PerJet30CleanByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),

    'jets30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numJets30Clean', 'PUWeight*IsoMu20', 'div' ),
    'threeProngTaus30ByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20', 'div' ),
    'threeProngTaus30IsoPassByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20', 'div' ),
    'taus30IsoPassPerJet30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    'taus30PerJet30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),

}


def RunPlots( runList ) :
    ''' timing... '''
    begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print "\nStart Time: %s" % str( begin )
    
    
    from collections import OrderedDict
    runColors = OrderedDict()
    runColors[runList[0]] = ROOT.kBlack
    runColors[runList[1]] = ROOT.kRed
    
    
    
    import multiprocessing
    ## Enable multiprocessing
    numCores = 20
    pool = multiprocessing.Pool(processes = numCores )
    multiprocessingOutputs = []
    for plot in plotMap.keys() :
        
        #plotter( runList, runColors, '%s' % plot ) # For Debugging
        multiprocessingOutputs.append( pool.apply_async(plotter, args=( runList, runColors, '%s' % plot, ) ) )
    
    mpResults = [p.get() for p in multiprocessingOutputs]
    mpResults.sort()
    for item in mpResults :
        print item
    
    print "Make html.index"
    htmlFile = open('/afs/cern.ch/user/t/truggles/www/threeProngs/%s/index.html' % runList[0].split('_')[0], 'w' )
    htmlFile.write( '<html><head><STYLE type="text/css">img { border:0px; }</STYLE>\n' )
    htmlFile.write( '<title>Tau Tracking Study/</title></head>\n' )
    htmlFile.write( '<body>\n' )
    for plot in plotMap.keys() :
        htmlFile.write( '<img src="%s.png">\n' % plot )
        if 'num' in plot: 
            htmlFile.write( '<img src="%s_log.png">\n' % plot )
    htmlFile.write( '</body></html>' )
    htmlFile.close()
    
    print "\nStart Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )







if __name__ == '__main__' :
    runs = [256677, 260627]
    versions = ['80X_RelVal','76X']
    for run in runs :
        runList = []
        for version in versions :
            runList.append( "%s_%s" % (str(run), version) )
        RunPlots( runList )




