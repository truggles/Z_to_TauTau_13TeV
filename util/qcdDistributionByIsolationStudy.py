import ROOT
import time
#import pyplotter.tdrstyle as tdr
import math
from collections import OrderedDict
ROOT.gROOT.SetBatch(True)
#tdr.setTDRStyle()
ROOT.gStyle.SetOptStat(0)


def symmTH2( th2 ) :
    th2new = ROOT.TH2D( th2.GetName()+'_', th2.GetTitle()+'_',plotBins[0],\
            plotBins[1],plotBins[2],plotBins[0],plotBins[1],plotBins[2])
    th2new.Sumw2()
    for i in range(1, th2.GetXaxis().GetNbins()+1) :
        #print "%i x" % i
        for j in range(1, th2.GetYaxis().GetNbins()+1) :
            #print "%i y" % j
            if i == j :
                th2new.SetBinContent( i, j, th2.GetBinContent( i, j ) )
                th2new.SetBinError( i, j, th2.GetBinError( i, j ) )
                #print "Init uncert:",th2.GetBinError( i, j )
                #print "After uncert:",th2new.GetBinError( i, j )
            if i > j : 
                lower = th2.GetBinContent( i, j )
                upper = th2.GetBinContent( j, i )
                th2new.SetBinContent( i, j, lower + upper )
                lower = th2.GetBinError( i, j )
                upper = th2.GetBinError( j, i )
                error = math.sqrt( lower**2 + upper**2 )
                th2new.SetBinError( i, j, error )
                #print "Init uncert1:",th2.GetBinError( i, j )
                #print "Init uncert2:",th2.GetBinError( j, i )
                #print "After uncert:",th2new.GetBinError( i, j )
    return th2new



def twoDTo1DMerge( th2 ) :
    th1 = ROOT.TH1D( th2.GetName()+'_1d', th2.GetTitle()+'_1d',\
            plotBins[0],plotBins[1],plotBins[2])
    th1.Sumw2()
    print "Merging:",th2.GetTitle()

    # Merge all x bins together for a given y value
    for j in range(1, th2.GetYaxis().GetNbins()+1) :
        #print "%i y" % j
        xTot = 0.
        xUncert = 0.
        for i in range(1, th2.GetXaxis().GetNbins()+1) :
            #print "%i x" % i
            xTot += th2.GetBinContent( i, j )
            xUncert += th2.GetBinError( i, j )**2
            #print " -- xTot: %.2f   uncert: %.2f" % (xTot, xUncert)
        #print " -- xTotF: %.2f   uncertF: %.2f" % (xTot, xUncert)
        th1.SetBinContent( j, xTot )
        th1.SetBinError( j, math.sqrt(xUncert) )
    return th1



def make2Ds( data, bkg, name= "", cut="" ) :
    #print data
    #print bkg
    dataH = ROOT.TH2D('dataH'+name,'dataH '+name,plotBins[0],\
            plotBins[1],plotBins[2],plotBins[0],plotBins[1],plotBins[2])
    bkgH = ROOT.TH2D('bkgH'+name,'bkgH '+name,plotBins[0],\
            plotBins[1],plotBins[2],plotBins[0],plotBins[1],plotBins[2])
    qcdH = ROOT.TH2D('qcdH'+name,'qcdH '+name,plotBins[0],\
            plotBins[1],plotBins[2],plotBins[0],plotBins[1],plotBins[2])

    mcWeight = '*(weight)*(tauIDweight_1 * tauIDweight_2)*(GenWeight/abs( GenWeight ))*(XSecLumiWeight)'

    data.Draw( plotVar+' >> dataH'+name,cut,'COLZ' )
    dataH.SetDirectory( 0 )
    bkg.Draw( plotVar+' >> bkgH'+name,cut+mcWeight,'COLZ' )
    bkgH.SetDirectory( 0 )

    # Combine like isolations
    data2 = symmTH2( dataH )
    bkg2 = symmTH2( bkgH )
    
    qcdH.Add( data2, bkg2, 1.0, -1.0 )
    qcdH.SetDirectory( 0 )
    #print "Data: ",dataH.Integral()
    #print "Bkg: ",bkgH.Integral()
    print "Data2: ",data2.Integral()
    print "Bkg2: ",bkg2.Integral()
    print "QCD: ",qcdH.Integral()

    # Set bin labels
    for h in [data2, bkg2, qcdH] :
        setBinLabels( h )
    return qcdH,data2,bkg2



