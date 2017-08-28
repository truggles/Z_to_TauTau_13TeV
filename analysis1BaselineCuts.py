from util.buildTChain import makeTChain, getTree, getEventCount
from util.fileLength import file_len
import util.pileUpVertexCorrections
from analysis2IsoJetsAndDups import renameBranches
import ROOT
from time import gmtime, strftime
import analysisCuts
import analysisPlots
import multiprocessing
import math
from ROOT import gPad, gROOT
from util.helpers import checkDir
import os
from smart_getenv import getenv
from util.htxsTools import getHtxsCutMapStage0, getHtxsCutMapStage1



# For defining numFilesPerCycle for specific samples
def getMergeMap( analysis ) :
    mergeMap = {
        'Sync' : {'x' : 999},
        'htt' : {'x' : 999},
        'azh' : {
	        #'x' : 999,
            'dataEE-B' : 10,
            'dataEE-C' : 10,
            'dataEE-D' : 10,
            'dataEE-E' : 10,
            'dataEE-F' : 10,
            'dataEE-G' : 10,
            'dataEE-H' : 10,
            'dataMM-B' : 10,
            'dataMM-C' : 10,
            'dataMM-D' : 10,
            'dataMM-E' : 10,
            'dataMM-F' : 10,
            'dataMM-G' : 10,
            'dataMM-H' : 10,
            'DYJets' : 20,
            'DYJets1' : 20,
            'DYJets2' : 20,
            'DYJets3' : 20,
            'DYJets4' : 20,
            'WZ3l1nu' : 10,
            'ZZ4lAMCNLO' : 1,
            'TT' : 3,
            'ggZZ4m' : 1,
            'ggZZ2e2m' : 1,
            'ggZZ2e2tau' : 1,
            'ggZZ4tau' : 1,
            'ggZZ4e' : 1,
            'ggZZ2m2tau' : 1,
        } # end azh
    }
    return mergeMap[ analysis ]



def skipChanDataCombo( channel, sample, analysis ) :
    # HTT
    if analysis == 'htt' :
        if (channel == 'em') and ('data' in sample) and not ('dataEM' in sample) : return True
        if (channel == 'et') and ('data' in sample) and not ('dataET' in sample) : return True
        if (channel == 'mt') and ('data' in sample) and not ('dataMT' in sample) : return True
        if (channel == 'tt') and ('data' in sample) and not ('dataTT' in sample) : return True
    # AZH
    if analysis == 'azh' :
        if (channel in ['eeee', 'eeem', 'eeet', 'eemt', 'eett']) and ('data' in sample) and not ('dataEE' in sample) : return True
        if (channel in ['mmmm', 'emmm', 'emmt', 'mmmt', 'mmtt']) and ('data' in sample) and not ('dataMM' in sample) : return True
    return False



