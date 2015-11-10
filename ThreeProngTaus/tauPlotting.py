import ROOT
from time import gmtime, strftime
from ROOT import gPad
import pyplotter.tdrstyle as tdr

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()
numT = 5
numJ = 7

def finishPlots( histos, plot, plotMap, run, name ) :
    c1 = ROOT.TCanvas(plot,plot,400,400)
    p1 = ROOT.TPad('p_%s' % plot,'p_%s' % plot,0,0,1,1)
    p1.Draw()
    p1.cd()

    histos[259721].Draw('e0')
    histos[254833].Draw('same e0')
    histos[254790].Draw('same e0')
    histos[258425].Draw('same e0')
   
    maxi = 0
    for run in runs :
        #print histos[run].GetMaximum()
        histos[run].SetLineColor( runs[ run ] )
        histos[run].SetLineWidth( 2 )
        if histos[run].GetMaximum() > maxi : maxi = histos[run].GetMaximum()
    histos[259721].SetMaximum( maxi * 1.5 )
    histos[259721].GetXaxis().SetTitle( '%s' % plotMap[plot][0] )
    #p1.SetTitle( '%s' % plot.replace('By',' vs. ') )
    #c1.SetTitle( '%s' % plot.replace('By',' vs. ') )
    if 'threeProng' in name : yaxis = 'Taus / Event'
    elif 'taus' in name : yaxis = 'Taus / Jet'
    elif 'jets' in name : yaxis = 'Jets / Event'
    else : yaxis = name
    histos[259721].GetYaxis().SetTitle( yaxis )

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
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/%s.png' % name )

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
    #'threeProngTausByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProng', 'PUWeight', 'div' ),
    #'threeProngTausIsoPassByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProngIsoPass', 'PUWeight', 'div' ),
    #'jets20ByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numJets20', 'PUWeight', 'div' ),
    #'taus20IsoPassPerJet20ByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProngIsoPass', 'PUWeight*numJets20', 'div' ),
    #'tausPerJetByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProng', 'PUWeight*numJets20', 'div' ),

    #''' With Trigger Matching !!! '''
    'threeProngTaus30ByTauPt' : ( 't1Pt', '(50,0,500)', 'PUWeight*PFJet450Pass', 'PFJet450Pass', 'div' ),
    'jets30CleanByJetPt' : ( 'j1Pt', '(50,0,500)', 'PUWeight*PFJet450Pass', 'PFJet450Pass', 'div' ),
    'threeProngTaus30ByTauPhi' : ( 't1Phi', '(40,-4,4)', 'PUWeight*PFJet450Pass', 'PFJet450Pass', 'div' ),
    'jets30CleanByJetPhi' : ( 'j1Phi', '(40,-4,4)', 'PUWeight*PFJet450Pass', 'PFJet450Pass', 'div' ),
    'threeProngTaus30ByTauEta' : ( 't1Eta', '(30,-3,3)', 'PUWeight*PFJet450Pass', 'PFJet450Pass', 'div' ),
    'jets30CleanByJetEta' : ( 'j1Eta', '(30,-3,3)', 'PUWeight*PFJet450Pass', 'PFJet450Pass', 'div' ),
    #'threeProngTaus30ByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*PFJet450Pass*numTausThreeProng30', 'PUWeight*PFJet450Pass', 'div' ),
    #'threeProngTaus30TrigByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*PFJet450Pass*numTausThreeProng30*PFJet450Pass', 'PUWeight*PFJet450Pass*PFJet450Pass', 'div' ),
    #'threeProngTaus30IsoPassByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoPass', 'PUWeight*PFJet450Pass', 'div' ),
    #'threeProngTaus30IsoChrgPassByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoChrgPass', 'PUWeight*PFJet450Pass', 'div' ),
    #'jets30CleanByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*PFJet450Pass*numJets30Clean', 'PUWeight*PFJet450Pass', 'div' ),
    #'taus30PerJet30CleanByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*PFJet450Pass*numTausThreeProng30', 'PUWeight*PFJet450Pass*numJets30Clean', 'div' ),
    #'taus30IsoPassPerJet30CleanByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoPass', 'PUWeight*PFJet450Pass*numJets30Clean', 'div' ),
    #'taus30IsoChrgPassPerJet30CleanByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoChrgPass', 'PUWeight*PFJet450Pass*numJets30Clean', 'div' ),

    #'jets30CleanByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*PFJet450Pass*numJets30Clean', 'PUWeight*PFJet450Pass', 'div' ),
    #'threeProngTaus30ByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*PFJet450Pass*numTausThreeProng30', 'PUWeight*PFJet450Pass', 'div' ),
    #'threeProngTaus30IsoPassByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoPass', 'PUWeight*PFJet450Pass', 'div' ),
    #'threeProngTaus30IsoChrgPassByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoPass', 'PUWeight*PFJet450Pass', 'div' ),
    #'taus30IsoPassPerJet30CleanByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoChrgPass', 'PUWeight*PFJet450Pass*numJets30Clean', 'div' ),
    #'taus30IsoChrgPassPerJet30CleanByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoChrgPass', 'PUWeight*PFJet450Pass*numJets30Clean', 'div' ),
    #'taus30PerJet30CleanByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*PFJet450Pass*numTausThreeProng30', 'PUWeight*PFJet450Pass*numJets30Clean', 'div' ),

    #'jets30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*PFJet450Pass*numJets30Clean', 'PUWeight*PFJet450Pass', 'div' ),
    #'threeProngTaus30ByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*PFJet450Pass*numTausThreeProng30', 'PUWeight*PFJet450Pass', 'div' ),
    #'threeProngTaus30IsoPassByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoPass', 'PUWeight*PFJet450Pass', 'div' ),
    #'taus30IsoPassPerJet30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*PFJet450Pass*numTausThreeProng30IsoPass', 'PUWeight*PFJet450Pass*numJets30Clean', 'div' ),
    #'taus30PerJet30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*PFJet450Pass*numTausThreeProng30', 'PUWeight*PFJet450Pass*numJets30Clean', 'div' ),

    #''' WithOUT Trigger Matching !!! '''
    #'threeProngTaus30ByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProng30', 'PUWeight', 'div' ),
    #'threeProngTaus30TrigByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProng30*PFJet450Pass', 'PUWeight*PFJet450Pass', 'div' ),
    #'threeProngTaus30IsoPassByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProng30IsoPass', 'PUWeight', 'div' ),
    #'threeProngTaus30IsoChrgPassByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProng30IsoChrgPass', 'PUWeight', 'div' ),
    #'jets30CleanByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numJets30Clean', 'PUWeight', 'div' ),
    #'taus30PerJet30CleanByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProng30', 'PUWeight*numJets30Clean', 'div' ),
    #'taus30IsoPassPerJet30CleanByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProng30IsoPass', 'PUWeight*numJets30Clean', 'div' ),
    #'taus30IsoChrgPassPerJet30CleanByNvtx' : ( 'nvtx', '(35,0,35)', 'PUWeight*numTausThreeProng30IsoChrgPass', 'PUWeight*numJets30Clean', 'div' ),

    #'jets30CleanByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*numJets30Clean', 'PUWeight', 'div' ),
    #'threeProngTaus30ByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*numTausThreeProng30', 'PUWeight', 'div' ),
    #'threeProngTaus30IsoPassByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*numTausThreeProng30IsoPass', 'PUWeight', 'div' ),
    #'threeProngTaus30IsoChrgPassByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*numTausThreeProng30IsoPass', 'PUWeight', 'div' ),
    #'taus30IsoPassPerJet30CleanByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*numTausThreeProng30IsoChrgPass', 'PUWeight*numJets30Clean', 'div' ),
    #'taus30IsoChrgPassPerJet30CleanByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*numTausThreeProng30IsoChrgPass', 'PUWeight*numJets30Clean', 'div' ),
    #'taus30PerJet30CleanByLumi' : ( 'lumi', '(51,0,1700)', 'PUWeight*numTausThreeProng30', 'PUWeight*numJets30Clean', 'div' ),

    #'jets30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*numJets30Clean', 'PUWeight', 'div' ),
    #'threeProngTaus30ByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*numTausThreeProng30', 'PUWeight', 'div' ),
    #'threeProngTaus30IsoPassByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*numTausThreeProng30IsoPass', 'PUWeight', 'div' ),
    #'taus30IsoPassPerJet30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*numTausThreeProng30IsoPass', 'PUWeight*numJets30Clean', 'div' ),
    #'taus30PerJet30CleanByBunchCrossing' : ( 'bunchCrossing', '(35,0,3500)', 'PUWeight*numTausThreeProng30', 'PUWeight*numJets30Clean', 'div' ),

    #'Nvtx' : ( 'nvtx', '(50,0,50)', '1', '1', 'scale' ),
    #'ReweightedNvtx' : ( 'nvtx', '(50,0,50)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByEta' : ( 'Eta', '(30,-3,3)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByPt' : ( 'Pt', '(20,0,200)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByPhi' : ( 'Phi', '(40,-4,4)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByIso' : ( 'Iso', '(20,0,200)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByIsoChrg' : ( 'IsoChrg', '(20,0,200)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByEtaTrig' : ( 'Eta', '(30,-3,3)', 'PUWeight*PFJet450Pass', '1', 'scale' ),
    #'threeProngTausByPtTrig' : ( 'Pt', '(20,0,200)', 'PUWeight*PFJet450Pass', '1', 'scale' ),
    #'threeProngTausByPhiTrig' : ( 'Phi', '(40,-4,4)', 'PUWeight*PFJet450Pass', '1', 'scale' ),
    #'threeProngTausByIsoTrig' : ( 'Iso', '(20,0,200)', 'PUWeight*PFJet450Pass', '1', 'scale' ),
    #'threeProngTausByIsoChrgTrig' : ( 'IsoChrg', '(20,0,200)', 'PUWeight*PFJet450Pass', '1', 'scale' ),
}

