import ROOT
from math import sqrt

ifile = ROOT.TFile('ntuplize20.root', 'r')
#ifile = ROOT.TFile('../SyncBaseRootsQuick/Sync_HtoTT.root', 'r')
idir = ifile.Get('mm/final')
#idir = ifile.Get('tt')
tree = idir.Get('Ntuple')

def deltaR( eta1, phi1, eta2, phi2 ) :
    dR = sqrt( (eta1 - eta2)*(eta1 - eta2) + (phi1 - phi2)*(phi1 - phi2) )
    return dR

#for row in tree :
#    dR = deltaR( row.eEta, row.ePhi, row.jet1Eta, row.jet1Phi )
#    #print "%i Elec & Jet1 dR: %f" % (row.evt, deltaR( row.eEta, row.ePhi, row.mEta, row.mPhi ))
#    if dR < 1:
#        #print "%i Elec & Mu dR: %f" % (row.evt, deltaR( row.eEta, row.ePhi, row.mEta, row.mPhi ))
#        print "%i Elec & Jet1 dR: %f" % (row.evt, dR)

for row in tree :
    if row.singleMuPass == 0: continue
    #dz1 = abs( row.pvZ - row.t1ZVertex )
    #dz2 = abs( row.pvZ - row.t2ZVertex )
    #print "t1 zv: %f        t2 zv: %f" % (dz1, dz2)
    #print "pvZ: %f, t1z %f, t2Z %f" % (row.pvZ, row.t1ZVertex, row.t2ZVertex)
    #print "pvZ: %f, t1zv %f, t1PVDZ %f" % (row.pvZ, row.t1ZVertex, row.t1ZTT_PVDZ)
    print "SingleMu - pass: %i,  m1:  %i,  m2:  %i" % (row.singleMuPass, row.m1MatchesSingleMu, row.m2MatchesSingleMu)
    print "m1Eta: %4.2f m1Phi %4.2f m1Pt %4.2f m2Eta %4.2f m2Phi %4.2f m2Pt %4.2f" % (row.m1Eta, row.m1Phi, row.m1Pt, row.m2Eta, row.m2Phi, row.m2Pt)
    print "\n"
