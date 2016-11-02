import ROOT
from ROOT import gPad
from array import array



# Make a histo, but fill it later so we can keep track of events for ALL histos at once
def makeHisto( cutName, varBins, varMin, varMax ) :
    hist = ROOT.TH1D( cutName, cutName, varBins, varMin, varMax )
    return hist



# Make a 2D histo
def get2DVars( cutName ) :
    if 'pt_sv:m_sv' in cutName :
        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,100,170,300,5000] )
    if 'mjj:m_sv' in cutName :
        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,300,500,800,5000] )
    if 'pt_1:m_sv' in cutName :
        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,60,100,5000] )
    return (xBins, yBins)


# Make a 2D histo
def make2DHisto( cutName ) :
    info = get2DVars( cutName )
    xBins = info[0]
    yBins = info[1]
    hist = ROOT.TH2D( cutName, cutName, len(xBins)-1, xBins, len(yBins)-1, yBins )
    return hist


def skipSystShapeVar( var, sample, channel ) :
        # Tau Pt Scale reweighting only applied to DYJets and signal
        if '_tauPt' in var :
            if channel == 'em' : return True
            if not ('ggH' in sample or 'bbH' in sample or 'DYJets' in sample or 'VBF' in sample) :
                return True
            
        # Energy Scale reweighting only applied to DYJets and signal
        elif '_energyScale' in var :
            if not ('ggH' in sample or 'bbH' in sample or 'DYJets' in sample or 'VBF' in sample) :
                return True

        # z pt reweight only applied to LO DYJets samples, DYJetsLow in amc@nlo
        # do run for DYJetsLow as weight is set to 1
        elif '_zPt' in var :
            if 'DYJets' not in sample : return True

        # top pt reweighting only applied to ttbar
        elif '_topPt' in var :
            if 'TT' not in sample : return True
            elif 'data' in sample :return True
            elif 'DYJets' in sample : return True

        # Jet Energy Scale, no data
        elif '_JES' in var :
            if 'data' in sample : return True
        return False


# Make specific extra cuts for different TES requirements
def ESCuts( sample, channel, var ) :
    tau2PtCut = 40.
    tau1PtCut = 50.
    if len( channel ) == 4 : return '*(1)'
    if 'data' in sample :
        if channel == 'tt' :
            return '*(pt_1 > %s && pt_2 > %s)' % (tau1PtCut, tau2PtCut)
        if channel == 'em' :
            return '*(pt_1 > 13 && pt_2 > 10)'
    ESMap = {
        'tt' : { 
            '_energyScaleUp' : '*( pt_1_UP > %s && pt_2_UP > %s)' % (tau1PtCut, tau2PtCut),
            '_energyScaleDown' : '*( pt_1_DOWN > %s && pt_2_DOWN > %s)' % (tau1PtCut, tau2PtCut),
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s)' % (tau1PtCut, tau2PtCut)},
        'em' : { 
            '_energyScaleUp' : '*((pt_1*1.03) > 13 && pt_2 > 10)',
            '_energyScaleDown' : '*((pt_1*0.97) > 13 && pt_2 > 10)',
            '_NoShift' : '*(pt_1 > 13 && pt_2 > 10)'}
        }
    if '_energyScaleUp' in var : return ESMap[ channel ]['_energyScaleUp']
    elif '_energyScaleDown' in var : return ESMap[ channel ]['_energyScaleDown']
    else : return ESMap[ channel ]['_NoShift']



# Specific high pt tau reweighting for shape uncertainties
def HighPtTauWeight( var ) :
    if not '_tauPt' in var: return ''
    # see analysis2 for how tauPtWeight is calculated
    elif '_tauPtUp' in var : return '*(tauPtWeightUp)'
    elif '_tauPtDown' in var : return '*(tauPtWeightDown)'
    else : return ''



