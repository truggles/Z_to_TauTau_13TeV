'''
A Class to add two additional Tau ID MVA run2v1 Iso WPs
This is based off of dR=0.5 and was provided by:
Christian Veelken christian.veelken@cern.ch, and
Arun Nayak aruna.nayak@cern.ch
'''


import ROOT

class IsoWPAdder :
    """A class to to two additional Tau Isolation WPs, VVLoose and VVTight
        DBoldDMwLT MVA run2v1 Iso"""
    

    def __init__(self):
        self.inFile = ROOT.TFile('data/wpDiscriminationByIsolationMVARun2v1_DBoldDMwLT.root','r')
        self.wpVVLoose = self.inFile.Get('DBoldDMwLTEff95')
        self.wpVLoose = self.inFile.Get('DBoldDMwLTEff90')
        self.wpVVTight = self.inFile.Get('DBoldDMwLTEff40')
        self.formula = self.inFile.Get('mvaOutput_normalization_DBoldDMwLT')

    def getFormula( self, x ) :
        return self.formula.Eval( x )

    def getVVLoose( self, isoRaw, pt ):
        # Make sure we stay on the TGraph
        # this could probably be tightened up on the low Pt side if we cared
        if pt > 1900 : pt = 1900
        if pt < 23 : pt = 23
        thresholdAtPt = self.wpVVLoose.Eval( pt )
        if self.formula.Eval( isoRaw ) > thresholdAtPt : return 1.0
        else : return 0.0

    # VLoose was used to confirm we match between miniAOD values and this
    # technique.  This was confirmed!
    def getVLoose( self, isoRaw, pt ):
        # Make sure we stay on the TGraph
        # this could probably be tightened up on the low Pt side if we cared
        if pt > 1900 : pt = 1900
        if pt < 23 : pt = 23
        thresholdAtPt = self.wpVLoose.Eval( pt )
        if self.formula.Eval( isoRaw ) > thresholdAtPt : return 1.0
        else : return 0.0

    def getVVTight( self, isoRaw, pt ):
        if pt > 1900 : pt = 1900
        if pt < 23 : pt = 23
        thresholdAtPt = self.wpVVTight.Eval( pt )
        if self.formula.Eval( isoRaw ) > thresholdAtPt : return 1.0
        else : return 0.0

    """ For reference: Christian's code for accessing the values
    //- before event loop
        edm::FileInPath tauIdMVArun2dR03DB_wpFilePath = edm::FileInPath("tthAnalysis/HiggsToTauTau/data/wpDiscriminationByIsolationMVARun2v1_DBdR03oldDMwLT.root");
        TFile* tauIdMVArun2dR03DB_wpFile = new TFile(tauIdMVArun2dR03DB_wpFilePath.fullPath().c_str());
        TGraph* DBdR03oldDMwLTEff95 = dynamic_cast<TGraph*>(gInstance->tauIdMVArun2dR03DB_wpFile_->Get("DBdR03oldDMwLTEff95"));
        TFormula* mvaOutput_normalization_DBdR03oldDMwLT = dynamic_cast<TFormula*>(gInstance->tauIdMVArun2dR03DB_wpFile_->Get("mvaOutput_normalization_DBdR03oldDMwLT"));
    
    //- in event loop
            if ( mvaOutput_normalization_DBdR03oldDMwLT->Eval(hadTau->rawMVA_dR03 > DBdR03oldDMwLTEff95->Eval(hadTau->pt) ) {
                    hadTau_idMVA_dR03 = 1;
            } else {
                    hadTau_idMVA_dR03 = 0;
    """



if __name__ == '__main__' :
    obj = IsoWPAdder()
    print obj.getVVLoose( 0.48, 1000 )
    print obj.getVVLoose( 0.42, 1000 )
    print obj.getVVTight( 0.48, 1000 )
    print obj.getFormula( 0.48 )
