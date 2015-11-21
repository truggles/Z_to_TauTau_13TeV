#!/usr/bin/env python

# A script for building a JSON file containg relevant info for each sample
# June, 12 2015

import os
from getMeta import getDBSInfo, getNumberOfFiles, getEventCount, printJson, getSummedWeights



def makeMetaJSON( grouping ) :
    #samplesSync = { 'Sync-HtoTT': ('/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 999)
    samplesSync = { 'Sync-HtoTT': ('/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM', 999)
    }
    
    ### Excellent Source: https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
    ### See Kenneth's Log Book for how to find this stuff on MCM: https://twiki.cern.ch/twiki/bin/view/Main/KDLLogBook#LogDay20150106
    
    # Cross Section updated on Aug 3, 2015 per HTT Twiki
    #            'data_tt' : ('/Tau/Run2015B-PromptReco-v1/MINIAOD', -999),
    #            'data_em' : ('/MuonEG/Run2015B-PromptReco-v1/MINIAOD', -999),
    
    # em enriched QCD has a filter efficiency applied to their cross sections
    campaign = 'RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-'
    old = 'RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-'
    samples25ns = { 
                'data_em' : ('', -999.0),
                'data_tt' : ('', -999.0),
                'ggHtoTauTau' : ('/GluGluHToTauTau_M125_13TeV_powheg_pythia8/%sv1/MINIAODSIM' % campaign, 43.92 * 0.0632 ),
                'VBFHtoTauTau' : ('/VBFHToTauTau_M125_13TeV_powheg_pythia8/%sv1/MINIAODSIM' % campaign, 3.748 * 0.0632 ),
                'DYJets' : ('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%sv1/MINIAODSIM' % campaign, 6025.0 ), 
                'DYJetsLow' : ('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%sv1/MINIAODSIM' % campaign, 18610.0 ), 
                'TTJets' : ('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%sv3/MINIAODSIM' % campaign, 831.76 ),
                'T-tW' : ('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%sv2/MINIAODSIM' % campaign, 35.6 ),
                'Tbar-tW' : ('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%sv1/MINIAODSIM' % campaign, 35.6),
                'WJets' : ('/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%sv1/MINIAODSIM' % campaign, 61526.7 ),
                'WW' : ('/WW_TuneCUETP8M1_13TeV-pythia8/%sv1/MINIAODSIM' % campaign, 63.21 ),
                'WZJets' : ('/WZ_TuneCUETP8M1_13TeV-pythia8/%sv1/MINIAODSIM' % campaign, 22.82 ),
                'ZZ' : ('/ZZ_TuneCUETP8M1_13TeV-pythia8/%sv1/MINIAODSIM' % campaign, 10.32 ),
                'QCD' : ('/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/%sv1/MINIAODSIM' % campaign, 720648000 * 0.00042),
    }
    
    samplesDataCards = { 
                'data_em' : ('', -999.0),
                'data_tt' : ('', -999.0),
                'DYJets' : ('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%sv1/MINIAODSIM' % campaign, 6025.2 ), 
                'DYJetsLow' : ('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%sv1/MINIAODSIM' % campaign, 18610.0 ), 
                'T-tW' : ('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%sv2/MINIAODSIM' % campaign, 35.6 ),
                'T-tchan' : ('/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%sv1/MINIAODSIM' % campaign, 136.02 * 0.108*3 ),
                'TT' : ('/TT_TuneCUETP8M1_13TeV-powheg-pythia8/%sv1/MINIAODSIM' % campaign, 831.76 ),
                'Tbar-tW' : ('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%sv1/MINIAODSIM' % campaign, 35.6),
                'Tbar-tchan' : ('/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%sv1/MINIAODSIM' % campaign, 80.95 * 0.108*3 ),
                'WJets' : ('/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%sv1/MINIAODSIM' % campaign, 61526.7 ),
                'WW1l1nu2q' : ('/WWToLNuQQ_13TeV-powheg/%sv1/MINIAODSIM' % campaign, 49.997 ),
                'WW2l2nu' : ('/WWTo2L2Nu_13TeV-powheg/%sv1/MINIAODSIM' % campaign, 12.178 ),
                'WZ1l1nu2q' : ('/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/%sv1/MINIAODSIM' % campaign, 10.71 ),
                'WZ1l3nu' : ('/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/%sv1/MINIAODSIM' % campaign, 3.05 ),
                'WZ2l2q' : ('/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/%sv1/MINIAODSIM' % campaign, 5.595 ),
                'WZ3l1nu' : ('/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/%sv1/MINIAODSIM' % campaign, 4.42965 ),
                'ZZ2l2nu' : ('/ZZTo2L2Nu_13TeV_powheg_pythia8/%sv2/MINIAODSIM' % campaign, 0.564 ),
                'ZZ2l2q' : ('/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/%sv1/MINIAODSIM' % campaign, 3.22 ),
                'ZZ4l' : ('/ZZTo4L_13TeV-amcatnloFXFX-pythia8/%sv1/MINIAODSIM' % campaign, 1.212 ),
    }
    if grouping == 'Sync': samples = samplesSync
    if grouping == '25ns': samples = samples25ns
    if grouping == 'dataCards': samples = samplesDataCards
     
    dataSamples = {
                'data_em' : ['/MuonEG/Run2015C-23Sep2015-v1/MINIAOD', '/MuonEG/Run2015D-05Oct2015-v2/MINIAOD', '/MuonEG/Run2015D-PromptReco-v4/MINIAOD'],
                'data_tt' : ['/Tau/Run2015C-23Sep2015-v1/MINIAOD', '/Tau/Run2015D-05Oct2015-v1/MINIAOD', '/Tau/Run2015D-PromptReco-v4/MINIAOD'],
    }
    
    # A dictionary to store each samples info
    jDict = {}
    
    for k, v in samples.iteritems() :
        # Get the DAS info from DBS
        # Sum up data sets by channels
        if 'data' in k :
            dataSamps = dataSamples[ k ]
            infoDAS = [0, 0, 0, 0, u'ok']
            for samp in dataSamps :
                infoDAStmp = getDBSInfo( k, samp )
                infoDAS[0] += infoDAStmp[0]
                infoDAS[1] += infoDAStmp[1]
                infoDAS[2] += infoDAStmp[2]
                infoDAS[3] += infoDAStmp[3]
                if infoDAStmp[4] != u'ok' :
                    infoDAS[4] = 'error'
                print "Data: ", infoDAStmp
        else : infoDAS = getDBSInfo( k, v[0] )
        print infoDAS
    
        # Get the Ntuple info that FSA created
        numFiles = getNumberOfFiles( k, grouping )
        eventCount = 0
        summedWeights = 0
        summedWeightsNorm = 0
        inFiles = open('NtupleInputs_%s/%s.txt' % (grouping, k), 'r')
        for fileName in inFiles :
            eventCount += getEventCount( fileName.strip(), 'em' )
            w = getSummedWeights( fileName.strip(), 'em' )
            summedWeights += w[0]
            summedWeightsNorm += w[1]
        inFiles.close()
    
        # Check that DAS and FSA events and file numbers match
        status = "Error"
        if infoDAS[0] == numFiles : status = "Files Match"
        if infoDAS[2] == eventCount :
            status = "Good to Go!"
    
        infoNtup = [numFiles, int(eventCount), summedWeights, summedWeightsNorm, status]
        print infoNtup
    
        # Append each samples info to our dictionary jDict
        jDict[ k ] = {'DAS Path' : v[0], 'nfiles' : infoDAS[0], 'nblocks' : infoDAS[1], 'nevents' : infoDAS[2], 'nlumis' : infoDAS[3], 'DAS status' : infoDAS[4], 'nNtupleFiles' : infoNtup[0], 'nEvents' : infoNtup[1], 'summedWeights' : infoNtup[2], 'summedWeightsNorm' : infoNtup[3], 'STATUS' : infoNtup[4], 'Cross Section (pb)' : v[1] }
    
    # Print the dictionary to a JSON file
    printJson( jDict, grouping )

if __name__ == '__main__' :
    grouping = os.getenv('_GROUPING_', '25ns') # 25ns is default
    makeMetaJSON( grouping )
