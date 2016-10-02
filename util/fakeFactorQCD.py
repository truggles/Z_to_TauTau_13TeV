'''
A Class to interface with Fake Factor scale factors:
see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauJet2TauFakes
'''


from rootpy.io import root_open
import os

class fakeFactors :
    """A class to provide QCD Fake Factors, mainly needs to hold many
        FakeFactor ROOT items"""
    

    def __init__(self):
        date = '20160914'
        cmssw_base = os.getenv('CMSSW_BASE')
        self.fileInclusive = root_open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/tt/incl/fakeFactors_%s.root' % date,'r')
        self.ffInclusive = self.fileInclusive.Get('ff_qcd_os')
        self.file0jet = root_open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/tt/_0jet/fakeFactors_%s.root' % date,'r')
        self.ff0jet = self.file0jet.Get('ff_qcd_os')
        self.file1jet = root_open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/tt/_1jet/fakeFactors_%s.root' % date,'r')
        self.ff1jet = self.file1jet.Get('ff_qcd_os')
        self.file1jetLow = root_open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/tt/_1jetZ050/fakeFactors_%s.root' % date,'r')
        self.ff1jetLow = self.file1jetLow.Get('ff_qcd_os')
        self.file1jetMed = root_open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/tt/_1jetZ50100/fakeFactors_%s.root' % date,'r')
        self.ff1jetMed = self.file1jetMed.Get('ff_qcd_os')
        self.file1jetHigh = root_open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/tt/_1jetZ100/fakeFactors_%s.root' % date,'r')
        self.ff1jetHigh = self.file1jetHigh.Get('ff_qcd_os')
        self.file2jet = root_open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/tt/_2jet/fakeFactors_%s.root' % date,'r')
        self.ff2jet = self.file2jet.Get('ff_qcd_os')
        self.fileVBF = root_open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/tt/_2jetVBF/fakeFactors_%s.root' % date,'r')
        self.ffVBF = self.fileVBF.Get('ff_qcd_os')
        self.fileBTagged = root_open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/tt/_anyb/fakeFactors_%s.root' % date,'r')
        self.ffBTagged = self.fileBTagged.Get('ff_qcd_os')


        #print self.ffInclusive
        #print self.ff0jet
        #print self.ff1jet
        #print self.ff1jetLow
        #print self.ff1jetMed
        #print self.ff1jetHigh
        #print self.ff2jet
        #print self.ffVBF
        #print self.ffBTagged
        #print "finished here"

    def __del__(self):
        self.fileInclusive.Close()
        self.file0jet.Close()
        self.file1jet.Close()
        self.file1jetLow.Close()
        self.file1jetMed.Close()
        self.file1jetHigh.Close()
        self.file2jet.Close()
        self.fileVBF.Close()
        self.fileBTagged.Close()
        self.ffInclusive.Delete()
        self.ff0jet.Delete()
        self.ff1jet.Delete()
        self.ff1jetLow.Delete()
        self.ff1jetMed.Delete()
        self.ff1jetHigh.Delete()
        self.ff2jet.Delete()
        self.ffVBF.Delete()
        self.ffBTagged.Delete()
        

    ### Methods to return the fake factor objects
    ### Use via:
    ### inputs = [tau_pt, tau_decayMode, njets, mvis, mt, muon_iso]
    ### ff_nom = ff.value( len(inputs),array('d',inputs) ) # nominal fake factor
    ### ff_sys = ff.value( len(inputs),array('d',inputs), 'ff_qcd_syst_up' ) # systematic shift
    def getInclusive( self ):
        return self.ffInclusive
    def get0Jet( self ):
        return self.ff0jet
    def get1Jet( self ):
        return self.ff1jet
    def get1JetLow( self ):
        return self.ff1jetLow
    def get1JetMed( self ):
        return self.ff0jetMed
    def get1JetHigh( self ):
        return self.ff0jetHigh
    def get2Jet( self ):
        return self.ff2jet
    def getVBF( self ):
        return self.ffVBF
    def getBTagged( self ):
        return self.ffBTagged



if __name__ == '__main__' :
    obj = fakeFactors()
    print obj.get0Jet()
    del obj



