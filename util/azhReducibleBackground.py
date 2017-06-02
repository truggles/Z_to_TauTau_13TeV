import ROOT
import os
from util.helpers import checkDir
import analysis1BaselineCuts
from meta.sampleNames import returnSampleDetails
from util.helpers import setUpDirs 
import pyplotter.tdrstyle as tdr
import subprocess



def buildRedBkgFakeFunctions( inSamples, **params ) :
    analysis = 'azh'
    params['doRedBkg'] = True
    params['mid1'] = params['mid1']+'RedBkg'
    params['mid2'] = params['mid2']+'RedBkg'
    params['mid3'] = params['mid3']+'RedBkg'
    dir2 = 'azh'+params['mid2']

    setUpDirs( inSamples, params, analysis ) # Print config file and set up dirs
    inSamples = returnSampleDetails( analysis, inSamples )

    # Only do Red Bkg method on data
    samples = {}
    for samp, val in inSamples.iteritems() :
        if 'data' in samp : samples[samp] = val
    #print samples

#    # Apply initial Reducible Bkg Cuts for inclusive selection
#    analysis1BaselineCuts.doInitialCuts(analysis, samples, **params)
#    # Order events and choose best interpretation
#    analysis1BaselineCuts.doInitialOrder(analysis, samples, **params)
#
#    # HADD each channel together so we can avoid different data runs
#    for channel in params['channels'] :
#        print "HADD for",channel
#        subprocess.call(["bash","./util/haddRedBkg.sh",dir2,channel])

    # Next try without drawHistos
    # Red Bkg Obj : Channels providing stats
    redBkgMap = {
        'tau' : ['eeet', 'eett', 'eemt', 'emmt', 'mmtt', 'mmmt'],
        'tau-lltt' : ['eett', 'mmtt'],
        'tau-lllt' : ['eeet', 'eemt', 'emmt', 'mmmt'],
        'electron' : ['eeet', 'emmt'],
        'muon' : ['eemt', 'mmmt'],
    }

    fakeRateMap = {}
    for obj, chans in redBkgMap.iteritems() :
        tmpMap = doRedBkgPlots( obj, chans, dir2 )
        for name, info in tmpMap.iteritems() :
            fakeRateMap[name] = info

    # Save fits to out file
    outFile = ROOT.TFile('data/azhFakeRateFits.root', 'RECREATE')
    for name, info in fakeRateMap.iteritems() :
        func = info[0]
        func.SetName( name+'_fit' )
        func.SetTitle( 'Fake Rate Fit: '+name )
        func.Write()
        graph = info[1]
        graph.SetName( name+'_graph' )
        graph.SetTitle( 'Fake Rate Fit: '+name )
        graph.Write()
    outFile.Close()


