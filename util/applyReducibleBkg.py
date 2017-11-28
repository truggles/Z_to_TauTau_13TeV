'''
A Class to apply Reducible Bkg factors
'''


import ROOT

class ReducibleBkgWeights :
    """A class to provide Reducible Bkg weights for
    AZH/ZH analysis"""
    

    #def __init__( self, channel, jetMatched ):
    def __init__( self, channel ):
        assert(channel in ['eemm','eeet','eett','eemt','eeem','emmt','mmtt',
            'mmmt','emmm','eeee','mmmm']), "Channel: %s does not have a \
            Reducible Bkg component." % channel
        self.channel = channel
        self.file = ROOT.TFile('data/azhFakeRateFits.root','READ')
        #self.jetMatched = jetMatched
        self.tauFitCut = 19.
        #self.electronFitCut = 15.
        self.electronFitCut = 9.
        self.muonFitCut = 9.
        self.app = 'leptonPt'
        #if self.jetMatched :
        #    self.app = 'jetMatch'
        #if not self.jetMatched :
        #    self.app = 'noJetMatch'

        # Set Leg3 FR graphs
        if self.channel in ['eeet','eeem','emmt','emmm','eeee'] :
            self.frGraphBarrelL3 = self.file.Get( 'electron_Barrel_'+self.app+'_graph' )
            self.frFitBarrelL3 = self.file.Get( 'electron_Barrel_'+self.app+'_fit' )
            self.frGraphEndcapL3 = self.file.Get( 'electron_Endcap_'+self.app+'_graph' )
            self.frFitEndcapL3 = self.file.Get( 'electron_Endcap_'+self.app+'_fit' )
        elif self.channel in ['eemm','eemt','mmmt','mmmm'] :
            self.frGraphBarrelL3 = self.file.Get( 'muon_Barrel_'+self.app+'_graph' )
            self.frFitBarrelL3 = self.file.Get( 'muon_Barrel_'+self.app+'_fit' )
            self.frGraphEndcapL3 = self.file.Get( 'muon_Endcap_'+self.app+'_graph' )
            self.frFitEndcapL3 = self.file.Get( 'muon_Endcap_'+self.app+'_fit' )
        elif self.channel in ['eett','mmtt'] :
            # DM0
            self.frGraphBarrelL3dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_graph' )
            self.frFitBarrelL3dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_fit' )
            self.frGraphEndcapL3dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_graph' )
            self.frFitEndcapL3dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_fit' )
            # DM1
            self.frGraphBarrelL3dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_graph' )
            self.frFitBarrelL3dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_fit' )
            self.frGraphEndcapL3dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_graph' )
            self.frFitEndcapL3dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_fit' )
            # DM10
            self.frGraphBarrelL3dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_graph' )
            self.frFitBarrelL3dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_fit' )
            self.frGraphEndcapL3dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_graph' )
            self.frFitEndcapL3dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_fit' )

        # Set Leg4 FR graphs
        if self.channel in ['eeet','emmt','eemt','mmmt',] :
            # DM0
            self.frGraphBarrelL4dm0 = self.file.Get( 'tau-DM0_lllt_AllEta_'+self.app+'_graph' )
            self.frFitBarrelL4dm0 = self.file.Get( 'tau-DM0_lllt_AllEta_'+self.app+'_fit' )
            self.frGraphEndcapL4dm0 = self.file.Get( 'tau-DM0_lllt_AllEta_'+self.app+'_graph' )
            self.frFitEndcapL4dm0 = self.file.Get( 'tau-DM0_lllt_AllEta_'+self.app+'_fit' )
            # DM1
            self.frGraphBarrelL4dm1 = self.file.Get( 'tau-DM1_lllt_AllEta_'+self.app+'_graph' )
            self.frFitBarrelL4dm1 = self.file.Get( 'tau-DM1_lllt_AllEta_'+self.app+'_fit' )
            self.frGraphEndcapL4dm1 = self.file.Get( 'tau-DM1_lllt_AllEta_'+self.app+'_graph' )
            self.frFitEndcapL4dm1 = self.file.Get( 'tau-DM1_lllt_AllEta_'+self.app+'_fit' )
            # DM10
            self.frGraphBarrelL4dm10 = self.file.Get( 'tau-DM10_lllt_AllEta_'+self.app+'_graph' )
            self.frFitBarrelL4dm10 = self.file.Get( 'tau-DM10_lllt_AllEta_'+self.app+'_fit' )
            self.frGraphEndcapL4dm10 = self.file.Get( 'tau-DM10_lllt_AllEta_'+self.app+'_graph' )
            self.frFitEndcapL4dm10 = self.file.Get( 'tau-DM10_lllt_AllEta_'+self.app+'_fit' )
        elif self.channel in ['eett','mmtt',] :
            # DM0
            self.frGraphBarrelL4dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_graph' )
            self.frFitBarrelL4dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_fit' )
            self.frGraphEndcapL4dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_graph' )
            self.frFitEndcapL4dm0 = self.file.Get( 'tau-DM0_lltt_AllEta_'+self.app+'_fit' )
            # DM1
            self.frGraphBarrelL4dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_graph' )
            self.frFitBarrelL4dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_fit' )
            self.frGraphEndcapL4dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_graph' )
            self.frFitEndcapL4dm1 = self.file.Get( 'tau-DM1_lltt_AllEta_'+self.app+'_fit' )
            # DM10
            self.frGraphBarrelL4dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_graph' )
            self.frFitBarrelL4dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_fit' )
            self.frGraphEndcapL4dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_graph' )
            self.frFitEndcapL4dm10 = self.file.Get( 'tau-DM10_lltt_AllEta_'+self.app+'_fit' )
        elif self.channel in ['eeem','eemm','emmm','mmmm'] :
            self.frGraphBarrelL4 = self.file.Get( 'muon_Barrel_'+self.app+'_graph' )
            self.frFitBarrelL4 = self.file.Get( 'muon_Barrel_'+self.app+'_fit' )
            self.frGraphEndcapL4 = self.file.Get( 'muon_Endcap_'+self.app+'_graph' )
            self.frFitEndcapL4 = self.file.Get( 'muon_Endcap_'+self.app+'_fit' )
        elif self.channel in ['eeee',] :
            self.frGraphBarrelL4 = self.file.Get( 'electron_Barrel_'+self.app+'_graph' )
            self.frFitBarrelL4 = self.file.Get( 'electron_Barrel_'+self.app+'_fit' )
            self.frGraphEndcapL4 = self.file.Get( 'electron_Endcap_'+self.app+'_graph' )
            self.frFitEndcapL4 = self.file.Get( 'electron_Endcap_'+self.app+'_fit' )


    # Save some space with this
    def evalWeight( self, pt, absEta, useFit, fitBarrel, graphBarrel, fitEndcap, graphEndcap ) :
        if absEta < 1.4 :
            #if useFit :
            return fitBarrel.Eval( pt ) / ( 1. - fitBarrel.Eval( pt ) )
            #else :
            #    return graphBarrel.Eval( pt ) / ( 1. - graphBarrel.Eval( pt ) )
        if absEta >= 1.4 :
            #if useFit :
            return fitEndcap.Eval( pt ) / ( 1. - fitEndcap.Eval( pt ) )
            #else :
            #    return graphEndcap.Eval( pt ) / ( 1. - graphEndcap.Eval( pt ) )



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
        
        if pt > 200 : pt = 199

        # Check if we should use the graph points instead of the fit
        # for elec and muon, fits end before out lowest threshold
        # Also make sure we stay on the lowest threshold for the graphs
        useFit = True
        #if self.jetMatched : useFit = False # This is coarsely binned
        if 'e' in lep :
            #if pt < self.electronFitCut : useFit = False
            if pt <= 10 : pt = 10.1
        elif 'm' in lep :
            #if pt < self.muonFitCut : useFit = False
            if pt <= 10 : pt = 10.1

        if not 't' in lep :
            return self.evalWeight( pt, abs(eta), useFit, self.frFitBarrelL3, self.frGraphBarrelL3,\
                    self.frFitEndcapL3, self.frGraphEndcapL3 )
        if 't' in lep :
            if getattr( row, lep+'DecayMode' ) == 0 :
                return self.evalWeight( pt, abs(eta), useFit, self.frFitBarrelL3dm0, self.frGraphBarrelL3dm0,\
                        self.frFitEndcapL3dm0, self.frGraphEndcapL3dm0 )
            if getattr( row, lep+'DecayMode' ) == 1 :
                return self.evalWeight( pt, abs(eta), useFit, self.frFitBarrelL3dm1, self.frGraphBarrelL3dm1,\
                        self.frFitEndcapL3dm1, self.frGraphEndcapL3dm1 )
            if getattr( row, lep+'DecayMode' ) == 10 :
                return self.evalWeight( pt, abs(eta), useFit, self.frFitBarrelL3dm10, self.frGraphBarrelL3dm10,\
                        self.frFitEndcapL3dm10, self.frGraphEndcapL3dm10 )
        return 0. # Default


    def getFRWeightL4( self, pt, eta, lep, row ):
        if self.channel in ['eett','mmtt','eeet','emmt','eemt','mmmt',] :
            if self.tauPasses( lep, row ) : return 0.
        elif self.channel in ['eeem','eemm','emmm','mmmm'] :
            if self.muonPasses( lep, row ) : return 0.
        elif self.channel in ['eeee',] :
            if self.electronPasses( lep, row ) : return 0.
        
        if pt > 200 : pt = 199

        # Check if we should use the graph points instead of the fit
        # for elec and muon, fits end before out lowest threshold
        # Also make sure we stay on the lowest threshold for the graphs
        useFit = True
        #if self.jetMatched : useFit = False # This is coarsely binned
        if 'e' in lep :
            #if pt < self.electronFitCut : useFit = False
            if pt <= 10 : pt = 10.1
        elif 'm' in lep :
            #if pt < self.muonFitCut : useFit = False
            if pt <= 10 : pt = 10.1

        if not 't' in lep :
            return self.evalWeight( pt, abs(eta), useFit, self.frFitBarrelL4, self.frGraphBarrelL4,\
                    self.frFitEndcapL4, self.frGraphEndcapL4 )
        if 't' in lep :
            if getattr( row, lep+'DecayMode' ) == 0 :
                return self.evalWeight( pt, abs(eta), useFit, self.frFitBarrelL4dm0, self.frGraphBarrelL4dm0,\
                        self.frFitEndcapL4dm0, self.frGraphEndcapL4dm0 )
            if getattr( row, lep+'DecayMode' ) == 1 :
                return self.evalWeight( pt, abs(eta), useFit, self.frFitBarrelL4dm1, self.frGraphBarrelL4dm1,\
                        self.frFitEndcapL4dm1, self.frGraphEndcapL4dm1 )
            if getattr( row, lep+'DecayMode' ) == 10 :
                return self.evalWeight( pt, abs(eta), useFit, self.frFitBarrelL4dm10, self.frGraphBarrelL4dm10,\
                        self.frFitEndcapL4dm10, self.frGraphEndcapL4dm10 )
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


if '__main__' in __name__ :
    channel = 'emmt'
    fr = ReducibleBkgWeights( channel )

    print fr.getFRWeightL3( 34. ) 
    print fr.getFRWeightL4( 34. ) 
    print fr.getFRWeightBoth( 34., 34. ) 

