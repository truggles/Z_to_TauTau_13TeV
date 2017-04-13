#
# Quick script to print gen acceptance yields based off of FSA ntuples for
# different Pt thresholds

import ROOT

#f = ROOT.TFile('ggH125.root','r')
f = ROOT.TFile('vbf125.root','r')
t = f.Get('tt/final/Ntuple')

h1 = ROOT.TH1F('h1','h1',100,0,10000)


for pt1 in [35, 40, 45, 50] :
    for pt2 in [35, 40, 45, 50] :
        cut = "t1ZTTGenMatching == 5 && t2ZTTGenMatching == 5 && abs(t1ZTTGenEta) < 2.1 && abs(t2ZTTGenEta) < 2.1 && t1ZTTGenPt > %i && t2ZTTGenPt > %i" % (pt1, pt2)

        t.Draw("t1ZTTGenPt >> h1",cut)
        print "Pt1: %i Pt2: %i   ===>>> Event Yield: %i" % (pt1, pt2, h1.Integral())
