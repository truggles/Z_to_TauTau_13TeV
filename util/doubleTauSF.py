
"""
function provided by Riccardo Manzoni for scaling
double tau trigger MC to data
22 Feb 2016

Updated 30 Jan 2017 to include data/MC scale factors
"""


import math
import ROOT
import json
from helpers import getTH1FfromTGraphAsymmErrors

class DoubleTau35Efficiencies :
    """A class to provide trigger efficiencies 
    for HLT DoubleTau35 trigger"""
    

    def __init__( self, channel ):

        if channel == 'tt' :
            #print "Initializing LepWeight class for channel ",channel
            #effType = 'binned'
            #effType = 'cumulative'
            #with open('data/triggerSF/di-tau/high_mt_%s.json' % effType) as f1 :
            #    self.high_mt_json = json.load(f1)
            with open('data/triggerSF/di-tau/fitresults_tt_moriond2017.json') as f2 :
                self.real_taus_json = json.load(f2)
            #with open('data/triggerSF/di-tau/same_sign_%s.json' % effType) as f3 :
            #    self.same_sign_json = json.load(f3)

        else :
            #self.high_mt_json = ''
            self.real_taus_json = ''
            #self.high_mt_json = ''



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




    def doubleTauTriggerEff(self, pt, iso, genCode, decayMode ) :

        # Check that there are no 2 prong taus
        assert( decayMode in [0,1,10]), "You have not cleaned your decay \
            modes of your taus!"

        """ 2016 Moriond17 set up has differing efficiencies per decay mode
            remove the lumi weighted approach. Calculate Data/MC
            SF as final output """
        m0      = self.real_taus_json['data_genuine_TightIso_dm%i' % int(decayMode)]['m_{0}']
        sigma   = self.real_taus_json['data_genuine_TightIso_dm%i' % int(decayMode)]['sigma']
        alpha   = self.real_taus_json['data_genuine_TightIso_dm%i' % int(decayMode)]['alpha']
        n       = self.real_taus_json['data_genuine_TightIso_dm%i' % int(decayMode)]['n']
        norm    = self.real_taus_json['data_genuine_TightIso_dm%i' % int(decayMode)]['norm']
        dataW   = self.CBeff( pt, m0, sigma, alpha, n, norm )

        m0      = self.real_taus_json['mc_genuine_TightIso_dm%i' % int(decayMode)]['m_{0}']
        sigma   = self.real_taus_json['mc_genuine_TightIso_dm%i' % int(decayMode)]['sigma']
        alpha   = self.real_taus_json['mc_genuine_TightIso_dm%i' % int(decayMode)]['alpha']
        n       = self.real_taus_json['mc_genuine_TightIso_dm%i' % int(decayMode)]['n']
        norm    = self.real_taus_json['mc_genuine_TightIso_dm%i' % int(decayMode)]['norm']
        mcW     = self.CBeff( pt, m0, sigma, alpha, n, norm )

        return 1.*dataW / mcW



if __name__ == '__main__' :
    c = DoubleTau35Efficiencies('tt')
    print c.doubleTauTriggerEff(68., 'VTightIso', 5, 1 ) # 5 = gen_match real tau
    print c.doubleTauTriggerEff(68., 'VTightIso', 3, 0 ) # 3 = gen_match NOT real tau
    print c.doubleTauTriggerEff(68., 'TightIso', 5 , 10 ) # 5 = gen_match real tau
    print c.doubleTauTriggerEff(68., 'TightIso', 3 , 6 ) # 3 = gen_match NOT real tau

