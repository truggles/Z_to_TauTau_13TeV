
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




def doubleTauTriggerEff( pt, iso, genCode, ttSS ) :


    # Fit values from Riccardo
    # 2016B, 2 fb^-1
    # https://indico.cern.ch/event/544712/contributions/2213574/attachments/1295299/1930984/htt_tau_trigger_17_6_2016.pdf

    coefMap = {
    'Real Tau' : {
        'VTight' : {
            'm0'     : 3.77850E+01,
            'sigma'  : 4.93611E+00,
            'alpha'  : 4.22634E+00,
            'n'      : 2.85533E+00,
            'norm'   : 9.92196E-01 },
        'Tight' : {
            'm0'     : 3.81919E+01,
            'sigma'  : 5.38746E+00,
            'alpha'  : 4.44730E+00,
            'n'      : 7.39646E+00,
            'norm'   : 9.33402E-01 },
        'Medium' : {
            'm0'     : 3.81821E+01,
            'sigma'  : 5.33452E+00,
            'alpha'  : 4.42570E+00,
            'n'      : 4.70512E+00,
            'norm'   : 9.45637E-01 },
        'Loose' : {
            'm0'     : 3.85953E+01,
            'sigma'  : 5.74632E+00,
            'alpha'  : 5.08553E+00,
            'n'      : 5.45593E+00,
            'norm'   : 9.42168E-01 },
        'NoIso' : {
            'm0'     : 3.86506E+01,
            'sigma'  : 5.81155E+00,
            'alpha'  : 5.82783E+00,
            'n'      : 3.38903E+00,
            'norm'   : 9.33449E+00 
        },
    }, # end Real Tau
    'Fake Tau mT Cut' : {
        'VTight' : {
            'm0'     : 3.92867E+01,
            'sigma'  : 7.22249E+00,
            'alpha'  : 1.14726E+01,
            'n'      : 1.32792E+00,
            'norm'   : 1.00000E+00 },
        'Tight' : {
            'm0'     : 3.90677E+01,
            'sigma'  : 7.03152E+00,
            'alpha'  : 1.11690E+01,
            'n'      : 1.29314E+00,
            'norm'   : 9.99999E-01 },
        'Medium' : {
            'm0'     : 3.92674E+01,
            'sigma'  : 7.17092E+00,
            'alpha'  : 1.10546E+01,
            'n'      : 1.31852E+00,
            'norm'   : 1.00000E+00 },
        'Loose' : {
            'm0'     : 3.94747E+01,
            'sigma'  : 7.23546E+00,
            'alpha'  : 1.08089E+01,
            'n'      : 1.33930E+00,
            'norm'   : 1.00000E+00 },
        'NoIso' : {
            'm0'     : 4.03919E+01,
            'sigma'  : 7.55333E+00,
            'alpha'  : 1.20102E+01,
            'n'      : 1.26661E+00,
            'norm'   : 1.00000E+00 
        },
    }, # Fake Tau - mT Cut
    'Fake Tau SS' : {
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
            'norm'   : 7.99738e-01 
        },
    } # Fake Tau - SS
} # end coefMap



    if iso not in coefMap['Real Tau'].keys() :
        print "\n\n Provided isolation for doubleTauTriggerEff is not valid\n\n"
        return 1.



    cat = 'Real Tau'
    #if genCode == 5 :
    #    cat = 'Real Tau'
    #elif ttSS :
    #    cat = 'Fake Tau SS'    
    #else :
    #    cat = 'Fake Tau mT Cut'    



    return CBeff( pt, coefMap[cat][iso]['m0'], coefMap[cat][iso]['sigma'], coefMap[cat][iso]['alpha'], coefMap[cat][iso]['n'], coefMap[cat][iso]['norm'] )






