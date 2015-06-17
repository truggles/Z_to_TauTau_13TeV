#!/usr/bin/env python

# A script for building a JSON file containg relevant info for each sample
# June, 12 2015

import os
from getMeta import getDBSInfo, getNumberOfFiles, getEventCount, printJson

samples = { 'DYJets': ('/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 6025 ), 
			'TT' : ('/TT_Tune4C_13TeV-pythia8-tauola/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM', 832 ),
			'TTJets' : ('/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 832 ),
			'QCD' : ('/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Phys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1/MINIAODSIM', 125000000000 ),
			'Tbar_tW' : ('/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 35.6 ),
			'T_tW' : ('/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 35.6 ),
			'HtoTauTau' : ('/GluGluToHToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM', 43.9 ),
			'VBF_HtoTauTau' : ('/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/MINIAODSIM', 3.7 ),
			'WJets' : ('/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 20509 ),
			'WW' : ('/WWTo2L2Nu_CT10_13TeV-powheg-pythia8-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM', 110.8 ),
			'WZJets' : ('/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 1.634 ),
}

# A dictionary to store each samples info
jDict = {}

for k, v in samples.iteritems() :
	# Get the DAS info from DBS
	infoDAS = getDBSInfo( k, v[0] )
	print infoDAS

	# Get the Ntuple info that FSA created
	numFiles = getNumberOfFiles( k )
	eventCountEM = 0
	eventCountTT = 0
	inFiles = open('NtupleInputs/%s.txt' % k, 'r')
	for fileName in inFiles :
		eventCountEM += getEventCount( fileName.strip(), 'em' )
		eventCountTT += getEventCount( fileName.strip(), 'tt' )
	inFiles.close()

	# Check that DAS and FSA events and file numbers match
	status = "Error"
	if infoDAS[0] == numFiles and infoDAS[2] == eventCountEM and eventCountEM == eventCountTT:
		status = "Good to Go!"

	infoNtup = [numFiles, int(eventCountEM), int(eventCountTT), status]
	print infoNtup

	# Append each samples info to our dictionary jDict
	jDict[ k ] = {'DAS Path' : v[0], 'nfiles' : infoDAS[0], 'nblocks' : infoDAS[1], 'nevents' : infoDAS[2], 'nlumis' : infoDAS[3], 'DAS status' : infoDAS[4], 'nNtupleFiles' : infoNtup[0], 'nEventsEM' : infoNtup[1], 'nEventsTT' : infoNtup[2], 'STATUS' : infoNtup[3], 'Cross Section (pb)' : v[1] }

# Print the dictionary to a JSON file
printJson( jDict )	
