'''
A Class to apply Reducible Bkg factors
'''


import ROOT

class ReducibleBkgWeights :
    """A class to provide Reducible Bkg weights for
    AZH/ZH analysis"""
    

    def __init__( self, channel ):
        assert(channel in ['eemm','eeet','eett','eemt','eeem','emmt','mmtt',
            'mmmt','emmm','eeee','mmmm']), "Channel: %s does not have a \
            Reducible Bkg component." % channel
        self.channel = channel
        self.file = ROOT.TFile('data/azhFakeRateFits.root','READ')
        self.tauFitCut = 20.
        #self.electronFitCut = 15.
        self.electronFitCut = 250.
        self.muonFitCut = 12.5
        self.useFit = False
        self.app = 'leptonPt'

        # Set Leg3 FR graphs
        if self.channel in ['eeet','eeem','emmt','emmm','eeee'] :
            self.frGraphAllEtaL3 = self.file.Get( 'electron_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL3 = self.file.Get( 'electron_AllEta_'+self.app+'_fit' )
        elif self.channel in ['eemm','eemt','mmmt','mmmm'] :
            self.frGraphAllEtaL3 = self.file.Get( 'muon_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL3 = self.file.Get( 'muon_AllEta_'+self.app+'_fit' )
        elif self.channel in ['eett','mmtt'] :
            # DM0
            self.frGraphAllEtaL3dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL3dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_fit' )
            # DM1
            self.frGraphAllEtaL3dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL3dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_fit' )
            # DM10
            self.frGraphAllEtaL3dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL3dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_fit' )

        # Set Leg4 FR graphs
        if self.channel in ['eeet','emmt','eemt','mmmt',] :
            # DM0
            self.frGraphAllEtaL4dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL4dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_fit' )
            # DM1
            self.frGraphAllEtaL4dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL4dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_fit' )
            # DM10
            self.frGraphAllEtaL4dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL4dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_fit' )
        elif self.channel in ['eett','mmtt',] :
            # DM0
            self.frGraphAllEtaL4dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL4dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_fit' )
            # DM1
            self.frGraphAllEtaL4dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL4dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_fit' )
            # DM10
            self.frGraphAllEtaL4dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL4dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_fit' )
        elif self.channel in ['eeem','eemm','emmm','mmmm'] :
            self.frGraphAllEtaL4 = self.file.Get( 'muon_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL4 = self.file.Get( 'muon_AllEta_'+self.app+'_fit' )
        elif self.channel in ['eeee',] :
            self.frGraphAllEtaL4 = self.file.Get( 'electron_AllEta_'+self.app+'_graph' )
            self.frFitAllEtaL4 = self.file.Get( 'electron_AllEta_'+self.app+'_fit' )


    # Save some space with this
    def evalWeight( self, pt, absEta, fit, graph ) :
        if self.useFit :
            return fit.Eval( pt ) / ( 1. - fit.Eval( pt ) )
        else :
            return graph.Eval( pt ) / ( 1. - graph.Eval( pt ) )



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
        
        if pt > 100 : pt = 99

        # Check if we should use the graph points instead of the fit
        # for elec and muon, fits end before out lowest threshold
        # Also make sure we stay on the lowest threshold for the graphs
        # SPLINE: if the pT is too high, Eval does spline extrapolation
        # off the end of the TGraph, so I am capping it at the center
        # of the final bin
        if 'e' in lep :
            if pt <= 10 : pt = 10.1
            if pt > 70 : pt = 70
        elif 'm' in lep :
            if pt <= 10 : pt = 10.1
            if pt > 70 : pt = 70
        elif 't' in lep :
            if pt > 85 : pt = 85

        if not 't' in lep :
            return self.evalWeight( pt, abs(eta), self.frFitAllEtaL3, self.frGraphAllEtaL3 )
        if 't' in lep :
            if getattr( row, lep+'DecayMode' ) == 0 :
                return self.evalWeight( pt, abs(eta), self.frFitAllEtaL3dm0, self.frGraphAllEtaL3dm0 )
            if getattr( row, lep+'DecayMode' ) == 1 :
                return self.evalWeight( pt, abs(eta), self.frFitAllEtaL3dm1, self.frGraphAllEtaL3dm1 )
            if getattr( row, lep+'DecayMode' ) == 10 :
                return self.evalWeight( pt, abs(eta), self.frFitAllEtaL3dm10, self.frGraphAllEtaL3dm10 )
        return 0. # Default


    def getFRWeightL4( self, pt, eta, lep, row ):
        if self.channel in ['eett','mmtt','eeet','emmt','eemt','mmmt',] :
            if self.tauPasses( lep, row ) : return 0.
        elif self.channel in ['eeem','eemm','emmm','mmmm'] :
            if self.muonPasses( lep, row ) : return 0.
        elif self.channel in ['eeee',] :
            if self.electronPasses( lep, row ) : return 0.
        
        if pt > 100 : pt = 99

        # Check if we should use the graph points instead of the fit
        # for elec and muon, fits end before out lowest threshold
        # Also make sure we stay on the lowest threshold for the graphs
        if 'e' in lep :
            if pt <= 10 : pt = 10.1
        elif 'm' in lep :
            if pt <= 10 : pt = 10.1

        if not 't' in lep :
            return self.evalWeight( pt, abs(eta), self.frFitAllEtaL4, self.frGraphAllEtaL4 )
        if 't' in lep :
            if getattr( row, lep+'DecayMode' ) == 0 :
                return self.evalWeight( pt, abs(eta), self.frFitAllEtaL4dm0, self.frGraphAllEtaL4dm0 )
            if getattr( row, lep+'DecayMode' ) == 1 :
                return self.evalWeight( pt, abs(eta), self.frFitAllEtaL4dm1, self.frGraphAllEtaL4dm1 )
            if getattr( row, lep+'DecayMode' ) == 10 :
                return self.evalWeight( pt, abs(eta), self.frFitAllEtaL4dm10, self.frGraphAllEtaL4dm10 )
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


