'''
A Class to interface with HTT lepton scale factors:
https://github.com/CMS-HTT/LeptonEff-interface/
see: https://github.com/CMS-HTT/LeptonEff-interface/blob/master/instructions.txt
'''


import ROOT
from array import array

class LepWeights :
    """A class to provide lepton weights for Efficiency,
    Isolation&ID and Trigger"""
    

    def __init__(self, channel, count=0 ):
        #print "Initializing LepWeight class for channel ",channel
        self.count = count
        self.iter1 = 0
        self.channel = channel
        self.elecSingleEffMap = self.getSF( 'Electron_SingleEle_eff' )
        self.eSingleEffSF = self.sfHistos( self.elecSingleEffMap )
        self.muonSingleEffMap = self.getSF( 'Muon_SingleMu_eff' )
        self.mSingleEffSF = self.sfHistos( self.muonSingleEffMap )
        if channel == 'em' :
            self.elec12TrigMap = self.getSF( 'Electron_Ele12_eff' )
            self.eTrigSF = self.sfHistos( self.elec12TrigMap )
            self.elecIdIso0p15Map = self.getSF( 'Electron_IdIso0p15_eff' )
            self.eIdIsoSF = self.sfHistos( self.elecIdIso0p15Map )
            self.muon8TrigMap = self.getSF( 'Muon_Mu8_eff' )
            self.mTrigSF = self.sfHistos( self.muon8TrigMap )
            self.muonIdIso0p15Map = self.getSF( 'Muon_IdIso0p15_eff' )
            self.mIdIsoSF = self.sfHistos( self.muonIdIso0p15Map )
        if channel == 'et' :
            self.elec17TrigMap = self.getSF( 'Electron_Ele17_eff' )
            self.eTrigSF = self.sfHistos( self.elec17TrigMap )
            self.elecIdIso0p10Map = self.getSF( 'Electron_IdIso0p10_eff' )
            self.eIdIsoSF = self.sfHistos( self.elecIdIso0p10Map )
        if channel == 'mt' :
            self.muon17TrigMap = self.getSF( 'Muon_Mu17_eff' )
            self.mTrigSF = self.sfHistos( self.muon17TrigMap )
            self.muonIdIso0p10Map = self.getSF( 'Muon_IdIso0p10_eff' )
            self.mIdIsoSF = self.sfHistos( self.muonIdIso0p10Map )


    def getEtaCode( self, lepType, eta ) :
        aEta = abs(eta)
        if lepType == 'e' :
            if aEta < 1.48 : return 'Lt1p48'
            if aEta >= 1.48 : return 'Gt1p48'
        if lepType == 'm' :
            if aEta < 0.9 : return 'Lt0p9'
            if aEta >= 0.9 and aEta < 1.2 : return '0p9to1p2'
            if aEta > 1.2 : return 'Gt1p2'
        

    def getWeight( self, lepType, wType, pt, eta ):
        etaCode = self.getEtaCode( lepType, eta )
        if lepType == 'e' :
            if self.channel not in ['em', 'et'] : 
                print "ERROR: Instanciated with channel:", self.chanel
                return
            if wType == 'Trig' : return self.calcWeight( self.eTrigSF, pt, etaCode )
            if wType == 'IdIso' : return self.calcWeight( self.eIdIsoSF, pt, etaCode )
            if wType == 'Eff' : return self.calcWeight( self.eSingleEffSF, pt, etaCode )
        if lepType == 'm' :
            if self.channel not in ['em', 'mt'] : 
                print "ERROR: Instanciated with channel:", self.chanel
                return
            if wType == 'Trig' : return self.calcWeight( self.mTrigSF, pt, etaCode )
            if wType == 'IdIso' : return self.calcWeight( self.mIdIsoSF, pt, etaCode )
            if wType == 'Eff' : return self.calcWeight( self.mSingleEffSF, pt, etaCode )


    def calcWeight( self, sfMap, pt, etaCode ) :
        # Make sure Pts above the measure value have the value of
        # the highest bin
        nBins = sfMap[etaCode].GetNbinsX()
        ptMax = sfMap[etaCode].GetBinLowEdge( nBins + 1 ) # gives lower edge of overflow == high edge of max plotted bin
        if pt > ptMax : pt = ptMax
        bin_ = sfMap[etaCode].GetXaxis().FindBin( pt )
        return sfMap[etaCode].GetBinContent( bin_ )


    # returns a map with the various eta distributions and
    # Bin center, bin range low, bin range high, scale factor
    def getSF( self, file_ ) :
    
        if 'Electron' in file_ :
            particle = 'Electron'
            etas = ['Lt1p48', 'Gt1p48']
        if 'Muon' in file_ :
            particle = 'Muon'
            etas = ['Lt0p9', '0p9to1p2', 'Gt1p2']
        #if 'Tau' in file_ : particle = 'Tau'
            #particle = 'Tau'
            #tau = [....]
        #print "getSF -",particle
    
        scaleFactors = {}
    
        for eta in etas :
            #print eta
            sfs = []
            iFile = ROOT.TFile('lepSFdata/%s/%s.root' % (particle, file_), 'r' )
            eff1 = iFile.Get('ZMassEta%s_Data' % eta)
            eff2 = iFile.Get('ZMassEta%s_MC' % eta)
            nPts = eff1.GetN()
            for i in range(0, nPts) :
                #print "Data --- Pt: ",i,"x:y ",eff1.GetX()[i], eff1.GetY()[i]," range: ", eff1.GetErrorXhigh(i), eff1.GetErrorXlow(i)
                #print "MC   --- Pt: ",i,"x:y ",eff2.GetX()[i], eff2.GetY()[i]," range: ", eff2.GetErrorXhigh(i), eff2.GetErrorXlow(i)

                if eff1.GetY()[i] == 0 : 
                    sf = 0
                elif eff2.GetY()[i] == 0 : 
                    sf = 1
                else :
                    sf = eff1.GetY()[i] / eff2.GetY()[i]

                sfs.append( (eff1.GetX()[i], eff1.GetErrorXhigh(i), eff1.GetErrorXlow(i), sf) )
            scaleFactors[eta] = sfs
    
        return scaleFactors
    
    
    # takes map from getSF() and creates histograms of 
    # SF associated with each eta value
    def sfHistos( self, sfs ) :
        results = {}
        for key in sfs.keys() :
            binning = array('d', [0,])
            binning.append( sfs[key][0][0] - sfs[key][0][1] ) # [1] is lower range from bin center
            toFill = [0,]
            for i in range(0, len( sfs[key] ) ) :
                #print sfs[key][i]
                highEdge = sfs[key][i][0] + sfs[key][i][2] # [0] is bin center, [2] is upper range
                binning.append( highEdge )
                toFill.append( sfs[key][i][3] ) # [3] is the SF value
            results[ key ] = ROOT.TH1F( '%i_%i_%s' % (self.count, self.iter1, key), key, len(sfs[key]) + 1, binning )
            self.iter1 += 1
            for j in range(0, len( sfs[key] )+1 ) :
                results[key].SetBinContent( j+1, toFill[j] )
        return results
    





