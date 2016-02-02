#!/usr/bin/env python

# A script for building a JSON file containg relevant info for each sample
# June, 12 2015

import os
from getMeta import getDBSInfo, getNumberOfFiles, getEventCount, printJson, getSummedWeights



def makeMetaJSON( grouping, ch = 'em' ) :
    samplesSync = { 'Sync-HtoTT': ('/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 999) # c76x
    }
    
    ### Excellent Source: https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
    ### See Kenneth's Log Book for how to find this stuff on MCM: https://twiki.cern.ch/twiki/bin/view/Main/KDLLogBook#LogDay20150106
    
    # Cross Section updated on Aug 3, 2015 per HTT Twiki
    #            'data_tt' : ('/Tau/Run2015B-PromptReco-v1/MINIAOD', -999),
    #            'data_em' : ('/MuonEG/Run2015B-PromptReco-v1/MINIAOD', -999),
    
    # em enriched QCD has a filter efficiency applied to their cross sections
    c74x = 'RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2'
    c76x = 'RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12'
    samples25ns = { 
                'data_em' : ('', -999.0),
                'data_tt' : ('', -999.0),
                'ggHtoTauTau' : ('/GluGluHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c74x, 43.92 * 0.0632 ),
                'VBFHtoTauTau' : ('/VBFHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c74x, 3.748 * 0.0632 ),
                'DYJets' : ('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c74x, 6025.0 ), 
                'DYJetsLow' : ('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c74x, 18610.0 ), 
                'TTJets' : ('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%sv3/MINIAODSIM' % c74x, 831.76 ),
                'T-tW' : ('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%sv2/MINIAODSIM' % c74x, 35.6 ),
                'Tbar-tW' : ('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % c74x, 35.6),
                'WJets' : ('/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c74x, 61526.7 ),
                'WW' : ('/WW_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % c74x, 63.21 ),
                'WZJets' : ('/WZ_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % c74x, 22.82 ),
                'ZZ' : ('/ZZ_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % c74x, 10.32 ),
                'QCD' : ('/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/%s-v1/MINIAODSIM' % c74x, 720648000 * 0.00042),
    }
    
    # For QCD samples: https://github.com/cms-sw/genproductions/blob/master/python/ThirteenTeV/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8_cff.py
    samplesDataCards = { 
                'data_em' : ('', -999.0),
                'data_tt' : ('', -999.0),
                'ggHtoTauTau120' : ('/GluGluHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c76x, 43.92 * 0.0632 ),
                'ggHtoTauTau125' : ('/GluGluHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c76x, 43.92 * 0.0632 ),
                'ggHtoTauTau130' : ('/GluGluHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c76x, 43.92 * 0.0632 ),
                'VBFHtoTauTau120' : ('/VBFHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c76x, 3.748 * 0.0632 ),
                'VBFHtoTauTau125' : ('/VBFHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c76x, 3.748 * 0.0632 ),
                'VBFHtoTauTau130' : ('/VBFHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c76x, 3.748 * 0.0632 ),
                #'DYJets' : ('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 6025.2 ), 
                #'DYJetsLow' : ('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c76x, 18610.0 ), 
                'T-tW' : ('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%sv2/MINIAODSIM' % c76x, 35.6 ),
                'T-tchan' : ('/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % c76x, 136.02 * 0.108*3 ),
                'TT' : ('/TT_TuneCUETP8M1_13TeV-powheg-pythia8/%s_ext3-v1/MINIAODSIM' % c76x, 831.76 ),
                'Tbar-tW' : ('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % c76x, 35.6),
                #XXX#'Tbar-tchan' : ('/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % c76x, 80.95 * 0.108*3 ),
                #'WJets' : ('/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 61526.7 ),
                'WW1l1nu2q' : ('/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c76x, 49.997 ),
                'WZJets' : ('/WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c76x, 5.26 ),
                #'WW2l2nu' : ('/WWTo2L2Nu_13TeV-powheg/%s-v1/MINIAODSIM' % c74x, 12.178 ),
                #XXX#'WZ1l1nu2q' : ('/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c74x, 10.71 ),
                'WZ1l3nu' : ('/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c76x, 3.05 ),
                #'WZ2l2q' : ('/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c74x, 5.595 ),
                'WZ3l1nu' : ('/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/%s-v1/MINIAODSIM' % c74x, 4.42965 ),
                #'ZZ2l2nu' : ('/ZZTo2L2Nu_13TeV_powheg_pythia8/%sv2/MINIAODSIM' % c74x, 0.564 ),
                #XXX#'ZZ2l2q' : ('/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c74x, 3.22 ),
                'ZZ4l' : ('/ZZTo4L_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c76x, 1.212 ),
                #XXX#'QCD15-20' : ('/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/%s-v1/MINIAODSIM' % c74x, 1.27298e+09 * 0.00020 ), 
                #XXX#'QCD20-30' : ('/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/%s-v1/MINIAODSIM' % c74x, 5.57627e+08 * 0.00059 ),
                #XXX#'QCD30-80' : ('/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/%s-v1/MINIAODSIM' % c74x, 1.59068e+08 * 0.00255 ), 
                #XXX#'QCD80-170' : ('/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/%s-v1/MINIAODSIM' % c74x, 3.221e+06 * 0.01183 ), 
                #XXX#'QCD170-250' : ('/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8/%s-v1/MINIAODSIM' % c74x, 105771 * 0.02492 ), 
                #XXX#'QCD250-Inf' : ('/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/%s-v1/MINIAODSIM' % c74x, 21094.1 * 0.03375 ), 
                # The scale factor is for LO -> NNLO scaling see excel sheet below https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#MC_samples
                'WJets' : ('/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c76x, 50690 * 1.213783784),
                'WJets100-200' : ('/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 1345.0 * 1.213783784),
                'WJets200-400' : ('/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 359.7 * 1.213783784),
                'WJets400-600' : ('/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 48.91 * 1.213783784),
                'WJets600-Inf' : ('/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 18.77 * 1.213783784),
                'DYJets' : ('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 4895.0 * 1.230888662), 
                'DYJets100-200' : ('/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 139.4 * 1.230888662 ), 
                'DYJets200-400' : ('/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 42.75 * 1.230888662 ), 
                'DYJets400-600' : ('/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 5.497 * 1.230888662 ), 
                'DYJets600-Inf' : ('/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c76x, 2.21 * 1.230888662 ), 

                'DYJetsLow' : ('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c76x, 71310.0 ), 
                #'DYJetsLow100-200' : ('/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c74x, 224.2 ), 
                #'DYJetsLow200-400' : ('/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c74x, 37.2 ), 
                #'DYJetsLow400-600' : ('/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c74x, 3.581 ), 
                #'DYJetsLow600-Inf' : ('/DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c74x, 1.124 ), 
    }
    masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
    #masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 600, 900, 1000, 1200, 1500, 2000, 2900, 3200]
    samplesMSSM = {}
    for mass in masses :
       samplesMSSM['ggH%i' % mass] = ('/SUSYGluGluToHToTauTau_M-%i_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % (mass, c76x), 1 )
       samplesMSSM['bbH%i' % mass] = ('/SUSYGluGluToBBHToTauTau_M-%i_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % (mass, c76x), 1 )
       samplesDataCards['ggH%i' % mass] = ('/SUSYGluGluToHToTauTau_M-%i_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % (mass, c76x), 1 )
       samplesDataCards['bbH%i' % mass] = ('/SUSYGluGluToBBHToTauTau_M-%i_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % (mass, c76x), 1 )

    samplesTrigger = {
                'data_mt' : ('', -999.0),
                'ggHtoTauTau' : ('/GluGluHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c74x, 43.92 * 0.0632 ),
    }

    if grouping == 'Sync': samples = samplesSync
    if grouping == '25ns': samples = samples25ns
    if grouping == 'dataCards': samples = samplesDataCards
    if grouping == 'Trigger': samples = samplesTrigger
    if grouping == 'MSSM': samples = samplesMSSM
     
    dataSamples = {
                'data_em' : ['/MuonEG/Run2015D-16Dec2015-v1/MINIAOD'],
                'data_tt' : ['/Tau/Run2015D-16Dec2015-v1/MINIAOD'],
                'data_mt' : ['/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD', '/SingleMuon/Run2015D-PromptReco-v4/MINIAOD'],
    }

    sampleCodes = { # sample name : ( unique code, group ),
                # Groups are same as data cards: ZTT=1, TT=2, VV=3, WJets=4, QCD=5
                'data_em' : ( 1, 0),
                'data_tt' : ( 2, 0),
                'DYJets' : ( 3, 1),
                'DYJets100-200' : ( 94, 1),
                'DYJets200-400' : ( 95, 1),
                'DYJets400-600' : ( 96, 1),
                'DYJets600-Inf' : ( 97, 1),
                'DYJetsLow' : ( 98, 1),
                'T-tW' : ( 5, 3),
                'T-tchan' : ( 6, 3),
                'TT' : ( 7, 2),
                'Tbar-tW' : ( 8, 3),
                'Tbar-tchan' : ( 9, 3),
                'WJets' : ( 80, 4),
                'WJets100-200' : ( 81, 4),
                'WJets200-400' : ( 82, 4),
                'WJets400-600' : ( 83, 4),
                'WJets600-Inf' : ( 84, 4),
                'WW1l1nu2q' : ( 11, 3),
                'WW2l2nu' : ( 12, 3),
                'WZ1l1nu2q' : ( 13, 3),
                'WZ1l3nu' : ( 14, 3),
                'WZ2l2q' : ( 15, 3),
                'WZ3l1nu' : ( 16, 3),
                'WZJets' : ( 16.1, 3),
                'ZZ2l2nu' : ( 17, 3),
                'ZZ2l2q' : ( 18, 3),
                'ZZ4l' : ( 19, 3),
                'QCD15-20' : ( 20, 5),
                'QCD20-30' : ( 21, 5),
                'QCD30-80' : ( 22, 5),
                'QCD80-170' : ( 23, 5),
                'QCD170-250' : ( 24, 5),
                'QCD250-Inf' : ( 25, 5),
                'Sync-HtoTT' : ( 100, 100),
                'data_mt' : ( 101, 101),
                'ggHtoTauTau120' : ( 101, 99),
                'ggHtoTauTau125' : ( 102, 99),
                'ggHtoTauTau130' : ( 103, 99),
                'VBFHtoTauTau120' : ( 104, 99),
                'VBFHtoTauTau125' : ( 105, 99),
                'VBFHtoTauTau130' : ( 106, 99),
    }
    for mass in masses :
        sampleCodes['ggH%i' % mass] = (800, 800)
        sampleCodes['bbH%i' % mass] = (900, 900)
    
    
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
        else :
            try : infoDAS = getDBSInfo( k, v[0] )
            except IndexError :
                print "\n#######################################"
                print "IndexError for sample: %s" % k
                print "#######################################\n"
                continue
        print infoDAS
    
        # Get the Ntuple info that FSA created
        numFiles = getNumberOfFiles( k, grouping )
        eventCount = 0
        summedWeights = 0
        summedWeightsNorm = 0
        inFiles = open('NtupleInputs_%s/%s.txt' % (grouping, k), 'r')
        for fileName in inFiles :
            eventCount += getEventCount( fileName.strip(), ch )
            w = getSummedWeights( fileName.strip(), ch )
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
        jDict[ k ] = {'DAS Path' : v[0], 'nfiles' : infoDAS[0], 'nblocks' : infoDAS[1], 'nevents' : infoDAS[2], 'nlumis' : infoDAS[3], 'DAS status' : infoDAS[4], 'nNtupleFiles' : infoNtup[0], 'nEvents' : infoNtup[1], 'summedWeights' : infoNtup[2], 'summedWeightsNorm' : infoNtup[3], 'STATUS' : infoNtup[4], 'Cross Section (pb)' : v[1], 'UniqueID' : sampleCodes[k][0], 'BkgGroup' : sampleCodes[k][1] }
    
    # Print the dictionary to a JSON file
    printJson( jDict, grouping )

if __name__ == '__main__' :
    grouping = os.getenv('_GROUPING_', '25ns') # 25ns is default
    makeMetaJSON( grouping )
