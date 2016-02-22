
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

def doubleTauTriggerEff( pt ) :

    # Fit values from Riccardo
    m0_d     = 3.45412e+01
    sigma_d  = 5.63353e+00
    alpha_d  = 2.49242e+00
    n_d      = 3.35896e+00
    norm_d   = 1.00000e+00
    m0_mc    = 3.60274e+01
    sigma_mc = 5.89434e+00
    alpha_mc = 5.82870e+00
    n_mc     = 1.83737e+00
    norm_mc  = 9.58000e-01


    return CBeff( pt, m0_d, sigma_d, alpha_d, n_d, norm_d ) / CBeff( pt, m0_mc, sigma_mc, alpha_mc, n_mc, norm_mc )






