#!/usr/bin/env python

import ROOT
import os
from util.helpers import checkDir
import analysis1BaselineCuts
from meta.sampleNames import returnSampleDetails
from util.helpers import setUpDirs 
import pyplotter.tdrstyle as tdr
import subprocess
from array import array



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
        'tau-DM0' : ['eeet', 'eett', 'eemt', 'emmt', 'mmtt', 'mmmt'],
        'tau-DM1' : ['eeet', 'eett', 'eemt', 'emmt', 'mmtt', 'mmmt'],
        'tau-DM10' : ['eeet', 'eett', 'eemt', 'emmt', 'mmtt', 'mmmt'],
        'tau-lltt' : ['eett', 'mmtt'],
        'tau-DM0_lltt' : ['eett', 'mmtt'],
        'tau-DM1_lltt' : ['eett', 'mmtt'],
        'tau-DM10_lltt' : ['eett', 'mmtt'],
        'tau-lllt' : ['eeet', 'eemt', 'emmt', 'mmmt'],
        'tau-DM0_lllt' : ['eeet', 'eemt', 'emmt', 'mmmt'],
        'tau-DM1_lllt' : ['eeet', 'eemt', 'emmt', 'mmmt'],
        'tau-DM10_lllt' : ['eeet', 'eemt', 'emmt', 'mmmt'],
        'electron' : ['eeet', 'emmt'],
       'muon' : ['eemt', 'mmmt'],
        #'electron2' : ['eeem', 'emmm'],
        #'muon2' : ['eeem', 'emmm'],
    }

    fakeRateMap = {}
    #for matched in [True,]:# False] :
    for matched in [False,]:# False] :
        app = 'jetMatch' if matched else 'noJetMatch'
        app = 'leptonPt'
        for obj, chans in redBkgMap.iteritems() :
            tmpMap = doRedBkgPlots( obj, chans, dir2, matched )
            for name, info in tmpMap.iteritems() :
                fakeRateMap[name+'_'+app] = info

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


