import ROOT


def ttreeWithCuts( oldFile, oldTreePath, fOutName='ttreeWithCut.root', cut='' ) :
    f = ROOT.TFile( oldFile, 'r' )
    t = f.Get(oldTreePath)
    print "Num Events in initial TTree:",t.GetEntries()
    
    fOut = ROOT.TFile(fOutName,'RECREATE')
    tOut = t.CopyTree( cut )
    print "Num events in new TTree:",tOut.GetEntries()
    
    fOut.cd()
    tOut.Write()
    fOut.Close()



if __name__ == '__main__' :
    oldFile = 'vbf.root'
    oldTreePath = 'tt/final/Ntuple'
    fOutName = 'vbfCut.root'
    cut = '(evt==1428178)'
    ttreeWithCuts( oldFile, oldTreePath, fOutName, cut )



