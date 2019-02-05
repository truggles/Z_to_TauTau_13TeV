import ROOT
ROOT.gROOT.SetBatch(True)
from collections import OrderedDict


def get_yield( process, mass, tree, nBJets, nElectrons, nMuons ) :
    th_name = 'mA%s_nBjets%i_nElec%i_nMuon%i' % (mass, nBJets, nElectrons, nMuons)
    h = ROOT.TH1F( th_name, th_name, 10, 0, 10 )

    # Plot something that will all be easily contained like isMC in [0,10]
    var = 'isMC'
    cut = '(nBJets == %i && nElectrons == %i && nMuons == %i)' % (nBJets, nElectrons, nMuons)
    tree.Draw( '%s >> %s' % (var, th_name), cut )

    return h.Integral()




masses = ['225', '250', '275', '300', '325', '350', '400']

path = '/data/truggles/AZH_2016_llbb_samples/'
path_ggA = '/afs/cern.ch/work/a/aioannou/public/AZh_ggA_Ntuples/'
path_bbA = '/afs/cern.ch/work/a/aioannou/public/AZh_bbA_Ntuples/'

acceptance_dict = OrderedDict()
for nBJets in [0, 1, 2, 3] :
    for nElectrons in [0, 1, 2, 3, 4] :
        for nMuons in [0, 1, 2, 3, 4] :
            category = "nBJets=%i nElectrons=%i nMuons=%i" % (nBJets, nElectrons, nMuons)
            acceptance_dict[ category ] = OrderedDict()

for mass in masses :
    f_ggA = ROOT.TFile( path_ggA+'GluGluToAToZhToLLBB_M%s.root' % mass, 'READ' )
    t_ggA = f_ggA.Get('tree')
    f_bbA = ROOT.TFile( path_bbA+'BBAToZhToLLBB_M%s.root' % mass, 'READ' )
    t_bbA = f_bbA.Get('tree')
    
    for nBJets in [0, 1, 2, 3] :
        # FIXME
        # Many of these nElectron and nMuon combinations are unreasonable and have
        # zero yield.  One could filter them out, or only do the ones we care
        # about...
        for nElectrons in [0, 1, 2, 3, 4] :
            for nMuons in [0, 1, 2, 3, 4] :

                category = "nBJets=%i nElectrons=%i nMuons=%i" % (nBJets, nElectrons, nMuons)

                yield_ggA = get_yield( 'ggA', mass, t_ggA, nBJets, nElectrons, nMuons )
                yield_bbA = get_yield( 'bbA', mass, t_bbA, nBJets, nElectrons, nMuons )

                # FIXME
                # Should record acceptance instead of yield, can divide by DAS # of total events.
                # Is this the same for all samples?

                val = -1.
                if yield_ggA > 0. and yield_bbA > 0. : # FIXME just to make print out simpler, this ignores
                    ## super low contribution categories we don't care about comparing against
                    #print "%10s Mass=%s nBJets=%i nElectrons=%i nMuons=%i Yield=%.2f" % (process, mass, nBJets, nElectrons, nMuons, h.Integral() )
                    print "Mass=%s nBJets=%i nElectrons=%i nMuons=%i bbA/ggA=%.2f" % (mass, nBJets, nElectrons, nMuons, yield_bbA/yield_ggA )
                    val = yield_bbA/yield_ggA
                acceptance_dict[ category ][ mass ] = val

for category in acceptance_dict.keys() :
    print category
    for mass, val in acceptance_dict[ category ].iteritems() :
        if val == -1. : continue
        print " - mass=%s  bbA/ggA=%.2f" % (mass, val)



