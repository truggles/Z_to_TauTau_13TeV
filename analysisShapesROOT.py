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
p.add_argument('--samples', action='store', default='dataCards', dest='sampleName', help="Which samples should we run over? : 25ns, 50ns, Sync")
p.add_argument('--folder', action='store', default='2SingleIOAD', dest='folderDetails', help="What's our post-prefix folder name?")
p.add_argument('--blind', action='store', default=True, dest='blind', help="blind data above 150 GeV?")
p.add_argument('--useQCDMake', action='store', default=False, dest='useQCDMake', help="Make a data - MC qcd shape?")
options = p.parse_args()
grouping = options.sampleName
folderDetails = options.folderDetails

print "Running over %s samples" % grouping

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

luminosity = 2090 # / fb 25ns - Final 2015 25ns Golden JSON

# Scaling = 1 for data card sync
qcdTTScaleFactor = 1.06
qcdEMScaleFactor = 1.06
bkgsTTScaleFactor = 1.0

with open('meta/NtupleInputs_%s/samples.json' % grouping) as sampFile :
    sampDict = json.load( sampFile )

                # Sample : Color
samples = OrderedDict()
samples['DYJets']   = ('kOrange-4', '_ZTT120_')
samples['DYJetsLow']   = ('kOrange-4', '_ZTT120_')
samples['T-tW']     = ('kYellow+2', '_VV_')
samples['T-tchan']     = ('kYellow+2', '_VV_')
samples['TT']       = ('kBlue-8', '_TT_')
samples['Tbar-tW']  = ('kYellow-2', '_VV_')
samples['Tbar-tchan']  = ('kYellow-2', '_VV_')
samples['WJets']    = ('kAzure+2', '_W_')
samples['WW1l1nu2q']     = ('kAzure+4', '_VV_')
samples['WW2l2nu']       = ('kAzure+8', '_VV_')
samples['WZ1l1nu2q'] = ('kAzure-6', '_VV_')
samples['WZ1l3nu'] = ('kAzure-6', '_VV_')
samples['WZ2l2q'] = ('kAzure-6', '_VV_')
samples['WZ3l1nu'] = ('kAzure-6', '_VV_')
samples['ZZ2l2nu'] = ('kAzure-12', '_VV_')
samples['ZZ2l2q'] = ('kAzure-12', '_VV_')
samples['ZZ4l'] = ('kAzure-12', '_VV_')
samples['QCD']        = ('kMagenta-10', '_QCD_')
samples['data_tt']  = ('kBlack', '_data_obs_')
samples['data_em']  = ('kBlack', '_data_obs_')
samples['VBFHtoTauTau'] = ('kGreen', '_ggH125_')
samples['ggHtoTauTau'] = ('kGreen', '_vbfH125_')

nameArray = ['_data_obs_','_ZTT120_','_TT_','_QCD_','_VV_','_W_']#,'_ggH125_','_vbfH125_']

channels = { 'em' : 'EMu',
             'tt' : 'TauTau',}

for channel in channels.keys() :

    #if channel == 'tt' : continue
    if channel == 'em' : continue

    # Make an index file for web viewing
    if not os.path.exists( '%sShapes' % grouping ) :
        os.makedirs( '%sShapes' % grouping )

    print channel

    newVarMap = analysisPlots.getHistoDict( channel )
    plotDetails = analysisPlots.getPlotDetails( channel )

    for var, info in newVarMap.iteritems() :
        if not var == 'm_vis' : continue
        print "\n Output shapes file: %sShapes/htt_%s.inputs-sm-13TeV.root \n" % (grouping, channel)
        shapeFile = ROOT.TFile('%sShapes/htt_%s.inputs-sm-13TeV.root' % (grouping, channel), 'RECREATE')
        #shapeDir = shapeFile.mkdir( channels[ channel ] + '_inclusive' )
        shapeDir = shapeFile.mkdir( channel + '_inclusive' )

        # Defined out here for large scope
        name = info[0]
        print "Var: %s      Name: %s" % (var, name)


        binArray = array.array( 'd', [0,20,40,60,80,100,150,200,250,350,600] )
        numBins = len( binArray ) - 1
        histos = {}
        for name in nameArray :
            title = name.strip('_')
            histos[ name ] = ROOT.TH1F( name, name, numBins, binArray )
            #histos[ name ] = ROOT.TH1F( name, name, 60, 0, 600 )


        for sample in samples:
            print sample

            if channel == 'tt' and sample == 'data_em' : continue
            if channel == 'em' and sample == 'data_tt' : continue
            #if sample == 'DYJetsLow' : continue
            if 'HtoTauTau' in sample : continue

            if sample == 'data_em' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif sample == 'data_tt' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif sample == 'QCD' :
                if options.useQCDMake :
                    tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape.root' % (grouping, channel), 'READ')
                else :
                    print " \n\n ### SPECIFY A QCD SHAPE !!! ### \n\n"
            else :
                tFile = ROOT.TFile('%s%s/%s_%s.root' % (grouping, folderDetails, sample, channel), 'READ')


            dic = tFile.Get("%s_Histos" % channel )
            hist = dic.Get( "%s" % var )
            hist.SetDirectory( 0 )
            #print "Hist yield before scaling ",hist.Integral()



            ''' Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ),
            QCD gets special scaling from bkg estimation, see qcdYield[channel] above for details '''
            #print "PRE Sample: %s      Int: %f" % (sample, hist.Integral() )
            if sample == 'QCD' and hist.Integral() != 0 :
                if channel == 'em' : hist.Scale( qcdEMScaleFactor )
                if channel == 'tt' : hist.Scale( qcdTTScaleFactor )
            elif 'data' not in sample and hist.Integral() != 0:
                scaler = luminosity * sampDict[ sample ]['Cross Section (pb)'] / ( sampDict[ sample ]['summedWeightsNorm'] )
                if 'TT' in sample :
                    hist.Scale( scaler * bkgsTTScaleFactor )
                else :
                    hist.Scale( scaler )

            if 'QCD' not in sample :
                #hist.Rebin( 10 )
                #print "hist # bins pre: %i" % hist.GetXaxis().GetNbins()
                hNew = hist.Rebin( numBins, "new%s" % sample, binArray )
                #print "hist # bins post: %i" % hNew.GetXaxis().GetNbins()
                histos[ samples[ sample ][1] ].Add( hNew )
            else :
                histos[ samples[ sample ][1] ].Add( hist )

            #print "Hist yield ",hist.Integral()
            #hist2 = hist.Rebin( 18, 'rebinned', binArray )
            #histos[ samples[ sample ][1] ].Add( hist2 )
            tFile.Close()


        shapeDir.cd()
        for name in histos :
            print "name: %s Yield Pre: %f" % (name, histos[ name ].Integral() )
            # Make sure we have no negative bins
            for bin_ in range( 1, histos[ name ].GetXaxis().GetNbins() ) :
                setVal = 0.001
                if histos[ name ].GetBinContent( bin_ ) < 0 :
                    histos[ name ].SetBinContent( bin_, setVal )
                    print "Set bin %i to value: %f" % (bin_, setVal)
            print "name: %s Yield Post: %f" % (name, histos[ name ].Integral() )
            histos[ name ].GetXaxis().SetRangeUser( 0, 350 )
            histos[ name ].SetTitle( name.strip('_') )
            histos[ name ].SetName( name.strip('_') )
            histos[ name ].Write()
        shapeFile.Close()
