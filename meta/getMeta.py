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
	results = das_query( query )
	
	status = results['status']
	nfiles = results['data'][0]['summary'][0]['nfiles']
	nblocks = results['data'][0]['summary'][0]['nblocks']
	nevents = results['data'][0]['summary'][0]['nevents']
	nlumis = results['data'][0]['summary'][0]['nlumis']

	infoVect = [ nfiles, nblocks, nevents, nlumis, status ]
	return infoVect

def getNumberOfFiles( name, sampPrefix ) :
    try:
        ifile = open('NtupleInputs_%s/%s.txt' % (sampPrefix, name), 'r')
        fileCount = 0
        for line in ifile:
        	fileCount += 1
    except IOError :
        time.sleep( 10 )
        ifile = open('NtupleInputs_%s/%s.txt' % (sampPrefix, name), 'r')
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
    tree = ifile.Get( '%s/metaInfo' % channel )
    for row in tree :
        summedWeights += row.summedWeights
    #print "summed weights: ",summedWeights

    # Normalize summedWeights by GenWeight value
    tree2 = ifile.Get( '%s/final/Ntuple' % channel )
    tree2.GetEntry( 1 )
    weight = abs( tree2.GenWeight )
    #print "weight: ",weight
    weightedSum = summedWeights/weight
    #print "summed w/w: ",weightedSum
    ifile.Close()
    return (summedWeights,weightedSum)

def printJson( jDict, sampPrefix ) :
	with open('NtupleInputs_%s/samples.json' % sampPrefix, 'w') as outFile :
		json.dump( jDict, outFile, indent=2 )
		outFile.close()

