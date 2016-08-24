'''
Based on TWiki instructions from Christian V.
https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#MC_samples
scroll to "Stitching of W+jets and Z+jets background samples binned in HT"
'''

import json


def openMetaJson( analysis ) :
    with open('meta/NtupleInputs_%s/samples.json' % analysis) as sampFile :
        sampDict = json.load( sampFile )
    return sampDict



def WJetsHTTWeight( lumi, sampDict ) :
    NNLOxsec = 61526.7
    LOtoNNLO = NNLOxsec / sampDict['WJets']['Cross Section (pb)']
    print "correction WJets:",LOtoNNLO
    binnedSamps = {
        '100-200' : 'WJets100-200',
        '200-400' : 'WJets200-400',
        '400-600' : 'WJets400-600',
        '600-Inf' : 'WJets600-Inf',
    }
    weights = {}
    wjetsLumi = sampDict['WJets']['summedWeightsNorm'] / sampDict['WJets']['Cross Section (pb)'] 
    weights['<100'] = lumi * LOtoNNLO * wjetsLumi
    for key in binnedSamps.keys() :
        sampLumi = sampDict[binnedSamps[key]]['summedWeightsNorm'] / sampDict[binnedSamps[key]]['Cross Section (pb)']
        weights[key] = lumi * LOtoNNLO / ( wjetsLumi + sampLumi )
    return weights 


    
def ZJetsHTTWeight( lumi, sampDict ) :
    NNLOxsec = 6025.2
    LOtoNNLO = NNLOxsec / sampDict['DYJets']['Cross Section (pb)']
    print "correction DYJets: ",LOtoNNLO
    binnedSamps = {
        '100-200' : 'DYJets100-200',
        '200-400' : 'DYJets200-400',
        '400-600' : 'DYJets400-600',
        '600-Inf' : 'DYJets600-Inf',
    }
    weights = {}
    dyjetsLumi = sampDict['DYJets']['summedWeightsNorm'] / sampDict['DYJets']['Cross Section (pb)'] 
    weights['<100'] = lumi * LOtoNNLO * dyjetsLumi
    for key in binnedSamps.keys() :
        sampLumi = sampDict[binnedSamps[key]]['summedWeightsNorm'] / sampDict[binnedSamps[key]]['Cross Section (pb)']
        weights[key] = lumi * LOtoNNLO / ( dyjetsLumi + sampLumi )
    return weights 


    
def ZJetsLowHTTWeight( lumi, sampDict ) :
    # This ones doesn't have a LO to NNLO correction factor
    binnedSamps = {
        '100-200' : 'DYJetsLow100-200',
        '200-400' : 'DYJetsLow200-400',
        '400-600' : 'DYJetsLow400-600',
        '600-Inf' : 'DYJetsLow600-Inf',
    }
    weights = {}
    dyjetsLumi = sampDict['DYJetsLow']['summedWeightsNorm'] / sampDict['DYJetsLow']['Cross Section (pb)'] 
    weights['<100'] = lumi * dyjetsLumi
    for key in binnedSamps.keys() :
        sampLumi = sampDict[binnedSamps[key]]['summedWeightsNorm'] / sampDict[binnedSamps[key]]['Cross Section (pb)']
        weights[key] = lumi / ( dyjetsLumi + sampLumi )
    return weights
    

if __name__ == '__main__' :
    analysis = 'htt'
    lumi = 2.2
    sampDict = openMetaJson( analysis )
    print sampDict
    print WJetsHTTWeight( lumi, sampDict )