def doRedBkgPlots( obj, channels, inputDir ) :

    cmsLumi = float(os.getenv('LUMI'))/1000
    print "Lumi = %.1f / fb" % cmsLumi
    print "doing Red Bkg Plots for",obj
    print channels

    binInfo = [50, 0, 200]

    saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/June02'
    checkDir( saveDir )

    c1 = ROOT.TCanvas("c1","c1", 550, 550)
    pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
    pad1.Draw()
    pad1.cd()

    # Master histos
    xAxis = 'Jet p_{T} [GeV]'
    yAxis1 = 'Events / %i GeV' % ( (binInfo[2] - binInfo[1]) / binInfo[0] )
    yAxis2 = 'Fake Rate'
    denomAll = ROOT.TH1D( obj+'_denom', obj+'_denom;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
    passAll = ROOT.TH1D( obj+'_pass', obj+'_pass;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
    denomAll.Sumw2()
    passAll.Sumw2()

    # Channel leg map
    prodMap = {
        'eeem' : ('e3', 'm'),
        'eeet' : ('e3', 't'),
        'eemt' : ('m', 't'),
        'eett' : ('t1', 't2'),
        'emmm' : ('e', 'm3'),
        'emmt' : ('e', 't'),
        'mmmt' : ('m3', 't'),
        'mmtt' : ('t1', 't2'),
        'eeee' : ('e3', 'e4'),
        'eemm' : ('m1', 'm2'),
        'mmmm' : ('m3', 'm4'),
    }

    cuts = {
        'tau' : {
            'denom' : ['(1)',],
            'pass' : ['byMediumIsolationMVArun2v1DBoldDMwLT_Num > 0.5',],
        },
        'electron' : {
            'denom' : ['pfmt_3 < 30',], # to suppress real leptons from WZ and ZZ
            'pass' : ['iso_Num < 0.3', 'id_e_mva_nt_loose_Num > 0.5'],
        },
        'muon' : {
            'denom' : ['pfmt_3 < 30',], # to suppress real leptons from WZ and ZZ
            'pass' : ['iso_Num < 0.25', 'cand_PFIDLoose > 0.5'],
        },
    } 

    etaCuts = {
        'tau' : {
            'Barrel' : 'abs( eta_Num ) <= 1.4',
            'Endcap' : 'abs( eta_Num ) > 1.4',
            'AllEta' : '(1)',
        },
        'electron' : {
            'Barrel' : 'abs( eta_Num ) <= 1.4',
            'Endcap' : 'abs( eta_Num ) > 1.4',
            'AllEta' : '(1)',
        },
        'muon' :{
            'Barrel' : 'abs( eta_Num ) <= 1.4',
            'Endcap' : 'abs( eta_Num ) > 1.4',
            'AllEta' : '(1)',
        },
    }

    frMap = {}

    for etaRegion, etaCut in etaCuts[obj.split('-')[0]].iteritems() :
    # obj.split('-')[0] is to get the same cuts and mapping for
    # tau, tau-lltt, tau-lllt

        # If channels are lltt, then add an LT cut that is not present
        # for the other tau FRs
        if channels == ['eett', 'mmtt'] :
            cuts['tau']['denom'].append('LT_higgs > 50')

        denomCut = ' && '.join( cuts[obj.split('-')[0]]['denom'] )
        denomCut += ' && '+etaCut
        passCut = ' && '.join( cuts[obj.split('-')[0]]['pass'] )
        passCut = denomCut+' && '+passCut

        for channel in channels :
            print channel
            f = ROOT.TFile( inputDir+'/redBkg_'+channel+'.root', 'r' )
            t = f.Get('Ntuple')

            # check if first letter of 'obj' in leg3 then leg4 and draw if so
            for i, leg in enumerate(prodMap[channel]) :

                if not obj[0] in leg : continue

                # Replace vals in the passCut to match leg
                denomCutX = denomCut.replace( '_Num', '_%i' % (i+3) ) # i begins at 0, we being with leg3
                denomCutX = denomCutX.replace( 'cand_', leg ) # For vars we didn't use in sync ntuple
                passCutX = passCut.replace( '_Num', '_%i' % (i+3) ) # i begins at 0, we being with leg3
                passCutX = passCutX.replace( 'cand_', leg ) # For vars we didn't use in sync ntuple
                print "Denom Cut:",denomCutX
                print "Passing Cut:",passCutX

                # Denominator selection
                hTmp = ROOT.TH1D( 'hTmp', 'hTmp', binInfo[0], binInfo[1], binInfo[2] )
                t.Draw( leg+'JetPt >> hTmp', denomCutX )
                #print channel, leg, hTmp.Integral()
                denomAll.Add( hTmp )
                print " -- denomAll Int:",denomAll.Integral()

                # Passing selection
                hTmpPass = ROOT.TH1D( 'hTmpPass', 'hTmpPass', binInfo[0], binInfo[1], binInfo[2] )
                t.Draw( leg+'JetPt >> hTmpPass', passCutX )
                passAll.Add( hTmpPass )
                print " -- passAll Int:",passAll.Integral()
                del hTmp, hTmpPass


        #denomAll.SetMaximum( denomAll.GetMaximum() * 1.3 )
        #denomAll.Draw()
        #setText( obj+" Denominator", cmsLumi )
        #c1.SaveAs( saveDir+'/'+obj+'_'+etaRegion+'_Denominator.png' )
        #passAll.SetMaximum( passAll.GetMaximum() * 1.3 )
        #passAll.Draw()
        #setText( obj+" Passing", cmsLumi )
        #c1.SaveAs( saveDir+'/'+obj+'_'+etaRegion+'_Pass.png' )

        # Make Fake Rate plot
        graph = ROOT.TGraphAsymmErrors(passAll, denomAll)
        graph.GetXaxis().SetTitle(xAxis)
        graph.GetYaxis().SetTitle(yAxis2)
        graph.GetYaxis().SetTitle("Fake Rate")
        pad1.SetGrid()

        # For Log
        #pad1.SetLogy()
        #graph.SetMaximum( 10 )
        #graph.SetMinimum( 0.0005 )
        ## For Linear
        graph.SetMaximum( .25 )
        graph.SetMinimum( 0 )

        graph.Draw("AP")

        # do fit
        fitMin = binInfo[1] if binInfo[1] != 0 else 10
        f1 = ROOT.TF1( 'f1', '([0] + [1]*TMath::Exp(-[2]*x))', fitMin, binInfo[2])
        f1.SetParName( 0, "y rise" )
        f1.SetParName( 1, "scale" )
        f1.SetParName( 2, "decay" )
        if obj == 'electron' :
            f1.SetParameter( 0, 0. )
            f1.SetParameter( 1, .01 )
            f1.SetParameter( 2, .05 )
        else :
            f1.SetParameter( 0, 0. )
            f1.SetParameter( 1, 1. )
            f1.SetParameter( 2, .05 )
        graph.Fit('f1', 'S' )
        f2 = ROOT.TF1( 'f2', '([0] + [1]*TMath::Exp(-[2]*x))', binInfo[1], binInfo[2])
        f2.SetParameter( 0, f1.GetParameter( 0 ) )
        f2.SetParameter( 1, f1.GetParameter( 1 ) )
        f2.SetParameter( 2, f1.GetParameter( 2 ) )
        f2.Draw('SAME')

        ROOT.gStyle.SetStatX(.95)
        ROOT.gStyle.SetStatY(0.8)
        ROOT.gStyle.SetStatH(.2)
        ROOT.gStyle.SetStatW(.2)
        setText( "Fake Rate: %s %s" % (obj, etaRegion), cmsLumi )
        c1.SaveAs( saveDir+'/'+obj+'_'+etaRegion+'_FakeRate.png' )
        pad1.SetLogy(0)

        # Add FR fit to map
        frMap[obj+'_'+etaRegion] = [f2, graph]

    # Return map
    return frMap



def setText( text, cmsLumi ) :
    # Set CMS Styles Stuff
    logo = ROOT.TText(.2, .88,"CMS Preliminary")
    logo.SetTextSize(0.03)
    logo.DrawTextNDC(.2, .89,"CMS Preliminary")
    
    chan = ROOT.TLatex(.2, .80,"x")
    chan.SetTextSize(0.05)
    chan.DrawLatexNDC(.2, .84,"%s" % text )
    
    lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi.SetTextSize(0.03)
    lumi.DrawTextNDC(.7,.96,"%.1f / fb (13 TeV)" % cmsLumi )



if '__main__' in __name__ :
    
    ROOT.gROOT.SetBatch(True)
    tdr.setTDRStyle()
    
    dataSamples = []
    for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
        dataSamples.append('dataEE-%s' % era)
        dataSamples.append('dataMM-%s' % era)

    params = {
        #'debug' : 'true',
        'debug' : 'false',
        'numCores' : 15,
        'numFilesPerCycle' : 1,
        'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm','eeee','mmmm'], # 8 + eeee + mmmm + eemm
        #'channels' : ['eeet',],
        'cutMapper' : 'RedBkg',
        'mid1' : '1June02rb',
        'mid2' : '2June02rb',
        'mid3' : '3June02rb',
        'additionalCut' : '',
        'svFitPost' : 'false',
        'svFitPrep' : 'false',
        'doFRMthd' : 'false',
        #'skimmed' : 'false',
        'skimmed' : 'true',
        'skimHdfs' : 'false',
        #'skimHdfs' : 'true',
    }
    buildRedBkgFakeFunctions( dataSamples, **params )