def doRedBkgPlots( obj, channels, inputDir, jetMatched ) :

    cmsLumi = float(os.getenv('LUMI'))/1000
    print "Lumi = %.1f / fb" % cmsLumi
    print "doing Red Bkg Plots for",obj
    print channels


    #if jetMatched :
    #    xAxis = 'Jet p_{T} [GeV]'
    #    jetCut = 'cand_JetPt > pt_Num && cand_JetDR < 0.5'
    #    app = 'jetMatch'
    #else :
    #    xAxis = 'Lepton p_{T} [GeV]'
    #    jetCut = '(cand_JetPt <= pt_Num || cand_JetDR >= 0.5)'
    #    app = 'noJetMatch'
    # Lepton PT
    xAxis = 'Lepton p_{T} [GeV]'
    jetCut = '(1.)'
    app = 'leptonPt'
    #saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Nov22v2_ALLMC_mcRates_Linear_'+app
    #saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Nov22v1_ALLMC_mcRates_'+app
    #saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Nov23v1_ALLMC_mcRates_genFakes2_'+app
    saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Dec01v1_ALLMC_mcRates_genFakes_noBJets_'+app
    #saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Nov23v2_ALLMC_mcRates_looseMT40_'+app
    #saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Nov23v2_ALLMC_mcRates_nomMT30_'+app
    #saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Nov23v2_ALLMC_mcRates_nomMT30_nobjet_'+app
    #saveDir = '/afs/cern.ch/user/t/truggles/www/azhRedBkg/Nov23v2_ALLMC_mcRates_addEM_'+app
    checkDir( saveDir )

    c1 = ROOT.TCanvas("c1","c1", 550, 550)
    pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
    pad1.Draw()
    pad1.cd()


    yAxis2 = 'Fake Rate'
    binInfo = [80, 0, 140]
    #if 'electron' in obj :
    #    binInfo = [80, 0, 200]
    yAxis1 = 'Events / %i GeV' % ( (binInfo[2] - binInfo[1]) / binInfo[0] )
    useVariableBinning = True
    if not useVariableBinning :
        denomAll = ROOT.TH1D( obj+'_denom', obj+'_denom;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
        passAll = ROOT.TH1D( obj+'_pass', obj+'_pass;%s;%s'%(xAxis,yAxis1), binInfo[0], binInfo[1], binInfo[2] )
    else :
        xBins = array('d', [])
        if jetMatched :
            if obj == 'electron' :
                for i in range( 0, 20, 2) :
                    xBins.append( i )
                for i in range( 20, 40, 5) :
                    xBins.append( i )
                for i in range( 40, 100, 10) :
                    xBins.append( i )
            else :
                for i in range( 0, 40, 1) :
                    j = i * 5
                    #j = i * 2.5
                    if j >= 40 : continue
                    xBins.append( j )
                for i in range( 40, 60, 5) :
                    xBins.append( i )
                for i in range( 60, 100, 10) :
                    xBins.append( i )
        #elif 'tau-DM10_lllt' in obj :
        #    #for i in range( 0, 40, 10) :
        #    for i in range( 0, 3) :
        #        xBins.append( 20+i*6.75 )
        #    for i in range( 40, 150, 30) :
        #        xBins.append( i )
        else :
            #if 'tau-DM0_lltt' in obj or 'tau-DM1_lltt' in obj :
            #    for i in range( 0, 40, 4) :
            #        xBins.append( i )
            #if 'tau-DM10_lltt' in obj or 'tau-DM10_lllt' in obj :
            #    #for i in range( 0, 40, 10) :
            #    for i in range( 0, 3) :
            #        xBins.append( 20+i*6.75 )
            #elif 'lllt' in obj :
            #    for i in range( 0, 40, 4) :
            #        xBins.append( i )
            if 'tau' in obj :
                for i in range( 0, 40, 5) :
                    xBins.append( i )
            else :
                for i in range( 0, 40, 5) :
                    xBins.append( i )
            for i in range( 40, 60, 10) :
                xBins.append( i )
            if 'tau' in obj :
                for i in range( 60, 120, 20) :
                    xBins.append( i )
            else :
                for i in range( 60, 120, 40) :
                    xBins.append( i )
            #for i in range( 120, 150, 30) :
            #    xBins.append( i )
        for i in range( 100, 141, 40) :
            xBins.append( i )
        print xBins
        binInfo = ['x', xBins[0], xBins[-1]]
        yAxis1 = 'Events'
        denomAll = ROOT.TH1D( obj+'_denom', obj+'_denom;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )
        passAll = ROOT.TH1D( obj+'_pass', obj+'_pass;%s;%s'%(xAxis,yAxis1), len(xBins)-1, xBins )

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
            'denom' : ['byVVLooseIsolationMVArun2v1DBoldDMwLT_Num > 0.5 && gen_match_Num == 6',],
            #'denom' : ['byVVLooseIsolationMVArun2v1DBoldDMwLT_Num > 0.5',],
            'pass' : ['byMediumIsolationMVArun2v1DBoldDMwLT_Num > 0.5',],
        },
        'electron' : {
            'denom' : ['pfmt_3 < 30', 'gen_match_3 == 6',], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 30', 'bjetCISVVeto20MediumZTT == 0'], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 30',], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 30','id_e_mva_nt_loose_Num > 0.5'], # to suppress real leptons from WZ and ZZ
            'pass' : ['iso_Num < 0.15', 'id_e_mva_nt_tight_Num > 0.5'],

        },
        'electron2' : {
            #'denom' : ['pfmt_3 < 30 && gen_match_Num == 6',], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 30', 'bjetCISVVeto20MediumZTT == 0'], # to suppress real leptons from WZ and ZZ
            'denom' : ['pfmt_3 < 30',], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 30','id_e_mva_nt_loose_Num > 0.5'], # to suppress real leptons from WZ and ZZ
            'pass' : ['iso_Num < 0.15', 'id_e_mva_nt_tight_Num > 0.5'],

        },
        'muon' : {
            'denom' : ['pfmt_3 < 30', 'gen_match_3 == 6'], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 30', 'bjetCISVVeto20MediumZTT == 0'], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 30',], # to suppress real leptons from WZ and ZZ
            'pass' : ['iso_Num < 0.15', 'cand_PFIDLoose > 0.5'],
        },
        'muon2' : {
            #'denom' : ['pfmt_3 < 30 && gen_match_Num == 6',], # to suppress real leptons from WZ and ZZ
            #'denom' : ['pfmt_3 < 30', 'bjetCISVVeto20MediumZTT == 0'], # to suppress real leptons from WZ and ZZ
            'denom' : ['pfmt_3 < 30',], # to suppress real leptons from WZ and ZZ
            'pass' : ['iso_Num < 0.15', 'cand_PFIDLoose > 0.5'],
        },
    } 

    etaCuts = {
        'tau' : {
            #'Barrel' : 'abs( eta_Num ) <= 1.4',
            #'Endcap' : 'abs( eta_Num ) > 1.4',
            'AllEta' : '(1)',
        },
        'electron' : {
            'Barrel' : 'abs( eta_Num ) <= 1.5',
            'Endcap' : 'abs( eta_Num ) > 1.5',
            #'AllEta' : '(1)',
        },
        'electron2' : {
            'Barrel' : 'abs( eta_Num ) <= 1.5',
            'Endcap' : 'abs( eta_Num ) > 1.5',
            #'AllEta' : '(1)',
        },
        'muon' :{
            'Barrel' : 'abs( eta_Num ) <= 1.4',
            'Endcap' : 'abs( eta_Num ) > 1.4',
            #'AllEta' : '(1)',
        },
        'muon2' :{
            'Barrel' : 'abs( eta_Num ) <= 1.4',
            'Endcap' : 'abs( eta_Num ) > 1.4',
            #'AllEta' : '(1)',
        },
    }

    frMap = {}

    etaCode = 'tau' if 'tau' in obj else obj.split('-')[0]
    for etaRegion, etaCut in etaCuts[etaCode].iteritems() :
    # obj.split('-')[0] is to get the same cuts and mapping for
    # tau, tau-lltt, tau-lllt

        denomCut = ' && '.join( cuts[obj.split('-')[0]]['denom'] )
        denomCut += ' && '+etaCut
        denomCut += ' && '+jetCut
        denomCut += ' && bjetCISVVeto20MediumZTT == 0'

        ## If using tau decay modes:
        if 'tau-DM10' in obj : denomCut += ' && decayMode_Num == 10'
        elif 'tau-DM0' in obj : denomCut += ' && decayMode_Num == 0'
        elif 'tau-DM1' in obj : denomCut += ' && decayMode_Num == 1'

        passCut = ' && '.join( cuts[obj.split('-')[0]]['pass'] )
        passCut = denomCut+' && '+passCut
        # If using tau decay modes:
        if 'tau-DM10' in obj : passCut += ' && decayMode_Num == 10'
        elif 'tau-DM0' in obj : passCut += ' && decayMode_Num == 0'
        elif 'tau-DM1' in obj : passCut += ' && decayMode_Num == 1'

        totalDenomAll = 0.
        totalPassingAll = 0.

        for channel in channels :
            print channel

            # Apply loosened LT_higgs cuts for LLTT channels and
            # make sure to apply it for LLMT
            # LLET and LLEM essentially have no LT_higgs cut
            passCut2 = passCut
            denomCut2 = denomCut
            if channel in ['eett', 'mmtt'] :
                passCut2 += ' && LT_higgs > 50'
                denomCut2 += ' && LT_higgs > 50'
            elif channel in ['eemt','mmmt'] :
                passCut2 += ' && LT_higgs > 40'
                denomCut2 += ' && LT_higgs > 40'

            f = ROOT.TFile( '/data/truggles/'+inputDir+'/redBkg_'+channel+'.root', 'r' )
            t = f.Get('Ntuple')
            print "\n"
            print "Input: /data/truggles/"+inputDir+'/redBkg_'+channel+'.root'
            print t

            # check if first letter of 'obj' in leg3 then leg4 and draw if so
            for i, leg in enumerate(prodMap[channel]) :

                if not obj[0] in leg : continue

                # Replace vals in the passCut to match leg
                denomCutX = denomCut2.replace( '_Num', '_%i' % (i+3) ) # i begins at 0, we being with leg3
                denomCutX = denomCutX.replace( 'cand_', leg ) # For vars we didn't use in sync ntuple
                passCutX = passCut2.replace( '_Num', '_%i' % (i+3) ) # i begins at 0, we being with leg3
                passCutX = passCutX.replace( 'cand_', leg ) # For vars we didn't use in sync ntuple

                denomCutX = '('+denomCutX+')*azhWeight*puweight*XSecLumiWeight*GenWeight/abs(GenWeight)'
                passCutX = '('+passCutX+')*azhWeight*puweight*XSecLumiWeight*GenWeight/abs(GenWeight)'

                print "Denom Cut:",denomCutX
                print "Passing Cut:",passCutX

                # Denominator selection
                if not useVariableBinning :
                    hTmp = ROOT.TH1D( 'hTmp', 'hTmp', binInfo[0], binInfo[1], binInfo[2] )
                else :
                    hTmp = ROOT.TH1D( 'hTmp', 'hTmp', len(xBins)-1, xBins )

                t.Draw( 'pt_'+str(i+3)+' >> hTmp', denomCutX )
                #t.Draw( leg+'JetPt >> hTmp', denomCutX )

                #print channel, leg, hTmp.Integral()
                denomAll.Add( hTmp )
                print " -- denomAll Int:",denomAll.Integral()
                totalDenomAll += hTmp.Integral()

                # Passing selection
                if not useVariableBinning :
                    hTmpPass = ROOT.TH1D( 'hTmpPass', 'hTmpPass', binInfo[0], binInfo[1], binInfo[2] )
                else :
                    hTmpPass = ROOT.TH1D( 'hTmpPass', 'hTmpPass', len(xBins)-1, xBins )

                t.Draw( 'pt_'+str(i+3)+' >> hTmpPass', passCutX )
                #t.Draw( leg+'JetPt >> hTmpPass', passCutX )

                passAll.Add( hTmpPass )
                print " -- passAll Int:",passAll.Integral()
                totalPassingAll += hTmpPass.Integral()
                del hTmp, hTmpPass


        # Print totals for each plot
        print ' ---- '+obj+' '+etaRegion+'   denom: '+str(totalDenomAll)+'    passing: '+str(totalPassingAll)

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
        graph.SetName( graph.GetName()+' '+app )
        pad1.SetGrid()

        # For Log
        doLinear = True
        #doLinear = False
        if not doLinear :
            pad1.SetLogy()
            graph.SetMaximum( 10 )
            if 'DM10' in obj or 'DM0' in obj :
                graph.SetMinimum( 0.00005 )
            elif 'DM1' in obj :
                graph.SetMinimum( 0.0005 )
            else :
                graph.SetMinimum( 0.0005 )
        if doLinear :
            if 'muon' in obj  :
                graph.SetMaximum( .1 )
            #else :
            #    graph.SetMaximum( .15 )
            elif obj == 'electron' :
                graph.SetMaximum( .1 )
            else :
                graph.SetMaximum( 1 )
            graph.SetMinimum( 0 )

        graph.Draw("AP")

        # do fit
        #fitMin = binInfo[1] if binInfo[1] != 0 else 10

        # Set fit min for different objects
        if 'tau' in obj : fitMin = 20
        if jetMatched :
            if 'electron' in obj : fitMin = 0
            if 'muon' in obj : fitMin = 12.5
        else :
            if 'electron' in obj : fitMin = 10
            if 'muon' in obj : fitMin = 10

        useExp = True
        useExp = False
        if useExp :
            f1 = ROOT.TF1( 'f1', '([0] + [1]*TMath::Exp(-[2]*x))', fitMin, binInfo[2]) # default one used on 2012 data
            f1.SetParName( 2, "decay" )
            if 'electron' in obj or 'muon' in obj :
                f1.SetParameter( 0, 0. )
                f1.SetParameter( 1, 1 )
                f1.SetParameter( 2, .05 )
            else : # is tau
                f1.SetParameter( 0, 0. )
                f1.SetParameter( 1, 1 )
                f1.SetParameter( 2, .05 )
        #if 'tau' in obj : # : # No Exponential
        #    ### Try linear
        if obj == 'electron' or obj == 'muon' :
            f1 = ROOT.TF1( 'f1', '([0] + [1]*x)', fitMin, binInfo[2])
        else :
            f1 = ROOT.TF1( 'f1', '([0] + [1]*(TMath::Landau(x,[2],[3],0)) )', fitMin, binInfo[2])
            f1.SetParName( 2, "approx. max" )
            f1.SetParName( 3, "sigma param" )
            f1.SetParameter( 0, 0. )
            f1.SetParameter( 1, 1 )
            if jetMatched :
                if 'electron' in obj :
                    f1.SetParameter( 1, 0.2 )
                    f1.SetParameter( 2, 15. )
                    f1.SetParameter( 3, 2. )
                elif 'muon' in obj :
                    f1.SetParameter( 2, 20. )
                    f1.SetParameter( 3, 5. )
                elif 'tau-DM0' in obj :
                    f1.SetParameter( 1, .1 )
                    f1.SetParameter( 2, 20. )
                    f1.SetParameter( 3, 3. )
                else : # is tau
                    f1.SetParameter( 2, 30. )
                    f1.SetParameter( 3, 5. )
            else : # Not Jet Matched
                if 'electron' in obj :
                    f1.SetParameter( 1, 0.2 )
                    f1.SetParameter( 2, 100. )
                    f1.SetParameter( 3, 50. )
                elif 'muon' in obj :
                    f1.SetParameter( 2, 100. )
                    f1.SetParameter( 3, 50. )
                elif 'tau-DM10' == obj :
                    f1.SetParameter( 0, .1 )
                    f1.SetParameter( 1, .1 )
                    f1.SetParameter( 2, 35. )
                    f1.SetParameter( 3, 3. )
                elif 'tau-DM0' in obj :
                    f1.SetParameter( 1, .1 )
                    f1.SetParameter( 2, 20. )
                    f1.SetParameter( 3, 3. )
                elif 'tau-DM10_lllt' in obj :
                    f1.SetParameter( 0, .1 )
                    f1.SetParameter( 1, .05 )
                    f1.SetParameter( 2, 50. )
                    f1.SetParameter( 3, 20. )
                elif 'tau-DM10_lltt' in obj :
                    f1.SetParameter( 0, .13 )
                    f1.SetParameter( 1, .3 )
                    f1.SetParameter( 2, 40. )
                    f1.SetParameter( 3, 4. )
                else : # is tau
                    f1.SetParameter( 2, 30. )
                    f1.SetParameter( 3, 5. )
               #if obj == 'electron' :
               #    f1.SetParameter( 2, 18. )
               #    f1.SetParameter( 3, 2.5 )
               #elif obj == 'muon' :
               #    f1.SetParameter( 2, 15. )
               #    f1.SetParameter( 3, 2.5 )
               #else : # is tau
               #    f1.SetParameter( 2, 20. )
               #    f1.SetParameter( 3, 3. )
        #else : # No Exponential
        #    #f1 = ROOT.TF1( 'f1', '([0] + [1]*x + [2]*(x+[3])*(x+[3]) + [4]*(x+[5])*(x+[5])*(x+[5]))', fitMin, binInfo[2])
        #    f1 = ROOT.TF1( 'f1', '([0] + [1]*x + [2]*(x+[3])*(x+[3]))', fitMin, binInfo[2])
        #    f1.SetParName( 2, "approx. max" )
        #    f1.SetParName( 3, "sigma param" )
        #    f1.SetParameter( 0, 0. )
        #    f1.SetParameter( 1, 1 )

        f1.SetParName( 0, "y rise" )
        f1.SetParName( 1, "scale" )
        #if jetMatched and 'electron' in obj :
        #    graph.Fit('f1', 'SRN' ) # N skips drawing
        #elif jetMatched :
        #    graph.Fit('f1', 'SR' )
        #else :
        #    graph.Fit('f1', 'SRN' ) # N skips drawing
        graph.Fit('f1', 'SR' )

        if useExp :
            f2 = ROOT.TF1( 'f2 '+app, '([0] + [1]*TMath::Exp(-[2]*x))', fitMin, binInfo[2]) # default one used on 2012 data
        #if 'tau' in obj :
        if obj == 'electron' or obj == 'muon' :
            f2 = ROOT.TF1( 'f2', '([0] + [1]*x)', fitMin, binInfo[2])
        else :
            f2 = ROOT.TF1( 'f2 '+app, '([0] + [1]*(TMath::Landau(x,[2],[3],0)) )', fitMin, binInfo[2])
            #f2 = ROOT.TF1( 'f2', '([0] + [1]*x + [2]*x*x + [3]*x*x*x)', fitMin, binInfo[2])
            #f2 = ROOT.TF1( 'f2', '([0] + [1]*x + [2]*(x+[3])*(x+[3]))', fitMin, binInfo[2])
            f2.SetParameter( 3, f1.GetParameter( 3 ) )
            f2.SetParameter( 2, f1.GetParameter( 2 ) )
        f2.SetParameter( 0, f1.GetParameter( 0 ) )
        f2.SetParameter( 1, f1.GetParameter( 1 ) )
        
        #if jetMatched and 'electron' not in obj :
        f2.Draw('SAME R')

        ROOT.gStyle.SetStatX(.95)
        ROOT.gStyle.SetStatY(0.8)
        ROOT.gStyle.SetStatH(.2)
        ROOT.gStyle.SetStatW(.2)
        setText( "Fake Rate: %s %s" % (obj, etaRegion), cmsLumi )
        ROOT.gPad.Update()
        c1.SaveAs( saveDir+'/'+obj+'_'+etaRegion+'_FakeRate.png' )
        #c1.SaveAs( saveDir+'/'+obj+'_'+etaRegion+'_FakeRate.pdf' )
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
    # B - F for DYJets
    #for era in ['B', 'C', 'D', 'E', 'F',]:# 'G', 'H'] :
    #    dataSamples.append('dataEE-%s' % era)
    #    dataSamples.append('dataMM-%s' % era)
    # G for WZ3l1nu
    #for era in ['G',]:
    #    dataSamples.append('dataEE-%s' % era)
    #    dataSamples.append('dataMM-%s' % era)
    # H for TTbar
    #for era in ['H',]:
    #    dataSamples.append('dataEE-%s' % era)
    #    dataSamples.append('dataMM-%s' % era)
    # For ALL DYJets + WZ + TTbar
    for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
        dataSamples.append('dataEE-%s' % era)
        dataSamples.append('dataMM-%s' % era)

    params = {
        #'debug' : 'true',
        'debug' : 'false',
        'numCores' : 15,
        'numFilesPerCycle' : 1,
        'channels' : ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm'], # 8
        #'channels' : ['eeet',],
        'cutMapper' : 'RedBkg',
        #'mid1' : '1Sept03rb', # Normally data driven
        #'mid2' : '2Sept03rb',
        #'mid3' : '3Sept03rb',
        'mid1' : '1Nov29rb', # MC driven
        'mid2' : '2Nov29rb',
        'mid3' : '3Nov29rb',
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

