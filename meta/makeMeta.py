#!/usr/bin/env python

# A script for building a JSON file containg relevant info for each sample
# June, 12 2015

import os
from getMeta import getDBSInfo, getNumberOfFiles, getEventCount, printJson, getSummedWeights
from sampleNames import returnSampleDetails



def makeMetaJSON( analysis, channel = 'tt', skimmed=False ) :

    currentDASSamples = {
        'Sync' : ['Sync-HtoTT',],
        'htt' : ['DYJetsAMCNLO', 'DYJets', 'DYJetsAMCNLOReHLT', 'DYJetsOld', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'EWKWPlus', 'EWKWMinus', 'EWKZ2l', 'EWKZ2nu', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'dataTT-B', 'dataTT-C', 'dataTT-D', 'dataTT-E', 'dataTT-F', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130'],
        'azh' : ['dataEE', 'dataMM', 'ZZ4l', 'TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'ZZ4lAMCNLO', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4m', 'ggZZ4tau', 'WMinusHTauTau', 'WPlusHTauTau', 'ZHTauTau', 'ttHTauTau'],
    }

    # A to Zh sample masses
    for mass in [220, 240, 260, 280, 300, 320, 350, 400] :
        currentDASSamples['azh'].append('azh%i' % mass)

    samples = returnSampleDetails( analysis, currentDASSamples[ analysis ] )

    
    # A dictionary to store each samples info
    jDict = {}
    
    for k, v in samples.iteritems() :
        # Get the DAS info from DBS
        try : infoDAS = getDBSInfo( k, v['DASPath'] )
        except IndexError :
            print "\n#######################################"
            print "IndexError for sample: %s" % k
            print "#######################################\n"
            continue
        print infoDAS
    
        # Get the Ntuple info that FSA created
        eventCount = 0
        summedWeights = 0
        summedWeightsNorm = 0
        if skimmed :
            fileName = 'NtupleInputs_%s/skimmed/%s_%s.txt' % (analysis, k, channel)
        else :
            fileName = 'NtupleInputs_%s/%s.txt' % (analysis, k)
        inFiles = open( fileName, 'r')
        numFiles = getNumberOfFiles( fileName )
        try :
            for fileName in inFiles :
                eventCount += getEventCount( fileName.strip(), channel )
                w = getSummedWeights( fileName.strip(), channel )
                summedWeights += w[0]
                summedWeightsNorm += w[1]
        except AttributeError :
            print "\nAttributeError, maybe channel is wrong: %s\n" % channel
            continue
            inFiles.close()
        inFiles.close()
    
        # Check that DAS and FSA events and file numbers match
        status = "Error"
        if infoDAS[0] == numFiles : status = "Files Match"
        if infoDAS[2] == eventCount :
            status = "Good to Go!"
    
        infoNtup = [numFiles, int(eventCount), summedWeights, summedWeightsNorm, status]
        print infoNtup
    
        # Append each samples info to our dictionary jDict
        jDict[ k ] = {'DAS Path' : v['DASPath'], 'nfiles' : infoDAS[0], 'nblocks' : infoDAS[1], 'nevents' : infoDAS[2], 'nlumis' : infoDAS[3], 'DAS status' : infoDAS[4], 'nNtupleFiles' : infoNtup[0], 'nEvents' : infoNtup[1], 'summedWeights' : infoNtup[2], 'summedWeightsNorm' : infoNtup[3], 'STATUS' : infoNtup[4], 'Cross Section (pb)' : v['xsec'] }
    
    # Print the dictionary to a JSON file
    printJson( jDict, analysis )

if __name__ == '__main__' :
    analysis = os.getenv('_GROUPING_', 'htt') # 25ns is default
    if analysis == 'htt' :
        makeMetaJSON( analysis )
    if analysis == 'azh' :
        makeMetaJSON( analysis, 'eeet' )
