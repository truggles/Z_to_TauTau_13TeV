import ROOT
from ROOT import gPad
from array import array
from util.buildTChain import makeTChain

ROOT.gROOT.SetBatch(True)

# Canvas dimensions
cw = 400
ch = 400

def addDetails( hist ) :
    #hist.SetStats(0)
    hist.GetXaxis().SetTitle("#Tau p_{T}")

def savePlot( name, hist ) :
    cx = ROOT.TCanvas(name,"cx",cw,ch)
    px = ROOT.TPad("p%s" % name,"px",0,0,1,1)
    px.Draw()
    px.cd()
    addDetails( hist )
    hist.GetYaxis().SetTitle("Events")
    hist.Draw("hist")
    cx.SaveAs("/afs/cern.ch/user/t/truggles/www/triggerStudies/%s.png" % name)
    
def saveEffPlots( name, hist1, hist2 ) :
    cx = ROOT.TCanvas(name,"cx",cw,ch)
    px = ROOT.TPad("p%s" % name,"px",0,0,1,1)
    px.Draw()
    px.cd()
    addDetails( hist1 )
    hist1.SetStats(0)
    hist2.SetStats(0)
    hist1.GetYaxis().SetTitle("Passing / Initial Selection")
    hist1.SetLineColor( ROOT.kBlack )
    hist2.SetLineColor( ROOT.kRed )
    hist1.Draw("hist")
    hist2.Draw("hist same")
    px.BuildLegend()
    maxi = hist1.GetMaximum()
    if hist2.GetMaximum() > maxi : maxi = hist2.GetMaximum()
    hist1.SetMaximum( maxi * 1.4 )
    cx.SaveAs("/afs/cern.ch/user/t/truggles/www/triggerStudies/%s.png" % name)
    


xBin = array('d', [10,15,20,22.5,25,27.5,30,32.5,35,37.5,40,42.5,45,47.5,50,52.5,55,57.5,60,65,70,80,90,100,110,200])
xNum = len( xBin ) - 1

def getHistos( trigger="", dStr="" ) :
    histos = {}

    fileMin = 0
    fileMax = 9999
    dataList = 'data_trig.txt'
    path = 'Ntuple'
    Td = makeTChain( dataList, path, 0, fileMin, fileMax )
    mcList = 'ggHtoTauTau.txt'
    Tmc = makeTChain( mcList, path, 0, fileMin, fileMax )
    
    bkgElim = "( 1*(Z_SS == 0) - 1*(Z_SS == 1))"
    genAndPU = "*( (GenWeight/abs(GenWeight)) * puweight )"
    allMC = "%s%s" % (bkgElim, genAndPU)
    allData = bkgElim
    isoTau20 = '*(mMatchesIsoMu17LooseIsoTau20Path > 0.5)'
    isoTau35 = '*(mMatchesIsoMu17MedIsoTau35Path > 0.5)'
    plotNames = ['Denominator', 'IsoTau20', 'IsoTau35', 'IsoTau20Eff', 'IsoTau35Eff']

    for name in plotNames :
        histos["d%s" % name] = ROOT.TH1F("d%s" % name,"Data: %s" % name,xNum,xBin)
        histos["mc%s" % name] = ROOT.TH1F("mc%s" % name,"ggHtoTauTau: %s" % name,xNum,xBin)
    Td.Draw("pt_2>>dDenominator", allData)
    Tmc.Draw("pt_2>>mcDenominator", allMC)
    Td.Draw("pt_2>>dIsoTau20", "%s%s" % (allData, isoTau20) )
    Tmc.Draw("pt_2>>mcIsoTau20", "%s%s" % (allMC, isoTau20) )
    Td.Draw("pt_2>>dIsoTau35", "%s%s" % (allData, isoTau35) )
    Tmc.Draw("pt_2>>mcIsoTau35", "%s%s" % (allMC, isoTau35) )
    histos["dIsoTau20Eff"].Add( histos["dIsoTau20"] )
    histos["dIsoTau20Eff"].Divide( histos["dDenominator"] )
    histos["dIsoTau35Eff"].Add( histos["dIsoTau35"] )
    histos["dIsoTau35Eff"].Divide( histos["dDenominator"] )
    histos["mcIsoTau20Eff"].Add( histos["mcIsoTau20"] )
    histos["mcIsoTau20Eff"].Divide( histos["mcDenominator"] )
    histos["mcIsoTau35Eff"].Add( histos["mcIsoTau35"] )
    histos["mcIsoTau35Eff"].Divide( histos["mcDenominator"] )
    for hist in histos.keys() :
        if "Eff" not in hist :
            savePlot( hist, histos[hist] )
        elif hist[:1] == 'd' :
            nm = hist[1:]
            saveEffPlots( nm, histos[hist], histos[ 'mc' + nm ] ) 

    return histos

h = getHistos()
