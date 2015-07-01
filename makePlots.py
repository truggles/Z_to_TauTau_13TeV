from util.buildTChain import makeTChain
import ROOT
import json
from collections import OrderedDict
import cutsBaseSelection as bc
import pyplotter.plot_functions as pyplotter #import setTDRStyle, getCanvas
import pyplotter.tdrstyle as tdr

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

luminosity = 1000.0 # (pb)

with open('meta/data.json') as sampFile :
	sampDict = json.load( sampFile )

prodMap = { 'em' : ('e', 'm'),
			 'tt' : ('t1', 't2')
}
				# Sample : Color
samples = OrderedDict()
samples['DYJets']	= ('kBlack', 'dyj')
#samples['TT']		= ('kBlue-8', 'top')
samples['TTJets']	= ('kBlue-2', 'top')
samples['QCD']		= ('kMagenta-10', 'qcd')
samples['Tbar_tW']	= ('kYellow-2', 'top')
samples['T_tW']		= ('kYellow+2', 'top')
samples['HtoTauTau']		= ('kRed+2', 'higgs')
samples['VBF_HtoTauTau']	= ('kRed-2', 'higgs')
samples['WJets']	= ('kAzure+2', 'ewk')
samples['WW']		= ('kAzure+10', 'ewk')
samples['WZJets']	= ('kAzure-4', 'ewk')
samples['ZZ']	= ('kAzure-8', 'ewk')

higgsColors = {
	'ewk' : 'kRed+2',
	'top' : 'kBlue-8',
	'qcd' : 'kMagenta-10',
	'dyj' : 'kOrange-4',
}

plotDetails = {
	'eEta' : (-3, 3, 2, 'e Eta', ''),
	'ePt' : (0, 200, 2, 'e p_{T} [GeV]', ' GeV'),
	'eMtToPFMET' : (0, 200, 2, 'e m_{T} [GeV]', ' GeV'),
	'ePVDXY' : (-.1, .1, 2, "e PVDXY [cm]", " cm"),
	'ePVDZ' : (-.25, .25, 1, "e PVDZ [cm]", " cm"),
	'eRelPFIsoDB' : (0, 0.2, 1, 'e RelPFIsoDB', ''),
	'mEta' : (-3, 3, 1, 'm Eta', ''),
	'mNormTrkChi2' : (0, 4, 1, 'm NormTrkChi2', ''),
	'mPt' : (0, 200, 1, 'm p_{T} [GeV]', ' GeV'),
	'mMtToPFMET' : (0, 200, 2, 'm m_{T} [GeV]', ' GeV'),
	'mPVDXY' : (-.1, .1, 2, "m PVDXY [cm]", " cm"),
	'mPVDZ' : (-.25, .25, 1, "m PVDZ [cm]", " cm"),
	'mRelPFIsoDBDefault' : (0, 0.2, 1, 'm RelPFIsoDB', ''),
	'Z_Mass' : (0, 300, 2, 'Z Mass [GeV]', ' GeV'),
	'Z_Pt' : (0, 200, 2, 'Z p_{T} [GeV]', ' GeV'),
	'Z_SS' : (-1, 1, 1, 'Z Same Sign', ''),
	't1ByCombinedIsolationDeltaBetaCorrRaw3Hits' : (0, 2, 1, '#tau_{1}CombIsoDBCorrRaw3Hits', ''),
	't1Eta' : ( -3, 3, 4, '#tau_{1} Eta', ''),
	't1Pt' : (0, 200, 2, '#tau_{1} p_{T} [GeV]', ' GeV'),
	't1MtToPFMET' : (0, 200, 2, '#tau_{1} m_{T} [GeV]', ' GeV'),
	't2ByCombinedIsolationDeltaBetaCorrRaw3Hits' : (0, 2, 1, '#tau_{2}CombIsoDBCorrRaw3Hits', ''),
	't2Eta' : ( -3, 3, 4, '#tau_{2} Eta', ''),
	't2Pt' : (0, 200, 2, '#tau_{2} p_{T} [GeV]', ' GeV'),
	't2MtToPFMET' : (0, 200, 2, '#tau_{2} m_{T} [GeV]', ' GeV'),
	'pfMetEt' : (0, 400, 2, 'pfMet [GeV]', ' GeV'),
	'LT' : (0, 400, 2, 'Total LT [GeV]', ' GeV'),
	'Mt' : (0, 400, 2, 'Total m_{T} [GeV]', ' GeV'),
	'bjetCISVVeto20Medium' : (0, 5, 12, 'bJetCISVVeto20Medium', ''),
	'jetVeto30' : (0, 10, 10, 'jetVeto30', ''),
}	

for channel in prodMap.keys() :
	print channel
	if channel == 'em': varMap = bc.getEMHistoDict()
	if channel == 'tt': varMap = bc.getTTHistoDict()
	genVar = bc.getGeneralHistoDict()
	newVarMap = {}
	for var, name in varMap.iteritems() :
		newVarMap[ var ] = name[0]
	for var, name in genVar.iteritems() :
		newVarMap[ var ] = name[0]
	print newVarMap


	for var, name in newVarMap.iteritems() :
		print "Var: %s		Name: %s" % (var, name)
		stack = ROOT.THStack("All Backgrounds stack", "%s, %s" % (channel, var) )
		dyj = ROOT.THStack("All Backgrounds dyj", "dyj" )
		ewk = ROOT.THStack("All Backgrounds ewk", "ewk" )
		top = ROOT.THStack("All Backgrounds top", "top" )
		higgs = ROOT.THStack("All Backgrounds higgs", "higgs" )
		qcd = ROOT.THStack("All Backgrounds qcd", "qcd" )

		for sample in samples:
			print sample

			# Temporary QCD method of using a relaxed cut to get stats and having tighter for yield
			#qcdYield = 0
			if sample == 'QCD' :
				# Shape
				tFile = ROOT.TFile('baseSelectionRoot/%s.root' % sample, 'READ')
				dic = tFile.Get("%s_qcd_pre" % channel )
				hist = dic.Get( "%s" % var )
				hist.SetDirectory( 0 )
				print "QCD int loose: %f" % hist.Integral()
				# Yield
				tFileY = ROOT.TFile('baseSelectionRootQuick/%s.root' % sample, 'READ')
				dicY = tFileY.Get("%s" % channel )
				treeY = dicY.Get("Ntuple")
				qcdYield = 0
				evtS = set()
				for row in treeY :
					evtT = (row.run, row.lumi, row.evt)
					if evtT not in evtS :
						qcdYield += 1
						evtS.add( evtT )
				#histY = dicY.Get( "%s" % var )
				#qcdYield = histY.Integral()				
				#qcdYield = len( treeY )
				print "QCD int tight: %f" % qcdYield
			# All other samples
			else :
				tFile = ROOT.TFile('baseSelectionRootQuick/%s.root' % sample, 'READ')
				dic = tFile.Get("%s_BaseLine" % channel )
				hist = dic.Get( "%s" % var )
				hist.SetDirectory( 0 )


			hist.Rebin( plotDetails[ var ][2] )
			if samples[ sample ][1] != 'higgs':
				color = "ROOT.%s" % higgsColors[ samples[ sample ][1] ]
				hist.SetFillColor( eval( color ) )
				hist.SetLineColor( ROOT.kBlack )
				hist.SetLineWidth( 2 )
			else : 
				hist.SetLineColor( ROOT.kBlue )
				hist.SetLineWidth( 4 )
				hist.SetLineStyle( 7 )
			#hist.SaveAs('plots/%s/%s.root' % (channel, sample) )

			# Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ), QCD gets special scaling from bkg estimation
			scaler = luminosity * sampDict[ sample ]['Cross Section (pb)'] / ( sampDict[ sample ]['nEventsEM'] )
			if sample == 'QCD' :
				#print "QCD pre: %f" % scaler
				scaler = scaler * ( qcdYield / hist.Integral() )
				#print "QCD post: %f" % scaler
			if hist.Integral() != 0:
				hist.Scale( scaler )

			#print hist.Integral()
			if samples[ sample ][1] == 'dyj' :
				hist.SetTitle('Z #rightarrow #tau#tau')
				dyj.Add( hist )
			if samples[ sample ][1] == 'qcd' :
				hist.SetTitle('QCD')
				qcd.Add( hist )
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
		stack.Add( dyj.GetStack().Last() )
		print "Qcd Yield %f" % qcd.GetStack().Last().Integral()
		stack.Add( qcd.GetStack().Last() )
		c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 600, 600)
		pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
		pad1.Draw()
		pad1.cd()
		stack.Draw('hist')
		higgs.GetStack().Last().Draw('hist same')

		# X Axis!
		stack.GetXaxis().SetTitle("%s" % plotDetails[ var ][ 3 ])
		
		# Set Y axis titles appropriately
		if hist.GetBinWidth(1) < .05 :
			binWidth = round( hist.GetBinWidth(1), 2)
		elif hist.GetBinWidth(1) < .5 :
			binWidth = round( hist.GetBinWidth(1), 1)
		else:
			binWidth = round( hist.GetBinWidth(1), 0)
		if plotDetails[ var ][ 4 ] == '' :
			stack.GetYaxis().SetTitle("Events")
		else :
			stack.GetYaxis().SetTitle("Events / %i%s" % ( binWidth, plotDetails[ var ][ 4 ] ) )

		# Set axis and viewing area
		pad1.SetLogy()
		higgsMax = higgs.GetMaximum()
		stack.SetMinimum( higgsMax * 0.1 )
		#pad1.BuildLegend()

		''' Build the legend explicitly so we can specify marker styles '''
		legend = ROOT.TLegend(0.60, 0.65, 0.95, 0.93)
		legend.SetMargin(0.3)
		legend.SetBorderSize(0)
		legend.AddEntry( higgs.GetStack().Last(), "SM Higgs (125)", 'l')
		for j in range(0, stack.GetStack().GetLast() + 1) :
		    last = stack.GetStack().GetLast()
		    legend.AddEntry( stack.GetStack()[ last - j ], stack.GetStack()[last - j ].GetTitle(), 'f')
		legend.Draw()

		pad1.Update()
		stack.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )
		c1.SaveAs('plots/%s/%s.png' % (channel, var ) )
		c1.Close()

