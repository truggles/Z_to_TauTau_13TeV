import ROOT


channels =  ['eeet','eett','eemt','eeem','emmt','mmtt','mmmt','emmm']
ee_channels =  ['eeet','eett','eemt','eeem']
mm_channels =  ['emmt','mmtt','mmmt','emmm']

c = ROOT.TCanvas('c','c',400,400)
p = ROOT.TPad('p','p',0,0,1,1)
p.Draw()
p.cd()

eeCuts = {
    'BothLow' : 'pt_1 < 32 && pt_2 < 32',
    'LeadingHigh' : 'pt_1 >= 32 && pt_2 < 32',
    'BothHigh' : 'pt_1 >= 32 && pt_2 >= 32',
}
mmCuts = {
    'BothLow' : 'pt_1 < 27 && pt_2 < 27',
    'LeadingHigh' : 'pt_1 >= 27 && pt_2 < 27',
    'BothHigh' : 'pt_1 >= 27 && pt_2 >= 27',
}

for channel in ee_channels :
    f = ROOT.TFile('/data/truggles/tmp/ZZ_%s.root' % channel, 'r')

    t = f.Get('Ntuple')
    print "Channel: %s   nEntries: %i" % (channel, t.GetEntries() )

    #for var in ['zhTrigDataEff', 'zhTrigMCEff', 'zhTrigWeight'] :
    for cutName, cut in eeCuts.iteritems() :
        h1 = ROOT.TH1D('h1', 'h1', 200, -10, 10)
        t.Draw('eta_1 >> h1', cut)
        print "%s   Integral:  %f" % (cutName, h1.Integral() )
        #print "%s   Integral:  %.4f" % (var, h1.Integral() )
        #print "%s   Mean:  %.4f" % (var, h1.GetMean() )
        #print "%s   StdDev:  %.4f" % (var, h1.GetStdDev() )
        del h1
