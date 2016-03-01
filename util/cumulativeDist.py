import ROOT

def CDF( h1, zeroNegBins=False ) :
    nBins = h1.GetXaxis().GetNbins()
    minBin = h1.GetBinLowEdge( 1 )
    maxBin = h1.GetBinLowEdge( nBins+1 )
    
    h2 = ROOT.TH1F('h2','h2',nBins,minBin,maxBin)

    runningTotal = 0.
    for i in range( 1, nBins + 1 ) :
        if not zeroNegBins :
            runningTotal += h1.GetBinContent( i )
        elif h1.GetBinContent( i ) > 0 :
            runningTotal += h1.GetBinContent( i )
        #print i, runningTotal
        h2.SetBinContent( i, runningTotal )
    h2.Scale( 1./runningTotal )

    return h2

if __name__ == '__main__' :
    f = ROOT.TFile('../meta/dataCardsBackgrounds/tt_qcdShape_OSIsoCut.root','r')
    h = f.Get('tt_Histos/m_vis')
    h2 = CDF( h )
    h2.SaveAs('tmp.root')
    h3 = CDF( h, True )
    h3.SaveAs('tmp1.root')
