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
    #'threeProngTausByEta' : ( 'Eta', '(30,-3,3)', 'PUWeight', '1', 'scale' ),
    #'jets20ByEta' : ( 'Eta', '(30,-3,3)', 'PUWeight', '1', 'scale' ),
}

runs = {
    254790 : ROOT.kRed,
    254833 : ROOT.kBlue,
    258425 : ROOT.kCyan,
    259721 : ROOT.kGreen
}

def getHist( histDict, key, tree, fill, weight, histName, run ) :
    #print fill
    #print weight
    #print histName
    tree.Draw( fill, weight )
    histDict[ key ] = gPad.GetPrimitive( histName )
    histDict[ key ].SetDirectory( 0 )
    histDict[ key ].SetTitle( str(run) )
    histDict[ key ].Sumw2()
    
for plot in plotMap.keys() :
    hists = {}
    hists2 = {}
    for run in runs.keys() :
        info = plotMap[plot][1].strip('(').strip(')').split(',')
        #print info
        numB = int(info[0])
        first = int(info[1])
        last = int(info[2])
        hists[ run ] = ROOT.TH1F( '%i' % run, '%i' % run, numB, first, last)
        hists2[ run ] = ROOT.TH1F( '2_%i' % run, '2_%i' % run, numB, first, last)
        
    c1 = ROOT.TCanvas(plot,plot,400,400)
    p1 = ROOT.TPad('p_%s' % plot,'p_%s' % plot,0,0,1,1)
    p1.Draw()
    p1.cd()
    
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
            thists = {}
            jhists = {}


            if plot == 'threeProngTausByEta' :
                for i in range(1, numT + 1) :
                    #print "tau",i
                    thists[ '%itau%i' % (run, i) ] = ROOT.TH1F()
                    getHist( thists, '%itau%i' % (run, i), tree, 't%i%s>>th%i%s%s' % (i, plotMap[plot][0], i, plotMap[plot][0], plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][3], run), 'th%i%s' % (i, plotMap[plot][0]), run )
                    hists[ run ].Add( thists[ '%itau%i' % (run, i) ] )


            if plot == 'jets20ByEta' :
                for i in range(1, numJ + 1) :
                    #print "Jet %i" % i
                    jhists[ '%ijet%i' % (run, i) ] = ROOT.TH1F()
                    getHist( jhists, '%ijet%i' % (run, i), tree, 'j%i%s>>jh%i%s%s' % (i, plotMap[plot][0], i, plotMap[plot][0], plotMap[plot][1]), '%s*(run == %i)' % (plotMap[plot][3], run), 'jh%i%s' % (i, plotMap[plot][0]), run )
                    hists[ run ].Add( jhists[ '%ijet%i' % (run, i) ] )
            if 'scale' in plotMap[plot][4] :
                hists[ run ].Scale( 1 / hists[ run ].Integral() )
    
        
    
        hists[run].SetLineColor( runs[ run ] )
        hists[run].SetLineWidth( 2 )
    
    
    hists[259721].Draw('hist e0')
    hists[254833].Draw('hist same e0')
    hists[254790].Draw('hist same e0')
    hists[258425].Draw('hist same e0')
    
    maxi = 0
    for run in runs :
        if hists[run].GetMaximum() > maxi : maxi = hists[run].GetMaximum()
    hists[259721].SetMaximum( maxi * 1.5 )
    hists[259721].GetXaxis().SetTitle( '%s' % plotMap[plot][0] )
    hists[259721].GetYaxis().SetTitle( '%s' % plot )

    
    p1.BuildLegend( .65, .73, .95, .95, plot )
    p1.Update()
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/%s.png' % plot )
    


print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
