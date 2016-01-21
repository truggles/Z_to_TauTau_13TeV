'''
A Class to interface with HTT lepton scale factors:
https://github.com/CMS-HTT/LeptonEff-interface/
see: https://github.com/CMS-HTT/LeptonEff-interface/blob/master/instructions.txt
'''


import ROOT
from array import array

class LepWeights :
    """A class to provide lepton weights for
    Isolation&ID and Trigger"""
    

    def __init__(self, channel, count=0 ):
        #print "Initializing LepWeight class for channel ",channel
        self.count = count
        self.iter1 = 0
        self.channel = channel
        if channel == 'em' :
            self.elecIdIso0p15Map = self.getSF( 'Electron_IdIso0p15_eff' )
            self.eIdIsoSF = self.sfHistos( self.elecIdIso0p15Map )
            self.muonIdIso0p15Map = self.getSF( 'Muon_IdIso0p15_eff' )
            self.mIdIsoSF = self.sfHistos( self.muonIdIso0p15Map )

            self.elec12TrigMap = self.getSF( 'Electron_Ele12_eff' )
            self.e12TrigData = self.sfHistos( self.elec12TrigMap, 'data' )
            self.e12TrigMC = self.sfHistos( self.elec12TrigMap, 'mc' )
            self.muon8TrigMap = self.getSF( 'Muon_Mu8_eff' )
            self.m8TrigData = self.sfHistos( self.muon8TrigMap, 'data' )
            self.m8TrigMC = self.sfHistos( self.muon8TrigMap, 'mc' )
            self.muon17TrigMap = self.getSF( 'Muon_Mu17_eff' )
            self.m17TrigData = self.sfHistos( self.muon17TrigMap, 'data' )
            self.m17TrigMC = self.sfHistos( self.muon17TrigMap, 'mc' )
            self.elec17TrigMap = self.getSF( 'Electron_Ele17_eff' )
            self.e17TrigData = self.sfHistos( self.elec17TrigMap, 'data' )
            self.e17TrigMC = self.sfHistos( self.elec17TrigMap, 'mc' )
            #print self.elec12TrigMap
        if channel == 'et' :
            self.elecIdIso0p10Map = self.getSF( 'Electron_IdIso0p10_eff' )
            self.eIdIsoSF = self.sfHistos( self.elecIdIso0p10Map )
            self.elecSingleEffMap = self.getSF( 'Electron_SingleEle_eff' )
            self.eSingleEffSF = self.sfHistos( self.elecSingleEffMap )
        if channel == 'mt' :
            self.muonIdIso0p10Map = self.getSF( 'Muon_IdIso0p10_eff' )
            self.mIdIsoSF = self.sfHistos( self.muonIdIso0p10Map )
            self.muonSingleEffMap = self.getSF( 'Muon_SingleMu_eff' )
            self.mSingleEffSF = self.sfHistos( self.muonSingleEffMap )


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
            if wType == 'IdIso' : return self.calcWeight( self.eIdIsoSF, pt, etaCode )
            if wType == 'Trig' : 
                if self.channel == 'et' : return self.calcWeight( self.eSingleEffSF, pt, etaCode )
        if lepType == 'm' :
            if self.channel not in ['em', 'mt'] : 
                print "ERROR: Instanciated with channel:", self.chanel
                return
            if wType == 'IdIso' : return self.calcWeight( self.mIdIsoSF, pt, etaCode )
            if wType == 'Trig' : 
                if self.channel == 'mt' : return self.calcWeight( self.mSingleEffSF, pt, etaCode )
        else : print "ERROR: LepSF Instanciated with channel:", self.chanel," did not find a \
            corresponding SF to return."
        

    def getEMTrigWeight( self, pt1, eta1, pt2, eta2 ):
        etaCode1 = self.getEtaCode( 'e', eta1 )
        etaCode2 = self.getEtaCode( 'm', eta2 )
        effData = 0
        effData += self.calcWeight( self.e12TrigData, pt1, etaCode1 ) * self.calcWeight( self.m17TrigData, pt2, etaCode2 )
        effData += self.calcWeight( self.e17TrigData, pt1, etaCode1 ) * self.calcWeight( self.m8TrigData, pt2, etaCode2 )
        effData -= self.calcWeight( self.e17TrigData, pt1, etaCode1 ) * self.calcWeight( self.m17TrigData, pt2, etaCode2 )
        #print "effData:",effData
        effMC = 0
        effMC += self.calcWeight( self.e12TrigMC, pt1, etaCode1 ) * self.calcWeight( self.m17TrigMC, pt2, etaCode2 )
        effMC += self.calcWeight( self.e17TrigMC, pt1, etaCode1 ) * self.calcWeight( self.m8TrigMC, pt2, etaCode2 )
        effMC -= self.calcWeight( self.e17TrigMC, pt1, etaCode1 ) * self.calcWeight( self.m17TrigMC, pt2, etaCode2 )
        #print "effMC:",effMC
        if effMC == 0 : return 1
        return (effData / effMC)


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

                sfs.append( (eff1.GetX()[i], eff1.GetErrorXhigh(i), eff1.GetErrorXlow(i), sf, eff1.GetY()[i], eff2.GetY()[i]) )
            scaleFactors[eta] = sfs
    
        return scaleFactors
    
    
    # takes map from getSF() and creates histograms of 
    # SF associated with each eta value
    def sfHistos( self, sfs, extra='sf' ) :
        results = {}
        for key in sfs.keys() :
            binning = array('d', [0,])
            binning.append( sfs[key][0][0] - sfs[key][0][1] ) # [1] is lower range from bin center
            toFill = [0,]
            for i in range(0, len( sfs[key] ) ) :
                #print sfs[key][i]
                highEdge = sfs[key][i][0] + sfs[key][i][2] # [0] is bin center, [2] is upper range
                binning.append( highEdge )
                if extra == 'sf' :
                    toFill.append( sfs[key][i][3] ) # [3] is the SF value
                if extra == 'data' :
                    toFill.append( sfs[key][i][4] ) # [4] is the raw Data value
                if extra == 'mc' :
                    toFill.append( sfs[key][i][5] ) # [5] is the raw MC value
            results[ key ] = ROOT.TH1F( '%i_%i_%s_%s' % (self.count, self.iter1, key, extra), key, len(sfs[key]) + 1, binning )
            self.iter1 += 1
            for j in range(0, len( sfs[key] )+1 ) :
                results[key].SetBinContent( j+1, toFill[j] )
        return results
    





