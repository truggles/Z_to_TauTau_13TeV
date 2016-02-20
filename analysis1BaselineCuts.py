from util.buildTChain import makeTChain
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

def getBkgMap() :
    bkgMap = {
                # cutMapper       samples
        'WJets' : ['wJetsShape', ['WJets',]],
        'QCDSync'   : ['QCDShapeSync', ['data_em', 'data_tt',]],
        'QCDLoose'   : ['QCDShapeLoose', ['data_em', 'data_tt',]],
        'None'  : ['', '', '', '']
        }
    return bkgMap


#for sample in samples :
def initialCut( outFile, grouping, sample, channel, cutMapper, cutName, fileMin=0, fileMax=9999 ) :
    #print "initialCut fileMin: %i, fileMax %i" % (fileMin, fileMax)
    path = '%s/final/Ntuple' % channel
    #treeOutDir = outFile.mkdir( path.split('/')[0] )

    ''' Get initial chain '''
    #print "###   %s  ###" % sample
    #print "Channel:  %s" % channel
    sampleList = 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample)
    # This should allow us to run over sections of files
    chain = makeTChain( sampleList, path, 0, fileMin, fileMax )
    numEntries = chain.GetEntries()
    #print "%25s : %10i" % ('Initial', numEntries)
    initialQty = "%25s : %10i" % ('Initial', numEntries)
    
    
    ''' Get channel specific general cuts '''
    exec 'cutMap = analysisCuts.%s( channel )' % cutMapper
    	
    ''' Copy and make some cuts while doing it '''
    ROOT.gROOT.cd() # This makes copied TTrees get written to general ROOT, not our TFile
    
    cutString = ' && '.join(cutMap[ cutName ])
    cutString = '('+cutString+')'
    chainNew = analysisCuts.makeGenCut( chain, cutString )
    numEntries = chainNew.GetEntries()
    #print "%25s : %10i" % (cutName, numEntries)
    postCutQty = "%25s : %10i" % (cutName, numEntries)
    
    #treeOutDir.cd()
    #chainNew.Write()
    return (outFile, chainNew, initialQty, postCutQty)




def runCuts(grouping, sample, channel, count, num, bkgs, mid1, mid2,cutMapper,cutName,numFilesPerCycle) :

    if 'data' in sample : save = 'data_%i_%s' % (count, channel)
    else : save = '%s_%i_%s' % (sample, count, channel)
    bkgMap = getBkgMap()
    #print "save",save
    print "%5i %20s %10s %3i: ====>>> START <<<====" % (num, sample, channel, count)

    ''' 1. Make cuts and save '''
    print "%5i %20s %10s %3i: Started Cuts" % (num, sample, channel, count)
    if bkgs != 'None' :
        outFile1 = ROOT.TFile('meta/%sBackgrounds/%s/cut/%s.root' % (grouping, bkgMap[ bkgs ][0], save), 'RECREATE')
    else :
        outFile1 = ROOT.TFile('%s%s/%s.root' % (grouping, mid1, save), 'RECREATE')
    cutOut = initialCut( outFile1, grouping, sample, channel, cutMapper, cutName, count * numFilesPerCycle, ((count + 1) * numFilesPerCycle) - 1 )
    dir1 = cutOut[0].mkdir( channel )
    dir1.cd()
    cutOut[1].Write()
    outFile1.Close()
    initialQty = cutOut[2]
    postCutQty = cutOut[3]
    print "%5i %20s %10s %3i: Finished Cuts" % (num, sample, channel, count)

    return (num, sample, channel, count, initialQty, postCutQty)


def runIsoOrder(grouping, sample, channel, count, num, bkgs, mid1, mid2,cutMapper,cutName,svf,svfName,numFilesPerCycle) :

    if svf == 'true' : SVF = True
    else : SVF = False

    if 'data' in sample : save = 'data_%i_%s' % (count, channel)
    else : save = '%s_%i_%s' % (sample, count, channel)
    bkgMap = getBkgMap()
    #print "save",save
    print "%5i %20s %10s %3i: ====>>> START Iso Order <<<====" % (num, sample, channel, count)

    ''' 2. Rename branches, Tau and Iso order legs '''
    print "%5i %20s %10s %3i: Started Iso Ordering" % (num, sample, channel, count)
    if SVF : 
        print 'Infile: %s%s.root' % (svfName,save)
        print 'Output: %s%s/%s.root' % (grouping, mid2, save)
    else :
        print 'Output: %s%s/%s.root' % (grouping, mid2, save)
    isoQty = renameBranches( grouping, mid1, mid2, save, channel, bkgMap[ bkgs ][0], SVF,svfName, count )
    #output.put( '%s%s/%s.root' % (grouping, mid2, save) )
    print "%5i %20s %10s %3i: Finished Iso Ordering" % (num, sample, channel, count)

    #output.put((num, sample, channel, count, initialQty, postCutQty, isoQty ))
    print "%5i %20s %10s %3i: ====>>> DONE Iso Order <<<====" % (num, sample, channel, count)
    return (num, sample, channel, count, isoQty )



