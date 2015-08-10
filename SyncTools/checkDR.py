import ROOT
from math import sqrt

ifile = ROOT.TFile('ntuplize_3.root', 'r')
idir = ifile.Get('em/final')
tree = idir.Get('Ntuple')

def deltaR( eta1, phi1, eta2, phi2 ) :
    dR = sqrt( (eta1 - eta2)*(eta1 - eta2) + (phi1 - phi2)*(phi1 - phi2) )
    return dR

for row in tree :
    print "%i Elec & Jet1 dR: %f" % (row.evt, deltaR( row.eEta, row.ePhi, row.mEta, row.mPhi ))
