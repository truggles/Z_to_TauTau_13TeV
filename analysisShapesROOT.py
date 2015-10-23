from util.buildTChain import makeTChain
import ROOT
import json
from collections import OrderedDict
import pyplotter.plot_functions as pyplotter #import setTDRStyle, getCanvas
import pyplotter.tdrstyle as tdr
import argparse
import analysisPlots
from util.splitCanvas import fixFontSize
import os
import array

p = argparse.ArgumentParser(description="A script to set up json files with necessary metadata.")
p.add_argument('--samples', action='store', default='25ns', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--folder', action='store', default='2SingleIOAD', dest='folderDetails', help="What's our post-prefix folder name?")
p.add_argument('--qcdShape', action='store', default='Sync', dest='qcdShape', help="Which QCD shape to use? Sync or Loose triggers")
p.add_argument('--blind', action='store', default=True, dest='blind', help="blind data above 150 GeV?")
options = p.parse_args()
grouping = options.sampleName
folderDetails = options.folderDetails

print "Running over %s samples" % grouping

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

luminosity = 1280.23 # (pb) 25ns - Oct 21 certification
qcdTTScaleFactor = 1.00 # from running "python makeBaseSelections.py --invert=True" and checking ration of SS / OS
qcdEMScaleFactor = 1.06
bkgsTTScaleFactor = (1.11 + 0.99) / 2 # see pZeta_TT_Control.xlsx 
qcdYieldTT = 7350. * qcdTTScaleFactor  # From data - MC in OS region, see plots: 
                    # http://truggles.web.cern.ch/truggles/QCD_Yield_Oct13/25nsPlots/ - for 592pb-1
#qcdYieldEM = 899.4 * qcdEMScaleFactor   # Sync trigs all, L=1280.23, Oct21
#qcdYieldEM = 749.4 * qcdEMScaleFactor   # Sync trigs e23m8, L=1280.23, Oct21
#qcdYieldEM = 305.9 * qcdEMScaleFactor   # Sync trigs e12m23, L=1280.23, Oct21
''' Yikes, scale factor of "2" between SS/OS would make this all aligh PERFECTLY '''
qcdYieldEM = 2057.7 * qcdEMScaleFactor * .67 *2   # Loose trigs all, L=1280.23, Oct21
#qcdYieldEM = 1717.0 * qcdEMScaleFactor   # Loose trigs e17m8, L=1280.23, Oct21
#qcdYieldEM = 812.6 * qcdEMScaleFactor   # Loose trigs e12m17, L=1280.23, Oct21

with open('meta/NtupleInputs_%s/samples.json' % grouping) as sampFile :
    sampDict = json.load( sampFile )

                # Sample : Color
samples = OrderedDict()
samples['DYJets']   = ('kOrange-4', '_ZTT_')
#samples['DYJetsLow']   = ('kOrange-4', '_ZTT_')
#samples['TT']       = ('kBlue-8', '_TT_')
samples['TTJets']       = ('kBlue-8', '_TT_')
#samples['TTPow']       = ('kBlue-8', '_TT_')
samples['QCD']        = ('kMagenta-10', '_QCD_')
samples['Tbar-tW']  = ('kYellow-2', '_VV_')
samples['T-tW']     = ('kYellow+2', '_VV_')
samples['WJets']    = ('kAzure+2', '_W_')
samples['WW']       = ('kAzure+10', '_VV_')
#samples['WW2l2n']       = ('kAzure+8', '_VV_')
#samples['WW4q']     = ('kAzure+6', '_VV_')
#samples['WW1l1n2q']     = ('kAzure+4', '_VV_')
samples['WZJets']   = ('kAzure-4', '_VV_')
#samples['WZ1l1n2q'] = ('kAzure-6', '_VV_')
#samples['WZ3l1nu'] = ('kAzure-6', '_VV_')
samples['ZZ']   = ('kAzure-8', '_VV_')
#samples['ZZ4l'] = ('kAzure-12', '_VV_')
samples['data_tt']  = ('kBlack', '_data_obs_')
samples['data_em']  = ('kBlack', '_data_obs_')
samples['VBFHtoTauTau'] = ('kGreen', '_ggH125_')
samples['ggHtoTauTau'] = ('kGreen', '_vbfH125_')

channels = { 'em' : 'EMu',
             'tt' : 'TauTau',}

for channel in channels.keys() :

    if channel == 'tt' : continue

    # Make an index file for web viewing
    if not os.path.exists( '%sShapes' % grouping ) :
        os.makedirs( '%sShapes' % grouping )

    print channel

    newVarMap = analysisPlots.getHistoDict( channel )
    plotDetails = analysisPlots.getPlotDetails( channel )

    for var, info in newVarMap.iteritems() :
        if not var == 'm_vis' : continue
        shapeFile = ROOT.TFile('%sShapes/ztt_%s.inputs-sm-13TeV.root' % (grouping, channel), 'RECREATE')
        shapeDir = shapeFile.mkdir( channels[ channel ] + '_inclusive' )

        # Defined out here for large scope
        name = info[0]
        print "Var: %s      Name: %s" % (var, name)
        _ZTT_ = ROOT.THStack("All Backgrounds _ZTT_", "_ZTT_" )
        _VV_ = ROOT.THStack("All Backgrounds _VV_", "_VV_" )
        _TT_ = ROOT.THStack("All Backgrounds _TT_", "_TT_" )
        _ggH125_ = ROOT.THStack("All Backgrounds _ggH125_", "_ggH125_" )
        _vbfH125_ = ROOT.THStack("All Backgrounds _vbfH125_", "_vbfH125_" )
        _QCD_ = ROOT.THStack("All Backgrounds _QCD_", "_QCD_" )
        _W_ = ROOT.THStack("All Backgrounds _W_", "_W_" )
        _data_obs_ = ROOT.THStack("All Backgrounds _data_obs_", "_data_obs_" )


        for sample in samples:
            #print sample

            if channel == 'tt' and sample == 'data_em' : continue
            if channel == 'em' and sample == 'data_tt' : continue

            if sample == 'data_em' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif sample == 'data_tt' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif sample == 'QCD' :
                tFile = ROOT.TFile('meta/%sBackgrounds/QCDShape%s/shape/data_%s.root' % (grouping, options.qcdShape, channel), 'READ')
            else :
                tFile = ROOT.TFile('%s%s/%s_%s.root' % (grouping, folderDetails, sample, channel), 'READ')


            dic = tFile.Get("%s_Histos" % channel )
            hist = dic.Get( "%s" % var )
            hist.SetDirectory( 0 )


            ''' Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ),
            QCD gets special scaling from bkg estimation, see qcdYield[channel] above for details '''
            #print "PRE Sample: %s      Int: %f" % (sample, hist.Integral() )
            if sample == 'QCD' and hist.Integral() != 0 :
                if channel == 'em' : hist.Scale( qcdYieldEM / hist.Integral() )
                if channel == 'tt' : hist.Scale( qcdYieldTT / hist.Integral() )
            elif 'data' not in sample and hist.Integral() != 0:
                scaler = luminosity * sampDict[ sample ]['Cross Section (pb)'] / ( sampDict[ sample ]['summedWeightsNorm'] )
                if 'TT' in sample :
                    hist.Scale( scaler * bkgsTTScaleFactor )
                else :
                    hist.Scale( scaler )


            hist.SetName( samples[sample][1].strip('_') )
            hist.SetTitle( samples[sample][1].strip('_') )


            hist.Rebin( 20 )
            rebinArray = array.array( 'd', [0,20,40,60,80,100,120,140,160,180,200,250,300,350,400,450,500,550,600] )
            histNew = hist.Rebin( 18, 'rebinned', rebinArray )

            #print "Hist int: %s %f" % (sample, hist.Integral() )
            if samples[ sample ][1] == '_ZTT_' :
                _ZTT_.Add( hist )
            if samples[ sample ][1] == '_QCD_' :
                _QCD_.Add( hist )
            if samples[ sample ][1] == '_TT_' :
                _TT_.Add( hist )
            if samples[ sample ][1] == '_VV_' :
                _VV_.Add( hist )
            if samples[ sample ][1] == '_W_' :
                _W_.Add( hist )
            if samples[ sample ][1] == '_ggH125_' :
                _ggH125_.Add( hist )
            if samples[ sample ][1] == '_vbfH125_' :
                _vbfH125_.Add( hist )
            if samples[ sample ][1] == '_data_obs_' :
                _data_obs_.Add( hist )
            tFile.Close()
        shapeDir.cd()
        _data_obs_.GetStack().Last().Write()
        _ZTT_.GetStack().Last().Write()
        _QCD_.GetStack().Last().Write()
        _TT_.GetStack().Last().Write()
        _W_.GetStack().Last().Write()
        _VV_.GetStack().Last().Write()
        _ggH125_.GetStack().Last().Write()
        _vbfH125_.GetStack().Last().Write()
        shapeFile.Close()

