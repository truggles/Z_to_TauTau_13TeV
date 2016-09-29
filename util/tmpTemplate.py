import ROOT

fileName = 'xxx.root'
treePath = 'Ntuple'
pngName = 'xxx'
var = 'pt_1'
cut = ''

d1 = False
d1xAxis = 'x axis'
d1yAxis = 'y axis'

d2 = False
d2xAxis = 'x axis'
d2yAxis = 'y axis'




f = ROOT.TFile(fileName,'r')
t = f.Get(treePath)
c = ROOT.TCanvas('c','c',600,600)

if d1 :
    h = ROOT.TH1D('h1','h1',150,0,150)
    h.GetXaxis().SetTitle(d1xAxis)
    h.GetYaxis().SetTitle(d1yAxis)
    t.Draw(var+' >> h1', cut)

if d2 :
    h = ROOT.TH2D('h2','h2',150,0,150,100,0,1)
    h.GetXaxis().SetTitle(d2xAxis)
    h.GetYaxis().SetTitle(d2yAxis)
    t.Draw(var+' >> h2', cut)

c.SaveAs('/afs/cern.ch/user/t/truggles/www/tmp/'+pngName+'.png')
