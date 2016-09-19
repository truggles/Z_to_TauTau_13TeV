import ROOT
import math
import argparse
import json
from tauHelpers import calcDR, transMass, buildFullLumiList



p = argparse.ArgumentParser(description="A script to apply additional cuts and plot.")
p.add_argument('--inputFiles', action='store', default='xxx', dest='inputFiles', help="Which file should I run over?")
#FIXME p.add_argument('--inputFiles', action='store', type=list, dest='inputFiles', help="Which file should I run over?")
p.add_argument('--outputFile', action='store', default='xxx', dest='outputFile', help="Which file should I run over?")
p.add_argument('--external', action='store', default=False, type=bool, dest='external', help="Running on Condor?")
options = p.parse_args()
external = options.external
inputFileList = options.inputFiles
print "InputFile List"
print inputFileList
outputFile = options.outputFile
mpCount = 0

print "Opening JSON"
with open('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt') as jsonFile :
    jsonDict = json.load( jsonFile )
lumiJSON = buildFullLumiList( jsonDict )
#print lumiJSON

if inputFileList == 'xxx' :
    inputFileList = '/store/data/Run2016D/SingleMuon/MINIAOD/PromptReco-v2/000/276/528/00000/82386779-BF49-E611-ADD4-02163E013499.root'
maxEvents = 999999


doLumi=True
doLumi=False
localFile=False
includeTrigger=True

print "TAG-AND-PROBE ANALYZER CALLED:"
print "Count: %i" % mpCount
print "InputFileList:"
print inputFileList

# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

print "ROOT.AutoLibraryLoader.enable DONE"

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

taus, tauLabel = Handle("std::vector<pat::Tau>"), "slimmedTaus"
jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"
muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
mets, metLabel = Handle("std::vector<pat::MET>"), "slimmedMETs"
vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"
if includeTrigger :
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT")
    #triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT2")

print "DEFINED DATA FORMATS"

if localFile :
    import os.path
    here = os.path.dirname('.')
    print "Local path: %s" % here
    events = Events( here+inputFileList )
if not localFile :
    print "Not Local File"
    toLoad = ''
    #FIXME for file in inputFileList :
    #FIXME     file.strip()+','
    #FIXME events = Events(toLoad)
    events = Events(inputFileList)
    print "Opened File"

print "Loaded target file",inputFileList

#tFile = ROOT.TFile('study.root','RECREATE')
''' Store root files in separate folders by Run '''
import os
#outName = ''
#if not external : outName += 'processed/'
#outInfo = inputFile.strip('.root').split('/')
#outName += outInfo[-1]+'.root'
#tFile = ROOT.TFile('/CMSSW_8_0_13/src/TagAndProbe_13_tagAndProbeSept15-'+outName, 'RECREATE')
#tFile = ROOT.TFile('TagAndProbe_13_tagAndProbeSept15-'+outName, 'RECREATE')
tFile = ROOT.TFile(outputFile, 'RECREATE')
print tFile

#tFile = ROOT.TFile('tmp.root','RECREATE')
tDir = tFile.mkdir('TagAndProbe')
tDir.cd()
tTree = ROOT.TTree('Ntuple','Ntuple')
nEvents = ROOT.TH1D('nEvents','nEvents',1,-0.5,0.5)

print "Made TTree and TH1"

# Our tree of vars to fill
from collections import OrderedDict
varMap = OrderedDict()
varList = [
'run','lumi','evt','nvtx','nvtxCleaned','IsoMu20','IsoMu22','IsoMu24',\
'IsoMu27','IsoMu21MediumIsoTau32','TrigPass','mPt','mEta','mPhi',\
'tPt','tEta','tPhi','tMVAIsoLoose','tMVAIsoMedium','tMVAIsoTight',\
'tMVAIsoVTight','m_vis','mt','SS']
for i,var in enumerate( varList ) :
    varMap[i] = var

print "Made Ordered Dict"


### Make branches in TTree for all our variables in the varMap
vals = {}
branches = []
from array import array
for key in varMap.keys() :
    vals[key] = array('f', [0] )
    branches.append( tTree.Branch('%s' % varMap[key].strip('_'), vals[key], '%s/F' % varMap[key].strip('_') ) )

print "Used Array"

### To track the value of each var before it's filled
tally = OrderedDict()
for key in varMap.keys() :
    tally[ varMap[key] ] = 0.


print "Starting Events"

