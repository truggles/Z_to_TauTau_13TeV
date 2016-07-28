from util.buildTChain import makeTChain, getTree
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


def skipChanDataCombo( channel, sample, analysis ) :
    # HTT
    if analysis == 'htt' :
        if (channel == 'em') and ('data' in sample) and (sample != 'dataEM') : return True
        if (channel == 'et') and ('data' in sample) and (sample != 'dataE') : return True
        if (channel == 'mt') and ('data' in sample) and (sample != 'dataM') : return True
        if (channel == 'tt') and ('data' in sample) and (sample != 'dataTT') : return True
    # AZH
    if analysis == 'azh' :
        if (channel in ['eeee', 'eeem', 'eeet', 'eemt', 'eett']) and ('data' in sample) and (sample != 'dataEE') : return True
        if (channel in ['mmmm', 'emmm', 'emmt', 'mmmt', 'mmtt']) and ('data' in sample) and (sample != 'dataMM') : return True
    return False



#for sample in samples :
def initialCut( outFile, analysis, sample, channel, cutMapper, svFitPrep, svFitPost, count, fileMin=0, fileMax=9999 ) :
    #print "initialCut fileMin: %i, fileMax %i" % (fileMin, fileMax)
    #treeOutDir = outFile.mkdir( path.split('/')[0] )

    ''' Get initial chain '''
    #print "###   %s  ###" % sample
    #print "Channel:  %s" % channel
    if svFitPost == 'true' :
        sampleList = 'meta/NtupleInputs_%s/sv_%s_%s.txt' % (analysis, sample, channel)
        path = '%s/Ntuple' % channel
    else :
        sampleList = 'meta/NtupleInputs_%s/%s.txt' % (analysis, sample)
        path = '%s/final/Ntuple' % channel
    #print "sample List and path", sampleList, path
    # This should allow us to run over sections of files
    if svFitPrep == 'true' :
        files = open( sampleList, 'r' )	
        i = 0
        for file_ in files :
            if i == count :
                f = ROOT.TFile( file_.strip() )
                chain = f.Get( path )
            i += 1
    else :
        #print "svFitPrep not true"
        chain = makeTChain( sampleList, path, 0, fileMin, fileMax )
    numEntries = chain.GetEntries()
    #print "%25s : %10i" % ('Initial', numEntries)
    initialQty = "%25s : %10i" % ('Initial', numEntries)
    
    
    ''' Get channel specific general cuts '''
    #exec 'cutMap = analysisCuts.%s( channel )' % cutMapper
    cutString = ''
    if 'data' in sample :
        isData = True
        cutString = analysisCuts.getCut( analysis, channel, cutMapper, isData )
    else :
        cutString = analysisCuts.getCut( analysis, channel, cutMapper )
    	
    ''' Copy and make some cuts while doing it '''
    ROOT.gROOT.cd() # This makes copied TTrees get written to general ROOT, not our TFile
    
    chainNew = analysisCuts.makeGenCut( chain, cutString )
    numEntries = chainNew.GetEntries()
    postCutQty = "%25s : %10i" % (cutMapper, numEntries)
    
    #treeOutDir.cd()
    #chainNew.Write()
    return (outFile, chainNew, initialQty, postCutQty)




def runCuts(analysis, sample, channel, count, num, mid1, mid2,cutMapper,numFilesPerCycle,svFitPrep,svFitPost) :

    save = '%s_%i_%s' % (sample, count, channel)
    #print "save",save
    print "%5i %20s %10s %3i: ====>>> START Cuts <<<====" % (num, sample, channel, count)

    ''' 1. Make cuts and save '''
    #print "%5i %20s %10s %3i: Started Cuts" % (num, sample, channel, count)
    if svFitPrep == 'true' :
        outFile1 = ROOT.TFile('/data/truggles/svFitPrep/%s%s/%s.root' % (analysis, mid1, save), 'RECREATE')
    else :
        outFile1 = ROOT.TFile('%s%s/%s.root' % (analysis, mid1, save), 'RECREATE')
    #print "initialCut: file values: cnt %i   min %i   max %i" % ( count, count * numFilesPerCycle, ((count + 1) * numFilesPerCycle) - 1 )
    cutOut = initialCut( outFile1, analysis, sample, channel, cutMapper, svFitPrep, svFitPost, count, count * numFilesPerCycle, ((count + 1) * numFilesPerCycle) - 1 )
    dir1 = cutOut[0].mkdir( channel )
    dir1.cd()
    cutOut[1].Write()
    outFile1.Close()
    initialQty = cutOut[2]
    postCutQty = cutOut[3]
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
    #output.put( '%s%s/%s.root' % (analysis, mid2, save) )
    print "%5i %20s %10s %3i: Finished Iso Ordering" % (num, sample, channel, count)

    #output.put((num, sample, channel, count, initialQty, postCutQty, isoQty ))
    print "%5i %20s %10s %3i: ====>>> DONE Iso Order <<<====" % (num, sample, channel, count)
    return (num, sample, channel, count, isoQty )




