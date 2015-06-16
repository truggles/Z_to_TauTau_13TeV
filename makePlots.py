from util.buildTChain import makeTChain
import ROOT
import json

ROOT.gROOT.SetBatch(True)

with open('meta/data.json') as xSecFile :
	xSecs = json.load( xSecFile )
print xSecs['TT']['nevents']
#print xSecs

prodMap = { 'em' : ('e', 'm'),
			 'tt' : ('t1', 't2')
}
				# Sample : Color , Cross Section in (pb) XXX Check these
sampleColors = { 'DYJets': ('kBlack', 6025),
			'TT' : ('kBlue-8', 832),
			'TTJets' : ('kBlue-2', 832),
			'QCD' : ('kMagenta-10', 125000000000),
			'Tbar_tW': ('kYellow-2', 35.6),
			'T_tW': ('kYellow+2', 35.6),
			'HtoTauTau': ('kRed+2', 43.9),
			'VBF_HtoTauTau': ('kRed-2', 3.7),
			'WJets' : ('kAzure+2', 20509),
			'WW' : ('kAzure+10', 110.8),
			'WZJets': ('kAzure-4', 1.634),
}

varMapEM = {"Z Pt" : ('e_m_Pt', 10, 200),
			"Z Mass" : ('e_m_Mass', 10, 200),
			"L1 Pt" : ('ePt', 10, 200),
			"L1 Eta" : ('eEta', 10, 200),
			"L2 Pt" : ('mPt', 10, 200),
			"L2 Eta" : ('mEta', 10, 200),
			"PF Met" : ('PFMet', 10, 200),
			"Jet Multiplicity" : ('jetVeto30_DR05', 1, 10),
}		

varMapTT = {"Z Pt" : ('t1_t2_Pt', 10, 200),
			"Z Mass" : ('t1_t2_Mass', 10, 200),
			"L1 Pt" : ('t1Pt', 10, 200),
			"L1 Eta" : ('t1Eta', 10, 200),
			"L2 Pt" : ('t2Pt', 10, 200),
			"L2 Eta" : ('t2Eta', 10, 200),
			"PF Met" : ('PFMet', 10, 200),
			"Jet Multiplicity" : ('jetVeto30_DR05', 1, 10),
}		
samples = ['Tbar_tW', 'T_tW', 'WW', 'WJets', 'TT', 'TTJets', 'HtoTauTau', 'VBF_HtoTauTau', 'WZJets', 'QCD']
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
		stack = ROOT.THStack("All Backgrounds", "title Stack")
		print varMap[ var ][0]

		for sample in samples:
			print sample
			hist = ROOT.TH1F("%s_%s_%s" % (channel, sample, var), "%s %s %s" % (channel, sample, var), varBin, 0, varRange)

			tFile = ROOT.TFile('baseSelectionRoot/%s.root' % sample, 'READ')
			tree = tFile.Get('%s/Ntuple' % channel)
			for row in tree :
				hist.Fill( getattr( row, '%s' % varMap[ var ][0] ) )
			color = "ROOT.%s" % sampleColors[ sample ][0]
			hist.SetFillColor( eval( color ) )
			hist.SetLineColor( ROOT.kBlack )
			#hist.SaveAs('plots/%s/%s.root' % (channel, sample) )

			# Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data )
			if hist.Integral() != 0:
				hist.Scale( ( hist.Integral() / xSecs[ sample ]['nevents']  ) * 1000 * sampleColors[ sample ][1] / hist.Integral() )

			print hist.Integral()
			stack.Add( hist )
			tFile.Close()
		#stack.SaveAs('plots/%s/stack.root' % channel )
		signal = ROOT.TH1F("DYJets_%s_%s" % (channel, var), "%s DYJets %s" % (channel, var), varBin, 0, varRange)
		sigFile = ROOT.TFile('baseSelectionRoot/DYJets.root', 'READ')
		tree = sigFile.Get('%s/Ntuple' % channel)
		for row in tree :
			signal.Fill( getattr( row, '%s' % varMap[ var ][0] ) )
		signal.SetLineColor( ROOT.kGreen )
		signal.SetLineWidth( 2 )
		#signal.SaveAs('plots/%s/DYJets.root' % channel )
		sigFile.Close()
		
		#finalPlot = ROOT.TH1F("final_plot", "Z -> #tau#tau, %s, %s" % (channel, var), varBin, 0, varRange)
		c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 600, 600)
		pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
		pad1.Draw()
		pad1.cd()

		stack.Draw('hist')
		stack.GetXaxis().SetTitle("%s (GeV)" % var)
		stack.GetYaxis().SetTitle("Events / %i (GeV)" % ( varRange / varBin ) )
		stack.SetMinimum( 0.1 )

		signal.Draw('hist same')

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
