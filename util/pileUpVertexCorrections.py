import ROOT
from array import array
from util.buildTChain import makeTChain
import os
import subprocess
from collections import OrderedDict
import math

# New minBias xsec: https://hypernews.cern.ch/HyperNews/CMS/get/luminosity/613/2/1/1/1.html
def makeDataPUTemplate( cert, puJson ) :
    zHome = os.getenv('_ZHOME_')
    os.chdir( zHome + 'data/PileUpInfo/' )
    executeArray = [
        'pileupCalc.py',
        '-i',
        '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/%s' % cert,
        '--inputLumiJSON',
        '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/%s' % puJson,
        '--calcMode',
        'true',
        '--minBiasXsec',
        '69200',
        '--maxPileupBin',
        '50',
        '--numPileupBins',
        '500',
        'DataTemplate.root']
    subprocess.call( executeArray )
    os.chdir( zHome )



def makeMCPUTemplate( ) :
    # 25ns pileup distributions found here: https://github.com/cms-sw/cmssw/blob/CMSSW_7_4_X/SimGeneral/MixingModule/python/mix_2015_25ns_Startup_PoissonOOTPU_cfi.py
    # 25ns PU for 80X (this is out of time, so we add a 0 at the bottom: https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimGeneral/MixingModule/python/mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi.py#L25
    MCDist = [
        0.000829312873542,
        0.00124276120498,
        0.00339329181587,
        0.00408224735376,
        0.00383036590008,
        0.00659159288946,
        0.00816022734493,
        0.00943640833116,
        0.0137777376066,
        0.017059392038,
        0.0213193035468,
        0.0247343174676,
        0.0280848773878,
        0.0323308476564,
        0.0370394341409,
        0.0456917721191,
        0.0558762890594,
        0.0576956187107,
        0.0625325287017,
        0.0591603758776,
        0.0656650815128,
        0.0678329011676,
        0.0625142146389,
        0.0548068448797,
        0.0503893295063,
        0.040209818868,
        0.0374446988111,
        0.0299661572042,
        0.0272024759921,
        0.0219328403791,
        0.0179586571619,
        0.0142926728247,
        0.00839941654725,
        0.00522366397213,
        0.00224457976761,
        0.000779274977993,
        0.000197066585944,
        7.16031761328e-05,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0]
    nBins = len(MCDist)
    print "MC # Bins:",nBins
    dHist = ROOT.TH1F('pileup', 'pileup', nBins*10, 0, nBins)
    for i in range( 1, (nBins*10)+1 ) :
        #print "bin: %i, MC position: %i" % (i, math.floor((i-1)/10) )
        dHist.SetBinContent( i, MCDist[ (i-1)/10 ] )
    dHist.SaveAs('data/PileUpInfo/MCTemplate.root')



def PUreweight() :
    # https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2015#PU_reweighting
    datafile = ROOT.TFile('data/PileUpInfo/DataTemplate.root', 'READ')
    dHist = datafile.Get('pileup')
    dHist.Scale( 1 / dHist.Integral() )

    samplefile = ROOT.TFile('data/PileUpInfo/MCTemplate.root', 'READ')
    sHist = samplefile.Get('pileup')
    sHist.Scale( 1 / sHist.Integral() )

    reweightDict = OrderedDict()
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
    zHome = os.getenv('CMSSW_BASE') + '/src/Z_to_TauTau_13TeV/'
    os.environ['_ZHOME_'] = zHome
    makeDataPUTemplate( 'Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt', 'pileup_latest.txt' ) # Aug 25, 20.1/fb
    #makeMCPUTemplate()
    print PUreweight()



