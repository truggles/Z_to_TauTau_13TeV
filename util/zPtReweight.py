'''
A Class to interface with MSSM LO DYJets Z Pt scale factors:
see: https://twiki.cern.ch/twiki/bin/view/CMS/MSSMAHTauTauEarlyRun2#Z_reweighting
'''


import ROOT

class ZPtReweighter :
    """A class to provide LO DYJets Z Pt based reweighting factors"""
    

    def __init__(self):
        #print "Initializing LepWeight class for channel ",channel
        self.zptFile = ROOT.TFile('data/zpt_weights_2016_mssm.root','r')
        self.zptHist = self.zptFile.Get('zptmass_histo')


    def getZPtReweight( self, genMass, genPt ):
        massBin = self.zptHist.GetXaxis().FindBin(genMass)
        ptBin = self.zptHist.GetYaxis().FindBin(genPt)
        return self.zptHist.GetBinContent( massBin, ptBin )



if __name__ == '__main__' :
    obj = ZPtReweighter()
    print obj.getZPtReweight( 90, 100 )
