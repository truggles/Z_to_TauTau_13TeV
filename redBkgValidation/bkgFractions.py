
import ROOT
from ROOT import gPad
from array import array
import pyplotter.tdrstyle as tdr
from collections import OrderedDict
ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

def buildLegend( hists ) :
    ''' Build the legend explicitly so we can specify marker styles '''
    legend = ROOT.TLegend(0.60, 0.75, 0.95, 0.93)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for name, hist in hists.iteritems() :
        legend.AddEntry( hist, name, 'f')
    return legend

def decorate( p, channel ) :

    channelNames = {
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
    cmsLumi = 35.9
    # Set CMS Styles Stuff
    logo = ROOT.TText(.2, .88,"CMS Preliminary")
    logo.SetTextSize(0.03)
    logo.DrawTextNDC(.2, .89,"CMS Preliminary")
    
    chan = ROOT.TLatex(.2, .80,"x")
    chan.SetTextSize(0.05)
    chan.DrawLatexNDC(.2, .84,"Channel: %s" % channelNames[channel] )
    
    lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi.SetTextSize(0.03)
    lumi.DrawTextNDC(.7,.96,"%.1f / fb (13 TeV)" % cmsLumi )



azhMass = '350'
azhSF = .025
colors = {
    'ZZ' : [ROOT.kGreen-9, 'ZZ'],
    'ttZ' : [ROOT.kYellow-7, 'ttZ'],
    'WZ' : [ROOT.kRed+1, 'WZ'],
    'TriBoson' : [ROOT.kOrange+7, 'Rare'],
    'DYJ' : [ROOT.TColor.GetColor(248,206,104), 'ZJets'],
    'TT' : [ROOT.kBlue-8, 't#bar{t}'],
    'redBkg' : [ROOT.kCyan, 'Reducible Bkg.'],
    'higgs' : [ROOT.kRed-4, 'SM HZZ (125)'],
    'VH' : [ROOT.kGreen, 'SM VHiggs(125)'],
    'azh' : [ROOT.kBlue, 'A#rightarrowZh M%s #sigma=%.3fpb' % (azhMass, azhSF)],
        } # azh

inVars = {
    'pt_3' : ['Higgs Leg 1 p_{T} GeV',],
    'pt_4' : ['Higgs Leg 2 p_{T} GeV',]
}

c = ROOT.TCanvas('c','c',600,600)
p = ROOT.TPad('p','p',0,0,1,1)
p.Draw()
p.cd()

bkgs = ['TT', 'DYJ', 'WZ', 'TriBoson', 'ZZ', 'ttZ']
groups = ['LLET','LLMT','LLTT','LLEM']

xBins = array( 'd', [0, 20, 40, 60, 100, 200] )
xNum = len( xBins ) - 1

fileNames = ['OS_Not_Signal','OS_Signal_Relaxed','SS_Not_Signal','SS_Signal_Relaxed']
for fileName in fileNames :
    plotDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkgComp/Nov28/%s/' % fileName
    for var in inVars.keys() :
        #var = 'pt_3'
        iFile = ROOT.TFile('../shapes/azh/fr_%s/htt_zh.inputs-sm-13TeV_%s.root' % (fileName, var), 'r')
            
        for group in groups :
            #group = 'LLMT'
            print var, group
            
            tDir = iFile.Get( group+'_inclusive' )
            
            tDir.ls()
            
            stack = ROOT.THStack("All Backgrounds stack", group + var )
            fracStack = ROOT.THStack("All Backgrounds Frac stack", group + var + '_frac' )
            
            fracHists = OrderedDict()
            
            for bkg in bkgs :
                fracHists[ bkg ] = ROOT.TH1D( bkg+'_frac'+var, bkg+'_frac'+var, xNum, xBins )
                hist = tDir.Get( bkg )
                hist.SetFillColor( colors[ bkg ][0] )
                hist.GetXaxis().SetTitle( inVars[var][0] )
                stack.Add( hist ) #.Rebin( xNum, "rebinned", xBins ) )
            
            # With total yield known we can normalize per bin now
            for b in range( 1, stack.GetStack().Last().GetNbinsX()+1 ) :
                binTotal = stack.GetStack().Last().GetBinContent( b )
                if binTotal > 0. :
                    for bkg in bkgs :
                        hist = tDir.Get( bkg )
                        #print b, binTotal
                        fracHists[ bkg ].SetBinContent( b, hist.GetBinContent( b ) / binTotal )
            
            for bkg in bkgs :
                fracHists[ bkg ].SetFillColor( colors[ bkg ][0] )
                fracHists[ bkg ].GetXaxis().SetTitle( inVars[var][0] )
                print bkg, fracHists[ bkg ]
                fracStack.Add( fracHists[ bkg ] )
            
            
            stack.Draw('HIST')
            stack.GetXaxis().SetTitle( inVars[var][0] )
            stack.GetYaxis().SetTitle( 'Events per 20 / GeV' )
            stack.SetMaximum( stack.GetMaximum() * 1.2 )
            decorate( p, group )
            leg1 = buildLegend( fracHists )
            leg1.Draw('SAME')
            c.SaveAs( plotDir + group + '_' + var + '.png' )
            
            c.Clear()
            fracStack.Draw('HIST')
            fracStack.GetXaxis().SetTitle( inVars[var][0] )
            fracStack.GetYaxis().SetTitle( 'Fraction of Events per Bin' )
            fracStack.SetMaximum( 1.4 )
            decorate( p, group )
            leg = buildLegend( fracHists )
            leg.Draw('SAME')
            c.SaveAs( plotDir + group + '_' + var + '_frac.png' )
    
        del fracHists, stack


