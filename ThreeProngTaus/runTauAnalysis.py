import ROOT
from time import gmtime, strftime
import json
import tauAnalyzer
import multiprocessing
import tauHelpers
from array import array
from ROOT import gPad
import subprocess


"""
Main Settings
"""
runs = [256677, 260627,]#[254790, 254833, 258425, 259721]
versions = ['80X_RelVal',]#'76X']



''' timing... '''
begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "\nStart Time: %s" % str( begin )

''' Configs '''
ROOT.gROOT.SetBatch(True)
maxEvents = 999999
numCores = 25

''' Being the selections '''
with open('targetRunsJSON.txt') as jsonFile :
    jsonDict = json.load( jsonFile )
runAndLumis = tauHelpers.buildFullLumiList( jsonDict )

''' Enable multiprocessing '''
pool = multiprocessing.Pool(processes = numCores )
multiprocessingOutputs = []

for run in runAndLumis.keys() :
    for version in versions:
        files = open('targetRun%s_%s.txt' % (run,version), 'r' )
        cnt = 0
        for file_ in files :
            targetFile = file_.strip()
            multiprocessingOutputs.append( pool.apply_async(tauAnalyzer.tauAnalyzer, args=( cnt, run, runAndLumis[ run ], targetFile, maxEvents, version ) ) )
            cnt += 1

mpResults = [p.get() for p in multiprocessingOutputs]

mpResults.sort()
for item in mpResults :
    print item


for run in runs :
    for version in versions:
        subprocess.call( ['bash', 'haddRuns.sh', '%s' % run, '%s' % version] )
        f = ROOT.TFile('%s_%s/%s.root' % (run, version, run),'r')
        tree = f.Get('tauEvents/Ntuple')
        tauHelpers.nvtxTemplate( tree, run, version )
        #tauHelpers.jetPtTemplate( tree, run )

for run in runs :
    for version in versions:
        #puDict = tauHelpers.PUreweightDict( 260627, run )
        puDict = tauHelpers.PUreweightDict( run, run, version )
        #jetPtpuDict = tauHelpers.jetPtPUreweightDict( 254833, run )
        print "\n RUN: %s VERSION %s" % (run, version)
        #for key in puDict.keys() :
        #    print key,puDict[ key ]
        f = ROOT.TFile('%s_%s/%s.root' % (run, version, run),'update')
        dic = f.Get('tauEvents')
        tree = dic.Get('Ntuple')
        PUWeight = array('f', [ 0 ] )
        PUWeightB = tree.Branch('PUWeight', PUWeight, 'PUWeight/F')
        #jetPtWeight = array('f', [ 0 ] )
        #jetPtWeightB = tree.Branch('jetPtWeight', jetPtWeight, 'jetPtWeight/F')
        for row in tree :
            PUWeight[0] = puDict[ row.nvtx ]
            PUWeightB.Fill()
            #if row.j1Pt < 1000 : jetPtWeight[0] = jetPtpuDict[ int(row.j1Pt/20) ]
            #else : jetPtWeight[0] = jetPtpuDict[ int(999/20) ]
            #jetPtWeightB.Fill()
        dic.cd()
        tree.Write('', ROOT.TObject.kOverwrite)

    
    


print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )


