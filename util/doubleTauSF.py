
"""
function provided by Riccardo Manzoni for scaling
double tau trigger MC to data
22 Feb 2016
"""


import math
import ROOT

# Directly from Riccardo
def CBeff(x, m0, sigma, alpha, n, norm):
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

def doubleTauTriggerEff( pt, iso ) :

    # Fit values from Riccardo
    # 2016B, 2 fb^-1
    # https://indico.cern.ch/event/544712/contributions/2213574/attachments/1295299/1930984/htt_tau_trigger_17_6_2016.pdf
    coefMap = {
        'VTight' : {
            'm0'     : 3.96158e+01,
            'sigma'  : 7.87478e+00,
            'alpha'  : 3.99837e+01,
            'n'      : 6.70004e+01,
            'norm'   : 7.57548e-01 },
        'Tight' : {
            'm0'     : 3.99131e+01,
            'sigma'  : 7.77317e+00,
            'alpha'  : 3.99403e+01,
            'n'      : 1.40999e+02,
            'norm'   : 7.84025e-01 },
        'Medium' : {
            'm0'     : 4.04241e+01,
            'sigma'  : 7.95194e+00,
            'alpha'  : 3.99649e+01,
            'n'      : 1.41000e+02,
            'norm'   : 8.00926e-01 },
        'Loose' : {
            'm0'     : 4.05980e+01,
            'sigma'  : 7.87581e+00,
            'alpha'  : 3.98818e+01,
            'n'      : 1.41000e+02,
            'norm'   : 7.98198e-01 },
        'NoIso' : {
            'm0'     : 4.14353e+01,
            'sigma'  : 8.10732e+00,
            'alpha'  : 9.58501e+00,
            'n'      : 1.41000e+02,
            'norm'   : 7.99738e-01 },
    }

    if iso not in coefMap.keys() :
        print "\n\n Provided isolation for doubleTauTriggerEff is not valid\n\n"
        return 1.


    return CBeff( pt, coefMap[iso]['m0'], coefMap[iso]['sigma'], coefMap[iso]['alpha'], coefMap[iso]['n'], coefMap[iso]['norm'] )






