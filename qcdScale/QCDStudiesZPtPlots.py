import ROOT
from ROOT import gPad
from array import array

ROOT.gROOT.SetBatch(True)

# Canvas dimensions
cw = 1200
ch = 800

def addDetails( hist ) :
    hist.SetStats(0)
    hist.GetXaxis().SetTitle("Z p_{T}")
    #hist.GetYaxis().SetTitle("Secondary #tau_{h} p_{T}")


#xBin = array('d', [0,1,3,4.5,7,10])
xBin = array('d', [0,10,20,30,40,60,100,200])
#yBin = array('d', [45,55,65,75,100,150,200])
#yBin = array('d', [0,10])
xNum = len( xBin ) - 1
#yNum = len( yBin ) - 1

def getHistos( decay="", dStr="" ) :
    histos = {}

    fd = ROOT.TFile("dataTT.root","READ")
    Td = fd.Get("Ntuple")
    fmc = ROOT.TFile("mcTT.root","READ")
    Tmc = fmc.Get("Ntuple")
    fqcd = ROOT.TFile("qcdTT.root","READ")
    Tqcd = fqcd.Get("Ntuple")
    
    iso = "((iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5))"
    #XSec = "*( (GenWeight/abs(GenWeight)) * XSecLumiWeight)"# * puweight )"
    XSec = "*( (GenWeight/abs(GenWeight)) * XSecLumiWeight * puweight )"
    isoMC = "%s%s" % (iso, XSec)
    for cut in cutMap.keys() :
        dataCut = "%s%s%s" % (iso, cutMap[ cut ], dStr )
        mcCut = "%s%s%s" % (isoMC, cutMap[ cut ], dStr )

        c2 = ROOT.TCanvas("c2%s" % cut,"c2",cw,ch)
        p2 = ROOT.TPad("p2","p2",0,0,1,1)
        p2.Divide(2,2)
        p2.Draw()
        p2.cd(1)
        histos[cut + "hData"] = ROOT.TH1F("hData%s" % cut,"Raw Data: %s%s" % (cut,decay),xNum,xBin)
        Td.Draw("t1_t2_Pt>>hData%s" % cut, dataCut)
        addDetails( histos[cut + "hData"])
        histos[cut + "hData"].Draw("colz text")
        p2.cd(2)
        histos[cut + "hMC"] = ROOT.TH1F("hMC%s" % cut,"NonQCD MC: %s%s" % (cut,decay),xNum,xBin)
        Tmc.Draw("t1_t2_Pt>>hMC%s" % cut, mcCut)
        addDetails( histos[cut + "hMC"] )
        histos[cut + "hMC"].Draw("colz text")
        p2.cd(3)
        histos[cut + "hQCDmc"] = ROOT.TH1F("hQCDmc%s" % cut, "QCD (MC sample): %s%s" % (cut,decay),xNum,xBin)
        Tqcd.Draw("t1_t2_Pt>>hQCDmc%s" % cut, mcCut)
        addDetails( histos[cut + "hQCDmc"] )
        histos[cut + "hQCDmc"].Draw("colz text")
        p2.cd(4)
        histos[cut + "hQCDdd"] = ROOT.TH1F("hQCDdd%s" % cut, "QCD (data - MC): %s%s" % (cut,decay),xNum,xBin)
        histos[cut + "hQCDdd"].Add( histos[cut + "hData"] )
        mcInv = histos[cut + "hMC"].Clone()
        mcInv.Scale( -1 )
        histos[cut + "hQCDdd"].Add( mcInv )
        addDetails( histos[cut + "hQCDdd"] )
        histos[cut + "hQCDdd"].Draw("colz text")
        c2.SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcdZPtPlots/quad_%s%s.png" % (cut, decay) )
        
        c3 = ROOT.TCanvas("c3%s" % cut,"c3",cw,ch)
        p3 = ROOT.TPad("p3","p3",0,0,1,1)
        p3.Draw()
        p3.cd()
        ratio = ROOT.TH1F("ratio%s" % cut,"(data / MC): %s%s" % (cut, decay),xNum,xBin)
        ratio.Add( histos[cut + "hQCDdd"] )
        ratio.Divide( histos[cut + "hData"] )
        addDetails( ratio )
        ratio.Draw("colz text")
        c3.SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcdZPtPlots/ratio_%s%s.png" % (cut, decay) )

        c5 = ROOT.TCanvas("c5%s" % cut,"c5",cw,ch)
        p5 = ROOT.TPad("p5","p5",0,0,1,1)
        p5.Draw()
        p5.cd()
        histos[cut + "hData"].Draw("colz text")
        c5.SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcdZPtPlots/occupancy_%s%s.png" % (cut, decay) )


    c4 = ROOT.TCanvas("c4","c4",cw,ch)
    p4 = ROOT.TPad("p4","p4",0,0,1,1)
    p4.Draw()
    p4.cd()
    OSvsSS = ROOT.TH1F("OSvsSS", "DD QCD %s: OS / SS" % decay,xNum,xBin)
    #histos[ "OShQCDdd" ].SaveAs('tmp.root')
    OSvsSS.Add( histos[ "OShQCDdd" ] )
    OSvsSS.Divide( histos[ "SShQCDdd" ] )
    addDetails( OSvsSS )
    OSvsSS.Draw("colz text")
    c4.SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcdZPtPlots/OSvsSS-ddQCD%s.png" % decay)
    OSvsSS.SaveAs("roots/OSvsSS%s.root" % decay)
    histos[ "OShQCDdd" ].SaveAs("roots/OShQCDdd%s.root" % decay)
    histos[ "SShQCDdd" ].SaveAs("roots/SShQCDdd%s.root" % decay)


    return histos

cutMap = {
    "NoSign" : "",
    "SS" : "*(Z_SS==1)",
    #"SSdm00" : "*(Z_SS==1)*(t1DecayMode == 0)",
    #"SSdm01" : "*(Z_SS==1)*(t1DecayMode == 1)",
    #"SSdm10" : "*(Z_SS==1)*(t1DecayMode == 10)",
    "OS" : "*(Z_SS==0)",
}
decays = {
    #"dm0" : "*(t1DecayMode==0)",
    #"dm1" : "*(t1DecayMode==1)",
    #"dm10" : "*(t1DecayMode==10)",
    "isoL1" : "*(t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5)",
    "isoG3L10" : "*(iso_1 > 1 && iso_1 < 10)",
}

h = getHistos()
for decay in decays.keys() :
    histos = getHistos( decay, decays[ decay ] )
#for key in histos :
#    print key
