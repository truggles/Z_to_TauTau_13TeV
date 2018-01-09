import ROOT
from collections import OrderedDict
from util.helpers import checkDir
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


def mass( name ) :
    
    c = ROOT.TCanvas('c1','c1',1200,800)
    p = ROOT.TPad('p1','p1',0,0,1,1)
    p.Draw()
    p.cd()
    
    hists = OrderedDict()

    if name == 'mssm' :
        #masses = [220, 240, 260, 280, 300, 320, 340, 350, 400]
        masses = [220, 240, 260, 300, 350]
        base = 'azh'
    if name == 'sm_higgs' :
        #masses = [110, 120, 125, 130, 140]
        masses = [120, 130,]
        #masses = [110, 125, 140]
        base = 'ZH'
    
    maxi = 0
    for mass in masses :
        f = ROOT.TFile( '/data/truggles/azh2newAZH/azh%i_eett.root' % mass, 'r' )
        print f
        t = f.Get('Ntuple')
        print t
        hists[mass] = ROOT.TH1F( '%s' % mass, 'A_Gen_Mass %s' % mass, 100, 100, 600 )
        t.Draw( 'genMass >> %s' % mass )
        print hists[mass].Integral()
        hists[mass].SetDirectory(0)
        hists[mass].Scale( 1. / hists[mass].Integral() )
        if hists[mass].GetMaximum() > maxi :
            maxi = hists[mass].GetMaximum()
    
    i = 0
    for mass in masses :
        i = i + 1
        if i == 5 : i += 1
        print mass
        print hists[mass]
        hists[mass].SetLineWidth( 3 )
        hists[mass].SetLineColor( i )
        hists[mass].SetMarkerColor( i )
        if mass == 220 :
            hists[mass].SetMaximum( maxi * 1.2 )
            #hists[mass].Draw('HIST 1e')
            hists[mass].Draw('HIST')
        else :
            #hists[mass].Draw('SAME HIST 1e')
            hists[mass].Draw('SAME HIST')

    p.BuildLegend()
        
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/mass_jan08_%s.png' % name)
    p.SetLogy()
    hists[220].SetMinimum( 2 )
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/azhMass/mass_jan08_%s_log.png' % name)

def basicPlotVarAZh( path, channel, var ) :
    
    c = ROOT.TCanvas('c1','c1',500,400)
    p = ROOT.TPad('p1','p1',0,0,1,1)
    p.Draw()
    p.cd()
    
    hists = OrderedDict()

    #masses = [220, 240, 260, 280, 300, 320, 340, 350, 400]
    masses = [220, 240, 260, 300, 320, 350, 400]
    nameMap = {
        'Mass' : 'A_Vis_Mass',
        'A_Mass' : 'A_Full_Mass',
        'm_vis' : 'Z_Vis_Mass',
        'H_vis' : 'H_Vis_Mass'
        }
    
    maxi = 0
    for mass in masses :
        f = ROOT.TFile( path+str(mass)+'_'+channel+'.root', 'r' )
        print f
        h = f.Get(channel+'_Histos/'+var)
        print h
        h.SetName( str(mass) )
        h.SetTitle( str(mass) )
        h.SetDirectory(0)
        hists[mass] = h
        #hists[mass].Scale( 1. / hists[mass].Integral() )
        if hists[mass].GetMaximum() > maxi :
            maxi = hists[mass].GetMaximum()
    
    i = 0
    for mass in masses :
        i = i + 1
        print hists[mass]
        hists[mass].SetLineWidth( 3 )
        hists[mass].SetLineColor( i )
        hists[mass].SetMarkerColor( i )
        if mass == 220 :
            toName = var
            if var in nameMap.keys() :
                toName = nameMap[var]
            hists[mass].SetTitle(toName)
            hists[mass].SetMaximum( maxi * 1.2 )
            hists[mass].Draw('HIST 1e')
        else :
            hists[mass].Draw('SAME HIST 1e')

    hists[220].Draw('SAME HIST 1e')
    legend = ROOT.TLegend(0.70, 0.50, 0.95, 0.93)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for mass in masses :
        legend.AddEntry( hists[mass], str(mass)+' GeV', 'lep')
    legend.Draw()
    #p.BuildLegend()

    chans = {
        'eeet' : 'eee#tau_{h}',
        'eemt' : 'ee#mu#tau_{h}',
        'eett' : 'ee#tau_{h}#tau_{h}',
        'eeem' : 'eee#mu',
        'eeee' : 'eeee',
        'eemm' : 'ee#mu#mu',
        'emmt' : '#mu#mue#tau_{h}',
        'mmmt' : '#mu#mu#mu#tau_{h}',
        'mmtt' : '#mu#mu#tau_{h}#tau_{h}',
        'emmm' : '#mu#mue#mu',
        'mmmm' : '#mu#mu#mu#mu',
        'ZEE' : 'Z#rightarrowee',
        'ZMM' : 'Z#rightarrow#mu#mu',
        'ZXX' : 'Z#rightarrowee/#mu#mu',
        'LLET' : "ll'e#tau_{h}",
        'LLMT' : "ll'#mu#tau_{h}",
        'LLTT' : "ll'#tau_{h}#tau_{h}",
        'LLEM' : "ll'e#mu",
    }
    chan = ROOT.TLatex(.2, .80,"x")
    chan.SetTextSize(0.05)
    chan.DrawLatexNDC(.2, .84,"Channel: %s" % chans[channel] )
        
    savePath = '/afs/cern.ch/user/t/truggles/www/azhMass/otherVars_Aug15/'+channel+'/'
    checkDir( savePath )
    c.SaveAs(savePath+'%s.png' % var)
    if var == 'genMass' :
        p.SetLogy()
        hists[220].SetMaximum( maxi * 20 )
        hists[220].SetMinimum( maxi / 1000 )
        c.SaveAs(savePath+'%s_log.png' % var)
    del c, p

#n1 = 'shapes/azh/htt_zh.inputs-mssm-13TeV_AMass_LT20.root'
n2 = 'shapes/azh/htt_zh.inputs-sm-13TeV_svFitMass_LT20.root'
#
#mass( n1, 'mssm' )
#mass( n2, 'sm_higgs' )
mass( 'mssm' )


#path = 'azh3July17FR/azh'
#channel = 'ZXX'
#channels = ['ZXX', 'ZMM', 'ZEE', 'LLEM', 'LLET', 'LLMT', 'LLTT']
#plotVars = ['genpT','genMass','m_vis','H_vis','Mass','A_Mass','Z_Pt','H_Pt','Z_Eta','H_Eta','pt_1','pt_2','pt_3','pt_4']
#for var in plotVars :
#    for channel in channels :
#        basicPlotVarAZh( path, channel, var )
#
#
#
