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
samples = {
    #'ttbar_2017_pu35' : {
    #    'targetFile' : '2017TrackerScripts/ttbar_2017_pu35_PAT.root',
    #    'version' : 'PAT'},
    #'ttbar_2017_pu50' : {
    #    'targetFile' : '2017TrackerScripts/ttbar_2017_pu50_PAT.root',
    #    'version' : 'PAT'},
    #'ttbar_2017_pu70' : {
    #    'targetFile' : '2017TrackerScripts/ttbar_2017_pu70_PAT.root',
    #    'version' : 'PAT'},
    'ttbar_800' : {
        'targetFile' : '2017TrackerScripts/ttbar_800_PAT.root',
        'version' : 'PAT'},
    'ttbar_800_pu25' : {
        'targetFile' : '2017TrackerScripts/ttbar_800_pu25_PAT.root',
        'version' : 'PAT'},
    'ttbar_2017_800' : {
        'targetFile' : '2017TrackerScripts/ttbar_2017_800_PAT.root',
        'version' : 'PAT'},
    'ttbar_2017_800_pu25' : {
        'targetFile' : '2017TrackerScripts/ttbar_2017_800_pu25_PAT.root',
        'version' : 'PAT'}
    }


''' timing... '''
begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "\nStart Time: %s" % str( begin )

''' Configs '''
ROOT.gROOT.SetBatch(True)
maxEvents = 999999

for sample in samples.keys() :
    cnt = 0
    targetLumis = [0,]
    doLumi = False
    localFile = True
    includeTrigger = False
    tauAnalyzer.tauAnalyzer( cnt, 999, targetLumis, samples[sample]['targetFile'], maxEvents, sample, doLumi, localFile, includeTrigger )
    

''' Enable multiprocessing '''

#for run in runs :
#    for version in versions:
#        subprocess.call( ['bash', 'haddRuns.sh', '%s' % run, '%s' % version] )
#        f = ROOT.TFile('%s_%s/%s.root' % (run, version, run),'r')
#        tree = f.Get('tauEvents/Ntuple')
#        tauHelpers.nvtxTemplate( tree, run, version )
#        #tauHelpers.jetPtTemplate( tree, run )
#
#for run in runs :
#    for version in versions:
#        #puDict = tauHelpers.PUreweightDict( 260627, run )
#        puDict = tauHelpers.PUreweightDict( run, run, version )
#        #jetPtpuDict = tauHelpers.jetPtPUreweightDict( 254833, run )
#        print "\n RUN: %s VERSION %s" % (run, version)
#        #for key in puDict.keys() :
#        #    print key,puDict[ key ]
#        f = ROOT.TFile('%s_%s/%s.root' % (run, version, run),'update')
#        dic = f.Get('tauEvents')
#        tree = dic.Get('Ntuple')
#        PUWeight = array('f', [ 0 ] )
#        PUWeightB = tree.Branch('PUWeight', PUWeight, 'PUWeight/F')
#        #jetPtWeight = array('f', [ 0 ] )
#        #jetPtWeightB = tree.Branch('jetPtWeight', jetPtWeight, 'jetPtWeight/F')
#        for row in tree :
#            PUWeight[0] = puDict[ row.nvtx ]
#            PUWeightB.Fill()
#            #if row.j1Pt < 1000 : jetPtWeight[0] = jetPtpuDict[ int(row.j1Pt/20) ]
#            #else : jetPtWeight[0] = jetPtpuDict[ int(999/20) ]
#            #jetPtWeightB.Fill()
#        dic.cd()
#        tree.Write('', ROOT.TObject.kOverwrite)

    
    


print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )


