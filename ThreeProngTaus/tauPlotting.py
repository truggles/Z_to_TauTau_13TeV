import ROOT
from time import gmtime, strftime
from ROOT import gPad
import pyplotter.tdrstyle as tdr

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

''' timing... '''
begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "\nStart Time: %s" % str( begin )


runs = {
    254790 : ROOT.kRed,
    254833 : ROOT.kBlue,
    258425 : ROOT.kCyan,
    259721 : ROOT.kGreen
}

hists = {}
nvtxhists = {}
for run in runs.keys() :
    hists[ run ] = ROOT.TH1F('hist%i' % run, 'hist%i' % run, 60, 0, 60)
    nvtxhists[ run ] = ROOT.TH1F('histnvtx%i' % run, 'histnvtx%i' % run, 60, 0, 60)
    
c1 = ROOT.TCanvas('c1','c1',600,600)
p1 = ROOT.TPad('p1','p1',0,0,1,1)
p1.Draw()
p1.cd()

for run in runs.keys() :
    print "Run: %i" % run
    f = ROOT.TFile('%i/%i.root' % (run, run),'r')
    tree = f.Get('tauEvents/Ntuple')
    totalEntries = tree.GetEntries()
    print totalEntries
    tree.Draw( 'nvtx>>hist%i(40,0,40)' % run, 'PUWeight*(run == %i)' % run )
    hists[ run ] = gPad.GetPrimitive( 'hist%i' % run )
    hists[ run ].SetDirectory( 0 )

    #@@@ About to normalize the above hist by the bin count in the below hist!!! #Do it!
    #tree.Draw( 'nvtx>>histnvtx%i' % run, )
    #nvtxhists[ run ] = gPad.GetPrimitive( 'histnvtx%i' % run )

    

    
    #for row in tree :
    #    try :
    #        hist.Fill( row.nvtx, (row.numTausThreeProng * row.PUWeight) )
    #    except :
    #        print "ERROR: nvtx: %f       numTaus3P: %f       PUWeight: %f" % (row.nvtx, row.numTausThreeProng, row.PUWeight)
    hists[run].Scale( 1 / hists[run].Integral() )
    hists[run].SetLineColor( runs[ run ] )
    hists[run].SetLineWidth( 2 )


hists[259721].Draw('hist')
hists[254833].Draw('hist same')
hists[254790].Draw('hist same')
hists[258425].Draw('hist same')
    
p1.BuildLegend()
p1.Update()
c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/ReweightedNvtx.png')
    


print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
