import ROOT
from time import gmtime, strftime
import json
import tauAnalyzer
import multiprocessing
import tauHelpers
from array import array
from ROOT import gPad

''' timing... '''
begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "\nStart Time: %s" % str( begin )

''' Configs '''
ROOT.gROOT.SetBatch(True)
maxEvents = 999999
numCores = 25

''' Being the selections '''
#with open('targetRunsJSON.txt') as jsonFile :
#    jsonDict = json.load( jsonFile )
#runAndLumis = tauHelpers.buildFullLumiList( jsonDict )
#
## Enable multiprocessing
#pool = multiprocessing.Pool(processes = numCores )
#multiprocessingOutputs = []
#
#for run in runAndLumis.keys() :
#    files = open('targetRun%i.txt' % run, 'r' )
#    cnt = 0
#    for file_ in files :
#        targetFile = file_.strip()
#        #tauAnalyzer.tauAnalyzer( cnt, run, runAndLumis[ run ], targetFile, maxEvents )
#        multiprocessingOutputs.append( pool.apply_async(tauAnalyzer.tauAnalyzer, args=( cnt, run, runAndLumis[ run ], targetFile, maxEvents ) ) )
#        cnt += 1
#
#mpResults = [p.get() for p in multiprocessingOutputs]
#
#mpResults.sort()
#for item in mpResults :
#    print item



runs = [254790, 254833, 258425, 259721]
for run in runs :
    f = ROOT.TFile('%i/%i.root' % (run, run),'r')
    tree = f.Get('tauEvents/Ntuple')
    tauHelpers.nvtxTemplate( tree, run )

for run in runs :
    puDict = tauHelpers.PUreweightDict( 258425, run )
    print "\n RUN: %i" % run
    #for key in puDict.keys() :
    #    print key,puDict[ key ]
    f = ROOT.TFile('%i/%i.root' % (run, run),'update')
    dic = f.Get('tauEvents')
    tree = dic.Get('Ntuple')
    PUWeight = array('f', [ 0 ] )
    PUWeightB = tree.Branch('PUWeight', PUWeight, 'PUWeight/F')
    for row in tree :
        PUWeight[0] = puDict[ row.nvtx ]
        PUWeightB.Fill()
    dic.cd()
    tree.Write('', ROOT.TObject.kOverwrite)

#for run in runs :
#    f = ROOT.TFile('%i/%i.root' % (run, run),'r')
#    tree = f.Get('tauEvents/Ntuple')
#    hist = ROOT.TH1F('reweight', 'nvtxReweighted', 60, 0, 60)
#    tree.Draw('nvtx>>reweight', 'PUWeight')
#    hist = gPad.GetPrimitive( 'reweight')
#    c1 = ROOT.TCanvas('c1','c1',600,600)
#    p1 = ROOT.TPad('p1','p1',0,0,1,1)
#    p1.Draw()
#    p1.cd()
#    hist.Draw()
#    c1.SaveAs('/afs/cern.ch/user/t/truggles/www/threeProngs/%s_nvtx.png' % run)
    
    


print "\nStart Time: %s" % str( begin )
print "End Time:   %s" % str( strftime("%Y-%m-%d %H:%M:%S", gmtime()) )


