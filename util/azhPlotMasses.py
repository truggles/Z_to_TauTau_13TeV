import ROOT
from collections import OrderedDict
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def buildLegend( items, names ) :
    legend = ROOT.TLegend(0.62, 0.42, 0.85, 0.88)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for item, name in zip(items, names) : #range(0, stack.GetStack().GetLast() + 1) :
        legend.AddEntry( item, name, 'lep')
    return legend

def mass( name ) :
    
    c = ROOT.TCanvas('c1','c1',1200,800)
    p = ROOT.TPad('p1','p1',0,0,1,1)
    p.Draw()
    p.cd()
    
    hists = OrderedDict()

    masses = [220, 240, 260, 280, 300, 320, 350, 400]
    base = 'azh'
    cutMap = {
        220 : "genMass < 300",
        240 : "genMass < 310",
        260 : "genMass < 320",
        280 : "genMass < 9999",
        300 : "genMass < 9999",
        320 : "genMass < 9999",
        350 : "genMass < 9999",
        400 : "genMass < 9999",
    }
    
    maxi = 0
    for mass in masses :
        f = ROOT.TFile( 'azh%i.root' % mass, 'r' )
        print mass
        t = f.Get('genMass/events/Ntuple')
        h_tmp = ROOT.TH1F( '%s_tmp' % mass, 'A_Gen_Mass %s' % mass, 100, 150, 6000 )
        t.Draw( 'genMass >> %s_tmp' % mass )
        hists[mass] = ROOT.TH1F( '%s' % mass, 'A_Gen_Mass %s' % mass, 100, 150, 600 )
        #t.Draw( 'genMass >> %s' % mass, cutMap[ mass ] )
        t.Draw( 'genMass >> %s' % mass )
        print "Yields: all - %i    cut - %i   SF = %f" % (h_tmp.Integral(), hists[mass].Integral(), hists[mass].Integral() / h_tmp.Integral())
        hists[mass].SetDirectory(0)
        hists[mass].Scale( 1. / hists[mass].Integral() )
        if hists[mass].GetMaximum() > maxi :
            maxi = hists[mass].GetMaximum()
    
    legItems = []
    legNames = []
    i = 0
    for mass in masses :
        i = i + 1
        if i == 5 : i += 1
        #print mass
        #print hists[mass]
        hists[mass].SetLineWidth( 3 )
        hists[mass].SetLineColor( i )
        hists[mass].SetMarkerColor( i )
        hists[mass].GetXaxis().SetTitle( 'm_{A} [GeV]' )
        hists[mass].GetYaxis().SetTitle( 'A.U.' )
        hists[mass].SetTitle( '' )
        legItems.append( hists[mass] )
        legNames.append( 'AZh, m_{A} = %i GeV' % mass )
        if mass == 220 :
            hists[mass].SetMaximum( maxi * 1.2 )
            #hists[mass].Draw('HIST 1e')
            hists[mass].Draw('HIST')
        else :
            #hists[mass].Draw('SAME HIST 1e')
            hists[mass].Draw('SAME HIST')

    #p.BuildLegend()
    leg = buildLegend( legItems, legNames )
    leg.Draw()

    lumi = ROOT.TLatex()
    lumi.SetTextSize(0.04)
    lumi.DrawLatexNDC(.16, .91,"#bf{CMS} #it{Simulation}")
        
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/june18_genMasses/mass_june18_%s.png' % name)
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/june18_genMasses/mass_june18_%s.pdf' % name)
    #c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/june18_genMasses/mass_june18_%s_cut.png' % name)
    #c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/june18_genMasses/mass_june18_%s_cut.pdf' % name)
    p.SetLogy()
    hists[220].SetMinimum( 0.0001 )
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/june18_genMasses/mass_june18_%s_log.png' % name)
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/june18_genMasses/mass_june18_%s_log.pdf' % name)
    #c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/june18_genMasses/mass_june18_%s_cut_log.png' % name)
    #c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/june18_genMasses/mass_june18_%s_cut_log.pdf' % name)

#def basicPlotVarAZh( path, channel, var ) :
#    
#    c = ROOT.TCanvas('c1','c1',500,400)
#    p = ROOT.TPad('p1','p1',0,0,1,1)
#    p.Draw()
#    p.cd()
#    
#    hists = OrderedDict()
#
#    #masses = [220, 240, 260, 280, 300, 320, 340, 350, 400]
#    masses = [220, 240, 260, 300, 320, 350, 400]
#    
#    maxi = 0
#    for mass in masses :
#        f = ROOT.TFile( path+str(mass)+'_'+channel+'.root', 'r' )
#        print f
#        h = f.Get(channel+'_Histos/'+var)
#        print h
#        h.SetName( str(mass) )
#        h.SetTitle( str(mass) )
#        h.SetDirectory(0)
#        hists[mass] = h
#        #hists[mass].Scale( 1. / hists[mass].Integral() )
#        if hists[mass].GetMaximum() > maxi :
#            maxi = hists[mass].GetMaximum()
#    
#    i = 0
#    for mass in masses :
#        i = i + 1
#        print hists[mass]
#        hists[mass].SetLineWidth( 3 )
#        hists[mass].SetLineColor( i )
#        hists[mass].SetMarkerColor( i )
#        if mass == 220 :
#            toName = var
#            hists[mass].SetTitle(toName)
#            hists[mass].SetMaximum( maxi * 1.2 )
#            hists[mass].Draw('HIST 1e')
#        else :
#            hists[mass].Draw('SAME HIST 1e')
#
#    hists[220].Draw('SAME HIST 1e')
#    legend = ROOT.TLegend(0.70, 0.50, 0.95, 0.93)
#    legend.SetMargin(0.3)
#    legend.SetBorderSize(0)
#    for mass in masses :
#        legend.AddEntry( hists[mass], str(mass)+' GeV', 'lep')
#    legend.Draw()
#    #p.BuildLegend()
#
#    savePath = '/afs/cern.ch/user/t/truggles/www/azhMass/otherVars_Aug15/'+channel+'/'
#    checkDir( savePath )
#    c.SaveAs(savePath+'%s.png' % var)
#    if var == 'genMass' :
#        p.SetLogy()
#        hists[220].SetMaximum( maxi * 20 )
#        hists[220].SetMinimum( maxi / 1000 )
#        c.SaveAs(savePath+'%s_log.png' % var)
#    del c, p


mass( 'mssm' )


