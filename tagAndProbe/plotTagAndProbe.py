import ROOT
import pyplotter.tdrstyle as tdr
from array import array


ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()



def getHist( tree, var, cut, name ) :
    binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
        42.5,45,47.5,50,55,60,67.5,80,100])
    #h = ROOT.TH1F( name, name, 20, 0, 100)
    h = ROOT.TH1F( name, name, len(binning)-1, binning)
    #doCut = '(IsoMu22 == 1 && mt < 30 && m_vis > 40 && m_vis < 80)*'+cut
    doCut = '(IsoMu22 == 1)*(tMVAIsoLoose==1)*'+cut
    t.Draw( var+' >> '+name, doCut )
    print name, h.Integral()
    h.GetXaxis().SetTitle('#tau p_{T} (GeV)')
    h.GetYaxis().SetTitle('Number of Events')
    h.SetDirectory( 0 )
    return h

def subtractTH1( h1, h2 ) :
    h3 = h1
    h3.Add( -1 * h2 )
    h3.SetTitle( h1.GetTitle()+'_Minus_'+h2.GetTitle() )
    return h3

def saveLoop( c, map ) :
    for name, h in map.iteritems() :
        h.Draw()
        c.SaveAs('/afs/cern.ch/user/t/truggles/www/TAP/'+name+'.png')
        c.Clear()

def divideTH1( h1, h2 ) :
    ### FIXME Check bins to make sure Pass <= All
    for b in range( 1, h1.GetNbinsX()+1 ) :
        b1 =  h1.GetBinContent( b )
        b2 =  h2.GetBinContent( b )
        print b1, b2
        if b1 > b2 :
            h2.SetBinContent( b, b1 )
    g = ROOT.TGraphAsymmErrors( h1, h2 )
    return g

if __name__ == '__main__' :

    colors = [i for i in range(1, 10)]
    effPlots = {}
    #for run in ['RunB', 'RunC', 'RunD', 'RunE', 'RunF', 'AllRuns', 'ICHEPRuns'] :
    runs = ['RunB', 'RunC', 'RunE', 'RunF', 'AllRuns', 'ICHEPRuns', 'DYJets', 'ggH125']
    for i, run in enumerate(runs) :
        f = ROOT.TFile('/data/truggles/TAP_hadd/'+run+'.root','r')
        t = f.Get('TagAndProbe/Ntuple')

        cuts = {
            'SSPass'+run: '(SS == 1 && IsoMu21MediumIsoTau32 == 1)',
            'OSPass'+run: '(SS == 0 && IsoMu21MediumIsoTau32 == 1)',
            'SSFail'+run: '(SS == 1 && IsoMu21MediumIsoTau32 == 0)',
            'OSFail'+run: '(SS == 0 && IsoMu21MediumIsoTau32 == 0)',
            'SSAll'+run: '(SS == 1)',
            'OSAll'+run: '(SS == 0)',
            }

        hists = {}
        for name, cut in cuts.iteritems() :
            print name, cut
            hists[ name ] = getHist( t, 'tPt', cut, name )
            
        ### Save all
        c = ROOT.TCanvas('c','c',600,600)
        saveLoop( c, hists )

        ### Do OS - SS
        groups = ['Pass'+run,'Fail'+run,'All'+run]
        subMap = {}
        for group in groups :
            subMap[ group ] = subtractTH1( hists['OS'+group], hists['SS'+group] )
        saveLoop( c, subMap )


        ### Make Eff Plot
        g = divideTH1( subMap['Pass'+run], subMap['All'+run] )    
        c.SetGrid()
        g.SetMaximum( 1.2 )
        g.GetXaxis().SetTitle('#tau p_{T} (GeV)')
        g.GetYaxis().SetTitle('HLT Efficiency')
        #g.SetTitle(run+' HLT MediumIso35Tau Eff. per Tau')
        g.SetTitle(run)
        g.SetLineColor( colors[i] )
        g.SetLineWidth(2)
        g.Draw()
        c.SaveAs('/afs/cern.ch/user/t/truggles/www/TAP/FinalEff_'+run+'.png')
        c.Clear()
        effPlots[run] = g

    del c
    c = ROOT.TCanvas('c','c',900,900)
    effPlots['DYJets'].SetMaximum(1.5)
    effPlots['DYJets'].Draw()
    finalRuns = ['ggH125', 'AllRuns', 'ICHEPRuns', 'DYJets']
    colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen]
    for i, run in enumerate(finalRuns) :
        print i, run
        effPlots[run].SetLineColor( colors[i] )
        effPlots[run].Draw('SAME')
    c.BuildLegend()
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/TAP/_Combined_FinalEff.png')
    








