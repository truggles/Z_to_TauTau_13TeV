# From truggles
# https://github.com/truggles/Z_to_TauTau_13TeV/blob/master/util/svFitMerger.py

import ROOT
from ROOT import TMath
import os, glob, subprocess
import multiprocessing
from array import array

# Because we run this in the svFit area we need the function locally defined
def getProdMap() :
    prodMap = {
        'em' : ('e', 'm'),
        'et' : ('e', 't'),
        'mt' : ('m', 't'),
        'tt' : ('t1', 't2'),
        'eeem' : ('e1', 'e2', 'e3', 'm'),
        'eeet' : ('e1', 'e2', 'e3', 't'),
        'eemt' : ('e1', 'e2', 'm', 't'),
        'eett' : ('e1', 'e2', 't1', 't2'),
        'emmm' : ('m1', 'm2', 'e', 'm3'),
        'emmt' : ('m1', 'm2', 'e', 't'),
        'mmmt' : ('m1', 'm2', 'm3', 't'),
        'mmtt' : ('m1', 'm2', 't1', 't2'),
        'eeee' : ('e1', 'e2', 'e3', 'e4'),
        'eemm' : ('e1', 'e2', 'm1', 'm2'),
        'mmmm' : ('m1', 'm2', 'm3', 'm4'),
    }
    return prodMap

# Check if directory exists, make it if not
def checkDir( dirName ) :
    if not os.path.exists( dirName ) : os.makedirs( dirName )

def adjustMet(met, metPhi, dx3, dy3, dx4, dy4 ) :
    # MET in x and y
    met_x = met * TMath.Cos(metPhi)
    met_y = met * TMath.Sin(metPhi)
    #print row.evt, row.lumi
    #print "Met x, y",met_x,met_y

    # adjusted met x and y
    met_x = met_x - dx3 - dx4
    met_y = met_y - dy3 - dy4
    #print "shifted MET x,y",met_x,met_y
    
    # shifted MET and METPhi
    #print "Initial MET",met,metPhi
    shiftedMET = TMath.Sqrt( met_x*met_x + met_y*met_y)
    shiftedMETPhi = TMath.ATan2( met_y, met_x )
    #print "Final MET",shiftedMET,shiftedMETPhi
    #print "\n"
    return shiftedMET, shiftedMETPhi

def correctTauPt( lep, p4, gen_match, decay_mode ) :
    # if E or Mu return origianal pT
    if 't' not in lep : return p4
    
    if gen_match == 5 : # Real Tau, use 2017 shift measurements
        # DM 0 needs to keep pion mass
        if decay_mode == 0 : 
            p4new = p4 * (1. + 0.007)
            p4new.SetPtEtaPhiM( p4new.Pt(), p4new.Eta(), p4new.Phi(), 0.1395699 )
            return p4new
        if decay_mode == 1 : return p4 * (1. - 0.002)
        if decay_mode == 10 : return p4 * (1. + 0.001)
        return p4

    #if gen_match == 2 or gen_match == 4 :
    #    if decay_mode == 1 : return p4 * (1. + 0.015)
    #    return p4
        
    if gen_match == 1 or gen_match == 3 :
        if decay_mode == 0 : return p4 * (1. + 0.003)
        if decay_mode == 1 : return p4 * (1. + 0.036)
        return p4

    return p4

