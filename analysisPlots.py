import ROOT
from collections import OrderedDict
from ROOT import gPad



# Make a histo, but fill it later so we can keep track of events for ALL histos at once
def makeHisto( cutName, varBins, varMin, varMax ) :
    hist = ROOT.TH1F( cutName, cutName, varBins, varMin, varMax )
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
            elif 'DYJets' in sample : return True
        return False


# Make specific extra cuts for different TES requirements
def ESCuts( sample, channel, var ) :
    if not ('ggH' in sample or 'bbH' in sample or 'DYJets' in sample or 'VBF' in sample) :
        if channel == 'tt' :
            return '*(pt_1 > 40 && pt_2 > 40)'
        if channel == 'em' :
            return '*(pt_1 > 13 && pt_2 > 10)'
    ESMap = {
        'tt' : { 
            '_energyScaleUp' : '*((pt_1*1.03) > 40 && (pt_2*1.03) > 40)',
            '_energyScaleDown' : '*((pt_1*0.97) > 40 && (pt_2*0.97) > 40)',
            '_NoShift' : '*(pt_1 > 40 && pt_2 > 40)'},
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
def plotHistosProof( outFile, chain, sample, channel, isData, additionalCut, blind=False ) :
    ''' Make a channel specific selection of desired histos and fill them '''
    newVarMap = getHistoDict( channel )

    histosDir = outFile.mkdir( "%s_Histos" % channel )
    histosDir.cd()
    ''' Combine Gen and Chan specific into one fill section '''
    histos = {}
    for var, info in newVarMap.iteritems() :


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
            
        # Energy Scale reweighting only applied to DYJets and signal
        # this is not an "if" style shape b/c we need to apply
        # normal pt cuts if the shape syst is not called
        # so instead we appeand it to what ever else we have
        shapeSyst += ESCuts( sample, channel, var )


    	histos[ var ] = makeHisto( var, info[0], info[1], info[2])

        # Adding Trigger, ID and Iso, & Efficiency Scale Factors
        # and, top pt reweighting
        # weight is a composition of all applied MC/Data corrections
        #sfs = '*(weight)' 
        sfs = '*(effweight*puweight)' 
        xsec = '*(XSecLumiWeight)'

        #print "%s     High Pt Tau Weight: %s" % (var, tauW)
        dataES = '*(pt_1 > 40 && pt_2 > 40)'
        #print var,es
        #totalCutAndWeightMC = '(GenWeight/abs( GenWeight ))%s%s%s%s' % (additionalCut, sfs, xsec, shapeSyst) 
        totalCutAndWeightMC = '(GenWeight/abs( GenWeight ))%s%s%s' % (xsec, sfs, additionalCut)


        # Check if the variable to plot is in the chain, if not, skip it
        # don't crash on systematics based variables
        varBase = var
        if 'Up' in var or 'Down' in var :
            varBase = var.split('_')[0]
        if '_sv' in var :
            varBase += '_sv'
        #print "Var: %s   VarBase: %s" % (var, varBase)
        if hasattr( chain, varBase ) :
            #print "trying"
            if isData : # Data has no GenWeight and by def has puweight = 1
                if var == 'm_vis' and blind :
                    chain.Draw( '%s>>%s' % (var, var), '(m_vis < 150)%s' % additionalCut )
                    histos[ var ] = gPad.GetPrimitive( "%s" % var )
                else :
                    chain.Draw( '%s>>%s' % (var, var), '1%s%s' % (additionalCut, dataES) )
                    histos[ var ] = gPad.GetPrimitive( "%s" % var )
                    if var == 'm_vis' :
                        print 'm_vis'
                        print "Data Count:", histos[ var ].Integral()
            else :

                chain.Draw( '%s>>%s' % (var, var), '%s' % totalCutAndWeightMC )
                ''' No reweighting at the moment! '''
                histos[ var ] = gPad.GetPrimitive( var )
                if chain.GetEntries() > 0 :
                    integralPost = histos[ var ].Integral()
                    if var == 'm_vis' :
                        print 'm_vis'
                        print "tmpIntPost: %f" % integralPost
                else :
                    print " #### ENTRIES = 0 #### "
                    histos[ var ] = makeHisto( var, info[0], info[1], info[2])

        # didn't have var in chain
        else : 
            del histos[ var ]
            continue

        histos[ var ].Write()

    #outFile.Write()
    return outFile


# Provides a list of histos to create for both channels
def getHistoDict( channel ) :
    genVarMap = {
#        'Z_SS' : (20, -1, 1, 1, 'Z Same Sign', ''),
        'Z_Pt' : (400, 0, 400, 40, 'Z p_{T} [GeV]', ' GeV'),
        'Z_DR' : (500, 0, 5, 20, 'Z dR', ' dR'),
        'Z_DPhi' : (800, -4, 4, 40, 'Z dPhi', ' dPhi'),
        'Z_DEta' : (1000, -5, 5, 40, 'Z dEta', ' dEta'),
        'LT' : (600, 0, 300, 20, 'Total LT [GeV]', ' GeV'),
        'Mt' : (600, 0, 400, 40, 'Total m_{T} [GeV]', ' GeV'),
#        'met' : (250, 0, 250, 20, 'pfMet [GeV]', ' GeV'),
#        'metphi' : (80, -4, 4, 10, 'pfMetPhi', ''),
#        'mvamet' : (100, 0, 400, 2, 'mvaMetEt [GeV]', ' GeV'),
#        'mvametphi' : (100, -5, 5, 2, 'mvaMetPhi', ''),
        'bjetCISVVeto20Medium' : (60, 0, 6, 5, 'nBTag_20Medium', ''),
        'bjetCISVVeto30Medium' : (60, 0, 6, 5, 'nBTag_30Medium', ''),
        'njetspt20' : (100, 0, 10, 10, 'nJetPt20', ''),
        'jetVeto30' : (100, 0, 10, 10, 'nJetPt30', ''),
        #'jetVeto40' : (100, 0, 10, 10, 'nJetPt40', ''),
        #'nbtag' : (6, 0, 6, 1, 'nBTag', ''),
        'bjetCISVVeto30Tight' : (60, 0, 6, 5, 'nBTag_30Tight', ''),
        #'extraelec_veto' : (20, 0, 2, 1, 'Extra Electron Veto', ''),
        #'extramuon_veto' : (20, 0, 2, 1, 'Extra Muon Veto', ''),
        'jpt_1' : (400, 0, 200, 20, 'Leading Jet Pt', ' GeV'),
        'jeta_1' : (100, -5, 5, 10, 'Leading Jet Eta', ' Eta'),
        'jpt_2' : (400, 0, 200, 20, 'Second Jet Pt', ' GeV'),
        'jeta_2' : (100, -5, 5, 10, 'Second Jet Eta', ' Eta'),
#        'weight' : (60, -30, 30, 1, 'Gen Weight', ''),
        'npv' : (40, 0, 40, 2, 'Number of Vertices', ''),
        #'npu' : (50, 1, 40, 2, 'Number of True PU Vertices', ''),
#        'm_vis_mssm' : (3900, 0, 3900, 20, 'Z Vis Mass [GeV]', ' GeV'),
        'm_vis' : (350, 0, 350, 10, 'Z Vis Mass [GeV]', ' GeV'),
#        'm_sv_mssm' : (3900, 0, 3900, 10, 'Z svFit Mass [GeV]', ' GeV'),
#        'm_sv' : (350, 0, 350, 10, 'Z svFit Mass [GeV]', ' GeV'),
#        'mt_sv_mssm' : (3900, 0, 3900, 10, 'Total Transverse Mass (svFit) [GeV]', ' GeV'),
#        'mt_tot_mssm' : (3900, 0, 3900, 10, 'Total Transverse Mass [GeV]', ' GeV'),
#XX        'mt_sv' : (350, 0, 350, 10, 'Total Transverse Mass (svFit) [GeV]', ' GeV'),
#        'mt_tot' : (350, 0, 350, 10, 'Total Transverse Mass [GeV]', ' GeV'),
#        'pzetavis' : (300, 0, 300, 20, 'pZetaVis', ' GeV'),
#        'pfpzetamis' : (300, 0, 300, 20, 'pfpZetaMis', ' GeV'),
#        'pzetamiss' : (500, -200, 300, 20, 'pZetaMis', ' GeV'),
    }

    ''' added shape systematics '''
    #toAdd = ['mt_sv', 'm_sv', 'm_vis', 'mt_tot']
    #varsForShapeSyst = []
    #for item in toAdd :
    #    varsForShapeSyst.append( item )
    #    varsForShapeSyst.append( item+'_mssm' )
    #shapesToAdd = ['energyScale', 'tauPt', 'topPt', 'zPt']
    #for var in genVarMap.keys() :
    #    if var in varsForShapeSyst :
    #        for shape in shapesToAdd :
    #            genVarMap[ var+'_'+shape+'Up' ] = genVarMap[ var ]
    #            genVarMap[ var+'_'+shape+'Down' ] = genVarMap[ var ]
    #    

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
            'pt_1' : (200, 0, 200, 5, '#tau_{1} p_{T} [GeV]', ' GeV'),
            'eta_1' : (60, -3, 3, 4, '#tau_{1} Eta', ' Eta'),
            'byIsolationMVArun2v1DBoldDMwLTraw_1' : (200, -1, 1, 1, '#tau_{1} MVArun2v1DBoldDMwLTraw', ''),
            'pt_2' : (200, 0, 200, 5, '#tau_{2} p_{T} [GeV]', ' GeV'),
            'eta_2' : (60, -3, 3, 4, '#tau_{2} Eta', ' Eta'),
            'byIsolationMVArun2v1DBoldDMwLTraw_2' : (200, -1, 1, 1, '#tau_{2} MVArun2v1DBoldDMwLTraw', ''),
            'decayMode_1' : (15, 0, 15, 1, 't1 Decay Mode', ''),
#            't1JetPt' : (400, 0, 400, 20, 't1 Overlapping Jet Pt', ' GeV'),
            'm_1' : (60, 0, 3, 4, 't1 Mass', ' GeV'),
            'decayMode_2' : (15, 0, 15, 1, 't2 Decay Mode', ''),
#            't2JetPt' : (400, 0, 400, 20, 't2 Overlapping Jet Pt', ' GeV'),
            'm_2' : (60, 0, 3, 4, 't2 Mass', ' GeV'),
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



