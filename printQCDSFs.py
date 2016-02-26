import ROOT
from ROOT import gPad
import glob
from util.buildTChain import makeTChainFromGlob


ROOT.gROOT.SetBatch(True)

def getSF( region ) :
    f = ROOT.TFile('meta/dataCardsBackgrounds/tt_qcdShape_%s.root' % region,'r')
    #print f
    h = f.Get('tt_Histos/m_vis')
    #print h
    int_ = h.Integral()
    print "QCD Region: %s   QCD Integral: %f" % (region, int_ )
    f.Close()
    return int_    








if __name__ == '__main__' :
    regions = ['SSsig', 'SSl2loose', 'SSsigNoBT', 'SSl2looseNoBT', 'SSsigBT', 'SSl2looseBT']
    vals = []
    for region in regions :
        vals.append( getSF( region ) )
    #for val_ in vals:
    #    print val_
    print "Inclusive: %f" % (float(vals[0])/float(vals[1]))
    print "No B Tag: %f" % (float(vals[2])/float(vals[3]))
    print "B Tag: %f" % (float(vals[4])/float(vals[5]))








