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
        self.wpVVTight = self.inFile.Get('DBoldDMwLTEff40')


    def getVVLoose( self, isoRaw, pt ):
        # Make sure we stay on the TGraph
        # this could probably be tightened up on the low Pt side if we cared
        if pt > 1900 : pt = 1900
        if pt < 23 : pt = 23
        thresholdAtPt = self.wpVVLoose.Eval( pt )
        if isoRaw > thresholdAtPt : return 1.0
        else : return 0.0

    def getVVTight( self, isoRaw, pt ):
        if pt > 1900 : pt = 1900
        if pt < 23 : pt = 23
        thresholdAtPt = self.wpVVTight.Eval( pt )
        if isoRaw > thresholdAtPt : return 1.0
        else : return 0.0



if __name__ == '__main__' :
    obj = IsoWPAdder()
    print obj.getVVLoose( 0.48, 1000 )
    print obj.getVVLoose( 0.42, 1000 )
    print obj.getVVTight( 0.48, 1000 )
