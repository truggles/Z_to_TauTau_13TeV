import ROOT
from ROOT import gPad
from array import array
import json
from collections import OrderedDict
import math



def calcDR( eta1, phi1, eta2, phi2 ) :
    return float(math.sqrt( (eta1-eta2)*(eta1-eta2) + (phi1-phi2)*(phi1-phi2) ))


def transMass( met, metphi, l1pt, l1phi ) :
    return math.sqrt( 2 * l1pt * met * (1 - math.cos( l1phi - metphi)))
 


def nvtxTemplate( tree, run, version ) :
    hist = ROOT.TH1F('nvtx', 'nvtx', 60, 0, 60)
    tree.Draw('nvtx>>nvtx')
    hist = gPad.GetPrimitive( 'nvtx')
    hist.SaveAs('%s_%s/nvtx.root' % (run, version) )

def jetPtTemplate( tree, run ) :
    hist = ROOT.TH1F('jetPt', 'jetPt', 50, 0, 1000)
    tree.Draw('j1Pt>>jetPt')
    hist = gPad.GetPrimitive( 'jetPt')
    hist.SaveAs('%s/jetPt.root' % run)

def PUreweightDict( templateRun, run, version ) :
    tmpFile = ROOT.TFile('%s_%s/nvtx.root' % (templateRun, version), 'READ')
    tmpHist = tmpFile.Get('nvtx')
    tmpHist.Scale( 1 / tmpHist.Integral() )

    samplefile = ROOT.TFile('%s_%s/nvtx.root' % (run, version), 'READ')
    sHist = samplefile.Get('nvtx')
    sHist.Scale( 1 / sHist.Integral() )

    reweightDict = {}
    for i in range( 1, 61 ) :
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
        #print targetRun
        lumis = []
        for i in range( 0, len(jsonDict[ targetRun ]) ) :
            first = jsonDict[ targetRun ][i][0]
            last = jsonDict[ targetRun ][i][1]
            for j in range( first, last + 1 ) :
                lumis.append( j )
            #print lumis
        expandedLumis[ int(targetRun) ] = lumis
    return expandedLumis



def makeBunchSpacingJSON( run, version='76X' ) :
    f = ROOT.TFile( '%i_%s/%i.root' % (run,version,run), 'r' )
    t = f.Get('tauEvents/Ntuple')

    jsonF = open('%i_%s/%i_BunchFill.json' %(run,version,run), 'w')
    fillScheme = OrderedDict()
    for i in range( 3564 ) :
        fillScheme[ i ] = 0

    for row in t :
        bunchBC = int(row.bunchCrossing)
        fillScheme[ bunchBC ] = fillScheme[ bunchBC ] + 1

    json.dump( fillScheme, jsonF, indent=2 )
    jsonF.close()

if __name__ == '__main__' :
    for run in [256677,260627] :
        makeBunchSpacingJSON( run )
