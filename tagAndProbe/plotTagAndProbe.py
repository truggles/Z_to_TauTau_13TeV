import ROOT
import pyplotter.tdrstyle as tdr
from array import array


ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()



def getHist( tree, var, cut, name ) :
    binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
        42.5,45,47.5,50,55,60,65,70,80,90,100])
    #h = ROOT.TH1F( name, name, 20, 0, 100)
    h = ROOT.TH1F( name, name, len(binning)-1, binning)
    #doCut = '(IsoMu22 == 1 && mt < 30 && m_vis > 40 && m_vis < 80)*'+cut
    doCut = '(IsoMu22 == 1)*'+cut
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
    #f = ROOT.TFile('firstRound.root','r')
    #t = f.Get('tauEvents/Ntuple')
    f = ROOT.TFile('third.root','r')
    t = f.Get('TagAndProbe/Ntuple')

    cuts = {
        'SSPass' : '(SS == 1 && IsoMu21MediumIsoTau32 == 1)',
        'OSPass' : '(SS == 0 && IsoMu21MediumIsoTau32 == 1)',
        'SSFail' : '(SS == 1 && IsoMu21MediumIsoTau32 == 0)',
        'OSFail' : '(SS == 0 && IsoMu21MediumIsoTau32 == 0)',
        'SSAll' : '(SS == 1)',
        'OSAll' : '(SS == 0)',
        }

    hists = {}
    for name, cut in cuts.iteritems() :
        print name, cut
        hists[ name ] = getHist( t, 'tPt', cut, name )
        
    ### Save all
    c = ROOT.TCanvas('c','c',600,600)
    saveLoop( c, hists )

    ### Do OS - SS
    groups = ['Pass','Fail','All']
    subMap = {}
    for group in groups :
        subMap[ group ] = subtractTH1( hists['OS'+group], hists['SS'+group] )
    saveLoop( c, subMap )


    ### Make Eff Plot
    g = divideTH1( subMap['Pass'], subMap['All'] )    
    c.SetGrid()
    g.SetMaximum( 1.2 )
    g.Draw()
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/TAP/FinalEff.png')








