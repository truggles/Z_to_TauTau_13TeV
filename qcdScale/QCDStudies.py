import ROOT
from ROOT import gPad
from array import array

ROOT.gROOT.SetBatch(True)

def addDetails( hist ) :
    hist.SetStats(0)
    hist.GetXaxis().SetTitle("Leading #tau_{h} DBIsoRawComb3Hits")
    hist.GetYaxis().SetTitle("Secondary #tau_{h} DBIsoRawComb3Hits")


#f = ROOT.TFile('mcTT.root','READ')
#t = f.Get('Ntuple')
#hist = ROOT.TH2F('h1','h1',5,xBin,5,xBin)
#t.Draw('iso_1:iso_2>>h1','','colz')
#c2 = ROOT.TCanvas('c2','c2',600,600)
#p1 = ROOT.TPad('p1','p1',0,0,1,1)
#p1.Draw()
#p1.cd()
#hist.Draw('colz text')
#
##hist.SaveAs('temper.root')
#c2.SaveAs('/afs/cern.ch/user/t/truggles/www/qcdScale/4x4yyy.png')

cutMap = {
    "NoSign" : "",
    "SS" : "*(Z_SS==1)",
    "OS" : "*(Z_SS==0)",
}

xBin = array('d', [0,1,3,4.5,7,10])

def go() :
    fd = ROOT.TFile("dataTT.root","READ")
    Td = fd.Get("Ntuple")
    fmc = ROOT.TFile("mcTT.root","READ")
    Tmc = fmc.Get("Ntuple")
    fqcd = ROOT.TFile("qcdTT.root","READ")
    Tqcd = fqcd.Get("Ntuple")
    
    iso = "((iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5))"
    XSec = "*( (GenWeight/abs(GenWeight)) * XSecLumiWeight * puweight )"
    isoMC = "%s%s" % (iso, XSec)
    for cut in cutMap.keys() :
        dataCut = "%s%s" % (iso, cutMap[ cut ])
        mcCut = "%s%s" % (isoMC, cutMap[ cut ])

        c2 = ROOT.TCanvas("c2","c2",800,800)
        p2 = ROOT.TPad("p2","p2",0,0,1,1)
        p2.Divide(2,2)
        p2.Draw()
        p2.cd(1)
        hData = ROOT.TH2F("hData","Raw Data",5,xBin,5,xBin)
        Td.Draw("iso_1:iso_2>>hData",dataCut)
        addDetails( hData )
        hData.Draw("colz text")
        p2.cd(2)
        hMC = ROOT.TH2F("hMC","NonQCD MC",5,xBin,5,xBin)
        Tmc.Draw("iso_1:iso_2>>hMC",mcCut)
        addDetails( hMC )
        hMC.Draw("colz text")
        p2.cd(3)
        hQCDmc = ROOT.TH2F("hQCDmc","QCD (MC sample)",5,xBin,5,xBin)
        Tqcd.Draw("iso_1:iso_2>>hQCDmc",mcCut)
        addDetails( hQCDmc )
        hQCDmc.Draw("colz text")
        p2.cd(4)
        hQCDdd = ROOT.TH2F("hQCDdd","QCD (data - MC)",5,xBin,5,xBin)
        hQCDdd.Add( hData )
        mcInv = hMC.Clone()
        mcInv.Scale( -1 )
        hQCDdd.Add( mcInv )
        addDetails( hQCDdd )
        hQCDdd.Draw("colz text")
        c2.SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcdPlots/quad_%s.png" % cut )
        
        c3 = ROOT.TCanvas("c3","c3",800,800)
        p3 = ROOT.TPad("p3","p3",0,0,1,1)
        p3.Draw()
        p3.cd()
        ratio = ROOT.TH2F("ratio","data / MC",5,xBin,5,xBin)
        ratio.Add( hQCDdd )
        ratio.Divide( hData )
        addDetails( ratio )
        ratio.Draw("colz text")
        c3.SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcdPlots/ratio_%s.png" % cut )

go()
