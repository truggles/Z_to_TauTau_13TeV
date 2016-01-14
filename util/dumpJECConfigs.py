import FWCore.ParameterSet.Config as cms
process = cms.Process("jectxt")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
# define your favorite global tag
process.GlobalTag.globaltag = cms.string('74X_mcRun2_asymptotic_v4')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))
process.source = cms.Source("EmptySource")
process.readAK4PFchs    = cms.EDAnalyzer('JetCorrectorDBReader',  
      # below is the communication to the database 
      payloadName    = cms.untracked.string('AK4PFchs'),
      # this is used ONLY for the name of the printed txt files. You can use any name that you like, 
      # but it is recommended to use the GT name that you retrieved the files from.
      globalTag      = cms.untracked.string('74X_mcRun2_asymptotic_v4'),  
      printScreen    = cms.untracked.bool(False),
      createTextFile = cms.untracked.bool(True)
)
process.readAK8PFchs = process.readAK4PFchs.clone(payloadName = 'AK8PFchs')
process.readAK4PF = process.readAK4PFchs.clone(payloadName = 'AK4PF')
process.p = cms.Path(process.readAK4PFchs * process.readAK8PFchs * process.readAK4PF)
