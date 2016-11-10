
"""
function provided by Riccardo Manzoni for scaling
double tau trigger MC to data
22 Feb 2016
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
            effType = 'binned'
            #effType = 'cumulative'
            with open('data/triggerSF/di-tau/high_mt_%s.json' % effType) as f1 :
                self.high_mt_json = json.load(f1)
            with open('data/triggerSF/di-tau/real_taus_%s.json' % effType) as f2 :
                self.real_taus_json = json.load(f2)
            with open('data/triggerSF/di-tau/same_sign_%s.json' % effType) as f3 :
                self.same_sign_json = json.load(f3)

            ### New Method
            self.fVL = ROOT.TFile('data/doubleTau35/allRuns-VLoose.root','r')
            self.vloose = getTH1FfromTGraphAsymmErrors( \
                self.fVL.Get('divide_OSPassAllRuns_by_OSAllAllRuns'), 'vloose')
            self.fL = ROOT.TFile('data/doubleTau35/allRuns-Loose.root','r')
            self.loose = getTH1FfromTGraphAsymmErrors( \
                self.fL.Get('divide_OSPassAllRuns_by_OSAllAllRuns'), 'loose')
            self.fM = ROOT.TFile('data/doubleTau35/allRuns-Medium.root','r')
            self.medium = getTH1FfromTGraphAsymmErrors( \
                self.fM.Get('divide_OSPassAllRuns_by_OSAllAllRuns'), 'medium')
            self.fT = ROOT.TFile('data/doubleTau35/allRuns-Tight.root','r')
            self.tight = getTH1FfromTGraphAsymmErrors( \
                self.fT.Get('divide_OSPassAllRuns_by_OSAllAllRuns'), 'tight')
            self.fVT = ROOT.TFile('data/doubleTau35/allRuns-VTight.root','r')
            self.vtight = getTH1FfromTGraphAsymmErrors( \
                self.fVT.Get('divide_OSPassAllRuns_by_OSAllAllRuns'), 'vtight')
        else :
            self.high_mt_json = ''
            self.real_taus_json = ''
            self.high_mt_json = ''

        # These are the 2.1/fb efficiencies
        #self.effMap = {
        #    'Real Tau' : {
        #        'VTight' : {
        #            'm_{0}'     : 3.77850E+01,
        #            'sigma'  : 4.93611E+00,
        #            'alpha'  : 4.22634E+00,
        #            'n'      : 2.85533E+00,
        #            'norm'   : 9.92196E-01 },
        #        'Tight' : {
        #            'm_{0}'     : 3.81919E+01,
        #            'sigma'  : 5.38746E+00,
        #            'alpha'  : 4.44730E+00,
        #            'n'      : 7.39646E+00,
        #            'norm'   : 9.33402E-01 },
        #        'Medium' : {
        #            'm_{0}'     : 3.81821E+01,
        #            'sigma'  : 5.33452E+00,
        #            'alpha'  : 4.42570E+00,
        #            'n'      : 4.70512E+00,
        #            'norm'   : 9.45637E-01 },
        #        'Loose' : {
        #            'm_{0}'     : 3.85953E+01,
        #            'sigma'  : 5.74632E+00,
        #            'alpha'  : 5.08553E+00,
        #            'n'      : 5.45593E+00,
        #            'norm'   : 9.42168E-01 },
        #        'NoIso' : {
        #            'm_{0}'     : 3.86506E+01,
        #            'sigma'  : 5.81155E+00,
        #            'alpha'  : 5.82783E+00,
        #            'n'      : 3.38903E+00,
        #            'norm'   : 9.33449E+00 
        #        },
        #    }, # end Real Tau
        #    'Fake Tau SS' : {
        #        'VTight' : {
        #            'm_{0}'     : 3.96158e+01,
        #            'sigma'  : 7.87478e+00,
        #            'alpha'  : 3.99837e+01,
        #            'n'      : 6.70004e+01,
        #            'norm'   : 7.57548e-01 },
        #        'Tight' : {
        #            'm_{0}'     : 3.99131e+01,
        #            'sigma'  : 7.77317e+00,
        #            'alpha'  : 3.99403e+01,
        #            'n'      : 1.40999e+02,
        #            'norm'   : 7.84025e-01 },
        #        'Medium' : {
        #            'm_{0}'     : 4.04241e+01,
        #            'sigma'  : 7.95194e+00,
        #            'alpha'  : 3.99649e+01,
        #            'n'      : 1.41000e+02,
        #            'norm'   : 8.00926e-01 },
        #        'Loose' : {
        #            'm_{0}'     : 4.05980e+01,
        #            'sigma'  : 7.87581e+00,
        #            'alpha'  : 3.98818e+01,
        #            'n'      : 1.41000e+02,
        #            'norm'   : 7.98198e-01 },
        #        'NoIso' : {
        #            'm_{0}'     : 4.14353e+01,
        #            'sigma'  : 8.10732e+00,
        #            'alpha'  : 9.58501e+00,
        #            'n'      : 1.41000e+02,
        #            'norm'   : 7.99738e-01 
        #        },
        #    } # Fake Tau - SS
        #} # end coefMap


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
        #iso = 'TightIso'

        ### 2.1/FB EFFICIENCIES
        ### If you want to use 2.1/fb, uncomment the 'effMap'
        ### related lines and directly below
        #iso = iso.strip('Iso')


        if genCode == 5 : # Real Hadronically decay Tau
            m0 = self.real_taus_json[iso]['m_{0}']
            sigma = self.real_taus_json[iso]['sigma']
            alpha = self.real_taus_json[iso]['alpha']
            n = self.real_taus_json[iso]['n']
            norm = self.real_taus_json[iso]['norm']
            #m0 = self.effMap['Real Tau'][iso]['m_{0}']
            #sigma = self.effMap['Real Tau'][iso]['sigma']
            #alpha = self.effMap['Real Tau'][iso]['alpha']
            #n = self.effMap['Real Tau'][iso]['n']
            #norm = self.effMap['Real Tau'][iso]['norm']
            ''' for the moment stick with real vs. fake '''
        else : # Fake Tau (measurements were done in SS region)
            m0 = self.same_sign_json[iso]['m_{0}']
            sigma = self.same_sign_json[iso]['sigma']
            alpha = self.same_sign_json[iso]['alpha']
            n = self.same_sign_json[iso]['n']
            norm = self.same_sign_json[iso]['norm']
            #m0 = self.effMap['Fake Tau SS'][iso]['m_{0}']
            #sigma = self.effMap['Fake Tau SS'][iso]['sigma']
            #alpha = self.effMap['Fake Tau SS'][iso]['alpha']
            #n = self.effMap['Fake Tau SS'][iso]['n']
            #norm = self.effMap['Fake Tau SS'][iso]['norm']
        
        ### Temporary check using efficiency bins instead of fit function
        #if pt > 160 : pt = 159
        #if 'VLoose' in iso : return self.vloose.GetBinContent( self.vloose.FindBin( pt ) )
        #if 'Loose' in iso : return self.loose.GetBinContent( self.loose.FindBin( pt ) )
        #if 'Medium' in iso : return self.medium.GetBinContent( self.medium.FindBin( pt ) )
        #if 'Tight' in iso : return self.tight.GetBinContent( self.tight.FindBin( pt ) )
        #if 'VTight' in iso : return self.vtight.GetBinContent( self.vtight.FindBin( pt ) )
        #return self.tight.GetBinContent( self.tight.FindBin( pt ) )


        return self.CBeff( pt, m0, sigma, alpha, n, norm )




if __name__ == '__main__' :
    c = DoubleTau35Efficiencies('tt')
    print c.doubleTauTriggerEff(68., 'VTightIso', 5 ) # 5 = gen_match real tau
    print c.doubleTauTriggerEff(68., 'VTightIso', 3 ) # 3 = gen_match NOT real tau
    print c.doubleTauTriggerEff(68., 'TightIso', 5 ) # 5 = gen_match real tau
    print c.doubleTauTriggerEff(68., 'TightIso', 3 ) # 3 = gen_match NOT real tau

