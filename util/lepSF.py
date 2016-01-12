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
    

    def __init__(self, channel):
        self.channel = channel
        self.elecSingleEffMap = getSF( 'Electron_SingleEle_eff' )
        self.eSingleEffSF = sfHistos( elecSingleEffMap )
        self.muonSingleEffMap = getSF( 'Muon_SingleMu_eff' )
        self.mSingleEffSF = sfHistos( muonSingleEffMap )
        if channel == 'em' :
            self.elec12TrigMap = getSF( 'Electron_Ele12_eff' )
            self.eTrigSF = sfHistos( elec12TrigMap )
            self.elecIdIso0p15Map = getSF( 'Electron_IdIso0p15_eff' )
            self.eIdIsoSF = sfHistos( elecIdIso0p15Map )
            self.muon8TrigMap = getSF( 'Muon_Mu8_eff' )
            self.mTrigSF = sfHistos( muon8TrigMap )
            self.muonIdIso0p15Map = getSF( 'Muon_IdIso0p15_eff' )
            self.mIdIsoSF = sfHistos( muonIdIso0p15Map )
        if channel == 'et' :
            self.elec17TrigMap = getSF( 'Electron_Ele17_eff' )
            self.eTrigSF = sfHistos( elec17TrigMap )
            self.elecIdIso0p10Map = getSF( 'Electron_IdIso0p10_eff' )
            self.eIdIsoSF = sfHistos( elecIdIso0p10Map )
        if channel == 'mt' :
            self.muon17TrigMap = getSF( 'Muon_Mu17_eff' )
            self.mTrigSF = sfHistos( muon17TrigMap )
            self.muonIdIso0p10Map = getSF( 'Muon_IdIso0p10_eff' )
            self.mIdIsoSF = sfHistos( muonIdIso0p10Map )


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
        etaCode = getEtaCode( self, lepType, eta )
        if lepType == 'e' :
            if self.channel not in ['em', 'et'] : 
                print "ERROR: Instanciated with channel:", self.chanel
                return
            if wType == 'Trig' : return self.calcWeight( eTrigSF, pt, etaCode )
            if wType == 'IdIso' : return self.calcWeight( eIdIsoSF, pt, etaCode )
            if wType == 'Eff' : return self.calcWeight( eEffSF, pt, etaCode )
        if lepType == 'm' :
            if self.channel not in ['em', 'mt'] : 
                print "ERROR: Instanciated with channel:", self.chanel
                return
            if wType == 'Trig' : return self.calcWeight( mTrigSF, pt, etaCode )
            if wType == 'IdIso' : return self.calcWeight( mIdIsoSF, pt, etaCode )
            if wType == 'Eff' : return self.calcWeight( mEffSF, pt, etaCode )


    def calcWeight( self, sfMap, pt, etaCode ) :
        # Make sure Pts above the measure value have the value of
        # the highest bin
        nBins = sfMap[etaCode].GetNbinsX()
        ptMax = sfMap[etaCode].GetBinLowEdge( nBins + 1 ) # gives lower edge of overflow == high edge of max plotted bin
        if pt > ptMax : pt = ptMax
        bin_ = sfMap[etaCode].GetXaxis().FindBin( pt )
        return sfMap[etaCode].GetXaxis().GetBinContent( bin_ )


# returns a map with the various eta distributions and
# Bin center, bin range low, bin range high, scale factor
def getSF( file_ ) :

    if 'Electron' in file_ :
        particle = 'Electron'
        etas = ['Lt1p48', 'Gt1p48']
    if 'Muon' in file_ :
        particle = 'Muon'
        etas = ['Lt0p9', '0p9to1p2', 'Gt1p2']
    #if 'Tau' in file_ : particle = 'Tau'
        #particle = 'Tau'
        #tau = [....]

    scaleFactors = {}

    for eta in etas :
        print eta
        sfs = []
        iFile = ROOT.TFile('lepSFdata/%s/%s.root' % (particle, file_), 'r' )
        eff1 = iFile.Get('ZMassEta%s_Data' % eta)
        eff2 = iFile.Get('ZMassEta%s_MC' % eta)
        nPts = eff1.GetN()
        for i in range(0, nPts) :
            #print "Pt: ",i,"x:y ",eff1.GetX()[i], eff1.GetY()[i]," range: ", eff1.GetErrorXhigh(i), eff1.GetErrorXlow(i)
            #print "Pt: ",i,"x:y ",eff2.GetX()[i], eff2.GetY()[i]," range: ", eff2.GetErrorXhigh(i), eff2.GetErrorXlow(i)
            if eff2.GetY()[i] > 0 :
                sf = eff1.GetY()[i] / eff2.GetY()[i]
            else :
                print "MC Efficiency less than or equal to Zero, check histos for missing data"
                return
            sfs.append( (eff1.GetX()[i], eff1.GetErrorXhigh(i), eff1.GetErrorXlow(i), sf) )
        scaleFactors[eta] = sfs

    return scaleFactors


# takes map from getSF() and creates histograms of 
# SF associated with each eta value
def sfHistos( sfs ) :
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
        results[ key ] = ROOT.TH1F( key, key, len(sfs[key]) + 1, binning )
        for j in range(0, len( sfs[key] )+1 ) :
            results[key].SetBinContent( j+1, toFill[j] )
        results[key].SaveAs('tmp/%s.root' % key )
        #print binning
        #print toFill
    return results
    


if __name__ == '__main__' :
    file1 = 'Muon_IdIso0p10_eff'
    print file1
    mapper = getSF( file1 )
    print mapper
    #for item in mapper :
        #print item
        #print mapper[item]
        #print "\n\n"
    histos = sfHistos( mapper )
    print histos
