import ROOT

f = ROOT.TFile('ntuplize.root','r')
#f = ROOT.TFile('svFitTester.root','r')
t = f.Get('em/final/Ntuple')

for row in t :
    evt = row.evt
    lumi = row.lumi
    run = row.run
    mvamet = row.mvaMetEt
    mvametphi = row.mvaMetPhi
    print evt,":",lumi,":",run,":",mvamet,":",mvametphi
