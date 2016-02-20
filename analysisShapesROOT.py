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
p.add_argument('--useQCDMakeName', action='store', default='x', dest='useQCDMakeName', help="Use a specific qcd shape?")
p.add_argument('--sync', action='store', default=False, dest='sync', help="Is this for data card sync?")
p.add_argument('--ztt', action='store', default=False, dest='ztt', help="Is Z->tautau the signal POI?")
p.add_argument('--mssm', action='store', default=False, dest='mssm', help="Is this the MSSM H->TauTau search?")
p.add_argument('--category', action='store', default='inclusive', dest='category', help="directory name channel_[category]?")
p.add_argument('--channels', action='store', default='em,tt', dest='channels', help="What channels?")
options = p.parse_args()
grouping = options.sampleName
folderDetails = options.folderDetails

print "Running over %s samples" % grouping

ROOT.gROOT.SetBatch(True)
tdr.setTDRStyle()

luminosity = 2246.0 # / fb 25ns

# Scaling = 1 for data card sync
qcdTTScaleFactor = 1.06
qcdEMScaleFactor = 1.06
bkgsTTScaleFactor = 1.0
qcdTTScaleFactorNew = 0.49 # no 2 prong, baseline

with open('meta/NtupleInputs_%s/samples.json' % grouping) as sampFile :
    sampDict = json.load( sampFile )

                # Sample : Color
samples = OrderedDict()
#samples['DYJets']   = ('kOrange-4', '_ZTT_')
samples['DYJets-ZTT']   = ('kOrange-4', '_ZTT_')
samples['DYJets-ZL']   = ('kOrange-4', '_ZL_')
samples['DYJets-ZJ']   = ('kOrange-4', '_ZJ_')
samples['DYJets-ZLL']   = ('kOrange-4', '_ZLL_')
#samples['DYJets100-200']   = ('kOrange-4', '_ZTT_')
#samples['DYJets200-400']   = ('kOrange-4', '_ZTT_')
#samples['DYJets400-600']   = ('kOrange-4', '_ZTT_')
#samples['DYJets600-Inf']   = ('kOrange-4', '_ZTT_')
#samples['DYJetsLow']   = ('kOrange-4', '_ZTT_')
samples['T-tW']     = ('kYellow+2', '_VV_')
samples['T-tchan']     = ('kYellow+2', '_VV_')
samples['TT']       = ('kBlue-8', '_TT_')
samples['Tbar-tW']  = ('kYellow-2', '_VV_')
samples['Tbar-tchan']  = ('kYellow-2', '_VV_')
samples['WJets']    = ('kAzure+2', '_W_')
#samples['WJets100-200']    = ('kAzure+2', '_W_')
#samples['WJets200-400']    = ('kAzure+2', '_W_')
#samples['WJets400-600']    = ('kAzure+2', '_W_')
#samples['WJets600-Inf']    = ('kAzure+2', '_W_')
samples['WW1l1nu2q']     = ('kAzure+4', '_VV_')
#samples['WW2l2nu']       = ('kAzure+8', '_VV_')
samples['WZ1l1nu2q'] = ('kAzure-6', '_VV_')
samples['WZ1l3nu'] = ('kAzure-6', '_VV_')
#samples['WZ2l2q'] = ('kAzure-6', '_VV_')
#samples['WZ3l1nu'] = ('kAzure-6', '_VV_')
#samples['ZZ2l2nu'] = ('kAzure-12', '_VV_')
samples['ZZ2l2q'] = ('kAzure-12', '_VV_')
samples['ZZ4l'] = ('kAzure-12', '_VV_')
samples['QCD']        = ('kMagenta-10', '_QCD_')
samples['data_tt']  = ('kBlack', '_data_obs_')
samples['data_em']  = ('kBlack', '_data_obs_')
samples['VBFHtoTauTau125'] = ('kGreen', '_ggH125_')
samples['ggHtoTauTau125'] = ('kGreen', '_vbfH125_')

nameArray = ['_data_obs_','_ZTT_','_ZL_','_ZJ_','_ZLL_','_TT_','_QCD_','_VV_','_W_','_ggH125_','_vbfH125_']