def setBinLabels( thx ) :
    binLabels = ['<VVL', 'VVL', 'VL', 'L', 'M', 'T', 'VT', 'VVT']
    if thx.GetXaxis().GetNbins() == 8 : # n Bins for MVA Iso WP dist
        if thx.IsA() == ROOT.TH2D.Class() :
            thx.GetXaxis().SetTitle('#tau_{h} MVA Isolation WP')
            thx.GetYaxis().SetTitle('Anti-Isolated #tau_{h} MVA Isolation WP')
            for i in range(1, thx.GetXaxis().GetNbins()+1) :
                thx.GetXaxis().SetBinLabel( i, binLabels[i-1] )
                thx.GetYaxis().SetBinLabel( i, binLabels[i-1] )
        if thx.IsA() == ROOT.TH1D.Class() :
            thx.GetXaxis().SetTitle('Anti-Isolated #tau_{h} MVA Isolation WP')
            thx.GetYaxis().SetTitle('OS/SS Ratio')
            for i in range(1, thx.GetXaxis().GetNbins()+1) :
                thx.GetXaxis().SetBinLabel( i, binLabels[i-1] )
    else :
        if thx.IsA() == ROOT.TH2D.Class() :
            thx.GetXaxis().SetTitle('#tau_{h} MVA Iso Raw')
            thx.GetYaxis().SetTitle('Anti-Isolated #tau_{h} MVA Iso Raw')
        if thx.IsA() == ROOT.TH1D.Class() :
            thx.GetXaxis().SetTitle('Anti-Isolated #tau_{h} MVA Iso Raw')
            thx.GetYaxis().SetTitle('OS/SS Ratio')





bkgFile = ROOT.TFile('QCDStudies/BKGS.root','r')
bkg = bkgFile.Get('Ntuple')

dataFile = ROOT.TFile('QCDStudies/dataTT.root','r')
data = dataFile.Get('Ntuple')



isoT = 'Tight'
isoL = 'Loose'
#isoL1ML2loose = '((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5)\
#|| (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_1 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_1 > 0.5))' % (isoT, isoL, isoT, isoL)

iso = '*((by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_2 > 0.5) || (by%sIsolationMVArun2v1DBoldDMwLT_1 < 0.5 && by%sIsolationMVArun2v1DBoldDMwLT_1 > 0.5))' % (isoT, isoL, isoT, isoL)
iso = '*(by%sIsolationMVArun2v1DBoldDMwLT_2 < 0.5 || by%sIsolationMVArun2v1DBoldDMwLT_1 < 0.5)' % (isoT, isoT)

higgsPtVar = 'Higgs_Pt'
#higgsPtVar = 'pt_sv'
categoryAndCut = {
    'Inclusive' : '(pt_1 > 50 && pt_2 > 40)%s' % iso,
    'Boosted' : '(pt_1 > 50 && pt_2 > 40)*(jetVeto30==1 || ((jetVeto30>=2)*!(abs(jdeta) > 2.5 && njetingap < 1 && %s>100)))%s' % (higgsPtVar, iso),
    'VBF' : '(pt_1 > 50 && pt_2 > 40)*(jetVeto30>=2)*(%s>100)*(abs(jdeta)>2.5 && njetingap<1)%s' % (higgsPtVar, iso),
}

