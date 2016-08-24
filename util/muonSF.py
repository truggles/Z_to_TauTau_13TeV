'''
A Class to interface with Muon Scale Factors:
https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults#Results_on_7_6_fb
Currently using PF ID Loose and Medium WPs
'''


import ROOT
from util.helpers import getTH1FfromTGraphAsymmErrors

class MuonSF :
    """A class to provide muon SFs for
    Isolation, ID and Trigger (not using trigger currenly)"""
    

    def __init__( self ):

        ### Load the ICHEP SFs provided by the Muon POG
        self.muonIDFile = ROOT.TFile( 'data/MuonID_Z_RunBCD_prompt80X_7p65.root', 'r' )
        self.ID_L_eta = self.muonIDFile.Get( 'MC_NUM_LooseID_DEN_genTracks_PAR_eta/eta_ratio' )
        self.ID_L_pt = self.muonIDFile.Get( 'MC_NUM_LooseID_DEN_genTracks_PAR_pt_alleta_bin1/pt_ratio' )
        self.ID_L_vtx = self.muonIDFile.Get( 'MC_NUM_LooseID_DEN_genTracks_PAR_pt_vtx/tag_nVertices_ratio' )
        self.ID_M_eta = self.muonIDFile.Get( 'MC_NUM_MediumID_DEN_genTracks_PAR_eta/eta_ratio' )
        self.ID_M_pt = self.muonIDFile.Get( 'MC_NUM_MediumID_DEN_genTracks_PAR_pt_alleta_bin1/pt_ratio' )
        self.ID_M_vtx = self.muonIDFile.Get( 'MC_NUM_MediumID_DEN_genTracks_PAR_pt_vtx/tag_nVertices_ratio' )



        self.muonIsoFile = ROOT.TFile( 'data/MuonIso_Z_RunBCD_prompt80X_7p65.root', 'r' )
        self.RelIso_L_eta = self.muonIsoFile.Get( 'MC_NUM_LooseRelIso_DEN_TightID_PAR_eta/eta_ratio' )
        self.RelIso_L_pt = self.muonIsoFile.Get( 'MC_NUM_LooseRelIso_DEN_TightID_PAR_pt_alleta_bin1/pt_ratio' )
        self.RelIso_L_vtx = self.muonIsoFile.Get( 'MC_NUM_LooseRelIso_DEN_TightID_PAR_vtx/tag_nVertices_ratio' )
        self.RelIso_T_eta = self.muonIsoFile.Get( 'MC_NUM_TightRelIso_DEN_TightID_PAR_eta/eta_ratio' )
        self.RelIso_T_pt = self.muonIsoFile.Get( 'MC_NUM_TightRelIso_DEN_TightID_PAR_pt_alleta_bin1/pt_ratio' )
        self.RelIso_T_vtx = self.muonIsoFile.Get( 'MC_NUM_TightRelIso_DEN_TightID_PAR_vtx/tag_nVertices_ratio' )



        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffsRun2#Tracking_efficiency_provided_by
        self.muonTkFile = ROOT.TFile( 'data/2016_Tk_POG_Muon_Ratios.root', 'r' )
        Tk_eta_Asym = self.muonTkFile.Get( 'ratio_eta' )
        Tk_vtx_Asym = self.muonTkFile.Get( 'ratio_vtx' )
        self.Tk_eta = getTH1FfromTGraphAsymmErrors( Tk_eta_Asym, 'ratio_etaH' )
        self.Tk_vtx = getTH1FfromTGraphAsymmErrors( Tk_vtx_Asym, 'ratio_vtxH' )
        
        


    def getRelIsoScaleFactor( self, Iso, pt, eta, vtx ) :
        #print "Iso",Iso
        SF = 1.
        # Make sure we stay on our histograms
        if pt > 199 : pt = 199
        elif pt < 20 : pt = 20
        if vtx > 30 : vtx = 30
        if Iso == 'Loose' :
            SF = self.RelIso_L_eta.GetBinContent( self.RelIso_L_eta.FindBin( eta ) )
            SF *= self.RelIso_L_pt.GetBinContent( self.RelIso_L_pt.FindBin( pt ) )
            SF *= self.RelIso_L_vtx.GetBinContent( self.RelIso_L_vtx.FindBin( vtx ) )
            return SF
        elif Iso == 'Tight' :
            SF = self.RelIso_T_eta.GetBinContent( self.RelIso_T_eta.FindBin( eta ) )
            SF *= self.RelIso_T_pt.GetBinContent( self.RelIso_T_pt.FindBin( pt ) )
            SF *= self.RelIso_T_vtx.GetBinContent( self.RelIso_T_vtx.FindBin( vtx ) )
            return SF
        else :
            return SF


    def getIDScaleFactor( self, ID, pt, eta, vtx ) :
        #print "ID",ID
        SF = 1.
        # Make sure we stay on our histograms
        if pt > 199 : pt = 199
        elif pt < 20 : pt = 20
        if vtx > 30 : vtx = 30
        if ID == 'Loose' :
            SF = self.ID_L_eta.GetBinContent( self.ID_L_eta.FindBin( eta ) )
            SF *= self.ID_L_pt.GetBinContent( self.ID_L_pt.FindBin( pt ) )
            SF *= self.ID_L_vtx.GetBinContent( self.ID_L_vtx.FindBin( vtx ) )
            return SF
        elif ID == 'Medium' :
            SF = self.ID_M_eta.GetBinContent( self.ID_M_eta.FindBin( eta ) )
            SF *= self.ID_M_pt.GetBinContent( self.ID_M_pt.FindBin( pt ) )
            SF *= self.ID_M_vtx.GetBinContent( self.ID_M_vtx.FindBin( vtx ) )
            return SF
        else :
            return SF


    def getTkScaleFactor( self, eta, vtx ) :
        #print "Tk",Tk
        SF = 1.
        # Make sure we stay on our histograms
        if eta > 2.39 : eta = 2.39
        elif eta < -2.39 : eta = -2.39
        if vtx > 32 : vtx = 32
        elif vtx < 1 : vtx = 1
        SF = self.Tk_eta.GetBinContent( self.Tk_eta.FindBin( eta ) )
        SF *= self.Tk_vtx.GetBinContent( self.Tk_vtx.FindBin( vtx ) )
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
    print mSF.getRelIsoScaleFactor( 'Loose', 27.69, 2.01, 33.66
 )



