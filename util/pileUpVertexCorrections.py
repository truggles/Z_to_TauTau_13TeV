import ROOT
from array import array
from util.buildTChain import makeTChain
import os
import subprocess

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


def PUreweight( ) :
    datafile = ROOT.TFile('meta/PileUpInfo/DataTemplate.root', 'READ')
    dHist = datafile.Get('pileup')
    dHist.Scale( 1 / dHist.Integral() )

    samplefile = ROOT.TFile('meta/PileUpInfo/MCTemplate.root', 'READ')
    sHist = samplefile.Get('nTruePU')
    sHist.Scale( 1 / sHist.Integral() )

    reweightDict = {}
    #i_data = 0
    #i_mc = 0
    for i in range( 1, 53 ) :
        if sHist.GetBinContent( i ) > 0 :
            #i_data += dHist.GetBinContent( i )
            #i_mc += sHist.GetBinContent( i )
            #print "%i data: %f    mc: %f    ratio: %f" % (i, dHist.GetBinContent( i ), sHist.GetBinContent( i ), (dHist.GetBinContent( i ) / sHist.GetBinContent( i )) )
            ratio = dHist.GetBinContent( i ) / sHist.GetBinContent( i )
        else : ratio = 0
        reweightDict[ i-1 ] = ratio

    #print "Data = %f   MC = %f" % (i_data, i_mc)
    #print reweightDict
    return reweightDict


def addNvtxWeight( grouping, sample, fileName, channel ) :
    
    tfile = ROOT.TFile('%s.root' % fileName, 'update')
    tree = tfile.Get('%s/Ntuple' % channel )

    puDict = PUreweight( grouping, sample, channel )

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
    ary = PUreweight()
    for key in ary.keys() :
        print key, ary[key]
