import ROOT
from time import gmtime, strftime
from ROOT import gPad
import pyplotter.tdrstyle as tdr

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()
numT = 6
numJ = 8

def finishPlots( histos, plot, plotMap, run, name ) :
    c1 = ROOT.TCanvas(plot,plot,400,400)
    p1 = ROOT.TPad('p_%s' % plot,'p_%s' % plot,0,0,1,1)
    p1.Draw()
    p1.cd()

    histos[259721].Draw('hist e0')
    histos[254833].Draw('hist same e0')
    histos[254790].Draw('hist same e0')
    histos[258425].Draw('hist same e0')
   
    maxi = 0
    for run in runs :
        #print histos[run].GetMaximum()
        histos[run].SetLineColor( runs[ run ] )
        histos[run].SetLineWidth( 2 )
        if histos[run].GetMaximum() > maxi : maxi = histos[run].GetMaximum()
    histos[259721].SetMaximum( maxi * 1.5 )
    histos[259721].GetXaxis().SetTitle( '%s' % plotMap[plot][0] )
    p1.SetTitle( '%s' % plot.replace('By',' vs. ') )
    c1.SetTitle( '%s' % plot.replace('By',' vs. ') )
    if 'threeProng' in name : yaxis = 'Taus / Event'
    elif 'taus' in name : yaxis = 'Taus / Jet'
    elif 'jets' in name and not 'taus' : yaxis = 'Jets / Event'
    else : yaxis = name
    histos[259721].GetYaxis().SetTitle( yaxis )

    logo = ROOT.TText(.2, .88,"CMS Preliminary")
    logo.SetTextSize(0.03)
    logo.DrawTextNDC(.2, .89,"CMS Preliminary")

    lumi = ROOT.TText(.7,1.05,"(13 TeV)")
    lumi.SetTextSize(0.035)
    lumi.DrawTextNDC(.4,.96,"%s   (13 TeV)" % plot.replace('By',' vs. ') )
 
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
    'threeProngTausByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numTausThreeProng', 'PUWeight', 'div' ),
    'threeProngTaus30ByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numTausThreeProng30', 'PUWeight', 'div' ),
    'threeProngTausIsoPassByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numTausThreeProngIsoPass', 'PUWeight', 'div' ),
    'threeProngTaus30IsoPassByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numTausThreeProng30IsoPass', 'PUWeight', 'div' ),
    'jets20ByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numJets20', 'PUWeight', 'div' ),
    'jets30CleanByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numJets30Clean', 'PUWeight', 'div' ),
    'tausPerJetByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numTausThreeProng', 'PUWeight*numJets20', 'div' ),
    'taus30PerJet30CleanByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numTausThreeProng30', 'PUWeight*numJets30Clean', 'div' ),
    'taus20IsoPassPerJet20ByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numTausThreeProngIsoPass', 'PUWeight*numJets20', 'div' ),
    'taus30IsoPassPerJet30CleanByNvtx' : ( 'nvtx', '(25,0,25)', 'PUWeight*numTausThreeProng30IsoPass', 'PUWeight*numJets30Clean', 'div' ),
    'Nvtx' : ( 'nvtx', '(50,0,50)', '1', '1', 'scale' ),
    'ReweightedNvtx' : ( 'nvtx', '(50,0,50)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByEta' : ( 'Eta', '(30,-3,3)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByPt' : ( 'Pt', '(20,0,200)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByPhi' : ( 'Phi', '(40,-4,4)', 'PUWeight', '1', 'scale' ),
    #'threeProngTausByBunchCrossing' : ( 'bunchCrossing', '(350,0,3500)', 'PUWeight', '1', 'scale' ),
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
        if plotMap[plot][0] == 'nvtx' :
            getHist( hists, run, tree, '%s>>hist%i%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][2], run), 'hist%i' % run, run )
            getHist( hists2, run, tree, '%s>>hist2%i%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][3], run), 'hist2%i' % run, run )

            if 'div' in plotMap[plot][4] :
                hists[ run ].Divide( hists2[ run ] )
            if 'scale' in plotMap[plot][4] :
                hists[ run ].Scale( 1 / hists[ run ].Integral() )


        if plotMap[plot][0] != 'nvtx' :
            var_ = plotMap[plot][0]
            cnt = 0
            for row in tree :
                cnt += 1
                #if cnt > 1000 : continue
                for i in range(1, numT + 1) :
                    inVar = 't_%s' % var_
                    newVar = inVar.replace('_',str(i))
                    if plotMap[plot][0] == 'bunchCrossing' :
                        newVar = 'bunchCrossing'
                    if plotMap[plot][0] == 'Pt' :
                        inVar = 't_Jet%s' % var_
                        newVar = inVar.replace('_',str(i))
                    hists[ run ].Fill( getattr(row, newVar), row.PUWeight )
                    hists2[ run ].Fill( getattr(row, newVar) )
                for j in range(1, numJ + 1) :
                    inVar = 'j_%s' % var_
                    newVar = inVar.replace('_',str(j))
                    if plotMap[plot][0] == 'bunchCrossing' :
                        newVar = 'bunchCrossing'
                    jhists[ run ].Fill( getattr(row, newVar), row.PUWeight )
                    jhists2[ run ].Fill( getattr( row, newVar) )
                
            

                
            
            #thists = {}
            #thists2 = {}
            #jhists = {}
            #jhists2 = {}


            #if 'threeProngTausBy' in plot :
            #    for i in range(1, numT + 1) :
            #        #print "tau",i
            #        thists[ '%itau%i' % (run, i) ] = ROOT.TH1F()
            #        thists2[ '2%itau%i' % (run, i) ] = ROOT.TH1F()
            #        getHist( thists, '%itau%i' % (run, i), tree, 't%i%s>>th%i%s%s' % (i, plotMap[plot][0], i, plotMap[plot][0], plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][2], run), 'th%i%s' % (i, plotMap[plot][0]), run )
            #        hists[ run ].Add( thists[ '%itau%i' % (run, i) ] )
            #    #if 'div' in plotMap[plot][4] :
            #    #    for i in range(1, numT + 1) :
            #    #        getHist( thists2, '2%itau%i' % (run, i), tree, 't%i%s>>th%i%s%s' % (i, plotMap[plot][0], i, plotMap[plot][0], plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][3], run), 'th%i%s' % (i, plotMap[plot][0]), run )
            #    #    hists2[ run ].Add( thists2[ '2%itau%i' % (run, i) ] )
            #    #    hists[ run ].Divide( hists2[ run ] )

            #        

            #if plot == 'jets20ByEta' :
            #    for i in range(1, numJ + 1) :
            #        #print "Jet %i" % i
            #        jhists[ '%ijet%i' % (run, i) ] = ROOT.TH1F()
            #        jhists2[ '2%ijet%i' % (run, i) ] = ROOT.TH1F()
            #        getHist( jhists, '%ijet%i' % (run, i), tree, 'j%i%s>>jh%i%s%s' % (i, plotMap[plot][0], i, plotMap[plot][0], plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][3], run), 'jh%i%s' % (i, plotMap[plot][0]), run )
            #        hists[ run ].Add( jhists[ '%ijet%i' % (run, i) ] )
            #if 'scale' in plotMap[plot][4] :
            #    hists[ run ].Scale( 1 / hists[ run ].Integral() )
    
        
    
        #hists[run].SetLineColor( runs[ run ] )
        #hists[run].SetLineWidth( 2 )
    
   
    if plotMap[plot][0] == 'nvtx' :
        name = plot
        finishPlots( hists, plot, plotMap, runs, name )
    else :
        name = 'tmp2/%s_tau' % plot
        finishPlots( hists, plot, plotMap, runs, name )
        name = 'tmp2/%s_tau2' % plot
        finishPlots( hists2, plot, plotMap, runs, name )
        name = 'tmp2/%s_jet' % plot
        finishPlots( jhists, plot, plotMap, runs, name )
        name = 'tmp2/%s_jet2' % plot
        finishPlots( jhists2, plot, plotMap, runs, name )
        for run in runs :
            hists[ run ].Divide( jhists[ run ] )
            hists[ run ].Scale( 1 / hists[ run ].Integral() )
        name = 'tmp2/%s_tauPerJet' % plot
        finishPlots( hists, plot, plotMap, runs, name )
    return "Finished Plotting %s" % plot
        

        
#    c1 = ROOT.TCanvas(plot,plot,400,400)
#    p1 = ROOT.TPad('p_%s' % plot,'p_%s' % plot,0,0,1,1)
#    p1.Draw()
#    p1.cd()
#
#    histos[259721].Draw('hist e0')
#    histos[254833].Draw('hist same e0')
#    histos[254790].Draw('hist same e0')
#    histos[258425].Draw('hist same e0')
#    
#    maxi = 0
#    for run in runs :
#        if histos[run].GetMaximum() > maxi : maxi = histos[run].GetMaximum()
#    histos[259721].SetMaximum( maxi * 1.5 )
#    histos[259721].GetXaxis().SetTitle( '%s' % plotMap[plot][0] )
#    histos[259721].GetYaxis().SetTitle( '%s' % plot )
#
#    
#    p1.BuildLegend( .65, .73, .95, .95 )
#    p1.Update()
#    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/%s.png' % plot )
    

import multiprocessing
## Enable multiprocessing
numCores = 10
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
