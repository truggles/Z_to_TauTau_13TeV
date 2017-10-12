'''
A Class to interface with Electron Scale Factors provided by the HTT group:
https://github.com/CMS-HTT/LeptonEff-interface/blob/master/instructions.txt
https://github.com/CMS-HTT/LeptonEfficiencies/tree/master/Electron

This is just to apply the MVA ID and Isolation WP SFs
'''


import ROOT

class ElectronSFhtt :
    """A class to provide electron SFs provided by HTT group for
    Isolation and ID"""
    

    def __init__( self, wp ):

        assert( wp in ['IdIso0p10', 'IdIso0p15'] ), "Given WP (%s) is not supported" % wp

        ### Load the SF Files provided by HTT
        base = 'data/LeptonEfficiencies/Electron/Run2016BtoH/'
        if wp == 'IdIso0p10' :
            self.elecSFFile = ROOT.TFile( base+'Electron_IdIso_IsoLt0p1_eff.root', 'r' )
        if wp == 'IdIso0p15' :
            self.elecSFFile = ROOT.TFile( base+'Electron_IdIso_IsoLt0p15_eff.root', 'r' )
        self.mcBarrel = self.elecSFFile.Get( 'ZMassEtaLt1p48_MC' )
        self.mcMid = self.elecSFFile.Get( 'ZMassEta1p48to2p1_MC' )
        self.mcEndcap = self.elecSFFile.Get( 'ZMassEtaGt2p1_MC' )
        self.dataBarrel = self.elecSFFile.Get( 'ZMassEtaLt1p48_Data' )
        self.dataMid = self.elecSFFile.Get( 'ZMassEta1p48to2p1_Data' )
        self.dataEndcap = self.elecSFFile.Get( 'ZMassEtaGt2p1_Data' )


    def getIDAndIsoScaleFactor( self, pt, eta ) :
        #print wp
        # Make sure we stay on our histograms
        if pt > 99 : pt = 99
        elif pt < 11 : pt = 11
        absEta = abs(eta)

        if absEta <= 1.48 :
            return self.dataBarrel.Eval( pt ) / self.mcBarrel.Eval( pt )
        elif absEta <= 2.1 :
            return self.dataMid.Eval( pt ) / self.mcMid.Eval( pt )
        else :
            return self.dataEndcap.Eval( pt ) / self.mcEndcap.Eval( pt )


        

if __name__ == '__main__' :
    eSF = ElectronSFhtt('IdIso0p10')
    print eSF.getIDAndIsoScaleFactor( 47.4, 1.9 )
    print eSF.getIDAndIsoScaleFactor( 25, .7 )
    del eSF
    eSF = ElectronSFhtt('IdIso0p15')
    print eSF.getIDAndIsoScaleFactor( 47.4, 1.9 )
    print eSF.getIDAndIsoScaleFactor( 25, .7 )



