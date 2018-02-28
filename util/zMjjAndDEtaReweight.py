'''
A Class to interface with anomalous HiggsTauTau 2D mjj and jet dEta SFs
Only apply to VBF events (needs 2 good jets)
From Cecile /afs/cern.ch/work/c/ccaillol/public/mjj_detajj_weights_2016_BtoH.root
'''


import ROOT

class ZMjjAndDEtaReweighter :
    """A class to provide LO DYjets reweighting for dEta and mjj"""
    

    def __init__(self):
        #print "Initializing LepWeight class for channel ",channel
        self.zFile = ROOT.TFile('data/mjj_detajj_weights_2016_BtoH.root','r')
        self.zHist = self.zFile.Get('detajjmjj_histo')


    def getZMjjAndDEtaReweight( self, mjj, jetDEta ):
        absDEta = abs( jetDEta )
        if absDEta > 9.9 : absDEta = 9.9
        if mjj > 4900 : mjj = 4900
        dEtaBin = self.zHist.GetXaxis().FindBin( absDEta )
        mjjBin = self.zHist.GetYaxis().FindBin( mjj )
            
        rtn = self.zHist.GetBinContent( dEtaBin, mjjBin )
        if rtn <= 0. : rtn = 1.
        return rtn



if __name__ == '__main__' :
    obj = ZMjjAndDEtaReweighter()
    print obj.getZMjjAndDEtaReweight( 10, -10 )
