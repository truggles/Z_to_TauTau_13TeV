'''
A Class to interface with Electron Scale Factors:
https://twiki.cern.ch/twiki/bin/view/CMS/EgammaIDRecipesRun2#Electron_efficiencies_and_scale
Currently using WP90
Also, GSF SFs must be applied on top as well
'''


import ROOT

class ElectronSF :
    """A class to provide electron SFs for
    Isolation, ID and Trigger (not using trigger currenly)"""
    

    def __init__( self ):

        ### Load the ICHEP SFs provided by the Electron POG
        self.electronGSFFile = ROOT.TFile( 'data/2016Electron_GSF_EG2D.root', 'r' )
        self.gsfSF = self.electronGSFFile.Get( 'EGamma_SF2D' )

        self.electronWP80File = ROOT.TFile( 'data/2016Electron_WP80_EG2D.root', 'r' )
        self.wp80SF = self.electronWP80File.Get( 'EGamma_SF2D' )

        self.electronWP90File = ROOT.TFile( 'data/2016Electron_WP90_EG2D.root', 'r' )
        self.wp90SF = self.electronWP90File.Get( 'EGamma_SF2D' )



    def getGSFAndWPScaleFactor( self, wp, pt, eta ) :
        assert( wp in ['WP90', 'WP80', 'TrkOnly'] ), "Given WP (%s) is not supported" % wp
        #print wp
        # Make sure we stay on our histograms
        if pt > 199 : pt = 199
        elif pt < 20 : pt = 20
        if eta > 2.5 : eta = 2.5
        elif eta < -2.5 : eta = -2.5

        # GSF file cuts off at pt 25 GeV
        ptGSF = pt if pt > 26 else 26
        SF = self.gsfSF.GetBinContent( self.gsfSF.FindBin( eta, ptGSF ) )
        if wp == 'TrkOnly' : return SF
        if wp == 'WP90' :
            SF *= self.wp90SF.GetBinContent( self.wp90SF.FindBin( eta, pt ) )
            return SF
        elif wp == 'WP80' :
            SF *= self.wp80SF.GetBinContent( self.wp80SF.FindBin( eta, pt ) )
            return SF
        else :
            return SF


        

if __name__ == '__main__' :
    eSF = ElectronSF()
    print eSF.getGSFAndWPScaleFactor( 'WP80', 47.4, 1.9 )
    print eSF.getGSFAndWPScaleFactor( 'WP90', 47.4, 1.9 )
    print eSF.getGSFAndWPScaleFactor( 'WP80', 25, .7 )
    print eSF.getGSFAndWPScaleFactor( 'WP90', 25, .7 )
    print eSF.getGSFAndWPScaleFactor( 'TrkOnly', 25, .7 )
    print eSF.getGSFAndWPScaleFactor( 'TrkOnly', 25, .7 )



