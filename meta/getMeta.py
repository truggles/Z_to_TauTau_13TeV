#!/usr/bin/env python

# Provides the functions to grab DAS info and build the json file which stores sample info

import json
import os
from das_query import das_query
import ROOT
from ROOT import TFile


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

def getNumberOfFiles( name ) :
	ifile = open('NtupleInputs/%s.txt' % name, 'r')
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

def formatJson( name, DASpath, info = [], info2 = []) :
	with open('data.json', 'a') as outfile:
		json.dump( { name : {'DAS Path' : DASpath, 'nfiles' : info[0], 'nblocks' : info[1], 'nevents' : info[2], 'nlumis' : info[3], 'DAS status' : info[4], 'nNtupleFiles' : info2[0], 'nEventsEM' : info2[1], 'nEventsTT' : info2[2], 'STATUS' : info2[3] } }, outfile, indent=2 )
		outfile.close()

