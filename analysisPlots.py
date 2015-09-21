import ROOT
from collections import OrderedDict

# Make a histo, but fill it later so we can keep track of events for ALL histos at once
def makeHisto( cutName, varBins, varMin, varMax ) :
	hist = ROOT.TH1F( cutName, cutName, varBins, varMin, varMax )
	return hist
			
# Provides a list of histos to create for both channels
def getGeneralHistoDict() :
	genVarMap = {
		'LT' : ('LT', 600, 0, 600),
		'Mt' : ('Mt', 600, 0, 600),
		'met' : ('met', 100, 0, 400),
		'metPhi' : ('metPhi', 100, -5, 5),
		'mvaMetEt' : ('mvaMetEt', 100, 0, 400),
		'mvaMetPhi' : ('mvaMetPhi', 100, -5, 5),
		#'bjetCISVVeto20Medium' : ('bjetCISVVeto20Medium', 60, 0, 5),
		'njetspt20' : ('njetspt20', 100, 0, 10),
		'nbtag' : ('nbtag', 100, 0, 10),
        'extraelec_veto' : ('extraelec_veto', 20, 0, 2),
        'extramuon_veto' : ('extramuon_veto', 20, 0, 2),
		'jpt_1' : ('jpt_1', 100, 0, 400),
		'jeta_1' : ('jeta_1', 100, -5, 5),
		'jpt_1' : ('jpt_2', 100, 0, 400),
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
	return genVarMap
			
# Provides a list of histos to create for 'EM' channel
def getEMHistoDict() :
	chanVarMap = {
		'Z_Pt' : ('e_m_Pt', 100, 0, 400),
		'Z_SS' : ('e_m_SS', 20, 0, 2),
		'eJetPt' : ('eJetPt', 100, 0, 400),
		'mJetPt' : ('mJetPt', 100, 0, 400),
		#'ePVDZ' : ('ePVDZ', 100, -1, 1),
		#'ePVDXY' : ('ePVDXY', 100, -.2, .2),
		#'mPVDZ' : ('mPVDZ', 100, -1, 1),
		#'mPVDXY' : ('mPVDXY', 100, -.2, .2),
	}
	return chanVarMap

# Provides a list of histos to create for 'TT' channel
def getTTHistoDict() :
	chanVarMap = {
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
	return chanVarMap

