import ROOT
from time import gmtime, strftime
from ROOT import gPad, gROOT, gStyle
import pyplotter.tdrstyle as tdr

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()
numT = 5
numJ = 7

def finishPlots( histos, plot, plotMap, run, name ) :
    c1 = ROOT.TCanvas(plot,plot,600,600)
    p1 = ROOT.TPad('p_%s' % plot,'p_%s' % plot,0,0,1,1)
    p1.Draw()
    p1.cd()

    histos[258425].Draw('e0')
    histos[259721].Draw('same e0')
    histos[254833].Draw('same e0')
    histos[254790].Draw('same e0')

    maxi = 0
    for run in runs :
        #print histos[run].GetMaximum()
        histos[run].SetLineColor( runs[ run ] )
        histos[run].SetLineWidth( 2 )
        if histos[run].GetMaximum() > maxi : maxi = histos[run].GetMaximum()
    histos[258425].SetMaximum( maxi * 1.5 )
    histos[258425].GetXaxis().SetTitle( '%s' % plotMap[plot][0] )
    #p1.SetTitle( '%s' % plot.replace('By',' vs. ') )
    #c1.SetTitle( '%s' % plot.replace('By',' vs. ') )
    if 'threeProng' in name : yaxis = 'Taus / Event'
    elif 'taus' in name : yaxis = 'Taus / Jets Rate'
    elif 'jets' in name : yaxis = 'Jets / Event'
    else : yaxis = name
    if 'scale' in plotMap[plot][4] :
        yaxis = 'A.U.'
    histos[258425].GetYaxis().SetTitle( yaxis )

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
        for run in runs :
            funcs[ run ] = ROOT.TF1( 'funx%i' % run, '[0] + (x * [1])', 5, 27 )
            f1 = gROOT.GetFunction('funx%i' % run )
            f1.SetParName( 0, 'Y-int' )
            f1.SetParName( 1, 'slope' )
            f1.SetParameter( 0, 99 )
            f1.SetParameter( 1, 99 ) 

            #histos[run].Fit('funx%i' % run, 'EMRIW')
            histos[run].Fit('funx%i' % run, 'R' )
            fits[ run ] = histos[run].GetFunction("funx%i" % run )
            fits[ run ].SetLineColor( runs[ run ] )
            fits[ run ].SetLineWidth( 4 )
            fits[ run ].SetLineStyle( 1 )
            fits[ run ].Draw('same')

    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/%s.png' % name )
    if 'num' in name :
        p1.SetLogy()
        histos[258425].SetMaximum( 2 )
        p1.Update()
        c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/%s_log.png' % name )

def getHist( histDict, key, tree, fill, weight, histName, run ) :
    tree.Draw( fill, weight )
    histDict[ key ] = gPad.GetPrimitive( histName )
    histDict[ key ].SetDirectory( 0 )
    histDict[ key ].SetTitle( str(run) )
    histDict[ key ].Sumw2()
    

''' timing... '''
begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "\nStart Time: %s" % str( begin )

