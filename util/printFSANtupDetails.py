import ROOT

def printMets( chan ) :
    """ FSA """
    #f = ROOT.TFile('/afs/cern.ch/work/t/truggles/Z_to_tautau/UWAnalysisCMSSW/CMSSW_7_6_3/src/UWAnalysis/testSVFitFarmOut/svf1.root','r')
    #XXX f = ROOT.TFile('/afs/cern.ch/work/t/truggles/Z_to_tautau/UWAnalysisCMSSW/CMSSW_7_6_3/src/UWAnalysis/svf1.root','r')
    #f = ROOT.TFile('Sync2Mar31b/Sync-HtoTT_0_%s.root' % chan,'r')
    f = ROOT.TFile('Sync2April04a_svFitVerify/Sync-HtoTT_0_%s.root' % chan,'r')
    #XXX f = ROOT.TFile('Sync2April1a/Sync-HtoTT_0_%s.root' % chan,'r')
    #f = ROOT.TFile('svFitTester.root','r')
    #t = f.Get('%s/final/Ntuple' % chan)
    t = f.Get('Ntuple')
    #t = f.Get('tt/Ntuple')
    print t
    
    uw =set()
    uw2 = {}
    for row in t :
        evt = int(row.evt)
        lumi = int(row.lumi)
        run = int(row.run)
        genPx = round(row.genpX,4)
        genPy = round(row.genpY,4)
        visPx = round(row.vispX,4)
        visPy = round(row.vispY,4)
        #njets = int(row.jetVeto30RecoilZTT)
        m_sv = round(row.m_sv,2)
        #pt1 = round(row.t1Pt,6)
        #pt2 = round(row.t2Pt,6)
        njets = int(row.njets)
        pt1 = round(row.pt_1,6)
        pt2 = round(row.pt_2,6)
        #if evt in [475952, 253925, 37279, 260429] :
        #    print "event",evt
        #    print "pt1",row.t1Pt
        #    print "pt2",row.t2Pt
        #    print "\n"
        #if chan == 'tt' :
        #    mvamet = round(row.t1_t2_MvaMet,4)
        #    mvametphi = round(row.t1_t2_MvaMetPhi,4)
        #if chan == 'em' :
        #    mvamet = round(row.e_m_MvaMet,4)
        #    mvametphi = round(row.e_m_MvaMetPhi,4)
        mvamet = round(row.mvamet,2)
        mvametphi = round(row.mvametphi,3)
        #print evt,":",lumi,":",run,":",mvamet,":",mvametphi
        uw.add( (run, lumi, evt) )
#        uw2[(run, lumi, evt)] = (mvamet, mvametphi)
        #uw2[(run, lumi, evt)] = (njets, genPx, genPy, visPx, visPy)
        uw2[(run, lumi, evt)] = (njets, pt1, pt2, genPx, genPy, visPx, visPy, mvamet, mvametphi, m_sv)
        #uw2[(run, lumi, evt)] = (njets, mvamet, mvametphi, m_sv)
        #uw2[(run, lumi, evt)] = (njets, genPx, genPy, visPx, visPy, mvamet, m_sv)
        if evt == 179379 : print "UW: ",mvamet, mvametphi
    
    """ Imperial """
    #f = ROOT.TFile('/afs/cern.ch/user/t/truggles/syncFile/SYNCFILE_SUSYGluGluToHToTauTau_M-160_%s_fall15.root' % chan,'r')
    f = ROOT.TFile('/afs/cern.ch/work/t/truggles/Z_to_tautau/checkMess/CMSSW_7_6_3/src/2015-sync/imp_%s_new.root' % chan,'r')
    t = f.Get('TauCheck')
    
    imp = set()
    imp2 = {}
    for row in t :
        evt = int(row.evt)
        lumi = int(row.lumi)
        run = int(row.run)
        mvamet = round(row.mvamet,2)
        mvametphi = round(row.mvametphi,3)
        m_sv = round(row.m_sv,2)
        genPx = round(row.genpX,4)
        genPy = round(row.genpY,4)
        visPx = round(row.vispX,4)
        visPy = round(row.vispY,4)
        njets = int(row.njets)
        pt1 = round(row.pt_1,6)
        pt2 = round(row.pt_2,6)
        #if evt in [475952, 253925, 37279, 260429] :
        #    print "EVENT",evt
        #    print "pt1",row.pt_1
        #    #print "eta1",row.eta_1
        #    #print "phi1",row.phi_1
        #    #print "mass1",row.m_1
        #    #print "decaymode1",row.tau_decay_mode_1
        #    print "pt2",row.pt_2
        #    #print "eta2",row.eta_2
        #    #print "phi2",row.phi_2
        #    #print "mass2",row.m_2
        #    #print "decaymode2",row.tau_decay_mode_2
        #    #print "cor mvamet",mvamet
        #    #print "cor mvametphi",mvametphi
        #    #print "genPx",genPx
        #    #print "genPy",genPy
        #    #print "visPy",visPy
        #    #print "visPx",visPx
        #    #print "njets",njets
        #    print "\n"
        #print evt,":",lumi,":",run,":",mvamet,":",mvametphi
        imp.add( (run, lumi, evt) )
        #imp2[(run, lumi, evt)] = (njets, genPx, genPy, visPx, visPy, mvamet, mvametphi, m_sv)
        imp2[(run, lumi, evt)] = (njets, pt1, pt2, genPx, genPy, visPx, visPy, mvamet, mvametphi, m_sv)
        #imp2[(run, lumi, evt)] = (njets, mvamet, mvametphi, m_sv)
        #imp2[(run, lumi, evt)] = (njets, genPx, genPy, visPx, visPy, mvamet, m_sv)
#        imp2[(run, lumi, evt)] = (mvamet, mvametphi)
    
    print "Len UW:",len(uw)
    print "Len Imp:",len(imp)
    
    match = 0
    noMatch = 0
    njetOff = 0
    ptDiff = 0
    for item in uw :
        #print "EVENT: ",item
        #print uw2[item]
        #if item in imp2.keys() :
        #    print imp2[item]
        if item in imp :
            if uw2[item] == imp2[item] : match += 1
            elif uw2[item][0] != imp2[item][0] : njetOff += 1
            elif uw2[item][1] != imp2[item][1] : ptDiff += 1
            elif uw2[item][2] != imp2[item][2] : ptDiff += 1
            else : 
                noMatch += 1
                print item
                print " - UW ", uw2[item]
                print " - Imp ", imp2[item]
    print "Matching:",match
    print "No Match:",noMatch
    print "NJet MisMatch:",njetOff
    print "Pt Diff MisMatch:",ptDiff

if __name__ == '__main__' :
    for chan in ['tt',]:# 'em'] :
        print chan
        printMets( chan )
