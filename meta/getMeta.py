#!/usr/bin/env python

# Provides the functions to grab DAS info and build the json file which stores sample info

import json
import os
from das_query import das_query
import ROOT
from ROOT import TFile
import time


def getDBSInfo( key, name ) :
    query = "summary dataset=%s" % name
    print query
    try: results = das_query( query )
    except "DAS query returned result status fail" :
        print "DAS query failed initially, sleeping for 60 seconds, then retry"
        time.sleep( 60 )
        results = das_query( query )
    
    status = results['status']
    nfiles = results['data'][0]['summary'][0]['nfiles']
    nblocks = results['data'][0]['summary'][0]['nblocks']
    nevents = results['data'][0]['summary'][0]['nevents']
    nlumis = results['data'][0]['summary'][0]['nlumis']
    
    infoVect = [ nfiles, nblocks, nevents, nlumis, status ]
    return infoVect



def getNumberOfFiles( fileName ) :
    try:
        ifile = open( fileName, 'r')
        fileCount = 0
        for line in ifile:
        	fileCount += 1
    except IOError :
        time.sleep( 10 )
        ifile = open( fileName, 'r')
        fileCount = 0
        for line in ifile:
        	fileCount += 1
        
    return fileCount



def getEventCount( fileName, channel ) :
	ifile = ROOT.TFile('%s' % fileName, 'r')
	eventCount = 0
	hist = ifile.Get( '%s/eventCount' % channel )
	#eventCount = ntuple.Get('eventCount')
	eventCount = hist.Integral()
	ifile.Close()
	return eventCount



def getSummedWeights( fileName, channel ) :
    ifile = ROOT.TFile('%s' % fileName, 'r')
    summedWeights = 0
    summedWeights = ifile.Get( '%s/summedWeights' % channel ).Integral()

    # Normalize summedWeights by GenWeight value
    tree2 = ifile.Get( '%s/final/Ntuple' % channel )
    if tree2.GetEntries() == 0 and not 'data' in fileName.split('/')[0] :
        # If tree length == 0, check if this is a non-data file
        # if it is non-data try other channel
        # (happened for ggZZ4m when running on channel eeet 
        nFileName = fileName.replace( channel, 'mmmt' )
        print "\nNon-data file with TTree length == 0"
        print " -- Checking file from other channel:"
        print " -- previous file: ",fileName
        #print " -- new file: ",nFileName,"\n"
        print " -- In case you have different length file lists"
        print " -- you will need to go edit the summedWieghts manually, sorry"
        #return getSummedWeights( nFileName, 'mmmt' )
        return (-999999,-999999)
    tree2.GetEntry( 1 )
    weight = abs( tree2.GenWeight )
    #print "weight: ",weight
    if weight != 0 :
        weightedSum = summedWeights/weight
    else :
        weightedSum = -999
    #print "summed w/w: ",weightedSum
    ifile.Close()
    return (summedWeights,weightedSum)



def printJson( jDict, sampPrefix ) :
	with open('NtupleInputs_%s/samples.json' % sampPrefix, 'w') as outFile :
		json.dump( jDict, outFile, indent=2 )
		outFile.close()



