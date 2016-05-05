# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: ttbar_2017_800_pu25 --conditions auto:phase1_2017_realistic --filein /store/relval/CMSSW_8_1_0_pre1/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v4_UPG17PU35-v1/10000/829292FC-EFED-E511-8AED-0025905B85D6.root -n 99999 --era Run2_2017 -s PAT --runUnscheduled --eventcontent MINIAODSIM --mc --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2017 --geometry Extended2017 --customise_commands del process.patTrigger; del process.selectedPatTrigger --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('PAT',eras.Run2_2017)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2017Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(99999)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/02D678DD-FCD3-E511-8B71-0CC47A4C8E26.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/04ADB568-01D4-E511-B436-0CC47A745294.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/1A49B96E-FAD3-E511-AABD-0CC47A4D7600.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/26AD97E1-F2D3-E511-978E-0CC47A78A3EE.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/2853F819-F8D3-E511-81CF-0CC47A4C8E16.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/2A943257-F7D3-E511-BEFC-0025905A60AA.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/3487BDC4-01D4-E511-A6A1-0025905B85DA.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/42B2B532-03D4-E511-A0AE-0CC47A78A440.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/44D9828D-02D4-E511-8470-0CC47A78A41C.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/5247106E-FAD3-E511-909A-0025905B85C6.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/5A49171D-03D4-E511-95D5-0026189438AA.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/5C9A223C-03D4-E511-8AD7-0025905964BE.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/828B9826-D1D4-E511-B802-0025905964B4.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/82987C71-FAD3-E511-A353-0CC47A4D7600.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/8A5DA4A2-01D4-E511-98A8-0025905A6094.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/9C984C4B-9AD4-E511-9CCD-0CC47A4C8E3C.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/BA330B37-9BD4-E511-ABA4-003048FFD71C.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/C00BAB28-04D4-E511-AFD8-0025905A60F8.root',
        'root://eoscms//eos/cms/store/relval/CMSSW_8_0_0_pre6/RelValTTbar_13/GEN-SIM-RECO/PU25ns_80X_upgrade2017_design_v3_UPG17-v1/10000/D2BC4224-03D4-E511-829C-002590593902.root', 
        ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('ttbar_2017_800_pu25 nevts:99999'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('ttbar_2017_800_pu25_PAT.root'),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2017_realistic', '')

# Path and EndPath definitions
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_globalSuperTightHalo2016Filter = cms.Path(process.globalSuperTightHalo2016Filter)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_chargedHadronTrackResolutionFilter = cms.Path(process.chargedHadronTrackResolutionFilter)
process.Flag_globalTightHalo2016Filter = cms.Path(process.globalTightHalo2016Filter)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_HcalStripHaloFilter = cms.Path(process.HcalStripHaloFilter)
process.Flag_muonBadTrackFilter = cms.Path(process.muonBadTrackFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.Flag_HBHENoiseFilter,process.Flag_HBHENoiseIsoFilter,process.Flag_CSCTightHaloFilter,process.Flag_CSCTightHaloTrkMuUnvetoFilter,process.Flag_CSCTightHalo2015Filter,process.Flag_globalTightHalo2016Filter,process.Flag_globalSuperTightHalo2016Filter,process.Flag_HcalStripHaloFilter,process.Flag_hcalLaserEventFilter,process.Flag_EcalDeadCellTriggerPrimitiveFilter,process.Flag_EcalDeadCellBoundaryEnergyFilter,process.Flag_goodVertices,process.Flag_eeBadScFilter,process.Flag_ecalLaserCorrFilter,process.Flag_trkPOGFilters,process.Flag_chargedHadronTrackResolutionFilter,process.Flag_muonBadTrackFilter,process.Flag_trkPOG_manystripclus53X,process.Flag_trkPOG_toomanystripclus53X,process.Flag_trkPOG_logErrorTooManyClusters,process.Flag_METFilters,process.endjob_step,process.MINIAODSIMoutput_step)

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2017 

#call to customisation function cust_2017 imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
process = cust_2017(process)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
process.load('Configuration.StandardSequences.PATMC_cff')
from FWCore.ParameterSet.Utilities import cleanUnscheduled
process=cleanUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

# End of customisation functions

# Customisation from command line
del process.patTrigger; del process.selectedPatTrigger; process.pfSimpleInclusiveSecondaryVertexHighEffBJetTags = cms.EDProducer("JetTagProducer", jetTagComputer = cms.string('candidateSimpleSecondaryVertex2TrkComputer'), tagInfos = cms.VInputTag(cms.InputTag("pfInclusiveSecondaryVertexFinderTagInfos")))
