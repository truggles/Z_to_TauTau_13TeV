
def tauAnalyzer( mpCount, targetRun, targetLumis, targetFile, maxEvents ) :
    print "TAU ANALYZER CALLED:"
    print "Count: %i    targetRun %i targetFile %s" % (mpCount, targetRun, targetFile)
    
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
    triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT")
    
    import math
    dRCut = 0.4
    def calcDR( eta1, phi1, eta2, phi2 ) :
        return float(math.sqrt( (eta1-eta2)*(eta1-eta2) + (phi1-phi2)*(phi1-phi2) ))
    
    # open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
    #events = Events("root://eoscms//eos/cms/store/relval/CMSSW_7_4_1/RelValTTbar_13/MINIAODSIM/PU25ns_MCRUN2_74_V9_gensim71X-v1/00000/72C84BA7-F9EC-E411-B875-002618FDA210.root")
    # didn't work! events = Events("edmFileUtil -d /store/data/Run2015D/JetHT/MINIAOD/PromptReco-v4/000/259/721/00000/FEB5B9FA-1B7B-E511-8791-02163E011B09.root")
    #events = Events("root://eoscms//eos/cms/store/data/Run2015D/JetHT/MINIAOD/PromptReco-v4/000/259/721/00000/FEB5B9FA-1B7B-E511-8791-02163E011B09.root")
    events = Events("root://eoscms//eos/cms%s" % targetFile)
    #events = Events("/afs/cern.ch/work/t/truggles/Z_to_tautau/sync_mcRun2.root")
    #events = Events("/afs/cern.ch/work/t/truggles/Z_to_tautau/JetHT.root")
    
    #tFile = ROOT.TFile('study.root','RECREATE')
    ''' Store root files in separate folders by Run '''
    import os
    if not os.path.exists( '%i' % targetRun ):
        os.makedirs( '%i' % targetRun )
    tFile = ROOT.TFile('%i/%i_%i_%s.root' % (targetRun, targetRun, mpCount, targetFile.split('/')[-1].split('.')[0]),'RECREATE')
    #tFile = ROOT.TFile('tmp.root','RECREATE')
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
    varMap[6] = 'numTausThreeProngIsoPass'
    varMap[7] = 'numTausThreeProng30'
    varMap[8] = 'numJets20'
    varMap[9] = 'numJets30'
    varMap[10] = 'numJets30Clean'
    varMap[11] = 'nvtxCleaned'
    varMap[12] = 'orbitNumber'
    varMap[13] = 'bunchCrossing'
    varMap[14] = 'numTausThreeProng30IsoPass'
    varMap[15] = 'numTausThreeProng30IsoChrgPass'
    varMap[16] = 'PFJet450Pass'
    
    # Add Jets to tree
    count = 0
    for i in range(1, 43, 6):
        count += 1
        varMap[19+i] = 'j%iPt' % count
        varMap[19+i+1] = 'j%iEta' % count
        varMap[19+i+2] = 'j%iPhi' % count
        varMap[19+i+3] = 'j%iLooseID' % count
        varMap[19+i+4] = 'j%iPUdisc' % count
        varMap[19+i+5] = 'j%iPassPU' % count

    
    # Add Taus to tree
    # Only keey 3 prong taus!!!
    count = 0
    for i in range(1, 36, 7):
        count += 1
        varMap[150+i] = 't%iPt' % count
        varMap[150+i+1] = 't%iEta' % count
        varMap[150+i+2] = 't%iPhi' % count
        varMap[150+i+3] = 't%iJetDR' % count
        varMap[150+i+4] = 't%iJetPt' % count
        varMap[150+i+5] = 't%iIso' % count
        varMap[150+i+6] = 't%iIsoChrg' % count
        
    
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
    #print "targetLumis : ",targetLumis
    for iev,event in enumerate(events):
        if iev > maxEvents: break
        event.getByLabel(tauLabel, taus) 
        event.getByLabel(vertexLabel, vertices)
        event.getByLabel(vertexLabel, verticesScore)
        event.getByLabel(jetLabel, jets)
        event.getByLabel(triggerBitLabel, triggerBits)
    
        for key in tally.keys() :
            tally[ key ] = -10
    
        if iev % 10000 == 0 :
            print "Run: %i   Count: %i" % (targetRun, mpCount)
            print " --- iev: %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
        # Check if this evt is in the Run and Good Lumis we want
        tally['run'] = event.eventAuxiliary().run()
        if targetRun != tally['run'] : continue
        tally['lumi'] = event.eventAuxiliary().luminosityBlock()
        if tally['lumi'] not in targetLumis : continue

        tally['evt'] = event.eventAuxiliary().event()
        tally['orbitNumber'] = event.eventAuxiliary().orbitNumber()
        tally['bunchCrossing'] = event.eventAuxiliary().bunchCrossing()

        # log the lowest un-prescaled HLT trigger for these 4 runs
        trignames = event.object().triggerNames(triggerBits.product())
        for i in xrange(triggerBits.product().size()):
            #if triggerBits.product().accept(i) : print "PASS trigger: %s" % trignames.triggerName(i) 
            #if 'HLT_PFJet450' in trignames.triggerName(i) : print "%s %s" % (trignames.triggerName(i), triggerBits.product().accept(i) )
            if 'HLT_PFJet450' in trignames.triggerName(i) :
                if triggerBits.product().accept(i) : tally['PFJet450Pass'] = 1
                else : tally['PFJet450Pass'] = 0
    
        # Vertices
        tally['nvtx'] = 0
        tally['nvtxCleaned'] = 0
        if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
            #print "Event has no good primary vertex."
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
        tally['numTausThreeProngIsoPass'] = 0
        tally['numTausThreeProng30'] = 0
        tally['numTausThreeProng30IsoPass'] = 0
        tally['numTausThreeProng30IsoChrgPass'] = 0
        cnt = 0
        for i,tau in enumerate(taus.product()):
            if tau.pt() < 20: continue
            if abs( tau.eta() ) > 2.5: continue
            tally['numTaus'] += 1
            if tau.decayMode() != 10: continue
            tally['numTausThreeProng'] += 1
            if tau.pt() < 30 : continue
            cnt += 1
            tally['numTausThreeProng30'] += 1
            tally['t%iPt' % cnt] = tau.pt()
            tEta = tau.eta()
            tPhi = tau.phi()
            tIso = tau.tauID('byCombinedIsolationDeltaBetaCorrRaw3Hits')
            tIsoChrg = tau.tauID('chargedIsoPtSum')
            #print "tIso: ",tIso
            #if tIso < 1.5 : print "Not FAKE! Iso: ",tIso
            if tIso < 1.5 :
                tally['numTausThreeProngIsoPass'] += 1 
                tally['numTausThreeProng30IsoPass'] += 1 
            if tIsoChrg < 2 :
                tally['numTausThreeProng30IsoChrgPass'] += 1 
                
            tally['t%iEta' % cnt] = tEta
            tally['t%iPhi' % cnt] = tPhi
            tally['t%iIso' % cnt] = tIso
            tally['t%iIsoChrg' % cnt] = tIsoChrg

            # Find the JetPt and dR of our matching Jet
            jetDRAndPt = []
            for k,jet in enumerate(jets.product()) :
                if jet.pt() < 30: continue
                if abs( jet.eta() ) > 3: continue
                jEta = jet.eta()
                jPhi = jet.phi()
                dR = calcDR( jEta, jPhi, tEta, tPhi )
                jetDRAndPt.append( ( dR, jet.pt() ) )
            #print jetDRAndPt
            jetDRAndPt.sort()
            #print jetDRAndPt
            #print "Closest DR: %f   JPt: %f" % (jetDRAndPt[0][0], jetDRAndPt[0][1])
            #if len( jetDRAndPt[0] ) > 1 :
            try :
                tally['t%iJetDR' % cnt] = jetDRAndPt[0][0]
                tally['t%iJetPt' % cnt] = jetDRAndPt[0][1]
            except :
                print "No Jets were found.  Len jetDRAndPt = %i" % len( jetDRAndPt )
    
        # Jets (standard AK4)
        tally['numJets20'] = 0
        tally['numJets30'] = 0
        tally['numJets30Clean'] = 0
        cnt = 0
        for i,j in enumerate(jets.product()):
            if j.pt() < 20: continue
            if abs( j.eta() ) > 2.5: continue
            tally['numJets20'] += 1
            if j.pt() < 30: continue
            cnt += 1
            tally['numJets30'] += 1
            jPt = j.pt()
            jEta = j.eta()
            jPhi = j.phi()
            NHF = j.neutralHadronEnergyFraction()
            NEMF = j.neutralEmEnergyFraction()
            CHF = j.chargedHadronEnergyFraction()
            MUF = j.muonEnergyFraction()
            CEMF = j.chargedEmEnergyFraction()
            NumConst = j.chargedMultiplicity()+j.neutralMultiplicity()
            NumNeutralParticles = j.neutralMultiplicity()
            CHM = j.chargedMultiplicity()
            looseJetID = 0
            if ( NHF<0.99 and NEMF<0.99 and NumConst>1 ):
                if ((abs(jEta)<=2.4 and CHF>0 and CHM>0 and CEMF<0.99) or ( abs(jEta)>2.4 and abs(jEta)<=3.0 ) ): looseJetID = 1
            jPUval = j.userFloat("pileupJetId:fullDiscriminant")
            if jPUval <= -0.63 : jPassPU = 0
            else : jPassPU = 1
            
            tally['j%iPt' % cnt] = jPt
            tally['j%iEta' % cnt] = jEta
            tally['j%iPhi' % cnt] = jPhi
            tally['j%iLooseID' % cnt] = looseJetID
            tally['j%iPUdisc' % cnt] = jPUval
            tally['j%iPassPU' % cnt] = jPassPU
    
            if jPassPU>0 and looseJetID>0 :
                tally['numJets30Clean'] += 1
    
    
    
        for key in varMap.keys() :
            vals[key][0] = tally[ varMap[key] ]
    
    
        tTree.Fill()
    tDir.cd()
    tTree.Write()
    tFile.Close() 
    return( 'FINISHED', targetRun, mpCount )
    
    
    
if __name__ == '__main__' :    
    mpCount = 0
    targetRun = 259721
    targetLumis = [322,335,]
    #targetFile = '/store/data/Run2015D/JetHT/MINIAOD/PromptReco-v4/000/259/721/00000/FEB5B9FA-1B7B-E511-8791-02163E011B09.root'
    #targetFile = '/store/data/Run2015D/JetHT/MINIAOD/PromptReco-v4/000/259/721/00000/0406B003-1C7B-E511-AFD3-02163E0138BA.root'
    targetRun = 254833
    targetFile = '/store/data/Run2015C_50ns/JetHT/MINIAOD/05Oct2015-v1/50000/02D10C8B-896F-E511-A562-0026189438BA.root'
    maxEvents = 999999
    tauAnalyzer( mpCount, targetRun, targetLumis, targetFile, maxEvents )
