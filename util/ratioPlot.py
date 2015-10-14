# Function to building ration plots

import ROOT

def ratioPlot( canvas, topSize ) :
    plotPad = ROOT.TPad("pad1", "plot", 0., (1-topSize), 1., 1.)
    plotPad.Draw()
    ratioPad = ROOT.TPad("pad2", "ratio", 0., 0., 1., (1-topSize))
    ratioPad.Draw()
    plotPad.cd()

    return (plotPad, ratioPad)
