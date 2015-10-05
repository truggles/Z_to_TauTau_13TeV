import ROOT

def makeDataPUTemplate( grouping, dataTree, channel ) :
    dHist = ROOT.TH1F('nvtx', 'dhist', 100, 0, 100)
    for row in dataTree :
        dHist.Fill( row.nvtx )
    dHist.Scale( 1 / dHist.Integral() )
    dHist.SaveAs('meta/PileUpInfo/%s_%s.root' % (grouping, channel) )

def makePUTemplate( grouping, sample, channel, dataTree ) :
    dHist = ROOT.TH1F('nvtx', 'dhist', 100, 0, 100)
    prevEvt = (0,0,0)
    for row in dataTree :
        currentEvt = (row.lumi, row.run, row.evt)
        if currentEvt != prevEvt :
            if row.GenWeight >= 0 :
                genW = 1
            else : # this is for data
                genW = -1
            #print "Filling - nvtx:%i    genW:%i" % (row.nvtx, genW)
            dHist.Fill( row.nvtx * genW )
            prevEvt = currentEvt
    dHist.Scale( 1 / dHist.Integral() )
    if 'data' in sample :
        dHist.SaveAs('meta/PileUpInfo/%s_%s.root' % (grouping, sample) )
    else :
        dHist.SaveAs('meta/PileUpInfo/%s_%s_%s.root' % (grouping, sample, channel) )


def PUreweight( grouping, sample, channel ) :
    datafile = ROOT.TFile('meta/PileUpInfo/%s_data_%s.root' % (grouping, channel), 'READ')
    dHist = datafile.Get('nvtx')

    samplefile = ROOT.TFile('meta/PileUpInfo/%s_%s_%s.root' % (grouping, sample, channel), 'READ')
    sHist = samplefile.Get('nvtx')

    reweightDict = {}
    for i in range( 1, 101 ) :
        if sHist.GetBinContent( i ) > 0 :
            ratio = dHist.GetBinContent( i ) / sHist.GetBinContent( i )
        else : ratio = 0
        reweightDict[ i ] = ratio

    #print reweightDict
    return reweightDict
