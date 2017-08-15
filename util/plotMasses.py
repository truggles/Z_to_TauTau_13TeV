import ROOT
from collections import OrderedDict
ROOT.gROOT.SetBatch(True)

def mass( n1, name ) :
    f = ROOT.TFile( n1, 'r' )
    print f
    
    c = ROOT.TCanvas('c1','c1',1200,800)
    p = ROOT.TPad('p1','p1',0,0,1,1)
    p.Draw()
    p.cd()
    
    hists = OrderedDict()

    if name == 'mssm' :
        masses = [220, 240, 260, 280, 300, 320, 340, 350, 400]
        base = 'azh'
    if name == 'sm_higgs' :
        #masses = [110, 120, 125, 130, 140]
        masses = [120, 130,]
        #masses = [110, 125, 140]
        base = 'ZH'
    
    maxi = 0
    for mass in masses :
        h = f.Get('eett_inclusive/%s%i' % (base, mass) )
        #h.SetName( mass )
        #h.SetTitle( mass )
        hists[mass] = h
        hists[mass].Scale( 1. / hists[mass].Integral() )
        if hists[mass].GetMaximum() > maxi :
            maxi = hists[mass].GetMaximum()
    
    i = 0
    for mass in masses :
        i = i + 1
        hists[mass].SetLineWidth( 3 )
        hists[mass].SetLineColor( i )
        hists[mass].SetMarkerColor( i )
        if mass == 220 :
            hists[mass].SetMaximum( maxi * 1.2 )
            hists[mass].Draw('HIST 1e')
        else :
            hists[mass].Draw('SAME HIST 1e')

    p.BuildLegend()
        
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/mass_%s.png' % name)


n1 = 'shapes/azh/htt_zh.inputs-mssm-13TeV_AMass_LT20.root'
n2 = 'shapes/azh/htt_zh.inputs-sm-13TeV_svFitMass_LT20.root'

mass( n1, 'mssm' )
mass( n2, 'sm_higgs' )





