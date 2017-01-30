from util.buildTChain import makeTChain
import ROOT
import json
from collections import OrderedDict
import pyplotter.plot_functions as pyplotter #import setTDRStyle, getCanvas
import pyplotter.tdrstyle as tdr
import argparse
import analysisPlots
from util.splitCanvas import fixFontSize
from array import array
from analysisPlots import skipSystShapeVar
from util.helpers import checkDir, unroll2D, returnSortedDict
from analysis1BaselineCuts import skipChanDataCombo
import os
from smart_getenv import getenv


def makeDataCards( analysis, inSamples, channels, folderDetails, **kwargs ) :
    assert( type(inSamples) == type(OrderedDict())
        or type(inSamples) == type({}) ), "Provide a samples list which \
        is a dict or OrderedDict"

    ops = {
    'useQCDMakeName' : 'x',
    'qcdSF' : 1.0,
    'mssm' : False,
    'category' : 'inclusive',
    'fitShape' : 'm_vis',
    'btag' : False,
    'ES' : False,
    'tauPt' : False,
    'sync' : False,
    'redBkg' : False,
    'allShapes' : False,}

    for key in kwargs :
        #print "another keyword arg: %s: %s" % (key, kwargs[key])
        if key in ops.keys() :
             ops[key] = kwargs[key]

    print ops

    # Use FF built QCD backgrounds
    doFF = getenv('doFF', type=bool)

    """ Add in the gen matched DY catagorization """
    # FIXME - do this later
    print "\n Samples currently hardcoded \n"

    
    ROOT.gROOT.SetBatch(True)
    tdr.setTDRStyle()
    
    
    with open('meta/NtupleInputs_%s/samples.json' % analysis) as sampFile :
        sampDict = json.load( sampFile )
    
    # Build samples list with val for which grouping each sample belongs to
    samples = OrderedDict()
    genMap = ['ZTT', 'ZLL', 'ZL', 'ZJ']
    dyJets = ['DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4',]# 'DYJetsLow']
    for dyj in dyJets :
        for gen in genMap : samples[dyj+'-'+gen] = gen
    #print samples
    samples['T-tW']       = 'VV'
    samples['T-tchan']    = 'VV'
    samples['Tbar-tW']    = 'VV'
    samples['Tbar-tchan'] = 'VV'
    samples['WJets']      = 'W'
    samples['WJets1']     = 'W'
    samples['WJets2']     = 'W'
    samples['WJets3']     = 'W'
    samples['WJets4']     = 'W'
    samples['WW1l1nu2q']  = 'VV'
    samples['WW2l2nu']    = 'VV'
    samples['WZ1l1nu2q']  = 'VV'
    samples['WZ1l3nu']    = 'VV'
    samples['WZ2l2q']     = 'VV'
    samples['WZ3l1nu']    = 'VV'
    samples['ZZ2l2nu']    = 'VV'
    samples['ZZ2l2q']     = 'VV'
    samples['ZZ4l']       = 'VV'
    samples['VV']         = 'VV'
    samples['WWW']        = 'VV'
    samples['ZZZ']        = 'VV'
    samples['EWKWPlus']   = 'W'
    samples['EWKWMinus']  = 'W'
    samples['EWKZ2l']     = 'EWKZ'
    samples['EWKZ2nu']    = 'EWKZ'
    samples['QCD']        = 'QCD'

    eras =  ['B', 'C', 'D', 'E', 'F', 'G', 'H']
    for era in eras :
        samples['dataTT-%s' % era]  = 'data_obs'
        samples['dataEE-%s' % era]  = 'data_obs'
        samples['dataMM-%s' % era]  = 'data_obs'

    for mass in ['120', '125', '130'] :
        samples['VBFHtoTauTau%s' % mass] = 'qqH%s' % mass
        samples['ggHtoTauTau%s' % mass] = 'ggH%s' % mass
        samples['WMinusHTauTau%s' % mass] = 'WH%s' % mass
        samples['WPlusHTauTau%s' % mass] = 'WH%s' % mass
        samples['ZHTauTau%s' % mass] = 'ZH%s' % mass
    
    if ops['mssm'] : # FIXME - make sure SM Higgs 120 and 130 don't overlap?
        masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
        for mssmMass in masses :
            samples['ggH%i' % mssmMass] = 'ggH%i' % mssmMass
            samples['bbH%i' % mssmMass] = 'bbH%i' % mssmMass 

    if analysis == 'azh' :
        samples['ZZ4l'] = 'ZZ'
        for era in eras :
            samples['RedBkgShape-%s' % era] = 'RedBkg'

    if doFF :
        samples['QCD'] = 'jetFakes'
    
    # Remove samples which are not part of input samples
    # and build list of names/samples which will be used
    # for a given final channel. This differs for some HTT
    # channels
    nameArray = []
    for samp in samples :

        # Keep QCD if normal htt analysis
        if samp == 'QCD' and analysis == 'htt' and not doFF :
            if samples[samp] not in nameArray : nameArray.append( samples[samp] )

        if samp not in inSamples.keys() :
            del samples[samp]
            continue
        if samples[samp] not in nameArray : nameArray.append( samples[samp] )
    # Add DYJets gen splitting and ttbar
    genMapDYJ = ['ZTT', 'ZLL', 'ZL', 'ZJ']
    genMapTT = ['TTT', 'TTJ']
    for samp in inSamples.keys() :
        if 'DYJets' in samp and not '-' in samp : # '-' means we already have Gen additions
            for gen in genMapDYJ : samples[samp+'-'+gen] = gen
        if samp == 'TT' and not '-' in samp : # '-' means we already have Gen additions
            for gen in genMapTT : samples[samp+'-'+gen] = gen
    # Using final samples map, build nameArray
    for samp in samples :
        if samples[samp] not in nameArray : nameArray.append( samples[samp] )
    
    extra = ''
    checkDir( '%sShapes' % analysis )
    if ops['mssm'] : 
        checkDir( '%sShapes/mssm' % analysis )
        extra = 'mssm'
    if analysis == 'azh' :
        extra = 'azh'
    else : 
        checkDir( '%sShapes/htt' % analysis )
        extra = 'htt'
    
    for channel in channels :
    
        if channel == 'tt' :
            for sample in samples.keys() :
                if '-ZLL' in sample :
                    del samples[ sample ]
            if 'ZLL' in nameArray : nameArray.remove('ZLL')
        if channel == 'em' :
            for sample in samples.keys() :
                if sample[-3:] == '-ZL' or '-ZJ' in sample :
                    del samples[ sample ]
            if 'ZJ' in nameArray : nameArray.remove('ZJ')
            if 'ZL' in nameArray : nameArray.remove('ZL')


        print nameArray    
        print channel
    
        newVarMapUnsorted = analysisPlots.getHistoDict( analysis, channel )
        newVarMap = returnSortedDict( newVarMapUnsorted )
    
        baseVar = ops['fitShape']
        #if 'data' in sample : print "Fitting",baseVar
        appendMap = {
            'm_vis' : 'visMass',
            'm_sv' : 'svFitMass',
            'mt_sv' : 'svFitMt',
            'mt_tot' : 'mtTot',
            #'pt_sv:m_sv' : 'svFitMass2D',
            #'mjj:m_sv' : 'svFitMass2D',
            'Higgs_Pt:m_vis' : 'visMass2D',
            'mjj:m_vis' : 'visMass2D',
            'Mass' : '4LMass',
            }
        if '0jet2D' in ops['category'] : 
            #append = '_svFitMass2D'
            append = '_visMass2D'
        else :
            append = '_'+appendMap[baseVar]
    
        if ops['mssm'] :
        #    if not var == baseVar+'_mssm' : continue
            mid = 'mssm'
        else :
            mid = 'sm'
    
        nameChan = 'tt' if analysis != 'azh' else 'zh'
        shapeFile = ROOT.TFile('%sShapes/%s/htt_%s.inputs-%s-13TeV%s.root' % (analysis, extra, nameChan, mid, append), 'UPDATE')
        # We have two pathways to create tt_0jet and need to maintain their seperate root files for 1D vs 2D
        # so we need this override that renames 0jet2D -> 0jet and places in the unrolled root file
        if '0jet2D' in ops['category'] : 
            cr = '_qcd_cr' if '_qcd_cr' in ops['category'] else ''
            shapeDir = shapeFile.mkdir( channel + '_0jet'+cr, channel + '_0jet'+cr )
        else :
            shapeDir = shapeFile.mkdir( channel + '_%s' % ops['category'], channel + '_%s' % ops['category'] )
        assert( shapeDir != None ), "It looks like the directory already exists, remove the old root file and start again: rm httShapes/htt/htt_tt.inputs-sm-13TeV_ ..."
    
        for var in newVarMap.keys() :
    
            print var
            if not baseVar in var : continue
            if ops['fitShape'] == 'm_sv' and ':' in var : continue # Get rid of the 2D shapes in 0jet
            if ops['fitShape'] == 'm_vis' and ':' in var : continue # Get rid of the 2D shapes in 0jet
            print "\n\n=============================================================="
            if ops['allShapes'] :
                print "All Shapes Applied: %s" % var
                #if not (('_energyScale' in var) or ('_tauPt' in var)  or ('_zPt' in var) or ('_topPt' in var) or (baseVar == var)) :
                if doFF :
                    if not (('_energyScale' in var) or ('_zPt' in var) or\
                            ('_ffSyst' in var) or ('_ffStat' in var) or ('_topPt' in var) or\
                            ('_metResponse' in var) or ('_metResolution' in var)\
                            or ('_ffSub' in var) or (baseVar == var)) :
                        continue

                else :
                    if not (('_energyScale' in var) or ('_zPt' in var) or ('_topPt' in var) \
                        or ('_JES' in var) or ('_ggH' in var) or ('_JetToTau' in var) \
                        or ('_Zmumu' in var) or (baseVar == var)) :
                        print "Did we fail?"
                        continue
            #if ops['mssm'] :
            #    if not var == baseVar+'_mssm' : continue
            #    if var != baseVar : continue
            #elif ops['ES'] :
            elif ops['ES'] and not ops['tauPt'] :
                if not (('_energyScaleUp' in var) or ('_energyScaleDown' in var) or (baseVar == var)) : continue
            elif ops['tauPt'] and not ops['ES'] :
                if not (('_tauPtUp' in var) or ('_tauPtDown' in var) or (baseVar == var)) : continue
            elif ops['tauPt'] and ops['ES'] :
                if not (('_energyScaleUp' in var) or ('_energyScaleDown' in var) or ('_tauPtUp' in var) or ('_tauPtDown' in var) or (baseVar == var)) : continue
            else :
                if not var == baseVar : continue
    
    
            # Defined out here for large scope
            print "\nVar: ",var
    
            #print "MSSM btag option:",ops['btag']
            binArray = array( 'd', [] )
            if ops['mssm'] :
                print "MSSM btag option:",ops['btag']
                #if ops['btag'] == True :
                #if doBTagging == True :
                if 'ZTT' in folderDetails :
                    print "Inclusive"
                    binArray = array( 'd', [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900] )
                elif 'NoBTL' in ops['folderDetails'] :
                    print "No-BTAGGING"
                    binArray = array( 'd', [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900] )
                elif 'NoBTL' not in ops['folderDetails'] :
                    print "BTAGGING"
                    binArray = array( 'd', [0,20,40,60,80,100,120,140,160,180,200,250,300,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900] )

            elif var == 'mt_tot' :
                binArray = array( 'd', [0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,\
                        80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,\
                        170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,\
                        350.0,400.0,500.0,700.0,900.0, 1100.0,1300.0,1500.0,\
                        1700.0,1900.0,2100.0,2300.0,2500.0,2700.0,2900.0,3100.0,\
                        3300.0,3500.0,3700.0,3900.0] )
            elif ops['sync'] :
                binArray = array( 'd', [i*20 for i in range( 11 )] )
            # This is the proposed binning for ZTT 2015 paper
            elif doFF and ('m_sv' in var or 'm_vis' in var) :
                binArray = array( 'd', [i*10 for i in range( 31 )] )
            else :
                if ":" in var : binArray = array( 'd', [i for i in range( 49 )] )
                elif ops['category'] in ['1jet_low', '1jet_high'] :
                    binArray = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
                elif 'vbf' in ops['category'] :
                    binArray = array( 'd', [0,40,60,80,100,120,150,200,250] )
                else :
                    binArray = array( 'd', [i*10 for i in range( 31 )] )
            numBins = len( binArray ) - 1
            #print binArray
            #print numBins

            histos = OrderedDict()
            for name in nameArray :
                title = name
                if ops['ES'] or ops['tauPt'] or ops['allShapes'] :

                    if '_' in var and ('Up' in var or 'Down' in var) :
                        systName = var.split('_')[-1]
                        histos[ name ] = ROOT.TH1D( name+systName, name+systName, numBins, binArray )
                    #if '_energyScaleUp' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'energyScaleUp', name+'energyScaleUp', numBins, binArray )
                    #elif '_energyScaleDown' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'energyScaleDown', name+'energyScaleDown', numBins, binArray )
                    #elif '_tauPtUp' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'tauPtUp', name+'tauPtUp', numBins, binArray )
                    #elif '_tauPtDown' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'tauPtDown', name+'tauPtDown', numBins, binArray )
                    #elif '_zPtUp' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'zPtUp', name+'zPtUp', numBins, binArray )
                    #elif '_zPtDown' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'zPtDown', name+'zPtDown', numBins, binArray )
                    #elif '_topPtUp' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'topPtUp', name+'topPtUp', numBins, binArray )
                    #elif '_topPtDown' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'topPtDown', name+'topPtDown', numBins, binArray )
                    #elif '_JESUp' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'JESUp', name+'JESUp', numBins, binArray )
                    #elif '_JESDown' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'JESDown', name+'JESDown', numBins, binArray )
                    #elif '_JetToTauUp' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'jetToTauUp', name+'jetToTauUp', numBins, binArray )
                    #elif '_JetToTauDown' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'jetToTauDown', name+'jetToTauDown', numBins, binArray )
                    #elif '_ggHUp' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'ggHUp', name+'ggHUp', numBins, binArray )
                    #elif '_ggHDown' in var :
                    #    histos[ name ] = ROOT.TH1D( name+'ggHDown', name+'ggHDown', numBins, binArray )
                    #elif '_ffSystUp' in var and doFF :
                    #    histos[ name ] = ROOT.TH1D( name+'ffSystUp', name+'ffSystUp', numBins, binArray )
                    #elif '_ffSystDown' in var and doFF :
                    #    histos[ name ] = ROOT.TH1D( name+'ffSystDown', name+'ffSystDown', numBins, binArray )
                    #elif '_ffStatUp' in var and doFF :
                    #    histos[ name ] = ROOT.TH1D( name+'ffStatUp', name+'ffStatUp', numBins, binArray )
                    #elif '_ffStatDown' in var and doFF :
                    #    histos[ name ] = ROOT.TH1D( name+'ffStatDown', name+'ffStatDown', numBins, binArray )
                    #elif '_metResponseUp' in var and doFF :
                    #    histos[ name ] = ROOT.TH1D( name+'metResponseUp', name+'metResponseUp', numBins, binArray )
                    #elif '_metResponseDown' in var and doFF :
                    #    histos[ name ] = ROOT.TH1D( name+'metResponseDown', name+'metResponseDown', numBins, binArray )
                    #elif '_metResolutionUp' in var and doFF :
                    #    histos[ name ] = ROOT.TH1D( name+'metResolutionUp', name+'metResolutionUp', numBins, binArray )
                    #elif '_metResolutionDown' in var and doFF :
                    #    histos[ name ] = ROOT.TH1D( name+'metResolutionDown', name+'metResolutionDown', numBins, binArray )
                    else :
                        histos[ name ] = ROOT.TH1D( name, name, numBins, binArray )
                else :
                    histos[ name ] = ROOT.TH1D( name, name, numBins, binArray )
                histos[ name ].Sumw2()
    
    
            for sample in samples:
    
                ''' Skip plotting unused shape systematics '''
                if skipSystShapeVar( var, sample, channel ) : continue
                if '_topPt' in var : print "Top Pt still in Var: "+var+" sample: "+sample
    
                # Skip looping over nonsense channel / sample combos
                if skipChanDataCombo( channel, sample, analysis ) : continue

                #if sample == 'DYJetsLow' : continue
                #if 'HtoTauTau' in sample : continue
                #print sample
    
                if sample == 'dataEM' :
                    tFile = ROOT.TFile('%s%s/%s_em.root' % (analysis, folderDetails, sample), 'READ')
                elif 'dataTT' in sample :
                    tFile = ROOT.TFile('%s%s/%s_tt.root' % (analysis, folderDetails, sample), 'READ')
                elif sample == 'QCD' :
                    if ops['useQCDMakeName'] != 'x'  :
                        print "Use QCD MAKE NAME: ",ops['useQCDMakeName']
                        tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s.root' % (analysis, channel, ops['useQCDMakeName']), 'READ')
                    elif doFF :
                        tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                        print " \n### Using Fake Factor QCD Shape !!! ###\n"
                    else :
                        print " \n\n ### SPECIFY A QCD SHAPE !!! ### \n\n"
                elif ops['redBkg'] and 'RedBkgShape' in sample :
                    tFileYield = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample.replace('Shape','Yield'), channel), 'READ')
                    tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                else :
                    tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
    
    
                dic = tFile.Get("%s_Histos" % channel )
                if not doFF :
                    hist = dic.Get( "%s" % var )
                if doFF :
                    if sample == 'QCD' :
                        hist = dic.Get( "%s_ffSub" % var )
                    else :
                        hist = dic.Get( "%s" % var )
                        if 'DYJets' in sample or sample == 'TT' or 'WJets' in sample :
                            if not '_ffSub' in var :
                                ffSubHist = dic.Get( var+'_ffSub' )
                                #print sample," FF Sub int",ffSubHist.Integral()
                                ffSubHist2 = ffSubHist.Rebin( numBins, "rebinned", binArray )
                                ffSubHist2.GetXaxis().SetRangeUser( binArray[0], binArray[-1] )
                                if "DYJets" in sample and "ZTT" in sample :
                                    ffSubHist2.Scale( zttScaleTable[ops['category']] )
                                histos[ 'jetFakes' ].Add( ffSubHist2, -1.0 )
                hist.SetDirectory( 0 )
                #print "Hist yield before scaling ",hist.Integral()
    

                """ Scale reducible bkg shape by yield estimate """
                if ops['redBkg'] and 'RedBkgShape' in sample :
                    redBkgYield = tFileYield.Get('%s_Histos/%s' % (channel, var)).Integral()
                    if hist.Integral() != 0 :
                        hist.Scale( redBkgYield / hist.Integral() )
    
    
                ''' Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ),
                QCD gets special scaling from bkg estimation, see qcdYield[channel] above for details '''
                #print "PRE Sample: %s      Int: %f" % (sample, hist.Integral() )
                if sample == 'QCD' and ops['useQCDMakeName'] != 'x' :
                    #print "Using QCD SCALE FACTOR <<<< NEW >>>>"
                    qcdScale = ops['qcdSF']
                    assert( qcdScale > 0. ), "\nQCD Scale is wrong, you probably need to rerun all channels together\n"
                    print "Skip rebin; Scale QCD shape by %f" % qcdScale
                    #print "QCD yield Pre: %f" % hist.Integral()
                    hist.Scale( qcdScale )
                    #print "QCD yield Post Scale: %f" % hist.Integral()
    
                #if 'QCD' not in sample :
                #    #hist.Rebin( 10 )
                #    #print "hist # bins pre: %i" % hist.GetXaxis().GetNbins()
                #    hNew = hist.Rebin( numBins, "new%s" % sample, binArray )
                #    #print "hist # bins post: %i" % hNew.GetXaxis().GetNbins()
                #    histos[ samples[ sample ] ].Add( hNew )
                #else :
                #    #print "hist # bins pre: %i" % hist.GetXaxis().GetNbins()
                #    hNew = hist.Rebin( numBins, "new%s" % sample, binArray )
                #    #print "hist # bins post: %i" % hNew.GetXaxis().GetNbins()
                #    histos[ samples[ sample ] ].Add( hNew )
                if ":" in var :
                    hNew = unroll2D( hist )
                    #print "nbinsX",hNew.GetNbinsX() ,hNew.GetBinLowEdge(1),hNew.GetBinLowEdge( hNew.GetNbinsX()+1 )
                else :
                    hNew = hist.Rebin( numBins, "new%s" % sample, binArray )

                # If using the qcd CR, we want a single bin for all
                if '_qcd_cr' in ops['category'] :
                    nBins = hNew.GetNbinsX()
                    hNew.Rebin( nBins )
                    # If histos haven't been Rebinned, do it
                    nBinsHistos = histos[ samples[ sample ] ].GetNbinsX()
                    if nBins == nBinsHistos :
                        histos[ samples[ sample ] ].Rebin( nBins )

                histos[ samples[ sample ] ].Add( hNew )
    
                if ops['mssm'] and not 'ggH' in sample and not 'bbH' in sample :
                    print "SampleName: %20s   Hist yield %.2f" % (sample, hist.Integral())
                else :
                    print "SampleName: %20s   Hist yield %.2f" % (sample, hist.Integral())
                #hist2 = hist.Rebin( 18, 'rebinned', binArray )
                #histos[ samples[ sample ] ].Add( hist2 )
                tFile.Close()
    
    
            print ".............................................................."
            shapeDir.cd()
            for name in histos :
                #print "name: %s Yield Pre: %f" % (name, histos[ name ].Integral() )
                # Make sure we have no negative bins
                for bin_ in range( 1, histos[ name ].GetXaxis().GetNbins()+1 ) :
                    setVal = 0.0
                    if histos[ name ].GetBinContent( bin_ ) < 0 :
                        histos[ name ].SetBinContent( bin_, setVal )
                        print "name: %s   Set bin %i to value: %f" % (name, bin_, setVal)
                if histos[ name ].Integral() != 0.0 :
                    print "DataCard Name: %10s Yield Post: %.2f" % (name, histos[ name ].Integral() )
                #if not ops['mssm'] :
                #    histos[ name ].GetXaxis().SetRangeUser( 0, 350 )
                
    
                # Proper naming of output histos
                if (ops['ES'] or ops['allShapes']) and ('_energyScale' in var or '_tauPt' in var or '_zPt' in var \
                        or '_JES' in var or '_topPt' in var or '_ggH' in var or '_JetToTau' in var or '_Zmumu' in var) :

                    # Systematics naming removes CRs
                    category = ops['category'].strip('_qcd_cr')

                    if name in ['data_obs','QCD'] : continue 
                    if name == 'jetFakes' and not doFF : continue
                    if name == 'jetFakes' and not ('_ffSyst' in var or '_ffStat' in var) : continue
                    if '_ggH' in var and not name in ['ggH120','ggH125','ggH130'] : continue
                    if '_JetToTau' in var and not name in ['W', 'TTJ', 'ZJ'] : continue
                    if '_Zmumu' in var and (name not in ['ZTT', 'ZL', 'ZJ'] or \
                            category != 'VBF') : continue # Shape only used in VBF category atm
                    lep = 'x'
                    if channel == 'tt' : lep = 't'
                    if channel == 'em' : lep = 'e'

                    # JES Breakdown
                    shiftDir = ''
                    if var[-2:] == 'Up' : shiftDir = 'Up'
                    if var[-4:] == 'Down' : shiftDir = 'Down'
                    if '_JES' in var :
                        print var
                        jesUnc = var.split('_')[-1]
                        print jesUnc
                        jesUnc = jesUnc.replace('JES', '')
                        print jesUnc
                        if 'Up' in jesUnc[-2:] : jesUnc = jesUnc[:-2]
                        print jesUnc
                        if 'Down' in jesUnc[-4:] : jesUnc = jesUnc[:-4]
                        print jesUnc
                        jesUnc += '_13TeV'+shiftDir
                        print jesUnc
    
                    if '_zPt' in var :
                        if name not in ['ZTT','ZL','ZJ','ZLL',] : continue
                        elif '_zPtUp' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_dyShape_13TeVUp' )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_dyShape_13TeVUp' )
                        elif '_zPtDown' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_dyShape_13TeVDown' )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_dyShape_13TeVDown' )
                    elif '_topPt' in var :
                        if name not in ['_TTT_','_TTJ_'] : continue
                        elif '_topPtUp' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_ttbarShape_13TeVUp' )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_ttbarShape_13TeVUp' )
                        elif '_topPtDown' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_ttbarShape_13TeVDown' )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_ttbarShape_13TeVDown' )
                    #elif name in ['TTT','TTJ'] : continue # this is to catch TT when it's not wanted
                    elif '_energyScaleUp' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_'+lep+'_'+channel+'_13TeVUp' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_'+lep+'_'+channel+'_13TeVUp' )
                    elif '_energyScaleDown' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_'+lep+'_'+channel+'_13TeVDown' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_'+lep+'_'+channel+'_13TeVDown' )
                    elif '_JES' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_j_'+jesUnc )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_j_'+jesUnc )
                    #elif '_JESUp' in var :
                    #    histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_j_13TeVUp' )
                    #    histos[ name ].SetName( name.strip('_')+'_CMS_scale_j_13TeVUp' )
                    #elif '_JESDown' in var :
                    #    histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_j_13TeVDown' )
                    #    histos[ name ].SetName( name.strip('_')+'_CMS_scale_j_13TeVDown' )
                    elif '_JetToTauUp' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_jetToTauFake_13TeVUp' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_htt_jetToTauFake_13TeVUp' )
                    elif '_JetToTauDown' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_jetToTauFake_13TeVDown' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_htt_jetToTauFake_13TeVDown' )
                    elif '_tauPtUp' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_eff_t_mssmHigh_'+channel+'_13TeVUp' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_eff_t_mssmHigh_'+channel+'_13TeVUp' )
                    elif '_tauPtDown' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_eff_t_mssmHigh_'+channel+'_13TeVDown' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_eff_t_mssmHigh_'+channel+'_13TeVDown' )
                    elif '_ggHUp' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_gg_13TeVUp' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_gg_13TeVUp' )
                    elif '_ggHDown' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_gg_13TeVDown' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_gg_13TeVDown' )
                    elif '_ZmumuUp' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_zmumuShape_'+category+'_13TeVUp' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_htt_zmumuShape_'+category+'_13TeVUp' )
                    elif '_ZmumuDown' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_zmumuShape_'+category+'_13TeVDown' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_htt_zmumuShape_'+category+'_13TeVDown' )
                    histos[ name ].Write()
                else :
                    histos[ name ].SetTitle( name.strip('_') )
                    histos[ name ].SetName( name.strip('_') )
                    histos[ name ].Write()
        shapeFile.Close()
    
    
        print "\n Output shapes file: %sShapes/%s/htt_%s.inputs-%s-13TeV%s.root \n" % (analysis, extra, nameChan, mid, append)
    
if __name__ == '__main__' :
    analysis = 'htt'
    samples = ['x',]   
    channels = ['tt',]
    folderDetails = '2Aug25x5pt45b_OSl1ml2_Tight_ZTT' 
    kwargs = {
    'useQCDMakeName' : '2Aug25x5pt45b_OSl1ml2_Tight_LooseZTT',
    'qcdSF' : 0.653408213966,
    'mssm' : False,
    'category' : 'inclusive',
    'fitShape' : 'm_vis',
    'ES' : True,
    }
    makeDataCards( analysis, samples, channels, folderDetails, **kwargs )
    





