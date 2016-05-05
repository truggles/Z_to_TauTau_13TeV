import ROOT

def printMets( chan ) :
    """ FSA """
    f = ROOT.TFile('Sync2April03d/Sync-HtoTT_0_tt.root','r')
    #f = ROOT.TFile('Sync2Mar31b/Sync-HtoTT_0_%s.root' % chan,'r')
    #XXX f = ROOT.TFile('Sync2April1bIsoOrder/Sync-HtoTT_0_%s.root' % chan,'r')
    #XXX f = ROOT.TFile('Sync2April1a/Sync-HtoTT_0_%s.root' % chan,'r')
    #f = ROOT.TFile('svFitTester.root','r')
    #t = f.Get('%s/final/Ntuple' % chan)
    #t = f.Get('Ntuple')
    t = f.Get('Ntuple')
    print t
    evts = [431049, 472682, 442134, 445321, 455729, 12759, 343429, 234311, 143590, 143882, 164255, 181356, 236476, 256972, 243573, 7648, 409614, 52935, 77829, 77839, 282295, 280601, 280798, 470347, 57358, 103790, 113459, 114069, 119137, 137236, 138226, 163516, 158257, 162668, 55962, 302440, 385093, 40655, 444352, 444761, 231449, 267734, 267740, 272159, 53225, 56957, 185677, 417440, 417706, 414726, 71847, 91908, 121000, 144123, 156305, 153776, 430205, 446507, 406693, 65211, 70008, 220434, 76914, 38254, 59732, 87719, 178316, 184624, 213339, 141883, 157194, 170417, 190755, 191775, 189042, 179591, 256193, 291882, 293447, 189688, 219422, 219529, 210191, 233025, 413874, 396447, 484936, 454611, 422534, 495314, 106400, 285689, 338367, 365721, 365799, 391486, 395161, 375184, 433488, 467478, 471046, 156766, 42566, 25781, 52343, 52505, 240816, 241355, 476640, 478840, 230684, 230997, 272371, 344148, 344526, 489059, 407418, 216165, 217092, 217139, 105382, 496630, 391094]
    
    cnt = 0
    for row in t :
        evt = int(row.evt)
        if evt in evts :
            njets = int(row.jetVeto30RecoilZTT)
            extraE = int(row.extraelec_veto)
            extraM = int(row.extramuon_veto)
            antiE1 = int(row.againstElectronVLooseMVA6_1)
            antiE2 = int(row.againstElectronVLooseMVA6_2)
            antiM1 = int(row.againstMuonLoose3_1)
            antiM2 = int(row.againstMuonLoose3_2)
            vt1 = int(row.t1ByVTightIsolationMVArun2v1DBoldDMwLT)
            vt2 = int(row.t2ByVTightIsolationMVArun2v1DBoldDMwLT)
            print extraE, extraM, antiE1, antiE2, antiM1, antiM2, vt1, vt2
            if extraE > 0 or extraM > 0 or antiE1 < 1 or antiE2 < 1 or antiM1 < 1 or antiM2 <1 or vt1 < 1 or vt2 < 1 :
                cnt += 1

    print "Tally w/ extras: ",cnt
        

if __name__ == '__main__' :
    for chan in ['tt',]:# 'em'] :
        print chan
        printMets( chan )