plotMap = {

    #''' With Trigger Matching !!! '''
    'numTausThreeProng' : ( 'numTausThreeProng', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'numTausThreeProng30' : ( 'numTausThreeProng30', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'numTausThreeProngIsoPass' : ( 'numTausThreeProngIsoPass', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'numJets30Clean' : ( 'numJets30Clean', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    'numLeadingTauMissingHits' : ( 't1MissingHits', '(4,0,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),

    #'threeProngTaus30ByTauPt' : ( 't1Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'threeProngTaus30ByTau2Pt' : ( 't2Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'threeProngTaus30ByTauIso' : ( 't1Iso', '(20,0,200)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'threeProngTaus30ByTau2Iso' : ( 't2Iso', '(20,0,200)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'threeProngTaus30ByTauIsoChrg' : ( 't1IsoChrg', '(20,0,100)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'threeProngTaus30ByTau2IsoChrg' : ( 't2IsoChrg', '(20,0,100)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'jets30CleanByJetPt' : ( 'j1Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'jets30CleanByJet2Pt' : ( 'j2Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'jets30CleanByJet3Pt' : ( 'j3Pt', '(30,0,150)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'threeProngTaus30ByTauPhi' : ( 't1Phi', '(20,-4,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'jets30CleanByJetPhi' : ( 'j1Phi', '(20,-4,4)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'threeProngTaus30ByTauEta' : ( 't1Eta', '(30,-3,3)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'jets30CleanByJetEta' : ( 'j1Eta', '(30,-3,3)', 'PUWeight*IsoMu20', 'IsoMu20', 'scale' ),
    #'missingHitsPer3ProngTaus30ByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTauMissingHits', 'PUWeight*IsoMu20*numTausThreeProng30', 'div' ),
    #'missingHitsPer3ProngTaus30ByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTauMissingHits', 'PUWeight*IsoMu20*numTausThreeProng30', 'div' ),
    #'missingHitsPer3ProngTaus30ByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTauMissingHits', 'PUWeight*IsoMu20*numTausThreeProng30', 'div' ),
    #'threeProngTaus30ByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20', 'div' ),
    #'threeProngTaus30ByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20', 'div' ),
    #'threeProngTaus30IsoPassByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20', 'div' ),
    #'threeProngTaus30IsoChrgPassByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30IsoChrgPass', 'PUWeight*IsoMu20', 'div' ),
    #'jets30CleanByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numJets30Clean', 'PUWeight*IsoMu20', 'div' ),
    #'taus30PerJet30CleanByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    #'taus30IsoPassPerJet30CleanByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    #'taus30IsoChrgPassPerJet30CleanByNvtx' : ( 'nvtx', '(30,0,30)', 'PUWeight*IsoMu20*numTausThreeProng30IsoChrgPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),

    #'jets30CleanByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numJets30Clean', 'PUWeight*IsoMu20', 'div' ),
    #'threeProngTaus30ByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20', 'div' ),
    #'threeProngTaus30IsoPassByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20', 'div' ),
    #'threeProngTaus30IsoChrgPassByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20', 'div' ),
    #'taus30IsoPassPerJet30CleanByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30IsoChrgPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    #'taus30IsoChrgPassPerJet30CleanByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30IsoChrgPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    #'taus30PerJet30CleanByLumi' : ( 'lumi', '(17,0,1700)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),

    #'jets30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numJets30Clean', 'PUWeight*IsoMu20', 'div' ),
    #'threeProngTaus30ByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20', 'div' ),
    #'threeProngTaus30IsoPassByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20', 'div' ),
    #'taus30IsoPassPerJet30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTausThreeProng30IsoPass', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),
    #'taus30PerJet30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*IsoMu20*numTausThreeProng30', 'PUWeight*IsoMu20*numJets30Clean', 'div' ),

}

from collections import OrderedDict
runs = OrderedDict()
runs[258425] = ROOT.kCyan
runs[259721] = ROOT.kGreen
runs[254833] = ROOT.kBlue
runs[254790] = ROOT.kRed

def plotter( plot ) :
    print "Starting: %s" % plot
#for plot in plotMap.keys() :
    numEventsPerRun = {}
    hists = {}
    #jhists = {}
    hists2 = {}
    #jhists2 = {}
    for run in runs.keys() :
        info = plotMap[plot][1].strip('(').strip(')').split(',')
        #print info
        numB = int(info[0])
        first = int(info[1])
        last = int(info[2])
        hists[ run ] = ROOT.TH1F( '%i' % run, '%i' % run, numB, first, last)
        #jhists[ run ] = ROOT.TH1F( 'j%i' % run, 'j%i' % run, numB, first, last)
        hists2[ run ] = ROOT.TH1F( '2_%i' % run, '2_%i' % run, numB, first, last)
        #jhists2[ run ] = ROOT.TH1F( 'j2_%i' % run, 'j2_%i' % run, numB, first, last)
        
    
    for run in runs.keys() :
        print "Run: %i" % run
        f = ROOT.TFile('%i/%i.root' % (run, run),'r')
        #f = ROOT.TFile('%i.root' % run,'r')
        tree = f.Get('tauEvents/Ntuple')
        weightedSum = 0
        for row in tree :
            weightedSum += row.PUWeight
        numEventsPerRun[ run ] = (tree.GetEntries(), weightedSum)
        #if (plotMap[plot][0] == 'nvtx') or (plotMap[plot][0] == 'bunchCrossing') or (plotMap[plot][0] == 'lumi') :
        getHist( hists, run, tree, '%s>>hist%i%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][2], run), 'hist%i' % run, run )
        getHist( hists2, run, tree, '%s>>hist2%i%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][3], run), 'hist2%i' % run, run )

        if 'div' in plotMap[plot][4] :
            hists[ run ].Divide( hists2[ run ] )
        if 'scale' in plotMap[plot][4] :
            hists[ run ].Scale( 1 / hists[ run ].Integral() )
        if 'x' in plotMap[plot][4] :
            print "Scaling by weighted sum: %f" % numEventsPerRun[ run ][1]
            hists[ run ].Scale( 1 / numEventsPerRun[ run ][1] )
            print "New Integral: %f" % hists[ run ].Integral()
        print "### Done first"


        #else :
        #    var_ = plotMap[plot][0]
        #    cnt = 0
        #    for row in tree :
        #        cnt += 1
        #        if cnt > 1000 : continue
        #        for i in range(1, numT + 1) :
        #            inVar = 't_%s' % var_
        #            newVar = inVar.replace('_',str(i))
        #            if plotMap[plot][0] == 'bunchCrossing' :
        #                newVar = 'bunchCrossing'
        #            if plotMap[plot][0] == 'Pt' :
        #                inVar = 't_Jet%s' % var_
        #                newVar = inVar.replace('_',str(i))
        #            hists[ run ].Fill( getattr(row, newVar), row.PUWeight )
        #            hists2[ run ].Fill( getattr(row, newVar) )
        #        if 'Iso' not in plotMap[plot][0] :
        #            for j in range(1, numJ + 1) :
        #                inVar = 'j_%s' % var_
        #                newVar = inVar.replace('_',str(j))
        #                if plotMap[plot][0] == 'bunchCrossing' :
        #                    newVar = 'bunchCrossing'
        #                if ( getattr( row, 'j%iLooseID' % j ) > 0 ) and ( getattr( row, 'j%iPassPU' % j ) > 0 ) and ( getattr( row, 'j%iPt' % j) > 30 ) :
        #                    jhists[ run ].Fill( getattr(row, newVar), row.PUWeight )
        #                    jhists2[ run ].Fill( getattr( row, newVar) )
    #for iRun in numEventsPerRun :
    #    print "RUN: %i  Evt Stuff:" % iRun, numEventsPerRun[iRun]
                
            
   
    #if (plotMap[plot][0] == 'nvtx') or (plotMap[plot][0] == 'bunchCrossing') or (plotMap[plot][0] == 'lumi') :
    print " <<< Plotting"
    name = plot
    finishPlots( hists, plot, plotMap, runs, name )
    #else :
    #    for run in runs :
    #        if numEventsPerRun[run][0] > 0 :
    #            hists[ run ].Scale( 1 / numEventsPerRun[run][0] )
#   #             hists2[ run ].Scale( 1 / numEventsPerRun[run][0] )
    #            jhists[ run ].Scale( 1 / numEventsPerRun[run][0] )
#   #             jhists2[ run ].Scale( 1 / numEventsPerRun[run][0] )
    #    name = 'tmp2/%s_tau' % plot
    #    finishPlots( hists, plot, plotMap, runs, name )
#   #     name = 'tmp2/%s_tau2' % plot
#   #     finishPlots( hists2, plot, plotMap, runs, name )
    #    name = 'tmp2/%s_jet' % plot
    #    finishPlots( jhists, plot, plotMap, runs, name )
#   #     name = 'tmp2/%s_jet2' % plot
#   #     finishPlots( jhists2, plot, plotMap, runs, name )
    #    if ('Iso' not in plotMap[plot][0]) and (hists[run].Integral() > 0 ) :
    #        for run in runs :
    #            hists[ run ].Divide( jhists[ run ] )
    #            hists[ run ].Scale( 1 / hists[ run ].Integral() )
    #        name = 'tmp2/%s_tauPerJet' % plot
    #        finishPlots( hists, plot, plotMap, runs, name )
    return "Finished Plotting %s" % plot
        

        
    

import multiprocessing
## Enable multiprocessing
numCores = 20
pool = multiprocessing.Pool(processes = numCores )
multiprocessingOutputs = []
for plot in plotMap.keys() :
    multiprocessingOutputs.append( pool.apply_async(plotter, args=( '%s' % plot, ) ) )

mpResults = [p.get() for p in multiprocessingOutputs]
mpResults.sort()
for item in mpResults :
    print item

print "Make html.index"
htmlFile = open('/afs/cern.ch/user/t/truggles/www/threeProngs/index.html', 'w')
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



