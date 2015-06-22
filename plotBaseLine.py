import ROOT
import json
import cutsBaseSelection as bc

ROOT.gROOT.SetBatch(True)

with open('meta/data.json') as sampFile :
	sampDict = json.load( sampFile )

genHistos = bc.getGeneralHistoDict()

samples = ['DYJets', 'Tbar_tW', 'T_tW', 'WW', 'WJets', 'TT', 'TTJets', 'HtoTauTau', 'VBF_HtoTauTau', 'WZJets', 'QCD']
channels = ['em', 'tt']


for channel in channels :
	if channel == 'em' : chanHistos = bc.getEMHistoDict() 
	if channel == 'tt' : chanHistos = bc.getTTHistoDict()

	varList = []
	for var in genHistos.keys() :
		varList.append( genHistos[ var ][0] )
	for var in chanHistos.keys() :
		varList.append( chanHistos[ var ][0] )
	#varList.append( 'Initial' )

	print channel
	cutMap = bc.getCutMap( channel )
	cutMap['Initial'] = '' # this is to plot the initial state before cuts
	cutMapLen = len( cutMap )
	cutCount = 0
	for cut in cutMap.keys() :
		cutCount += 1
		if cutCount == cutMapLen: cutCount = 0
		print "### %s ###" % cut
		for var in varList :
			print var
			c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s, %s" % (cut, channel, var), 1200, 800)
			pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
			pad1.Draw()
			pad1.Divide( 4, 3 )
			pad1.Update()

			dyj = ROOT.TH1F()
			tbar = ROOT.TH1F()


			count = 1
			for sample in samples :
				print sample
				pad1.cd( count )	
				tFile = ROOT.TFile('baseSelectionRootSolstice/%s.root' % sample, 'READ')
				dic = tFile.Get('%s_%s' % ( channel, cut ) )
				hist = dic.Get('%s' % var )
				hist.SetTitle("%s" % sample )
				hist.SetFillColor( ROOT.kBlue )
				hist.Draw()
				hist.SetDirectory( 0 )
				pad1.cd()
				pad1.Update()
				count += 1

			c1.SaveAs('basePlots/%s/%s_%s_%s.png' % (channel, var, str( cutCount ), cut) )
			c1.Close()
