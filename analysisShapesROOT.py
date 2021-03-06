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
from util.helpers import checkDir, unroll2D, returnSortedDict, \
        dataCardGenMatchedSamples
from analysis1BaselineCuts import skipChanDataCombo
import os
from smart_getenv import getenv
from math import sqrt


def makeDataCards( analysis, inSamples, channels, folderDetails, **kwargs ) :
    assert( type(inSamples) == type(OrderedDict())
        or type(inSamples) == type({}) ), "Provide a samples list which \
        is a dict or OrderedDict"

    # Get expanded list of samples with gen appended names
    samples = dataCardGenMatchedSamples( analysis, inSamples )
    #for key in samples :
    #    print key, samples[key]

    ops = {
    'useQCDMakeName' : 'x',
    'qcdSF' : 1.0,
    'mssm' : False,
    'doZH' : False,
    'category' : 'inclusive',
    'fitShape' : 'm_visCor',
    'sync' : False,
    'redBkg' : False,
    'allShapes' : False,}

    for key in kwargs :
        #print "another keyword arg: %s: %s" % (key, kwargs[key])
        if key in ops.keys() :
             ops[key] = kwargs[key]

    print ops

    ROOT.gROOT.SetBatch(True)
    tdr.setTDRStyle()
    
    
    with open('meta/NtupleInputs_%s/samples.json' % analysis) as sampFile :
        sampDict = json.load( sampFile )
    

    # Change or alter samples based on flags
    if analysis == 'azh' :
        eras =  []
        for s in samples :
            if 'dataMM' in s : eras.append( s.split('-').pop() )
        for era in eras :
            samples['RedBkgShapeSingleLep-%s' % era] = 'allFakes'
            samples['RedBkgShapeDoubleLep-%s' % era] = 'allFakes'
        if ops['doZH'] : # then remove AZH samples
            for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
                if 'azh%i' % mass in samples : del samples['azh%i' % mass]
        #if not ops['doZH'] : # then removed 110 120 130 140 mass points for SM Higgs
        #    for mass in ['110', '120', '130', '140'] :
        #        if 'ZHTauTau%s' % mass in samples : del samples['ZHTauTau%s' % mass]
        #        if 'WHTauTau%s' % mass in samples : del samples['WHTauTau%s' % mass]


    # Use FF built QCD backgrounds
    doFF = getenv('doFF', type=bool)
    # value saved to renormalize the FF shape uncertainties
    jetFakesNomYield = -999.
    if doFF :
        eras =  []
        for s in samples :
            if 'dataTT' in s : eras.append( s.split('-').pop() )
        if 'QCD' in samples.keys() :
            del samples['QCD']
        for era in eras :
            samples['QCD-%s' % era] = 'jetFakes'

    
    # Build list of names/samples which will be used
    # for a given final channel. This differs for some HTT
    # channels
    nameArray = []
    for samp in samples :
        if samples[samp] not in nameArray : nameArray.append( samples[samp] )


    # the shape names are changed to reflect the fact that they have the
    # jet -> tau fakes removed
    if doFF :
        ffRenameMap = {
            'W' : 'W_rest',
            'ZJ' : 'ZJ_rest',
            'TTJ' : 'TTJ_rest',
            'VVJ' : 'VVJ_rest'
        }
        for samp, val in samples.iteritems() :
            if val in ffRenameMap.keys() :
                print "Val in ffRenameMap", val
                samples[samp] = ffRenameMap[ val ]
                if val in nameArray :
                    nameArray.remove( val )
                    nameArray.append( ffRenameMap[ val ] )


    print "Samples to use and their mapping"
    for key in samples :
        print key, samples[key]


    extra = ''
    if ops['mssm'] : 
        extra = 'mssm'
    elif ops['doZH'] :
        extra = 'zh'
    elif analysis == 'azh' : # and not doZH
        extra = 'azh'
    else : 
        extra = 'htt'
    checkDir( 'shapes/%s' % analysis )
    
    for channel in channels :

        # not sure why the ZH conglomerates are still here
        if channel in ['ZEE', 'ZMM', 'ZXX', 'LLET', 'LLMT', 'LLTT', 'LLEM'] : continue
    
        if channel == 'tt' :
            for sample in samples.keys() :
                if '-ZLL' in sample :
                    del samples[ sample ]
            if 'ZLL' in nameArray : nameArray.remove('ZLL')
        #if channel == 'em' :
        #    for sample in samples.keys() :
        #        if sample[-3:] == '-ZL' or '-ZJ' in sample :
        #            del samples[ sample ]
        #    if 'ZJ' in nameArray : nameArray.remove('ZJ')
        #    if 'ZL' in nameArray : nameArray.remove('ZL')


        print "Name Array"
        print nameArray    
        print channel
    
        newVarMapUnsorted = analysisPlots.getHistoDict( analysis, channel )
        newVarMap = returnSortedDict( newVarMapUnsorted )
    
        baseVar = ops['fitShape']
        #if 'data' in sample : print "Fitting",baseVar
        appendMap = {
            'm_sv' : 'svFitMass2D',
            'pt_sv:m_sv' : 'svFitMass2D',
            'mjj:m_sv' : 'svFitMass2D',
            'm_visCor' : 'visMass2D',
            'Higgs_PtCor:m_sv' : 'svFitMass2D',
            'Higgs_PtCor:m_visCor' : 'visMass2D',
            'mjj:m_visCor' : 'visMass2D',
            'AMassConst' : 'AMassConst',
            'Mass' : '4LMass',
            'A_Mass' : 'AMass',
            'm_vis' : 'VisMass',
            'H_vis' : 'HVisMass',
            'LT_higgs:m_sv' : 'svFitMass',
            }
        if analysis == 'azh' : appendMap['m_sv'] = 'svFitMass'
        #if '0jet2D' in ops['category'] : 
        #    if ops['fitShape'] == 'm_sv' :
        #        Append = '_svFitMass2D'
        #    else :
        #        Append = '_visMass2D'
        #else :
        #    Append = '_'+appendMap[baseVar]
        Append = '_'+appendMap[baseVar]
    
        if ops['mssm'] or not ops['doZH'] :
            mid = 'mssm'
        else :
            mid = 'sm'
        if 'svFitMass' in Append : mid = 'sm'
    
        nameChan = 'tt' if analysis != 'azh' else 'zh'
        shapeFileName = 'shapes/%s/htt_%s.inputs-%s-13TeV%s.root' % (analysis, nameChan, mid, Append)
        shapeFile = ROOT.TFile(shapeFileName, 'UPDATE')
        # We have two pathways to create tt_0jet and need to maintain their seperate root files for 1D vs 2D
        # so we need this override that renames 0jet2D -> 0jet and places in the unrolled root file
        if '0jet2D' in ops['category'] : 
            cr = '_qcd_cr' if '_qcd_cr' in ops['category'] else ''
            shapeDir = shapeFile.mkdir( channel + '_0jet'+cr, channel + '_0jet'+cr )
        else :
            shapeDir = shapeFile.mkdir( channel + '_%s' % ops['category'], channel + '_%s' % ops['category'] )
        assert( shapeDir != None ), "It looks like the directory already exists, remove the old root file and start again: rm %s" % shapeFileName
    
        for var in newVarMap.keys() :
    
            print var
            if not baseVar in var : continue
            if ops['fitShape'] == 'm_sv' and ':' in var : continue # Get rid of the 2D shapes in 0jet
            if ops['fitShape'] == 'm_visCor' and ':' in var : continue # Get rid of the 2D shapes in 0jet
            print "\n\n=============================================================="
            if ops['allShapes'] :
                print "All Shapes Applied: %s" % var
                if doFF :
                    if not (('_energyScale' in var) or ('_zPt' in var) or \
                            ('ffSyst' in var) or ('ffStat' in var) or ('_topPt' in var) or \
                            ('_metUnclustered' in var) or ('_metClustered' in var) \
                            or ('_JES' in var) or ('_JetToTau' in var) or \
                            ('_Zmumu' in var) or ('_ggH' in var) \
                            or ('_ffSub' in var) or (baseVar == var)) :
                        continue

                else :
                    if not (('_energyScale' in var) or ('_zPt' in var) or ('_topPt' in var) \
                        or ('_JES' in var) or ('_ggH' in var) or ('_JetToTau' in var) \
                        or ('_metUnclustered' in var) or ('_metClustered' in var) \
                        or ('_Zmumu' in var) or ('_tauPt' in var) or ('_promptMC' in var) \
                        or (baseVar == var)) :
                        print "Did we fail?"
                        continue
            else :
                if not var == baseVar : continue
    
    
            # Defined out here for large scope
            print "\nVar: ",var
    
            binArray = array( 'd', [] )
            if ops['sync'] :
                binArray = array( 'd', [i*20 for i in range( 11 )] )
            # This is the proposed binning for ZTT 2015 paper
            elif doFF and ('m_sv' in var or 'm_visCor' in var) :
                if ":" in var : binArray = array( 'd', [i for i in range( 49 )] )
                else : binArray = array( 'd', [i*10 for i in range( 31 )] )
            elif analysis == 'azh' and ops['doZH'] and ":" not in var :
                binArray = array( 'd', [i*20 for i in range( 1, 12 )] )
            elif analysis == 'azh' and ops['doZH'] and ":" in var :
                binArray = array( 'd', [i for i in range( 21 )] )
            elif analysis == 'azh' and var == 'm_vis' :
                binArray = array( 'd', [i*20 for i in range( 21 )] )
            elif analysis == 'azh' : # For 4lMass and A_Mass
                binArray = array( 'd', [i*20 for i in range( 31 )] )
            else :
                if ":" in var : 
                    binArray = array( 'd', [i for i in range( 49 )] )
                elif ops['category'] in ['1jet_low', '1jet_high'] :
                    binArray = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
                elif 'vbf' in ops['category'] :
                    binArray = array( 'd', [0,40,60,80,100,120,150,200,250] )
                else :
                    #binArray = array( 'd', [i*10 for i in range( 31 )] )
                    binArray = array( 'd', [0,50,60,70,80,90,100,110,120,130,\
                        140,150,160,170,180,190,200,210,220,230,240,250,\
                        260,270,280,290,300] )
            numBins = len( binArray ) - 1
            #print binArray
            #print numBins

            histos = OrderedDict()
            for name in nameArray :
                title = name
                if ops['allShapes'] :

                    if '_' in var and ('Up' in var or 'Down' in var) :
                        systName = var.split('_')[-1]
                        histos[ name ] = ROOT.TH1D( name+systName, name+systName, numBins, binArray )
                    else :
                        histos[ name ] = ROOT.TH1D( name, name, numBins, binArray )
                else :
                    histos[ name ] = ROOT.TH1D( name, name, numBins, binArray )
                histos[ name ].Sumw2()
    
    
            redBkgYield = 0.0
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
                elif 'QCD' in sample :
                    if ops['useQCDMakeName'] != 'x'  :
                        print "Use QCD MAKE NAME: ",ops['useQCDMakeName']
                        tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s.root' % (analysis, channel, ops['useQCDMakeName']), 'READ')
                    elif doFF :
                        tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                        #print " \n### Using Fake Factor QCD Shape !!! ###\n"
                    else :
                        print " \n\n ### SPECIFY A QCD SHAPE !!! ### \n\n"
                elif ops['redBkg'] and 'RedBkgShape' in sample :
                    tFileYield = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample.replace('Shape','Yield'), channel), 'READ')
                    tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                    #tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample.replace('Shape','Yield'), channel), 'READ')
                else :
                    tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
    
    
                dic = tFile.Get("%s_Histos" % channel )
                if not doFF :
                    hist = dic.Get( "%s" % var )
                if doFF :
                    if 'QCD' in sample :
                        hist = dic.Get( "%s_ffSub" % var )
                    else :
                        hist = dic.Get( "%s" % var )
                        # This is where we subtract off the fakes from MC from jetFakes
                        if '-ZJ' in sample or '-TTJ' in sample or 'WJets' in sample or '-VVJ' in sample :
                            if not '_ffSub' in var :
                                ffSubHist = dic.Get( var+'_ffSub' )
                                #print sample," FF Sub int",ffSubHist.Integral()
                                if ":" in var :
                                    ffSubHist2 = unroll2D( ffSubHist )
                                else :
                                    ffSubHist2 = ffSubHist.Rebin( numBins, "rebinned", binArray )
                                ffSubHist2.GetXaxis().SetRangeUser( binArray[0], binArray[-1] )
                                #if "DYJets" in sample and "ZTT" in sample :
                                #    ffSubHist2.Scale( zttScaleTable[ops['category']] )
                                histos[ 'jetFakes' ].Add( ffSubHist2, -1.0 )
                hist.SetDirectory( 0 )
                #print "Hist yield before scaling ",hist.Integral()
    

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
                    #print binArray
                else :
                    hNew = hist.Rebin( numBins, "new%s" % sample, binArray )

                """ Scale reducible bkg shape by yield estimate """
                if ops['redBkg'] and 'RedBkgShape' in sample :
                    hNew.Sumw2()
                    redBkgYield += tFileYield.Get('%s_Histos/%s' % (channel, var)).Integral()
                    #XXX if hNew.Integral() != 0 :
                    #XXX     hNew.Scale( redBkgYield / hNew.Integral() )

                # If using the qcd CR, we want a single bin for all
                if '_qcd_cr' in ops['category'] :
                    nBins = hNew.GetNbinsX()
                    hNew.Rebin( nBins )
                    # If histos haven't been Rebinned, do it
                    nBinsHistos = histos[ samples[ sample ] ].GetNbinsX()
                    if nBins == nBinsHistos :
                        histos[ samples[ sample ] ].Rebin( nBins )

                # Before adding, make sure to remove RedBkgYield histos
                # in case it was forgotten earlier
                if ops['redBkg'] and 'RedBkgYield' in sample : continue

                # Add samples to final histos
                histos[ samples[ sample ] ].Add( hNew )
    
                #XXX LOTS OF PRINT OUTS if ops['mssm'] and not 'ggH' in sample and not 'bbH' in sample :
                #XXX LOTS OF PRINT OUTS     print "SampleName: %20s   Hist yield %.2f" % (sample, hist.Integral())
                #XXX LOTS OF PRINT OUTS else :
                #XXX LOTS OF PRINT OUTS     print "SampleName: %20s   Hist yield %.2f" % (sample, hist.Integral())
                #hist2 = hist.Rebin( 18, 'rebinned', binArray )
                #histos[ samples[ sample ] ].Add( hist2 )
                tFile.Close()

            # With all RB added together, now do normalization
            if histos[ 'allFakes' ].Integral() != 0 :
                histos[ 'allFakes' ].Scale( redBkgYield / histos[ 'allFakes' ].Integral() )
    
            # All files looped through, now renormalize jetFakes
            # background if doing Fake Factor method
            if doFF :
                if var == baseVar :
                    jetFakesNomYield = histos[ 'jetFakes' ].Integral()
                    print " -- FF Normalization: var == basevar %s %s yield: %.2f" % (baseVar,var,jetFakesNomYield)
                elif ('ffSyst' in var or 'ffStat' in var) :
                    assert( jetFakesNomYield > 0. ), "Why didn't you loop over the base variable yet?"
                    preYield = histos[ 'jetFakes' ].Integral()
                    histos[ 'jetFakes' ].Scale( jetFakesNomYield / preYield )
                    postYield = histos[ 'jetFakes' ].Integral()
                    print " -- FF Normalization: var is a ff shape: %s %s pre: %.2f post: %.2f" % (baseVar,var,preYield,postYield)

    
            print ".............................................................."
            shapeDir.cd()


            # We need to check for any total bkg bins which have 0
            # Recall ROOT TH1 bin numbers start at 1 for the useful bins
            # Don't worry about this in QCD CR
            setVal = 0.00001
            if not '_qcd_cr' in ops['category'] : 
                #dataArray = []
                bkgArray = [0] * numBins
                for name in histos :
                    if 'ggH' in name or 'qqH' in name or 'ZH' in name or 'WH' in name or 'azh' in name :
                        continue # we don't care about signal here
                    elif name == 'data_obs' : continue # can use this later if need be
                    #    for bin_id in range( histos[ name ].GetNbinsX() ) :
                    #        dataArray.append( histos[ name ].GetBinContent( bin_id+1 ) )
                    else : # All backgrounds
                        for bin_id in range( histos[ name ].GetNbinsX() ) :
                            bkgArray[bin_id] = bkgArray[bin_id] + histos[ name ].GetBinContent( bin_id+1 )


                if ('Up' not in var and 'Down' not in var) or 'promptMC' in var : # promptMC for allFake shape uncert
                    print "\n --- Bkg Yields By Bin: ",channel,var
                    # Choose data_obs because it should always be here
                    for bin_id in range( histos[ 'data_obs' ].GetNbinsX() ) :
                        print "  --- %i %3.4f" % ( bin_id+1, bkgArray[bin_id] )
                    #print dataArray
                    #print bkgArray
                    #assert( len(dataArray) == len(bkgArray) ), "Zero bin check is not working, are you missing data_obs?"

                    # Find problem bins
                    # ZH / AZh analysis has well populated background templates, skip this portion
                    problemBins = []
                    print "Checking for problem bins"
                    sampToCheck = ''
                    if analysis == 'azh' : sampToCheck = 'allFakes'
                    if analysis == 'htt' : sampToCheck = 'QCD'

                    for bin_id in range( len(bkgArray) ) :
                        #if dataArray[bin_id] > 0. and bkgArray[bin_id] == 0. :
                        print bin_id+1, bkgArray[bin_id], " QCD/allFakes val: ",histos[ sampToCheck ].GetBinContent( bin_id+1 )
                        if bkgArray[bin_id] == 0. :
                            problemBins.append( bin_id+1 ) # +1 here gets us to ROOT coords

                    nEntries = histos[ sampToCheck ].GetEntries()
                    assert (nEntries > 0), "\nFailing to make a DC because you have no irreducible bkg"
                    integral = histos[ sampToCheck ].Integral()
                    avgW = integral/nEntries
                    print "Simple method uncer on zero bin method - avg allFakes entry #entries %i, weight: %3.4f" % (nEntries, avgW)
                    print problemBins
                    """ To reduce confusion with 2D unrolled, I am taking a yield slightly larger
                        than the average for RedBkg, 0.01 as the uncertainty to apply for empty
                        bins. This was updated Aug 8, 2018 based on EETT weights """
                    avgW = 0.01

                    # Apply correction and set an empyt bin to QCD = 1e-5
                    if sampToCheck in histos.keys() :
                        #for problemBin in problemBins :
                        #    print "Setting QCD bin_id %i to %s" % (problemBin, setVal)
                        #    histos[ sampToCheck ].SetBinContent( problemBin, setVal )
                        #    # Poissonian error for 0
                        #    histos[ sampToCheck ].SetBinError( problemBin, avgW*1.8 )
                        for bin_id in range( 1, histos[ 'data_obs' ].GetNbinsX()+1 ) :
                            if histos[ sampToCheck ].GetBinContent( bin_id ) <= 0.0 :
                                print "Setting allFakes bin_id %i to %s" % (bin_id, setVal)
                                histos[ sampToCheck ].SetBinContent( bin_id, setVal )
                                # Poissonian error for 0
                                histos[ sampToCheck ].SetBinError( bin_id, avgW*1.8 )
                    elif len(problemBins) > 0 : 
                        print "\nQCD Bkg not included so zero bins are not being corrected properly"
                        print problemBins
                        print "\n\n\n"


                # Check QCD 
                #for bin_id in range( 1, histos[ 'QCD' ].GetNbinsX()+1 ) :
                #    print bin_id, histos[ 'QCD' ].GetBinContent( bin_id )


            for name in histos :
                #print "name: %s Yield Pre: %f" % (name, histos[ name ].Integral() )
                # First, if we are doing Fake Factor and jetFakes is negative
                # zero it
                if histos[ name ].Integral() < 0.0 and name == 'jetFakes' :
                    for bin_ in range( 1, histos[ name ].GetXaxis().GetNbins()+1 ) :
                        histos[ name ].SetBinContent( bin_, setVal )
                # Make sure we have no negative bins
                for bin_ in range( 1, histos[ name ].GetXaxis().GetNbins()+1 ) :
                    if name == 'QCD' : # Set all QCD 0.0 and negative vals to 1e-5
                        if histos[ name ].GetBinContent( bin_ ) == 0. :
                            histos[ name ].SetBinContent( bin_, setVal )
                            # Poissonian error for 0
                            histos[ name ].SetBinError( bin_, 1.8 )
                            print "name: %s   Set bin %i to value: %s" % (name, bin_, setVal)
                        elif histos[ name ].GetBinContent( bin_ ) < 0. :
                            # Don't change the uncertainty on the bin
                            # it was set by the negative content, leave it as is
                            histos[ name ].SetBinContent( bin_, setVal )
                            print "name: %s   Set bin %i to value: %s" % (name, bin_, setVal)
                    if histos[ name ].GetBinContent( bin_ ) < 0 :
                        # Don't change the uncertainty on the bin
                        # it was set by the negative content, leave it as is
                        histos[ name ].SetBinContent( bin_, setVal )
                        print "name: %s   Set bin %i to value: %f" % (name, bin_, setVal)
                if histos[ name ].Integral() != 0.0 :
                    print "DataCard Name: %10s Yield Post: %.2f" % (name, histos[ name ].Integral() )
                #else :
                #    print "DataCard Name: %10s Yield Post: %.2f" % (name, histos[ name ].Integral() )
                #if not ops['mssm'] :
                #    histos[ name ].GetXaxis().SetRangeUser( 0, 350 )

                # Scale AZh to 1 fb cross section, it is set at 1 pb in meta
                if analysis == 'azh' and not ops['doZH'] and 'azh' in name :
                    histos[ name ].Scale( 1. / 1000. )


                # There is additional ZEE scaling for EES in EEET, EEMT, EETT, EEEM channels
                if '_energyScaleEES' in var :
                    if name != 'data_obs' and 'allFakes' not in name :
                        if channel in ['eeee','eeet','eemt','eett','eeem'] :
                            #print "    ----    EES - %20s pre yield: %3.3f" % (name, histos[ name ].Integral() )
                            if var[-2:] == 'Up' : histos[ name ].Scale( 1.006 )
                            if var[-4:] == 'Down' : histos[ name ].Scale( 1./1.006 )
                            #print "    ----    EES - %20s post yield: %3.3f" % (name, histos[ name ].Integral() )
                            
                
    
                # Proper naming of output histos
                if ops['allShapes'] and ('_energyScale' in var or '_tauPt' in var or '_zPt' in var \
                        or '_JES' in var or '_topPt' in var or '_ggH' in var or '_JetToTau' in var or '_Zmumu' in var \
                        or '_metUnclustered' in var or '_metClustered' in var or '_promptMC' in var \
                        or 'ffSyst' in var or 'ffStat' in var) :

                    # Systematics naming removes CRs
                    category = ops['category'].strip('_qcd_cr')

                    if name in ['data_obs','QCD'] : continue 
                    if name == 'jetFakes' and not doFF : continue
                    if name == 'jetFakes' and not ('ffSyst' in var or 'ffStat' in var) : continue
                    if ('ffSyst' in var or 'ffStat' in var) and name != 'jetFakes' : continue
                    if '_ggH' in var and not name in ['ggH110', 'ggH120','ggH125','ggH130', 'ggH140'] : continue
                    if '_JetToTau' in var and not name in ['W', 'TTJ', 'ZJ', 'VVJ',
                            'VVJ_rest', 'W_rest', 'TTJ_rest', 'ZJ_rest'] : continue
                    if '_Zmumu' in var and (name not in ['ZTT', 'ZL', 'ZJ', 'ZJ_rest', 'EWKZ'] or \
                            category != 'vbf') : continue # Shape only used in vbf category atm
                    if 'allFakes' in name and not '_promptMC' in var : continue
                    if '_promptMC' in var and not 'allFakes' in name : continue
                    lep = 'x'
                    if channel == 'tt' : lep = 't'
                    if channel == 'em' : lep = 'e'

                    shiftDir = ''
                    shiftVar = var.replace('_ffStat','').replace('_ffSyst','')
                    #print "shiftVar1:",shiftVar
                    if shiftVar[-2:] == 'Up' : shiftDir = 'Up'
                    if shiftVar[-4:] == 'Down' : shiftDir = 'Down'
                    assert( shiftDir == 'Up' or shiftDir == 'Down' ), "Is var a +/- shift? %s" % var

                    # JES Breakdown
                    if '_JES' in var :
                        jesUnc = var.split('_')[-1]
                        jesUnc = jesUnc.replace('JES', '')
                        if 'Up' in jesUnc[-2:] : jesUnc = jesUnc[:-2]
                        if 'Down' in jesUnc[-4:] : jesUnc = jesUnc[:-4]

                        if jesUnc == '' : jesUnc = '13TeV'+shiftDir
                        # Keep a normal shift included for checks at Combine level
                        elif 'Total' in jesUnc and 'Sub' not in jesUnc : jesUnc = '13TeV'+shiftDir
                        else : jesUnc += '_13TeV'+shiftDir

                    # For naming conventions for systematics    
                    if category == 'vbf' : tmpCat = 'VBF'
                    else : tmpCat = category

                    if '_zPt' in var :
                        if name not in ['ZTT','ZL','ZJ','ZLL','ZJ_rest'] : continue
                        elif '_zPt' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_dyShape_13TeV'+shiftDir )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_dyShape_13TeV'+shiftDir )
                    elif '_topPt' in var :
                        if name not in ['TTT','TTJ','TTJ_rest'] : continue
                        elif '_topPt' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_ttbarShape_13TeV'+shiftDir )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_ttbarShape_13TeV'+shiftDir )
                    #elif name in ['TTT','TTJ'] : continue # this is to catch TT when it's not wanted
                    elif '_energyScaleAll' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_t_'+channel+'_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_t_'+channel+'_13TeV'+shiftDir )
                        altName = histos[ name ].Clone( name.strip('_')+'_CMS_scale_t_13TeV'+shiftDir )
                        altName.SetTitle( name.strip('_')+'_CMS_scale_t_13TeV'+shiftDir )
                        altName.Write()
                        del altName
                    elif '_energyScaleDM0' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_t_1prong_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_t_1prong_13TeV'+shiftDir )
                    elif '_energyScaleDM10' in var : # Gotta do this one first to elif DM10 and DM1
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_t_3prong_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_t_3prong_13TeV'+shiftDir )
                    elif '_energyScaleDM1' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_t_1prong1pizero_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_t_1prong1pizero_13TeV'+shiftDir )
                    elif '_energyScaleEES' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_e_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_e_13TeV'+shiftDir )
                    elif '_JES' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_j_'+jesUnc )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_j_'+jesUnc )
                    elif '_JetToTau' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_jetToTauFake_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_htt_jetToTauFake_13TeV'+shiftDir )
                    elif '_tauPt' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_eff_t_High_'+channel+'_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_eff_t_High_'+channel+'_13TeV'+shiftDir )
                    elif '_ggH' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_gg_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_gg_13TeV'+shiftDir )
                    elif '_Zmumu' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_zmumuShape_'+tmpCat+'_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_htt_zmumuShape_'+tmpCat+'_13TeV'+shiftDir )
                    elif '_metClustered' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_met_clustered_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_met_clustered_13TeV'+shiftDir )
                    elif '_metUnclustered' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_met_unclustered_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_met_unclustered_13TeV'+shiftDir )
                    elif '_promptMCElecMu' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_fake_rate_prompt_MC_EandM_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_fake_rate_prompt_MC_EandM_13TeV'+shiftDir )
                    elif '_promptMCTau' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_fake_rate_prompt_MC_Tau_13TeV'+shiftDir )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_fake_rate_prompt_MC_Tau_13TeV'+shiftDir )
                    ### For these Fake Factor shapes, we need 2 copies with slightly different names
                    elif 'ffSyst' in var :
                        if 'qcdffSyst' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_norm_ff_qcd_tt_syst_13TeV'+shiftDir )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_norm_ff_qcd_tt_syst_13TeV'+shiftDir )
                        elif 'ttbarffSyst' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_norm_ff_ttbar_tt_syst_13TeV'+shiftDir )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_norm_ff_ttbar_tt_syst_13TeV'+shiftDir )
                        elif 'wjetsffSyst' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_norm_ff_w_tt_syst_13TeV'+shiftDir )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_norm_ff_w_tt_syst_13TeV'+shiftDir )
                        else : assert (2 + 2 == 5), "This shouldn't happen.  Problem in your FF shapes."
                    elif 'ffStat' in var :
                        if '0jet1prongffStat' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_norm_ff_qcd_1prong_njet0_tt_stat_13TeV'+shiftDir )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_norm_ff_qcd_1prong_njet0_tt_stat_13TeV'+shiftDir )
                        elif '0jet3prongffStat' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_norm_ff_qcd_3prong_njet0_tt_stat_13TeV'+shiftDir )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_norm_ff_qcd_3prong_njet0_tt_stat_13TeV'+shiftDir )
                        elif '1jet1prongffStat' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_norm_ff_qcd_1prong_njet1_tt_stat_13TeV'+shiftDir )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_norm_ff_qcd_1prong_njet1_tt_stat_13TeV'+shiftDir )
                        elif '1jet3prongffStat' in var :
                            histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_norm_ff_qcd_3prong_njet1_tt_stat_13TeV'+shiftDir )
                            histos[ name ].SetName( name.strip('_')+'_CMS_htt_norm_ff_qcd_3prong_njet1_tt_stat_13TeV'+shiftDir )
                        else : assert (2 + 2 == 5), "This shouldn't happen.  Problem in your FF shapes."
                    histos[ name ].Write()
                else :
                    histos[ name ].SetTitle( name.strip('_') )
                    histos[ name ].SetName( name.strip('_') )
                    histos[ name ].Write()
        shapeFile.Close()
    
    
        print "\n Output shapes file: ", shapeFileName 
    




