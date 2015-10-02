import ROOT
from collections import OrderedDict

# Make a histo, but fill it later so we can keep track of events for ALL histos at once
def makeHisto( cutName, varBins, varMin, varMax ) :
    hist = ROOT.TH1F( cutName, cutName, varBins, varMin, varMax )
    return hist

# Provides a list of histos to create for both channels
def getHistoDict( channel ) :
    genVarMap = {
        'LT' : ('LT', 600, 0, 600),
        'Mt' : ('Mt', 600, 0, 600),
        'met' : ('met', 100, 0, 400),
        'metPhi' : ('metphi', 100, -5, 5),
        #'mvaMetEt' : ('mvamet', 100, 0, 400),
        #'mvaMetPhi' : ('mvametphi', 100, -5, 5),
        #'bjetCISVVeto20Medium' : ('bjetCISVVeto20Medium', 60, 0, 5),
        'njetspt20' : ('njetspt20', 100, 0, 10),
        'nbtag' : ('nbtag', 100, 0, 10),
        'extraelec_veto' : ('extraelec_veto', 20, 0, 2),
        'extramuon_veto' : ('extramuon_veto', 20, 0, 2),
        'jpt_1' : ('jpt_1', 100, 0, 400),
        'jeta_1' : ('jeta_1', 100, -5, 5),
        'jpt_2' : ('jpt_2', 100, 0, 400),
        'jeta_2' : ('jeta_2', 100, -5, 5),
        'GenWeight' : ('GenWeight', 1000, -300000, 300000),
        'nvtx' : ('nvtx', 50, 0, 50),
        'm_vis' : ('m_vis', 600, 0, 600),
        'pt_1' : ('pt_1', 100, 0, 400),
        'eta_1' : ('eta_1', 100, -5, 5),
        'iso_1' : ('iso_1', 200, 0, 1),
        'mt_1' : ('mt_1', 100, 0, 400),
        'pt_2' : ('pt_2', 100, 0, 400),
        'eta_2' : ('eta_2', 100, -5, 5),
        'iso_2' : ('iso_2', 200, 0, 1),
        'mt_2' : ('mt_2', 100, 0, 400),
    }

    if channel == 'em' :
        # Provides a list of histos to create for 'EM' channel
        chanVarMapEM = {
            'Z_Pt' : ('e_m_Pt', 100, 0, 400),
            'Z_SS' : ('e_m_SS', 20, 0, 2),
            'eJetPt' : ('eJetPt', 100, 0, 400),
            'mJetPt' : ('mJetPt', 100, 0, 400),
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
            'Z_SS' : ('t1_t2_SS', 20, 0, 2),
            #'t1Pt' : ('t1Pt', 100, 0, 400),
            #'t1Eta' : ('t1Eta', 100, -5, 5),
            #'t1ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t1ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 5),
            #'t1ByIsolationMVA3newDMwLTraw' : ('t1ByIsolationMVA3newDMwLTraw', 100, -1, 1),
            #'t1ByIsolationMVA3newDMwoLTraw' : ('t1ByIsolationMVA3newDMwoLTraw', 100, -1, 1),
            #'t1ByIsolationMVA3oldDMwLTraw' : ('t1ByIsolationMVA3oldDMwLTraw', 100, -1, 1),
            #'t1ByIsolationMVA3oldDMwoLTraw' : ('t1ByIsolationMVA3oldDMwoLTraw', 100, -1, 1),
            #'t1ChargedIsoPtSum' : ('t1ChargedIsoPtSum', 100, 0, 10),
            #'t1NeutralIsoPtSum' : ('t1NeutralIsoPtSum', 100, 0, 10),
            #'t1PuCorrPtSum' : ('t1PuCorrPtSum', 40, 0, 40),
            #'t1MtToPFMET' : ('t1MtToPFMET', 100, 0, 400),
            'decayModeFindingOldDMs_1' : ('decayModeFindingOldDMs_1', 12, 0, 12),
            't1JetPt' : ('t1JetPt', 100, 0, 400),
            'm_1' : ('m_1', 60, 0, 3),
            #'t2Pt' : ('t2Pt', 100, 0, 400),
            #'t2Eta' : ('t2Eta', 100, -5, 5),
            #'t2ByCombinedIsolationDeltaBetaCorrRaw3Hits' : ('t2ByCombinedIsolationDeltaBetaCorrRaw3Hits', 100, 0, 5),
            #'t2ByIsolationMVA3newDMwLTraw' : ('t1ByIsolationMVA3newDMwLTraw', 100, -1, 1),
            #'t2ByIsolationMVA3newDMwoLTraw' : ('t1ByIsolationMVA3newDMwoLTraw', 100, -1, 1),
            #'t2ByIsolationMVA3oldDMwLTraw' : ('t1ByIsolationMVA3oldDMwLTraw', 100, -1, 1),
            #'t2ByIsolationMVA3oldDMwoLTraw' : ('t1ByIsolationMVA3oldDMwoLTraw', 100, -1, 1),
            #'t2ChargedIsoPtSum' : ('t1ChargedIsoPtSum', 100, 0, 10),
            #'t2NeutralIsoPtSum' : ('t1NeutralIsoPtSum', 100, 0, 10),
            #'t2PuCorrPtSum' : ('t1PuCorrPtSum', 40, 0, 40),
            #'t2MtToPFMET' : ('t2MtToPFMET', 100, 0, 400),
            'decayModeFindingOldDMs_2' : ('decayModeFindingOldDMs_2', 12, 0, 12),
            't2JetPt' : ('t2JetPt', 100, 0, 400),
            'm_2' : ('m_2', 60, 0, 3),
        }
        for key in chanVarMapTT.keys() :
            genVarMap[ key ] = chanVarMapTT[ key ]
        return genVarMap


