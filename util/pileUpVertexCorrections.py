import ROOT

def makeDataPUTemplate( grouping, dataTree, channel ) :
    dHist = ROOT.TH1F('nvtx', 'dhist', 100, 0, 100)
    for row in dataTree :
        dHist.Fill( row.nvtx )
    dHist.Scale( 1 / dHist.Integral() )
    dHist.SaveAs('meta/PileUpInfo/%s_%s.root' % (grouping, channel) )


def PUreweight(sampleTree, dataFile) :
    datafile = ROOT.TFile('meta/PileUpInfo/%s.root' % dataFile, 'READ')
    dHist = datafile.Get('nvtx')


    sHist = ROOT.TH1F('samp hist', 'shist', 100, 0, 100)
    for row in sampleTree :
        # Do Gen Weighting here too
        if row.GenWeight >= 0 : genWeight = 1
        if row.GenWeight < 0 : genWeight = -1
        sHist.Fill( row.nvtx * genWeight )
    sHist.Scale( 1 / sHist.Integral() )
    
    reweightDict = {}
    for i in range( 1, 101 ) :
        if sHist.GetBinContent( i ) > 0 :
            ratio = dHist.GetBinContent( i ) / sHist.GetBinContent( i )
        else : ratio = 0
        reweightDict[ i ] = ratio

    #for j in range( 1, 101 ) :
    #    prev = sHist.GetBinContent( j )
    #    sHist.SetBinContent( j, prev * reweightDict[ i ] )

    #c1 = ROOT.TCanvas('c1', 'c1', 800, 800)
    #dHist.Draw()
    #sHist.Draw('same')
    #c1.SaveAs('test.root')

    return reweightDict
