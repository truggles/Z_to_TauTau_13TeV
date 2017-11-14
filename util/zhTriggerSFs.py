'''
A Class to implement trigger SF for ZH analyses
'''


import ROOT

class zhTriggerSF :
    """ A class to fetch ZH trigger SF """
    

    def __init__( self, zType ):
        assert( zType in ['ZEE','ZMM'] ), "Provided zType %s is not one of 'ZEE' or 'ZMM'" % zType

        self.zType = zType
        self.ptMax = 199.0
        self.nvtxMax = 49
        
        ### Load the zhSF for the appropriate zType
        if self.zType == 'ZEE' :
            self.etaMax = 2.49
            self.singleTrigThreshold = 32.0
            self.singleMin = 28.1
            self.doubleSubleadingMin = 15.1
            self.doubleLeadingMin = 25.1
            self.singleName = 'HLT_Ele27_WPTight_Gsf'
            self.doubleLeadingName = 'HLT_Ele23_CaloIdL_TrackIdL_IsoVL'
            self.doubleSubleadingName = 'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_and_DZ'

        if self.zType == 'ZMM' :
            self.etaMax = 2.39
            self.singleTrigThreshold = 27.0
            self.singleMin = 25.1
            self.doubleSubleadingMin = 7.1
            self.doubleLeadingMin = 15.1
            self.singleName = 'HLT_Mu24'
            self.doubleLeadingName = 'HLT_Mu17_TrkIsoVVL'
            self.doubleSubleadingName = 'HLT_Mu8_and_DZ'

        self.sfFile = ROOT.TFile( 'data/zhTriggerSFs_2016Full.root', 'r' )
        self.singleTriggerData = self.sfFile.Get( self.singleName+'_data' )
        self.doubleLeadingData = self.sfFile.Get( self.doubleLeadingName+'_data' )
        self.doubleSubleadingData = self.sfFile.Get( self.doubleSubleadingName+'_data' )
        self.singleTriggerMC = self.sfFile.Get( self.singleName+'_MC' )
        self.doubleLeadingMC = self.sfFile.Get( self.doubleLeadingName+'_MC' )
        self.doubleSubleadingMC = self.sfFile.Get( self.doubleSubleadingName+'_MC' )




    def getZHTriggerSF( self, nvtx, pt1, eta1, pt2, eta2 ) :
        assert( pt1 >= pt2 ), "Lepton pTs must be ordered"

        # Make sure we stay on our histograms
        if pt1 > self.ptMax : pt1 = self.ptMax
        elif pt1 < self.doubleLeadingMin : pt1 = self.doubleLeadingMin
        if pt2 > self.ptMax : pt2 = self.ptMax
        elif pt2 < self.doubleSubleadingMin : pt2 = self.doubleSubleadingMin

        if eta1 > self.etaMax : eta1 = self.etaMax
        elif eta1 < -1 * self.etaMax : eta1 = -1 * self.etaMax

        if eta2 > self.etaMax : eta2 = self.etaMax
        elif eta2 < -1 * self.etaMax : eta2 = -1 * self.etaMax

        if nvtx > self.nvtxMax : nvtx = self.nvtxMax

        # Start with double lepton SF as that applies to all events
        ineff_data = (1. - self.doubleLeadingData.GetBinContent( self.doubleLeadingData.FindBin( pt1, eta1 ) ) \
                * self.doubleSubleadingData.GetBinContent( self.doubleSubleadingData.FindBin( pt2, nvtx ) ) )
        ineff_mc = (1. - self.doubleLeadingMC.GetBinContent( self.doubleLeadingMC.FindBin( pt1, eta1 ) ) \
                * self.doubleSubleadingMC.GetBinContent( self.doubleSubleadingMC.FindBin( pt2, nvtx ) ) )

        # second "region"
        if pt1 > self.singleTrigThreshold :
            ineff_data *= (1. - self.singleTriggerData.GetBinContent( self.singleTriggerData.FindBin( pt1, eta1 ) ) )
            ineff_mc *= (1. - self.singleTriggerMC.GetBinContent( self.singleTriggerMC.FindBin( pt1, eta1 ) ) )

            # third "region" only possible if second region is true
            if pt2 > self.singleTrigThreshold :
                ineff_data *= (1. - self.singleTriggerData.GetBinContent( self.singleTriggerData.FindBin( pt2, eta2 ) ) )
                ineff_mc *= (1. - self.singleTriggerMC.GetBinContent( self.singleTriggerMC.FindBin( pt2, eta2 ) ) )

        eff_data = 1.0 - ineff_data
        eff_mc = 1.0 - ineff_mc
        return eff_data / eff_mc


    def getZHTriggerDataEff( self, nvtx, pt1, eta1, pt2, eta2 ) :
        assert( pt1 >= pt2 ), "Lepton pTs must be ordered"

        # Make sure we stay on our histograms
        if pt1 > self.ptMax : pt1 = self.ptMax
        elif pt1 < self.doubleLeadingMin : pt1 = self.doubleLeadingMin
        if pt2 > self.ptMax : pt2 = self.ptMax
        elif pt2 < self.doubleSubleadingMin : pt2 = self.doubleSubleadingMin

        if eta1 > self.etaMax : eta1 = self.etaMax
        elif eta1 < -1 * self.etaMax : eta1 = -1 * self.etaMax

        if eta2 > self.etaMax : eta2 = self.etaMax
        elif eta2 < -1 * self.etaMax : eta2 = -1 * self.etaMax

        if nvtx > self.nvtxMax : nvtx = self.nvtxMax

        # Start with double lepton SF as that applies to all events
        ineff_data = (1. - self.doubleLeadingData.GetBinContent( self.doubleLeadingData.FindBin( pt1, eta1 ) ) \
                * self.doubleSubleadingData.GetBinContent( self.doubleSubleadingData.FindBin( pt2, nvtx ) ) )

        # second "region"
        if pt1 > self.singleTrigThreshold :
            ineff_data *= (1. - self.singleTriggerData.GetBinContent( self.singleTriggerData.FindBin( pt1, eta1 ) ) )

            # third "region" only possible if second region is true
            if pt2 > self.singleTrigThreshold :
                ineff_data *= (1. - self.singleTriggerData.GetBinContent( self.singleTriggerData.FindBin( pt2, eta2 ) ) )

        eff_data = 1.0 - ineff_data
        return eff_data


    def getZHTriggerMCEff( self, nvtx, pt1, eta1, pt2, eta2 ) :
        assert( pt1 >= pt2 ), "Lepton pTs must be ordered"

        # Make sure we stay on our histograms
        if pt1 > self.ptMax : pt1 = self.ptMax
        elif pt1 < self.doubleLeadingMin : pt1 = self.doubleLeadingMin
        if pt2 > self.ptMax : pt2 = self.ptMax
        elif pt2 < self.doubleSubleadingMin : pt2 = self.doubleSubleadingMin

        if eta1 > self.etaMax : eta1 = self.etaMax
        elif eta1 < -1 * self.etaMax : eta1 = -1 * self.etaMax

        if eta2 > self.etaMax : eta2 = self.etaMax
        elif eta2 < -1 * self.etaMax : eta2 = -1 * self.etaMax

        if nvtx > self.nvtxMax : nvtx = self.nvtxMax

        # Start with double lepton SF as that applies to all events
        ineff_mc = (1. - self.doubleLeadingMC.GetBinContent( self.doubleLeadingMC.FindBin( pt1, eta1 ) ) \
                * self.doubleSubleadingMC.GetBinContent( self.doubleSubleadingMC.FindBin( pt2, nvtx ) ) )

        # second "region"
        if pt1 > self.singleTrigThreshold :
            ineff_mc *= (1. - self.singleTriggerMC.GetBinContent( self.singleTriggerMC.FindBin( pt1, eta1 ) ) )

            # third "region" only possible if second region is true
            if pt2 > self.singleTrigThreshold :
                ineff_mc *= (1. - self.singleTriggerMC.GetBinContent( self.singleTriggerMC.FindBin( pt2, eta2 ) ) )

        eff_mc = 1.0 - ineff_mc
        return eff_mc



        

if __name__ == '__main__' :
    zhSF = zhTriggerSF('ZMM')
    # getZHTriggerSF( self, nvtx, pt1, eta1, pt2, eta2 )
    print zhSF.getZHTriggerSF( 25.1, 18., 2.2, 11.1, -1.5 )
    print zhSF.getZHTriggerSF( 25.1, 28., 2.2, 21.1, -1.5 )
    print zhSF.getZHTriggerSF( 45, 28., 2.2, 21.1, -1.5 )
    print zhSF.getZHTriggerSF( 25.1, 90., 2.2, 21.1, -1.5 )
    print zhSF.getZHTriggerSF( 25.1, 90., 2.2, 71.1, -1.5 )