def correctTausInTree( sample, channel, ttreePath, inDir ) :
    #files = glob.glob(inDir+'/%s_*_%s.root' % (sample, channel) )
    files = glob.glob(inDir+'/*.root' )
    checkDir( inDir )
    for file in files :
        print file

    # Add return if no files found
    # this is useful for all the many signal masses
    if len(files) == 0 : 
        print "\n\n"
        print "No files of samples %s found in dir %s for channel %s" % (sample, inDir, channel)
        print "\n\n"
        return

    prodMap = getProdMap()
    print prodMap[ channel ] 
    l1 = prodMap[ channel ][0]
    l2 = prodMap[ channel ][1]
    print l1, l2

    rep = 0
    runningSize = 0
    runningNumFiles = 0
    toMerge = []
    ints = []
    for file_ in files :

        # Merge to ~ 1000 events per file
        f = ROOT.TFile(file_,'UPDATE')
        iDir = f.Get(ttreePath.replace('/Ntuple',''))
        updateTree = f.Get(ttreePath)

        # New shifted pt branches only for Taus
        shiftedPt_1 = array('f', [ 0 ] )
        shiftedPt_1B = updateTree.Branch('shiftedPt_1', shiftedPt_1, 'shiftedPt_1/F')
        shiftedPt_2 = array('f', [ 0 ] )
        shiftedPt_2B = updateTree.Branch('shiftedPt_2', shiftedPt_2, 'shiftedPt_2/F')
        shiftedMass_3 = array('f', [ 0 ] )
        shiftedMass_3B = updateTree.Branch('shiftedMass_3', shiftedMass_3, 'shiftedMass_3/F')
        shiftedMass_4 = array('f', [ 0 ] )
        shiftedMass_4B = updateTree.Branch('shiftedMass_4', shiftedMass_4, 'shiftedMass_4/F')
        # Nominal
        shiftedMET = array('f', [ 0 ] )
        shiftedMETB = updateTree.Branch('shiftedMET', shiftedMET, 'shiftedMET/F')
        shiftedMETPhi = array('f', [ 0 ] )
        shiftedMETPhiB = updateTree.Branch('shiftedMETPhi', shiftedMETPhi, 'shiftedMETPhi/F')
        # Unclustered EN
        shiftedUncMETUp = array('f', [ 0 ] )
        shiftedUncMETUpB = updateTree.Branch('shiftedUncMETUp', shiftedUncMETUp, 'shiftedUncMETUp/F')
        shiftedUncMETPhiUp = array('f', [ 0 ] )
        shiftedUncMETPhiUpB = updateTree.Branch('shiftedUncMETPhiUp', shiftedUncMETPhiUp, 'shiftedUncMETPhiUp/F')
        shiftedUncMETDown = array('f', [ 0 ] )
        shiftedUncMETDownB = updateTree.Branch('shiftedUncMETDown', shiftedUncMETDown, 'shiftedUncMETDown/F')
        shiftedUncMETPhiDown = array('f', [ 0 ] )
        shiftedUncMETPhiDownB = updateTree.Branch('shiftedUncMETPhiDown', shiftedUncMETPhiDown, 'shiftedUncMETPhiDown/F')
        # Clustered EN
        shiftedClustMETUp = array('f', [ 0 ] )
        shiftedClustMETUpB = updateTree.Branch('shiftedClustMETUp', shiftedClustMETUp, 'shiftedClustMETUp/F')
        shiftedClustMETPhiUp = array('f', [ 0 ] )
        shiftedClustMETPhiUpB = updateTree.Branch('shiftedClustMETPhiUp', shiftedClustMETPhiUp, 'shiftedClustMETPhiUp/F')
        shiftedClustMETDown = array('f', [ 0 ] )
        shiftedClustMETDownB = updateTree.Branch('shiftedClustMETDown', shiftedClustMETDown, 'shiftedClustMETDown/F')
        shiftedClustMETPhiDown = array('f', [ 0 ] )
        shiftedClustMETPhiDownB = updateTree.Branch('shiftedClustMETPhiDown', shiftedClustMETPhiDown, 'shiftedClustMETPhiDown/F')
        hDR = array('f', [ 0 ] )
        hDRB = updateTree.Branch('hDR', hDR, 'hDR/F')

        size = updateTree.GetEntries()
        print size,"   ",file_
        cnt = 0
        for row in updateTree :
            cnt += 1
            #if cnt > 100 : break

            l1pt = getattr( row, '%sPt' % l1 )
            l1eta = getattr( row, '%sEta' % l1 )
            l1phi = getattr( row, '%sPhi' % l1 )
            l1mass = getattr( row, '%sMass' % l1 )
            l1p4 = ROOT.TLorentzVector()
            l1p4.SetPtEtaPhiM( l1pt, l1eta, l1phi, l1mass )
            l2pt = getattr( row, '%sPt' % l2 )
            l2eta = getattr( row, '%sEta' % l2 )
            l2phi = getattr( row, '%sPhi' % l2 )
            l2mass = getattr( row, '%sMass' % l2 )
            l2p4 = ROOT.TLorentzVector()
            l2p4.SetPtEtaPhiM( l2pt, l2eta, l2phi, l2mass )

            shiftedPt_1[0] = l1pt
            shiftedPt_2[0] = l2pt
            shiftedMass_3[0] = l1mass
            shiftedMass_4[0] = l2mass
            shiftedMET[0] = getattr( row, 'type1_pfMetEt' )
            shiftedMETPhi[0] = getattr( row, 'type1_pfMetPhi' )
            shiftedUncMETUp[0] = getattr( row, 'type1_pfMet_shiftedPt_UnclusteredEnUp' )
            shiftedUncMETPhiUp[0] = getattr( row, 'type1_pfMet_shiftedPhi_UnclusteredEnUp' )
            shiftedUncMETDown[0] = getattr( row, 'type1_pfMet_shiftedPt_UnclusteredEnDown' )
            shiftedUncMETPhiDown[0] = getattr( row, 'type1_pfMet_shiftedPhi_UnclusteredEnDown' )
            shiftedClustMETUp[0] = getattr( row, 'type1_pfMet_shiftedPt_JetEnUp' )
            shiftedClustMETPhiUp[0] = getattr( row, 'type1_pfMet_shiftedPhi_JetEnUp' )
            shiftedClustMETDown[0] = getattr( row, 'type1_pfMet_shiftedPt_JetEnDown' )
            shiftedClustMETPhiDown[0] = getattr( row, 'type1_pfMet_shiftedPhi_JetEnDown' )

            # Always recompute hDR
            hDR[0] = l1p4.DeltaR( l2p4 )
            hDRB.Fill()



            # Don't even check this for data
            if 'data' in sample :
                shiftedPt_1B.Fill()
                shiftedPt_2B.Fill()
                shiftedMass_3B.Fill()
                shiftedMass_4B.Fill()
                shiftedMETB.Fill()
                shiftedMETPhiB.Fill()
                shiftedUncMETUpB.Fill()
                shiftedUncMETPhiUpB.Fill()
                shiftedUncMETDownB.Fill()
                shiftedUncMETPhiDownB.Fill()
                shiftedClustMETUpB.Fill()
                shiftedClustMETPhiUpB.Fill()
                shiftedClustMETDownB.Fill()
                shiftedClustMETPhiDownB.Fill()
                continue

            # only MC at this point
            l1Shifted = False
            if 't' in l1 and getattr( row, '%sZTTGenMatching' % l1 ) != 6 :
                #print "l1Pt:        ", l1pt," DM: ",getattr( row, '%sDecayMode' % l1 )," gen_match: ",getattr( row, '%sZTTGenMatching' % l1 )
                #print " -- corr pt: ", correctTauPt( l1, l1pt, getattr( row, '%sZTTGenMatching' % l1 ), getattr( row, '%sDecayMode' % l1 ) )
                shiftedP4 = correctTauPt( l1, l1p4, getattr( row, '%sZTTGenMatching' % l1 ), getattr( row, '%sDecayMode' % l1 ) )
                shiftedPt_1[0] = shiftedP4.Pt()
                shiftedMass_3[0] = shiftedP4.M()
                if shiftedPt_1[0] != l1pt :
                    l1Shifted = True
            l2Shifted = False
            if 't' in l2 and getattr( row, '%sZTTGenMatching' % l2 ) != 6 :
                #print "l2Pt:        ", l2pt," DM: ",getattr( row, '%sDecayMode' % l2 )," gen_match: ",getattr( row, '%sZTTGenMatching' % l2 )
                #print " -- corr pt: ", correctTauPt( l2, l2pt, getattr( row, '%sZTTGenMatching' % l2 ), getattr( row, '%sDecayMode' % l2 ) )
                shiftedP4 = correctTauPt( l2, l2p4, getattr( row, '%sZTTGenMatching' % l2 ), getattr( row, '%sDecayMode' % l2 ) )
                shiftedPt_2[0] = shiftedP4.Pt()
                shiftedMass_4[0] = shiftedP4.M()
                if shiftedPt_2[0] != l2pt :
                    l2Shifted = True

            # only recompute if there were shifts applied
            if l1Shifted or l2Shifted :
                # delta x, y shifts from corrections
                dx3 = TMath.Cos( l1phi ) * (shiftedPt_1[0] - l1pt)
                dy3 = TMath.Sin( l1phi ) * (shiftedPt_1[0] - l1pt)
                dx4 = TMath.Cos( l2phi ) * (shiftedPt_2[0] - l2pt)
                dy4 = TMath.Sin( l2phi ) * (shiftedPt_2[0] - l2pt)
                #print "dx3,dy3,dx4,dy4",dx3,dy3,dx4,dy4
                
                shiftedMET[0], shiftedMETPhi[0] = adjustMet(shiftedMET[0], shiftedMETPhi[0], dx3, dy3, dx4, dy4 )
                shiftedUncMETUp[0], shiftedUncMETPhiUp[0] = adjustMet(shiftedUncMETUp[0], shiftedUncMETPhiUp[0], dx3, dy3, dx4, dy4 )
                shiftedUncMETDown[0], shiftedUncMETPhiDown[0] = adjustMet(shiftedUncMETDown[0], shiftedUncMETPhiDown[0], dx3, dy3, dx4, dy4 )
                shiftedClustMETUp[0], shiftedClustMETPhiUp[0] = adjustMet(shiftedClustMETUp[0], shiftedClustMETPhiUp[0], dx3, dy3, dx4, dy4 )
                shiftedClustMETDown[0], shiftedClustMETPhiDown[0] = adjustMet(shiftedClustMETDown[0], shiftedClustMETPhiDown[0], dx3, dy3, dx4, dy4 )


            shiftedPt_1B.Fill()
            shiftedPt_2B.Fill()
            shiftedMass_3B.Fill()
            shiftedMass_4B.Fill()
            shiftedMETB.Fill()
            shiftedMETPhiB.Fill()
            shiftedUncMETUpB.Fill()
            shiftedUncMETPhiUpB.Fill()
            shiftedUncMETDownB.Fill()
            shiftedUncMETPhiDownB.Fill()
            shiftedClustMETUpB.Fill()
            shiftedClustMETPhiUpB.Fill()
            shiftedClustMETDownB.Fill()
            shiftedClustMETPhiDownB.Fill()


        iDir.cd()
        updateTree.Write('', ROOT.TObject.kOverwrite)
        f.Close()