plotVar = 'isoCode1:isoCode2'
plotBins = [8,0,8]
#plotVar = 'iso_1:iso_2'
#plotBins = [10,-0.4,1]
etaMap = {
    #'All Eta' : '',
    ' ' : '',
    #'Both Barrel' : '*(abs(eta_1) < 1.5 && abs(eta_2) < 1.5)',
    #'Both Endcap' : '*(abs(eta_1) >= 1.5 && abs(eta_2) >= 1.5)',
    #'Mixed Eta' : '*((abs(eta_1) >= 1.5 && abs(eta_2) < 1.5) || (abs(eta_1) < 1.5 && abs(eta_2) >= 1.5))',
}

boostMap = OrderedDict()
boostMap['all Pt Higgs Pt'  ] = '*(1)'
boostMap['0-100 GeV Higgs Pt'  ] = '*(Higgs_Pt <= 100)'
boostMap['100-170 GeV Higgs Pt'] = '*(Higgs_Pt > 100 && Higgs_Pt <= 170)'
#boostMap['170-300 GeV Higgs Pt'] = '*(Higgs_Pt > 170 && Higgs_Pt <= 300)'
#boostMap['300+ GeV Higgs Pt'] = '*(Higgs_Pt > 300)'
boostMap['170+ GeV Higgs Pt'] = '*(Higgs_Pt > 170)'

mjjMap = OrderedDict()
mjjMap['all Pt di-Jet Mass'  ] = '*(1)'
mjjMap['0-300 GeV di-Jet Mass'  ] = '*(mjj <= 300)'
mjjMap['300-500 GeV di-Jet Mass'] = '*(mjj > 300 && mjj <= 500)'
#mjjMap['500-800 GeV di-Jet Mass'] = '*(mjj > 500 && mjj <= 800)'
#mjjMap['800+ GeV di-Jet Mass'] = '*(mjj > 800)'
mjjMap['500+ GeV di-Jet Mass'] = '*(mjj > 500)'

saveDir = '/afs/cern.ch/user/t/truggles/www/tmp/QCDStudy/Nov25/'