def getPlotDetails( channel ) :
    plotDetails = {
        'm_vis' : (0, 300, 4, 'Z Vis Mass [GeV]', ' GeV'),
        'Z_Pt' : (0, 200, 2, 'Z p_{T} [GeV]', ' GeV'),
        'Z_SS' : (-1, 1, 1, 'Z Same Sign', ''),
        'met' : (0, 400, 2, 'pfMet [GeV]', ' GeV'),
        'metPhi' : (-5, 5, 2, 'pfMetPhi', ''),
        #'mvaMetEt' : (0, 400, 2, 'mvaMetEt [GeV]', ' GeV'),
        #'mvaMetPhi' : (-5, 5, 2, 'mvaMetPhi', ''),
        'LT' : (0, 600, 6, 'Total LT [GeV]', ' GeV'),
        'Mt' : (0, 600, 6, 'Total m_{T} [GeV]', ' GeV'),
        'nbtag' : (0, 5, 10, 'nBTag', ''),
        'njetspt20' : (0, 10, 10, 'nJetPt20', ''),
        'jpt_1' : (0, 200, 2, 'Leading Jet Pt', ' GeV'),
        'jeta_1' : (-5, 5, 2, 'Leading Jet Eta', ''),
        'jpt_2' : (0, 200, 2, 'Second Jet Pt', ' GeV'),
        'jeta_2' : (-5, 5, 2, 'Second Jet Eta', ''),
        'extraelec_veto' : (0, 2, 1, 'Extra Electron Veto', ''),
        'extramuon_veto' : (0, 2, 1, 'Extra Muon Veto', ''),
        'GenWeight' : (-30000, 30000, 1, 'Gen Weight', ''),
        'nvtx' : (0, 50, 1, 'Number of Vertices', ''),
        }

    if channel == 'em' :
        plotDetailsEM  = {
        'eta_1' : (-3, 3, 2, 'e Eta', ''),
        'pt_1' : (0, 200, 2, 'e p_{T} [GeV]', ' GeV'),
        'mt_1' : (0, 200, 2, 'e m_{T} [GeV]', ' GeV'),
        'ePVDXY' : (-.1, .1, 2, "e PVDXY [cm]", " cm"),
        'ePVDZ' : (-.25, .25, 1, "e PVDZ [cm]", " cm"),
        'eRelPFIsoDB' : (0, 0.2, 1, 'e RelPFIsoDB', ''),
        'iso_1' : (0, 0.2, 1, 'e RelIsoDB03', ''),
        'eJetPt' : (0, 200, 2, 'e Overlapping Jet Pt', ' GeV'),
        'eta_2' : (-3, 3, 2, 'm Eta', ''),
        'pt_2' : (0, 200, 1, 'm p_{T} [GeV]', ' GeV'),
        'mt_2' : (0, 200, 2, 'm m_{T} [GeV]', ' GeV'),
        'mPVDXY' : (-.1, .1, 2, "m PVDXY [cm]", " cm"),
        'mPVDZ' : (-.25, .25, 1, "m PVDZ [cm]", " cm"),
        'mRelPFIsoDBDefault' : (0, 0.3, 1, 'm RelPFIsoDB', ''),
        'iso_2' : (0, 0.3, 1, 'm RelIsoDB03', ''),
        'mJetPt' : (0, 200, 2, 'm Overlapping Jet Pt', ' GeV'),
        }
        for key in plotDetailsEM.keys() :
            plotDetails[ key ] = plotDetailsEM[ key ]
        return plotDetails

    if channel == 'tt' :
        plotDetailsTT = {
        'iso_1' : (0, 5, 1, '#tau_{1}CombIsoDBCorrRaw3Hits', ''),
        'eta_1' : ( -3, 3, 4, '#tau_{1} Eta', ''),
        'pt_1' : (0, 200, 2, '#tau_{1} p_{T} [GeV]', ' GeV'),
        'mt_1' : (0, 200, 2, '#tau_{1} m_{T} [GeV]', ' GeV'),
        'm_1' : (0, 3, 2, 't1 Mass', ' GeV'),
        'decayModeFindingOldDMs_1' : (0, 15, 1, 't1 Decay Mode', ''),
        'iso_2' : (0, 5, 1, '#tau_{2}CombIsoDBCorrRaw3Hits', ''),
        'eta_2' : ( -3, 3, 4, '#tau_{2} Eta', ''),
        'pt_2' : (0, 200, 2, '#tau_{2} p_{T} [GeV]', ' GeV'),
        'mt_2' : (0, 200, 2, '#tau_{2} m_{T} [GeV]', ' GeV'),
        'm_2' : (0, 3, 2, 't2 Mass', ' GeV'),
        'decayModeFindingOldDMs_2' : (0, 15, 1, 't2 Decay Mode', ''),
        't1JetPt' : (0, 400, 2, 't1 Overlapping Jet Pt', ' GeV'),
        't2JetPt' : (0, 400, 2, 't2 Overlapping Jet Pt', ' GeV'),
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