#for sample in samples :
def initialCut( outFile, analysis, sample, samples, channel, cutMapper, svFitPrep, svFitPost, skimHdfs, skimmed, count, fileMin=0, fileMax=9999 ) :
    #print "initialCut fileMin: %i, fileMax %i" % (fileMin, fileMax)
    #treeOutDir = outFile.mkdir( path.split('/')[0] )

    ''' Get initial chain '''
    #print "###   %s  ###" % sample
    #print "Channel:  %s" % channel
    sampF = ''
    if svFitPost == 'true' : sampF = 'sv/'
    if skimHdfs == 'true' : sampF = 'hdfs/'
    if skimmed == 'true' : sampF = 'skimmed/'
    if svFitPost == 'true' or skimmed == 'true' :
        sampleList = 'meta/NtupleInputs_%s/%s%s_%s.txt' % (analysis, sampF, sample, channel)
    else :
        sampleList = 'meta/NtupleInputs_%s/%s%s.txt' % (analysis, sampF, sample)
    path = '%s/final/Ntuple' % channel
    #print "sample List and path", sampleList, path
    chain = makeTChain( sampleList, path, 0, fileMin, fileMax )

    # Store eventCount
    getEvtInfo = getEventCount( sampleList, channel, 0, fileMin, fileMax )
    eventCount = getEvtInfo[0]
    summedWeights = getEvtInfo[1]

    numEntries = chain.GetEntries()
    #print "%25s : %10i" % ('Initial', numEntries)
    initialQty = "%25s : %10i" % ('Initial', numEntries)
    
    
    ''' Get channel specific general cuts '''
    #exec 'cutMap = analysisCuts.%s( channel )' % cutMapper
    cutString = ''
    isData = False
    hdfsSkim = False # Adjust MC trigger for final analysis (should be changed
                     # if we are skimming
    if 'data' in sample :
        isData = True
    if skimHdfs == 'true' :
        hdfsSkim = True
    cutString = analysisCuts.getCut( analysis, channel, cutMapper, isData, hdfsSkim )
    #print cutString
    	
    ''' Copy and make some cuts while doing it '''
    ROOT.gROOT.cd() # This makes copied TTrees get written to general ROOT, not our TFile
    
    chainNew = analysisCuts.makeGenCut( chain, cutString )
    numEntries = chainNew.GetEntries()
    postCutQty = "%25s : %10i" % (cutMapper, numEntries)
    
    #treeOutDir.cd()
    #chainNew.Write()
    return (outFile, chainNew, initialQty, postCutQty, eventCount, summedWeights)




def runCuts(analysis, sample, samples, channel, count, num, mid1, mid2,cutMapper,numFilesPerCycle,svFitPrep,svFitPost,skimHdfs,skimmed) :

    save = '%s_%i_%s' % (sample, count, channel)
    #print "save",save
    print "%5i %20s %10s %3i: ====>>> START Cuts <<<====" % (num, sample, channel, count)

    ''' 1. Make cuts and save '''
    #print "%5i %20s %10s %3i: Started Cuts" % (num, sample, channel, count)
    if svFitPrep == 'true' :
        outFile1 = ROOT.TFile('/data/truggles/svFitPrep/%s%s/%s.root' % (analysis, mid1, save), 'RECREATE')
    elif skimHdfs == 'true' :
        outFile1 = ROOT.TFile('/nfs_scratch/truggles/%s%s/%s.root' % (analysis, mid1.strip('1'), save), 'RECREATE')
    else :
        outFile1 = ROOT.TFile('%s%s/%s.root' % (analysis, mid1, save), 'RECREATE')
    #print "initialCut: file values: cnt %i   min %i   max %i" % ( count, count * numFilesPerCycle, ((count + 1) * numFilesPerCycle) - 1 )
    cutOut = initialCut( outFile1, analysis, sample, samples, channel, cutMapper, svFitPrep, svFitPost, skimHdfs, skimmed, count, count * numFilesPerCycle, ((count + 1) * numFilesPerCycle) - 1 )
    initialQty = cutOut[2]
    postCutQty = cutOut[3]
    eventCount = cutOut[4]
    summedWeights = cutOut[5]
    dir1 = cutOut[0].mkdir( channel )
    dir1.cd()
    # Make a histo with "eventCount" for making meta stats after initial cut
    eventCountH = ROOT.TH1D('eventCount','eventCount',1,-0.5,0.5)
    eventCountH.SetBinContent( 1, eventCount )
    eventCountH.Write()
    summedWeightsH = ROOT.TH1D('summedWeights','summedWeights',1,-0.5,0.5)
    summedWeightsH.SetBinContent( 1, summedWeights )
    summedWeightsH.Write()
    dir2 = dir1.mkdir( 'final' )
    dir2.cd()
    cutOut[1].Write()

    outFile1.Close()
    print "%5i %20s %10s %3i: Finished Cuts" % (num, sample, channel, count)

    if num < 1000 :
        return (num, sample, channel, count, initialQty, postCutQty)
    else :
        print "Over 1000 iterations.  Summary skipped"


