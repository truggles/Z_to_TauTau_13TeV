import ROOT
from time import gmtime, strftime
from ROOT import gPad
import pyplotter.tdrstyle as tdr

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

''' timing... '''
begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "\nStart Time: %s" % str( begin )

plotMap = {
    'threeProngTausByNvtx' : ( 'nvtx', '(40,0,40)', 'PUWeight*numTausThreeProng', 'PUWeight', 'div' ),
    'jets20ByNvtx' : ( 'nvtx', '(40,0,40)', 'PUWeight*numJets20', 'PUWeight', 'div' ),
    'tausPerJetByNvtx' : ( 'nvtx', '(40,0,40)', 'PUWeight*numTausThreeProng', 'PUWeight*numJets20', 'div' ),
    'Nvtx' : ( 'nvtx', '(50,0,50)', '1', '1', 'scale' ),
    'ReweightedNvtx' : ( 'nvtx', '(50,0,50)', 'PUWeight', '1', 'scale' ),
}

runs = {
    254790 : ROOT.kRed,
    254833 : ROOT.kBlue,
    258425 : ROOT.kCyan,
    259721 : ROOT.kGreen
}

for plot in plotMap.keys() :
    hists = {}
    hists2 = {}
    for run in runs.keys() :
        hists[ run ] = ROOT.TH1F()
        hists2[ run ] = ROOT.TH1F()
        
    c1 = ROOT.TCanvas('c1','c1',400,400)
    p1 = ROOT.TPad('p1','p1',0,0,1,1)
    p1.Draw()
    p1.cd()
    
    for run in runs.keys() :
        print "Run: %i" % run
        f = ROOT.TFile('%i/%i.root' % (run, run),'r')
        tree = f.Get('tauEvents/Ntuple')
        #totalEntries = tree.GetEntries()
        #print totalEntries
        tree.Draw( '%s>>hist%i%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][2], run) )
        hists[ run ] = gPad.GetPrimitive( 'hist%i' % run )
        hists[ run ].SetDirectory( 0 )
        hists[ run ].SetTitle( str(run) )
        hists[ run ].Sumw2()
    
        tree.Draw( '%s>>hist2%i%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][3], run) )
        hists2[ run ] = gPad.GetPrimitive( 'hist2%i' % run )
        hists2[ run ].SetDirectory( 0 )
        hists2[ run ].Sumw2()
        if 'div' in plotMap[plot][4] :
            hists[ run ].Divide( hists2[ run ] )
        if 'scale' in plotMap[plot][4] :
            hists[ run ].Scale( 1 / hists[ run ].Integral() )
    
        
    
        
        #for row in tree :
        #    try :
        #        hist.Fill( row.nvtx, (row.numTausThreeProng * row.PUWeight) )
        #    except :
        #        print "ERROR: nvtx: %f       numTaus3P: %f       PUWeight: %f" % (row.nvtx, row.numTausThreeProng, row.PUWeight)
    
    
        #hists[run].Scale( 1 / hists[run].Integral() )
        hists[run].SetLineColor( runs[ run ] )
        hists[run].SetLineWidth( 2 )
    
    
    hists[259721].Draw('hist e0')
    hists[254833].Draw('hist same e0')
    hists[254790].Draw('hist same e0')
    hists[258425].Draw('hist same e0')
    
    maxi = 0
    for run in runs :
        if hists[run].GetMaximum() > maxi : maxi = hists[run].GetMaximum()
    hists[259721].SetMaximum( maxi * 1.2 )
    hists[259721].GetXaxis().SetTitle( '%s' % plotMap[plot][0] )
    hists[259721].GetYaxis().SetTitle( '%s' % plot )

    
    p1.BuildLegend()
    p1.Update()
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/ReweightedNvtx.png')
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/%s.png' % plot )
    


print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