if options.mssm :
    #masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 600, 900, 1000, 1200, 1500, 2900, 3200]
    masses = [80, 100, 110, 120, 130, 140, 160, 180, 600, 900, 1000, 1200, 1500, 2900]
    for mssmMass in masses :
        samples['ggH%i' % mssmMass] = ('kPink', '_ggH%i_' % mssmMass)
        samples['bbH%i' % mssmMass] = ('kPink', '_bbH%i_' % mssmMass) 
        nameArray.append('_ggH%i_' % mssmMass)
        nameArray.append('_bbH%i_' % mssmMass)
    del samples['VBFHtoTauTau125']
    del samples['ggHtoTauTau125']
    nameArray.remove('_vbfH125_')
    nameArray.remove('_ggH125_')


extra = ''
if not os.path.exists( '%sShapes' % grouping ) :
    os.makedirs( '%sShapes' % grouping )
if options.ztt : 
    if not os.path.exists( '%sShapes/ztt' % grouping ) :
        os.makedirs( '%sShapes/ztt' % grouping )
    extra = 'ztt'
elif options.mssm : 
    if not os.path.exists( '%sShapes/mssm' % grouping ) :
        os.makedirs( '%sShapes/mssm' % grouping )
    extra = 'mssm'
#if not options.ztt : 
else : 
    if not os.path.exists( '%sShapes/htt' % grouping ) :
        os.makedirs( '%sShapes/htt' % grouping )
    extra = 'htt'

if options.ztt :
    del samples['VBFHtoTauTau125']
    del samples['ggHtoTauTau125']
    #XXX#samples['DYJets'] = ('kOrange-4', '_ZTT_')
    #XXX#samples['DYJets'] = ('kOrange-4', '_ZTT90_')
    #XXX#samples['DYJetsLow'] = ('kOrange-4', '_ZTT90_')
    nameArray.remove('_vbfH125_')
    nameArray.remove('_ggH125_')
    #XXX#nameArray.remove('_ZTT_')
    #XXX#nameArray.append('_ZTT90_')

