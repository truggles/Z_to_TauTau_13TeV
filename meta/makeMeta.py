#!/usr/bin/env python

# A script for building a JSON file containg relevant info for each sample
# June, 12 2015

import os
from getMeta import getDBSInfo, getNumberOfFiles, getEventCount, printJson

### Excellent Source: https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
### See Kenneth's Log Book for how to find this stuff on MCM: https://twiki.cern.ch/twiki/bin/view/Main/KDLLogBook#LogDay20150106
samples = { 'DYJets': ('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM', 6025 ), 
			'TTJets' : ('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 832 ),
			'QCD' : ('/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISpring15DR74-Asympt25nsRaw_MCRUN2_74_V9-v3/MINIAODSIM', 2022100000 ), # MCM
			'Tbar_tW' : ('/ST_tW_antitop_5f_mtop1755_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 35.6 ),
			'T_tW' : ('/ST_tW_top_5f_mtop1755_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 35.6 ),
			'HtoTauTau' : ('/GluGluToHToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM', 43.9 ),
			'VBF_HtoTauTau' : ('/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/MINIAODSIM', 3.7 ),
			'WJets' : ('/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 20509 ),
			'WW' : ('/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 110.8 ),
			'WZJets' : ('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 1.634 ),
			'ZZ' : ('/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM', 15.4 ),
#			'QCD15-20' : ('/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 1273000000 ),
#			'QCD20-30' : ('/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 557600000 ),
#			'QCD30-50' : ('/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 136000000 ),
#			'QCD50-80' : ('/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 19800000 ),
#			'QCD80-120' : ('/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM', 2800000 ),
#			'QCD-120-170' : ('/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 477000),
#			'QCD170-300' : ('/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 114000 ),
#			'QCD300-Inf' : ('/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM', 9000 ),
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
