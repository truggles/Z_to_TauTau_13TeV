# Use to plot the correlation matrix output from an MaxLikelihood fit in HiggsCombine
# Currently set to print all Jet Energy Scale systematics

import ROOT
import time
import subprocess

ROOT.gROOT.SetBatch(True)

def plotFitCorMatrix( rootName, setRange=-1 ) :
    c = ROOT.TCanvas('c1', 'c1', 2000, 2000 )

    f = ROOT.TFile( rootName, 'r' )
    fit = f.Get('fit_s')
    th2 = fit.correlationHist() 
    #if setRange != -1 :
    #    print matrix.GetXaxis().GetNbins()
    th2.Draw('colz')
    #print "Top:",ROOT.gPad.GetTopMargin()
    #print "Bottom:",ROOT.gPad.GetBottomMargin()
    #print "Left:",ROOT.gPad.GetLeftMargin()
    #print "Right:",ROOT.gPad.GetRightMargin()
    ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin()*2 )
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin()*1.5 )
    ROOT.gPad.SetBottomMargin( ROOT.gPad.GetBottomMargin()*1 )
    ROOT.gPad.SetTopMargin( ROOT.gPad.GetTopMargin()*1.3 )

    ROOT.gStyle.SetOptStat(0)
    #ROOT.gPad.SaveAs('tmp.pdf')

    # Find first JES uncert
    firstJesIndexX = -1
    lastJesIndexX = -1
    firstJesIndexY = -1
    lastJesIndexY = -1
    for bin in range(1, th2.GetXaxis().GetNbins()+1) :
        label = th2.GetXaxis().GetBinLabel(bin)
        label = label.replace('CMS_','')
        label = label.replace('_13TeV','')
        if 'scale_j_' in label :
            print label
            if firstJesIndexX == -1 : firstJesIndexX = bin
            lastJesIndexX = bin
        #label = label.replace('scale_j_','')
        th2.GetXaxis().SetBinLabel(bin, label)
    for bin in range(1, th2.GetYaxis().GetNbins()+1) :
        label = th2.GetYaxis().GetBinLabel(bin)
        label = label.replace('CMS_','')
        label = label.replace('_13TeV','')
        if 'scale_j_' in label :
            print label
            if firstJesIndexY == -1 : firstJesIndexY = bin
            lastJesIndexY = bin
        #label = label.replace('scale_j_','')
        th2.GetYaxis().SetBinLabel(bin, label)

    print "X:", firstJesIndexX, lastJesIndexX 
    print "Y:", firstJesIndexY, lastJesIndexY 
    th2.GetXaxis().SetRange( firstJesIndexX, lastJesIndexX )
    th2.GetYaxis().SetRange( firstJesIndexY, lastJesIndexY )
    th2.GetXaxis().SetLabelSize( th2.GetXaxis().GetLabelSize()*0.4 )
    th2.GetYaxis().SetLabelSize( th2.GetYaxis().GetLabelSize()*0.7 )

    # Set Z axis for legend
    print th2.GetContour()
    th2.SetContour( th2.GetContour() * 1000 )
    print th2.GetContour()

    ROOT.gPad.Update()
    c.SaveAs('correlations.pdf')




if '__main__' in __name__ :

    rName = 'mlfit.root'
    plotFitCorMatrix( rName )

