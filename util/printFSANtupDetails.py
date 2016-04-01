import ROOT

def printMets( chan ) :
    """ FSA """
    f = ROOT.TFile('/afs/cern.ch/work/t/truggles/Z_to_tautau/mar24/CMSSW_7_6_3_patch2/src/FinalStateAnalysis/NtupleTools/test/ntup130.root','r')
    #f = ROOT.TFile('Sync2Mar31b/Sync-HtoTT_0_%s.root' % chan,'r')
    #XXX f = ROOT.TFile('Sync2April1bIsoOrder/Sync-HtoTT_0_%s.root' % chan,'r')
    #XXX f = ROOT.TFile('Sync2April1a/Sync-HtoTT_0_%s.root' % chan,'r')
    #f = ROOT.TFile('svFitTester.root','r')
    #t = f.Get('%s/final/Ntuple' % chan)
    t = f.Get('Ntuple')
    print t
    
    uw =set()
    uw2 = {}
    for row in t :
        evt = int(row.evt)
        lumi = int(row.lumi)
        run = int(row.run)
#        genPx = round(row.genPx,6)
#        genPy = round(row.genPy,6)
#        visPx = round(row.visPx,6)
#        visPy = round(row.visPy,6)
        if chan == 'tt' :
            mvamet = round(row.t1_t2_MvaMet,6)
            mvametphi = round(row.t1_t2_MvaMetPhi,6)
        if chan == 'em' :
            mvamet = round(row.e_m_MvaMet,6)
            mvametphi = round(row.e_m_MvaMetPhi,6)
        #print evt,":",lumi,":",run,":",mvamet,":",mvametphi
        uw.add( (run, lumi, evt) )
        uw2[(run, lumi, evt)] = (mvamet, mvametphi)
#        uw2[(run, lumi, evt)] = (mvamet, mvametphi, genPx, genPy, visPx, visPy)
        if evt == 179379 : print "UW: ",mvamet, mvametphi
    
    """ Imperial """
    #f = ROOT.TFile('/afs/cern.ch/user/t/truggles/syncFile/SYNCFILE_SUSYGluGluToHToTauTau_M-160_%s_fall15.root' % chan,'r')
    f = ROOT.TFile('/afs/cern.ch/work/t/truggles/Z_to_tautau/CMSSW_7_6_3_patch2/src/2015-sync/imp_%s_new.root' % chan,'r')
    t = f.Get('TauCheck')
    
    imp = set()
    imp2 = {}
    for row in t :
        evt = int(row.evt)
        lumi = int(row.lumi)
        run = int(row.run)
        mvamet = round(row.mvamet,6)
        mvametphi = round(row.mvametphi,6)
        genPx = round(row.genpX,6)
        genPy = round(row.genpY,6)
        visPx = round(row.vispX,6)
        visPy = round(row.vispY,6)
        #print evt,":",lumi,":",run,":",mvamet,":",mvametphi
        imp.add( (run, lumi, evt) )
#        imp2[(run, lumi, evt)] = (mvamet, mvametphi, genPx, genPy, visPx, visPy)
        imp2[(run, lumi, evt)] = (mvamet, mvametphi)
        if evt == 179379 : print "IC: ",mvamet, mvametphi
    
    print "Len UW:",len(uw)
    print "Len Imp:",len(imp)
    
    match = 0
    noMatch = 0
    for item in uw :
        if item in imp :
            if uw2[item] == imp2[item] : match += 1
            else : 
                noMatch += 1
#                print item
#                print " - UW ", uw2[item]
#                print " - Imp ", imp2[item]
    print "Matching:",match
    print "No Match:",noMatch

if __name__ == '__main__' :
    for chan in ['tt', 'em'] :
        print chan
        printMets( chan )
