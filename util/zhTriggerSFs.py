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
            self.singleTrigThreshold = 28.0
            self.subleadingDoubleTrigThreshold = 13.0
            self.singleMin = 27.1
            self.doubleSubleadingMin = 7.1
            self.doubleLeadingMin = 23.1
            self.singleName = 'HLT_Ele27_WPTight_Gsf'
            self.doubleLeadingName = 'HLT_Ele23_CaloIdL_TrackIdL_IsoVL'
            self.doubleSubleadingName = 'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_and_DZ'

        if self.zType == 'ZMM' :
            self.etaMax = 2.39
            self.singleTrigThreshold = 25.0
            self.subleadingDoubleTrigThreshold = 10.0
            self.singleMin = 23.1
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

        #print nvtx, pt1, eta1, pt2, eta2

        # In Z->EE it is possible to not fire the double trigger b/c
        # of low pT subleading with high pT leading firing single E
        ineff_data = 1.0
        ineff_mc = 1.0
        # Check double lep thresholds
        if pt2 > self.subleadingDoubleTrigThreshold :
            ineff_data *= (1. - self.doubleLeadingData.GetBinContent( self.doubleLeadingData.FindBin( pt1, eta1 ) ) \
                    * self.doubleSubleadingData.GetBinContent( self.doubleSubleadingData.FindBin( pt2, nvtx ) ) )
            ineff_mc *= (1. - self.doubleLeadingMC.GetBinContent( self.doubleLeadingMC.FindBin( pt1, eta1 ) ) \
                    * self.doubleSubleadingMC.GetBinContent( self.doubleSubleadingMC.FindBin( pt2, nvtx ) ) )
            #print self.doubleLeadingMC.GetBinContent( self.doubleLeadingMC.FindBin( pt1, eta1 ) )
            #print self.doubleSubleadingMC.GetBinContent( self.doubleSubleadingMC.FindBin( pt2, nvtx ) )
            #print 1, ineff_mc

        # second "region"
        if pt1 > self.singleTrigThreshold :
            ineff_data *= (1. - self.singleTriggerData.GetBinContent( self.singleTriggerData.FindBin( pt1, eta1 ) ) )
            ineff_mc *= (1. - self.singleTriggerMC.GetBinContent( self.singleTriggerMC.FindBin( pt1, eta1 ) ) )
            #print 2, ineff_mc

            # third "region" only possible if second region is true
            if pt2 > self.singleTrigThreshold :
                ineff_data *= (1. - self.singleTriggerData.GetBinContent( self.singleTriggerData.FindBin( pt2, eta2 ) ) )
                ineff_mc *= (1. - self.singleTriggerMC.GetBinContent( self.singleTriggerMC.FindBin( pt2, eta2 ) ) )
                #print 3, ineff_mc

        #print 4, ineff_mc
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

        # In Z->EE it is possible to not fire the double trigger b/c
        # of low pT subleading with high pT leading firing single E
        ineff_data = 1.0
        # Check double lep thresholds
        if pt2 > self.subleadingDoubleTrigThreshold :
            ineff_data *= (1. - self.doubleLeadingData.GetBinContent( self.doubleLeadingData.FindBin( pt1, eta1 ) ) \
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

        # In Z->EE it is possible to not fire the double trigger b/c
        # of low pT subleading with high pT leading firing single E
        ineff_mc = 1.0
        # Check double lep thresholds
        if pt2 > self.subleadingDoubleTrigThreshold :
            ineff_mc *= (1. - self.doubleLeadingMC.GetBinContent( self.doubleLeadingMC.FindBin( pt1, eta1 ) ) \
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
    zhSF2 = zhTriggerSF('ZEE')
    print zhSF2.getZHTriggerSF( 15, 24.0714149475, 1.04681718349, 21.9751396179, -1.60170006752 )