# Plot histos using TTree::Draw which works very well with Proof
def plotHistosProof( analysis, outFile, chain, sample, channel, isData, additionalCut, blind=False, skipSSQCDDetails=False ) :
    ''' Make a channel specific selection of desired histos and fill them '''
    newVarMap = getHistoDict( analysis, channel )

    histosDir = outFile.mkdir( "%s_Histos" % channel )
    histosDir.cd()
    ''' Combine Gen and Chan specific into one fill section '''
    histos = {}
    for var, info in newVarMap.iteritems() :
        if skipSSQCDDetails and not (var == 'eta_1' or var == 'm_vis')  : continue
        print var


        ''' Skip plotting unused shape systematics '''
        if skipSystShapeVar( var, sample, channel ) : continue

        ''' Define syst shape weights if applicable '''
        shapeSyst = ''
        # High Pt tau reweighting only applied to DYJets and signal
        if '_tauPt' in var :
            shapeSyst = HighPtTauWeight( var )

        # top pt reweighting only applied to ttbar
        elif '_topPt' in var :
            if '_topPtUp' in var : shapeSyst = '*(topWeight)'
            elif '_topPtDown' in var : shapeSyst = '*(1./topWeight)'

        # z pt reweight only applied to LO DYJets samples, DYJetsLow in amc@nlo
        elif '_zPt' in var :
            if '_zPtUp' in var : shapeSyst = '*(zPtWeight)'
            elif '_zPtDown' in var : shapeSyst = '*(1./zPtWeight)'
            
        # Energy Scale reweighting applied to all Real Hadronic Taus
        # gen_match == 5
        # this is not an "if" style shape b/c we need to apply
        # normal pt cuts if the shape syst is not called
        # so instead we appeand it to what ever else we have
        shapeSyst += ESCuts( sample, channel, var )
        # Additionally, if we have Energy Scale, we also need
        # to change any Higgs_Pt vars to Higgs_Pt_UP/DOWN
        additionalCutToUse = additionalCut
        if 'energyScale' in var and 'data' not in sample :
            if 'Up' in var and 'pt_sv' in additionalCutToUse :
                additionalCutToUse = additionalCutToUse.replace('pt_sv','pt_sv_UP')
            elif 'Down' in var and 'pt_sv' in additionalCutToUse :
                additionalCutToUse = additionalCutToUse.replace('pt_sv','pt_sv_DOWN')


        # Jet Energy Scale:
        # similar as TES above, edit the additionalCut
        # so that njets is replaced by njets_JESUP
        # make because we unroll in mjj, edit that
        # as well when it's in the plotVar for 2D
        # plotVar is changed below with this happens for other shifts
        if 'JES' in var and 'data' not in sample :
            if 'Up' in var :
                additionalCutToUse = additionalCutToUse.replace('jetVeto30','jetVeto30_JetEnUp')
                # We changed naming to simple mjj, njetingap20 and jdeta for sync for nominal
                additionalCutToUse = additionalCutToUse.replace('mjj','vbfMass_JetEnUp')
                additionalCutToUse = additionalCutToUse.replace('njetingap20','vbfJetVeto20_JetEnUp')
                additionalCutToUse = additionalCutToUse.replace('jdeta','vbfDeta_JetEnUp')
                #print additionalCutToUse+"\n"
            if 'Down' in var :
                additionalCutToUse = additionalCutToUse.replace('jetVeto30','jetVeto30_JetEnDown')
                additionalCutToUse = additionalCutToUse.replace('mjj','vbfMass_JetEnDown')
                additionalCutToUse = additionalCutToUse.replace('njetingap20','vbfJetVeto20_JetEnDown')
                additionalCutToUse = additionalCutToUse.replace('jdeta','vbfDeta_JetEnDown')
                #print additionalCutToUse+"\n"
                


        if ":" in var :
    	    histos[ var ] = make2DHisto( var )
        else :
    	    histos[ var ] = makeHisto( var, info[0], info[1], info[2])

        # Adding Trigger, ID and Iso, & Efficiency Scale Factors
        # and, top pt reweighting
        # weight is a composition of all applied MC/Data corrections
        sfs = '*(1)'
        if analysis == 'htt' :
            sfs = '*(weight)'
            if channel == 'tt' :
                # Not currently included in weight for sync ntuple
                sfs += '*(tauIDweight_1 * tauIDweight_2)'
        if analysis == 'azh' :
            sfs = '*(puweight*azhWeight)' 
        xsec = '*(XSecLumiWeight)'

        #print "%s     High Pt Tau Weight: %s" % (var, tauW)
        #print var,shapeSyst
        totalCutAndWeightMC = '(GenWeight/abs( GenWeight ))%s%s%s%s' % (additionalCutToUse, sfs, xsec, shapeSyst) 
        #print totalCutAndWeightMC


        # Check if the variable to plot is in the chain, if not, skip it
        # don't crash on systematics based variables
        varBase = var.replace('_ffSub','')
        plotVar = var.replace('_ffSub','') # remove the histo naming off the back of the plotting var
        if 'Up' in var or 'Down' in var :
            tmp = varBase.split('_')
            shapeName = tmp.pop()
            varBase = '_'.join(tmp)
            if 'energyScale' in shapeName :
                if 'pt_sv:m_sv' in var :
                    if 'Up' in var : plotVar = 'pt_sv_UP:m_sv_UP'
                    if 'Down' in var : plotVar = 'pt_sv_DOWN:m_sv_DOWN'
                elif 'Up' in var :
                    plotVar = varBase + '_UP'
                elif 'Down' in var :
                    plotVar = varBase + '_DOWN'
            elif 'metResolution' in shapeName :
                if 'Up' in var :
                    plotVar = varBase + '_ResolutionUP'
                if 'Down' in var :
                    plotVar = varBase + '_ResolutionDOWN'
            elif 'metResponse' in shapeName :
                if 'Up' in var :
                    plotVar = varBase + '_ResponseUP'
                if 'Down' in var :
                    plotVar = varBase + '_ResponseDOWN'
            elif 'JES' in shapeName :
                if 'mjj:m_sv' in var :
                    if 'Up' in var :
                        plotVar = 'vbfMass_JetEnUp:m_sv'
                    if 'Down' in var :
                        plotVar = 'vbfMass_JetEnDown:m_sv'
                else : # For this one, we adjust the additionalCuts to 
                    # provide different yields
                    plotVar = varBase
            # Else includes zPt and topPt  
            else :
                plotVar = varBase

                
        #print "Var: %s   VarBase: %s" % (var, varBase)

        ### Make sure that if we have no events
        ### we still save a blank histo for use later
        if chain.GetEntries() == 0 :
            print " #### ENTRIES = 0 #### "
            if ":" in var :
                histos[ var ] = make2DHisto( var )
            else :
                histos[ var ] = makeHisto( var, info[0], info[1], info[2])

        ### Check that the target var is in the TTrees
        elif hasattr( chain, plotVar ) or ":" in varBase :
            #print "trying"
            #print "Var:",var,"   VarBase:",varBase, "    VarPlot:",plotVar
            if isData : # Data has no GenWeight and by def has puweight = 1
                dataES = ESCuts( 'data', channel, var )
                #print 'dataES',dataES
                chain.Draw( '%s>>%s' % (plotVar, var), '1%s%s' % (additionalCutToUse, dataES) )
                histos[ var ] = gPad.GetPrimitive( var )
                if var == 'm_vis' :
                    print 'm_vis'
                    print "Data Count:", histos[ var ].Integral()
                    #print "Cut: %s%s" % (additionalCutToUse, dataES)
            else :

                chain.Draw( '%s>>%s' % (plotVar, var), '%s' % totalCutAndWeightMC )
                ''' No reweighting at the moment! '''
                histos[ var ] = gPad.GetPrimitive( var )
                integralPost = histos[ var ].Integral()
                if var == 'm_vis' :
                    #print 'm_vis'
                    print "tmpIntPost: %f" % integralPost
                    #print "Cut: %s" % totalCutAndWeightMC

        # didn't have var in chain
        else : 
            del histos[ var ]
            continue

        histos[ var ].Write()

    #outFile.Write()
    return outFile