def svFitPrep(grouping, samples, **fargs) :
        
    begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print begin
    channels = fargs[ 'channels' ]
    ''' Start multiprocessing tests '''
    #output = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes= fargs[ 'numCores' ] )
    multiprocessingOutputs = []
    
    num = 0
    for sample in samples :
    
        fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample) )
        go = True
        count = 0
        while go :
            for channel in channels :
    
                if (channel == 'em') and ('data' in sample) and (sample != 'data_em') : continue
                if (channel == 'et') and ('data' in sample) and (sample != 'data_et') : continue
                if (channel == 'mt') and ('data' in sample) and (sample != 'data_mt') : continue
                if (channel == 'tt') and ('data' in sample) and (sample != 'data_tt') : continue
                print " ====>  Adding %s_%s_%i_%s  <==== " % (grouping, sample, count, channel)
    
                multiprocessingOutputs.append( pool.apply_async(runCuts, args=(grouping,
                                                                                    sample,
                                                                                    channel,
                                                                                    count,
                                                                                    num,
                                                                                    fargs['bkgs'],
                                                                                    fargs['mid1'],
                                                                                    fargs['mid2'],
                                                                                    fargs['cutMapper'],
                                                                                    fargs['cutName'],
                                                                                    fargs['numFilesPerCycle'])) )
                num +=  1
    
            count += 1
            
            # Make sure we loop over large samples to get all files
            if count * fargs['numFilesPerCycle'] > fileLen : go = False
    
    
    mpResults = [p.get() for p in multiprocessingOutputs]
    
    #print(mpResults)
    print "#################################################################"
    print "###               Finished, summary below                     ###"
    print "#################################################################"
    
    print "\nStart Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
    print "\n"
    
    print " --- CutTable used: %s" % fargs['cutMapper']
    print " --- Cut used: %s" % fargs['cutName']
    print " --- Grouping: %s" % grouping
    print " --- Cut folder: %s%s" % (grouping, fargs['mid1'])
    print " --- Iso folder: %s%s" % (grouping, fargs['mid2'])
    print "\n"
    
    mpResults.sort()
    for item in mpResults :
        print "%5s %10s %5s count %s:" % (item[0], item[1], item[2], item[3])
        print item[4]
        print item[5]
    
    print "Start Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )



def doInitialCuts(grouping, samples, **fargs) :
        
    begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print begin
    channels = fargs[ 'channels' ]
    ''' Start multiprocessing tests '''
    #output = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes= fargs[ 'numCores' ] )
    multiprocessingOutputs = []
    
    num = 0
    for sample in samples :
    
        fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample) )
        for count in range( fileLen ) :
            for channel in channels :
    
                if (channel == 'em') and ('data' in sample) and (sample != 'data_em') : continue
                if (channel == 'et') and ('data' in sample) and (sample != 'data_et') : continue
                if (channel == 'mt') and ('data' in sample) and (sample != 'data_mt') : continue
                if (channel == 'tt') and ('data' in sample) and (sample != 'data_tt') : continue
                print " ====>  Adding %s_%s_%i_%s  <==== " % (grouping, sample, count, channel)
    
                multiprocessingOutputs.append( pool.apply_async(runSVFitCuts, args=(grouping,
                                                                                    sample,
                                                                                    channel,
                                                                                    count,
                                                                                    num,
                                                                                    fargs['bkgs'],
                                                                                    fargs['mid1'],
                                                                                    fargs['cutMapper'],
                                                                                    fargs['cutName'],)) )
                num +=  1
    
    
    mpResults = [p.get() for p in multiprocessingOutputs]
    
    #print(mpResults)
    print "#################################################################"
    print "###               Finished, summary below                     ###"
    print "#################################################################"
    
    print "\nStart Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
    print "\n"
    
    print " --- CutTable used: %s" % fargs['cutMapper']
    print " --- Cut used: %s" % fargs['cutName']
    print " --- Grouping: %s" % grouping
    print " --- Cut folder: %s%s" % (grouping, fargs['mid1'])
    print " --- Iso folder: %s%s" % (grouping, fargs['mid2'])
    print "\n"
    
    mpResults.sort()
    for item in mpResults :
        print "%5s %10s %5s count %s:" % (item[0], item[1], item[2], item[3])
        print item[4]
        print item[5]
    
    print "Start Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )


def doInitialOrder(grouping, samples, **fargs) :
        
    begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print begin
    channels = fargs[ 'channels' ]
    ''' Start multiprocessing tests '''
    #output = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes= fargs[ 'numCores' ] )
    multiprocessingOutputs = []
    
    num = 0
    for sample in samples :
    
        fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample) )
        go = True
        count = 0
        while go :
            for channel in channels :
    
                if (channel == 'em') and ('data' in sample) and (sample != 'data_em') : continue
                if (channel == 'et') and ('data' in sample) and (sample != 'data_et') : continue
                if (channel == 'mt') and ('data' in sample) and (sample != 'data_mt') : continue
                if (channel == 'tt') and ('data' in sample) and (sample != 'data_tt') : continue
                print " ====>  Adding %s_%s_%i_%s  <==== " % (grouping, sample, count, channel)
    
                multiprocessingOutputs.append( pool.apply_async(runIsoOrder, args=(grouping,
                                                                                    sample,
                                                                                    channel,
                                                                                    count,
                                                                                    num,
                                                                                    fargs['bkgs'],
                                                                                    fargs['mid1'],
                                                                                    fargs['mid2'],
                                                                                    fargs['cutMapper'],
                                                                                    fargs['cutName'],
                                                                                    fargs['svf'],
                                                                                    fargs['svfName'],
                                                                                    fargs['numFilesPerCycle'])) )
                num +=  1
    
            count += 1
            
            # Make sure we loop over large samples to get all files
            if count * fargs['numFilesPerCycle'] > fileLen : go = False
    
    
    mpResults = [p.get() for p in multiprocessingOutputs]
    
    #print(mpResults)
    print "#################################################################"
    print "###               Finished, summary below                     ###"
    print "#################################################################"
    
    print "\nStart Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
    print "\n"
    
    print " --- CutTable used: %s" % fargs['cutMapper']
    print " --- Cut used: %s" % fargs['cutName']
    print " --- Grouping: %s" % grouping
    print " --- Cut folder: %s%s" % (grouping, fargs['mid1'])
    print " --- Iso folder: %s%s" % (grouping, fargs['mid2'])
    print "\n"
    
    mpResults.sort()
    for item in mpResults :
        print "%5s %10s %5s count %s:" % (item[0], item[1], item[2], item[3])
        print item[4]
    
    print "Start Time: %s" % str( begin )
    print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )



def drawHistos(grouping, samples, **fargs ) :
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
    }
    channels = fargs['channels']
    ''' Start PROOF multiprocessing Draw '''
    ROOT.TProof.Open('workers=%s' % str( int(fargs['numCores']) ) )
    gROOT.SetBatch(True)
    bkgMap = getBkgMap()
    
    for sample in samples :

        # the gen matching samples are: based off of the DYJets samples
        loopList = []
        if 'DYJets' in sample :
            genList = ['ZTT', 'ZL', 'ZJ', 'ZLL']
            loopList = genList
            loopList.append( sample ) 
        else : loopList.append( sample )
        fileLen = file_len( 'meta/NtupleInputs_%s/%s.txt' % (grouping, sample) )
        print "File len: %5i  File name: meta/NtupleInputs_%s/%s.txt" % (fileLen, grouping, sample)
        numIters = int( math.ceil( fileLen / fargs['numFilesPerCycle'] ) )
        print "Num Iters: %i" % numIters
    
        for subName in loopList :
            print "SubName:",subName
            if subName != sample : saveName = "%s-%s" % (sample.split('_')[0], subName)
            else : saveName = sample.split('_')[0]
            
            for channel in channels :
    
                if (channel == 'em') and ('data' in sample) and (sample != 'data_em') : continue
                if (channel == 'et') and ('data' in sample) and (sample != 'data_et') : continue
                if (channel == 'mt') and ('data' in sample) and (sample != 'data_mt') : continue
                if (channel == 'tt') and ('data' in sample) and (sample != 'data_tt') : continue
                print " ====>  Starting Plots For %s_%s_%s  <==== " % (grouping, saveName, channel)
    
                chain = ROOT.TChain('Ntuple')
                if fargs['bkgs'] != 'None' :
                    outFile = ROOT.TFile('meta/%sBackgrounds/%s/shape/%s_%s.root' % (grouping, bkgMap[ fargs['bkgs'] ][0], sample.split('_')[0], channel), 'RECREATE')
                    for i in range( numIters+1 ) :
                        #print "%s_%i" % ( sample, i)
                        chain.Add('meta/%sBackgrounds/%s/iso/%s_%i_%s.root' % (grouping, bkgMap[ fargs['bkgs'] ][0], sample.split('_')[0], i, channel) )
                else :
                    outFile = ROOT.TFile('%s%s/%s_%s.root' % (grouping, fargs['mid3'], saveName , channel), 'RECREATE')
                    for i in range( numIters+1 ) :
                        #print "%s_%i" % ( sample, i)
                        chain.Add('%s%s/%s_%i_%s.root' % (grouping, fargs['mid2'], sample.split('_')[0], i, channel) )
                print "ENTRIES: %s %i" % (sample, chain.GetEntries() )
                if 'data' in sample : isData = True
                else : isData = False
                additionalCut = fargs['additionalCut']
                if subName != sample : 
                    if genMap[subName][channel] == '' : continue
                    if additionalCut == '' : additionalCut = genMap[subName][channel] 
                    else : additionalCut += genMap[subName][channel] 
                print "AdditionalCuts",additionalCut
                #if fargs['bkgs'] != 'None' : blind = False
                #else : blind = True
                blind = False
                analysisPlots.plotHistosProof( outFile, chain, channel, isData, additionalCut, blind )
                outFile.Close()
         
if __name__ == '__main__' :
    runCutsAndIso('25ns', 'data_em', 'em', 3, 1, 'None', '1nov2newNtups', '2nov2newNtups','signalCuts','PostSync',25)
