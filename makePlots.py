from util.buildTChain import makeTChain
import ROOT
import json

ROOT.gROOT.SetBatch(True)

with open('meta/data.json') as sampFile :
	sampDict = json.load( sampFile )

prodMap = { 'em' : ('e', 'm'),
			 'tt' : ('t1', 't2')
}
				# Sample : Color
sampleColors = { 'DYJets': 'kBlack',
			'TT' : 'kBlue-8',
			'TTJets' : 'kBlue-2',
			'QCD' : 'kMagenta-10',
			'Tbar_tW' : 'kYellow-2',
			'T_tW': 'kYellow+2',
			'HtoTauTau': 'kRed+2',
			'VBF_HtoTauTau': 'kRed-2',
			'WJets' : 'kAzure+2',
			'WW' : 'kAzure+10',
			'WZJets': 'kAzure-4',
}

varMapEM = {"Z Pt" : ('e_m_Pt', 10, 200, 0),
#			"Z Mass" : ('e_m_Mass', 8, 130, 50),
#			"Electron Pt" : ('ePt', 10, 200, 0),
#			"Electron Eta" : ('eEta', 12, 3., -3),
#			"Muon Pt" : ('mPt', 10, 200, 0),
#			"Muon Eta" : ('mEta', 12, 3., -3.),
#			"PF Met" : ('pfMetEt', 10, 200, 0),
#			"Jet Multiplicity" : ('jetVeto30_DR05', 10, 10, 0),
}		

varMapTT = {"Z Pt" : ('t1_t2_Pt', 10, 200, 0),
#			"Z Mass" : ('t1_t2_Mass', 8, 130, 50),
#			"#tau_{h1} Pt" : ('t1Pt', 10, 200, 0),
#			"#tau_{h1} Eta" : ('t1Eta', 30, 3., -3.),
#			"#tau_{h2} Pt" : ('t2Pt', 10, 200, 0),
#			"#tau_{h2} Eta" : ('t2Eta', 30, 3., -3),
#			"PF Met" : ('pfMetEt', 10, 200, 0),
#			"Jet Multiplicity" : ('jetVeto30_DR05', 10, 10, 0),
}		
samples = ['Tbar_tW', 'T_tW', 'WW', 'WJets', 'TT', 'TTJets', 'HtoTauTau', 'VBF_HtoTauTau', 'WZJets', 'DYJets', 'QCD']
#samples = ['TT', 'QCD', 'Tbar_tW', 'T_tW', 'HtoTauTau', 'VBF_HtoTauTau', 'WJets', 'WW', 'WZJets']

for channel in prodMap.keys() :
	print channel
	if channel == 'em': varMap = varMapEM
	if channel == 'tt': varMap = varMapTT
	for var in varMap :
		print var
		varBin = varMap[ var ][1]
		print varBin
		varRange = varMap[ var ][2]
		print varRange
		varMin = varMap[ var ][3]
		stack = ROOT.THStack("All Backgrounds", "%s, %s" % (channel, var) )
		print varMap[ var ][0]

		for sample in samples:
			print sample
			hist = ROOT.TH1F("%s_%s_%s" % (channel, sample, var), "%s %s %s" % (channel, sample, var), varBin, varMin, varRange)

			tFile = ROOT.TFile('baseSelectionRoot/%s.root' % sample, 'READ')
			tree = tFile.Get('%s/Ntuple' % channel)
			for row in tree :
				hist.Fill( getattr( row, '%s' % varMap[ var ][0] ) )
			color = "ROOT.%s" % sampleColors[ sample ]
			hist.SetFillColor( eval( color ) )
			hist.SetLineColor( ROOT.kBlack )
			#hist.SaveAs('plots/%s/%s.root' % (channel, sample) )

			# Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data )
			if hist.Integral() != 0:
				hist.Scale( ( hist.Integral() * 1000 * sampDict[ sample ]['Cross Section (pb)'] ) / ( hist.Integral() * sampDict[ sample ]['nevents'] ) )

			print hist.Integral()
			stack.Add( hist )
			tFile.Close()
		
		#finalPlot = ROOT.TH1F("final_plot", "Z -> #tau#tau, %s, %s" % (channel, var), varBin, 0, varRange)
		c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 600, 600)
		pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
		pad1.Draw()
		pad1.cd()

		stack.Draw('hist')
		stack.GetXaxis().SetTitle("%s (GeV)" % var)
		stack.GetYaxis().SetTitle("Events / %s (GeV)" % ( str( round(varRange / varBin,1) ) ) )
		stack.SetMinimum( 0.1 )

		# Set axis and viewing area
		pad1.SetLogy()
		pad1.BuildLegend()

		pad1.Update()
		c1.SaveAs('plots/%s/%s.png' % (channel, varMap[ var ][0] ) )
		c1.Close()

# Get histos from samples


# Scale histos


# Plot histos

#TT = ROOT.TH1F("%s_TT_%s" % (channel, var), "%s TT %s" % (channel, var), varBin, 0, varRange)
#TTJets = ROOT.TH1F("%s_TTJets_%s" % (channel, var), "%s TTJets %s" % (channel, var), varBin, 0, varRange)
#QCD = ROOT.TH1F("%s_QCD_%s" % (channel, var), "%s QCD %s" % (channel, var), varBin, 0, varRange)
#Tbar_tW = ROOT.TH1F("%s_Tbar_tW_%s" % (channel, var), "%s Tbar_tW %s" % (channel, var), varBin, 0, varRange)
#T_tW = ROOT.TH1F("%s_T_tW_%s" % (channel, var), "%s T_tW %s" % (channel, var), varBin, 0, varRange)
#HtoTauTau = ROOT.TH1F("%s_HtoTauTau_%s" % (channel, var), "%s HtoTauTau %s" % (channel, var), varBin, 0, varRange)
#VBF_HtoTauTau = ROOT.TH1F("%s_VBF_HtoTauTau_%s" % (channel, var), "%s VBF_HtoTauTau %s" % (channel, var), varBin, 0, varRange)
#WJets = ROOT.TH1F("%s_WJets_%s" % (channel, var), "%s WJets %s" % (channel, var), varBin, 0, varRange)
#WW = ROOT.TH1F("%s_WW_%s" % (channel, var), "%s WW %s" % (channel, var), varBin, 0, varRange)
#WZJets = ROOT.TH1F("%s_WZJets_%s" % (channel, var), "%s WZJets %s" % (channel, var), varBin, 0, varRange)
		##stack.SaveAs('plots/%s/stack.root' % channel )
		#signal = ROOT.TH1F("DYJets_%s_%s" % (channel, var), "%s DYJets %s" % (channel, var), varBin, varMin, varRange)
		#sigFile = ROOT.TFile('baseSelectionRoot/DYJets.root', 'READ')
		#tree = sigFile.Get('%s/Ntuple' % channel)
		#for row in tree :
		#	signal.Fill( getattr( row, '%s' % varMap[ var ][0] ) )
		#signal.SetLineColor( ROOT.kGreen )
		#signal.SetLineWidth( 2 )
		##signal.SaveAs('plots/%s/DYJets.root' % channel )
		#sigFile.Close()
		#signal.Draw('hist same')