# Provides a list of histos to create for both channels
def getHistoDict( analysis, channel ) :
    if analysis == 'htt' :
        genVarMap = {
            #'Z_SS' : (20, -1, 1, 1, 'Z Same Sign', ''),
#XXX            'mjj' : (40, 0, 2000, 1, 'M_{jj} [GeV]', ' GeV'),
#XXX            'Z_Pt' : (100, 0, 500, 5, 'Z p_{T} [GeV]', ' GeV'),
#XXX            'Higgs_Pt' : (10, 0, 500, 1, 'Higgs p_{T} [GeV]', ' GeV'),
#XXX            'pt_sv' : (10, 0, 500, 1, 'Higgs svFit p_{T} [GeV]', ' GeV'),
#XXX            'jdeta' : (20, 0, 10, 1, 'VBF Jets dEta', ' dEta'),
#XXX#            'Z_DR' : (500, 0, 5, 20, 'Z dR', ' dR'),
#XXX#            'Z_DPhi' : (800, -4, 4, 40, 'Z dPhi', ' dPhi'),
#XXX#            'Z_DEta' : (1000, -5, 5, 40, 'Z dEta', ' dEta'),
#XXX#            'LT' : (600, 0, 300, 20, 'Total LT [GeV]', ' GeV'),
#XXX#            'Mt' : (600, 0, 400, 40, 'Total m_{T} [GeV]', ' GeV'),
#XXX            'met' : (250, 0, 250, 20, 'pfMet [GeV]', ' GeV'),
#XXX            't1_t2_MvaMet' : (250, 0, 250, 20, 't1 t2 MvaMet [GeV]', ' GeV'),
#XXX#            #'metphi' : (80, -4, 4, 10, 'pfMetPhi', ''),
#XXX            'mvamet' : (100, 0, 400, 2, 'mvaMetEt [GeV]', ' GeV'),
#XXX#            'mvametphi' : (100, -5, 5, 2, 'mvaMetPhi', ''),
#XXX#            'bjetCISVVeto20Medium' : (60, 0, 6, 5, 'nBTag_20Medium', ''),
#XXX#            'bjetCISVVeto30Medium' : (60, 0, 6, 5, 'nBTag_30Medium', ''),
#XXX#            'njetspt20' : (100, 0, 10, 10, 'nJetPt20', ''),
#XXX            'jetVeto30' : (100, 0, 10, 10, 'nJetPt30', ''),
#XXX            'njetingap20' : (100, 0, 10, 10, 'njetingap20', ''),
#XXX#            #'jetVeto40' : (100, 0, 10, 10, 'nJetPt40', ''),
#XXX#            #'nbtag' : (6, 0, 6, 1, 'nBTag', ''),
#XXX#            'bjetCISVVeto30Tight' : (60, 0, 6, 5, 'nBTag_30Tight', ''),
#XXX#            #'extraelec_veto' : (20, 0, 2, 1, 'Extra Electron Veto', ''),
#XXX#            #'extramuon_veto' : (20, 0, 2, 1, 'Extra Muon Veto', ''),
#XXX#            'jpt_1' : (400, 0, 200, 20, 'Leading Jet Pt', ' GeV'),
#XXX#            'jeta_1' : (100, -5, 5, 10, 'Leading Jet Eta', ' Eta'),
#XXX#            'jpt_2' : (400, 0, 200, 20, 'Second Jet Pt', ' GeV'),
#XXX#            'jeta_2' : (100, -5, 5, 10, 'Second Jet Eta', ' Eta'),
#XXX#            #'weight' : (60, -30, 30, 1, 'Gen Weight', ''),
#XXX#            'npv' : (40, 0, 40, 2, 'Number of Vertices', ''),
#XXX            #'npu' : (50, 1, 40, 2, 'Number of True PU Vertices', ''),
#XXX            #'m_vis_mssm' : (3900, 0, 3900, 20, 'Z Vis Mass [GeV]', ' GeV'),
#XXX            'm_vis' : [30, 0, 300, 1, 'M_{vis} [GeV]', ' GeV'],
            #'m_sv_mssm' : (3900, 0, 3900, 10, 'Z svFit Mass [GeV]', ' GeV'),
            'm_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
#XXX            'Higgs_Pt:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
#XXX            'mjj:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
#XXX            'pt_1:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
            #'mt_sv_mssm' : (3900, 0, 3900, 10, 'Total Transverse Mass (svFit) [GeV]', ' GeV'),
            #'mt_tot_mssm' : (3900, 0, 3900, 10, 'Total Transverse Mass [GeV]', ' GeV'),
#            'mt_sv' : (350, 0, 350, 10, 'Total Transverse Mass (svFit) [GeV]', ' GeV'),
#            'mt_tot' : (3900, 0, 3900, 10, 'Total Transverse Mass [GeV]', ' GeV'),
            #'pzetavis' : (300, 0, 300, 20, 'pZetaVis', ' GeV'),
            #'pfpzetamis' : (300, 0, 300, 20, 'pfpZetaMis', ' GeV'),
            #'pzetamiss' : (500, -200, 300, 20, 'pZetaMis', ' GeV'),
        }

        ''' added shape systematics '''
        toAdd = ['mt_sv', 'm_sv', 'm_vis', 'mt_tot', 'Higgs_Pt:m_sv']
        #toAdd = ['m_vis', 'm_sv', 'mt_sv',]
        toAdd = ['mt_sv', 'mt_tot', 'Higgs_Pt:m_sv', 'mjj:m_sv', 'm_sv'] # No extra shapes
        #toAdd = ['m_sv', ] # No extra shapes
        varsForShapeSyst = []
        for item in toAdd :
            varsForShapeSyst.append( item )
            #varsForShapeSyst.append( item+'_mssm' )
        #shapesToAdd = ['energyScale', 'tauPt', 'topPt', 'zPt']
        shapesToAdd = {'energyScale':'TES',
                    'zPt':'Z p_{T}/Mass Reweight',
                    #'metResponse':'Met Response',
                    #'metResolution':'Met Resolution',
                    #'tauPt':'High P_{T} Tau',
                    'topPt':'Top P_{T} Reweight',
                    'JES' : 'Jet Energy Scale',
                    }
        for var in genVarMap.keys() :
            if var in varsForShapeSyst :
                for shape, app in shapesToAdd.iteritems() :
                    genVarMap[ var+'_'+shape+'Up' ] = list(genVarMap[ var ])
                    genVarMap[ var+'_'+shape+'Up' ][4] = genVarMap[ var+'_'+shape+'Up' ][4]+' '+app+' UP'
                    genVarMap[ var+'_'+shape+'Down' ] = list(genVarMap[ var ])
                    genVarMap[ var+'_'+shape+'Down' ][4] = genVarMap[ var+'_'+shape+'Down' ][4]+' '+app+' Down'
            

        if channel == 'em' :
            # Provides a list of histos to create for 'EM' channel
            chanVarMapEM = {
                'pt_1' : (200, 0, 200, 10, 'e p_{T} [GeV]', ' GeV'),
                'eta_1' : (60, -3, 3, 2, 'e Eta', ' Eta'),
                #'iso_1' : (20, 0, 0.2, 1, 'e RelIsoDB03', ''),
                'mt_1' : (200, 0, 200, 5, 'e m_{T} [GeV]', ' GeV'),
                'pt_2' : (200, 0, 200, 10, 'm p_{T} [GeV]', ' GeV'),
                'eta_2' : (60, -3, 3, 2, 'm Eta', ' Eta'),
                #'iso_2' : (20, 0, 0.2, 1, 'm RelIsoDB03', ''),
                'mt_2' : (200, 0, 200, 5, 'm m_{T} [GeV]', ' GeV'),
                'eJetPt' : (200, 0, 200, 10, 'e Overlapping Jet Pt', ' GeV'),
                'mJetPt' : (200, 0, 200, 10, 'm Overlapping Jet Pt', ' GeV'),
                #'e_m_Pt + mvamet' : (400, 0, 400, 10, 'ditau Pt + mvamet', ' GeV'),
                #'ePVDZ' : (25, -.25, .25, 1, "e PVDZ [cm]", " cm"),
                #'ePVDXY' : (50, -.1, .1, 2, "e PVDXY [cm]", " cm"),
                #'mPVDZ' : (25, -.25, .25, 1, "m PVDZ [cm]", " cm"),
                #'mPVDXY' : (50, -.1, .1, 2, "m PVDXY [cm]", " cm"),
            }
            for key in chanVarMapEM.keys() :
                genVarMap[ key ] = chanVarMapEM[ key ]
            return genVarMap

        # Provides a list of histos to create for 'TT' channel
        if channel == 'tt' :
            chanVarMapTT = {
#                'pt_1' : (200, 0, 200, 5, '#tau_{1} p_{T} [GeV]', ' GeV'),
#                'gen_match_1' : (14, 0, 7, 1, '#tau_{1} Gen Match', ''),
                'eta_1' : (60, -3, 3, 4, '#tau_{1} Eta', ' Eta'),
#                'iso_1' : (100, -1, 1, 1, '#tau_{1} MVArun2v1DBoldDMwLTraw', ''),
#                'chargedIsoPtSum_1' : (100, 0, 5, 1, '#tau_{1} charge iso pt sum', ' GeV'),
#                'chargedIsoPtSum_2' : (100, 0, 5, 1, '#tau_{2} charge iso pt sum', ' GeV'),
#                'chargedIsoPtSumdR03_1' : (100, 0, 5, 1, '#tau_{1} charge iso pt sum dR03', ' GeV'),
#                'chargedIsoPtSumdR03_2' : (100, 0, 5, 1, '#tau_{2} charge iso pt sum dR03', ' GeV'),
#                'pt_2' : (200, 0, 200, 5, '#tau_{2} p_{T} [GeV]', ' GeV'),
#                'gen_match_2' : (14, 0, 7, 1, '#tau_{2} Gen Match', ''),
#                'eta_2' : (60, -3, 3, 4, '#tau_{2} Eta', ' Eta'),
#                'iso_2' : (100, -1, 1, 1, '#tau_{2} MVArun2v1DBoldDMwLTraw', ''),
#                'decayMode_1' : (15, 0, 15, 1, 't1 Decay Mode', ''),
#                #'t1JetPt' : (400, 0, 400, 20, 't1 Overlapping Jet Pt', ' GeV'),
#                'm_1' : (60, 0, 3, 4, 't1 Mass', ' GeV'),
#                'decayMode_2' : (15, 0, 15, 1, 't2 Decay Mode', ''),
#                #'t2JetPt' : (400, 0, 400, 20, 't2 Overlapping Jet Pt', ' GeV'),
#                'm_2' : (60, 0, 3, 4, 't2 Mass', ' GeV'),
                #'t1ChargedIsoPtSum' : (0, 10, 8, 't1 ChargedIsoPtSum', ' GeV'),
                #'t1NeutralIsoPtSum' : (0, 10, 8, 't1 NeutralIsoPtSum', ' GeV'),
                #'t1PuCorrPtSum' : (0, 40, 4, 't1 PuCorrPtSum', ' GeV'),
                #'t2ChargedIsoPtSum' : (0, 10, 8, 't2 ChargedIsoPtSum', ' GeV'),
                #'t2NeutralIsoPtSum' : (0, 10, 8, 't2 NeutralIsoPtSum', ' GeV'),
                #'t2PuCorrPtSum' : (0, 40, 4, 't2 PuCorrPtSum', ' GeV'),
            }
            for key in chanVarMapTT.keys() :
                genVarMap[ key ] = chanVarMapTT[ key ]
            return genVarMap
    if analysis == 'azh' :
        genVarMap = {
            'Z_Pt' : (400, 0, 400, 40, 'Z p_{T} [GeV]', ' GeV'),
            'Z_DR' : (500, 0, 5, 50, 'Z dR', ' dR'),
            'Z_DPhi' : (800, -4, 4, 80, 'Z dPhi', ' dPhi'),
            'Z_DEta' : (100, -5, 5, 10, 'Z dEta', ' dEta'),
            'mjj' : (40, 0, 800, 1, 'M_{jj}', ' [GeV]'),
            'jdeta' : (100, -5, 5, 10, 'VBF dEta', ' dEta'),
            'm_vis' : (80, 50, 130, 10, 'Z Mass [GeV]', ' GeV'),
            'H_vis' : (400, 0, 400, 40, 'H Visible Mass [GeV]', ' GeV'),
            'Mass' : (600, 0, 600, 60, 'M_{ll#tau#tau} [GeV]', ' GeV'),
            'LT' : (600, 0, 600, 40, 'Total LT [GeV]', ' GeV'),
            'Mt' : (600, 0, 600, 40, 'Total m_{T} [GeV]', ' GeV'),
            'met' : (250, 0, 250, 20, 'pfMet [GeV]', ' GeV'),
            'pt_1' : (200, 0, 200, 10, 'Leg1 p_{T} [GeV]', ' GeV'),
            'pt_2' : (200, 0, 200, 10, 'Leg2 p_{T} [GeV]', ' GeV'),
            'pt_3' : (200, 0, 200, 10, 'Leg3 p_{T} [GeV]', ' GeV'),
            'pt_4' : (200, 0, 200, 10, 'Leg4 p_{T} [GeV]', ' GeV'),
            'eta_1' : (60, -3, 3, 10, 'Leg1 Eta', ' Eta'),
            'eta_2' : (60, -3, 3, 10, 'Leg2 Eta', ' Eta'),
            'eta_3' : (60, -3, 3, 10, 'Leg3 Eta', ' Eta'),
            'eta_4' : (60, -3, 3, 10, 'Leg4 Eta', ' Eta'),
            'iso_1' : (20, 0, 0.5, 1, 'Leg1 RelIsoDB03', ''),
            'iso_2' : (20, 0, 0.5, 1, 'Leg2 RelIsoDB03', ''),
            'iso_3' : (20, 0, 1, 1, 'Leg3 Iso', ''),
            'iso_4' : (20, 0, 1, 1, 'Leg4 Iso', ''),
            #'jpt_1' : (400, 0, 200, 20, 'Leading Jet Pt', ' GeV'),
            #'jeta_1' : (100, -5, 5, 10, 'Leading Jet Eta', ' Eta'),
            #'jpt_2' : (400, 0, 200, 20, 'Second Jet Pt', ' GeV'),
            #'jeta_2' : (100, -5, 5, 10, 'Second Jet Eta', ' Eta'),
            #'weight' : (60, -30, 30, 1, 'Gen Weight', ''),
            'npv' : (40, 0, 40, 4, 'Number of Vertices', ''),
#            'njetspt20' : (100, 0, 10, 10, 'nJetPt20', ''),
            'jetVeto30' : (100, 0, 10, 10, 'nJetPt30', ''),
#            'azhWeight' : (50, 0, 2, 1, 'Muon + Electron Weights', ''),
            'muVetoZTTp001dxyz' : (6, -1, 5, 1, 'muVetoZTTp001dxyz', ''),
            'eVetoZTTp001dxyz' : (6, -1, 5, 1, 'eVetoZTTp001dxyz', ''),
            'muVetoZTTp001dxyzR0' : (6, -1, 5, 1, 'muVetoZTTp001dxyzR0', ''),
            'eVetoZTTp001dxyzR0' : (6, -1, 5, 1, 'eVetoZTTp001dxyzR0', ''),
            'bjetCISVVeto20Medium' : (60, 0, 6, 5, 'nBTag_20Medium', ''),
            'bjetCISVVeto30Medium' : (60, 0, 6, 5, 'nBTag_30Medium', ''),
            'bjetCISVVeto30Tight' : (60, 0, 6, 5, 'nBTag_30Tight', ''),
        }
        llltMap = {
            'againstElectronVLooseMVA6_4' : (9, -1, 2, 1, 'Against E VL MVA6 Leg 4', ''),
            'againstElectronLooseMVA6_4' : (9, -1, 2, 1, 'Against E L MVA6 Leg 4', ''),
            'againstMuonLoose3_4' : (9, -1, 2, 1, 'Against M Loose 3 Leg 4', ''),
            'againstMuonTight3_4' : (9, -1, 2, 1, 'Against M Tight 3 Leg 4', ''),
        }
        llttMap = {
            'againstElectronVLooseMVA6_3' : (9, -1, 2, 1, 'Against E VL MVA6 Leg 3', ''),
            'againstElectronLooseMVA6_3' : (9, -1, 2, 1, 'Against E L MVA6 Leg 3', ''),
            'againstMuonLoose3_3' : (9, -1, 2, 1, 'Against M Loose 3 Leg 3', ''),
            'againstMuonTight3_3' : (9, -1, 2, 1, 'Against M Tight 3 Leg 3', ''),
        }
        if channel == 'xxxx' :
            return genVarMap
        if channel in ['eeet', 'eemt', 'eett', 'emmt', 'mmmt', 'mmtt'] :
            for var in llltMap.keys() :
                genVarMap[var] = llltMap[ var ]
        if channel in ['eett', 'mmtt'] :
            for var in llttMap.keys() :
                genVarMap[var] = llttMap[ var ]
        return genVarMap







