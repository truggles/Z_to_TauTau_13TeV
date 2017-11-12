#!/usr/bin/env python

# A script for building a JSON file containg relevant info for each sample
# June, 12 2015

import os
from getMeta import getDBSInfo, getNumberOfFiles, getEventCount, printJson, getSummedWeights
from sampleNames import returnSampleDetails



def makeMetaJSON( analysis, channel = 'tt', skimmed=False ) :

    currentDASSamples = {
        'Sync' : ['Sync-SUSY160','Sync-VBF125','Sync-DYJets4', 'Sync-data2016RunB', 'Sync-data2016RunH', 'Sync-data2016All',],
        'azh' : ['dataEE-B', 'dataEE-C', 'dataEE-D', 'dataEE-E', 'dataEE-F', 'dataMM-B', 'dataMM-C', 'dataMM-D', 'dataMM-E', 'dataMM-F', 'ZZ4l', 'TT', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'WZ3l1nu', 'ZZ4lAMCNLO', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4m', 'ggZZ4tau', 'WWW'],
        'htt' : ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJets1Low', 'DYJets2Low', 'EWKWPlus', 'EWKWMinus', 'EWKZ2l', 'EWKZ2nu', 'WWW', 'WWZ', 'WZZ', 'ZZZ', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'ZZ2l2q', 'ZZ4l', 'VV', 'dataTT-B', 'dataTT-C', 'dataTT-D', 'dataTT-E', 'dataTT-F', 'dataTT-G', 'dataTT-H', 'WZ3l1nu'], # just removed WZJets, ZZ4l, WW, WZ, ZZ
    }

    # SM-HTT
    for mass in [110, 120, 125, 130, 140] :
        currentDASSamples['htt'].append('ggHtoTauTau%i' % mass)
        currentDASSamples['htt'].append('VBFHtoTauTau%i' % mass)
        currentDASSamples['htt'].append('WMinusHTauTau%i' % mass)
        currentDASSamples['htt'].append('WPlusHTauTau%i' % mass)
        currentDASSamples['htt'].append('ZHTauTau%i' % mass)
    
    for mass in [120, 125, 130] :
        currentDASSamples['azh'].append('ggHtoTauTau%i' % mass)
        currentDASSamples['azh'].append('VBFHtoTauTau%i' % mass)
        currentDASSamples['azh'].append('WMinusHTauTau%i' % mass)
        currentDASSamples['azh'].append('WPlusHTauTau%i' % mass)
        currentDASSamples['azh'].append('ZHTauTau%i' % mass)
        currentDASSamples['azh'].append('ttHTauTau125%i' % mass)

    # These are the background like Higgs samples
    currentDASSamples['htt'].append('ttHTauTau125')
    currentDASSamples['htt'].append('HtoWW2l2nu125')
    currentDASSamples['htt'].append('VBFHtoWW2l2nu125')

    # A to Zh sample masses
    for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
        currentDASSamples['azh'].append('azh%i' % mass)

    # Adding anomalous couplings VBF Higgs, these are normalized based on VBF125
    anomalous = ['HtoTauTau0PHf05ph0125', 'HtoTauTau0L1f05ph0125', 'HtoTauTau0L1125',
        'HtoTauTau0PM125', 'HtoTauTau0Mf05ph0125', 'HtoTauTau0PH125', 'HtoTauTau0M125']
    for aHiggs in anomalous :
        currentDASSamples['htt'].append( 'VBF'+aHiggs )
        currentDASSamples['htt'].append( 'W'+aHiggs )
        currentDASSamples['htt'].append( 'Z'+aHiggs )
    # New ggH test samples
    currentDASSamples['htt'].append( 'ggH125-sm' )
    currentDASSamples['htt'].append( 'ggH125-pseudoscalar' )
    currentDASSamples['htt'].append( 'ggH125-maxmix' )

    samples = returnSampleDetails( analysis, currentDASSamples[ analysis ] )

    
    # A dictionary to store each samples info
    jDict = {}
    
    for k, v in samples.iteritems() :
        # Get the DAS info from DBS
        try : infoDAS = getDBSInfo( k, v['DASPath'] )
        except IndexError :
            print "\n#######################################"
            print "DAS didn't work: IndexError for sample: %s" % k
            print "#######################################\n"
            continue
        print infoDAS
    
        # Because of using a single channel skim to find all our events
        # and some data sets don't do other channels well, we have 
        # to be able to override the channel
        chanToUse = channel
        if 'dataMM' in k : chanToUse = 'mmmt'

        # Get the Ntuple info that FSA created
        eventCount = 0
        summedWeights = 0
        summedWeightsNorm = 0
        if skimmed :
            fileName = 'NtupleInputs_%s/skimmed/%s_%s.txt' % (analysis, k, chanToUse)
        else :
            fileName = 'NtupleInputs_%s/%s.txt' % (analysis, k)
        inFiles = open( fileName, 'r')
        numFiles = getNumberOfFiles( fileName )
        try :
            for fileName in inFiles :
                eventCount += getEventCount( fileName.strip(), chanToUse )
                w = getSummedWeights( fileName.strip(), chanToUse )
                summedWeights += w[0]
                summedWeightsNorm += w[1]
        except AttributeError :
            print "\nAttributeError, maybe channel is wrong: %s\n" % chanToUse
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
