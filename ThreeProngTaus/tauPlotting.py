import ROOT
from time import gmtime, strftime
from ROOT import gPad
import pyplotter.tdrstyle as tdr

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()
numT = 10
numJ = 12

''' timing... '''
begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "\nStart Time: %s" % str( begin )

plotMap = {
    'threeProngTausByNvtx' : ( 'nvtx', '(40,0,40)', 'PUWeight*numTausThreeProng', 'PUWeight', 'div' ),
    'jets20ByNvtx' : ( 'nvtx', '(40,0,40)', 'PUWeight*numJets20', 'PUWeight', 'div' ),
    'tausPerJetByNvtx' : ( 'nvtx', '(40,0,40)', 'PUWeight*numTausThreeProng', 'PUWeight*numJets20', 'div' ),
    'Nvtx' : ( 'nvtx', '(50,0,50)', '1', '1', 'scale' ),
    'ReweightedNvtx' : ( 'nvtx', '(50,0,50)', 'PUWeight', '1', 'scale' ),
    #'jets20ByEta' : ( 'Eta', '(30,-3,3)', 'PUWeight', '1', 'div' )
}

runs = {
    254790 : ROOT.kRed,
    254833 : ROOT.kBlue,
    258425 : ROOT.kCyan,
    259721 : ROOT.kGreen
}

def getHist( histDict, tree, fill, weight, newHist, run ) :
    print fill
    print weight
    print newHist
    tree.Draw( fill, weight )
    histDict[ run ] = gPad.GetPrimitive( newHist )
    histDict[ run ].SetDirectory( 0 )
    histDict[ run ].SetTitle( str(run) )
    histDict[ run ].Sumw2()
    
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
        if plotMap[plot][0] == 'nvtx' :
            getHist( hists, tree, '%s>>hist%i%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][2], run), 'hist%i' % run, run )
            getHist( hists2, tree, '%s>>hist2%i%s' % (plotMap[plot][0], run, plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][3], run), 'hist2%i' % run, run )

            if 'div' in plotMap[plot][4] :
                hists[ run ].Divide( hists2[ run ] )
            if 'scale' in plotMap[plot][4] :
                hists[ run ].Scale( 1 / hists[ run ].Integral() )
        #if plotMap[plot][0] != 'nvtx' :
        #    thists = {}
        #    jhists = {}
        #    for i in range(1, numT + 1) :
        #        thists[ '%itau%i' % (run, i) ] = ROOT.TH1F()
        #    for i in range(1, numJ + 1) :
        #        jhists[ '%ijet%i' % (run, i) ] = ROOT.TH1F()
        
    
        
    
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
