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

def correctTauPt( lep, pt, gen_match, decay_mode ) :
    # if E or Mu return origianal pT
    if 't' not in lep : return pt
    
    if gen_match == 5 : # Real Tau, use 2016 shift measurements
        if decay_mode == 0 : return pt * (1. - 0.005)
        if decay_mode == 1 : return pt * (1. + 0.011)
        if decay_mode == 10 : return pt * (1. + 0.006)
        return pt

    if gen_match == 2 or gen_match == 4 :
        if decay_mode == 1 : return pt * (1. + 0.015)
        return pt
        
    if gen_match == 1 or gen_match == 3 :
        if decay_mode == 1 : return pt * (1. + 0.095)
        return pt

    return pt

def correctTausInTree( sample, channel, ttreePath, inDir ) :
    files = glob.glob(inDir+'/%s_*_%s.root' % (sample, channel) )
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
    l3 = prodMap[ channel ][2]
    l4 = prodMap[ channel ][3]
    print l1, l2, l3, l4

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
        shiftedPt_3 = array('f', [ 0 ] )
        shiftedPt_3B = updateTree.Branch('shiftedPt_3', shiftedPt_3, 'shiftedPt_3/F')
        shiftedPt_4 = array('f', [ 0 ] )
        shiftedPt_4B = updateTree.Branch('shiftedPt_4', shiftedPt_4, 'shiftedPt_4/F')
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

        size = updateTree.GetEntries()
        print size,"   ",file_
        cnt = 0
        for row in updateTree :
            cnt += 1
            #if cnt > 100 : break

            l3pt = getattr( row, '%sPt' % l3 )
            l3phi = getattr( row, '%sPhi' % l3 )
            l4pt = getattr( row, '%sPt' % l4 )
            l4phi = getattr( row, '%sPhi' % l4 )

            shiftedPt_3[0] = l3pt
            shiftedPt_4[0] = l4pt
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



            # Don't even check this for data
            if 'data' in sample :
                shiftedPt_3B.Fill()
                shiftedPt_4B.Fill()
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
            l3Shifted = False
            if 't' in l3 and getattr( row, '%sZTTGenMatching' % l3 ) != 6 :
                #print "l3Pt:        ", l3pt," DM: ",getattr( row, '%sDecayMode' % l3 )," gen_match: ",getattr( row, '%sZTTGenMatching' % l3 )
                #print " -- corr pt: ", correctTauPt( l3, l3pt, getattr( row, '%sZTTGenMatching' % l3 ), getattr( row, '%sDecayMode' % l3 ) )
                shiftedPt_3[0] = correctTauPt( l3, l3pt, getattr( row, '%sZTTGenMatching' % l3 ), getattr( row, '%sDecayMode' % l3 ) )
                if shiftedPt_3[0] != l3pt :
                    l3Shifted = True
            l4Shifted = False
            if 't' in l4 and getattr( row, '%sZTTGenMatching' % l4 ) != 6 :
                #print "l4Pt:        ", l4pt," DM: ",getattr( row, '%sDecayMode' % l4 )," gen_match: ",getattr( row, '%sZTTGenMatching' % l4 )
                #print " -- corr pt: ", correctTauPt( l4, l4pt, getattr( row, '%sZTTGenMatching' % l4 ), getattr( row, '%sDecayMode' % l4 ) )
                shiftedPt_4[0] = correctTauPt( l4, l4pt, getattr( row, '%sZTTGenMatching' % l4 ), getattr( row, '%sDecayMode' % l4 ) )
                if shiftedPt_4[0] != l4pt :
                    l4Shifted = True

            # only recompute if there were shifts applied
            if l3Shifted or l4Shifted :
                # delta x, y shifts from corrections
                dx3 = TMath.Cos( l3phi ) * (shiftedPt_3[0] - l3pt)
                dy3 = TMath.Sin( l3phi ) * (shiftedPt_3[0] - l3pt)
                dx4 = TMath.Cos( l4phi ) * (shiftedPt_4[0] - l4pt)
                dy4 = TMath.Sin( l4phi ) * (shiftedPt_4[0] - l4pt)
                #print "dx3,dy3,dx4,dy4",dx3,dy3,dx4,dy4
                
                shiftedMET[0], shiftedMETPhi[0] = adjustMet(shiftedMET[0], shiftedMETPhi[0], dx3, dy3, dx4, dy4 )
                shiftedUncMETUp[0], shiftedUncMETPhiUp[0] = adjustMet(shiftedUncMETUp[0], shiftedUncMETPhiUp[0], dx3, dy3, dx4, dy4 )
                shiftedUncMETDown[0], shiftedUncMETPhiDown[0] = adjustMet(shiftedUncMETDown[0], shiftedUncMETPhiDown[0], dx3, dy3, dx4, dy4 )
                shiftedClustMETUp[0], shiftedClustMETPhiUp[0] = adjustMet(shiftedClustMETUp[0], shiftedClustMETPhiUp[0], dx3, dy3, dx4, dy4 )
                shiftedClustMETDown[0], shiftedClustMETPhiDown[0] = adjustMet(shiftedClustMETDown[0], shiftedClustMETPhiDown[0], dx3, dy3, dx4, dy4 )


            shiftedPt_3B.Fill()
            shiftedPt_4B.Fill()
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
    pool = multiprocessing.Pool(processes = 7 )
    #pool = multiprocessing.Pool(processes = 1 )
    multiprocessingOutputs = []
    debug = False
    #debug = True
    doAZH = True



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
            #azhSamples.append('ttHTauTau%i' % mass)
        for mass in [125,] :
            azhSamples.append('ZHWW%i' % mass)
            azhSamples.append('HZZ%i' % mass)

        #azhSamples = ['ggZZ4m','ggZZ4e']
        for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
            azhSamples.append('azh%i' % mass)

        #azhSamples = []
        for era in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] :
            azhSamples.append('dataEE-%s' % era)
            azhSamples.append('dataMM-%s' % era)
            azhSamples.append('dataSingleE-%s' % era)
            azhSamples.append('dataSingleM-%s' % era)

        azhSamples = ['azh300',]

        name = 'azhJune19AZH_test'
        #inDir = '/nfs_scratch/truggles/'+name+'_svFitPrep/'
        inDir = '/nfs_scratch/truggles/'+name+'/'
        #name = 'svFitTmp'
        #inDir = '/data/truggles/'+name+'/'
        checkDir( inDir )
        jobId = ''
        channels = ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm',] # 8
        #channels = ['mmtt',] # 10
        for channel in channels :
            ttreePath = channel+'/final/Ntuple'
            for sample in azhSamples :
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