### Start looping over event
for iev,event in enumerate(events):
    if iev > maxEvents: break
    event.getByLabel(vertexLabel, vertices)
    if includeTrigger :
        event.getByLabel(triggerBitLabel, triggerBits)

    for key in tally.keys() :
        tally[ key ] = -10
    #if iev > 20000 : break    

    if iev % 10000 == 0 or (localFile and iev % 1000 == 0) :
        print " --- File #: %i iev: %d: run %6d, lumi %4d, event %12d" %\
                (mpCount,iev,event.eventAuxiliary().run(),\
                event.eventAuxiliary().\
                luminosityBlock(),event.eventAuxiliary().event())



    ### Check if this evt is in the Golden Json
    tally['run'] = event.eventAuxiliary().run()
    tally['lumi'] = event.eventAuxiliary().luminosityBlock()
    if doLumi :
        if not tally['run'] in lumiJSON.keys() : continue
        if not tally['lumi'] in lumiJSON[tally['run']] : continue
    tally['evt'] = event.eventAuxiliary().event()
    nEvents.Fill( 0, 1 )



    ### Check our HLT paths, skip if neither trig is included
    if includeTrigger :
        # log the lowest un-prescaled HLT trigger for these 4 runs
        trignames = event.object().triggerNames(triggerBits.product())
        tally['TrigPass'] = 0
        for i in xrange(triggerBits.product().size()):
            #if triggerBits.product().accept(i) : print "PASS trigger: %s" % trignames.triggerName(i) 
            if 'HLT_IsoMu20_v'\
                    in trignames.triggerName(i) :
                if triggerBits.product().accept(i) :
                    tally['IsoMu20'] = 1
                    tally['TrigPass'] += 1
                else : tally['IsoMu20'] = 0
            if 'HLT_IsoMu22_v'\
                    in trignames.triggerName(i) :
                if triggerBits.product().accept(i) :
                    tally['IsoMu22'] = 1
                    tally['TrigPass'] += 1
                else : tally['IsoMu22'] = 0
            if 'HLT_IsoMu24_v'\
                    in trignames.triggerName(i) :
                if triggerBits.product().accept(i) :
                    tally['IsoMu24'] = 1
                    tally['TrigPass'] += 1
                else : tally['IsoMu24'] = 0
            if 'HLT_IsoMu27_v'\
                    in trignames.triggerName(i) :
                if triggerBits.product().accept(i) :
                    tally['IsoMu27'] = 1
                    tally['TrigPass'] += 1
                else : tally['IsoMu27'] = 0
            if 'HLT_IsoMu21_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v'\
                    in trignames.triggerName(i) :
                if triggerBits.product().accept(i) :
                    tally['IsoMu21MediumIsoTau32'] = 1
                    tally['TrigPass'] += 1
                    #print "IsoMu21MediumIsoTau32 Passed!"
                else : tally['IsoMu21MediumIsoTau32'] = 0
        if tally['TrigPass'] == 0 : continue



    ### Check for good Vertices
    tally['nvtx'] = 0
    tally['nvtxCleaned'] = 0
    if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
        #print "Event has no good primary vertex."
        continue
    else:
        PV = vertices.product()[0]
        for vtx in vertices.product() :
            if not vtx.isFake() : tally['nvtxCleaned'] += 1
    tally['nvtx'] = vertices.product().size()



    ### Find the best muon
    ### If more than 1 muon, skip event
    event.getByLabel(muonLabel, muons)
    muonCount = 0
    bestMuon = 0
    for k,muon in enumerate(muons.product()) :
        mPt = muon.pt()
        if mPt < 20: continue
        mAbsEta = abs( muon.eta() )
        if mAbsEta > 2.1: continue
        mID = muon.isMediumMuon()
        if mID < 0.5 : continue
        mIso = (muon.pfIsolationR04().sumChargedHadronPt\
            + max(0., muon.pfIsolationR04().sumNeutralHadronEt\
            + muon.pfIsolationR04().sumPhotonEt\
            - 0.5*muon.pfIsolationR04().sumPUPt))\
            /muon.pt()
        if mIso > 0.1 : continue
        muonCount += 1
        bestMuon = muon
        #print "Muon %i   pt: %.2f   absEta: %.2f   MedID: %i   Iso: %.2f" %\
        #        (muonCount, mPt, mAbsEta, mID, mIso)
    if muonCount == 0 : continue



    ### Extra Muon Veto
    if muonCount > 1 :
        #print "Extra muon veto"
        continue
    #if muonCount > 0 :
    #    print "bestmuon pt:",bestMuon.pt()



    ### Find the best elec
    ### If more than 0 elec, skip event
    event.getByLabel(electronLabel, electrons)
    elecCount = 0
    for k,elec in enumerate(electrons.product()) :
        ePt = elec.pt()
        if ePt < 20: continue
        eAbsEta = abs( elec.eta() )
        if eAbsEta > 2.1: continue
        #eID1 = elec.userFloat("ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values")
        #print " ---- eID1",eID1
        eID2 = elec.electronID("mvaEleID-Spring15-25ns-nonTrig-V1-wp90")
        #print " ---- eID2",eID2
        if eID2 < 0.5 : continue
        eIso = (elec.pfIsolationVariables().sumChargedHadronPt + max(\
            elec.pfIsolationVariables().sumNeutralHadronEt + \
            elec.pfIsolationVariables().sumPhotonEt - \
            0.5 * elec.pfIsolationVariables().sumPUPt, 0.0)) / elec.pt()
        if eIso > 0.1 : continue
        elecCount += 1
        #print "Elec %i   pt: %.2f   absEta: %.2f   MedID: %i   Iso: %.2f" %\
        #        (elecCount, ePt, eAbsEta, eID2, eIso)



    ### Extra Electron Veto
    if elecCount > 0 :
        #print "Extra electron veto"
        continue



    ### Find the best Tau
    event.getByLabel(tauLabel, taus) 
    tauCount = 0
    bestTau = 0
    for i,tau in enumerate(taus.product()):
        tPt = tau.pt()
        if tPt < 20: continue
        tAbsEta = abs( tau.eta() )
        if tAbsEta > 2.1: continue
        tIsoPass = tau.tauID('byLooseIsolationMVArun2v1DBoldDMwLT')
        if tIsoPass < 0.5 : continue
        if tau.tauID("decayModeFinding") < 0.5 : continue
        if tau.tauID('againstElectronLooseMVA6') < 0.5 : continue
        if tau.tauID('againstMuonTight3') < 0.5 : continue
        tIso = tau.tauID('byIsolationMVArun2v1DBoldDMwLTraw')
        if tauCount > 0 :
            if tIso > bestTau.tauID('byIsolationMVArun2v1DBoldDMwLTraw') :
                bestTau = tau
            else : continue
        else : bestTau = tau
        tauCount += 1
    if tauCount == 0 : continue
    #print "Best Tau Pt:",bestTau.pt()



    ### BJet Veto
    event.getByLabel(jetLabel, jets) 
    numBTaggedJets = 0
    for k,jet in enumerate(jets.product()) :
        if jet.pt() < 20 : continue
        if abs(jet.eta()) > 2.4 : continue
        if calcDR( jet.eta(), jet.phi(), bestMuon.eta(), bestMuon.phi() ) < 0.5 :
            continue # overlapping, so skip it
        if calcDR( jet.eta(), jet.phi(), bestTau.eta(), bestTau.phi() ) < 0.5 :
            continue # overlapping, so skip it
        #FIXME if jet.userFloat('idLoose') < 0.5 : continue
        if jet.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.8 :
            numBTaggedJets += 1
            #print "Jet CISV Val: %.2f" % jet.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')
    if numBTaggedJets > 0 : continue



    ### Visible Mass Cut
    lorentz1 = ROOT.TLorentzVector( 0.,0.,0.,0. )
    lorentz1.SetPtEtaPhiM( bestMuon.pt(), bestMuon.eta(),\
            bestMuon.phi(), bestMuon.mass() )
    lorentz2 = ROOT.TLorentzVector( 0.,0.,0.,0. )
    lorentz2.SetPtEtaPhiM( bestTau.pt(), bestTau.eta(),\
            bestTau.phi(), bestTau.mass() )
    visMass = (lorentz1 + lorentz2).M()



    ### Get PF MET for Transverse Mass Cut
    event.getByLabel(metLabel, mets) 
    met = mets.product()[0]
    #print " --- MET Pt",met.pt()
    #print " --- MET Phi",met.phi()
    


    ### Transverse Mass Cut
    mt = transMass( met.pt(), met.phi(), bestMuon.pt(), bestMuon.phi() )


    ### Sign comparison
    SS = 0 if bestMuon.charge() + bestTau.charge() == 0 else 1
    #print "SS:",SS

    ### Fill Stuff!
    tally['mPt'] = bestMuon.pt()
    tally['mEta'] = bestMuon.eta()
    tally['mPhi'] = bestMuon.phi()
    tally['tPt'] = bestTau.pt()
    tally['tEta'] = bestTau.eta()
    tally['tPhi'] = bestTau.phi()
    tally['tMVAIsoLoose'] = tau.tauID('byLooseIsolationMVArun2v1DBoldDMwLT')
    tally['tMVAIsoMedium'] = tau.tauID('byMediumIsolationMVArun2v1DBoldDMwLT')
    tally['tMVAIsoTight'] = tau.tauID('byTightIsolationMVArun2v1DBoldDMwLT')
    tally['tMVAIsoVTight'] = tau.tauID('byVTightIsolationMVArun2v1DBoldDMwLT')
    tally['m_vis'] = visMass
    tally['mt'] = mt
    tally['SS'] = SS



    for key in varMap.keys() :
        vals[key][0] = tally[ varMap[key] ]


    tTree.Fill()
tDir.cd()
tTree.Write()
nEvents.Write()
tFile.Close() 













