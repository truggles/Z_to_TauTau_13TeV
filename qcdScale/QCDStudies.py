import ROOT
from ROOT import gPad
from array import array

ROOT.gROOT.SetBatch(True)

def addDetails( hist ) :
    hist.SetStats(0)
    hist.GetXaxis().SetTitle("Leading #tau_{h} DBIsoRawComb3Hits")
    hist.GetYaxis().SetTitle("Secondary #tau_{h} DBIsoRawComb3Hits")


xBin = array('d', [0,1,3,4.5,7,10])

def getHistos( decay="", dStr="" ) :
    histos = {}

    fd = ROOT.TFile("dataTT.root","READ")
    Td = fd.Get("Ntuple")
    fmc = ROOT.TFile("mcTT.root","READ")
    Tmc = fmc.Get("Ntuple")
    fqcd = ROOT.TFile("qcdTT.root","READ")
    Tqcd = fqcd.Get("Ntuple")
    
    iso = "((iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5))"
    XSec = "*( (GenWeight/abs(GenWeight)) * XSecLumiWeight)"# * puweight )"
    isoMC = "%s%s" % (iso, XSec)
    for cut in cutMap.keys() :
        dataCut = "%s%s%s" % (iso, cutMap[ cut ], dStr )
        mcCut = "%s%s%s" % (isoMC, cutMap[ cut ], dStr )

        c2 = ROOT.TCanvas("c2%s" % cut,"c2",800,800)
        p2 = ROOT.TPad("p2","p2",0,0,1,1)
        p2.Divide(2,2)
        p2.Draw()
        p2.cd(1)
        histos[cut + "hData"] = ROOT.TH2F("hData%s" % cut,"Raw Data: %s%s" % (cut,decay),5,xBin,5,xBin)
        Td.Draw("iso_1:iso_2>>hData%s" % cut, dataCut)
        addDetails( histos[cut + "hData"])
        histos[cut + "hData"].Draw("colz text")
        p2.cd(2)
        histos[cut + "hMC"] = ROOT.TH2F("hMC%s" % cut,"NonQCD MC: %s%s" % (cut,decay),5,xBin,5,xBin)
        Tmc.Draw("iso_1:iso_2>>hMC%s" % cut, mcCut)
        addDetails( histos[cut + "hMC"] )
        histos[cut + "hMC"].Draw("colz text")
        p2.cd(3)
        histos[cut + "hQCDmc"] = ROOT.TH2F("hQCDmc%s" % cut, "QCD (MC sample): %s%s" % (cut,decay),5,xBin,5,xBin)
        Tqcd.Draw("iso_1:iso_2>>hQCDmc%s" % cut, mcCut)
        addDetails( histos[cut + "hQCDmc"] )
        histos[cut + "hQCDmc"].Draw("colz text")
        p2.cd(4)
        histos[cut + "hQCDdd"] = ROOT.TH2F("hQCDdd%s" % cut, "QCD (data - MC): %s%s" % (cut,decay),5,xBin,5,xBin)
        histos[cut + "hQCDdd"].Add( histos[cut + "hData"] )
        mcInv = histos[cut + "hMC"].Clone()
        mcInv.Scale( -1 )
        histos[cut + "hQCDdd"].Add( mcInv )
        addDetails( histos[cut + "hQCDdd"] )
        histos[cut + "hQCDdd"].Draw("colz text")
        c2.SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcdPlots/quad_%s%s.png" % (cut, decay) )
        
        c3 = ROOT.TCanvas("c3%s" % cut,"c3",600,600)
        p3 = ROOT.TPad("p3","p3",0,0,1,1)
        p3.Draw()
        p3.cd()
        ratio = ROOT.TH2F("ratio%s" % cut,"(data / MC): %s%s" % (cut, decay),5,xBin,5,xBin)
        ratio.Add( histos[cut + "hQCDdd"] )
        ratio.Divide( histos[cut + "hData"] )
        addDetails( ratio )
        ratio.Draw("colz text")
        c3.SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcdPlots/ratio_%s%s.png" % (cut, decay) )


    c4 = ROOT.TCanvas("c4","c4",600,600)
    p4 = ROOT.TPad("p4","p4",0,0,1,1)
    p4.Draw()
    p4.cd()
    OSvsSS = ROOT.TH2F("OSvsSS", "DD QCD %s: OS / SS" % decay,5,xBin,5,xBin)
    #histos[ "OShQCDdd" ].SaveAs('tmp.root')
    OSvsSS.Add( histos[ "OShQCDdd" ] )
    OSvsSS.Divide( histos[ "SShQCDdd" ] )
    addDetails( OSvsSS )
    OSvsSS.Draw("colz text")
    c4.SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcdPlots/OSvsSS-ddQCD%s.png" % decay)


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
    "dm0" : "*(t1DecayMode==0)",
    "dm1" : "*(t1DecayMode==1)",
    "dm10" : "*(t1DecayMode==10)",
}

h = getHistos()
for decay in decays.keys() :
    histos = getHistos( decay, decays[ decay ] )
#for key in histos :
#    print key
