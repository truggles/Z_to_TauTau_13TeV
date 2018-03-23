
import ROOT
ROOT.gROOT.SetBatch(True)


#n0 = 'data/azhFakeRateFits_Nominal.root'
n0 = '/afs/cern.ch/work/t/truggles/Z_to_tautau/RT/CMSSW_8_0_26_patch1/src/newTrig_ZH_13TeV/data/azhFakeRateFits4.root'

baseDir = '/afs/cern.ch/work/c/ccaillol/public/WHFR/'
n1 = 'eFR_data.root'
n2 = 'muFR_data.root'
n3 = 'tauFR_data.root'

f0 = ROOT.TFile( n0, 'r' )
f1 = ROOT.TFile( baseDir+n1, 'r' )
#f2 = ROOT.TFile( baseDir+n2, 'r' )
f2 = ROOT.TFile( '/afs/cern.ch/work/c/ccaillol/public/FitHistograms_muFR_looseID_ido0p25.root', 'r' )
f3 = ROOT.TFile( baseDir+n3, 'r' )

e1 = f1.Get('efr_numerator_efr_denominator')
m1 = f2.Get('mufr_numerator_mufr_denominator')
m2 = f0.Get('muon_AllEta_leptonPt_graph')
e2 = f0.Get('electron_AllEta_leptonPt_graph')

#t1 = f3.Get('hpt_dm0_tight_hpt_dm0_veryloose')
#t1 = f3.Get('hpt_dm1_tight_hpt_dm1_veryloose')
#t1 = f3.Get('hpt_dm10_tight_hpt_dm10_veryloose')
#t1 = f3.Get('hpt_dm0_verytight_hpt_dm0_veryloose')
#t1 = f3.Get('hpt_dm1_verytight_hpt_dm1_veryloose')
#t1 = f3.Get('hpt_dm10_verytight_hpt_dm10_veryloose')

#t1 = f0.Get('tau-DM10_lllt_AllEta_leptonPt_graph')
#t1 = f0.Get('tau-DM0_lllt_AllEta_leptonPt_graph')
#t1 = f0.Get('tau-DM1_lllt_AllEta_leptonPt_graph')
tdm1 = f0.Get('tau-DM1_lltt_AllEta_leptonPt_graph')
tdm10 = f0.Get('tau-DM10_lltt_AllEta_leptonPt_graph')
tdm0 = f0.Get('tau-DM0_lltt_AllEta_leptonPt_graph')

cdm0 = f3.Get('hpt_dm0_medium_hpt_dm0_veryloose')
cdm1 = f3.Get('hpt_dm1_medium_hpt_dm1_veryloose')
cdm10 = f3.Get('hpt_dm10_medium_hpt_dm10_veryloose')

c = ROOT.TCanvas('c1','c1',500,500)

def makePlot( c, g1, g2, name, maxi ) :
    p = ROOT.TPad('p1','p1',0,0,1,1)
    p.Draw()
    p.cd()
    g1.SetTitle(name+' Fake Rate')
    g1.SetLineColor( ROOT.kRed )
    g1.SetMarkerColor( ROOT.kRed )
    g1.SetLineWidth( 3 )
    g2.SetLineColor( ROOT.kBlue )
    g2.SetMarkerColor( ROOT.kBlue )
    g2.SetLineWidth( 3 )
    
    g1.SetMinimum( 0.0 )
    g1.SetMaximum( maxi )
    g1.GetYaxis().SetTitleOffset( 1.7 )
    p.SetLeftMargin( .15 )
    
    
    g1.Draw()
    g2.Draw('SAME')

    legend = ROOT.TLegend(0.5, 0.6, 0.9, 0.85)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    legend.AddEntry( g1, 'ZH Fake Rate', 'lep')
    legend.AddEntry( g2, 'WH Fake Rate', 'lep')
    legend.Draw()
    
    logo = ROOT.TText(.2, .88,"CMS Preliminary")
    logo.SetTextSize(0.04)
    logo.DrawTextNDC(.2, .85,"CMS Preliminary")
    
    c.SaveAs( '/afs/cern.ch/user/t/truggles/www/vhFRComp_align_defs4/'+name+'.png')
    c.SaveAs( '/afs/cern.ch/user/t/truggles/www/vhFRComp_align_defs2/'+name+'.pdf')
    del p

makePlot( c, e2, e1, 'Electron', 0.015 )
makePlot( c, m2, m1, 'Muon', 0.05 )
makePlot( c, tdm0, cdm0, 'Tau-DM0', 0.7 )
makePlot( c, tdm1, cdm1, 'Tau-DM1', 0.7 )
makePlot( c, tdm10, cdm10, 'Tau-DM10', 0.7 )


