'''
A Class to apply Reducible Bkg factors
calculated from the 3L method by Jaana
'''


import ROOT

class ReducibleBkgWeights3L :
    """A class to provide Reducible Bkg weights for
    AZH/ZH analysis"""
    

    def __init__( self, channel, shift='Nominal' ):
        assert(channel in ['eemm','eeet','eett','eemt','eeem','emmt','mmtt',
            'mmmt','emmm','eeee','mmmm']), "Channel: %s does not have a \
            Reducible Bkg component." % channel
        assert( shift in ['Nominal', 'UP', 'DOWN'] ), "Selected shift %s is not \
            one of the supported shifts: Nominal, UP, DOWN" % shift
        self.channel = channel
        self.shift = shift
        self.file = ROOT.TFile('data/azhFakeRateFits_3L_Feb27.root','READ')
        self.app = 'leptonPt'

        # Set Leg3 FR hists
        if self.channel in ['eeet','eeem','emmt','emmm','eeee'] :
            self.frHistAllEtaL3 = self.file.Get( 'FR_ele_data' )
        elif self.channel in ['eemm','eemt','mmmt','mmmm'] :
            self.frHistAllEtaL3 = self.file.Get( 'FR_muon_data' )
        elif self.channel in ['eett','mmtt'] :
            self.frHistAllEtaL3Tau = self.file.Get( 'FR_tau_data' )

        # Set Leg4 FR hists
        if self.channel in ['eeet','emmt','eemt','mmmt',] :
            self.frHistAllEtaL4Tau = self.file.Get( 'FR_tau_data' )
        elif self.channel in ['eett','mmtt',] :
            self.frHistAllEtaL4Tau = self.file.Get( 'FR_tau_data' )
        elif self.channel in ['eeem','eemm','emmm','mmmm'] :
            self.frHistAllEtaL4 = self.file.Get( 'FR_muon_data' )
        elif self.channel in ['eeee',] :
            self.frHistAllEtaL4 = self.file.Get( 'FR_ele_data' )


    # Save some space with this
    def evalWeight( self, pt, absEta, hist, dm=-1 ) :
        if dm == -1 :
            val = hist.GetBinContent( hist.FindBin( pt, absEta ) )
        elif dm == 0 :
            val = hist.GetBinContent( hist.FindBin( pt, 0.1 ) )
        elif dm == 1 :
            val = hist.GetBinContent( hist.FindBin( pt, 1.5 ) )
        elif dm == 10 :
            val = hist.GetBinContent( hist.FindBin( pt, 10.5 ) )
        else : print "\n\n\n\nBAD NEWS!!!!!!"
        return val / ( 1. - val )



    # Retrieve values
    # For each of these calls, check if the lepton fails their associated
    # cuts.  If it fails, assign a FF value, if it pass -> 0
    def getFRWeightL3( self, pt, eta, lep, row ):
        if self.channel in ['eeet','eeem','emmt','emmm','eeee'] :
            if self.electronPasses( lep, row ) : return 0.
        elif self.channel in ['eemm','eemt','mmmt','mmmm'] :
            if self.muonPasses( lep, row ) : return 0.
        elif self.channel in ['eett','mmtt'] :
            if self.tauPasses( lep, row ) : return 0.
        
        if pt > 90 : pt = 89

        # Check if we should use the graph points instead of the fit
        # for elec and muon, fits end before out lowest threshold
        # Also make sure we stay on the lowest threshold for the graphs
        # SPLINE: if the pT is too high, Eval does spline extrapolation
        # off the end of the TGraph, so I am capping it at the center
        # of the final bin
        if 'e' in lep :
            if pt <= 10 : pt = 10.1
            if pt > 60 : pt = 59
        elif 'm' in lep :
            if pt <= 10 : pt = 10.1
            if pt > 60 : pt = 59

        if not 't' in lep :
            return self.evalWeight( pt, abs(eta), self.frHistAllEtaL3 )
        if 't' in lep :
            return self.evalWeight( pt, abs(eta), self.frHistAllEtaL3Tau, getattr( row, lep+'DecayMode' ) )
        return 0. # Default


    def getFRWeightL4( self, pt, eta, lep, row ):
        if self.channel in ['eett','mmtt','eeet','emmt','eemt','mmmt',] :
            if self.tauPasses( lep, row ) : return 0.
        elif self.channel in ['eeem','eemm','emmm','mmmm'] :
            if self.muonPasses( lep, row ) : return 0.
        elif self.channel in ['eeee',] :
            if self.electronPasses( lep, row ) : return 0.
        
        if pt > 90 : pt = 89

        # Check if we should use the graph points instead of the fit
        # for elec and muon, fits end before out lowest threshold
        # Also make sure we stay on the lowest threshold for the graphs
        if 'e' in lep :
            if pt <= 10 : pt = 10.1
            if pt > 60 : pt = 59
        elif 'm' in lep :
            if pt <= 10 : pt = 10.1
            if pt > 60 : pt = 59

        if not 't' in lep :
            return self.evalWeight( pt, abs(eta), self.frHistAllEtaL4 )
        if 't' in lep :
            return self.evalWeight( pt, abs(eta), self.frHistAllEtaL4Tau, getattr( row, lep+'DecayMode' ) )
        return 0. # Default

 
    # Check to see if e/m/t pass their cuts
    # and should be skipped   
    def electronPasses( self, lep, row ):
        if getattr( row, lep+'IsoDB03' ) < 0.15 and \
            getattr( row, lep+'MVANonTrigWP80' ) > 0.5 : return True
        else : return False

    def muonPasses( self, lep, row ):
        if getattr( row, lep+'IsoDB04' ) < 0.15 and \
            getattr( row, lep+'PFIDLoose' ) > 0.5 : return True
        else : return False

    def tauPasses( self, lep, row ):
        if getattr( row, lep+'ByMediumIsolationMVArun2v1DBoldDMwLT' ) > 0.5 : return True
        else : return False


