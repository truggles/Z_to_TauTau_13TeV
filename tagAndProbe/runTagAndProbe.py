import ROOT
from time import gmtime, strftime
import json
import tagAndProbeLite
import multiprocessing
import ThreeProngTaus.tauHelpers
from array import array
from ROOT import gPad
import subprocess


"""
Main Settings
"""
runs = ['RunD',]



''' timing... '''
begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "\nStart Time: %s" % str( begin )

''' Configs '''
ROOT.gROOT.SetBatch(True)
maxEvents = 999999
numCores = 7

''' Being the selections '''
with open('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt') as jsonFile :
    jsonDict = json.load( jsonFile )
lumiJSON = tauHelpers.buildFullLumiList( jsonDict )
#print lumiJSON

''' Enable multiprocessing '''
pool = multiprocessing.Pool(processes = numCores )
multiprocessingOutputs = []

for run in runs :
    files = open('targetRunSingleMuon%s.txt' % run, 'r' )
    cnt = 0
    for file_ in files :
        targetFile = file_.strip()
        multiprocessingOutputs.append( pool.apply_async(tagAndProbeLite.tagAndProbeAnalyzer, args=( cnt, lumiJSON, targetFile, maxEvents ) ) )
        cnt += 1

mpResults = [p.get() for p in multiprocessingOutputs]

mpResults.sort()
for item in mpResults :
    print item


#for run in runs :
#    subprocess.call( ['bash', 'haddRuns.sh', '%s' % run, '%s' % version] )
#    f = ROOT.TFile('%s_%s/%s.root' % (run, version, run),'r')
#    tree = f.Get('tauEvents/Ntuple')
#    tauHelpers.nvtxTemplate( tree, run, version )
#    #tauHelpers.jetPtTemplate( tree, run )
#
#for run in runs :
#    #puDict = tauHelpers.PUreweightDict( 260627, run )
#    puDict = tauHelpers.PUreweightDict( run, run, version )
#    #jetPtpuDict = tauHelpers.jetPtPUreweightDict( 254833, run )
#    print "\n RUN: %s VERSION %s" % (run, version)
#    #for key in puDict.keys() :
#    #    print key,puDict[ key ]
#    f = ROOT.TFile('%s_%s/%s.root' % (run, version, run),'update')
#    dic = f.Get('tauEvents')
#    tree = dic.Get('Ntuple')
#    PUWeight = array('f', [ 0 ] )
#    PUWeightB = tree.Branch('PUWeight', PUWeight, 'PUWeight/F')
#    #jetPtWeight = array('f', [ 0 ] )
#    #jetPtWeightB = tree.Branch('jetPtWeight', jetPtWeight, 'jetPtWeight/F')
#    for row in tree :
#        PUWeight[0] = puDict[ row.nvtx ]
#        PUWeightB.Fill()
#        #if row.j1Pt < 1000 : jetPtWeight[0] = jetPtpuDict[ int(row.j1Pt/20) ]
#        #else : jetPtWeight[0] = jetPtpuDict[ int(999/20) ]
#        #jetPtWeightB.Fill()
#    dic.cd()
#    tree.Write('', ROOT.TObject.kOverwrite)

    
    


print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )


