'''
A class to provide the SFs for azh samples because of faulty modeling

The low mass points are simple scalings while the 350 and 400 GeV
masses require scaling to a shape template.
'''


import ROOT
from util.helpers import getTH1FfromTGraphAsymmErrors

class GenMassSF :
    

    def __init__( self, sample ):
        assert( 'azh' in sample ), "Not an AZh sample... can't genMass rescale %s" % sample

    
        ### Load the ICHEP SFs provided by the Muon POG
        self.genMassFile = ROOT.TFile( 'data/gen_mass_SFs.root', 'r' )
        self.mass350 = self.genMassFile.Get( 'mA350_SF' )
        self.mass400 = self.genMassFile.Get( 'mA400_SF' )





    def getGenMassSF( self, sample, genMass ) :
        if sample == 'azh220' : 
            if genMass < 219 : return 0.
            if genMass > 221 : return 0.
            else return 2.37
        if sample == 'azh240' : 
            if genMass < 239 : return 0.
            if genMass > 241 : return 0.
            else return 1.53
        if sample == 'azh260' : 
            if genMass < 259 : return 0.
            if genMass > 261 : return 0.
            else return 1.46
        if sample == 'azh280' : 
            if genMass < 279 : return 0.
            if genMass > 281 : return 0.
            else return 1.44
        if sample == 'azh300' : 
            if genMass < 299 : return 0.
            if genMass > 301 : return 0.
            else return 1.44
        if sample == 'azh320' : 
            if genMass < 319 : return 0.
            if genMass > 321 : return 0.
            else return 1.43
        if sample == 'azh340' : 
            if genMass < 339 : return 0.
            if genMass > 341 : return 0.
            else return 1.44
        if sample == 'azh350' : 
            # Do flat line extension for +/- 10 GeV from peak
            if genMass < 340 : return self.mass350.getBinContent( 340.5 )
            if genMass > 359 : return self.mass350.getBinContent( 358.5 ) # Jaana chose this bin as the flat line extension
            else return self.mass350.getBinContent( genMass )
        if sample == 'azh400' : 
            # Do flat line extension for +/- 10 GeV from peak
            if genMass < 390 : return self.mass400.getBinContent( 390.5 )
            if genMass > 410 : return self.mass400.getBinContent( 409.5 )
            else return self.mass400.getBinContent( genMass )




