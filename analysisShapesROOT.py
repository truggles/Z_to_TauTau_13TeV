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
from util.helpers import checkDir


def makeDataCards( analysis, samples, channels, folderDetails, **kwargs ) :

    ops = {
    'useQCDMakeName' : 'x',
    'qcdSF' : 1.0,
    'mssm' : False,
    'category' : 'inclusive',
    'fitShape' : 'm_vis',
    'btag' : False,
    'ES' : False,
    'tauPt' : False,
    'allShapes' : False,}

    for key in kwargs :
        #print "another keyword arg: %s: %s" % (key, kwargs[key])
        if key in ops.keys() :
             ops[key] = kwargs[key]

    print ops


    """ Add in the gen matched DY catagorization """
    # FIXME - do this later
    print "\n Samples currently hardcoded \n"
    #if analysis == 'htt' :
    #    genList = ['ZTT', 'ZLL', 'ZL', 'ZJ']
    #    dyJets = ['DYJetsAMCNLO', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4']
    #    newSamples = {}
    #    for sample in samples.keys() :
    #        #print sample
    #        if sample in dyJets :
    #            for gen in genList :
    #                #print gen, sample+'-'+gen
    #                samples[ sample+'-'+gen ] = deepcopy(samples[ sample ])
    #                genApp = gen.lower()
    #                samples[ sample+'-'+gen ]['group'] = genApp

    #    # Clean the samples list
    #    for dyJet in dyJets :
    #        if dyJet in samples.keys() :
    #            del samples[ dyJet ]
    #    samples[ 'QCD' ] = {'xsec' : 0.0, 'group' : 'qcd' }


    
    ROOT.gROOT.SetBatch(True)
    tdr.setTDRStyle()
    
    
    with open('meta/NtupleInputs_%s/samples.json' % analysis) as sampFile :
        sampDict = json.load( sampFile )
    
    samples = OrderedDict()
    samples['DYJets-ZTT']   = ('kOrange-4', '_ZTT_')
    samples['DYJets-ZL']   = ('kOrange-4', '_ZL_')
    samples['DYJets-ZJ']   = ('kOrange-4', '_ZJ_')
    samples['DYJets-ZLL']   = ('kOrange-4', '_ZLL_')
    #samples['DYJets1-ZTT']   = ('kOrange-4', '_ZTT_')
    #samples['DYJets1-ZL']   = ('kOrange-4', '_ZL_')
    #samples['DYJets1-ZJ']   = ('kOrange-4', '_ZJ_')
    #samples['DYJets1-ZLL']   = ('kOrange-4', '_ZLL_')
    #samples['DYJets2-ZTT']   = ('kOrange-4', '_ZTT_')
    #samples['DYJets2-ZL']   = ('kOrange-4', '_ZL_')
    #samples['DYJets2-ZJ']   = ('kOrange-4', '_ZJ_')
    #samples['DYJets2-ZLL']   = ('kOrange-4', '_ZLL_')
    #samples['DYJets3-ZTT']   = ('kOrange-4', '_ZTT_')
    #samples['DYJets3-ZL']   = ('kOrange-4', '_ZL_')
    #samples['DYJets3-ZJ']   = ('kOrange-4', '_ZJ_')
    #samples['DYJets3-ZLL']   = ('kOrange-4', '_ZLL_')
    #samples['DYJets4-ZTT']   = ('kOrange-4', '_ZTT_')
    #samples['DYJets4-ZL']   = ('kOrange-4', '_ZL_')
    #samples['DYJets4-ZJ']   = ('kOrange-4', '_ZJ_')
    #samples['DYJets4-ZLL']   = ('kOrange-4', '_ZLL_')
    #samples['DYJetsLow-ZTT']   = ('kOrange-4', '_ZTT_')
    #samples['DYJetsLow-ZL']   = ('kOrange-4', '_ZL_')
    #samples['DYJetsLow-ZJ']   = ('kOrange-4', '_ZJ_')
    #samples['DYJetsLow-ZLL']   = ('kOrange-4', '_ZLL_')
    samples['T-tW']     = ('kYellow+2', '_VV_')
    samples['T-tchan']     = ('kYellow+2', '_VV_')
    samples['TT']       = ('kBlue-8', '_TT_')
    samples['Tbar-tW']  = ('kYellow-2', '_VV_')
    samples['Tbar-tchan']  = ('kYellow-2', '_VV_')
    #samples['WJets']    = ('kAzure+2', '_W_')
    #samples['WJets1']    = ('kAzure+2', '_W_')
    #samples['WJets2']    = ('kAzure+2', '_W_')
    #samples['WJets3']    = ('kAzure+2', '_W_')
    #samples['WJets4']    = ('kAzure+2', '_W_')
    samples['WW1l1nu2q']     = ('kAzure+4', '_VV_')
    #samples['WW2l2nu']       = ('kAzure+8', '_VV_')
    samples['WZ1l1nu2q'] = ('kAzure-6', '_VV_')
    samples['WZ1l3nu'] = ('kAzure-6', '_VV_')
    samples['WZ2l2q'] = ('kAzure-6', '_VV_')
    #samples['WZ3l1nu'] = ('kAzure-6', '_VV_')
    #samples['ZZ2l2nu'] = ('kAzure-12', '_VV_')
    samples['ZZ2l2q'] = ('kAzure-12', '_VV_')
    #samples['ZZ4l'] = ('kAzure-12', '_VV_')
    samples['VV'] = ('kAzure-12', '_VV_')
    samples['QCD']        = ('kMagenta-10', '_QCD_')
    samples['dataTT']  = ('kBlack', '_data_obs_')
    samples['dataEM']  = ('kBlack', '_data_obs_')
    samples['VBFHtoTauTau120'] = ('kGreen', '_vbf120_')
    samples['VBFHtoTauTau125'] = ('kGreen', '_vbf125_')
    samples['VBFHtoTauTau130'] = ('kGreen', '_vbf130_')
    samples['ggHtoTauTau120'] = ('kGreen', '_ggH120_')
    samples['ggHtoTauTau125'] = ('kGreen', '_ggH125_')
    samples['ggHtoTauTau130'] = ('kGreen', '_ggH130_')
    
    nameArray = ['_data_obs_','_ZTT_','_ZL_','_ZJ_','_ZLL_','_TT_','_QCD_','_VV_','_W_','_ggH120_','_ggH125_','_ggH130_','_vbf120_','_vbf125_','_vbf130_']
    
    if ops['mssm'] : # FIXME - make sure SM Higgs 120 and 130 don't overlap?
        masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
        for mssmMass in masses :
            samples['ggH%i' % mssmMass] = ('kPink', '_ggH%i_' % mssmMass)
            samples['bbH%i' % mssmMass] = ('kPink', '_bbH%i_' % mssmMass) 
            nameArray.append('_ggH%i_' % mssmMass)
            nameArray.append('_bbH%i_' % mssmMass)
    
    
    extra = ''
    checkDir( '%sShapes' % analysis )
    if ops['mssm'] : 
        checkDir( '%sShapes/mssm' % analysis )
        extra = 'mssm'
    else : 
        checkDir( '%sShapes/htt' % analysis )
        extra = 'htt'
    
    for channel in channels :
    
        if channel == 'tt' :
            for sample in samples.keys() :
                if '-ZLL' in sample :
                    del samples[ sample ]
            nameArray.remove('_ZLL_')
        if channel == 'em' :
            for sample in samples.keys() :
                if sample[-3:] == '-ZL' or '-ZJ' in sample :
                    del samples[ sample ]
            nameArray.remove('_ZJ_')
            nameArray.remove('_ZL_')
    
        print channel
    
        newVarMap = analysisPlots.getHistoDict( analysis, channel )
    
        baseVar = ops['fitShape']
        if 'data' in sample : print "Fitting",baseVar
        if 'm_vis' in baseVar :
            append = ''
        elif 'm_sv' in baseVar :
            append = '_svFit'
        elif 'mt_sv' in baseVar :
            append = '_MtsvFit'
        elif 'mt_tot' in baseVar :
            append = '_MtTot'
    
        if ops['mssm'] :
        #    if not var == baseVar+'_mssm' : continue
            mid = 'mssm'
        else :
            mid = 'sm'
    
        shapeFile = ROOT.TFile('%sShapes/%s/htt_%s.inputs-%s-13TeV%s.root' % (analysis, extra, channel, mid, append), 'UPDATE')
        shapeDir = shapeFile.mkdir( channel + '_%s' % ops['category'] )
        print shapeDir
    
        for var in newVarMap.keys() :
    
            if not baseVar in var : continue
            if ops['allShapes'] :
                if not (('_energyScale' in var) or ('_tauPt' in var)  or ('_zPt' in var) or ('_topPt' in var) or (baseVar == var)) :
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
            print "Var: ",var
    
            #if not ops['sync'] :
            #    binArray = array( 'd', [0,20,40,60,80,100,150,200,250,350,600] )
            #if ops['mssm'] and not ops['btag'] :
            print "MSSM btag option:",ops['btag']
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

            else :
                binArray = array( 'd', [] )
                for i in range( 36 ) :
                    binArray.append( i * 10 )
                #binArray.append( 600 )
            print binArray
            numBins = len( binArray ) - 1
            histos = {}
            for name in nameArray :
                title = name.strip('_')
                if ops['ES'] or ops['tauPt'] :
                    if '_energyScaleUp' in var :
                        histos[ name ] = ROOT.TH1D( name+'energyScaleUp', name+'energyScaleUp', numBins, binArray )
                    elif '_energyScaleDown' in var :
                        histos[ name ] = ROOT.TH1D( name+'energyScaleDown', name+'energyScaleDown', numBins, binArray )
                    elif '_tauPtUp' in var :
                        histos[ name ] = ROOT.TH1D( name+'tauPtUp', name+'tauPtUp', numBins, binArray )
                    elif '_tauPtDown' in var :
                        histos[ name ] = ROOT.TH1D( name+'tauPtDown', name+'tauPtDown', numBins, binArray )
                    elif '_zPtUp' in var :
                        histos[ name ] = ROOT.TH1D( name+'zPtUp', name+'zPtUp', numBins, binArray )
                    elif '_zPtDown' in var :
                        histos[ name ] = ROOT.TH1D( name+'zPtDown', name+'zPtDown', numBins, binArray )
                    elif '_topPtUp' in var :
                        histos[ name ] = ROOT.TH1D( name+'topPtUp', name+'topPtUp', numBins, binArray )
                    elif '_topPtDown' in var :
                        histos[ name ] = ROOT.TH1D( name+'topPtDown', name+'topPtDown', numBins, binArray )
                    else :
                        histos[ name ] = ROOT.TH1D( name, name, numBins, binArray )
                histos[ name ].Sumw2()
    
    
            for sample in samples:
    
                ''' Skip plotting unused shape systematics '''
                if skipSystShapeVar( var, sample, channel ) : continue
                if '_topPt' in var : print "Top Pt still in Var: "+var+" sample: "+sample
    
                if channel == 'tt' and sample == 'dataEM' : continue
                if channel == 'em' and sample == 'dataTT' : continue
                #if sample == 'DYJetsLow' : continue
                #if 'HtoTauTau' in sample : continue
                #print sample
    
                if sample == 'dataEM' :
                    tFile = ROOT.TFile('%s%s/%s_em.root' % (analysis, folderDetails, sample), 'READ')
                elif sample == 'dataTT' :
                    tFile = ROOT.TFile('%s%s/%s_tt.root' % (analysis, folderDetails, sample), 'READ')
                elif sample == 'QCD' :
                    if ops['useQCDMakeName'] != 'x'  :
                        print "Use QCD MAKE NAME: ",ops['useQCDMakeName']
                        tFile = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s.root' % (analysis, channel, ops['useQCDMakeName']), 'READ')
                    else :
                        print " \n\n ### SPECIFY A QCD SHAPE !!! ### \n\n"
                else :
                    tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
    
    
                dic = tFile.Get("%s_Histos" % channel )
                hist = dic.Get( "%s" % var )
                hist.SetDirectory( 0 )
                #print "Hist yield before scaling ",hist.Integral()
    
    
    
                ''' Scale Histo based on cross section ( 1000 is for 1 fb^-1 of data ),
                QCD gets special scaling from bkg estimation, see qcdYield[channel] above for details '''
                #print "PRE Sample: %s      Int: %f" % (sample, hist.Integral() )
                if sample == 'QCD' and ops['useQCDMakeName'] != 'x' :
                    print "Using QCD SCALE FACTOR <<<< NEW >>>>"
                    qcdScale = ops['qcdSF']
                    print "Skip rebin; Scale QCD shape by %f" % qcdScale
                    print "QCD yield Pre: %f" % hist.Integral()
                    hist.Scale( qcdScale )
                    print "QCD yield Post Scale: %f" % hist.Integral()
    
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
    
                if ops['mssm'] and not 'ggH' in sample and not 'bbH' in sample :
                    print "SampleName: %s   Hist yield %f" % (sample, hist.Integral())
                else :
                    print "SampleName: %s   Hist yield %f" % (sample, hist.Integral())
                #hist2 = hist.Rebin( 18, 'rebinned', binArray )
                #histos[ samples[ sample ][1] ].Add( hist2 )
                tFile.Close()
    
    
            shapeDir.cd()
            for name in histos :
                #print "name: %s Yield Pre: %f" % (name, histos[ name ].Integral() )
                # Make sure we have no negative bins
                #for bin_ in range( 1, histos[ name ].GetXaxis().GetNbins()+1 ) :
                #    setVal = 0.0
                #    if histos[ name ].GetBinContent( bin_ ) < 0 :
                #        histos[ name ].SetBinContent( bin_, setVal )
                #        print "name: %s   Set bin %i to value: %f" % (name, bin_, setVal)
                if not 'ggH' in name and not 'bbH' in name :
                    print "name: %s Yield Post: %f" % (name, histos[ name ].Integral() )
                if not ops['mssm'] :
                    histos[ name ].GetXaxis().SetRangeUser( 0, 350 )
    
                # Proper naming of output histos
                #if (ops['allShapes']) and ('_energyScale' in var or '_tauPt' in var or '_zPt' in var or '_topPt' in var) :
                if (ops['ES']) and ('_energyScale' in var or '_tauPt' in var or '_zPt' in var or '_topPt' in var) :
                    if name in ['_data_obs_','_QCD_','_VV_','_W_'] : continue 
                    lep = 'x'
                    if channel == 'tt' : lep = 't'
                    if channel == 'em' : lep = 'e'
    
                    if '_topPt' in var :
                        if name == '_TT_' :
                            if '_topPtUp' in var :
                                histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_ttbarShape_13TeVUp' )
                                histos[ name ].SetName( name.strip('_')+'_CMS_htt_ttbarShape_13TeVUp' )
                            elif '_topPtDown' in var :
                                histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_ttbarShape_13TeVDown' )
                                histos[ name ].SetName( name.strip('_')+'_CMS_htt_ttbarShape_13TeVDown' )
                        else : continue
                    elif name == '_TT_' : continue # this is to catch TT when it's not wanted
                    elif '_energyScaleUp' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_'+lep+'_'+channel+'_13TeVUp' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_'+lep+'_'+channel+'_13TeVUp' )
                    elif '_energyScaleDown' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_scale_'+lep+'_'+channel+'_13TeVDown' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_scale_'+lep+'_'+channel+'_13TeVDown' )
                    elif '_tauPtUp' in var :
                        hisos[ name ].SetTitle( name.strip('_')+'_CMS_eff_t_mssmHigh_'+channel+'_13TeVUp' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_eff_t_mssmHigh_'+channel+'_13TeVUp' )
                    elif '_tauPtDown' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_eff_t_mssmHigh_'+channel+'_13TeVDown' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_eff_t_mssmHigh_'+channel+'_13TeVDown' )
                    elif '_zPtUp' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_dyShape_13TeVUp' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_htt_dyShape_13TeVUp' )
                    elif '_zPtDown' in var :
                        histos[ name ].SetTitle( name.strip('_')+'_CMS_htt_dyShape_13TeVDown' )
                        histos[ name ].SetName( name.strip('_')+'_CMS_htt_dyShape_13TeVDown' )
                    histos[ name ].Write()
                else :
                    histos[ name ].SetTitle( name.strip('_') )
                    histos[ name ].SetName( name.strip('_') )
                    histos[ name ].Write()
        shapeFile.Close()
    
    
        print "\n Output shapes file: %sShapes/%s/htt_%s.inputs-%s-13TeV%s.root \n" % (analysis, extra, channel, mid, append)
    
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
    