def runIsoOrder(analysis, sample, channel, count, num, mid1, mid2,cutMapper,numFilesPerCycle) :

    #if svFitPost == 'true' : SVF = True
    #else : SVF = False

    save = '%s_%i_%s' % (sample, count, channel)
    #print "save",save
    print "%5i %20s %10s %3i: ====>>> START Iso Order <<<====" % (num, sample, channel, count)

    ''' 2. Rename branches, Tau and Iso order legs '''
    print "%5i %20s %10s %3i: Started Iso Ordering" % (num, sample, channel, count)
    isoQty = renameBranches( analysis, mid1, mid2, save, channel, count )

    ### FF values for data events
    doFF = getenv('doFF', type=bool)
    if doFF and channel == 'tt' :
        from util.applyFakeFactors import fillFakeFactorValues
        fillFakeFactorValues( analysis, mid2, save, channel )

    #output.put( '%s%s/%s.root' % (analysis, mid2, save) )
    print "%5i %20s %10s %3i: Finished Iso Ordering" % (num, sample, channel, count)

    #output.put((num, sample, channel, count, initialQty, postCutQty, isoQty ))
    print "%5i %20s %10s %3i: ====>>> DONE Iso Order <<<====" % (num, sample, channel, count)
    return (num, sample, channel, count, isoQty )