if __name__ == '__main__' :
    ''' Start multiprocessing tests '''
    pool = multiprocessing.Pool(processes = 14 )
    #pool = multiprocessing.Pool(processes = 1 )
    multiprocessingOutputs = []
    debug = False
    #debug = True
    doAZH = False
    doHTT = True



    # For svFit, skip eeee, mmmm channels
    if doAZH :
        # AZH Halloween Wisconsin -> uwlogin
        azhSamples = ['ttZ', 'ttZ2', 'DYJets', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'ggZZ4m', 'ggZZ2e2m', 'ggZZ2e2tau', 'ggZZ4e', 'ggZZ2m2tau', 'ggZZ4tau', 'TT', 'WWW', 'WWZ', 'WZ3l1nu', 'WZZ', 'WZ', 'ZZ4l', 'ZZZ',] # May 31 samples, no ZZ->all, use ZZ4l

        for mass in [110, 120, 125, 130, 140] :
            azhSamples.append('ggHtoTauTau%i' % mass)
            azhSamples.append('VBFHtoTauTau%i' % mass)
            azhSamples.append('WMinusHTauTau%i' % mass)
            azhSamples.append('WPlusHTauTau%i' % mass)
            azhSamples.append('ZHTauTau%i' % mass)
        for mass in [125,] :
            azhSamples.append('ZHWW%i' % mass)
            azhSamples.append('HZZ%i' % mass)
            azhSamples.append('VBFHtoWW2l2nu%i' % mass)
            azhSamples.append('WPlusHHWW%i' % mass)
            azhSamples.append('WMinusHHWW%i' % mass)
            azhSamples.append('HtoWW2l2nu%i' % mass)
            azhSamples.append('ttHTauTau%i' % mass)
            azhSamples.append('ttHJNonBB%i' % mass)
            azhSamples.append('ttHNonBB%i' % mass)

        #azhSamples = ['ggZZ4m','ggZZ4e']
        for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
            azhSamples.append('azh%i' % mass)

        #azhSamples = []
        for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
            azhSamples.append('dataEE-%s' % era)
            azhSamples.append('dataMM-%s' % era)
            azhSamples.append('dataSingleE-%s' % era)
            azhSamples.append('dataSingleM-%s' % era)

        #azhSamples = ['azh300',]


        name = 'azhJune19AZH_test'
        name = 'azhJune19AZH_azh_svFitPrep'
        #inDir = '/nfs_scratch/truggles/'+name+'_svFitPrep/'
        inDir = '/nfs_scratch/truggles/'+name+'/'
        dataDir = inDir+'data/'
        recoilDir = inDir+'recoil/'
        noRecoilDir = inDir+'noRecoil/'
        checkDir( dataDir )
        checkDir( recoilDir )
        checkDir( noRecoilDir )
        getsRecoil = ['DYJet', 'ggHtoTauTau', 'VBF', 'HZZ', 'HtoWW']
        #name = 'svFitTmp'
        #inDir = '/data/truggles/'+name+'/'
        checkDir( inDir )
        jobId = ''
        channels = ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm',] # 8
        #channels = ['mmtt',] # 10
        for channel in channels :
            ttreePath = channel+'/final/Ntuple'
            for sample in azhSamples :

                # Get proper sub-directory
                targetDirNew = inDir
                if 'data' in sample : targetDirNew = dataDir
                for recoil in getsRecoil :
                    if recoil in sample : targetDirNew = recoilDir
                if targetDirNew == inDir : # didn't find a new dir yet
                    targetDirNew = noRecoilDir

                if debug:
                    correctTausInTree( sample, channel, ttreePath, targetDirNew )
                else :
                    multiprocessingOutputs.append( pool.apply_async(correctTausInTree, args=(
                        sample,
                        channel,
                        ttreePath,
                        targetDirNew )))
        if not debug :
            mpResults = [p.get() for p in multiprocessingOutputs]




    if doHTT :
        httSamples = ['VBFHtoTauTau125',]

        name = 'Ceciles_files2'
        inDir = '/data/truggles/vbf_sync_20181127/'+name+'/'
        checkDir( inDir )
        outDir = 'TECed'
        targetDirNew = '/data/truggles/vbf_sync_20181127/'+name+'_'+outDir+'/'
        checkDir( targetDirNew )
        jobId = ''
        channels = ['mt',]
        for channel in channels :
            ttreePath = channel+'/final/Ntuple'
            for sample in httSamples :


                if debug:
                    correctTausInTree( sample, channel, ttreePath, inDir )
                else :
                    multiprocessingOutputs.append( pool.apply_async(correctTausInTree, args=(
                        sample,
                        channel,
                        ttreePath,
                        inDir )))
        if not debug :
            mpResults = [p.get() for p in multiprocessingOutputs]




