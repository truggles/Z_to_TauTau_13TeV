#!/usr/bin/env python

# Provides a method for building a json file from our samples
# June, 12 2015

import os
from getMeta import getDBSInfo, formatJson, getNumberOfFiles, getEventCount

samples = {'DYJets': '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 
			'TT' : '/TT_Tune4C_13TeV-pythia8-tauola/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM',
			'TTJets' : '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
			'QCD' : '/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Phys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1/MINIAODSIM', 
			'Tbar_tW' : '/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 
			'T_tW' : '/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 
			'HtoTauTau' : '/GluGluToHToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM', 
			'VBF_HtoTauTau' : '/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/MINIAODSIM', 
			'WJets' : '/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM', 
			'WW' : '/WWTo2L2Nu_CT10_13TeV-powheg-pythia8-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM', 
			'WZJets' : '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
}

ofile = open('data.json', 'w')
ofile.write('')
ofile.close()
for k, v in samples.iteritems() :
	# Get the DAS info from DBS
	infoDAS = getDBSInfo( k, v )
	print infoDAS

	# Get the Ntuple info that FSA created
	numFiles = getNumberOfFiles( k)
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

	# Send outputs to be JSONed and saved as data.json
	formatJson( k, v, infoDAS, infoNtup )

