import ROOT
from ROOT import gPad
import glob
from util.buildTChain import makeTChainFromGlob


ROOT.gROOT.SetBatch(True)

def getEff( sample, channel, folder1, folder2 ) :
    #print sample
    weights = '*(trigweight_1 * idisoweight_1 * idisoweight_2 * puweight)'
    files1 = glob.glob('%s/%s_*_%s.root' % (folder1, sample, channel) )
    path = 'Ntuple'
    chain = makeTChainFromGlob( files1, path )
    #print "File1: %i entries" % chain.GetEntries()
    h1 = ROOT.TH1F('h1','h1',100,-10,10)
    h2 = ROOT.TH1F('h2','h2',100,-10,10)
    chain.Draw('Eta>>h1', '(weight/abs( weight ))')
    h1 = gPad.GetPrimitive( 'h1' )
    looseRaw = h1.Integral()
    chain.Draw('Eta>>h2', '(weight/abs( weight ))%s' % weights )
    h2 = gPad.GetPrimitive( 'h2' )
    looseWeight = h2.Integral()
    files2 = glob.glob('%s/%s_*_%s.root' % (folder2, sample, channel) )
    chain2 = makeTChainFromGlob( files2, path )
    #print "File2: %i entries" % chain2.GetEntries()
    h3 = ROOT.TH1F('h3','h3',100,-10,10)
    h4 = ROOT.TH1F('h4','h4',100,-10,10)
    chain2.Draw('Eta>>h3', '(Z_SS == 0)*(weight/abs( weight ))')
    h3 = gPad.GetPrimitive( 'h3' )
    tightRaw = h3.Integral()
    chain2.Draw('Eta>>h4', '(Z_SS == 0)*(weight/abs( weight ))%s' % weights )
    h4 = gPad.GetPrimitive( 'h4' )
    tightWeight = h4.Integral()
    print "%15s    Channel:%s   RawL    %f  RawT    %f   Percent %f" % ( sample, channel, looseRaw, tightRaw, tightRaw/looseRaw )
    print "%15s    Channel:%s   Weightl %f  WeightT %f   Percent %f" % ( sample, channel, looseWeight, tightWeight, tightWeight/looseWeight )
    








if __name__ == '__main__' :
    folder1 = 'dataCards2Feb26b'
    folder2 = 'dataCards2Feb25a'
    channels = ['em','tt'] 
                # sample : normalized summed weight of events processed   
    samples = {'DYJets' : 9004328,
             'DYJets1' : 65314144,
             'DYJets2' : 19980779,
             'DYJets3' : 5701878,
             'DYJets4': 4189017,
             'DYJetsLow' : 22482567,
             'DYJetsFXFX' : 19259718,
    }
    for sample in samples.keys() :
        #if sample != 'DYJets' or sample!= 'DYJets1' : continue
        #genSamps = []
        #genSamps.append( sample )
        #for gen in ['-ZL', '-ZLL', '-ZJ'] :
        #    genSamps.append( sample+gen )
        #for fullName in genSamps :
        #print sample
        for channel in channels :
            print channel
            getEff( sample, channel, folder1, folder2 )








