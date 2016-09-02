#####################################################
### Quick stuff for grabbing and comparing TTrees ###
#####################################################


import ROOT


def getListOfVar( fName, ttree, var ) :
    f1 = ROOT.TFile(fName,'r')
    t1 = f1.Get(ttree)
    
    inTree = set()
    for row in t1 :
        if hasattr( row, var ) :
            inTree.add( getattr( row, var ) )
    return inTree

def getLumiAndRunForEvt( fName, ttree, evt, evtVar='evt' ) :
    f1 = ROOT.TFile(fName,'r')
    t1 = f1.Get(ttree)
    
    for row in t1 :
        if hasattr( row, evtVar ) :
            if getattr( row, evtVar) == evt :
                print "Run",row.run
                print "Lumi",row.lumi
                print "For Evt",evt
    
def makeNewTreeWithCuts( fName, tName, fOut, tOut, cut ) :
    f1 = ROOT.TFile(fName,'r')
    t1 = f1.Get(tName)
    print "In Tree # entries: ", t1.GetEntries()

    outFile = ROOT.TFile(fOut,'RECREATE')
    outTree = t1.CopyTree( cut )
    outTree.SetName(tOut)
    print "Out Tree # entries: ", outTree.GetEntries()

    outFile.cd()

    outTree.Write()
    outFile.Close()

if __name__ == '__main__' :
    n1 = 'emmt_basic.root'
    t1 = 'Ntuple'
    var = 'evt'
    s1 = getListOfVar( n1, t1, var )
    s2 = getListOfVar( 'azh300_mmet.root', t1, var )


    print "S1 dir S2"
    print s1.difference( s2 )
    print "S2 dir S1"
    print s2.difference( s1 )


    s3 = s1.difference( s2 )
    targetEvt = 0
    for i in s3 :
        targetEvt = i
    print targetEvt

    getLumiAndRunForEvt( n1, t1, targetEvt )
   
    makeNewTreeWithCuts( 'azh300FSA.root', 'emmt/final/Ntuple', 'tmp.root', t1, 'evt == 3460' ) 
