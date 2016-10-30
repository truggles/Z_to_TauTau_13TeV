'''
A Class to interface with SM-HTT LO DYJets Z Pt, Eta, Mass scale factors:
see: FIXME not currently in HTT twiki
Original reweight files was based off of :
https://github.com/lperrini/ZmumuFinalSelection/blob/master/UserCode/ztautau_fwk/data/amcatnlo/reweighting.root

Current reweight file is altered for low stats regions and is from :
/afs/cern.ch/user/v/veelken/public/forAlexei/reweighting_rebinned_wEmptyBinFix.root
'''


import ROOT

class ZPtReweighterSMHTT :
    """A class to provide LO DYJets Z Pt based reweighting factors"""
    

    def __init__(self, channel):
        self.zptFile = ROOT.TFile('data/reweighting_rebinned_wEmptyBinFix.root','r')

        if channel == 'em' :
            self.zptHist = self.zptFile.Get('rweight_3d_EM_noMET')
        elif channel == 'et' :
            self.zptHist = self.zptFile.Get('rweight_3d_ET_noMET')
        elif channel == 'mt' :
            self.zptHist = self.zptFile.Get('rweight_3d_MT_noMET')
        else :
            self.zptHist = self.zptFile.Get('rweight_3d_TT_noMET')


    def getZPtReweightSMHTT( self, genMass, genPt, genEta ):
        ptBin = self.zptHist.GetXaxis().FindBin(genPt)
        massBin = self.zptHist.GetYaxis().FindBin(genMass)
        etaBin = self.zptHist.GetZaxis().FindBin(genEta)
        return self.zptHist.GetBinContent( ptBin, massBin, etaBin )



if __name__ == '__main__' :
    obj = ZPtReweighter()
    print obj.getZPtReweight( 90, 100 )
