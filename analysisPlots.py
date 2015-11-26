import ROOT
from collections import OrderedDict
from ROOT import gPad

# Make a histo, but fill it later so we can keep track of events for ALL histos at once
def makeHisto( cutName, varBins, varMin, varMax ) :
    hist = ROOT.TH1F( cutName, cutName, varBins, varMin, varMax )
    return hist


# Plot histos using TTree::Draw which works very well with Proof
def plotHistosProof( outFile, chain, channel, isData, additionalCut, blind ) :
    ''' Make a channel specific selection of desired histos and fill them '''
    newVarMap = getHistoDict( channel )

    histosDir = outFile.mkdir( "%s_Histos" % channel )
    histosDir.cd()
    ''' Combine Gen and Chan specific into one fill section '''
    histos = {}
    histos2 = {}
    for var, cv in newVarMap.iteritems() :
        #if var != 'npv' : continue
        var2 = '%s%i' % (var, 2)
    	histos[ var ] = makeHisto( var, cv[1], cv[2], cv[3])
    	histos2[ var2 ] = makeHisto( var2, cv[1], cv[2], cv[3])
        # the >> sends the output to a predefined histo
        if isData : # Data has no GenWeight and by def has puweight = 1
            if var == 'm_vis' and blind :
                chain.Draw( '%s>>%s' % (newVarMap[ var ][0], var), '(m_vis < 150)%s' % additionalCut )
                histos[ var ] = gPad.GetPrimitive( "%s" % var )
            else :
                chain.Draw( '%s>>%s' % (newVarMap[ var ][0], var), '1%s' % additionalCut )
                histos[ var ] = gPad.GetPrimitive( "%s" % var )
        else :
            chain.Draw( '%s>>%s' % (newVarMap[ var ][0], var2), 'GenWeight/abs( GenWeight )%s' % additionalCut )
            histos2[ var ] = gPad.GetPrimitive( var2 )

            chain.Draw( '%s>>%s' % (newVarMap[ var ][0], var), 'puweight * (GenWeight/abs( GenWeight ))%s' % additionalCut )
            ''' No reweighting at the moment! '''
            #chain.Draw( '%s>>%s' % (newVarMap[ var ][0], var), '(GenWeight/abs( GenWeight ))%s' % additionalCut )
            histos[ var ] = gPad.GetPrimitive( var )
            if chain.GetEntries() > 0 :
                integralPre = histos2[ var ].Integral()
                integralPost = histos[ var ].Integral()
                if var == 'm_vis' :
                    print 'm_vis'
                    print "intPre: %f" % integralPre
                    print "tmpIntPost: %f" % integralPost
                    if integralPre != 0 :
                        print " --- percent increase w/ PU reweight %f" % ( integralPost / ( integralPre ) )
                    #print "  ---!!! UNSCALING !!!--- "
                #if integralPost != 0 :
                #    histos[ var ].Scale( integralPre / integralPost )
            else :
                print " #### ENTRIES = 0 #### "
                histos[ var ] = makeHisto( var, cv[1], cv[2], cv[3])
        histos[ var ].Write()

    #outFile.Write()
    return outFile