histos = {}
for etaName, etaCut in etaMap.iteritems() :
    for cat in categoryAndCut.keys() :
        print cat
        cut = categoryAndCut[cat]
        histos[cat] = {}
        histos1d = []
        for boost, bCut in boostMap.iteritems() :
        #for boost, bCut in mjjMap.iteritems() :
            bCut += etaCut
            histos[cat][boost] = {}
            for sign, num in {'OS':0, 'SS':1}.iteritems() :
                print sign
                Zsign = '*(Z_SS==%i)' % num
                newCut = cut + Zsign + bCut
                #print "  -- ",newCut
                #newCut += '*(byVVTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5 && byVVTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)'
                newCut += '*(m_vis>100)'
    
                # 2D histos
                qcdH,dataH,bkgH = make2Ds( data, bkg, cat+sign+boost, newCut )
                # 1D histos
                data1d = twoDTo1DMerge( dataH )
                bkg1d = twoDTo1DMerge( bkgH )
                qcd1d = ROOT.TH1D( cat+sign+boost+'qcd', cat+sign+boost+'qcd',\
                        plotBins[0],plotBins[1],plotBins[2])
                qcd1d.Add( data1d, bkg1d, 1.0, -1.0 )
                histos[cat][boost][sign] = [qcdH, dataH, bkgH, qcd1d, data1d, bkg1d]
                c2 = ROOT.TCanvas('c2','c2',600,600)
                p1 = ROOT.TPad('p1', 'p1', 0,0,1,1)
                p1.Draw()
                #p1.SetRightMargin(0.2)
                #p1.Update()
    
                ### Some good verification plots
                qcdH.Draw('COLZ text')
                c2.SaveAs(saveDir+cat+boost.replace(' ','_')+sign+'_QCD.png')
                dataH.Draw('COLZ text')
                c2.SaveAs(saveDir+cat+boost.replace(' ','_')+sign+'_Data.png')
                bkgH.Draw('COLZ text')
                c2.SaveAs(saveDir+cat+boost.replace(' ','_')+sign+'_MC.png')
                #bkg1d.Draw()
                #c2.SaveAs(saveDir+'1d_bkgh'+cat+boost.replace(' ','_')+sign+'.png')
                #data1d.Draw()
                #c2.SaveAs(saveDir+'1d_datah'+cat+boost.replace(' ','_')+sign+'.png')
                #qcd1d.Draw()
                #c2.SaveAs(saveDir+'1d_qcdh'+cat+boost.replace(' ','_')+sign+'.png')
                
            # 2D os / ss
            osVSss = ROOT.TH2D( 'OSvSS'+cat+boost, 'OSvSS '+cat+' '+boost, plotBins[0],\
                    plotBins[1],plotBins[2],plotBins[0],plotBins[1],plotBins[2])
            osVSss.Add( histos[cat][boost]['OS'][0] )
            osVSss.Divide( histos[cat][boost]['SS'][0] )
            setBinLabels( osVSss )
            osVSss.Draw('COLZ text')
            c2.SaveAs(saveDir+'raw_2d_osOverSS_'+cat+boost.replace(' ','_')+'.png')
            c2.SaveAs(saveDir+'raw_2d_osOverSS_'+cat+boost.replace(' ','_')+'.pdf')
    
            # 1D os / ss
            osVSss1d = ROOT.TH1D( 'OSvSS1d'+cat+boost, boost,plotBins[0],plotBins[1],plotBins[2])
            osVSss1d.Add(histos[cat][boost]['OS'][3] )
            osVSss1d.Divide(histos[cat][boost]['SS'][3])
            osVSss1d.Draw()
            setBinLabels( osVSss1d )
            #c2.SaveAs(saveDir+'1d_osOverSS_'+cat+boost+'.png')
            histos1d.append( osVSss1d )
    
        # Final 1D os / ss plot with all categories
        c3 = ROOT.TCanvas('c3','c3',600,600)
        p3 = ROOT.TPad('p3', 'p3', 0,0,1,1)
        p3.Draw()
        p3.cd()
        maxi = 0.
        for i, h in enumerate(histos1d) :
            if h.GetMaximum() > maxi : maxi = h.GetMaximum()
            h.SetLineColor( i+1 )
            h.SetLineWidth( 2 )
            if i == 0 :
                h.Draw('E1')
                setBinLabels( h )
            else : h.Draw('E1 SAME')
            print i, h
    
        if maxi > 10 : 
            print "\n\n\nMax was %.1f.  Max was set to 10\n\n" % maxi
            maxi = 10
        histos1d[0].SetMaximum( maxi * 1.3 )
        histos1d[0].SetTitle( 'OS/SS '+cat+' Cat. '+etaName )
        p3.BuildLegend( .6, .65, .95, .9 )
        #p3.SetLogy()
        histos1d[0].SetMaximum(5)
        #histos1d[0].SetMinimum(0.5)
        p3.Update()
        #c3.SaveAs(saveDir+etaName.replace(' ','_')+'_mjj_1dComb_osOverSS_'+cat+'.png')
        #c3.SaveAs(saveDir+etaName.replace(' ','_')+'_mjj_1dComb_osOverSS_'+cat+'.pdf')
        #c3.SaveAs(saveDir+etaName.replace(' ','_')+'_boostDef_noMVisCut_1dComb_osOverSS_'+cat+'.png')
        #c3.SaveAs(saveDir+etaName.replace(' ','_')+'_boostDef_noMVisCut_1dComb_osOverSS_'+cat+'.pdf')
        c3.SaveAs(saveDir+etaName.replace(' ','_')+'_boostDef_1dComb_osOverSS_'+cat+'.png')
        c3.SaveAs(saveDir+etaName.replace(' ','_')+'_boostDef_1dComb_osOverSS_'+cat+'.pdf')
        
        



