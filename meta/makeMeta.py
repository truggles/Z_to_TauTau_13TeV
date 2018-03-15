#!/usr/bin/env python

# A script for building a JSON file containg relevant info for each sample
# June, 12 2015

import os
from getMeta import getDBSInfo, getNumberOfFiles, getEventCount, printJson, getSummedWeights
from sampleNames import returnSampleDetails
from analysis1BaselineCuts import skipChanDataCombo



def makeMetaJSON( analysis, channel = 'tt', skimmed=False ) :

    currentDASSamples = {
        'Sync' : ['Sync-SUSY160','Sync-VBF125','Sync-DYJets4', 'Sync-data2016RunB', 'Sync-data2016RunH', 'Sync-data2016All',],
        'azh' : ['ttZ', 'ttZ2', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'TT', 'WWW', 'WWZ', 'WZ3l1nu', 'WZZ', 'WZ', 'ZZ4l', 'ZZZ',], # May 31 samples, no ZZ->all, use ZZ4l
        'htt' : ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJets1Low', 'DYJets2Low', 'EWKWPlus', 'EWKWMinus', 'EWKZ2l', 'EWKZ2nu', 'WWW', 'WWZ', 'WZZ', 'ZZZ', 'T-tchan', 'Tbar-tchan', 'TT', 'Tbar-tW', 'T-tW', 'WJets', 'WJets1', 'WJets2', 'WJets3', 'WJets4', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'ZZ2l2q', 'ZZ4l', 'VV', 'WZ3l1nu'], # just removed WZJets, ZZ4l, WW, WZ, ZZ
    }

    # Data
    for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
        currentDASSamples['htt'].append('dataTT-%s' % era)
        currentDASSamples['azh'].append('dataEE-%s' % era)
        currentDASSamples['azh'].append('dataMM-%s' % era)
        currentDASSamples['azh'].append('dataSingleE-%s' % era)
        currentDASSamples['azh'].append('dataSingleM-%s' % era)

    # SM-HTT
    for mass in [110, 120, 125, 130, 140] :
        for ana in ['htt', 'azh'] :
            currentDASSamples[ ana ].append('ggHtoTauTau%i' % mass)
            currentDASSamples[ ana ].append('VBFHtoTauTau%i' % mass)
            currentDASSamples[ ana ].append('WMinusHTauTau%i' % mass)
            currentDASSamples[ ana ].append('WPlusHTauTau%i' % mass)
            currentDASSamples[ ana ].append('ZHTauTau%i' % mass)
    
    # These are the background like Higgs samples
    currentDASSamples['htt'].append('ttHTauTau125')
    currentDASSamples['htt'].append('HtoWW2l2nu125')
    currentDASSamples['htt'].append('VBFHtoWW2l2nu125')

    currentDASSamples['azh'].append('ZHWW125')
    currentDASSamples['azh'].append('HZZ125')
    currentDASSamples['azh'].append('VBFHtoWW2l2nu125')
    currentDASSamples['azh'].append('HtoWW2l2nu125')
    currentDASSamples['azh'].append('WMinusHHWW125')
    currentDASSamples['azh'].append('WPlusHHWW125')
    currentDASSamples['azh'].append('ttHTauTau125')
    currentDASSamples['azh'].append('ttHNonBB125')
    currentDASSamples['azh'].append('ttHJNonBB125')

    # A to Zh sample masses
    for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
        currentDASSamples['azh'].append('azh%i' % mass)

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
        ''' today try getting info for all channels '''
        if analysis == 'azh' : channels = ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'] # 8 Normal
        else : channels = ['tt',]
        
        chanMap = {}
        for channel in channels :
            if skipChanDataCombo( channel, k, analysis ) :
                chanInfoNtup = [-9, -9, -9, -9, 'N/A']
            else :

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
                    chanInfoNtup = [-9, -9, -9, -9, 'N/A']
                inFiles.close()
    
                # Check that DAS and FSA events and file numbers match
                status = "Error"
                if infoDAS[0] == numFiles : status = "Files Match"
                if infoDAS[2] == eventCount :
                    status = "Good to Go!"
            
            infoNtupMap = {
                'nNtupleFiles' : numFiles,
                'nEvents' : int(eventCount),
                'summedWeights' : summedWeights,
                'summedWeightsNorm' : summedWeightsNorm,
                'STATUS' : status
            }
            print channel, infoNtupMap
            chanMap[ channel ] = infoNtupMap
    
        # Append each samples info to our dictionary jDict
        jDict[ k ] = {'DAS Path' : v['DASPath'], 'nDASFiles' : infoDAS[0], 'nDASEvents' : infoDAS[2], 'nDASLumis' : infoDAS[3], 'DAS Status' : infoDAS[4], 'Cross Section (pb)' : v['xsec'] }
        for channel in channels :
            jDict[ k ][ channel ] = chanMap[ channel ]
    
    # Print the dictionary to a JSON file
    printJson( jDict, analysis )

if __name__ == '__main__' :
    analysis = os.getenv('_GROUPING_', 'htt') # 25ns is default
    if analysis == 'htt' :
        makeMetaJSON( analysis )
    if analysis == 'azh' :
        makeMetaJSON( analysis, 'eeet' )
