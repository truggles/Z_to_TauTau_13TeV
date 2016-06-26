import ROOT
from array import array
from util.buildTChain import makeTChain
import os
import subprocess
from collections import OrderedDict

def makeDataPUTemplate( cert, puJson ) :
    zHome = os.getenv('_ZHOME_')
    os.chdir( zHome + 'meta/PileUpInfo/' )
    executeArray = [
        'pileupCalc.py',
        '-i',
        '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/%s' % cert,
        '--inputLumiJSON',
        '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/%s' % puJson,
        '--calcMode',
        'true',
        '--minBiasXsec',
        '69000',
        '--maxPileupBin',
        '52',
        '--numPileupBins',
        '52',
        'DataTemplate.root']
    subprocess.call( executeArray )
    os.chdir( zHome )



def makeMCPUTemplate( ) :
    # 25ns pileup distributions found here: https://github.com/cms-sw/cmssw/blob/CMSSW_7_4_X/SimGeneral/MixingModule/python/mix_2015_25ns_Startup_PoissonOOTPU_cfi.py
    MCDist = [4.8551E-07,
              1.74806E-06,
              3.30868E-06,
              1.62972E-05,
              4.95667E-05,
              0.000606966,
              0.003307249,
              0.010340741,
              0.022852296,
              0.041948781,
              0.058609363,
              0.067475755,
              0.072817826,
              0.075931405,
              0.076782504,
              0.076202319,
              0.074502547,
              0.072355135,
              0.069642102,
              0.064920999,
              0.05725576,
              0.047289348,
              0.036528446,
              0.026376131,
              0.017806872,
              0.011249422,
              0.006643385,
              0.003662904,
              0.001899681,
              0.00095614,
              0.00050028,
              0.000297353,
              0.000208717,
              0.000165856,
              0.000139974,
              0.000120481,
              0.000103826,
              8.88868E-05,
              7.53323E-05,
              6.30863E-05,
              5.21356E-05,
              4.24754E-05,
              3.40876E-05,
              2.69282E-05,
              2.09267E-05,
              1.5989E-05,
              4.8551E-06,
              2.42755E-06,
              4.8551E-07,
              2.42755E-07,
              1.21378E-07,
              4.8551E-08]
    dHist = ROOT.TH1F('nTruePU', 'dhist', 52, 0, 52)
    for i in range( 0, 52 ) :
        dHist.SetBinContent( i, MCDist[i] )
    dHist.SaveAs('meta/PileUpInfo/MCTemplate.root')

def makeDYJetsPUTemplate( analysis ) :
    import util.buildTChain as chainer
    from ROOT import gPad
    inFiles = 'meta/NtupleInputs_%s/DYJets.txt' % analysis
    #avgHist = ROOT.TH1F('nTruePU', 'avgHist', 52, 0, 52)

    for channel in ['em', 'tt'] :
        chain = chainer.makeTChain( inFiles, '%s/final/Ntuple' % channel )
        prevEvt = (0,0,0)
        tmpHist = ROOT.TH1F('nTruePU', 'tmpHist', 52, 0, 52)
        for row in chain :
            currentEvt = (row.lumi, row.run, row.evt)
            if currentEvt != prevEvt :
                if row.GenWeight > 0 :
                    genW = 1
                else : # this is for data
                    genW = -1
                #print "Filling - nvtx:%i    genW:%i" % (row.nvtx, genW)
                tmpHist.Fill( row.nTruePU * genW )
                prevEvt = currentEvt
        tmpHist.Scale( 1 / tmpHist.Integral() )
        tmpHist.SaveAs('meta/PileUpInfo/DYJetsNTruePU_%s.root' % channel )
        #avgHist.Add( tmpHist )
    #avgHist.Scale( 1 / avgHist.Integral() )
    #avgHist.SaveAs('meta/PileUpInfo/DYJetsNTruePU.root' % (analysis) )


def PUreweight( channel ) :
    # https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2015#PU_reweighting
    #datafile = ROOT.TFile('meta/PileUpInfo/DataTemplate.root', 'READ')
    datafile = ROOT.TFile('meta/PileUpInfo/Data_Pileup_2015D_Feb02.root', 'READ') # Made by Adinda
    dHist = datafile.Get('pileup')
    dHist.Scale( 1 / dHist.Integral() )

    samplefile = ROOT.TFile('meta/PileUpInfo/MC_Fall15_PU25_V1.root', 'READ') # Made by Adinda, same as mine but shifter up 1 bin
    #samplefile = ROOT.TFile('meta/PileUpInfo/MCTemplate.root', 'READ')
    #sHist = samplefile.Get('nTruePU')
    sHist = samplefile.Get('pileup')
    sHist.Scale( 1 / sHist.Integral() )

    reweightDict = OrderedDict()
    #i_data = 0
    #i_mc = 0
    for i in range( 1, dHist.GetXaxis().GetNbins()+1 ) :
        # dHist has exactly 600 bins, not 601 w/ over/underflow
        if sHist.GetBinContent( i ) > 0 :
            ratio = dHist.GetBinContent( i ) / sHist.GetBinContent( i )
        else : ratio = 0
        reweightDict[ (i-1)/10. ] = ratio

    #print "Data = %f   MC = %f" % (i_data, i_mc)
    #print reweightDict
    return reweightDict


def addNvtxWeight( analysis, sample, fileName, channel ) :
    
    tfile = ROOT.TFile('%s.root' % fileName, 'update')
    tree = tfile.Get('%s/Ntuple' % channel )

    puDict = PUreweight( analysis, sample, channel )

    nvtxWeight = array('f', [ 0 ] )
    nvtxWeightB = tree.Branch('nvtxWeight', nvtxWeight, 'nvtxWeight/F')

    # Need to cd to the tree's directory
    tfile.cd( '%s' % channel )
    
    for i in range( tree.GetEntries() ):
        tree.GetEntry( i )
        nvtxWeight[0] = puDict[ tree.nvtx ]
        nvtxWeightB.Fill()
        #print "%10i %10i %10i %4f" % (tree.run, tree.lumi, tree.evt, puDict[ tree.nvtx ])
    tree.Write('', ROOT.TObject.kOverwrite)
    tfile.Close()




if __name__ == '__main__' :
    #zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
    #os.environ['_ZHOME_'] = zHome
    #print zHome
    #makeDataPUTemplate( 'Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt', 'pileup_JSON_10-23-2015.txt' )
    #makeMCPUTemplate()
    ary = PUreweight( 'em' )
    tot = 0
    for key in ary.keys() :
        print key, ary[key]
        tot += ary[key]
    print tot
    #makeDYJetsPUTemplate( 'dataCards' )