def doInitialCuts(analysis, samples, **fargs) :
        
    begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print begin
    channels = fargs[ 'channels' ]
    ''' Start multiprocessing tests '''
    #output = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes= fargs[ 'numCores' ] )
    multiprocessingOutputs = []

    import os
    if fargs[ 'svFitPrep' ] == 'true' :
        if not os.path.exists( '/data/truggles/svFitPrep/%s%s' % (analysis, fargs[ 'mid1']) ) :
            os.makedirs( '/data/truggles/svFitPrep/%s%s' % (analysis, fargs[ 'mid1' ]) )
    
    num = 0
    for sample in samples :
    
        fileLenEM = 9999
        fileLenTT = 9999
        if fargs['svFitPost'] == 'true' :
            fileLenEM = file_len( 'meta/NtupleInputs_%s/sv_%s_em.txt' % (analysis, sample) )
            fileLenTT = file_len( 'meta/NtupleInputs_%s/sv_%s_tt.txt' % (analysis, sample) )
            fileLen = max( fileLenEM, fileLenTT )
        else :
            fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (analysis, sample) )
        if fileLen == 0 : 
            print "\n\nFile Length == 0 !!!!!! skipping sample %s \n\n" % sample
            continue
        go = True
        count = 0
        while go :
            for channel in channels :

                # Check if we should skip running over data set
                if skipChanDataCombo( channel, sample, analysis ) : continue

                print " ====>  Adding %s_%s_%i_%s  <==== " % (analysis, sample, count, channel)
    





                if not fargs['debug'] == 'true' :
                    multiprocessingOutputs.append( pool.apply_async(runCuts, args=(analysis,
                                                                                    sample,
                                                                                    channel,
                                                                                    count,
                                                                                    num,
                                                                                    fargs['mid1'],
                                                                                    fargs['mid2'],
                                                                                    fargs['cutMapper'],
                                                                                    fargs['numFilesPerCycle'],
                                                                                    fargs['svFitPrep'],
                                                                                    fargs['svFitPost'])) )
                """ for debugging without multiprocessing """
                if fargs['debug'] == 'true' :
                    runCuts(analysis,
                                                                                    sample,
                                                                                    channel,
                                                                                    count,
                                                                                    num,
                                                                                    fargs['mid1'],
                                                                                    fargs['mid2'],
                                                                                    fargs['cutMapper'],
                                                                                    fargs['numFilesPerCycle'],
                                                                                    fargs['svFitPrep'],
                                                                                    fargs['svFitPost'])

                num +=  1
    
            count += 1
            
            # Make sure we loop over large samples to get all files
            if count * fargs['numFilesPerCycle'] >= fileLen : go = False
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
        
    begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print begin
    channels = fargs[ 'channels' ]
    ''' Start multiprocessing tests '''
    #output = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes= fargs[ 'numCores' ] )
    multiprocessingOutputs = []
    
    num = 0
    for sample in samples :
    
        fileLenEM = 9999
        fileLenTT = 9999
        if fargs['svFitPost'] == 'true' :
            fileLenEM = file_len( 'meta/NtupleInputs_%s/sv_%s_em.txt' % (analysis, sample) )
            fileLenTT = file_len( 'meta/NtupleInputs_%s/sv_%s_tt.txt' % (analysis, sample) )
            fileLen = max( fileLenEM, fileLenTT )
        else :
            fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (analysis, sample) )
        if fileLen == 0 : 
            print "\n\nFile Length == 0 !!!!!! skipping sample %s \n\n" % sample
            continue
        go = True
        count = 0
        while go :
            for channel in channels :
    
                # Check if we should skip running over data set
                if skipChanDataCombo( channel, sample, analysis ) : continue

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
                                                                                    fargs['numFilesPerCycle'])) )
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
                                                                                    fargs['numFilesPerCycle'])
                num +=  1
    
            count += 1
            
            # Make sure we loop over large samples to get all files
            if count * fargs['numFilesPerCycle']+1 > fileLen : go = False
    
    
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
    genMap = {
        # sample : em , tt
        'ZTT' : {'em' : '*(gen_match_1 > 2 && gen_match_2 > 3)',
                'tt' : '*(gen_match_1 == 5 && gen_match_2 == 5)'},
        'ZL' : {'em' : '',
                'tt' : '*(gen_match_1 < 6 && gen_match_2 < 6 && !(gen_match_1 == 5 && gen_match_2 == 5))'},
        'ZJ' : {'em' : '',
                'tt' : '*(gen_match_2 == 6 || gen_match_1 == 6)'},
        'ZLL' : {'em' : '*(gen_match_1 < 3 || gen_match_2 < 4)',
                'tt' : '*(gen_match_1 != 5 && gen_match_2 != 5)'},
        'QCD' : {'em' : '*(FFWeightQCD)',
                'tt' : '*(FFWeightQCD)'},
    }
    channels = fargs['channels']
    ''' Start PROOF multiprocessing Draw '''
    ROOT.TProof.Open('workers=%s' % str( int(fargs['numCores']) ) )
    gROOT.SetBatch(True)
    
    for sample in samples :

        # the gen matching samples are: based off of the DYJets samples
        loopList = []
        if 'DYJets' in sample and analysis == 'htt' :
            genList = ['ZTT', 'ZL', 'ZJ', 'ZLL']
            loopList = genList
            loopList.append( sample ) 
        elif 'data' in sample and fargs['doFRMthd'] == 'true' :
            loopList.append( sample )
            loopList.append( 'QCD' )
        else : loopList.append( sample )

    
        for subName in loopList :
            print "SubName:",subName
            if subName == 'QCD' and 'data' in sample : saveName = 'QCD'
            elif subName != sample : saveName = "%s-%s" % (sample.split('_')[0], subName)
            else : saveName = sample.split('_')[0]
            
            for channel in channels :

                # Check if we should skip running over data set
                if skipChanDataCombo( channel, sample, analysis ) : continue

                if fargs['svFitPost'] == 'true' :
                    fileLen = file_len( 'meta/NtupleInputs_%s/sv_%s_%s.txt' % (analysis, sample, channel) )
                else :
                    fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (analysis, sample) )
                print "File len:",fileLen
                print "Num files / cycle:",fargs['numFilesPerCycle']
                numIters = int( math.ceil( 1. * fileLen / fargs['numFilesPerCycle'] ) )
                print "Num Iters: %i" % numIters


                print " ====>  Starting Plots For %s_%s_%s  <==== " % (analysis, saveName, channel)
    
                chain = ROOT.TChain('Ntuple')
                outFile = ROOT.TFile('%s%s/%s_%s.root' % (analysis, fargs['mid3'], saveName , channel), 'RECREATE')
                for i in range( numIters ) :
                    #print "%s_%i" % ( sample, i)
                    #print " --- Adding to chain: %s%s/%s_%i_%s.root" % (analysis, fargs['mid2'], sample.split('_')[0], i, channel)
                    chain.Add('%s%s/%s_%i_%s.root' % (analysis, fargs['mid2'], sample.split('_')[0], i, channel) )
                print "ENTRIES: %s %i" % (sample, chain.GetEntries() )
                if 'data' in sample : isData = True
                else : isData = False
                additionalCut = fargs['additionalCut']
                if subName != sample : 
                    if genMap[subName][channel] == '' : continue
                    if additionalCut == '' : additionalCut = genMap[subName][channel] 
                    else : additionalCut += genMap[subName][channel] 
                print "AdditionalCuts",additionalCut
                blind = False
                analysisPlots.plotHistosProof( analysis, outFile, chain, sample, channel, isData, additionalCut, blind )
                outFile.Close()
         

if __name__ == '__main__' :
    runCutsAndIso('25ns', 'dataEM', 'em', 3, 1, 'None', '1nov2newNtups', '2nov2newNtups','signalCuts','PostSync',25)
