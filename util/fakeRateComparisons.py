
import ROOT
ROOT.gROOT.SetBatch(True)


#n0 = 'data/azhFakeRateFits_Nominal.root'
#n0 = '/afs/cern.ch/work/t/truggles/Z_to_tautau/RT/CMSSW_8_0_26_patch1/src/newTrig_ZH_13TeV/data/azhFakeRateFits4.root'
n0 = '/afs/cern.ch/work/t/truggles/Z_to_tautau/RT/CMSSW_8_0_26_patch1/src/newTrig_ZH_13TeV/redBkgValidation/azhFakeRateFits_alignedDefs.root'

baseDir = '/afs/cern.ch/work/t/truggles/Z_to_tautau/RT/CMSSW_8_0_26_patch1/src/newTrig_ZH_13TeV/redBkgValidation/WH_nom/'
n1 = 'eFR_data.root'
n2 = 'muFR_data.root'
n3 = 'tauFR_data.root'
baseDirX = '/afs/cern.ch/work/t/truggles/Z_to_tautau/RT/CMSSW_8_0_26_patch1/src/newTrig_ZH_13TeV/redBkgValidation/WH_1jetPlus/'

f0 = ROOT.TFile( n0, 'r' )
f1 = ROOT.TFile( baseDir+n1, 'r' )
f1x = ROOT.TFile( baseDirX+n1, 'r' )
f2 = ROOT.TFile( baseDir+n2, 'r' )
f2x = ROOT.TFile( baseDirX+n2, 'r' )
#f2 = ROOT.TFile( '/afs/cern.ch/work/c/ccaillol/public/FitHistograms_muFR_looseID_ido0p25.root', 'r' )
f3 = ROOT.TFile( baseDir+n3, 'r' )
f3x = ROOT.TFile( baseDirX+n3, 'r' )

e1 = f1.Get('efr_numerator_efr_denominator')
e1x = f1x.Get('efr_numerator_efr_denominator')
m1 = f2.Get('mufr_numerator_mufr_denominator')
m1x = f2x.Get('mufr_numerator_mufr_denominator')

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
cdm0x = f3x.Get('hpt_dm0_medium_hpt_dm0_veryloose')
cdm1x = f3x.Get('hpt_dm1_medium_hpt_dm1_veryloose')
cdm10x = f3x.Get('hpt_dm10_medium_hpt_dm10_veryloose')

c = ROOT.TCanvas('c1','c1',600,600)

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
    
    c.SaveAs( '/afs/cern.ch/user/t/truggles/www/vhFRComp_align_april20/'+name+'.png')
    c.SaveAs( '/afs/cern.ch/user/t/truggles/www/vhFRComp_align_april20/'+name+'.pdf')
    del p

def makePlot3( c, g1, g2, g3, name, maxi ) :
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
    g3.SetLineColor( ROOT.kGreen+2 )
    g3.SetMarkerColor( ROOT.kGreen+2 )
    g3.SetLineWidth( 3 )
    
    g1.SetMinimum( 0.0 )
    g1.SetMaximum( maxi )
    g1.GetYaxis().SetTitleOffset( 1.7 )
    p.SetLeftMargin( .15 )
    
    
    g1.Draw()
    g2.Draw('SAME')
    g3.Draw('SAME')

    legend = ROOT.TLegend(0.5, 0.6, 0.9, 0.85)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    legend.AddEntry( g1, 'ZH Fake Rate', 'lep')
    legend.AddEntry( g2, 'WH Fake Rate: inclusive', 'lep')
    legend.AddEntry( g3, 'WH Fake Rate: nJets >= 1', 'lep')
    legend.Draw()
    
    logo = ROOT.TText(.2, .88,"CMS Preliminary")
    logo.SetTextSize(0.04)
    logo.DrawTextNDC(.2, .85,"CMS Preliminary")
    
    c.SaveAs( '/afs/cern.ch/user/t/truggles/www/vhFRComp_align_april20/'+name+'.png')
    c.SaveAs( '/afs/cern.ch/user/t/truggles/www/vhFRComp_align_april20/'+name+'.pdf')
    del p

makePlot3( c, e2, e1, e1x, 'Electron', 0.015 )
makePlot3( c, m2, m1, m1x, 'Muon', 0.05 )
makePlot3( c, tdm0, cdm0, cdm0x, 'Tau-DM0', 0.7 )
makePlot3( c, tdm1, cdm1, cdm1x, 'Tau-DM1', 0.7 )
makePlot3( c, tdm10, cdm10, cdm10x, 'Tau-DM10', 0.7 )


