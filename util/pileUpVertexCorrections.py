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
        '80000',
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

    samplefile = ROOT.TFile('meta/PileUpInfo/MCTemplate.root', 'READ')
    sHist = samplefile.Get('nTruePU')

    reweightDict = {}
    for i in range( 1, 52 ) :
        if sHist.GetBinContent( i ) > 0 :
            ratio = dHist.GetBinContent( i ) / sHist.GetBinContent( i )
        else : ratio = 0
        reweightDict[ i ] = ratio

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


def makeAllPUTemplates( count, grouping, sample, channel, fileMin=0, fileMax=9999 ) :

    ''' Get initial chain '''
    out1 = "###   %s PU Template   ###" % sample
    out2 = "Channel:  %s" % channel
    sampleList = 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample)
    path = '%s/final/Ntuple' % channel
    # This should allow us to run over sections of files
    chain = makeTChain( sampleList, path, fileMax, fileMin, fileMax )
    numEntries = chain.GetEntries()
    out3 = "%25s : %10i" % ('Initial', numEntries)

    makePUTemplate( grouping, sample, channel, chain )
    return (count, out1, out2, out3)


def buildAllPUTemplates( samples, numCores, maxFiles=20 ) :
    import multiprocessing
    import os
    
    if not os.path.exists( 'meta/PileUpInfo' ) : os.makedirs( 'meta/PileUpInfo' )

    grouping = os.getenv('_GROUPING_', '25ns') # 25ns is default
    pool = multiprocessing.Pool(processes= numCores )
    mpPU = []

    channels = ['em', 'tt']
    
    count = 0
    for sample in samples :
        if 'data' in sample : tmpMax = 999
        else : tmpMax = maxFiles
    
        for channel in channels :
            if sample == 'data_em' and channel == 'tt' : continue
            if sample == 'data_tt' and channel == 'em' : continue
    
            mpPU.append( pool.apply_async( makeAllPUTemplates, args=(count, grouping, sample, channel, 0, tmpMax) ) )
            count += 1

    mpPUResults = [p.get() for p in mpPU]
    mpPUResults.sort()
    for item in mpPUResults :
        print item[1]
        print item[2]
        print item[3]

if __name__ == '__main__' :
    zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
    os.environ['_ZHOME_'] = zHome
    print zHome
    makeDataPUTemplate( 'Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt', 'pileup_JSON_10-23-2015.txt' )
    makeMCPUTemplate()
