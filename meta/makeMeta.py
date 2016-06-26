#!/usr/bin/env python

# A script for building a JSON file containg relevant info for each sample
# June, 12 2015

import os
from getMeta import getDBSInfo, getNumberOfFiles, getEventCount, printJson, getSummedWeights
from sampleNames import returnSampleDetails



def makeMetaJSON( analysis, ch = 'tt' ) :

    currentDASSamples = {
        'Sync' : ['Sync-HtoTT',],
        'htt' : ['DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh', 'DYJetsLow', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV', 'data_tt', 'VBFHtoTauTau120', 'VBFHtoTauTau125', 'VBFHtoTauTau130', 'ggHtoTauTau120', 'ggHtoTauTau125', 'ggHtoTauTau130']
    }

    samples = returnSampleDetails( analysis, currentDASSamples[ analysis ] )
    
    # A dictionary to store each samples info
    jDict = {}
    
    for k, v in samples.iteritems() :
        # Get the DAS info from DBS
        # Sum up data sets by channels
        #if 'data' in k :
        #    dataSamps = dataSamples[ k ]
        #    infoDAS = [0, 0, 0, 0, u'ok']
        #    for samp in dataSamps :
        #        infoDAStmp = getDBSInfo( k, samp )
        #        infoDAS[0] += infoDAStmp[0]
        #        infoDAS[1] += infoDAStmp[1]
        #        infoDAS[2] += infoDAStmp[2]
        #        infoDAS[3] += infoDAStmp[3]
        #        if infoDAStmp[4] != u'ok' :
        #            infoDAS[4] = 'error'
        #        print "Data: ", infoDAStmp
        #else :
        try : infoDAS = getDBSInfo( k, v['DASPath'] )
        except IndexError :
            print "\n#######################################"
            print "IndexError for sample: %s" % k
            print "#######################################\n"
            continue
        print infoDAS
    
        # Get the Ntuple info that FSA created
        numFiles = getNumberOfFiles( k, analysis )
        eventCount = 0
        summedWeights = 0
        summedWeightsNorm = 0
        inFiles = open('NtupleInputs_%s/%s.txt' % (analysis, k), 'r')
        try :
            for fileName in inFiles :
                eventCount += getEventCount( fileName.strip(), ch )
                w = getSummedWeights( fileName.strip(), ch )
                summedWeights += w[0]
                summedWeightsNorm += w[1]
        except AttributeError :
            print "\nAttributeError\n"
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
    makeMetaJSON( analysis )