runs = {
    254790 : ROOT.kRed,
    254833 : ROOT.kBlue,
    258425 : ROOT.kCyan,
    259721 : ROOT.kGreen
}

def plotter( plot ) :
    print "Starting: %s" % plot
#for plot in plotMap.keys() :
    numEventsPerRun = {}
    hists = {}
    jhists = {}
    hists2 = {}
    jhists2 = {}
    for run in runs.keys() :
        info = plotMap[plot][1].strip('(').strip(')').split(',')
        #print info
        numB = int(info[0])
        first = int(info[1])
        last = int(info[2])
        hists[ run ] = ROOT.TH1F( '%i' % run, '%i' % run, numB, first, last)
        jhists[ run ] = ROOT.TH1F( 'j%i' % run, 'j%i' % run, numB, first, last)
        hists2[ run ] = ROOT.TH1F( '2_%i' % run, '2_%i' % run, numB, first, last)
        jhists2[ run ] = ROOT.TH1F( 'j2_%i' % run, 'j2_%i' % run, numB, first, last)
        
    
    for run in runs.keys() :
        print "Run: %i" % run
        f = ROOT.TFile('%i/%i.root' % (run, run),'r')
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
    for iRun in numEventsPerRun :
        print "RUN: %i  Evt Stuff:" % iRun, numEventsPerRun[iRun]
                
            
   
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
numCores = 23
pool = multiprocessing.Pool(processes = numCores )
multiprocessingOutputs = []
for plot in plotMap.keys() :
    multiprocessingOutputs.append( pool.apply_async(plotter, args=( '%s' % plot, ) ) )

mpResults = [p.get() for p in multiprocessingOutputs]
mpResults.sort()
for item in mpResults :
    print item
print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
