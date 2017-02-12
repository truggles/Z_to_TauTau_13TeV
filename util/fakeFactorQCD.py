'''
A Class to interface with Fake Factor scale factors:
see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauJet2TauFakes
'''


#from rootpy.io import root_open
import ROOT
import os

class fakeFactors :
    """A class to provide QCD Fake Factors, mainly needs to hold many
        FakeFactor ROOT items"""
    

    def __init__(self):
        date = '20170111'
        path = '/src/Z_to_TauTau_13TeV/data/FakeFactors/tt/'
        cmssw_base = os.getenv('CMSSW_BASE')
        #self.fileInclusive = ROOT.TFile(cmssw_base+path+'inclusive/fakeFactors_%s.root' % date,'r')
        #self.ffInclusive = self.fileInclusive.Get('ff_comb')
        self.file0jet = ROOT.TFile(cmssw_base+path+'0Jet/fakeFactors_%s.root' % date,'r')
        self.ff0jet = self.file0jet.Get('ff_comb')
        self.fileBoosted = ROOT.TFile(cmssw_base+path+'boosted/fakeFactors_%s.root' % date,'r')
        self.ffBoosted = self.fileBoosted.Get('ff_comb')
        self.fileVBF = ROOT.TFile(cmssw_base+path+'vbf/fakeFactors_%s.root' % date,'r')
        self.ffVBF = self.fileVBF.Get('ff_comb')


    def __del__(self):
        #self.fileInclusive.Close()
        self.file0jet.Close()
        self.fileBoosted.Close()
        self.fileVBF.Close()
        #self.ffInclusive.Delete()
        self.ff0jet.Delete()
        self.ffBoosted.Delete()
        self.ffVBF.Delete()
        

    ### Methods to return the fake factor objects
    ### Use via:
    ### inputs = [tau_pt, tau_decayMode, njets, mvis, mt, muon_iso]
    ### ff_nom = ff.value( len(inputs),array('d',inputs) ) # nominal fake factor
    ### ff_sys = ff.value( len(inputs),array('d',inputs), 'ff_qcd_syst_up' ) # systematic shift
    #def getInclusive( self ):
    #    return self.ffInclusive
    def get0Jet( self ):
        return self.ff0jet
    def getBoosted( self ):
        return self.ffBoosted
    def getVBF( self ):
        return self.ffVBF



if __name__ == '__main__' :
    obj = fakeFactors()
    print obj.get0Jet()
    del obj




