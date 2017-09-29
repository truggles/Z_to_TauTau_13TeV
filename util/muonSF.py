'''
A Class to interface with Muon Scale Factors:
https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults#Results_on_the_full_2016_data
Currently using PF ID Loose and Medium WPs

New addition is lumi based weighting for pre- and post-HIP fix
'''


import ROOT
from util.helpers import getTH1FfromTGraphAsymmErrors

class MuonSF :
    """A class to provide muon SFs for
    Isolation, ID and Trigger (not using trigger currenly)"""
    

    def __init__( self ):

    
        #self.bcdef = 27200.0
        #self.total = 35870.0
        #self.gh = self.total - self.bcdef
        # Lumis as ratios
        self.bcdef = 0.76
        self.gh = 0.24

        ### Load the ICHEP SFs provided by the Muon POG
        self.muonIDFile1 = ROOT.TFile( 'data/2016MuonEfficienciesAndSF_BCDEF_ID.root', 'r' )
        self.ID_L_eta1 = self.muonIDFile1.Get( 'MC_NUM_LooseID_DEN_genTracks_PAR_eta/eta_ratio' )
        self.ID_L_pt1 = self.muonIDFile1.Get( 'MC_NUM_LooseID_DEN_genTracks_PAR_pt/pt_ratio' )
        self.ID_L_vtx1 = self.muonIDFile1.Get( 'MC_NUM_LooseID_DEN_genTracks_PAR_vtx/tag_nVertices_ratio' )
        self.ID_M_eta1 = self.muonIDFile1.Get( 'MC_NUM_MediumID_DEN_genTracks_PAR_eta/eta_ratio' )
        self.ID_M_pt1 = self.muonIDFile1.Get( 'MC_NUM_MediumID_DEN_genTracks_PAR_pt/pt_ratio' )
        self.ID_M_vtx1 = self.muonIDFile1.Get( 'MC_NUM_MediumID_DEN_genTracks_PAR_vtx/tag_nVertices_ratio' )
        self.muonIDFile2 = ROOT.TFile( 'data/2016MuonEfficienciesAndSF_GH_ID.root', 'r' )
        self.ID_L_eta2 = self.muonIDFile2.Get( 'MC_NUM_LooseID_DEN_genTracks_PAR_eta/eta_ratio' )
        self.ID_L_pt2 = self.muonIDFile2.Get( 'MC_NUM_LooseID_DEN_genTracks_PAR_pt/pt_ratio' )
        self.ID_L_vtx2 = self.muonIDFile2.Get( 'MC_NUM_LooseID_DEN_genTracks_PAR_vtx/tag_nVertices_ratio' )
        self.ID_M_eta2 = self.muonIDFile2.Get( 'MC_NUM_MediumID_DEN_genTracks_PAR_eta/eta_ratio' )
        self.ID_M_pt2 = self.muonIDFile2.Get( 'MC_NUM_MediumID_DEN_genTracks_PAR_pt/pt_ratio' )
        self.ID_M_vtx2 = self.muonIDFile2.Get( 'MC_NUM_MediumID_DEN_genTracks_PAR_vtx/tag_nVertices_ratio' )



        self.muonIsoFile1 = ROOT.TFile( 'data/2016MuonEfficienciesAndSF_BCDEF_Iso.root', 'r' )
        self.RelIso_L_eta1 = self.muonIsoFile1.Get( 'LooseISO_LooseID_eta/eta_ratio' )
        self.RelIso_L_pt1 = self.muonIsoFile1.Get( 'LooseISO_LooseID_pt/pt_ratio' )
        self.RelIso_L_vtx1 = self.muonIsoFile1.Get( 'LooseISO_LooseID_vtx/tag_nVertices_ratio' )
        self.RelIso_T_eta1 = self.muonIsoFile1.Get( 'TightISO_TightID_eta/eta_ratio' )
        self.RelIso_T_pt1 = self.muonIsoFile1.Get( 'TightISO_TightID_pt/pt_ratio' )
        self.RelIso_T_vtx1 = self.muonIsoFile1.Get( 'TightISO_TightID_vtx/tag_nVertices_ratio' )
        self.muonIsoFile2 = ROOT.TFile( 'data/2016MuonEfficienciesAndSF_GH_Iso.root', 'r' )
        self.RelIso_L_eta2 = self.muonIsoFile2.Get( 'LooseISO_LooseID_eta/eta_ratio' )
        self.RelIso_L_pt2 = self.muonIsoFile2.Get( 'LooseISO_LooseID_pt/pt_ratio' )
        self.RelIso_L_vtx2 = self.muonIsoFile2.Get( 'LooseISO_LooseID_vtx/tag_nVertices_ratio' )
        self.RelIso_T_eta2 = self.muonIsoFile2.Get( 'TightISO_TightID_eta/eta_ratio' )
        self.RelIso_T_pt2 = self.muonIsoFile2.Get( 'TightISO_TightID_pt/pt_ratio' )
        self.RelIso_T_vtx2 = self.muonIsoFile2.Get( 'TightISO_TightID_vtx/tag_nVertices_ratio' )



        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffsRun2#Tracking_efficiency_provided_by
        self.muonTkFile = ROOT.TFile( 'data/2016MuonTracking_EfficienciesAndSF_BCDEFGH.root', 'r' )
        self.Tk_eta = self.muonTkFile.Get( 'ratio_eff_eta3_dr030e030_corr' )
        self.Tk_vtx = self.muonTkFile.Get( 'ratio_eff_vtx_dr030e030_corr' )
        
        


    def getRelIsoScaleFactor( self, Iso, pt, eta, vtx ) :
        #print "Iso",Iso
        SF = 1.
        # Make sure we stay on our histograms
        if pt > 199 : pt = 199
        elif pt < 20 : pt = 21
        if vtx > 50 : vtx = 50
        if Iso == 'Loose' :
            SF1 = self.RelIso_L_eta1.GetBinContent( self.RelIso_L_eta1.FindBin( eta ) )
            SF1 *= self.RelIso_L_pt1.GetBinContent( self.RelIso_L_pt1.FindBin( pt ) )
            SF1 *= self.RelIso_L_vtx1.GetBinContent( self.RelIso_L_vtx1.FindBin( vtx ) )
            SF1 *= self.bcdef
            SF2 = self.RelIso_L_eta2.GetBinContent( self.RelIso_L_eta2.FindBin( eta ) )
            SF2 *= self.RelIso_L_pt2.GetBinContent( self.RelIso_L_pt2.FindBin( pt ) )
            SF2 *= self.RelIso_L_vtx2.GetBinContent( self.RelIso_L_vtx2.FindBin( vtx ) )
            SF2 *= self.gh
            return SF1 + SF2
        elif Iso == 'Tight' :
            SF1 = self.RelIso_T_eta1.GetBinContent( self.RelIso_T_eta1.FindBin( eta ) )
            SF1 *= self.RelIso_T_pt1.GetBinContent( self.RelIso_T_pt1.FindBin( pt ) )
            SF1 *= self.RelIso_T_vtx1.GetBinContent( self.RelIso_T_vtx1.FindBin( vtx ) )
            SF1 *= self.bcdef
            SF2 = self.RelIso_T_eta2.GetBinContent( self.RelIso_T_eta2.FindBin( eta ) )
            SF2 *= self.RelIso_T_pt2.GetBinContent( self.RelIso_T_pt2.FindBin( pt ) )
            SF2 *= self.RelIso_T_vtx2.GetBinContent( self.RelIso_T_vtx2.FindBin( vtx ) )
            SF2 *= self.gh
            return SF1 + SF2
        else :
            return SF


    def getIDScaleFactor( self, ID, pt, eta, vtx ) :
        #print "ID",ID
        SF = 1.
        # Make sure we stay on our histograms
        if pt > 199 : pt = 199
        elif pt < 20 : pt = 21
        if vtx > 50 : vtx = 50
        if ID == 'Loose' :
            SF1 = self.ID_L_eta1.GetBinContent( self.ID_L_eta1.FindBin( eta ) )
            SF1 *= self.ID_L_pt1.GetBinContent( self.ID_L_pt1.FindBin( pt ) )
            SF1 *= self.ID_L_vtx1.GetBinContent( self.ID_L_vtx1.FindBin( vtx ) )
            SF1 *= self.bcdef
            SF2 = self.ID_L_eta2.GetBinContent( self.ID_L_eta2.FindBin( eta ) )
            SF2 *= self.ID_L_pt2.GetBinContent( self.ID_L_pt2.FindBin( pt ) )
            SF2 *= self.ID_L_vtx2.GetBinContent( self.ID_L_vtx2.FindBin( vtx ) )
            SF2 *= self.gh
            return SF1 + SF2
        elif ID == 'Medium' :
            SF1 = self.ID_M_eta1.GetBinContent( self.ID_M_eta1.FindBin( eta ) )
            SF1 *= self.ID_M_pt1.GetBinContent( self.ID_M_pt1.FindBin( pt ) )
            SF1 *= self.ID_M_vtx1.GetBinContent( self.ID_M_vtx1.FindBin( vtx ) )
            SF1 *= self.bcdef
            SF2 = self.ID_M_eta2.GetBinContent( self.ID_M_eta2.FindBin( eta ) )
            SF2 *= self.ID_M_pt2.GetBinContent( self.ID_M_pt2.FindBin( pt ) )
            SF2 *= self.ID_M_vtx2.GetBinContent( self.ID_M_vtx2.FindBin( vtx ) )
            SF2 *= self.gh
            return SF1 + SF2
        else :
            return SF


    def getTkScaleFactor( self, eta, vtx ) :
        #print "Tk",Tk
        SF = 1.
        # Make sure we stay on our histograms
        if eta > 2.39 : eta = 2.39
        elif eta < -2.39 : eta = -2.39
        if vtx > 45 : vtx = 45
        elif vtx < 1 : vtx = 1
        SF = self.Tk_eta.Eval( eta )
        SF *= self.Tk_vtx.Eval( vtx )
        return SF
        

if __name__ == '__main__' :
    mSF = MuonSF()
    #print mSF.getIDScaleFactor( 'Loose', 47.4, 1.9, 18. )
    #print mSF.getIDScaleFactor( 'Medium', 47.4, 1.9, 18. )
    #print mSF.getRelIsoScaleFactor( 'Loose', 47.4, 1.9, 18. )
    #print mSF.getRelIsoScaleFactor( 'Loose', 47.4, 1.9, 21. )
    #print mSF.getRelIsoScaleFactor( 'Tight', 47.4, 1.9, 21. )
    #print mSF.getIDScaleFactor( 'Loose', 10.26, 2.13, 21.8 )
    #print mSF.getRelIsoScaleFactor( 'Loose', 10.26, 2.13, 21.8 )
    print mSF.getIDScaleFactor( 'Loose', 27.69, 2.01, 33.66 )
    print mSF.getRelIsoScaleFactor( 'Loose', 27.69, 2.01, 33.66 )
    print mSF.getTkScaleFactor( 1.8, 23 )