# Provides a list of histos to create for both channels
def getHistoDict( channel ) :
    genVarMap = {
        'Z_SS' : ('Z_SS', 20, 0, 2),
        'LT' : ('LT', 600, 0, 600),
        'Mt' : ('Mt', 600, 0, 600),
        'met' : ('met', 400, 0, 400),
        'metphi' : ('metphi', 80, -4, 4),
        'mvamet' : ('mvamet', 100, 0, 400),
        'mvametphi' : ('mvametphi', 100, -5, 5),
        #'bjetCISVVeto20Medium' : ('bjetCISVVeto20Medium', 60, 0, 5),
        'njetspt20' : ('njetspt20', 100, 0, 10),
        'jetVeto30' : ('jetVeto30', 100, 0, 10),
        'jetVeto40' : ('jetVeto40', 100, 0, 10),
        'nbtag' : ('nbtag', 6, 0, 6),
        'bjetCISVVeto30Medium' : ('bjetCISVVeto30Medium', 6, 0, 6),
        'bjetCISVVeto30Tight' : ('bjetCISVVeto30Tight', 6, 0, 6),
        'extraelec_veto' : ('extraelec_veto', 20, 0, 2),
        'extramuon_veto' : ('extramuon_veto', 20, 0, 2),
        'jpt_1' : ('jpt_1', 400, 0, 400),
        'jeta_1' : ('jeta_1', 100, -5, 5),
        'jpt_2' : ('jpt_2', 400, 0, 400),
        'jeta_2' : ('jeta_2', 100, -5, 5),
        'GenWeight' : ('GenWeight', 1000, -300000, 300000),
        'npv' : ('npv', 50, 0, 50),
        'npu' : ('npu', 50, 0, 50),
        'm_vis' : ('m_vis', 600, 0, 600),
        'pt_1' : ('pt_1', 400, 0, 400),
        'eta_1' : ('eta_1', 80, -4, 4),
        'iso_1' : ('iso_1', 100, 0, 1),
        'mt_1' : ('mt_1', 400, 0, 400),
        'pt_2' : ('pt_2', 400, 0, 400),
        'eta_2' : ('eta_2', 80, -4, 4),
        'iso_2' : ('iso_2', 100, 0, 1),
        'mt_2' : ('mt_2', 400, 0, 400),
        'Z_DEta' : ('eta_1 - eta_2', 1000, -5, 5),
        'pzetavis' : ('pzetavis', 1000, -100, 900),
        'pzetamis' : ('pzetamis', 1000, -400, 600),
        'pZeta-0.85pZetaVis' : ('pzetamis - 0.85 * pzetavis', 1000, -500, 500),
    }

    if channel == 'em' :
        # Provides a list of histos to create for 'EM' channel
        chanVarMapEM = {
            'Z_Pt' : ('e_m_Pt', 400, 0, 400),
            'eJetPt' : ('eJetPt', 400, 0, 400),
            'mJetPt' : ('mJetPt', 400, 0, 400),
            'Z_DR' : ('e_m_DR', 500, 0, 5),
            'Z_DPhi' : ('e_m_DPhi', 800, -4, 4),
            #'m_sv' : ('m_sv', 1000, 0, 1000),
            'pt_H' : ('e_m_Pt + mvamet', 1000, 0, 1000),
            #'ePVDZ' : ('ePVDZ', 100, -1, 1),
            #'ePVDXY' : ('ePVDXY', 100, -.2, .2),
            #'mPVDZ' : ('mPVDZ', 100, -1, 1),
            #'mPVDXY' : ('mPVDXY', 100, -.2, .2),
        }
        for key in chanVarMapEM.keys() :
            genVarMap[ key ] = chanVarMapEM[ key ]
        return genVarMap

    # Provides a list of histos to create for 'TT' channel
    if channel == 'tt' :
        chanVarMapTT = {
            'Z_Pt' : ('t1_t2_Pt', 400, 0, 400),
            #'m_vis' : ('m_vis', 600, 0, 600),
            'Z_DR' : ('t1_t2_DR', 500, 0, 5),
            'Z_DPhi' : ('t1_t2_DPhi', 800, -4, 4),
            #'m_sv' : ('m_sv', 1000, 0, 1000),
            'pt_H' : ('t1_t2_Pt + mvamet', 1000, 0, 1000),
            't1DecayMode' : ('t1DecayMode', 12, 0, 12),
            't1JetPt' : ('t1JetPt', 400, 0, 400),
            'm_1' : ('m_1', 60, 0, 3),
            't2DecayMode' : ('t2DecayMode', 12, 0, 12),
            't2JetPt' : ('t2JetPt', 400, 0, 400),
            'm_2' : ('m_2', 60, 0, 3),
        }
        for key in chanVarMapTT.keys() :
            genVarMap[ key ] = chanVarMapTT[ key ]
        return genVarMap