for channel in ['em', 'tt'] :

    #if channel == 'tt' : continue
    #if channel == 'em' : continue
    if 'tt' not in options.channels and channel == 'tt' : continue
    if 'em' not in options.channels and channel == 'em' : continue

    if channel == 'tt' :
        del samples['DYJets-ZLL']
        nameArray.remove('_ZLL_')
    if channel == 'em' :
        del samples['DYJets-ZJ']
        nameArray.remove('_ZJ_')
        del samples['DYJets-ZL']
        nameArray.remove('_ZL_')

    print channel

    newVarMap = analysisPlots.getHistoDict( channel )
    plotDetails = analysisPlots.getPlotDetails( channel )

    for var, info in newVarMap.iteritems() :
        mid = ''
        if options.mssm :
            if not var == 'm_vis_mssm' : continue
            mid = 'mssm'
        else :
            if not var == 'm_vis' : continue
            mid = 'sm'
        print "\n Output shapes file: %sShapes/%s/htt_%s.inputs-%s-13TeV.root \n" % (grouping, extra, channel, mid)

        shapeFile = ROOT.TFile('%sShapes/%s/htt_%s.inputs-%s-13TeV.root' % (grouping, extra, channel, mid), 'RECREATE')
        shapeDir = shapeFile.mkdir( channel + '_%s' % options.category )

        # Defined out here for large scope
        name = info[0]
        print "Var: %s      Name: %s" % (var, name)

        if not options.sync :
            binArray = array.array( 'd', [0,20,40,60,80,100,150,200,250,350,600] )
        if options.mssm :
            binArray = array.array( 'd', [0,20,40,60,80,100,150,200,250,350,600,1000,1500,2000,2500,3500] )
        else :
            binArray = array.array( 'd', [] )
            for i in range(0, 36 ) :
                binArray.append( i * 10 )
            #binArray.append( 600 )
        print binArray
        numBins = len( binArray ) - 1
        histos = {}
        for name in nameArray :
            title = name.strip('_')
            histos[ name ] = ROOT.TH1F( name, name, numBins, binArray )


        for sample in samples:

            if channel == 'tt' and sample == 'data_em' : continue
            if channel == 'em' and sample == 'data_tt' : continue
            #if sample == 'DYJetsLow' : continue
            #if 'HtoTauTau' in sample : continue
            print sample

            if sample == 'data_em' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif sample == 'data_tt' :
                tFile = ROOT.TFile('%s%s/%s.root' % (grouping, folderDetails, sample), 'READ')
            elif sample == 'QCD' :
                if options.useQCDMake :
                    if options.useQCDMakeName != 'x'  :
                        print "Use QCD MAKE NAME: ",options.useQCDMakeName
                        tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s.root' % (grouping, channel, options.useQCDMakeName), 'READ')
                    else :
                        tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape.root' % (grouping, channel), 'READ')
                    print "Got 'useQCDMake' QCD Shape"
                else :
                    print " \n\n ### SPECIFY A QCD SHAPE !!! ### \n\n"
            else :
                tFile = ROOT.TFile('%s%s/%s_%s.root' % (grouping, folderDetails, sample, channel), 'READ')


            dic = tFile.Get("%s_Histos" % channel )
            hist = dic.Get( "%s" % var )
            hist.SetDirectory( 0 )
            print "Hist yield before scaling ",hist.Integral()



            ''' Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ),
            QCD gets special scaling from bkg estimation, see qcdYield[channel] above for details '''
            #print "PRE Sample: %s      Int: %f" % (sample, hist.Integral() )
            if sample == 'QCD' and options.useQCDMakeName :
                if channel == 'tt' : qcdScale = qcdTTScaleFactor
                if channel == 'em' : qcdScale = qcdEMScaleFactor
                print "Skip rebin; Scale QCD shape by %f" % qcdScale
                print "QCD yield Pre: %f" % hist.Integral()
                #hist.Scale( qcdTTScaleFactorNew )
                hist.Scale( qcdScale )
                print "QCD yield Post Scale: %f" % hist.Integral()
            elif sample == 'QCD' and hist.Integral() != 0 :
                if channel == 'em' : hist.Scale( qcdEMScaleFactor )
                if channel == 'tt' : hist.Scale( qcdTTScaleFactor )
            elif 'data' not in sample and hist.Integral() != 0:
                if 'TT' in sample :
                    hist.Scale( bkgsTTScaleFactor )

            if 'QCD' not in sample :
                #hist.Rebin( 10 )
                #print "hist # bins pre: %i" % hist.GetXaxis().GetNbins()
                hNew = hist.Rebin( numBins, "new%s" % sample, binArray )
                #print "hist # bins post: %i" % hNew.GetXaxis().GetNbins()
                histos[ samples[ sample ][1] ].Add( hNew )
            else :
                #print "hist # bins pre: %i" % hist.GetXaxis().GetNbins()
                hNew = hist.Rebin( numBins, "new%s" % sample, binArray )
                #print "hist # bins post: %i" % hNew.GetXaxis().GetNbins()
                histos[ samples[ sample ][1] ].Add( hNew )

            #print "Hist yield ",hist.Integral()
            #hist2 = hist.Rebin( 18, 'rebinned', binArray )
            #histos[ samples[ sample ][1] ].Add( hist2 )
            tFile.Close()


        shapeDir.cd()
        for name in histos :
            #print "name: %s Yield Pre: %f" % (name, histos[ name ].Integral() )
            # Make sure we have no negative bins
            for bin_ in range( 1, histos[ name ].GetXaxis().GetNbins()+1 ) :
                setVal = 0.0
                if histos[ name ].GetBinContent( bin_ ) < 0 :
                    histos[ name ].SetBinContent( bin_, setVal )
                    print "name: %s   Set bin %i to value: %f" % (name, bin_, setVal)
            #print "name: %s Yield Post: %f" % (name, histos[ name ].Integral() )
            if not options.mssm :
                histos[ name ].GetXaxis().SetRangeUser( 0, 350 )
            histos[ name ].SetTitle( name.strip('_') )
            histos[ name ].SetName( name.strip('_') )
            histos[ name ].Write()
        shapeFile.Close()
