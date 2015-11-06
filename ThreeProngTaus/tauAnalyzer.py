
def tauAnalyzer( mpCount, targetRun, targetLumis, targetFile ) :
    
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
    #events = Events("root://eoscms//eos/cms/store/data/Run2015D/JetHT/MINIAOD/PromptReco-v4/000/259/721/00000/FEB5B9FA-1B7B-E511-8791-02163E011B09.root")
    events = Events("root://eoscms//eos/cms/store%s" % targetFile)
    #events = Events("/afs/cern.ch/work/t/truggles/Z_to_tautau/sync_mcRun2.root")
    #events = Events("/afs/cern.ch/work/t/truggles/Z_to_tautau/JetHT.root")
    
    #tFile = ROOT.TFile('study.root','RECREATE')
    ''' Store root files in separate folders by Run '''
    import os
    if not os.path.exists( '%i' % targetRun ):
        os.makedirs( '%i' % targetRun )
    tFile = ROOT.TFile('%i/%i_%i_%s.root' % (targetRun, targetRun, mpCount, targetFile.split('/')[-1].split('.')[0]),'RECREATE')
    tDir = tFile.mkdir('tauEvents')
    tDir.cd()
    tTree = ROOT.TTree('Ntuple','Ntuple')
    
    # Our tree of vars to fill
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
    varMap[8] = 'nvtxCleaned'
    varMap[9] = 'orbitNumber'
    varMap[10] = 'bunchCrossing'
    
    # Add Jets to tree
    count = 0
    for i in range(1, 31, 3):
        count += 1
        varMap[19+i] = 'j%iPt' % count
        varMap[19+i+1] = 'j%iEta' % count
        varMap[19+i+2] = 'j%iPhi' % count
    
    # Add Taus to tree
    # Only keey 3 prong taus!!!
    count = 0
    for i in range(1, 51, 5):
        count += 1
        varMap[99+i] = 't%iPt' % count
        varMap[99+i+1] = 't%iEta' % count
        varMap[99+i+2] = 't%iPhi' % count
        varMap[99+i+3] = 't%iJetDR' % count
        varMap[99+i+4] = 't%iJetPt' % count
        
    
    vals = {}
    branches = []
    
    #for key in varMap :
    #    print "key: %s    var: %s" % (key, varMap[key])
    # Make branches in TTree for all our variables in the varMap
    from array import array
    for key in varMap.keys() :
        vals[key] = array('f', [0] )
        branches.append( tTree.Branch('%s' % varMap[key].strip('_'), vals[key], '%s/F' % varMap[key].strip('_') ) )
    
    # To track the value of each var before it's filled
    tally = OrderedDict()
    for key in varMap.keys() :
        tally[ varMap[key] ] = 0
    
    
    ''' Start looping over event '''
    print "targetRun : %i" % targetRun
    print "targetLumis : ",targetLumis
    for iev,event in enumerate(events):
        event.getByLabel(tauLabel, taus) 
        event.getByLabel(vertexLabel, vertices)
        event.getByLabel(vertexLabel, verticesScore)
        event.getByLabel(jetLabel, jets)
    
        for key in tally.keys() :
            tally[ key ] = -10
    
        # Check if this evt is in the Run and Good Lumis we want
        tally['run'] = event.eventAuxiliary().run()
        if targetRun != tally['run'] : continue
        tally['lumi'] = event.eventAuxiliary().luminosityBlock()
        if tally['lumi'] not in targetLumis : continue

        tally['evt'] = event.eventAuxiliary().event()
        tally['orbitNumber'] = event.eventAuxiliary().orbitNumber()
        tally['bunchCrossing'] = event.eventAuxiliary().bunchCrossing()
        print "iev: %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

        
    
        # Vertices
        tally['nvtx'] = 0
        tally['nvtxCleaned'] = 0
        if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
            print "Event has no good primary vertex."
            continue
        else:
            PV = vertices.product()[0]
            #print "PV at x,y,z = %+5.3f, %+5.3f, %+6.3f, ndof: %.1f, score: (pt2 of clustered objects) %.1f" % (PV.x(), PV.y(), PV.z(), PV.ndof(),verticesScore.product().get(0))
            for vtx in vertices.product() :
                if not vtx.isFake() : tally['nvtxCleaned'] += 1
        tally['nvtx'] = vertices.product().size()
    
    
        # Tau
        tally['numTaus'] = 0
        tally['numTausThreeProng'] = 0
        cnt = 0
        for i,tau in enumerate(taus.product()):
            if tau.pt() < 20: continue
            if abs( tau.eta() ) > 2.5: continue
            tally['numTaus'] += 1
            if tau.decayMode() != 10: continue
            cnt += 1
            tally['numTausThreeProng'] += 1
            tally['t%iPt' % cnt] = tau.pt()
            tEta = tau.eta()
            tPhi = tau.phi()
            tally['t%iEta' % cnt] = tEta
            tally['t%iPhi' % cnt] = tPhi
            # Find the JetPt and dR of our matching Jet
            jetDRAndPt = []
            for k,jet in enumerate(jets.product()) :
                if jet.pt() < 20: continue
                if abs( jet.eta() ) > 3: continue
                jEta = jet.eta()
                jPhi = jet.phi()
                dR = calcDR( jEta, jPhi, tEta, tPhi )
                jetDRAndPt.append( ( dR, jet.pt() ) )
            #print jetDRAndPt
            jetDRAndPt.sort()
            #print jetDRAndPt
            #print "Closest DR: %f   JPt: %f" % (jetDRAndPt[0][0], jetDRAndPt[0][1])
            tally['t%iJetDR' % cnt] = jetDRAndPt[0][0]
            tally['t%iJetPt' % cnt] = jetDRAndPt[0][1]
            
    
        # Jets (standard AK4)
        tally['numJets10'] = 0
        tally['numJets20'] = 0
        cnt = 0
        for i,j in enumerate(jets.product()):
            if j.pt() < 10: continue
            if abs( j.eta() ) > 2.5: continue
            tally['numJets10'] += 1
            if j.pt() > 20: continue
            cnt += 1
            tally['numJets20'] += 1
            jPt = j.pt()
            jEta = j.eta()
            jPhi = j.phi()
            tally['j%iPt' % cnt] = jPt
            tally['j%iEta' % cnt] = jEta
            tally['j%iPhi' % cnt] = jPhi
    
    
    
    
        for key in varMap.keys() :
            vals[key][0] = tally[ varMap[key] ]
    
    
        tTree.Fill()
        #if iev > 9998: break
    tDir.cd()
    tTree.Write()
    tFile.Close() 
    
    
    
if __name__ == '__main__' :    
    mpCount = 0
    targetRun = 259721
    targetLumis = [322,335,]
    targetFile = '/data/Run2015D/JetHT/MINIAOD/PromptReco-v4/000/259/721/00000/FEB5B9FA-1B7B-E511-8791-02163E011B09.root'
    tauAnalyzer( mpCount, targetRun, targetLumis, targetFile )
