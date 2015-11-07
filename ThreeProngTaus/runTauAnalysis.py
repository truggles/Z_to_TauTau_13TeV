
from time import gmtime, strftime
import json
import tauAnalyzer
import multiprocessing

begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "\nStart Time: %s" % str( begin )
with open('targetRunsJSON.txt') as jsonFile :
    jsonDict = json.load( jsonFile )

# function to mae a dict to hold run vs its good lumiBlocks
def buildFullLumiList( jsonDict ) :
    expandedLumis = {}
    for targetRun in jsonDict.keys() :
        print targetRun
        lumis = []
        for i in range( 0, len(jsonDict[ targetRun ]) ) :
            first = jsonDict[ targetRun ][i][0]
            last = jsonDict[ targetRun ][i][1]
            for j in range( first, last + 1 ) :
                lumis.append( j )
            #print lumis
        expandedLumis[ int(targetRun) ] = lumis
    return expandedLumis

runAndLumis = buildFullLumiList( jsonDict )
maxEvents = 999999
numCores = 10

pool = multiprocessing.Pool(processes = numCores )
multiprocessingOutputs = []


for run in runAndLumis.keys() :
    files = open('targetRun%i.txt' % run, 'r' )
    cnt = 0
    for file_ in files :
        targetFile = file_.strip()
        #tauAnalyzer.tauAnalyzer( cnt, run, runAndLumis[ run ], targetFile, maxEvents )
        multiprocessingOutputs.append( pool.apply_async(tauAnalyzer.tauAnalyzer, args=( cnt, run, runAndLumis[ run ], targetFile, maxEvents ) ) )
        cnt += 1


mpResults = [p.get() for p in multiprocessingOutputs]

mpResults.sort()
for item in mpResults :
    print item

print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
