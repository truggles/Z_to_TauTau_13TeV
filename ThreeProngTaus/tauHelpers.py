import ROOT
from ROOT import gPad
from array import array

def nvtxTemplate( tree, run ) :
    hist = ROOT.TH1F('nvtx', 'nvtx', 60, 0, 60)
    tree.Draw('nvtx>>nvtx')
    hist = gPad.GetPrimitive( 'nvtx')
    hist.SaveAs('%s/nvtx.root' % run)

def jetPtTemplate( tree, run ) :
    hist = ROOT.TH1F('jetPt', 'jetPt', 50, 0, 1000)
    tree.Draw('j1Pt>>jetPt')
    hist = gPad.GetPrimitive( 'jetPt')
    hist.SaveAs('%s/jetPt.root' % run)

def PUreweightDict( templateRun, run ) :
    tmpFile = ROOT.TFile('%i/nvtx.root' % templateRun, 'READ')
    tmpHist = tmpFile.Get('nvtx')
    tmpHist.Scale( 1 / tmpHist.Integral() )

    samplefile = ROOT.TFile('%i/nvtx.root' % run, 'READ')
    sHist = samplefile.Get('nvtx')
    sHist.Scale( 1 / sHist.Integral() )

    reweightDict = {}
    for i in range( 1, 60 ) :
        if sHist.GetBinContent( i ) > 0 :
            ratio = tmpHist.GetBinContent( i ) / sHist.GetBinContent( i )
        else : ratio = 0
        reweightDict[ i-1 ] = ratio
    return reweightDict

def jetPtPUreweightDict( templateRun, run ) :
    tmpFile = ROOT.TFile('%i/jetPt.root' % templateRun, 'READ')
    tmpHist = tmpFile.Get('jetPt')
    tmpHist.Scale( 1 / tmpHist.Integral() )

    samplefile = ROOT.TFile('%i/jetPt.root' % run, 'READ')
    sHist = samplefile.Get('jetPt')
    sHist.Scale( 1 / sHist.Integral() )

    reweightDict = {}
    for i in range( 1, 51 ) :
        if sHist.GetBinContent( i ) > 0 :
            ratio = tmpHist.GetBinContent( i ) / sHist.GetBinContent( i )
        else : ratio = 0
        reweightDict[ i-1 ] = ratio
    return reweightDict

# function to mae a dict to hold run vs its good lumiBlocks
def buildFullLumiList( jsonDict ) :
    expandedLumis = {}
    for targetRun in jsonDict.keys() :
        print targetRun
        lumis = []
        for i in range( 0, len(jsonDict[ targetRun ]) ) :
            first = jsonDict[ targetRun ][i][0]
            last = jsonDict[ targetRun ][i][1]
            for j in range( first, last + 1 ) :
                lumis.append( j )
            #print lumis
        expandedLumis[ int(targetRun) ] = lumis
    return expandedLumis
