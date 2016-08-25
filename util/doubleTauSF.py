
"""
function provided by Riccardo Manzoni for scaling
double tau trigger MC to data
22 Feb 2016
"""


import math
import ROOT
import json



class DoubleTau35Efficiencies :
    """A class to provide trigger efficiencies 
    for HLT DoubleTau35 trigger"""
    

    def __init__( self, channel ):
        if channel == 'tt' :
            #print "Initializing LepWeight class for channel ",channel
            with open('data/triggerSF/di-tau/high_mt_cumulative.json') as f1 :
                self.high_mt_cumlative = json.load(f1)
            with open('data/triggerSF/di-tau/real_taus_cumulative.json') as f2 :
                self.real_taus_cumlative = json.load(f2)
            with open('data/triggerSF/di-tau/same_sign_cumulative.json') as f3 :
                self.same_sign_cumlative = json.load(f3)
        else :
            self.high_mt_cumlative = ''
            self.real_taus_cumlative = ''
            self.high_mt_cumlative = ''


    # Directly from Riccardo
    def CBeff(self, x, m0, sigma, alpha, n, norm):
        sqrtPiOver2 = math.sqrt(ROOT.TMath.PiOver2())
        sqrt2       = math.sqrt(2.)
        sig         = abs(sigma)
        t           = (x - m0)/sig * alpha / abs(alpha)
        absAlpha    = abs(alpha/sig)
        a           = ROOT.TMath.Power(n/absAlpha, n) * ROOT.TMath.Exp(-0.5 * absAlpha * absAlpha)
        b           = absAlpha - n/absAlpha
        arg         = absAlpha / sqrt2;
        if   arg >  5.: ApproxErf =  1.
        elif arg < -5.: ApproxErf = -1.
        else          : ApproxErf = ROOT.TMath.Erf(arg)
        leftArea    = (1. + ApproxErf) * sqrtPiOver2
        rightArea   = ( a * 1./ROOT.TMath.Power(absAlpha-b, n-1) ) / (n-1)
        area        = leftArea + rightArea
        if t <= absAlpha:
            arg = t / sqrt2
            if   arg >  5.: ApproxErf =  1.
            elif arg < -5.: ApproxErf = -1.
            else          : ApproxErf = ROOT.TMath.Erf(arg)
            return norm * (1 + ApproxErf) * sqrtPiOver2 / area
        else:
            return norm * (leftArea + a * (1/ROOT.TMath.Power(t-b,n-1) - \
                1/ROOT.TMath.Power(absAlpha - b,n-1)) / (1-n)) / area




    def doubleTauTriggerEff(self, pt, iso, genCode ) :

        # For Sync, they want all taus considered as "VTight" 
        iso = 'TightIso'


        if genCode == 5 : # Real Hadronically decay Tau
            m0 = self.real_taus_cumlative[iso]['m_{0}']
            sigma = self.real_taus_cumlative[iso]['sigma']
            alpha = self.real_taus_cumlative[iso]['alpha']
            n = self.real_taus_cumlative[iso]['n']
            norm = self.real_taus_cumlative[iso]['norm']
            ''' for the moment stick with real vs. fake '''
        #elif genCode == 6 : # Fake Tau (measurements were done in SS region)
        else : # Fake Tau (measurements were done in SS region)
            m0 = self.same_sign_cumlative[iso]['m_{0}']
            sigma = self.same_sign_cumlative[iso]['sigma']
            alpha = self.same_sign_cumlative[iso]['alpha']
            n = self.same_sign_cumlative[iso]['n']
            norm = self.same_sign_cumlative[iso]['norm']
        #else : # Not real and not fake, so high mt?
        #    m0 = self.high_mt_cumlative[iso]['m_{0}']
        #    sigma = self.high_mt_cumlative[iso]['sigma']
        #    alpha = self.high_mt_cumlative[iso]['alpha']
        #    n = self.high_mt_cumlative[iso]['n']
        #    norm = self.high_mt_cumlative[iso]['norm']
        
    
        return self.CBeff( pt, m0, sigma, alpha, n, norm )




if __name__ == '__main__' :
    c = DoubleTau35Efficiencies()
    print c.doubleTauTriggerEff(68., 'VTightIso', 'x', 'ss' )

