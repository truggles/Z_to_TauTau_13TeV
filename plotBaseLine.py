import ROOT
import json
import cutsBaseSelection as bc

ROOT.gROOT.SetBatch(True)

with open('meta/data.json') as sampFile :
	sampDict = json.load( sampFile )

genHistos = bc.getGeneralHistoDict()
eeHistos = bc.getEMHistoDict() 
ttHistos = bc.getTTHistoDict()

samples = ['Tbar_tW', 'T_tW', 'WW', 'WJets', 'TT', 'TTJets', 'HtoTauTau', 'VBF_HtoTauTau', 'WZJets', 'DYJets', 'QCD']

channels = ['em', 'tt']


for channel in channels :
	print channel
	cutMap = bc.getCutMap( channel )
	for cut in cutMap.keys() :
		print cut
		for var in genHistos.keys() :
			print var
			c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s, %s" % (cut, channel, var), 1200, 800)
			pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
			pad1.Draw()
			pad1.Divide( 4, 3 )
			pad1.Update()

			count = 1
			for sample in samples :
				print sample
				tFile = ROOT.TFile('baseSelectionRootSolstice/%s.root' % sample, 'READ')
				dic = tFile.Get('%s_%s' % ( channel, cut ) )
				hist = dic.Get('%s' % var )
				hist.SetTitle("%s" % sample )

				pad1.cd( count )	
				hist.Draw()
				hist.SetFillColor( ROOT.kBlue )
				pad1.cd()
				pad1.Update()
				count += 1

			c1.SaveAs('basePlots/%s/%s_%s.png' % (channel, cut, var) )
			c1.Close()

