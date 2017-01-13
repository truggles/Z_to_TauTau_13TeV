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

        # Set Leg3 FR graphs
        if self.channel in ['eeet','eeem','emmt','emmm','eeee'] :
            self.frGraphL3 = self.file.Get( 'electron_AllEta_graph' )
            self.frFitL3 = self.file.Get( 'electron_AllEta_fit' )
        elif self.channel in ['eemm','eemt','mmmt','mmmm'] :
            self.frGraphL3 = self.file.Get( 'muon_AllEta_graph' )
            self.frFitL3 = self.file.Get( 'muon_AllEta_fit' )
        elif self.channel in ['eett','mmtt'] :
            self.frGraphL3 = self.file.Get( 'tau_AllEta_graph' )
            self.frFitL3 = self.file.Get( 'tau_AllEta_fit' )

        # Set Leg4 FR graphs
        if self.channel in ['eett','mmtt','eeet','emmt','eemt','mmmt',] :
            self.frGraphL4 = self.file.Get( 'tau_AllEta_graph' )
            self.frFitL4 = self.file.Get( 'tau_AllEta_fit' )
        elif self.channel in ['eeem','eemm','emmm','mmmm'] :
            self.frGraphL4 = self.file.Get( 'muon_AllEta_graph' )
            self.frFitL4 = self.file.Get( 'muon_AllEta_fit' )
        elif self.channel in ['eeee',] :
            self.frGraphL4 = self.file.Get( 'electron_AllEta_graph' )
            self.frFitL4 = self.file.Get( 'electron_AllEta_fit' )

    # Retrieve values
    # For each of these calls, check if the lepton fails their associated
    # cuts.  If it fails, assign a FF value, if it pass -> 0

    # Not using Eta right now
    def getFRWeightL3( self, pt, lep, row ):
        if self.channel in ['eeet','eeem','emmt','emmm','eeee'] :
            if self.electronPasses( lep, row ) : return 0.
        elif self.channel in ['eemm','eemt','mmmt','mmmm'] :
            if self.muonPasses( lep, row ) : return 0.
        elif self.channel in ['eett','mmtt'] :
            if self.tauPasses( lep, row ) : return 0.
        
        if pt > 200 : pt = 199
        return self.frGraphL3.Eval( pt ) / ( 1. - self.frGraphL3.Eval( pt ) )


    def getFRWeightL4( self, pt, lep, row ):
        if self.channel in ['eett','mmtt','eeet','emmt','eemt','mmmt',] :
            if self.tauPasses( lep, row ) : return 0.
        elif self.channel in ['eeem','eemm','emmm','mmmm'] :
            if self.muonPasses( lep, row ) : return 0.
        elif self.channel in ['eeee',] :
            if self.electronPasses( lep, row ) : return 0.
        
        if pt > 200 : pt = 199
        return self.frGraphL4.Eval( pt ) / ( 1. - self.frGraphL4.Eval( pt ) )

 
    # Check to see if e/m/t pass their cuts
    # and should be skipped   
    def electronPasses( self, lep, row ):
        if getattr( row, lep+'IsoDB03' ) < 0.3 and \
            getattr( row, lep+'MVANonTrigWP90' ) > 0.5 : return True
        else : return False

    def muonPasses( self, lep, row ):
        if getattr( row, lep+'IsoDB04' ) < 0.25 and \
            getattr( row, lep+'PFIDLoose' ) > 0.5 : return True
        else : return False

    def tauPasses( self, lep, row ):
        if getattr( row, lep+'ByLooseIsolationMVArun2v1DBoldDMwLT' ) > 0.5 : return True
        else : return False


if '__main__' in __name__ :
    channel = 'emmt'
    fr = ReducibleBkgWeights( channel )

    print fr.getFRWeightL3( 34. ) 
    print fr.getFRWeightL4( 34. ) 
    print fr.getFRWeightBoth( 34., 34. ) 

