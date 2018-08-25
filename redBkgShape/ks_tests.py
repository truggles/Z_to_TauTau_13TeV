


import ROOT
import os
from util.helpers import checkDir
from collections import OrderedDict
ROOT.gROOT.SetBatch(True)


def ksTest( dir_, channel, h1, others ) :
    c1 = ROOT.TCanvas( 'c1', 'c1', 600, 600 )
    p1 = ROOT.TPad('p1', 'p1', 0, 0, 1, 1 )
    p1.Draw()
    p1.SetGrid()
    p1.cd()

    colors = [ROOT.kBlue, ROOT.kGreen, ROOT.kBlack ]
    h1.SetLineColor( ROOT.kRed )
    h1.SetFillColorAlpha( ROOT.kRed, 0.25 )
    h1.SetLineWidth( 3 )
    h1.SetStats(0)
    title = 'svFit m_{#tau#tau}'
    h1.GetXaxis().SetTitle('%s (GeV)' % title)
    h1.GetYaxis().SetTitle('A.U.')
    h1.GetYaxis().SetTitleOffset( 1.45 )
    h1.Scale( 1. / h1.Integral() )
    ksProbX = h1.KolmogorovTest( h1, 'X' )
    ksProb = h1.KolmogorovTest( h1 )
    print "%25s   KS Prob = %3.2f    KS ProbX = %3.2f" % (h1.GetTitle(), ksProb, ksProbX)

    ksReturns = []
    ksReturns.append( ksProbX )

    #h1.Draw('')
    cnt = 0
    for title, h in others.iteritems() :
        h.Scale( 1. / h.Integral() )
        ksProbX = h1.KolmogorovTest( h, 'X' )
        ksProb = h1.KolmogorovTest( h )
        print "%25s   KS Prob = %3.2f    KS ProbX = %3.2f" % (h.GetTitle(), ksProb, ksProbX)
        ksReturns.append( ksProbX )
        h.SetLineColor( colors[cnt] )
        h.SetFillColorAlpha( colors[cnt], 0.25 )
        h.SetLineWidth( 3 )
        #h.Draw('same')
        cnt += 1
    #h1.SetTitle( 'KS Prob = %3.3f, PseudoExp = %3.3f' % (ksProb, ksProbX ) )
    

    ''' Rebin for viewing '''
    #RebinValGeV = 10.0
    #currentBinW = float(h1.GetXaxis().GetBinWidth( 1 ))
    #print RebinValGeV,currentBinW
    #rebinNum = RebinValGeV / currentBinW
    #print RebinValGeV,currentBinW,rebinNum
    rebinNum = 20
    h1new = h1.Clone( h1.GetTitle()+'new' )
    h1new.Rebin( rebinNum )

    h1new.Draw('HIST e1')

    
    
    ''' Build the legend explicitly so we can specify marker styles '''
    legend = ROOT.TLegend(0.52, 0.6, 0.97, 0.9)
    legend.SetMargin(0.3)
    #legend.SetBorderSize(0)
    #legend.AddEntry( h1new, n1, 'l')
    #legend.AddEntry( h2new, n2, 'l')
    #legend.AddEntry( h1new, '%s, KS=%2.2f' % (h1.GetTitle(), ksReturns.pop(0)), 'l')
    maxi = 0.0
    for title, h in others.iteritems() :
        hNew = h.Clone( h.GetTitle()+'new' )
        hNew.Rebin( rebinNum )
        hNew.Draw('same HIST e1')
        if hNew.GetMaximum() > maxi : maxi = hNew.GetMaximum()
        legend.AddEntry( hNew, '%s, KS=%2.2f' % (h.GetTitle(), ksReturns.pop(0)), 'l')
    legend.Draw()

    h1new.SetTitle( 'KS Test: Relaxed Iso/ID MC as baseline: %s' % channel )
    #h1new.SetTitle( 'KS Test using Relaxed SS Shape as baseline: %s' % channel )

    maxX = 1.5 if channel != 'LLTT' else 2.0
    h1new.SetMaximum( max(h1new.GetMaximum(), maxi) * maxX )
    h1new.SetMinimum( 0.0 )
    
    #c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgShape/%s/redBkgComp_SSShapeBase_%s.png' % (dir_, channel) )
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgShape/%s/redBkgComp_MCBase_%s.png' % (dir_, channel) )
    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/redBkgShape/%s/redBkgComp_MCBase_%s.pdf' % (dir_, channel) )

    del c1, p1

#
# 1. MC shapes with correct yield hadded
# 2. FR raw shapes
# 3. SS RedBkg Shape VVLoose
# 4. SS iso raw > -0.5
# 5. SS iso raw > -0.6
# 6. SS iso raw > -0.7
# 7. SS iso raw > -0.8
# 8. SS iso raw > -0.9
# 9. SS iso raw ALL
#

chan_map = {
    'LLTT' : ['eett', 'mmtt'],
    'LLET' : ['eeet', 'emmt'],
    'LLMT' : ['eemt', 'mmmt'],
    'LLEM' : ['eeem', 'emmm'],
}


def getHist( dir_, channel, fName, histName ) :
    # These are Jaana's shapes which need to be combined by Higgs final state
    if fName == 'FF+WZ' :
        f = ROOT.TFile( 'dcSync_AsvConstr_SF_btag_August24_EXP_1GeV.root', 'r' )
        h = f.Get( '%s_inclusive/allFakes' % chan_map[channel][0] ) # Grab the RB shape which is FF+WZ
        h.Sumw2()
        h.SetDirectory( 0 )
        h.Add( f.Get( '%s_inclusive/allFakes' % chan_map[channel][1] ) )
    else :
        f = ROOT.TFile( '%s/%s_%s.root' % (dir_, fName, channel), 'r' )
        h = f.Get( '%s_Histos/%s' % (channel, histName) )
        h.Sumw2()
        h.SetDirectory( 0 )
    return h

#ksTest( channel, h1, others )

dir_ = 'shapes_Aug25v1'
checkDir( '/afs/cern.ch/user/t/truggles/www/redBkgShape/%s' % dir_ )

#histName = 'm_sv'
histName = 'AMassConst'
fNames = OrderedDict()
fNames['mc'] = 'MC OS Relaxed'
fNames['shape'] = 'Data SS Relaxed'
fNames['yield'] = 'FR OS Direct'
fNames['FF+WZ'] = 'FR OS Direct FF + WZ'
#fNames = ['shape','yield','mc']
#fNames = ['shape','yield',]
#for channel in ['LLTT', 'LLET', 'LLMT', 'LLEM'] :
for channel in ['LLTT', 'LLET', 'LLMT', 'LLEM'] :
    histMap = {}
    cnt = 0
    for fName in fNames :
        if cnt == 0 :
            h1 = getHist( dir_, channel, fName, histName )
            h1.SetTitle( fNames[ fName ] )
        else :
            histMap[ fName ] = getHist( dir_, channel, fName, histName )
            histMap[ fName ].SetTitle( fNames[ fName ] )
        cnt += 1
    ksTest( dir_, channel, h1, histMap )









