# Function to building ration plots

import ROOT

def ratioPlot( canvas ) :
    plotPad = ROOT.TPad("pad1", "", 0., .3, 1., 1.)
    plotPad.Draw()
    ratioPad = ROOT.TPad("pad1", "", 0., 0., 1., 0.3)
    ratioPad.Draw()
    plotPad.cd()

    return (plotPad, ratioPad)