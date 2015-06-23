from util.buildTChain import makeTChain
import ROOT
import json
from collections import OrderedDict
import cutsBaseSelection as bc

ROOT.gROOT.SetBatch(True)

with open('meta/data.json') as sampFile :
	sampDict = json.load( sampFile )

prodMap = { 'em' : ('e', 'm'),
			 'tt' : ('t1', 't2')
}
				# Sample : Color
samples = OrderedDict()
samples['DYJets']	= ('kBlack', 'dyj')
samples['TT']		= ('kBlue-8', 'top')
samples['TTJets']	= ('kBlue-2', 'top')
#samples['QCD']		= ('kMagenta-10', 'qcd')
samples['Tbar_tW']	= ('kYellow-2', 'top')
samples['T_tW']		= ('kYellow+2', 'top')
samples['HtoTauTau']		= ('kRed+2', 'higgs')
samples['VBF_HtoTauTau']	= ('kRed-2', 'higgs')
samples['WJets']	= ('kAzure+2', 'ewk')
samples['WW']		= ('kAzure+10', 'ewk')
samples['WZJets']	= ('kAzure-4', 'ewk')


#varMapEM = {"Z Pt" : ('e_m_Pt', 10, 200, 0),
#			"Z Mass" : ('e_m_Mass', 8, 130, 50),
#			"Electron Pt" : ('ePt', 10, 200, 0),
#			"Electron Eta" : ('eEta', 12, 3., -3),
#			"Muon Pt" : ('mPt', 10, 200, 0),
#			"Muon Eta" : ('mEta', 12, 3., -3.),
#			"PF Met" : ('pfMetEt', 10, 200, 0),
#			"Jet Multiplicity" : ('jetVeto30_DR05', 10, 10, 0),
#}		

#varMapTT = {"Z Pt" : ('t1_t2_Pt', 10, 200, 0),
#			"Z Mass" : ('t1_t2_Mass', 8, 130, 50),
#			"#tau_{h1} Pt" : ('t1Pt', 10, 200, 0),
#			"#tau_{h1} Eta" : ('t1Eta', 30, 3., -3.),
#			"#tau_{h2} Pt" : ('t2Pt', 10, 200, 0),
#			"#tau_{h2} Eta" : ('t2Eta', 30, 3., -3),
#			"PF Met" : ('pfMetEt', 10, 200, 0),
#			"Jet Multiplicity" : ('jetVeto30_DR05', 10, 10, 0),
#}		

# Cut out QCD for the moment and merge like backgrounds
#samples = ['Tbar_tW', 'T_tW', 'WW', 'WJets', 'TT', 'TTJets', 'HtoTauTau', 'VBF_HtoTauTau', 'WZJets', 'DYJets']#, 'QCD']
#samples = ['TT', 'QCD', 'Tbar_tW', 'T_tW', 'HtoTauTau', 'VBF_HtoTauTau', 'WJets', 'WW', 'WZJets']

for channel in prodMap.keys() :
	print channel
	if channel == 'em': varMap = bc.getEMHistoDict()
	if channel == 'tt': varMap = bc.getTTHistoDict()
	for var in varMap :
		print var
#		varBin = varMap[ var ][1]
#		print varBin
#		varRange = varMap[ var ][2]
#		print varRange
#		varMin = varMap[ var ][3]
		stack = ROOT.THStack("All Backgrounds stack", "%s, %s" % (channel, var) )
		dyj = ROOT.THStack("All Backgrounds dyj", "dyj" )
		ewk = ROOT.THStack("All Backgrounds ewk", "ewk" )
		top = ROOT.THStack("All Backgrounds top", "top" )
		higgs = ROOT.THStack("All Backgrounds higgs", "higgs" )
		qcd = ROOT.THStack("All Backgrounds qcd", "qcd" )
#		print varMap[ var ][0]

		for sample in samples:
			print sample
#			hist = ROOT.TH1F("%s_%s_%s" % (channel, sample, var), "%s %s %s" % (channel, sample, var), varBin, varMin, varRange)

			tFile = ROOT.TFile('baseSelectionRootQuick/%s.root' % sample, 'READ')
			dic = tFile.Get("%s_BaseLine" % channel )
			hist = dic.Get( "%s" % varMap[ var ][0] )
			hist.SetDirectory( 0 )
#			tree = tFile.Get('%s/Ntuple' % channel)
#			for row in tree :
#				hist.Fill( getattr( row, '%s' % varMap[ var ][0] ) )
			color = "ROOT.%s" % samples[ sample ][0]
			if samples[ sample ][1] != 'higgs':
				hist.SetFillColor( eval( color ) )
				hist.SetLineColor( ROOT.kBlack )
				hist.SetLineWidth( 2 )
			#hist.SaveAs('plots/%s/%s.root' % (channel, sample) )

			# Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data )
			if hist.Integral() != 0:
				hist.Scale( ( hist.Integral() * 1000 * sampDict[ sample ]['Cross Section (pb)'] ) / ( hist.Integral() * sampDict[ sample ]['nevents'] ) )

			print hist.Integral()
			if samples[ sample ][1] == 'dyj' :
				hist.SetTitle('Z #rightarrow #tau#tau')
				dyj.Add( hist )
			#if samples[ sample ][1] == 'qcd' :
			#	qcd.Add( hist )
			if samples[ sample ][1] == 'top' :
				hist.SetTitle('Single & Double Top')
				top.Add( hist )
			if samples[ sample ][1] == 'ewk' :
				hist.SetTitle('Electroweak')
				ewk.Add( hist )
			if samples[ sample ][1] == 'higgs' :
				hist.SetTitle('SM Higgs(125)')
				higgs.Add( hist )
			tFile.Close()

		
		stack.Add( top.GetStack().Last() )
		stack.Add( ewk.GetStack().Last() )
		#stack.Add( qcd.GetStack().Last() )
		stack.Add( dyj.GetStack().Last() )
		#finalPlot = ROOT.TH1F("final_plot", "Z -> #tau#tau, %s, %s" % (channel, var), varBin, 0, varRange)
		c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 600, 600)
		pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
		pad1.Draw()
		pad1.cd()

		stack.Draw('hist')
		higgs.Draw('hist same')
		stack.GetXaxis().SetTitle("%s (GeV)" % var)
		if hist.GetBinWidth(1) < .05 :
			binWidth = round( hist.GetBinWidth(1), 2)
		elif hist.GetBinWidth(1) < .5 :
			binWidth = round( hist.GetBinWidth(1), 1)
		else:
			binWidth = round( hist.GetBinWidth(1), 0)
		
		stack.GetYaxis().SetTitle("Events / %s (GeV)" % ( str( binWidth ) ) )
		stack.SetMinimum( 0.1 )

		# Set axis and viewing area
		pad1.SetLogy()
		pad1.BuildLegend()

		pad1.Update()
		c1.SaveAs('plots/%s/%s.png' % (channel, var ) )
		c1.Close()

