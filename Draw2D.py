#!/usr/bin/env python
import ROOT
import re
from array import array
import math
ROOT.gROOT.SetBatch(True)

def add_lumi():
    lowX=0.58
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.06)
    lumi.SetTextFont (   42 )
    lumi.AddText("2016, 35.9 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.21
    lowY=0.70
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.08)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.21
    lowY=0.63
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
        output = ROOT.TLegend(0.65, 0.4, 0.92, 0.82, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output

import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--mthd', action='store', dest='mthd', help="Which method? FF or Standard?")
args = parser.parse_args()
print args.mthd


ROOT.gStyle.SetFrameLineWidth(3)
ROOT.gStyle.SetLineWidth(3)
ROOT.gStyle.SetOptStat(0)

c=ROOT.TCanvas("canvas","",0,0,1200,600)
c.cd()

file=ROOT.TFile("httShapes/htt/htt_tt.inputs-sm-13TeV_svFitMass2D-5040-Tight.root","r")

adapt=ROOT.gROOT.GetColor(12)
new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1
trans=ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),adapt.GetBlue(), "",0.5)

categories= ["tt_boosted","tt_VBF",]
categories= ["tt_0jet",]


ncat=len(categories)

for cat in categories:
   print cat
   Data=file.Get(cat).Get("data_obs")
   print Data.Integral()
   QCD=file.Get(cat).Get("QCD")
   W=file.Get(cat).Get("W") 
   TT=file.Get(cat).Get("TTT")
   VV=file.Get(cat).Get("VV")
   #if not "2bjet" in cat :
   if W != None : VV.Add(W)
   ZL=file.Get(cat).Get("ZL")
   ZJ=file.Get(cat).Get("ZJ")
   if ZJ != None : ZL.Add(ZJ)
   ZTT=file.Get(cat).Get("ZTT")
   SMHiggs=file.Get(cat).Get("ggH125")
   SMHiggs.Add(file.Get(cat).Get("qqH125"))

   Data.GetXaxis().SetTitle("")
   Data.GetXaxis().SetTitleSize(0)
   Data.GetXaxis().SetNdivisions(505)
   Data.GetYaxis().SetLabelFont(42)
   Data.GetYaxis().SetLabelOffset(0.01)
   Data.GetYaxis().SetLabelSize(0.06)
   Data.GetYaxis().SetTitleSize(0.075)
   Data.GetYaxis().SetTitleOffset(1.04)
   Data.SetTitle("")
   Data.GetYaxis().SetTitle("Events/bin")

   QCD.SetFillColor(ROOT.TColor.GetColor("#ffccff"))
   VV.SetFillColor(ROOT.TColor.GetColor("#de5a6a"))
   TT.SetFillColor(ROOT.TColor.GetColor("#9999cc"))
   if not "2bjet" in cat :
    ZL.SetFillColor(ROOT.TColor.GetColor("#4496c8"))
   ZTT.SetFillColor(ROOT.TColor.GetColor("#ffcc66"))
   SMHiggs.SetLineColor(ROOT.kBlue)

   Data.SetMarkerStyle(20)
   Data.SetMarkerSize(1)
   QCD.SetLineColor(1)
   VV.SetLineColor(1)
   TT.SetLineColor(1)
   ZTT.SetLineColor(1)
   if not "2bjet" in cat :
    ZL.SetLineColor(1)
   Data.SetLineColor(1)
   Data.SetLineWidth(2)
   SMHiggs.SetLineWidth(2)

   stack=ROOT.THStack("stack","stack")
   stack.Add(QCD)
   stack.Add(VV)
   stack.Add(TT)
   if not "2bjet" in cat :
    stack.Add(ZL)
   stack.Add(ZTT)

   errorBand = QCD.Clone()
   errorBand.Add(VV)
   errorBand.Add(TT)
   if not "2bjet" in cat :
    errorBand.Add(ZL)
   errorBand.Add(ZTT)
   errorBand.SetMarkerSize(0)
   errorBand.SetFillColor(new_idx)
   errorBand.SetFillStyle(3001)
   errorBand.SetLineWidth(1)

   pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
   pad1.Draw()
   pad1.cd()
   pad1.SetFillColor(0)
   pad1.SetBorderMode(0)
   pad1.SetBorderSize(10)
   pad1.SetTickx(1)
   pad1.SetTicky(1)
   pad1.SetLeftMargin(0.18)
   pad1.SetRightMargin(0.05)
   pad1.SetTopMargin(0.122)
   pad1.SetBottomMargin(0.026)
   pad1.SetFrameFillStyle(0)
   pad1.SetFrameLineStyle(0)
   pad1.SetFrameLineWidth(3)
   pad1.SetFrameBorderMode(0)
   pad1.SetFrameBorderSize(10)

   Data.GetXaxis().SetLabelSize(0)
   Data.SetMaximum(Data.GetMaximum()*1.5)
   Data.Draw("e")
   stack.Draw("hist same")

   # Scale SMH x 10
   higgsSF = 10.
   SMHiggs.Scale( higgsSF )
   SMHiggs.Draw("histsame")
   errorBand.Draw("e2same")
   # Blind
   for bin in range(1, Data.GetNbinsX()+1):
    smh = SMHiggs.GetBinContent( bin ) / higgsSF
    bkg = stack.GetStack().Last().GetBinContent( bin )
    if smh > 0. or bkg > 0. :
        sig = smh / math.sqrt( smh + bkg )
    else :
        sig = 0.
    if sig > 0.1 :
        Data.SetBinContent( bin, 0. )
        Data.SetBinError( bin, 0. )
   Data.Draw("esamex0")

   legende=make_legend()
   legende.AddEntry(Data,"Observed","elp")
   legende.AddEntry(ZTT,"Z#rightarrow#tau_{h}#tau_{h}","f")
   if not "2bjet" in cat :
    legende.AddEntry(ZL,"DY others","f")
   legende.AddEntry(TT,"t#bar{t}+jets","f")
   legende.AddEntry(VV,"Electroweak","f")
   legende.AddEntry(QCD,"QCD multijet","f")
   legende.AddEntry(SMHiggs,"SM h(125) x %s" % higgsSF,"f")
   legende.AddEntry(errorBand,"Uncertainty","f")
   legende.Draw()

   l1=add_lumi()
   l1.Draw("same")
   l2=add_CMS()
   l2.Draw("same")
   l3=add_Preliminary()
   l3.Draw("same")
 
   pad1.RedrawAxis()

   categ  = ROOT.TPaveText(0.21, 0.5+0.013, 0.43, 0.70+0.155, "NDC")
   categ.SetBorderSize(   0 )
   categ.SetFillStyle(    0 )
   categ.SetTextAlign(   12 )
   categ.SetTextSize ( 0.06 )
   categ.SetTextColor(    1 )
   categ.SetTextFont (   41 )
   categ.AddText(cat)
   categ.Draw("same")

   c.cd()
   pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
   pad2.SetTopMargin(0.05);
   pad2.SetBottomMargin(0.35);
   pad2.SetLeftMargin(0.18);
   pad2.SetRightMargin(0.05);
   pad2.SetTickx(1)
   pad2.SetTicky(1)
   pad2.SetFrameLineWidth(3)
   pad2.SetGridx()
   pad2.SetGridy()
   pad2.Draw()
   pad2.cd()
   h1=Data.Clone()
   #h1.SetMaximum(1.5)#FIXME(1.5)
   #h1.SetMinimum(0.5)#FIXME(0.5)
   h1.SetMaximum(1.75)#FIXME(1.5)
   h1.SetMinimum(0.25)#FIXME(0.5)
   h1.SetMarkerStyle(20)
   h3=errorBand.Clone()
   hwoE=errorBand.Clone()
   for iii in range (1,hwoE.GetSize()-2):
     hwoE.SetBinError(iii,0)
   h3.Sumw2()
   h1.Sumw2()
   h1.SetStats(0)
   h1.Divide(hwoE)
   h3.Divide(hwoE)
   h1.GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
   #h1.GetXaxis().SetTitle("m_{vis} (GeV)")
   #h1.GetXaxis().SetTitle("N_{charged}")
   h1.GetXaxis().SetLabelSize(0.08)
   h1.GetYaxis().SetLabelSize(0.08)
   h1.GetYaxis().SetTitle("Obs./Exp.")
   h1.GetXaxis().SetNdivisions(505)
   h1.GetYaxis().SetNdivisions(5)

   h1.GetXaxis().SetTitleSize(0.15)
   h1.GetYaxis().SetTitleSize(0.15)
   h1.GetYaxis().SetTitleOffset(0.56)
   h1.GetXaxis().SetTitleOffset(1.04)
   h1.GetXaxis().SetLabelSize(0.11)
   h1.GetYaxis().SetLabelSize(0.11)
   h1.GetXaxis().SetTitleFont(42)
   h1.GetYaxis().SetTitleFont(42)

   h1.Draw("ep")
   h3.Draw("e2same")

   c.cd()
   pad1.Draw()

   ROOT.gPad.RedrawAxis()

   c.Modified()
   #c.SaveAs("mVis"+cat+args.mthd+".pdf")
   #c.SaveAs("mVis"+cat+args.mthd+".png")
   date='Nov02'
   c.SaveAs("/afs/cern.ch/user/t/truggles/www/2D/"+date+"/mSV"+cat+args.mthd+".pdf")
   c.SaveAs("/afs/cern.ch/user/t/truggles/www/2D/"+date+"/mSV"+cat+args.mthd+".png")
   pad1.SetLogy()
   del legende
   Data.SetMaximum(Data.GetMaximum()*3)
   Data.SetMinimum(0.01)
   pad1.Update()
   c.SaveAs("/afs/cern.ch/user/t/truggles/www/2D/"+date+"/mSV"+cat+args.mthd+"log.pdf")
   c.SaveAs("/afs/cern.ch/user/t/truggles/www/2D/"+date+"/mSV"+cat+args.mthd+"log.png")


