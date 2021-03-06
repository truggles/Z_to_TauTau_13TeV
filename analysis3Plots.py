from util.buildTChain import makeTChain
import ROOT
import json
import pyplotter.plot_functions as pyplotter #import setTDRStyle, getCanvas
import pyplotter.tdrstyle as tdr
from util.ratioPlot import ratioPlot
import analysisPlots
from util.splitCanvas import fixFontSize
import os
from array import array
import math
from analysisPlots import skipSystShapeVar
from copy import deepcopy
from util.helpers import checkDir, unroll2D, returnSortedDict
import subprocess
from smart_getenv import getenv




def makeLotsOfPlots( analysis, samples, channels, folderDetails, **kwargs ) :

    ops = {
    'qcdMakeDM' : 'x',
    'useQCDMakeName' : 'x',
    'isSSQCD' : False,
    'addUncert' : True,
    'qcdMC' : False,
    'qcdSF' : 1.0,
    'ratio' : True,
    'blind' : True,
    'fullBlind' : False,
    'text' : False,
    'mssm' : False,
    'log' : False,
    'sync' : False,
    'redBkg' : False,
    'targetDir' : ''}

    '''python analysis3Plots.py --folder=2June26_OSl1ml2_VTight_ZTT --channel=tt --text=True --useQCDMake=True --useQCDMakeName=OSl1ml2_VTight_LooseZTT --qcdSF=0.147 --btag=False'''

    for key in kwargs :
        #print "another keyword arg: %s: %s" % (key, kwargs[key])
        if key in ops.keys() :
             ops[key] = kwargs[key]
    print ops

    # Use FF built QCD backgrounds
    doFF = getenv('doFF', type=bool)
    vv = ['WW1l1nu2q', 'WW2l2nu', 'WZ1l1nu2q', 'WZ1l3nu', 
         'WZ2l2q', 'WZ3l1nu', 'ZZ2l2nu', 'ZZ2l2q', 'ZZ4l', 
         'VV', 'WWW', 'ZZZ', 'T-tW', 'T-tchan', 'Tbar-tW', 'Tbar-tchan']

    """ Add in the gen matched DY catagorization """
    if analysis == 'htt' :
        genList = ['ZTT', 'ZLL', 'ZL', 'ZJ']
        dyJets = ['DYJetsAMCNLO', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow']

        newSamples = {}
        for sample in samples.keys() :
            #print sample
            if sample in dyJets :
                for gen in genList :
                    #print gen, sample+'-'+gen
                    samples[ sample+'-'+gen ] = deepcopy(samples[ sample ])
                    genApp = gen.lower()
                    samples[ sample+'-'+gen ]['group'] = genApp
            if sample == 'TT' :
                for gen in ['TTT', 'TTJ'] :
                    samples[ sample+'-'+gen ] = deepcopy(samples[ sample ])
                    genApp = 'ttbar'
                    samples[ sample+'-'+gen ]['group'] = genApp
            if sample in vv : 
                for gen in ['VVT', 'VVJ'] :
                    samples[ sample+'-'+gen ] = deepcopy(samples[ sample ])
                    genApp = 'dib'
                    samples[ sample+'-'+gen ]['group'] = genApp

        # Clean the samples list
        if analysis == 'htt' and 'TT' in samples.keys() :
            del samples[ 'TT' ]
        for dyJet in dyJets :
            if dyJet in samples.keys() :
                del samples[ dyJet ]
        for vvSamp in vv :
            if vvSamp in samples.keys() :
                del samples[ vvSamp ]
        if not doFF :
            samples[ 'QCD' ] = {'xsec' : 0.0, 'group' : 'qcd' }
                
    # Don't plot sm higgs 120, 130
    smMassesNoInclude = ['110', '120', '130', '140']
    smHiggs = []
    for mass in smMassesNoInclude :
        smHiggs.append('ggHtoTauTau%s' % mass)
        smHiggs.append('VBFHtoTauTau%s' % mass)
        smHiggs.append('WMinusHTauTau%s' % mass)
        smHiggs.append('WPlusHTauTau%s' % mass)
        smHiggs.append('ZHTauTau%s' % mass)
    for higgs in smHiggs :
        if higgs in samples : del samples[ higgs ]
    
    # Define which azh sample to keep
    azhMass = 300
    for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
        if mass != azhMass and 'azh'+str(mass) in samples : del samples[ 'azh'+str(mass) ]

    higgsSF = 1.0
    azhSF = .010
    azhSF = .020

    for sample in samples :
        print sample, samples[ sample ][ 'group' ]


    print "Running over %s samples" % analysis
    
    ROOT.gROOT.SetBatch(True)
    tdr.setTDRStyle()
    
    cmsLumi = float(os.getenv('LUMI'))/1000
    print "Lumi = %.1f / fb" % cmsLumi
    

    with open('meta/NtupleInputs_%s/samples.json' % analysis) as sampFile :
        sampDict = json.load( sampFile )
    
    chans = {
        'tt' : '#tau_{h}#tau_{h}',
        'em' : 'e#mu',
        'eeet' : 'eee#tau_{h}',
        'eemt' : 'ee#mu#tau_{h}',
        'eett' : 'ee#tau_{h}#tau_{h}',
        'eeem' : 'eee#mu',
        'eeee' : 'eeee',
        'eemm' : 'ee#mu#mu',
        'emmt' : '#mu#mue#tau_{h}',
        'mmmt' : '#mu#mu#mu#tau_{h}',
        'mmtt' : '#mu#mu#tau_{h}#tau_{h}',
        'emmm' : '#mu#mue#mu',
        'mmmm' : '#mu#mu#mu#mu',
        'ZEE' : 'Z#rightarrowee',
        'ZMM' : 'Z#rightarrow#mu#mu',
        'ZXX' : 'll+#tau#tau',
        'LLET' : "ll'e#tau_{h}",
        'LLMT' : "ll'#mu#tau_{h}",
        'LLTT' : "ll'#tau_{h}#tau_{h}",
        'LLEM' : "ll'e#mu",
    }
    
    
    sampInfo = { 'htt' : {
        'dib' : [ROOT.kRed+2, 'VV'],
        'ttbar' : [ROOT.kBlue-8, 't#bar{t}'],
        'qcd' : [ROOT.TColor.GetColor(250,202,255), 'QCD'], #kMagenta-10
        'ztt' : [ROOT.TColor.GetColor(248,206,104), 'Z#rightarrow#tau#tau'], #kOrange-4,
        'zl' : [ROOT.kAzure+2, 'Z#rightarrowee (lepton)'],
        'zj' : [ROOT.kGreen+2, 'Z#rightarrowee (jet)'],
        'zll' : [ROOT.TColor.GetColor(100,182,232), 'Z#rightarrowee'],
        'wjets' : [ROOT.kAzure+6, 'WJets'],
        'higgs' : [ROOT.kBlue, 'SM Higgs(125)'],
        'VH' : [ROOT.kGreen, 'SM VHiggs(125)'],
        'obs' : [ROOT.kBlack, 'Data'],
        }, # htt
            'azh' : {
        'obs' : [ROOT.kBlack, 'Data'],
        'zz' : [ROOT.kGreen-9, 'ZZ'],
        'ttZ' : [ROOT.kYellow-7, 'ttZ'],
        'wz' : [ROOT.kRed+1, 'WZ'],
        #'rare' : [ROOT.kOrange+7, 'Other'],
        'rare' : [ROOT.kYellow-7, 'Other'],
        'dyj' : [ROOT.TColor.GetColor(248,206,104), 'ZJets'],
        'top' : [ROOT.kBlue-8, 't#bar{t}'],
        'redBkg' : [ROOT.kCyan, 'Jet Fakes'],
        'higgs' : [ROOT.kRed-4, 'SM Higgs(125)'],
        'VH' : [ROOT.kGreen, 'SM VHiggs(125)'],
        'azh' : [ROOT.kBlue, 'A#rightarrowZh M%s #sigmaBR=%ifb' % (azhMass, int(azhSF*1000))],
        } # azh
    } # sampInfo
    if not ops['mssm'] : sampInfo['htt']['higgs'][1] = "SM Higgs(125) x %.1f" % higgsSF

    # Make signal variable for later easy mapping
    signal = ''
    if analysis == 'htt' : 
        signal = 'higgs'
        signalSF = higgsSF
    if analysis == 'azh' : 
        signal = 'azh'
        signalSF = azhSF
        #signal = 'VH'
        #signalSF = higgsSF
        #sampInfo['azh']['VH'][1] = "SM VHiggs(125) x %.1f" % higgsSF
    if doFF :
        sampInfo['htt']['jetFakes'] = [ROOT.TColor.GetColor(250,202,255), 'jetFakes'] #kMagenta-10
        del sampInfo['htt']['qcd']
    
    
    for channel in channels :
        print channel
    
        # Make an index file for web viewing
        checkDir( '/afs/cern.ch/user/t/truggles/www/%sPlots/%s%s/' % (analysis, channel, ops['targetDir']))
        checkDir( '/afs/cern.ch/user/t/truggles/www/%sPlotsList/%s%s/' % (analysis, channel, ops['targetDir']))
        subprocess.call(['cp','util/index.php', '/afs/cern.ch/user/t/truggles/www/%sPlots/%s%s/' % (analysis, channel, ops['targetDir'])])
        #htmlFile = open('/afs/cern.ch/user/t/truggles/www/%sPlots/%s%s/index.html' % (analysis, channel, ops['targetDir']), 'w')
        #htmlFile.write( '<html><head><STYLE type="text/css">img { border:0px; }</STYLE>\n' )
        #htmlFile.write( '<title>Channel %s/</title></head>\n' % channel )
        #htmlFile.write( '<body>\n' )
    

        newVarMapUnsorted = analysisPlots.getHistoDict( analysis, channel )
        newVarMap = returnSortedDict( newVarMapUnsorted )

        if doFF :
            tmpDict = {}
            for var, info in newVarMap.iteritems() :
                tmpDict[var] = info
                tmpDict[var+'_ffSub'] = list(info)
                tmpDict[var+'_ffSub'][4] += ' FF Sub'
            newVarMap = returnSortedDict( tmpDict )
    
        finalQCDYield = 0.0
        finalDataYield = 0.0
        qcdMake = False
        if ops['qcdMakeDM'] != 'x' :
            qcdMake = True
            finalQCDYield = 0.0
            finalDataYield = 0.0
            checkDir('meta/%sBackgrounds' % analysis)
            print "qcdMakeDM called: ",ops['qcdMakeDM']
            qcdMaker = ROOT.TFile('meta/%sBackgrounds/%s_qcdShape_%s_%s.root' % (analysis, channel, folderDetails.split('_')[0], ops['qcdMakeDM']), 'RECREATE')
            qcdDir = qcdMaker.mkdir('%s_Histos' % channel)
    
        #print newVarMap
        for var, info in newVarMap.iteritems() :
    
            # This is to speed up the Data Card making process by 2x and not
            # create all the plots for SS when all we need it the yield from m_visCor
            if ops['isSSQCD'] and not var == 'm_visCor' : continue

            # speed up 2D plotting
            if ":" in var or "AMassConst" in var :
                ## Skip 1 bin plot of 2D vars
                #if 'plotMe' in ops['qcdMakeDM'] : continue
                #elif 'vbf' in ops['qcdMakeDM'] :
                #    if not ('mjj' in var or 'vbfMass' in var) : continue
                #elif 'boosted' in ops['qcdMakeDM'] :
                #    if not ('pt_sv' in var or 'Higgs_Pt' in var) : continue
                #else : continue
                ### Skip plotting systematic shifts
                if 'Up' in var : continue
                if 'Down' in var : continue


            #if 'mt_sv' in var : continue
            print "Var:",var
    
    
            """
            Handle variable binning and longer ranges for visible mass
            """
            isVBFCat = False
            is1JetCat = False
            is0JetCat = False
            # This was useful for lower stats sub-divided categories pre-unrolling
            #if 'm_sv' in var or 'm_visCor' in var :
            #    if ('1jet_low' in ops['useQCDMakeName'] or '1jet_high' in ops['useQCDMakeName']\
            #            or '1jet_low' in ops['qcdMakeDM'] or '1jet_high' in ops['qcdMakeDM']) :
            #        is1JetCat = True
            #    if ('vbf' in ops['useQCDMakeName'] or 'vbf' in ops['qcdMakeDM']) :
            #        isVBFCat = True
            #    if not (isVBFCat or is1JetCat) : is0JetCat = True


            varBinned = True
            #if analysis == 'azh' and 'm_sv' in var and 'LT_higgs' in var and 'const_' not in var :
            #    xBins = array( 'd', [i for i in range( 0, 21 )] )
            #elif analysis == 'azh' and 'm_sv' in var and 'LT_higgs' not in var and 'const_' not in var :
            #    xBins = array( 'd', [i*20 for i in range( 1, 12 )] )
            #    #xBins = array( 'd', [0,30,60,90,120,150,180,210,240] )
            #else :
            varBinned = False
            first = info[1] * 1.
            last = info[2] * 1.
            totBins = ( info[0] / info[3] ) * 1.
            binWidth = (last - first)/totBins
            #print first, last, totBins, binWidth
            xBins = array('d', []) 
            for i in range( 0, int(totBins)+1 ) :
                if 'iso' in var :
                    xBins.append( round(i*binWidth+first,2) )
                else :
                    xBins.append( round(i*binWidth+first,1) )
            
            # Make a single bin version for QCD CR plots
            if 'plotMe' in ops['qcdMakeDM'] :
                xBins = array( 'd', [xBins[0], xBins[-1]] )

            xNum = len( xBins ) - 1

            # Set info values to evenly spaced xBins if not varBinned for ease later
            if varBinned :
                info[0] = xNum
                info[1] = xBins[0]
                info[2] = xBins[-1]
            #print "Binning scheme: ",xBins
            #print "Binning Summary"
            #print xBins, xNum
            #print info
            #print "VarBinned",varBinned
                
    
    
            append = var + channel
            stack = ROOT.THStack("All Backgrounds stack", "%s, %s" % (channel, var) )
            sampHistos = {}
            if ":" not in var :
                for samp in sampInfo[analysis].keys() :
                    # Skip some DY gen based combos
                    if analysis == 'htt' and channel == 'em' :
                        if samp in ['zl', 'zj'] : continue
                    if analysis == 'htt' and channel == 'tt' :
                        if samp == 'zll' : continue

                    sampHistos[samp] = ROOT.TH1D("All Backgrounds %s %s %s" % (samp, append, ops['targetDir'].strip('/')), samp, xNum, xBins )

                    sampHistos[samp].Sumw2()
                    sampHistos[samp].SetFillColor( sampInfo[analysis][samp][0] )
                    sampHistos[samp].SetLineColor( ROOT.kBlack )
                    sampHistos[samp].SetLineWidth( 2 )
                    sampHistos[samp].SetTitle( sampInfo[analysis][samp][1] )
                    sampHistos[samp].SetDirectory( 0 )
                #sampHistos[ signal ].SetLineColor( ROOT.kPink )
                #sampHistos[ signal ].SetLineColor( ROOT.kMagenta+2 )
                sampHistos[ signal ].SetLineColor( ROOT.kRed )
                sampHistos[ signal ].SetLineWidth( 6 )
                sampHistos[ signal ].SetLineStyle( 1 )
                sampHistos[ signal ].SetMarkerStyle( 0 )
            else :
                twoDVars = analysisPlots.get2DVars( var, channel )
                for samp in sampInfo[analysis].keys() :
                    # Skip some DY gen based combos
                    if analysis == 'htt' and channel == 'em' :
                        if samp in ['zl', 'zj'] : continue
                    if analysis == 'htt' and channel == 'tt' :
                        if samp == 'zll' : continue
                    # For ZH analysis we want TH1s unrolled, not 2D
                    #sampHistos[samp] = ROOT.TH2D("All Backgrounds %s %s %s" % (samp, append, ops['targetDir'].strip('/')),
                    #        samp, len(twoDVars[0])-1, twoDVars[0], len(twoDVars[1])-1, twoDVars[1] )
                    length = ( len(twoDVars[0]) - 1) * ( len(twoDVars[1]) - 1)
                    sampHistos[samp] = ROOT.TH1D("All Backgrounds %s %s %s" % (samp, append, ops['targetDir'].strip('/')),
                            samp, length, 0, length )
                    sampHistos[samp].Sumw2()
                    sampHistos[samp].SetFillColor( sampInfo[analysis][samp][0] )
                    sampHistos[samp].SetLineColor( ROOT.kBlack )
                    sampHistos[samp].SetLineWidth( 2 )
                    sampHistos[samp].SetTitle( sampInfo[analysis][samp][1] )
                    sampHistos[samp].SetDirectory( 0 )
                #sampHistos[ signal ].SetLineColor( ROOT.kMagenta+2 )
                sampHistos[ signal ].SetLineColor( ROOT.kRed )
                sampHistos[ signal ].SetLineWidth( 4 )
                sampHistos[ signal ].SetLineStyle( 7 )
                sampHistos[ signal ].SetMarkerStyle( 0 )
                
    
            redBkgYield = 0.0
            for sample in samples.keys() :
                #print sample
                #print samples[sample]
    
                ''' Shape systematics are plotted with their 
                    unshifted counterparts '''
                getVar = var
                if skipSystShapeVar( var, sample, channel ) :
                    breakUp = var.split('_')
                    if breakUp[-1] == 'ffSub' :
                        breakUp.pop()
                        breakUp.pop()
                    else : breakUp.pop()
                    getVar = '_'.join(breakUp)
    
                # Remember data samples are called 'dataEE' and 'dataMM'
                if channel in ['eeet', 'eemt', 'eett', 'eeem', 'eeee', 'eemm', 'ZEE'] and ('dataMM' in sample or 'dataSingleM' in sample) : continue
                if channel in ['emmt', 'mmmt', 'mmtt', 'emmm', 'mmmm', 'ZMM'] and ('dataEE' in sample or 'dataSingleE' in sample) : continue
            
                if channel == 'tt' and sample == 'dataEM' : continue
                if channel == 'tt' and '-ZLL' in sample : continue
                if channel == 'em' and sample == 'dataTT' : continue
                if channel == 'em' and '-ZJ' in sample : continue
                if channel == 'em' and '-ZL' in sample and not '-ZLL' in sample : continue
                if ops['qcdMC'] and sample == 'QCD' : continue
                #print sample
                #if not ops['qcdMC'] and 'QCD' in sample and '-' in sample : continue # Why was this line here? QCD pt binned MC???
    
                #if var == 'm_visCor' : print sample
                #print '%s2IsoOrderAndDups/%s_%s.root' % (analysis, sample, channel)
    
                if 'QCD' in sample :
                    #print "qcd in sample",sample
                    if doFF :
                        tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                    elif ops['useQCDMakeName'] != 'x'  :
                        fName = 'meta/%sBackgrounds/%s_qcdShape_%s_%s.root' % (analysis, channel, folderDetails.split('_')[0], ops['useQCDMakeName'])
                        #print fName 
                        tFile = ROOT.TFile(fName, 'READ')
                    elif ops['qcdMC'] :
                        print "Got QCD MC file", sample
                        tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                        print "QCD MC: %s Integral %f" % (sample, hxx.Integral() )
                    elif not ops['qcdMakeDM'] :
                        tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                    else :
                        continue
                elif ops['redBkg'] and 'RedBkgShape' in sample :
                    tFileYield = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample.replace('Shape','Yield'), channel), 'READ')
                    tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                    #tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample.replace('Shape','Yield'), channel), 'READ')
                else :
                    #print "File: '%s%s/%s_%s.root'" % (analysis, folderDetails, sample, channel)
                    tFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, folderDetails, sample, channel), 'READ')
                #print tFile
    
    
                dic = tFile.Get("%s_Histos" % channel )

                # Require var to be in file or print note and skip
                keys = dic.GetListOfKeys()
                inVars = [key.GetName() for key in keys]
                #    inVars.append( key.GetName() )
                if getVar not in inVars :
                    print "\n"+getVar+" not in your root files!  Skipping...\n"
                    continue



                ''' Special ZTT scaling for DYJets -> ZTT samples '''
                zttScaleTable = {
                    'inclusive' : 1.0,
                    'inclusiveSS' : 1.0,
                    '0jet' : 1.0,
                    '1jet' : 1.0,
                    '2jet' : 1.0,
                    '1jet_low' : 1.0,
                    '1jet_medium' : 1.0,
                    '1jet_high' : 1.0,
                    '2jet_vbf' : 1.2,
                    '1bjet' : 1.2,
                    '2bjet' : 1.4,
                }
                """ Do the Fake Factor MC - jet->tau fake MC here """
                if doFF :
                    # Do this based on the gen appended break down (and WJets)
                    if '-ZJ' in sample or '-TTJ' in sample or 'WJets' in sample or \
                            '-VVJ' in sample :
                        preHist = dic.Get( getVar )
                        if not '_ffSub' in getVar :
                            ffSubHist = dic.Get( getVar+'_ffSub' )
                            #print sample," FF Sub int",ffSubHist.Integral()
                            ffSubHist2 = ffSubHist.Rebin( xNum, "rebinned", xBins )
                            ffSubHist2.GetXaxis().SetRangeUser( info[1], info[2] )
                            #if "DYJets" in sample and "ZTT" in sample :
                            #    ffSubHist2.Scale( zttScaleTable[dirCode] )
                            sampHistos[ 'jetFakes' ].Add( ffSubHist2, -1.0 )
                            #print "FFSub Int ",sample,sampHistos[ 'jetFakes' ].Integral()
                    # QCD takes shape and yield from anti-isolated
                    # the +'_ffSub' is already appended to getVar
                    elif 'QCD' in sample :
                        if not '_ffSub' in getVar :
                            preHist = dic.Get( getVar+'_ffSub' )
                        else :
                            preHist = dic.Get( getVar )
                    # Data and all other MC treated normally
                    else :
                        preHist = dic.Get( getVar )
                else :
                    preHist = dic.Get( getVar )
                preHist.SetDirectory( 0 )

                #XXX if ops['redBkg'] and 'RedBkgShape' in sample :
                #XXX     redBkgYield = tFileYield.Get('%s_Histos/%s' % (channel, getVar)).Integral()
                #XXX     #print "REd BKG Yield:",redBkgYield
                #XXX     preHist.Sumw2()
                #XXX     if preHist.Integral() != 0 :
                #XXX         preHist.Scale( redBkgYield / preHist.Integral() )
                #XXX     #if ":" in var :
                #XXX     #    #histX = preHist.Rebin2D( 1, 1, "rebinned" )
                #XXX     #    hist = unroll2D( preHist, sample )
                #XXX     #else :
                #XXX     #    hist = ROOT.TH1D( preHist )
    
                if sample == 'QCD' and ops['useQCDMakeName'] != 'x' :
                    #print "Using QCD SCALE FACTOR <<<< NEW >>>>"
                    preHist.Scale( ops['qcdSF'] )
                    #print "QCD yield: %f" % preHist.Integral()
                    if not ":" in var :
                        histX = ROOT.TH1D( preHist )
                    else :
                        histX = ROOT.TH2D( preHist )
                else :
                    if ":" in var :
                        #histX = preHist.Rebin2D( 1, 1, "rebinned" )
                        histX = unroll2D( preHist, sample )
                        #print sample, histX.Integral()
                    else : 
                        histX = preHist.Rebin( xNum, "rebinned", xBins )

                # If plotting qcd CR, we want a single bin for all
                if 'plotMe' in ops['qcdMakeDM'] :
                    nBins = histX.GetNbinsX()
                    hist = histX.Rebin( nBins )
                else : hist = histX.Clone()
    
    
                if var == 'm_visCor' :
                    if 'data' in sample and qcdMake : finalDataYield = hist.Integral()
    
                ''' Good Debugging stuff '''
                #nBins = hist.GetNbinsX()
                #print "sample %s    # bins, %i   range %i %i" % (sample, nBins, hist.GetBinLowEdge( 1 ), hist.GetBinLowEdge( nBins+1 ))
    
    
                #print sample, samples[ sample ]['group']
                #print sampHistos[ samples[ sample ]['group'] ], hist
                #print "%s int: %.2f" % (sample, sampHistos[ samples[ sample ]['group'] ].Integral() )
                sampHistos[ samples[ sample ]['group'] ].Add( hist )
                #if samples[ sample ]['group'] == 'jetFakes' :
                #    print "jetFakes Stack yield: %f" % hist.Integral()
                #    print "%s int: %.2f" % (sample, sampHistos[ samples[ sample ]['group'] ].Integral() )

                if ops['redBkg'] and 'RedBkgShape' in sample :
                    redBkgYield += tFileYield.Get('%s_Histos/%s' % (channel, getVar)).Integral()

                tFile.Close()
    
            # With all RB added together, now do normalization
            if sampHistos['redBkg'].Integral() != 0 :
                sampHistos['redBkg'].Scale( redBkgYield / sampHistos['redBkg'].Integral() )
            
    

            ''' Change bin yield to make this make sense with variable binning
                this is only for viewing, the DC process is seperate '''
            # old print out for some sensitivity estimates
            #if 'id_e_mva_nt_' in var :
            #    print "xx---"
            #    print "xx---",channel,var
            #    for samp in sampHistos.keys() :
            #        if samp in ['dyj','top','wz'] : continue
            #        print "%s xx--- yield 0 bin %f" % ( samp, sampHistos[samp].GetBinContent(1) )
            #    for samp in sampHistos.keys() :
            #        if samp in ['dyj','top','wz'] : continue
            #        print "%s xx--- yield 1 bin %f" % ( samp, sampHistos[samp].GetBinContent(2) )

            for samp in sampHistos.keys() :
                if var == 'm_visCor' or var == 'A_Mass' or var == 'pt_1' :
                    err = ROOT.Double(0.)
                    sampHistos[samp].IntegralAndError( 1, sampHistos[samp].GetNbinsX(), err )
                    print "%s --- yield %.3f  %.3f" % ( samp, sampHistos[samp].Integral(), err )
            #    # With Variable binning, need to set bin content appropriately
            #    if not varBinned : continue
            #    if samp == "qcd" : continue
            #    minWidth = 999.
            #    for bin_ in range( 1, sampHistos[samp].GetNbinsX()+1 ) :
            #        minTmp = sampHistos[samp].GetBinWidth(bin_)
            #        if minTmp < minWidth : minWidth = minTmp
            #    for bin_ in range( 1, sampHistos[samp].GetNbinsX()+1 ) :
            #        sampHistos[samp].SetBinContent( bin_, sampHistos[samp].GetBinContent( bin_ ) * ( minWidth / sampHistos[samp].GetBinWidth( bin_ ) ) )
    
    
            # Some specific HTT stuff
            if analysis == 'htt' :
                if doFF :
                    stack.Add( sampHistos['jetFakes'] )
                elif not qcdMake :
                    #print "Adding QCD: ",sampHistos['qcd'].Integral()
                    stack.Add( sampHistos['qcd'] )
                stack.Add( sampHistos['ttbar'] )
                stack.Add( sampHistos['dib'] )
                stack.Add( sampHistos['wjets'] )
                if channel != 'em' :
                    stack.Add( sampHistos['zl'] )
                    stack.Add( sampHistos['zj'] )
                if channel == 'em' :
                    stack.Add( sampHistos['zll'] )
                stack.Add( sampHistos['ztt'] )

            # A to Zh stuff
            if analysis == 'azh' :
                if ops['redBkg'] :
                    stack.Add( sampHistos['redBkg'] )
                stack.Add( sampHistos['rare'] ) # TT, DYJets, WZ are all in rare now because only rarely do they both gen match true leptons
                #stack.Add( sampHistos['ttZ'] )
                stack.Add( sampHistos['zz'] )
                stack.Add( sampHistos['higgs'] )
    
            # Scale signal samples for viewing
            sampHistos[ signal ].Scale( signalSF )
    
            ''' Print out yields for a given distribution '''
            #sensitivityVars = ['Higgs_Pt', 'pt_1', 'pt_2', 'mjj', 'jdeta', 'pt_sv']
            ##if var == 'Higgs_Pt' or var == 'pt_1' or var == 'pt_2' :
            #if var in sensitivityVars :
            #    print "\n\nX "+var+" Stack yields"
            #    totBkgVar = 0.
            #    totSig = 0.
            #    top = stack.GetStack().Last().GetNbinsX()+1
            #    for bin in range( 1, top ) :
            #        binBkg = stack.GetStack().Last().GetBinContent( top-bin )
            #        binSig = sampHistos[signal].GetBinContent( top-bin )/higgsSF
            #        if binBkg > 0. :
            #            binSensitivity = binSig / math.sqrt( binBkg+binSig )
            #        else : binSensitivity = 0.

            #        totBkgVar += binBkg
            #        totSig += binSig
            #        if totBkgVar > 0. :
            #            sensitivity = totSig / math.sqrt( totBkgVar+totSig )
            #        else : sensitivity = 0.
            #        edge = stack.GetStack().Last().GetBinLowEdge( top-bin )
            #        #print "Bin: %i     sensitivity: %.2f     signal %.2f    bkg: %.2f" % (edge, sensitivity, totSig, totBkgVar)
            #        print "Bin: %.1f     sensitivity: %.2f     binSensitivity: %.2f" % (edge, sensitivity, binSensitivity)
    
            """
            Calculate rough bin-by-bin uncertainties
            """
            uncertNormMap = { 'htt' : {
                'qcd' : .20,
                'jetFakes' : .0,
                'ttbar' : .15,
                'dib' : .10,
                'wjets' : .10,
                'ztt' : .05,
                'zl' : .30,
                'zj' : .30,
                'higgs' : .0,
                'VH' : .2,
                'obs' : .0,},
            'azh' : {
                'top' : .10,
                'dyj' : .10,
                'wz' : .10,
                'rare' : .25,
                'zz' : .05,
                'ttZ' : .25,
                'redBkg' : .40,
                'azh' : .0,
                'higgs' : .1,
                'VH' : .0,
                'obs' : .0,}
            }
            if channel in ['eeem', 'emmm', 'LLEM'] :
                uncertNormMap['azh']['redBkg'] = 1.00
            if channel in ['eeet', 'emmt', 'LLET'] :
                uncertNormMap['azh']['redBkg'] = 0.50
            if channel in ['eemt', 'mmmt', 'LLMT'] :
                uncertNormMap['azh']['redBkg'] = 0.25
            if channel in ['eett', 'mmtt', 'LLTT'] :
                uncertNormMap['azh']['redBkg'] = 0.40
            binErrors = []
            for k in range( stack.GetStack().Last().GetNbinsX()+1 ) :
                toRoot = 0.
                for samp in sampHistos.keys() :
                    if samp in ['obs', 'azh', 'VH', 'higgs'] : continue
                    toAdd = (sampHistos[samp].GetBinContent(k)*\
                        uncertNormMap[analysis][samp])**2
                    toAdd += sampHistos[samp].GetBinError(k)**2
                    if toAdd > 0.0 : toRoot += toAdd
                    #toRoot += sampHistos[samp].GetBinError(k)**2

                binErrors.append( math.sqrt(toRoot) )
    
            if qcdMake :
                if not ":" in var :
                    qcdVar = ROOT.TH1D( var, 'qcd%s%s' % (append,var), xNum, xBins )
                else :
                    qcdVar = ROOT.TH2D( var, 'qcd%s%s' % (append,var), len(twoDVars[0])-1, twoDVars[0], len(twoDVars[1])-1, twoDVars[1] )
                qcdVar.Sumw2()
                qcdVar.Add( sampHistos['obs'], stack.GetStack().Last(), 1., -1. )
                qcdVar.SetFillColor( ROOT.kMagenta-10 )
                qcdVar.SetLineColor( ROOT.kBlack )
                qcdVar.SetLineWidth( 2 )
                # Add the shape estimated here to the stack pre-scaling!!!
                stack.Add( qcdVar ) 
                if var == 'm_visCor_mssm' :
                    print "M_VIS_MSSM plot details: %f %f" % (info[1], info[2])
                qcdVar.GetXaxis().SetRangeUser( info[1], info[2] )
                print "qcdVar: %f   mean %f" % (qcdVar.Integral(), qcdVar.GetMean() )
                if var == 'm_visCor' :
                    finalQCDYield = qcdVar.Integral()
                qcdDir.cd()
                qcdVar.Write()
    
    
            # Maybe make ratio hist
            c1 = ROOT.TCanvas("c1","Z -> #tau#tau, %s, %s" % (channel, var), 550, 550)
    
            if not ops['ratio'] :
                pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
                pad1.Draw()
                pad1.cd()
                stack.Draw('hist')
                if not 'plotMe' in ops['qcdMakeDM'] :
                    sampHistos[signal].Draw('same')
                sampHistos['obs'].Draw('esamex0')
                # X Axis!
                stack.GetXaxis().SetTitle("%s" % info[ 4 ])
    
            else : # Do Ratio plots
                smlPadSize = .25
                pads = ratioPlot( c1, 1-smlPadSize )
                pad1 = pads[0]
                ratioPad = pads[1]
                ratioPad.SetTopMargin(0.0)
                ratioPad.SetBottomMargin(0.3)
                pad1.SetBottomMargin(0.03)
                ratioPad.SetGridy()
                ratioHist = ROOT.TH1D('ratio %s' % append, 'ratio', xNum, xBins )
                ratioHist.Sumw2()
                ratioHist.Add( sampHistos['obs'] )
                ratioHist.Divide( stack.GetStack().Last() )
                ratioHist.SetMaximum( 2. )
                ratioHist.SetMinimum( 0. )
                if channel == 'tt' :
                    ratioHist.SetMaximum( 1.5 )
                    ratioHist.SetMinimum( 0.5 )
                ratioHist.SetMarkerStyle( 21 )
                ratioPad.cd()
                ratioHist.Draw('ex0')

                """ Add uncertainty bands on ratio """
                er = ROOT.TH1D("er %s" % append, "er", xNum, xBins )
                er.Sumw2()
                er.GetXaxis().SetRangeUser( info[1], info[2] )
                for k in range( er.GetNbinsX()+1 ) :
                    er.SetBinContent( k, 1. )
                    if stack.GetStack().Last().GetBinContent(k) > 0. : 
                        er.SetBinError(k, binErrors[k]/stack.GetStack().Last().GetBinContent(k) )
                    #print "Qcd Error:",qcd.GetBinError(k)
                er.SetLineColor( 0 )
                er.SetLineWidth( 0 )
                er.SetMarkerSize( 0 )
                er.SetFillStyle( 3001 )
                er.SetFillColor( 15 )
                er.Draw('same e2')
                ratioHist.Draw('esamex0')

                line = ROOT.TLine( info[1], 1, info[2], 1 )
                line.SetLineColor(ROOT.kBlack)
                line.SetLineWidth( 1 )
                line.Draw()
                ratioHist.Draw('esamex0')
                # X Axis!
                ratioHist.GetXaxis().SetTitle("%s" % info[ 4 ])
                ratioHist.GetYaxis().SetTitle("Data / MC")
                ratioHist.GetYaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( (1-smlPadSize)/smlPadSize) )
                ratioHist.GetYaxis().SetTitleOffset( smlPadSize*1.5 )
                ratioHist.GetYaxis().SetLabelSize( ratioHist.GetYaxis().GetLabelSize()*( 1/smlPadSize) )
                ratioHist.GetYaxis().SetNdivisions( 5, True )
                ratioHist.GetXaxis().SetLabelSize( ratioHist.GetXaxis().GetLabelSize()*( 1/smlPadSize) )
                ratioHist.GetXaxis().SetTitleSize( ratioHist.GetXaxis().GetTitleSize()*( 1/smlPadSize) )
    
    
                pad1.cd()
                stack.Draw('hist')
                stack.GetXaxis().SetLabelSize( 0.0 )
                stack.GetYaxis().SetLabelSize( stack.GetYaxis().GetLabelSize() / (1-smlPadSize) )
                if not 'plotMe' in ops['qcdMakeDM'] :
                    sampHistos[signal].SetFillStyle(0)
                    sampHistos[signal].Draw('hist same')
                sampHistos['obs'].Draw('esamex0')
    
    
            # Set labels appropriately
            if info[ 5 ] == '' :
                stack.GetYaxis().SetTitle("Events")
            elif not ":" in var :
                if varBinned :
                    stack.GetYaxis().SetTitle("Events / Bin Width")
                else :
                    width = stack.GetStack().Last().GetBinWidth(1)
                    stack.GetYaxis().SetTitle("Events / %.1f%s" % (width, info[ 5 ])  )
            else :
                stack.GetYaxis().SetTitle("Events / Bin Width")
    

            # Set axis and viewing area
            stackMax = stack.GetStack().Last().GetMaximum()
            dataMax = sampHistos['obs'].GetMaximum()
            stack.SetMaximum( max(dataMax, stackMax) * 1.5 )
            if ops['fullBlind'] :
                stack.SetMaximum( stackMax * 1.5 )
            if ops['targetDir'] == '/vbf_low' :
                stack.SetMaximum( max(dataMax, stackMax) * 1.8 )
            if ops['log'] :
                pad1.SetLogy()
                stack.SetMaximum( max(dataMax, stackMax) * 10 )
                stack.SetMinimum( min(dataMax, stackMax) * .005 )
    

            ''' Build the legend explicitly so we can specify marker styles '''
            legend = ROOT.TLegend(0.60, 0.55, 0.95, 0.93)
            legend.SetMargin(0.3)
            legend.SetBorderSize(0)
            legend.AddEntry( sampHistos['obs'], "Data", 'lep')
            if not 'plotMe' in ops['qcdMakeDM'] :
                legend.AddEntry( sampHistos[signal], sampHistos[signal].GetTitle(), 'l')
            for j in range(0, stack.GetStack().GetLast() + 1) :
                last = stack.GetStack().GetLast()
                name_str = stack.GetStack()[last - j ].GetTitle()
                if 'qcd' in name_str or 'QCD' in name_str : name_str = 'QCD'
                legend.AddEntry( stack.GetStack()[ last - j ], name_str, 'f')
            legend.Draw()
    

            # Set CMS Styles Stuff
            logo = ROOT.TText(.2, .87,"CMS Preliminary")
            logo.SetTextSize(0.05)
            logo.DrawTextNDC(.2, .87,"CMS Preliminary")
    
            chan = ROOT.TLatex(.2, .77,"x")
            chan.SetTextSize(0.07)
            #chan.DrawLatexNDC(.2, .84,"Channel: %s" % chans[channel] )
            chan.DrawLatexNDC(.2, .80,"%s" % chans[channel] )
    
            lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
            lumi.SetTextSize(0.05)
            lumi.DrawTextNDC(.7,.96,"%.1f / fb (13 TeV)" % cmsLumi )
    

            ''' Random print outs on plots '''
            if ops['text'] :# and not varBinned :
                text1 = ROOT.TText(.4,.6,"Data Integral: %f" % sampHistos['obs'].GetMean() )
                text1.SetTextSize(0.04)
                text1.DrawTextNDC(.6,.6,"Data Integral: %s" % str( round( sampHistos['obs'].Integral(), 1) ) )
                text2 = ROOT.TText(.4,.55,"Data Int: %s" % str( sampHistos['obs'].Integral() ) )
                text2.SetTextSize(0.04)
                text2.DrawTextNDC(.6,.55,"MC Integral: %s" % str( round( stack.GetStack().Last().Integral(), 1) ) )
                text3 = ROOT.TText(.4,.55,"Data Mean: %s" % str( sampHistos['obs'].GetMean() ) )
                text3.SetTextSize(0.04)
                text3.DrawTextNDC(.6,.50,"Diff: %s" % str( round( sampHistos['obs'].Integral() - stack.GetStack().Last().Integral(), 1) ) )
    
    
            pad1.Update()
            if ":" not in var :
                stack.GetXaxis().SetRangeUser( info[1], info[2] )
            if ops['ratio'] :
                ratioHist.GetXaxis().SetRangeUser( info[1], info[2] )
    
    
            """
            Add uncertainty bands on background stack
            """
            if ops['addUncert'] :
                e1 = ROOT.TH1D("e1 %s" % append, "e1", xNum, xBins )
                e1.Sumw2()
                e1.GetXaxis().SetRangeUser( info[1], info[2] )
                for k in range( e1.GetNbinsX()+1 ) :
                    e1.SetBinContent( k, stack.GetStack().Last().GetBinContent( k ) )
                    e1.SetBinError(k, binErrors[k] )
                    #print "Qcd Error:",qcd.GetBinError(k)
                e1.SetLineColor( 0 )
                e1.SetLineWidth( 0 )
                e1.SetMarkerSize( 0 )
                e1.SetFillStyle( 3001 )
                e1.SetFillColor( 15 )
                e1.Draw('same e2')
    
    
            """ Blinding Data """
            #if ops['blind'] and not 'plotMe' in ops['qcdMakeDM'] :
            #    if (analysis == 'htt' and ('m_visCor' in var or 'm_sv' in var or 'mt_sv' in var\
            #             or 'mt_tot' in var) ) : # or\
            #             #(analysis=='azh' and ('H_vis' in var or 'Mass' in var) ) :
            #        if ops['mssm'] :
            #            targetMass = 170
            #            targetMassUp = 9999
            #        elif analysis == 'htt' and 'm_sv' in var :
            #            targetMassLow = 101
            #            #if '1jet' in ops['targetDir'] : targetMassLow = 90
            #            #elif 'vbf' in ops['targetDir'] : targetMassLow = 100
            #            #elif 'vbf_low' in ops['targetDir'] : targetMassLow = 100
            #            #elif 'vbf_high' in ops['targetDir'] : targetMassLow = 80
            #            #else : targetMassLow = 80
            #            targetMassUp = 149
            #        elif analysis == 'htt' and 'm_visCor' in var :
            #            targetMassLow = 81
            #            targetMassUp = 149
            #        else :
            #            targetMassLow = 81
            #            targetMassUp = 149
            #        nBins = stack.GetStack().Last().GetXaxis().GetNbins()
            #        for k in range( 1, nBins+1 ) :
            #            binHigh = sampHistos['obs'].GetXaxis().GetBinLowEdge(k) + \
            #                    sampHistos['obs'].GetXaxis().GetBinWidth(k)
            #            binLow = sampHistos['obs'].GetXaxis().GetBinLowEdge(k)
            #            if binHigh>targetMassLow and binLow<=targetMassUp :
            #                sampHistos['obs'].SetBinContent(k, 0.)
            #                sampHistos['obs'].SetBinError(k, 0.)
            #                if ops['ratio'] and not ":" in var :
            #                    ratioHist.SetBinContent(k, 0.)
            #                    ratioHist.SetBinError(k, 0.)
            #    # Do official sensitivity blinding
            #    zhBlindVars = {
            #        'LT_higgs' : [71,999],
            #        'm_sv' : [101,149],
            #        'H_vis' : [61,109],
            #        'Mass' : [201,299],
            #        'A_Mass' : [201,299],
            #    }


            #    if analysis == 'azh' and var in zhBlindVars.keys() :
            #        #b_criteria = 1.
            #        targetMassLow = zhBlindVars[var][0]
            #        targetMassUp = zhBlindVars[var][1]
            #        nBins = stack.GetStack().Last().GetXaxis().GetNbins()
            #        for k in range( 1, nBins+1 ) :
            #            binHigh = sampHistos['obs'].GetXaxis().GetBinLowEdge(k) + \
            #                    sampHistos['obs'].GetXaxis().GetBinWidth(k)
            #            binLow = sampHistos['obs'].GetXaxis().GetBinLowEdge(k)
            #            if binHigh>targetMassLow and binLow<=targetMassUp :
            #            #b_tot = stack.GetStack().Last().GetBinContent(k)
            #            #if b_tot > 0.0 :
            #            #    criteria = ( (sampHistos[signal].GetBinContent(k)/signalSF) / \
            #            #            math.sqrt( b_tot + (0.1*b_tot)**2 ) )
            #            #    print "Bin ",k, "val: ", criteria
            #            #    if criteria >= b_criteria :
            #            #        print "Blinded!"
            #                sampHistos['obs'].SetBinContent(k, 0.)
            #                sampHistos['obs'].SetBinError(k, 0.)
            #                if ops['ratio'] and not ":" in var :
            #                    ratioHist.SetBinContent(k, 0.)
            #                    ratioHist.SetBinError(k, 0.)
            #    if ops['ratio'] and not ":" in var : 
            #        ratioPad.cd()
            #        ratioHist.Draw('esamex0')
            #    pad1.cd()

            inputThreshold = 0.1
            if ops['fullBlind'] :
                inputThreshold = 0.0
            if ops['blind'] and not 'plotMe' in ops['qcdMakeDM'] :
                blindEpsilon = 0.01
                if analysis == 'azh' :
                    if 'Mass' in var : inputThreshold = 0.0
                    nBins = stack.GetStack().Last().GetXaxis().GetNbins()
                    for k in range( 1, nBins+1 ) :
                        maxSig = sampHistos[ signal ].GetBinContent( k )
                        # Get Estimated bkg
                        totBkg = max(stack.GetStack().Last().GetBinContent( k ), 1.e-30)
                        # Check if we blind based on HTT 2016  twiki base 
                        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#Blinding
                        #print "bin: %s   maxSig: %s   tot bkg: %s     sensitivity: %s" % (k, maxSig, totBkg, maxSig / math.sqrt( totBkg + (blindEpsilon * totBkg)**2 ))
                        if ( inputThreshold <= ( maxSig / math.sqrt( totBkg + (blindEpsilon * totBkg)**2 ) ) ) or (var == 'LT_higgs' and k > 5) \
                                or (var == 'm_sv' and sampHistos[ signal ].GetBinCenter( k ) > 100 and sampHistos[ signal ].GetBinCenter( k ) < 160) :
                            sampHistos['obs'].SetBinContent(k, 0.)
                            sampHistos['obs'].SetBinError(k, 0.)
                            if ops['ratio'] :
                                ratioHist.SetBinContent(k, 0.)
                                ratioHist.SetBinError(k, 0.)
                    if ops['ratio'] and not ":" in var : 
                        ratioPad.cd()
                        ratioHist.Draw('esamex0')
                    pad1.cd()
                    sampHistos['obs'].Draw('esamex0')
            #if not ops['fullBlind'] :
            #    sampHistos['obs'].Draw('esamex0')
                    
            sampHistos['obs'].Draw('esamex0')
                
    
    
            if ops['qcdMakeDM'] == 'x' or 'plotMe' in ops['qcdMakeDM'] :
                plotDir = '/afs/cern.ch/user/t/truggles/www/%sPlots/%s%s/' % (analysis, channel, ops['targetDir'] )
                c1.SaveAs(plotDir+'%s.png' % var.replace(":","_") )
                c1.SaveAs(plotDir+'%s.pdf' % var.replace(":","_") )
                #c1.SaveAs(plotDir+'%s.root' % var )
                #c1.SaveAs(plotDir+'%s.C' % var )

                # To speed up, just copy the new png/pdfs to other dir
                # this will help with 2D plots
                newPlotDir = plotDir.replace('Plots/','PlotsList/')
                subprocess.call(['cp',plotDir+'%s.png' % var, newPlotDir+'%s.png' % var])
                subprocess.call(['cp',plotDir+'%s.pdf' % var, newPlotDir+'%s.pdf' % var])
                #subprocess.call(['cp',plotDir+'%s.root' % var, newPlotDir+'%s.root' % var])
                #subprocess.call(['cp',plotDir+'%s.C' % var, newPlotDir+'%s.C' % var])
    
    
            """ Additional views for Visible Mass """
            #if 'm_visCor' in var :
            #    pad1.SetLogy()
            #    stack.SetMaximum( stack.GetMaximum() * 10 )
            #    stack.SetMinimum( higgs.GetMaximum() * .1 )
            #    if var == 'm_visCor_mssm' :
            #        pad1.SetLogx()
            #        if ratio : ratioPad.SetLogx()
            #    pad1.Update()
            #    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlots/%s/%s_LogY.png' % (analysis, channel, var ) )
            #    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/%sPlotsList/%s/%s_LogY.png' % (analysis, channel, var ) )
            #    htmlFile.write( '<img src="%s_LogY.png">\n' % var )
            c1.Close()
    
            #htmlFile.write( '<img src="%s.png">\n' % var )
            #htmlFile.write( '<br>\n' )
        #htmlFile.write( '</body></html>' )
        #htmlFile.close()
    
        if qcdMake :
            print "\n\n Final QCD and Data Info:\n -- QCD Name: %s\n -- Data Yield = %f\n -- QCD Yield = %f" % (ops['qcdMakeDM'], finalDataYield, finalQCDYield)
            dumpFile = open('plotsOut.txt', 'a')
            dumpFile.write("\nFinal QCD and Data Info:\n -- QCD Name: %s\n -- Data Yield = %f\n -- QCD Yield = %f" % (ops['qcdMakeDM'], finalDataYield, finalQCDYield))
            dumpFile.close()


    return finalQCDYield