def doInitialCuts(analysis, samples, **fargs) :
    assert isinstance(samples,dict)

    mergeMap = getMergeMap(analysis)
        
    begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print begin
    channels = fargs[ 'channels' ]
    ''' Start multiprocessing tests '''
    #output = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes= fargs[ 'numCores' ] )
    multiprocessingOutputs = []

    if fargs[ 'svFitPrep' ] == 'true' :
	checkDir( '/data/truggles/svFitPrep/%s%s' % (analysis, fargs[ 'mid1']) )
    if fargs[ 'skimHdfs' ] == 'true' :
	checkDir( '/nfs_scratch/truggles/%s%s' % (analysis, fargs[ 'mid1'].strip('1')) )
    
    num = 0
    for sample in samples :

        # Close pool between subsequent uses to reduce memory usage   
        if fargs['debug'] != 'true' and fargs['skimHdfs'] == 'true' :
            pool.close()
            pool = multiprocessing.Pool(processes= fargs[ 'numCores' ] )


        numFilesPerCycle = fargs['numFilesPerCycle']
        if sample in mergeMap.keys() and fargs[ 'skimmed' ] != 'true' :
            numFilesPerCycle = mergeMap[sample]

        sampF = ''
        if fargs['svFitPost'] == 'true' : sampF = 'sv/'
        if fargs['skimHdfs'] == 'true' : sampF = 'hdfs/'
        if fargs['skimmed'] == 'true' : sampF = 'skimmed/'

        for channel in channels :

            # Check if we should skip running over data set
            if skipChanDataCombo( channel, sample, analysis ) : continue

            if fargs['svFitPost'] == 'true' or fargs['skimmed'] == 'true' :
                fileLen = file_len( 'meta/NtupleInputs_%s/%s%s_%s.txt' % (analysis, sampF, sample, channel) )
            else :
                fileLen = file_len( 'meta/NtupleInputs_%s/%s%s.txt' % (analysis, sampF, sample) )
            if fileLen == 0 : 
                print "\n\nFile Length == 0 !!!!!! skipping sample %s \n\n" % sample
                continue

            count = 0
            go = True
            while go :

                print " ====>  Adding %s_%s_%i_%s  <==== " % (analysis, sample, count, channel)
    

                if not fargs['debug'] == 'true' :
                    multiprocessingOutputs.append( pool.apply_async(runCuts, args=(analysis,
                                                                                    sample,
                                                                                    samples,
                                                                                    channel,
                                                                                    count,
                                                                                    num,
                                                                                    fargs['mid1'],
                                                                                    fargs['mid2'],
                                                                                    fargs['cutMapper'],
                                                                                    numFilesPerCycle,
                                                                                    fargs['svFitPrep'],
                                                                                    fargs['svFitPost'],
                                                                                    fargs['skimHdfs'],
                                                                                    fargs['skimmed'])) )
                """ for debugging without multiprocessing """
                if fargs['debug'] == 'true' :
                    runCuts(analysis,
                                                                                    sample,
                                                                                    samples,
                                                                                    channel,
                                                                                    count,
                                                                                    num,
                                                                                    fargs['mid1'],
                                                                                    fargs['mid2'],
                                                                                    fargs['cutMapper'],
                                                                                    numFilesPerCycle,
                                                                                    fargs['svFitPrep'],
                                                                                    fargs['svFitPost'],
                                                                                    fargs['skimHdfs'],
                                                                                    fargs['skimmed'])

                num +=  1
                count += 1
                # Make sure we loop over large samples to get all files
                if count * numFilesPerCycle >= fileLen : go = False

        if fargs['debug'] != 'true' and fargs['skimHdfs'] == 'true' :
            mpResults = [p.get() for p in multiprocessingOutputs]

            print "\n"
            print "#################################################################"
            print "###       skimHdfs finished for %20s          ###" % sample
            print "#################################################################"
            print "\n"
            multiprocessingOutputs = []
    
            
    if fargs['debug'] == 'true' :
        print "#################################################################"
        print "###               Finished, summary below                     ###"
        print "#################################################################"
    
    
    if fargs['debug'] != 'true' and fargs['skimHdfs'] != 'true' :
        mpResults = [p.get() for p in multiprocessingOutputs]
    
        print "#################################################################"
        print "###               Finished, summary below                     ###"
        print "#################################################################"
        
        print "\nStart Time: %s" % str( begin )
        print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
        print "\n"

        print " --- Cut used: %s" % fargs['cutMapper']
        print " --- Analysis: %s" % analysis
        print " --- Cut folder: %s%s" % (analysis, fargs['mid1'])
        print " --- Iso folder: %s%s" % (analysis, fargs['mid2'])
        print "\n"
        
        totalIn = 0
        totalOut = 0
        mpResults.sort()
        for item in mpResults :
            if item is None : continue
            print "%5s %10s %5s count %s:" % (item[0], item[1], item[2], item[3])
            print item[4]
            print item[5]
            totalIn += int(item[4].split(' ')[-1])
            totalOut += int(item[5].split(' ')[-1])
    
        print "\nTotal In:", totalIn
        print "Total Out:", totalOut,"\n"
    print "Start Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )


def doInitialOrder(analysis, samples, **fargs) :
    assert isinstance(samples,dict)

    mergeMap = getMergeMap(analysis)
        
    begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print begin
    channels = fargs[ 'channels' ]
    ''' Start multiprocessing tests '''
    #output = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes= fargs[ 'numCores' ] )
    multiprocessingOutputs = []
    
    num = 0
    for sample in samples :
    
        numFilesPerCycle = fargs['numFilesPerCycle']
        if sample in mergeMap.keys() and fargs[ 'skimmed' ] != 'true' :
            numFilesPerCycle = mergeMap[sample]

        sampF = ''
        if fargs['svFitPost'] == 'true' : sampF = 'sv/'
        if fargs['skimmed'] == 'true' : sampF = 'skimmed/'

        for channel in channels :
    
            # Check if we should skip running over data set
            if skipChanDataCombo( channel, sample, analysis ) : continue

            if fargs['svFitPost'] == 'true' or fargs['skimmed'] == 'true' :
                fileLen = file_len( 'meta/NtupleInputs_%s/%s%s_%s.txt' % (analysis, sampF, sample, channel) )
            else :
                fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (analysis, sample) )
            if fileLen == 0 : 
                print "\n\nFile Length == 0 !!!!!! skipping sample %s \n\n" % sample
                continue

            count = 0
            go = True
            while go :

                print " ====>  Adding %s_%s_%i_%s  <==== " % (analysis, sample, count, channel)
    
                if not fargs['debug'] == 'true' :
                    multiprocessingOutputs.append( pool.apply_async(runIsoOrder, args=(analysis,
                                                                                    sample,
                                                                                    channel,
                                                                                    count,
                                                                                    num,
                                                                                    fargs['mid1'],
                                                                                    fargs['mid2'],
                                                                                    fargs['cutMapper'],
                                                                                    numFilesPerCycle)) )
                """ for debugging without multiprocessing """
                if fargs['debug'] == 'true' :
                    runIsoOrder(analysis,
                                                                                    sample,
                                                                                    channel,
                                                                                    count,
                                                                                    num,
                                                                                    fargs['mid1'],
                                                                                    fargs['mid2'],
                                                                                    fargs['cutMapper'],
                                                                                    numFilesPerCycle)
                num +=  1
                count += 1
                # Make sure we loop over large samples to get all files
                if count * numFilesPerCycle+1 > fileLen : go = False
    
    
    if fargs['debug'] == 'true' :
        print "#################################################################"
        print "###               Finished, summary below                     ###"
        print "#################################################################"

    if fargs['debug'] != 'true' :
        mpResults = [p.get() for p in multiprocessingOutputs]
    
        print "#################################################################"
        print "###               Finished, summary below                     ###"
        print "#################################################################"
        
        print "\nStart Time: %s" % str( begin )
        print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
        print "\n"
        
        print " --- Cut used: %s" % fargs['cutMapper']
        print " --- Analysis: %s" % analysis
        print " --- Cut folder: %s%s" % (analysis, fargs['mid1'])
        print " --- Iso folder: %s%s" % (analysis, fargs['mid2'])
        print "\n"
        
        mpResults.sort()
        totalIso = 0
        for item in mpResults :
            if item is None : continue
            print "%5s %10s %5s count %s:" % (item[0], item[1], item[2], item[3])
            print item[4]
            totalIso += int(item[4].split(' ')[-1])
            
        print "\nTotal Iso:", totalIso
        
    print "\nStart Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )



def drawHistos(analysis, samples, **fargs ) :

    print "\n%s\n" % fargs['mid3']

    mergeMap = getMergeMap(analysis)

    skipSSQCDDetails = False
    if 'skipSSQCDDetails' in fargs.keys() :
        if fargs['skipSSQCDDetails'] :
            skipSSQCDDetails = True

    genMap = {
        # sample : em , tt
        'ZTT' : {
                'tt' : '*(gen_match_1 == 5 && gen_match_2 == 5)'},
        'ZL' : {
                'tt' : '*(gen_match_1 < 6 && gen_match_2 < 6 && !(gen_match_1 == 5 && gen_match_2 == 5))'},
        'ZJ' : {
                'tt' : '*(gen_match_2 == 6 || gen_match_1 == 6)'},
        'QCD' : {
                'tt' : '*(FFWeightQCD)'},
        'TTT' : {
                'tt' : '*(gen_match_1 == 5 && gen_match_2 == 5)'},
        'TTJ' : {
                'tt' : '*(gen_match_1 != 5 || gen_match_2 != 5)'},
        'VVT' : {
                'tt' : '*(gen_match_1 == 5 && gen_match_2 == 5)'},
        'VVJ' : {
                'tt' : '*(gen_match_1 != 5 || gen_match_2 != 5)'},
        'RedBkgYield' : {'xxxx' : '*(1.)'},
        'RedBkgShape' : {'xxxx' : '*(1.)'},
    }

    htxsStage0 = getHtxsCutMapStage0()
    htxsStage1 = getHtxsCutMapStage1()

    channels = fargs['channels']
    ''' Start PROOF multiprocessing Draw '''
    #ROOT.TProof.Open('workers=%s' % str( int(fargs['numCores']) ) )
    gROOT.SetBatch(True)
    
    ''' Start multiprocessing tests '''
    #output = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes= fargs[ 'numCores' ] )
    multiprocessingOutputs = []

    for sample in samples :
    
        numFilesPerCycle = fargs['numFilesPerCycle']
        if sample in mergeMap.keys() and fargs[ 'skimmed' ] != 'true' :
            numFilesPerCycle = mergeMap[sample]

        # the gen matching samples are: based off of the DYJets samples
        loopList = []
        doFF = getenv('doFF', type=bool)
        if 'DYJets' in sample and analysis == 'htt' :
            genList = ['ZTT', 'ZL', 'ZJ']
            loopList = genList
            #loopList.append( sample ) # don't keep full original
        elif sample == 'TT' and analysis == 'htt' :
            genList = ['TTT', 'TTJ']
            loopList = genList
            #loopList.append( sample ) # don't keep full original
        elif sample in ['T-tW', 'T-tchan', 'Tbar-tW', 'Tbar-tchan', 
                'WW1l1nu2q', 'WW2l2nu', 'WZ1l1nu2q', 'WZ1l3nu', 
                'WZ2l2q', 'WZ3l1nu', 'ZZ2l2nu', 'ZZ2l2q', 'ZZ4l', 
                'VV', 'WWW', 'ZZZ'] and analysis == 'htt' :
            genList = ['VVT', 'VVJ']
            loopList = genList
            #loopList.append( sample ) # don't keep full original

        # HTXS / Rivet Section
        elif 'ggHtoTauTau' in sample :
            loopList.append( sample )
            for cat in htxsStage0[ 'ggHtoTauTau' ].keys() :
                loopList.append( cat )
            for cat in htxsStage1[ 'ggHtoTauTau' ].keys() :
                loopList.append( cat )
        elif 'VBFHtoTauTau' in sample :
            loopList.append( sample )
            for cat in htxsStage0[ 'VBFHtoTauTau' ].keys() :
                loopList.append( cat )
            for cat in htxsStage1[ 'VBFHtoTauTau' ].keys() :
                loopList.append( cat )
        elif 'WMinusHTauTau' in sample :
            loopList.append( sample )
            for cat in htxsStage0[ 'WMinusHTauTau' ].keys() :
                loopList.append( cat )
            for cat in htxsStage1[ 'WMinusHTauTau' ].keys() :
                loopList.append( cat )
        elif 'WPlusHTauTau' in sample :
            loopList.append( sample )
            for cat in htxsStage0[ 'WPlusHTauTau' ].keys() :
                loopList.append( cat )
            for cat in htxsStage1[ 'WPlusHTauTau' ].keys() :
                loopList.append( cat )
        elif 'ZHTauTau' in sample :
            loopList.append( sample )
            for cat in htxsStage0[ 'ZHTauTau' ].keys() :
                loopList.append( cat )
            for cat in htxsStage1[ 'ZHTauTau' ].keys() :
                loopList.append( cat )

        elif 'data' in sample and doFF :
            loopList.append( sample )
            loopList.append( 'QCD-'+sample.split('-')[1] )
        elif 'data' in sample and analysis == 'azh' :
            loopList.append( sample )
            loopList.append( 'RedBkgYield-'+sample.split('-')[1] )
            loopList.append( 'RedBkgShape-'+sample.split('-')[1] )
        else : loopList.append( sample )

    
        sampF = ''
        if fargs['svFitPost'] == 'true' : sampF = 'sv/'
        if fargs['skimmed'] == 'true' : sampF = 'skimmed/'
        for subName in loopList :
            #print "SubName:",subName
            if subName == 'QCD' and 'data' in sample : saveName = 'QCD'
            elif 'RedBkg' in subName and 'data' in sample : saveName = subName
            elif 'QCD' in subName and 'data' in sample and doFF : saveName = subName
            elif subName != sample : saveName = "%s-%s" % (sample.split('_')[0], subName)
            else : saveName = sample.split('_')[0]
            
            for channel in channels :

                # Check if we should skip running over data set
                if skipChanDataCombo( channel, sample, analysis ) : continue

                if fargs['svFitPost'] == 'true' or fargs['skimmed'] == 'true' :
                    fileLen = file_len( 'meta/NtupleInputs_%s/%s%s_%s.txt' % (analysis, sampF, sample, channel) )
                else :
                    fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (analysis, sample) )
                print "File len:",fileLen
                #print "Num files / cycle:",numFilesPerCycle
                numIters = int( math.ceil( 1. * fileLen / numFilesPerCycle ) )
                #print "Num Iters: %i" % numIters


                print " ====>  Starting Plots For %s_%s_%s  <==== " % (analysis, saveName, channel)
    
                chain = ROOT.TChain('Ntuple')
                for i in range( numIters ) :
                    #print "%s_%i" % ( sample, i)
                    #print " --- Adding to chain: %s%s/%s_%i_%s.root" % (analysis, fargs['mid2'], sample.split('_')[0], i, channel)
                    chain.Add('%s%s/%s_%i_%s.root' % (analysis, fargs['mid2'], sample.split('_')[0], i, channel) )
                print "ENTRIES: %s %i" % (sample, chain.GetEntries() )
                if 'data' in sample : isData = True
                else : isData = False
                additionalCut = fargs['additionalCut']
                if subName != sample and 'RedBkg' not in subName and 'QCD-' not in subName : 
                    if subName in genMap.keys() :
                        if genMap[subName][channel] == '' : continue
                        if additionalCut == '' : additionalCut = genMap[subName][channel] 
                        else : additionalCut += genMap[subName][channel] 
                    else : # hopefully HTXS
                        noMassSig = sample[:-3] # sample sans 3 digit mass
                        if subName in htxsStage0[noMassSig].keys() :
                            if additionalCut == '' : additionalCut = htxsStage0[noMassSig][subName]
                            else : additionalCut += htxsStage0[noMassSig][subName]
                        if subName in htxsStage1[noMassSig].keys() :
                            if additionalCut == '' : additionalCut = htxsStage1[noMassSig][subName]
                            else : additionalCut += htxsStage1[noMassSig][subName]
                                
                #print "AdditionalCuts",additionalCut

                blind = False
                outFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, fargs['mid3'], saveName , channel), 'RECREATE')
                if not fargs['debug'] == 'true' :
                    multiprocessingOutputs.append( pool.apply_async(analysisPlots.plotHistosProof,
                                                                                    args=(analysis,
                                                                                    outFile,
                                                                                    chain,
                                                                                    sample,
                                                                                    channel,
                                                                                    isData,
                                                                                    additionalCut,
                                                                                    blind,
                                                                                    skipSSQCDDetails,
                                                                                    sample+'-'+subName)) )
                """ for debugging without multiprocessing """
                if fargs['debug'] == 'true' :
                    analysisPlots.plotHistosProof(
                                                                                    analysis,
                                                                                    outFile,
                                                                                    chain,
                                                                                    sample,
                                                                                    channel,
                                                                                    isData,
                                                                                    additionalCut,
                                                                                    blind,
                                                                                    skipSSQCDDetails,
                                                                                    sample+'-'+subName) 
                #analysisPlots.plotHistosProof( analysis, outFile, chain, sample, channel, isData, additionalCut, blind, skipSSQCDDetails )
                #outFile.Close()

    if fargs['debug'] != 'true' :
        mpResults = [p.get() for p in multiprocessingOutputs]
    
    print "#################################################################"
    print "###               Finished plotting all samples               ###"
    print "#################################################################"
         