def getPlotDetails( channel ) :
    plotDetails = {
        'm_vis' : (0, 350, 10, 'Z Vis Mass [GeV]', ' GeV'),
        'Z_Pt' : (0, 200, 10, 'Z p_{T} [GeV]', ' GeV'),
        'Z_SS' : (-1, 1, 1, 'Z Same Sign', ''),
        'met' : (0, 250, 10, 'pfMet [GeV]', ' GeV'),
        'metphi' : (-4, 4, 2, 'pfMetPhi', ''),
        'mvamet' : (0, 400, 2, 'mvaMetEt [GeV]', ' GeV'),
        'mvametphi' : (-5, 5, 2, 'mvaMetPhi', ''),
        'LT' : (0, 300, 10, 'Total LT [GeV]', ' GeV'),
        'Mt' : (0, 400, 20, 'Total m_{T} [GeV]', ' GeV'),
        'nbtag' : (0, 6, 1, 'nBTag', ''),
        'bjetCISVVeto30Medium' : (0, 6, 1, 'nBTag_30Medium'),
        'bjetCISVVeto30Tight' : (0, 6, 1, 'nBTag_30Tight'),
        'njetspt20' : (0, 10, 10, 'nJetPt20', ''),
        'jetVeto30' : (0, 10, 10, 'nJetPt30', ''),
        'jetVeto40' : (0, 10, 10, 'nJetPt40', ''),
        'jpt_1' : (0, 200, 10, 'Leading Jet Pt', ' GeV'),
        'jeta_1' : (-5, 5, 10, 'Leading Jet Eta', ' Eta'),
        'jpt_2' : (0, 200, 10, 'Second Jet Pt', ' GeV'),
        'jeta_2' : (-5, 5, 10, 'Second Jet Eta', ' Eta'),
        'extraelec_veto' : (0, 2, 1, 'Extra Electron Veto', ''),
        'extramuon_veto' : (0, 2, 1, 'Extra Muon Veto', ''),
        'GenWeight' : (-30000, 30000, 1, 'Gen Weight', ''),
        'npv' : (0, 35, 1, 'Number of Vertices', ''),
        'npu' : (0, 35, 1, 'Number of True PU Vertices', ''),
        'pzetavis' : (0, 300, 10, 'pZetaVis', ' GeV'),
        'pzetamis' : (-200, 300, 10, 'pZetaMis', ' GeV'),
        'pZeta-0.85pZetaVis' : (-300, 300, 10, 'pZetaMis - 0.85 x pZetaVis', ' GeV'),
        'Z_DR' : (0, 5, 20, 'Z dR', ' dR'),
        'Z_DPhi' : (-4, 4, 10, 'Z dPhi', ' dPhi'),
        'Z_DEta' : (-5, 5, 40, 'Z dEta', ' dEta'),
        #'m_sv' : (0, 600, 20, 'ditau svFit Mass', ' GeV'),
        'pt_H' : (0, 400, 10, 'ditau Pt + mvamet', ' GeV'),
        }

    if channel == 'em' :
        plotDetailsEM  = {
        'eta_1' : (-3, 3, 2, 'e Eta', ' Eta'),
        'pt_1' : (0, 200, 10, 'e p_{T} [GeV]', ' GeV'),
        'mt_1' : (0, 200, 5, 'e m_{T} [GeV]', ' GeV'),
        'ePVDXY' : (-.1, .1, 2, "e PVDXY [cm]", " cm"),
        'ePVDZ' : (-.25, .25, 1, "e PVDZ [cm]", " cm"),
        'eRelPFIsoDB' : (0, 0.2, 1, 'e RelPFIsoDB', ''),
        'iso_1' : (0, 0.2, 1, 'e RelIsoDB03', ''),
        'eJetPt' : (0, 200, 10, 'e Overlapping Jet Pt', ' GeV'),
        'eta_2' : (-3, 3, 2, 'm Eta', ' Eta'),
        'pt_2' : (0, 200, 10, 'm p_{T} [GeV]', ' GeV'),
        'mt_2' : (0, 200, 5, 'm m_{T} [GeV]', ' GeV'),
        'mPVDXY' : (-.1, .1, 2, "m PVDXY [cm]", " cm"),
        'mPVDZ' : (-.25, .25, 1, "m PVDZ [cm]", " cm"),
        'mRelPFIsoDBDefault' : (0, 0.3, 1, 'm RelPFIsoDB', ''),
        'iso_2' : (0, 0.2, 1, 'm RelIsoDB03', ''),
        'mJetPt' : (0, 200, 10, 'm Overlapping Jet Pt', ' GeV'),
        }
        for key in plotDetailsEM.keys() :
            plotDetails[ key ] = plotDetailsEM[ key ]
        return plotDetails

    if channel == 'tt' :
        plotDetailsTT = {
        'iso_1' : (0, 10, 1, '#tau_{1}CombIsoDBCorrRaw3Hits', ''),
        'eta_1' : ( -3, 3, 4, '#tau_{1} Eta', ' Eta'),
        'pt_1' : (0, 200, 10, '#tau_{1} p_{T} [GeV]', ' GeV'),
        'mt_1' : (0, 200, 10, '#tau_{1} m_{T} [GeV]', ' GeV'),
        'm_1' : (0, 3, 2, 't1 Mass', ' GeV'),
        't1DecayMode' : (0, 15, 1, 't1 Decay Mode', ''),
        'iso_2' : (0, 10, 1, '#tau_{2}CombIsoDBCorrRaw3Hits', ''),
        'eta_2' : ( -3, 3, 4, '#tau_{2} Eta', ' Eta'),
        'pt_2' : (0, 200, 10, '#tau_{2} p_{T} [GeV]', ' GeV'),
        'mt_2' : (0, 200, 10, '#tau_{2} m_{T} [GeV]', ' GeV'),
        'm_2' : (0, 3, 2, 't2 Mass', ' GeV'),
        't2DecayMode' : (0, 15, 1, 't2 Decay Mode', ''),
        't1JetPt' : (0, 400, 10, 't1 Overlapping Jet Pt', ' GeV'),
        't2JetPt' : (0, 400, 10, 't2 Overlapping Jet Pt', ' GeV'),
        't1ChargedIsoPtSum' : (0, 10, 4, 't1 ChargedIsoPtSum', ' GeV'),
        't1NeutralIsoPtSum' : (0, 10, 4, 't1 NeutralIsoPtSum', ' GeV'),
        't1PuCorrPtSum' : (0, 40, 2, 't1 PuCorrPtSum', ' GeV'),
        't2ChargedIsoPtSum' : (0, 10, 4, 't2 ChargedIsoPtSum', ' GeV'),
        't2NeutralIsoPtSum' : (0, 10, 4, 't2 NeutralIsoPtSum', ' GeV'),
        't2PuCorrPtSum' : (0, 40, 2, 't2 PuCorrPtSum', ' GeV'),
        }
        for key in plotDetailsTT.keys() :
            plotDetails[ key ] = plotDetailsTT [ key ]
        return plotDetails

