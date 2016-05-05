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
    


print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )


