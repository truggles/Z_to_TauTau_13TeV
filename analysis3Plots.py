from util.buildTChain import makeTChain
import ROOT
import json
from collections import OrderedDict
import cutsBaseSelection as bc
import pyplotter.plot_functions as pyplotter #import setTDRStyle, getCanvas
import pyplotter.tdrstyle as tdr
import argparse
from util.ratioPlot import ratioPlot 

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='25ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--ratio', action='store', default=False, dest='ratio', help="Include ratio plots? Defaul = False")
p.add_argument('--numTT', action='store', default=9, dest='numTT', help="How many TT files are there?")
p.add_argument('--log', action='store', default=False, dest='log', help="Plot Log Y?")
options = p.parse_args()
pre_ = options.sampleName
ratio = options.ratio
numTT = options.numTT

print "Running over %s samples" % pre_

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

luminosity = 16.1 # (pb) 25ns
qcdTTScaleFactor = 1.00 # from running "python makeBaseSelections.py --invert=True" and checking ration of SS / OS
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
#samples['TT_0']		= ('kBlue-8', 'top')
#samples['TT_1']		= ('kBlue-8', 'top')
#samples['TT_2']		= ('kBlue-8', 'top')
#samples['TT_3']		= ('kBlue-8', 'top')
#samples['TT_4']		= ('kBlue-8', 'top')
#samples['TT_5']		= ('kBlue-8', 'top')
#samples['TT_6']		= ('kBlue-8', 'top')
#samples['TT_7']		= ('kBlue-8', 'top')
#samples['TT_8']		= ('kBlue-8', 'top')
#samples['TT_9']		= ('kBlue-8', 'top')
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
samples['WJets']	= ('kAzure+2', 'ewk')
samples['WW']		= ('kAzure+10', 'ewk')
samples['WW2l2n']		= ('kAzure+8', 'ewk')
samples['WW4q']		= ('kAzure+6', 'ewk')
samples['WW1l1n2q']		= ('kAzure+4', 'ewk')
samples['WZJets']	= ('kAzure-4', 'ewk')
samples['WZ1l1n2q']	= ('kAzure-6', 'ewk')
samples['ZZ']	= ('kAzure-8', 'ewk')
samples['ZZ4l']	= ('kAzure-12', 'ewk')
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
    'eMtToMET' : (0, 200, 2, 'e m_{T} [GeV]', ' GeV'),
    'ePVDXY' : (-.1, .1, 2, "e PVDXY [cm]", " cm"),
    'ePVDZ' : (-.25, .25, 1, "e PVDZ [cm]", " cm"),
    'eRelPFIsoDB' : (0, 0.2, 1, 'e RelPFIsoDB', ''),
    'eRelIsoDB03' : (0, 0.2, 1, 'e RelIsoDB03', ''),
    'eJetPt' : (0, 200, 2, 'e Overlapping Jet Pt', ' GeV'),
    'mEta' : (-3, 3, 2, 'm Eta', ''),
    'mNormTrkChi2' : (0, 4, 1, 'm NormTrkChi2', ''),
    'mPt' : (0, 200, 1, 'm p_{T} [GeV]', ' GeV'),
    'mMtToMET' : (0, 200, 2, 'm m_{T} [GeV]', ' GeV'),
    'mPVDXY' : (-.1, .1, 2, "m PVDXY [cm]", " cm"),
    'mPVDZ' : (-.25, .25, 1, "m PVDZ [cm]", " cm"),
    'mRelPFIsoDBDefault' : (0, 0.3, 1, 'm RelPFIsoDB', ''),
    'mRelIsoDB03' : (0, 0.3, 1, 'm RelIsoDB03', ''),
    'mJetPt' : (0, 200, 2, 'm Overlapping Jet Pt', ' GeV'),
    'Z_Mass' : (0, 300, 4, 'Z Mass [GeV]', ' GeV'),
    'Z_Pt' : (0, 200, 2, 'Z p_{T} [GeV]', ' GeV'),
    'Z_SS' : (-1, 1, 1, 'Z Same Sign', ''),
    't1ByCombinedIsolationDeltaBetaCorrRaw3Hits' : (0, 5, 1, '#tau_{1}CombIsoDBCorrRaw3Hits', ''),
    't1Eta' : ( -3, 3, 4, '#tau_{1} Eta', ''),
    't1Pt' : (0, 200, 2, '#tau_{1} p_{T} [GeV]', ' GeV'),
    't1MtToPFMET' : (0, 200, 2, '#tau_{1} m_{T} [GeV]', ' GeV'),
    't2ByCombinedIsolationDeltaBetaCorrRaw3Hits' : (0, 5, 1, '#tau_{2}CombIsoDBCorrRaw3Hits', ''),
    't2Eta' : ( -3, 3, 4, '#tau_{2} Eta', ''),
    't2Pt' : (0, 200, 2, '#tau_{2} p_{T} [GeV]', ' GeV'),
    't2MtToPFMET' : (0, 200, 2, '#tau_{2} m_{T} [GeV]', ' GeV'),
    'pfMetEt' : (0, 400, 2, 'pfMet [GeV]', ' GeV'),
    'pfMetPhi' : (-5, 5, 2, 'pfMetPhi', ''),
    'mvaMetEt' : (0, 400, 2, 'mvaMetEt [GeV]', ' GeV'),
    'mvaMetPhi' : (-5, 5, 2, 'mvaMetPhi', ''),
    'LT' : (0, 600, 6, 'Total LT [GeV]', ' GeV'),
    'Mt' : (0, 600, 6, 'Total m_{T} [GeV]', ' GeV'),
    'nbtag' : (0, 5, 10, 'nBTag', ''),
    'njetspt20' : (0, 10, 10, 'nJetPt20', ''),
    'jet1Pt' : (0, 200, 2, 'Leading Jet Pt', ' GeV'),
    'jet1Eta' : (-5, 5, 2, 'Leading Jet Eta', ''),
    'jet2Pt' : (0, 200, 2, 'Second Jet Pt', ' GeV'),
    'jet2Eta' : (-5, 5, 2, 'Second Jet Eta', ''),
    'eVetoZTT10' : (0, 2, 1, 'Extra Electron Veto', ''),
    'mVetoZTT10' : (0, 2, 1, 'Extra Muon Veto', ''),
    'GenWeight' : (-30000, 30000, 1, 'Gen Weight', ''),
    'nvtx' : (0, 50, 1, 'Number of Vertices', ''),
    't1DecayMode' : (0, 15, 1, 't1 Decay Mode', ''),
    't2DecayMode' : (0, 15, 1, 't2 Decay Mode', ''),
    't1Mass' : (0, 3, 2, 't1 Mass', ' GeV'),
    't2Mass' : (0, 3, 2, 't2 Mass', ' GeV'),
    't1JetPt' : (0, 400, 2, 't1 Overlapping Jet Pt', ' GeV'),
    't2JetPt' : (0, 400, 2, 't2 Overlapping Jet Pt', ' GeV'),
    't1ChargedIsoPtSum' : (0, 10, 4, 't1 ChargedIsoPtSum', ' GeV'),
    't1NeutralIsoPtSum' : (0, 10, 4, 't1 NeutralIsoPtSum', ' GeV'),
    't1PuCorrPtSum' : (0, 40, 2, 't1 PuCorrPtSum', ' GeV'),
    't2ChargedIsoPtSum' : (0, 10, 4, 't2 ChargedIsoPtSum', ' GeV'),
    't2NeutralIsoPtSum' : (0, 10, 4, 't2 NeutralIsoPtSum', ' GeV'),
    't2PuCorrPtSum' : (0, 40, 2, 't2 PuCorrPtSum', ' GeV'),
}	


