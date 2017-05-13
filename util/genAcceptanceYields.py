#
# Quick script to print gen acceptance yields based off of FSA ntuples for
# different Pt thresholds

import ROOT

def getCut( channel, pt1, pt2 ) :
    chnCutMap = {

        # TauTau trigger tau eta < 2.1
        'tt' : 't1ZTTGenMatching == 5 && t2ZTTGenMatching == 5 && abs(t1ZTTGenEta) < 2.1 && abs(t2ZTTGenEta) < 2.1 && t1ZTTGenPt > %i && t2ZTTGenPt > %i' % (pt1, pt2),
        # ETau e eta < 2.1, tau < 2.3
        'et' : 'eZTTGenMatching == 3 && tZTTGenMatching == 5 && abs(eGenEta) < 2.1 && abs(tZTTGenEta) < 2.3 && eGenPt > %i && tZTTGenPt > %i' % (pt1, pt2),
        # MTau m eta < 2.1, tau < 2.3
        'mt' : 'mZTTGenMatching == 4 && tZTTGenMatching == 5 && abs(mGenEta) < 2.1 && abs(tZTTGenEta) < 2.3 && mGenPt > %i && tZTTGenPt > %i' % (pt1, pt2),
    }
    return chnCutMap[channel]

def genAcceptance( sample, channel, pt1Cuts, pt2Cuts ) :

    base = '/nfs_scratch/truggles/2017_May_TauTriggerStudy/'

    print "\n\nGen Acceptance for %s : %s\n" % (sample, channel)

    f = ROOT.TFile(base+sample+'.root','r')
    t = f.Get(channel+'/final/Ntuple')

    h1 = ROOT.TH1F('h1','h1',100,0,10000)
    for pt1 in pt1Cuts :
        for pt2 in  pt2Cuts :
            cut = getCut( channel, pt1, pt2)
            t.Draw("Mass >> h1",cut)
            print "Pt1: %i Pt2: %i   ===>>> Event Yield: %i" % (pt1, pt2, h1.Integral())
    del h1


if __name__ == '__main__' :
#f = ROOT.TFile('ggH125.root','r')
    samples = [
    'ggH125',
    'qqH125',
    #'WH125',
    #'ZH125'
    ]

    channels = [
    'tt',
    #'et',
    #'mt',
    ]



    # TauTau
    pt1Cuts = [30, 35, 40, 45, 50]
    pt2Cuts = [30, 35, 40, 45, 50]
    ## ETau
    #pt1Cuts = [20, 22, 24, 26, 28, 30]
    #pt2Cuts = [20, 23, 26, 29, 32, 35, 38]
    ## MTau
    #pt1Cuts = [18, 20, 22, 24, 26]
    #pt2Cuts = [18, 20, 22, 24, 26, 28]

    for channel in channels :
        for sample in samples :
            genAcceptance( sample, channel, pt1Cuts, pt2Cuts )




