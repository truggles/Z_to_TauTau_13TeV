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

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

taus, tauLabel = Handle("std::vector<pat::Tau>"), "slimmedTaus"
vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"
verticesScore = Handle("edm::ValueMap<float>")
jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"

import math
dRCut = 0.4
def calcDR( eta1, phi1, eta2, phi2 ) :
    return float(math.sqrt( (eta1-eta2)*(eta1-eta2) + (phi1-phi2)*(phi1-phi2) ))

# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
#events = Events("root://eoscms//eos/cms/store/relval/CMSSW_7_4_1/RelValTTbar_13/MINIAODSIM/PU25ns_MCRUN2_74_V9_gensim71X-v1/00000/72C84BA7-F9EC-E411-B875-002618FDA210.root")
# didn't work! events = Events("edmFileUtil -d /store/data/Run2015D/JetHT/MINIAOD/PromptReco-v4/000/259/721/00000/FEB5B9FA-1B7B-E511-8791-02163E011B09.root")
events = Events("root://eoscms//eos/cms/store/data/Run2015D/JetHT/MINIAOD/PromptReco-v4/000/259/721/00000/FEB5B9FA-1B7B-E511-8791-02163E011B09.root")
#events = Events("/afs/cern.ch/work/t/truggles/Z_to_tautau/sync_mcRun2.root")
#events = Events("/afs/cern.ch/work/t/truggles/Z_to_tautau/JetHT.root")

from array import array
tFile = ROOT.TFile('study.root','RECREATE')
tDir = tFile.mkdir('tauEvents')
tDir.cd()
tTree = ROOT.TTree('Ntuple','Ntuple')

from collections import OrderedDict
varMap = OrderedDict()
varMap[0] = 'run'
varMap[1] = 'lumi'
varMap[2] = 'evt'
varMap[3] = 'nvtx'
varMap[4] = 'numTaus'
varMap[5] = 'numTausThreeProng'
varMap[6] = 'numJets10'
varMap[7] = 'numJets20'


# Add Jets
count = 0
for i in range(1, 41, 4):
    count += 1
    varMap[9+i] = 'j%iPt' % count
    varMap[9+i+1] = 'j%iEta' % count
    varMap[9+i+2] = 'j%iMatchTau' % count
    varMap[9+i+3] = 'j%iMatchTauThreeProng' % count

vals = {}
branches = []

for key in varMap :
    print "key: %s    var: %s" % (key, varMap[key])
# Make branches in TTree for all our variables in the varMap
for key in varMap.keys() :
    vals[key] = array('f', [0] )
    #branches.append( tTree.Branch('%s' % varMap[key][0].strip('_'), vals[key], '%s/%s' % (varMap[key][0].strip('_'), varMap[key][1].capitalize() ) ) )
    branches.append( tTree.Branch('%s' % varMap[key].strip('_'), vals[key], '%s/F' % varMap[key].strip('_') ) )

# To track the value of each var before it's filled
tally = OrderedDict()
for key in varMap.keys() :
    tally[ varMap[key] ] = 0


for iev,event in enumerate(events):
    event.getByLabel(tauLabel, taus) 
    event.getByLabel(vertexLabel, vertices)
    event.getByLabel(vertexLabel, verticesScore)
    event.getByLabel(jetLabel, jets)

    for key in tally.keys() :
        tally[ key ] = -10

    #print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    tally['run'] = event.eventAuxiliary().run()
    tally['lumi'] = event.eventAuxiliary().luminosityBlock()
    tally['evt'] = event.eventAuxiliary().event()
    

    # Vertices
    tally['nvtx'] = 0
    if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
        print "Event has no good primary vertex."
        continue
    else:
        PV = vertices.product()[0]
        #print "PV at x,y,z = %+5.3f, %+5.3f, %+6.3f, ndof: %.1f, score: (pt2 of clustered objects) %.1f" % (PV.x(), PV.y(), PV.z(), PV.ndof(),verticesScore.product().get(0))
        for vtx in vertices.product() :
            if not vtx.isFake() : tally['nvtx'] += 1
        #print "\n nvtx? %i \n" % nvtx_


    # Tau
    tally['numTaus'] = 0
    tally['numTausThreeProng'] = 0
    for i,tau in enumerate(taus.product()):
        if tau.pt() < 20: continue
        if abs( tau.eta() ) > 2.3: continue
        tally['numTaus'] += 1
        if tau.decayMode() != 10: continue
        tally['numTausThreeProng'] += 1
        
        #print "tau  %2d: pt %4.1f, dxy signif %.1f, ID(byMediumCombinedIsolationDeltaBetaCorr3Hits) %.1f, lead candidate pt %.1f, pdgId %d decayMode=%i" % (i, tau.pt(), tau.dxy_Sig(), tau.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits"), tau.leadCand().pt(), tau.leadCand().pdgId(), tau.decayMode()) 

    # Jets (standard AK4)
    tally['numJets10'] = 0
    tally['numJets20'] = 0
    tausMatched = 0
    tausMatchedThreeProng = 0
    for i,j in enumerate(jets.product()):
        if j.pt() < 10: continue
        if abs( j.eta() ) > 4.7: continue
        tally['numJets10'] += 1
        if j.pt() > 20: tally['numJets20'] += 1
        jPt = j.pt()
        jEta = j.eta()
        jPhi = j.phi()
        jMatchTau = 0
        jMatchTauThreeProng = 0
        for k,tau in enumerate(taus.product()) :
            if tau.pt() < 20: continue
            if abs( tau.eta() ) > 2.3: continue
            tPt = tau.pt()
            tEta = tau.eta()
            tPhi = tau.phi()
            dR = calcDR( jEta, jPhi, tEta, tPhi )
            if dR < dRCut :
                jMatchTau += 1
                tausMatched += 1
                print "evt:%i MATCH: dR = %f   j#%i   tau#%i" % (tally['evt'], dR, i, k)
                if tau.decayMode() == 10 :
                    jMatchTauThreeProng += 1
                    tausMatchedThreeProng += 1
        tally['j%iPt' % i] = jPt
        tally['j%iEta' % i] = jEta
        tally['j%iPhi' % i] = jPhi
        tally['j%iMatchTau' % i] = jMatchTau
        tally['j%iMatchTauThreeProng' % i] = jMatchTauThreeProng
        #print "jet %3d: pt %5.1f (raw pt %5.1f, matched-calojet pt %5.1f), eta %+4.2f, btag run1(CSV) %.3f, run2(pfCSVIVFV2) %.3f, pileup mva disc %+.2f" % (i, j.pt(), j.pt()*j.jecFactor('Uncorrected'), j.userFloat("caloJetMap:pt"), j.eta(), max(0,j.bDiscriminator("combinedSecondaryVertexBJetTags")), max(0,j.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")), j.userFloat("pileupJetId:fullDiscriminant"))
        #if i == 0: # for the first jet, let's print the leading constituents
        #    constituents = [ j.daughter(i2) for i2 in xrange(j.numberOfDaughters()) ]
        #    constituents.sort(key = lambda c:c.pt(), reverse=True)
        #    for i2, cand in enumerate(constituents):
        #        if i2 > 4: 
        #                #print "         ....."
        #                break
                #print "         constituent %3d: pt %6.2f, dz(pv) %+.3f, pdgId %+3d" % (i2,cand.pt(),cand.dz(PV.position()),cand.pdgId()) 
    #print "Num Jets %f" % numJets10_
    if tally['numTaus'] != tausMatched : print " --- evt:%i numTaus and Taus Matched to jets differs! nTau %f : nMatch: %f" % (tally['evt'], tally['numTaus'], tausMatched )
    if tally['numTausThreeProng'] != tausMatchedThreeProng : print " --- evt:%i numTaus3Prong and Taus Matched 3 Prong to jets differs! nTau3P %f : nMatch3P: %f" % (tally['evt'], tally['numTausThreeProng'], tausMatchedThreeProng )


    for key in varMap.keys() :
        vals[key][0] = tally[ varMap[key] ]


    tTree.Fill()
    #if iev > 98: break
tDir.cd()
tTree.Write()
tFile.Close() 