for channel in prodMap.keys() :
    # Make an index file for web viewing
    htmlFile = open('%sPlots/%s/index.html' % (pre_, channel), 'w')
    htmlFile.write( '<html><head><STYLE type="text/css">img { border:0px; }</STYLE>\n' )
    htmlFile.write( '<title>Channel %s/</title></head>\n' % channel )
    htmlFile.write( '<body>\n' )


    print channel
    if channel == 'em': varMap = bc.getEMHistoDict()
    if channel == 'tt': varMap = bc.getTTHistoDict()
    genVar = bc.getGeneralHistoDict()
    newVarMap = {}
    for var, name in varMap.iteritems() :
    	newVarMap[ var ] = name[0]
    for var, name in genVar.iteritems() :
    	newVarMap[ var ] = name[0]
    #print newVarMap
    
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
             
            # allow looping over TT sample
#       count = 0
#       done = False
#       while not done :
#           if sample == 'TT' :
#               tFile = ROOT.TFile('%s1BaseCut/%s_%i.root' % (pre_, sample, count), 'READ')
#               print sample,' ',count
#               count += 1
#           else :
#               print sample
#               tFile = ROOT.TFile('%s1BaseCut/%s.root' % (pre_, sample), 'READ')
            if sample == 'TT' : continue
            tFile = ROOT.TFile('%s1BaseCut/%s.root' % (pre_, sample), 'READ')
            # Make sure we can still read TT variables
            if 'TT' in sample : sample = 'TT'
 
            if channel == 'tt' and sample == 'data_em' : continue
            if channel == 'em' and sample == 'data_tt' : continue
            
            dic = tFile.Get("%s_Histos" % channel )
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

