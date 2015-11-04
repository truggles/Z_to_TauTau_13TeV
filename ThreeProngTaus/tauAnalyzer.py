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


# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
#events = Events("root://eoscms//eos/cms/store/relval/CMSSW_7_4_1/RelValTTbar_13/MINIAODSIM/PU25ns_MCRUN2_74_V9_gensim71X-v1/00000/72C84BA7-F9EC-E411-B875-002618FDA210.root")
events = Events("/afs/cern.ch/work/t/truggles/Z_to_tautau/sync_mcRun2.root")

from array import array
tFile = ROOT.TFile('threeProngTaus.root','RECREATE')
tDir = tFile.mkdir('tauEvents')
tDir.cd()
tTree = ROOT.TTree('Ntuple','Ntuple')

varMap = {
    0 : ('nvtx_', 'f'),
    1 : ('numTaus_', 'f'),
    2 : ('numJets_', 'f'),
}

vals = []
branches = []

for i, key in varMap.iteritems() :
    vals.append( array('%s' % varMap[i][1], [ 0 ] ) )
    branches.append( tTree.Branch('%s' % varMap[i][0].strip('_'), vals[i], '%s/%s' % (varMap[i][0].strip('_'), varMap[i][1].capitalize() ) ) )


for iev,event in enumerate(events):
    event.getByLabel(tauLabel, taus) 
    event.getByLabel(vertexLabel, vertices)
    event.getByLabel(vertexLabel, verticesScore)
    event.getByLabel(jetLabel, jets)

    print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    
    nvtx_ = 0
    numTaus_ = 0
    numJets_ = 0

    # Vertices
    if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
        print "Event has no good primary vertex."
        continue
    else:
        PV = vertices.product()[0]
        print "PV at x,y,z = %+5.3f, %+5.3f, %+6.3f, ndof: %.1f, score: (pt2 of clustered objects) %.1f" % (PV.x(), PV.y(), PV.z(), PV.ndof(),verticesScore.product().get(0))
        for vtx in vertices.product() :
            if not vtx.isFake() : nvtx_ += 1
        print "\n nvtx? %i \n" % nvtx_


    # Tau
    for i,tau in enumerate(taus.product()):
        if tau.pt() < 20: continue
        numTaus_ += 1
        print "tau  %2d: pt %4.1f, dxy signif %.1f, ID(byMediumCombinedIsolationDeltaBetaCorr3Hits) %.1f, lead candidate pt %.1f, pdgId %d decayMode=%i" % (
                    i, tau.pt(), tau.dxy_Sig(), tau.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits"), tau.leadCand().pt(), tau.leadCand().pdgId(), tau.decayMode()) 

    # Jets (standard AK4)
    for i,j in enumerate(jets.product()):
        if j.pt() < 10: continue
        numJets_ += 1
        print "jet %3d: pt %5.1f (raw pt %5.1f, matched-calojet pt %5.1f), eta %+4.2f, btag run1(CSV) %.3f, run2(pfCSVIVFV2) %.3f, pileup mva disc %+.2f" % (
            i, j.pt(), j.pt()*j.jecFactor('Uncorrected'), j.userFloat("caloJetMap:pt"), j.eta(), max(0,j.bDiscriminator("combinedSecondaryVertexBJetTags")), max(0,j.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")), j.userFloat("pileupJetId:fullDiscriminant"))
        if i == 0: # for the first jet, let's print the leading constituents
            constituents = [ j.daughter(i2) for i2 in xrange(j.numberOfDaughters()) ]
            constituents.sort(key = lambda c:c.pt(), reverse=True)
            for i2, cand in enumerate(constituents):
                if i2 > 4: 
                        print "         ....."
                        break
                print "         constituent %3d: pt %6.2f, dz(pv) %+.3f, pdgId %+3d" % (i2,cand.pt(),cand.dz(PV.position()),cand.pdgId()) 
    print "Num Jets %f" % numJets_


    vals[0][0] = nvtx_
    vals[1][0] = numTaus_
    vals[2][0] = numJets_




    tTree.Fill()
    if iev > 10: break
tDir.cd()
tTree.Write()
tFile.Close() 




