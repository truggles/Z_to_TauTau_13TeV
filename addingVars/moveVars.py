import ROOT
import os, glob
from collections import OrderedDict
from array import array
#import json
#import subprocess


def getFileList( dirName, sampName ) :
    assert( os.path.exists( dirName ) ), "ERROR: directory doesn't exist"
    files = glob.glob(dirName+'/'+sampName)
    return files

# creates an initial map of the vars of
# interest connected with a unique ID
# including lepton pt
# Note: to save space, we round the
# vars of interest to 6 decimal places

def mapInitialVars( files, treeName, vars, cut="" ) :
    eventMap = {}
    count = 0
    for file in files :
        fileEventMap = {}
        f = ROOT.TFile( file, 'r' )
        tInitial = f.Get( treeName )
        #print tInitial
        count += 1
        print "File:",count,"Length of initial TTree:",tInitial.GetEntries()

        # Make a cut so we don't deal with insane quantities of events
        t = tInitial.CopyTree( cut )
        print "Length of post-cut TTree:",t.GetEntries()

        for var in vars :
            #print var, vars[var]
            assert( hasattr( t, var ) ), "Proposed var: %s not in TTree" % var
        for row in t :
            # Removed Run because we're working on MC
            evnIDTup = (row.lumi, row.evt, round(row.t1Pt,6), round(row.t2Pt,6))
            #print evnIDTup
            varList = []
            for var in vars :
                # rounding happens here, remove if not desired
                varList.append( round( getattr( row, var ), 6) )

            # This portion is a waste of time if we have unique inputs
            # it simply shows if we have some duplicates that will
            # lead to improper mapping
            if evnIDTup in fileEventMap :
                print "Item already in input map!",evnIDTup

            fileEventMap[ evnIDTup ] = varList
        #for i, item in enumerate(fileEventMap) :
        #    print i,item,fileEventMap[item]

        f.Close()

        for var, key in fileEventMap.iteritems() :
            eventMap[var] = key

    print "Length of final map:",len(eventMap)

    # Save the mapping
    varNaming = ''
    for var in vars :
        varNaming += var
    with open(varNaming+'.txt', 'w') as outFile :
        for key, val in eventMap.iteritems() :
            outFile.write( repr(key)+':'+repr(val)+'\n' )
        outFile.close()

    # Also return the eventMap in case that is prefered
    return eventMap




def mapToNewTree( files, treeName, varMap, evtMap ) :
    newBranches = {}
    newVals = {}
    matched = 0
    totalEvents = 0
    for file in files :
        f = ROOT.TFile( file, 'UPDATE' )
        #print "Updating file",f
        t = f.Get( treeName )
        totalEvents += t.GetEntries()
        print "Events: %10i in file: %s" % (t.GetEntries(), f.GetName())
        #print t
        for key, val in varMap.iteritems() :
            var = val[0]
            # newVals [ new var name ] = [ val ]
            newVals[var] = array('f', [ 0 ] )
            # newBranches [ new var name ] = [ branch ]
            #print var, newVals[var]
            newBranches[var] = [ t.Branch(var, newVals[var], var+'/F') ]
            #print newBranches[var]

        for row in t :   
            # Removed Run because we're working on MC
            evnIDTup = (row.lumi, row.evt, round(row.t1Pt,6), round(row.t2Pt,6))
            #print evnIDTup

            # See if key exists and save value
            if evnIDTup not in evtMap.keys() :
                print evnIDTup, " not in the initial files, will fill with default values"
                print "Iso1",row.t1ByIsolationMVArun2v1DBoldDMwLTraw
                print "Iso2",row.t2ByIsolationMVArun2v1DBoldDMwLTraw
                for key, val in varMap.iteritems() :
                    var = val[0]
                    newVals[var][0] = -1
                
            
            else : # we have a match!
                matched += 1
                #print evnIDTup, " IN initial files"
                toMap = evtMap[ evnIDTup ]
                cnt = 0
                for key, val in varMap.iteritems() :
                    #print val[0], toMap[cnt]
                    newVals[ val[0] ][0] = toMap[cnt]
                    #print newBranches[ val[0] ][0]
                    newBranches[ val[0] ][0].Fill()
                    cnt += 1

        # Overwrite tree with new values
        f.cd()
        t.Write('', ROOT.TObject.kOverwrite)
        f.Close()

    print "Total number of events in out sample:",totalEvents
    print "Number of events matched:",matched


if '__main__' in __name__ :
    #dName = '/cms/truggles/ZTT/CMSSW_8_0_13/src/Z_to_TauTau_13TeV/addingVars'
    ##sampName = 'make_ntuples_cfg-00090D4B-AFC1-E511-B88B-001E673986B5' # No .root on the end
    #sampName = 'make_ntuples_cfg-00*' # No .root on the end
    dName = '/hdfs/store/user/truggles/oct30_2015ZTT76x/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
    #sampName = 'make_ntuples_cfg-00090D4B-AFC1-E511-B88B-001E673986B5' # No .root on the end
    sampName = 'make_ntuples_cfg-*.root'
    treeName = 'tt/final/Ntuple'
    files = getFileList( dName, sampName )

    # old var name, new var name (can be same as old var name)
    # need to keep this in order so when we retrieve that vals
    # they are correct
    varMap = OrderedDict()
    #varMap['topQuarkPt1'] = 'topQuarkPt1_v5',
    #varMap['topQuarkPt2'] = 'topQuarkPt2_v5',
    varMap['genEta'] = 'genEta_v3',
    varMap['genpT'] = 'genpT_v3',
    varMap['genM'] = 'genM_v3',
    varMap['genMass'] = 'genMass_v3',
    tmpCut = '(t1Pt > 38 && t2Pt > 38 && t1AbsEta < 2.1 && t2AbsEta < 2.1 && t1_t2_DR > 0.5 && abs( t1PVDZ ) < 0.2 && abs( t2PVDZ ) < 0.2 && abs( t1Charge ) == 1 && abs( t2Charge ) == 1 && t1ByIsolationMVArun2v1DBoldDMwLTraw > -0.4 && t2ByIsolationMVArun2v1DBoldDMwLTraw > -0.4 && eVetoZTTp001dxyzR0 == 0 && muVetoZTTp001dxyzR0 == 0 && t1AgainstElectronVLooseMVA6 > 0.5 && t1AgainstMuonLoose3 > 0.5 && t2AgainstElectronVLooseMVA6 > 0.5 && t2AgainstMuonLoose3 > 0.5 && t1DecayModeFinding == 1 && t2DecayModeFinding == 1)'
    #tmpCut = ""
    evtMap = mapInitialVars( files, treeName, varMap, tmpCut )

    # Add vars to other files
    newDir = '/cms/truggles/ZTT/CMSSW_8_0_13/src/Z_to_TauTau_13TeV/addingVars'
    newSample = 'TauTau_13_Recoil2_TESType1_isWJ0_metSyst1-DYJets4_*_tt.root'
    newFiles = getFileList( newDir, newSample )
    print newFiles

    newTreeName = 'tt/Ntuple'
    mapToNewTree( newFiles, newTreeName, varMap, evtMap )






