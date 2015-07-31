# Function to building ration plots

import ROOT

def ratioPlot( canvas ) :
    pad1 = ROOT.TPad("pad1", "", 0, .2, 1, 1)
    pad1.Draw()
    pad2 = ROOT.TPad("pad1", "", 0, 0, 1, 0.2)
    pad2.Draw()
    pad1.cd()

    return (pad1, pad2)
