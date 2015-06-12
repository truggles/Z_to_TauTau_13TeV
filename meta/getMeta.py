#!/usr/bin/env python

# Provides the functions to grab DAS info and build the json file which stores sample info

import json
import os
from das_query import das_query


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


def formatJson( name, DASpath, info = [] ) :
	with open('data.json', 'a') as outfile:
		json.dump( { name : [ {'DAS Path' : DASpath}, {'nfiles' : info[0]}, {'nblocks' : info[1]}, {'nevents' : info[2]}, {'nlumis' : info[3]}, {'status' : info[4]} ] }, outfile, indent=2 )
		outfile.close()

