import ROOT
from ROOT import gPad
import glob
from util.buildTChain import makeTChainFromGlob


ROOT.gROOT.SetBatch(True)

def getEff( sample, channel, folder ) :
    print sample
    weights = '*(trigweight_1 * idisoweight_1 * idisoweight_2 * puweight)'
    files = glob.glob('%s/%s_*_%s.root' % (folder, sample, channel) )
    #print files
    path = 'Ntuple'
    chain = makeTChainFromGlob( files, path )
    h1 = ROOT.TH1F('h1','h1',100,-10,10)
    h2 = ROOT.TH1F('h2','h2',100,-10,10)
    chain.Draw('Eta>>h1', '(Z_SS == 0)*(weight/abs( weight ))')
    h1 = gPad.GetPrimitive( 'h1' )
    chain.Draw('Eta>>h2', '(Z_SS == 0)*(weight/abs( weight ))%s' % weights )
    h2 = gPad.GetPrimitive( 'h2' )
    print "%15s    Channel:%s   Raw Count %f" % ( sample, channel, h1.Integral() )
    print "%15s    Channel:%s   Weight Count %f" % ( sample, channel, h2.Integral() )
    #h1.SaveAs('tmp_%s.root' % channel )
    








if __name__ == '__main__' :
    folder = 'dataCards2Feb24b'
    channels = ['em','tt']    
    samples = ['DYJets',]# 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsLow', 'DYJetsFXFX']
    for sample in samples :
        genSamps = []
        genSamps.append( sample )
        for gen in ['-ZL', '-ZLL', '-ZJ'] :
            genSamps.append( sample+gen )
        for fullName in genSamps :
            for channel in channels :
                getEff( fullName, channel, folder )








