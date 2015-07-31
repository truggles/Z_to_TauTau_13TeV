from util.buildTChain import makeTChain
import ROOT
import json
from collections import OrderedDict
import cutsBaseSelection as bc
import pyplotter.plot_functions as pyplotter #import setTDRStyle, getCanvas
import pyplotter.tdrstyle as tdr
import argparse

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='50ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--includeHiggs', action='store', default=False, dest='includeHiggs', help="Include 25ns Higgs samples?")
results = p.parse_args()
pre_ = results.sampleName
includeHiggs = results.includeHiggs

print "Running over %s samples" % pre_

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

luminosity = 40.0 # (pb)
qcdTTScaleFactor = 1.09 # from running "python makeBaseSelections.py --invert=True" and checking ration of SS / OS
#qcdEMScaleFactor = 3.50
qcdEMScaleFactor = 1.0
qcdYieldTT = 0
qcdYieldEM = 0

with open('meta/NtupleInputs_%s/samples.json' % pre_) as sampFile :
	sampDict = json.load( sampFile )

prodMap = { 'em' : ('e', 'm'),
			 'tt' : ('t1', 't2')
}
				# Sample : Color
samples = OrderedDict()
samples['DYJets']	= ('kOrange-4', 'dyj')
#samples['TT']		= ('kBlue-8', 'top')
samples['TTJets']	= ('kBlue-2', 'top')
samples['QCD15-20']		= ('kMagenta-10', 'qcd')
samples['QCD20-30']		= ('kMagenta-10', 'qcd')
samples['QCD30-50']		= ('kMagenta-10', 'qcd')
samples['QCD50-80']		= ('kMagenta-10', 'qcd')
samples['QCD80-120']		= ('kMagenta-10', 'qcd')
samples['QCD120-170']		= ('kMagenta-10', 'qcd')
samples['QCD170-300']		= ('kMagenta-10', 'qcd')
samples['QCD300-Inf']		= ('kMagenta-10', 'qcd')
samples['Tbar_tW']	= ('kYellow-2', 'top')
samples['T_tW']		= ('kYellow+2', 'top')
samples['HtoTauTau']		= ('kRed+2', 'higgs')
samples['VBF_HtoTauTau']	= ('kRed-2', 'higgs')
samples['WJets']	= ('kAzure+2', 'ewk')
samples['WW']		= ('kAzure+10', 'ewk')
samples['WZJets']	= ('kAzure-4', 'ewk')
samples['ZZ']	= ('kAzure-8', 'ewk')
samples['data_tt']  = ('kBlack', 'data')
samples['data_em']  = ('kBlack', 'data')

sampColors = {
	'ewk' : 'kRed+2',
	'top' : 'kBlue-8',
	'qcd' : 'kMagenta-10',
	'dyj' : 'kOrange-4',
    'data' : 'kBlack',
}

plotDetails = {
	'eEta' : (-3, 3, 2, 'e Eta', ''),
	'ePt' : (0, 200, 2, 'e p_{T} [GeV]', ' GeV'),
	'eMtToPFMET' : (0, 200, 2, 'e m_{T} [GeV]', ' GeV'),
	'ePVDXY' : (-.1, .1, 2, "e PVDXY [cm]", " cm"),
	'ePVDZ' : (-.25, .25, 1, "e PVDZ [cm]", " cm"),
	'eRelPFIsoDB' : (0, 0.2, 1, 'e RelPFIsoDB', ''),
	'mEta' : (-3, 3, 2, 'm Eta', ''),
	'mNormTrkChi2' : (0, 4, 1, 'm NormTrkChi2', ''),
	'mPt' : (0, 200, 1, 'm p_{T} [GeV]', ' GeV'),
	'mMtToPFMET' : (0, 200, 2, 'm m_{T} [GeV]', ' GeV'),
	'mPVDXY' : (-.1, .1, 2, "m PVDXY [cm]", " cm"),
	'mPVDZ' : (-.25, .25, 1, "m PVDZ [cm]", " cm"),
	'mRelPFIsoDBDefault' : (0, 0.2, 1, 'm RelPFIsoDB', ''),
	'Z_Mass' : (0, 300, 4, 'Z Mass [GeV]', ' GeV'),
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
	'LT' : (0, 400, 4, 'Total LT [GeV]', ' GeV'),
	'Mt' : (0, 400, 4, 'Total m_{T} [GeV]', ' GeV'),
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
        data = ROOT.THStack("All Backgrounds data", "data" )
        
        for sample in samples:
            if not includeHiggs and 'HtoTauTau' in sample : continue
            if channel == 'tt' and sample == 'data_em' : continue
            if channel == 'em' and sample == 'data_tt' : continue
            print sample
            
            # Temporary QCD method of using a relaxed cut to get stats and having tighter for yield
            #qcdYield = 0
            if 'QCD' in sample :
            	# Shape
            	tFile = ROOT.TFile('%sQCD/%s.root' % (pre_, sample), 'READ')
            	dic = tFile.Get("%s_qcd_pre" % channel )
            	hist = dic.Get( "%s" % var )
            	hist.SetDirectory( 0 )
            	print "QCD int loose: %f" % hist.Integral()
            	# Yield
            	#tFileY1 = ROOT.TFile('50nsQCD/data_tt.root', 'READ')
            	#dicY1 = tFileY1.Get("%s_SS_DATA" % channel )
            	#qcdYield1 = dicY1.Get( "%s" % var ).Integral()
            	#tFileY2 = ROOT.TFile('50nsQCD/data_em.root', 'READ')
            	#dicY2 = tFileY2.Get("%s_SS_DATA" % channel )
            	#qcdYield2 = dicY2.Get( "%s" % var ).Integral()
                #qcdYield = qcdYield1 + qcdYield2

                ### REALLY BAD HARDCODE
                if channel == 'tt' : qcdYield = 50 # These numbers calculated by looking at data SS yield via "python makeBaseSelections.py --qcd=True"
                if channel == 'em' : qcdYield = 62 # only data from Tau files contributes to 'tt' and opposite for 'em'
            	#evtS = set()
            	#for row in treeY1 :
            	#	evtT = (row.run, row.lumi, row.evt)
            	#	if evtT not in evtS :
            	#		qcdYield += 1
            	#		evtS.add( evtT )
            	#print "Data SS: tt=%f em=%f" % (qcdYieldTT, qcdYieldEM)
                print "Data SS: %f" % qcdYield
            # All other samples
            elif 'HtoTauTau' in sample :
            	tFile = ROOT.TFile('25nsBaseRootsQuick/%s.root' % sample, 'READ')
            	dic = tFile.Get("%s_BaseLine" % channel )
            	hist = dic.Get( "%s" % var )
            	hist.SetDirectory( 0 )
            else :
            	tFile = ROOT.TFile('%sBaseRootsQuick/%s.root' % (pre_, sample), 'READ')
            	dic = tFile.Get("%s_PostSync" % channel )
            	hist = dic.Get( "%s" % var )
            	hist.SetDirectory( 0 )
            
            
            hist.Rebin( plotDetails[ var ][2] )
            if 'data' not in sample and samples[ sample ][1] != 'higgs' :
            	color = "ROOT.%s" % sampColors[ samples[ sample ][1] ]
            	hist.SetFillColor( eval( color ) )
            	hist.SetLineColor( ROOT.kBlack )
            	hist.SetLineWidth( 2 )
            elif samples[ sample ][1] == 'higgs' : 
            	hist.SetLineColor( ROOT.kBlue )
            	hist.SetLineWidth( 4 )
            	hist.SetLineStyle( 7 )
            else :
                hist.SetLineColor( ROOT.kBlack )
            	hist.SetLineWidth( 2 )
                hist.SetMarkerStyle( 21 )
            #hist.SaveAs('plots/%s/%s.root' % (channel, sample) )
            
            # Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ), QCD gets special scaling from bkg estimation
            if sample == 'HtoTauTau' :
                scaler = luminosity * 43.9 / 456682
            elif sample == 'VBF_HtoTauTau' :
                scaler = luminosity * 3.7 / 464755
            else :
                scaler = luminosity * sampDict[ sample ]['Cross Section (pb)'] / ( sampDict[ sample ]['nEventsEM'] )
            if sample == 'QCD' :
            	#print "QCD pre: %f" % scaler
            	#scaler = scaler * ( qcdYield / hist.Integral() )
            	scaler = 1
            	#print "QCD post: %f" % scaler
            if 'data' not in sample and hist.Integral() != 0:
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
            if samples[ sample ][1] == 'data' :
            	hist.SetTitle('Data')
            	data.Add( hist )
            tFile.Close()

        # Scale QCD shape to Data Driven Yield            
        qcdInt = qcd.GetStack().Last().Integral()
        print "qcdInt: %f" % qcdInt
        if channel == 'tt' : qcdScaleFactor = qcdTTScaleFactor
        if channel == 'em' : qcdScaleFactor = qcdEMScaleFactor
        qcd.GetStack().Last().Scale( qcdScaleFactor * qcdYield / qcdInt )
        qcdInt = qcd.GetStack().Last().Integral()
        print "New qcdInt: %f" % qcdInt

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
        if includeHiggs : higgs.GetStack().Last().Draw('hist same')
        data.GetStack().Last().Draw('esamex0')
        
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

        stack.SetTitle( "CMS Preliminary        %f pb^{-1} ( 13 TeV )" % luminosity )
        
        # Set axis and viewing area
        #pad1.SetLogy()
        #higgsMin = higgs.GetMaximum()
        #print "higgs max: %f" % higgsMin
        #stackMin = stack.GetStack().First().GetMaximum()
        #print "stack max: %f" % stackMin
        #stack.SetMinimum( min( higgsMin, stackMin) * 0.3 )
        stackMax = stack.GetStack().Last().GetMaximum()
        dataMax = data.GetStack().Last().GetMaximum()
        if dataMax > stackMax :
            stack.SetMaximum( dataMax * 1.5 )
        else :
            stack.SetMaximum( stackMax * 1.5 )
        
        ''' Build the legend explicitly so we can specify marker styles '''
        legend = ROOT.TLegend(0.60, 0.65, 0.95, 0.93)
        legend.SetMargin(0.3)
        legend.SetBorderSize(0)
        if includeHiggs : legend.AddEntry( higgs.GetStack().Last(), "SM Higgs (125)", 'l')
        legend.AddEntry( data.GetStack().Last(), "Data", 'lep')
        for j in range(0, stack.GetStack().GetLast() + 1) :
            last = stack.GetStack().GetLast()
            legend.AddEntry( stack.GetStack()[ last - j ], stack.GetStack()[last - j ].GetTitle(), 'f')
        legend.Draw()

        # Set CMS Styles Stuff
        logo = ROOT.TText(.2, .88,"CMS Preliminary")
        logo.SetTextSize(0.03)
        logo.DrawTextNDC(.2, .89,"CMS Preliminary")

        chan = ROOT.TText(.2, .80,"x")
        chan.SetTextSize(0.05)
        chan.DrawTextNDC(.2, .84,"Channel: %s" % channel.upper() )

        lumi = ROOT.TText(.7,1.05,"%i pb^{-1} (13 TeV)" % luminosity)
        lumi.SetTextSize(0.03)
        lumi.DrawTextNDC(.7,.96,"%i / pb (13 TeV)" % luminosity)
        
        pad1.Update()
        stack.GetXaxis().SetRangeUser( plotDetails[ var ][0], plotDetails[ var ][1] )
        c1.SaveAs('%sPlots/%s/%s.png' % (pre_, channel, var ) )
        c1.Close()
        