#           if 'data' in sample : done = True
#           if sample not in 'TT' :
#               done = True
#           elif sample == 'TT' and count > numTT :
#               done = True
    

        ## Scale QCD shape to Data Driven Yield            
        #qcdInt = qcd.GetStack().Last().Integral()
        #print "qcdInt: %f" % qcdInt
        #if channel == 'tt' : qcdScaleFactor = qcdTTScaleFactor
        #if channel == 'em' : qcdScaleFactor = qcdEMScaleFactor
        #qcd.GetStack().Last().Scale( qcdScaleFactor * qcdYield / qcdInt )
        #qcdInt = qcd.GetStack().Last().Integral()
        #print "New qcdInt: %f" % qcdInt

        #stack.Add( qcd.GetStack().Last() )
        stack.Add( top.GetStack().Last() )
        stack.Add( ewk.GetStack().Last() )
        stack.Add( dyj.GetStack().Last() )

        # Maybe make ratio hist
        c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 600, 600)

        if ratio == False :
            pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
            pad1.Draw()
            pad1.cd()
        if ratio == True :
            pads = ratioPlot( c1 )
            pad1 = pads[0]
            ratioPad = pads[1]
            pad1.cd()
            #varMin_ = dyj.GetStack().Last()
            #ratioHist = ROOT.TH1('ratio plot' + var, 'ratio', 

        stack.Draw('hist')
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
        #higgsMin = higgs.GetMaximum()
        #print "higgs max: %f" % higgsMin
        #stackMin = stack.GetStack().First().GetMaximum()
        #print "stack max: %f" % stackMin
        #stack.SetMinimum( min( higgsMin, stackMin) * 0.3 )
        stackMax = stack.GetStack().Last().GetMaximum()
        dataMax = data.GetStack().Last().GetMaximum()
        stack.SetMaximum( max(dataMax, stackMax) * 1.5 )
        #stack.SetMaximum( stackMax * 1.5 )
        if options.log :
            pad1.SetLogy()
            stack.SetMaximum( max(dataMax, stackMax) * 10 )
            stack.SetMinimum( min(dataMax, stackMax) * .05 )
        
        ''' Build the legend explicitly so we can specify marker styles '''
        legend = ROOT.TLegend(0.60, 0.65, 0.95, 0.93)
        legend.SetMargin(0.3)
        legend.SetBorderSize(0)
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
        c1.SaveAs('%sPlotsList/%s/%s.png' % (pre_, channel, var ) )
        c1.Close()

        htmlFile.write( '<img src="%s.png">\n' % var )
        htmlFile.write( '<br>\n' )
    htmlFile.write( '</body></html>' )
    htmlFile.close()
