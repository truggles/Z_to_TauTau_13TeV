import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *

def isAncestor(a,p) :
        if a == p : 
                return True
        for i in xrange(0,p.numberOfMothers()) :
                if isAncestor(a,p.mother(i)) :
                         return True
        return False

def calcDR( eta1, phi1, eta2, phi2 ) :
    return float(sqrt( (eta1-eta2)*(eta1-eta2) + (phi1-phi2)*(phi1-phi2) ))

def findGen( part, gens ) :
    bestDR = 999.
    bestIndex = -1
    pEta = part.eta()
    pPhi = part.phi()
    for i in range( len(gens) ):
        gen = gens[i]
        gEta = gen.eta()
        gPhi = gen.phi()
        tmpDR = calcDR( pEta, pPhi, gEta, gPhi )
        print tmpDR
        if tmpDR < bestDR :
            print "Best DR so far:",bestDR,tmpDR
            bestDR = tmpDR
            bestIndex = i
    print "BEST DR:",bestDR
    return i



#events = Events (['root://cms-xrd-global.cern.ch//store/mc/Spring14miniaod/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/F6EDDC10-8DFC-E311-BC5D-0025905A60D6.root'])
events = Events("/afs/cern.ch/work/t/truggles/Z_to_tautau/dyjets_76x.root")

handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
labelPruned = ("prunedGenParticles")
labelPacked = ("packedGenParticles")
taus, tauLabel = Handle("std::vector<pat::Tau>"), "slimmedTaus"
electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"

# loop over events
count= 0
for event in events:
    event.getByLabel (labelPacked, handlePacked)
    event.getByLabel (labelPruned, handlePruned)
    event.getByLabel(tauLabel, taus) 
    event.getByLabel(electronLabel, electrons) 
    event.getByLabel(muonLabel, muons) 
    # get the product
    packed = handlePacked.product()
    pruned = handlePruned.product()

    if count > 10 : break

    print "# Taus: %i" % len( taus.product() )
    for i,tau in enumerate(taus.product()):
        #print i
        genTau = tau.genParticle()
        if genTau :
            print genTau
            print " - # of mothers ",genTau.numberOfMothers()
        iGen = findGen( tau, pruned )
        genId = pruned[iGen].pdgId()
        genPrompt = pruned[iGen].statusFlags().isPrompt()
        genDecay = pruned[iGen].fromHardProcessDecayed()
        print "Gen pdgID: %i   Gen Decay: %s   Is Prompt %s" % (genId, genDecay, genPrompt)
        #print " - tau %i, Mother: %d" % (i, tau.mother(0).pdgId() ) 
    
    #for p in pruned :
    #    #if abs(p.pdgId()) > 500 and abs(p.pdgId()) < 600 :
    #    if p.pdgId() != 23 : continue
    #    print "PdgId : %s   pt : %s  eta : %s   phi : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi())    
    #    print "     daughters"
    #    for pa in packed:
    #                    mother = pa.mother(0)
    #                    if mother and isAncestor(p,mother) :
    #                          print "     PdgId : %s   pt : %s  eta : %s   phi : %s" %(pa.pdgId(),pa.pt(),pa.eta(),pa.phi())


    count += 1

