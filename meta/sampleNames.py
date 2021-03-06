
# Place to hold all sample specific information
# June - 2016

# Excellent Source: https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
# See Kenneth's Log Book for how to find this stuff on MCM: https://twiki.cern.ch/twiki/bin/view/Main/KDLLogBook#LogDay20150106
# When in MCM, click "Select View", check "Generator Parameters" and there should be a cross section for one of
# the versions of a given sample
# The scale factor is for LO -> NNLO scaling see excel sheet below https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#MC_samples

from collections import OrderedDict

def returnSampleDetails( analysis, samples=[] ) :
    sampleMap = sampleDetails( analysis )
    #print sampleMap
    returnMap = OrderedDict()
    for sample in samples :
        if sample in sampleMap.keys() :
            returnMap[ sample ] = sampleMap[ sample ]
        else : print "\n\nSample: %s    not in meta/sampleNames.py\n\n" % sample
    return returnMap


def sampleDetails( analysis ) :
    hBR110 = 0.0791
    hBR120 = 0.0698
    hBR125 = 0.0627
    hBR130 = 0.0541
    hBR140 = 0.0360
    
    moriond17 = 'RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6'
    sampleMap = {
        'Sync' : {
            'Sync-SUSY160': {
                'DASPath' : '/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 999.,
                'group' : 'sync'},
             'Sync-VBF125': {
                'DASPath' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 3.782 * hBR125,
                'group' : 'sync'},
            'Sync-DYJets4' :    { 
                'DASPath' : '/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 54.8 * 1.1638,
                'group' : 'dyj'},
            'Sync-data2016RunB' : {
                'DASPath' : '/Tau/Run2016B-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'Sync-data2016RunH' : {
                'DASPath' : '/Tau/Run2016H-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'Sync-data2016All' : {
                'DASPath' : '/Tau/Run2016H-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
        }, # end Sync sample

        'htt' : {
            'dataTT-B' : {
                'DASPath' : '/Tau/Run2016B-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataTT-C' : {
                'DASPath' : '/Tau/Run2016C-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataTT-D' : {
                'DASPath' : '/Tau/Run2016D-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataTT-E' : {
                'DASPath' : '/Tau/Run2016E-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataTT-F' : {
                'DASPath' : '/Tau/Run2016F-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataTT-G' : {
                'DASPath' : '/Tau/Run2016F-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataTT-H' : {
                'DASPath' : '/Tau/Run2016F-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
        }, # end HTT data
        'common' : {
            'EWKWMinus' :   { 
                'DASPath' : '/EWKWMinus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 20.25,
                'group' : 'dib'},
            'EWKWPlus' :    { 
                'DASPath' : '/EWKWPlus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 20.25,
                'group' : 'dib'},
            'EWKZ2l' :      { 
                'DASPath' : '/EWKZ2Jets_ZToLL_M-50_13TeV-madgraph-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 3.987,
                'group' : 'dib'},
            'EWKZ2nu' :     { 
                'DASPath' : '/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 10.01,
                'group' : 'dib'},
            'VV' :         { 
                'DASPath' : '/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 11.95,
                'group' : 'dib'},
            'ZZ2l2q' :     { 
                'DASPath' : '/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 3.22,
                'group' : 'dib'},
            'WW1l1nu2q' :  { 
                'DASPath' : '/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 49.997,
                'group' : 'dib'},
            'WZ2l2q' :     { 
                'DASPath' : '/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 5.595,
                'group' : 'dib'},
            'WZ1l3nu' :    { 
                'DASPath' : '/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 3.05,
                'group' : 'dib'},
            'WZ1l1nu2q' :  { 
                'DASPath' : '/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v3/MINIAODSIM' % moriond17,
                'xsec' : 10.71,
                'group' : 'dib'},
            'Tbar-tW' :    { 
                'DASPath' : '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s_ext1-v1/MINIAODSIM' % moriond17,
                'xsec' : 35.6,
                'group' : 'dib'},
            'T-tW' :       { 
                'DASPath' : '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s_ext1-v1/MINIAODSIM' % moriond17,
                'xsec' : 35.6,
                'group' : 'dib'},
            'T-tchan' :    { 
                'DASPath' : '/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 136.02,
                'group' : 'dib'},
            'Tbar-tchan' : { 
                'DASPath' : '/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 80.95,
                'group' : 'dib'},
            'TT' :         { 
                'DASPath' : '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 831.76,
                'group' : 'top'},
            'ZZ4l' : {
                'DASPath' : '/ZZTo4L_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.256, # See 1.1 k-factor is default, but just added a genMass based
                                # reweighting here util/qqZZ4l_reweight.py
                'group' : 'dib'}, # swappted to 'zz' below for azh analysis
            'WZ3l1nu' : {
                'DASPath' : '/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 4.708, # MCM
                'group' : 'dib'}, # swappted to 'wz' below for azh analysis
            'ZZ4lAMCNLO' : {
                'DASPath' : '/ZZTo4L_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.212 * 1.1, # See 1.1 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ2e2m' : {
                'DASPath' : '/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.00319 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ2e2tau' : {
                'DASPath' : '/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.00319 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ2m2tau' : {
                'DASPath' : '/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.00319 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ4e' : {
                'DASPath' : '/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.00159 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ4m' : {
                'DASPath' : '/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.00159 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ4tau' : {
                'DASPath' : '/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.00159 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ttZ' : {
                'DASPath' : '/ttZJets_13TeV_madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.616,
                'group' : 'rare'},
            'ttZ2' : {
                'DASPath' : '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/%s_ext3-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.616, # FIXME THIS IS WRONG!!! was copied from above inclusive version
                'group' : 'rare'},
        }, # end common
        'azh' : {
            # See H->ZZ samples: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsZZ4l2016#MC
            'dataEE-B' : {
                'DASPath' : '/DoubleEG/Run2016B-03Feb2017_ver2-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-C' : {
                'DASPath' : '/DoubleEG/Run2016C-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-D' : {
                'DASPath' : '/DoubleEG/Run2016D-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-E' : {
                'DASPath' : '/DoubleEG/Run2016E-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-F' : {
                'DASPath' : '/DoubleEG/Run2016F-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-G' : {
                'DASPath' : '/DoubleEG/Run2016G-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-H' : {
                'DASPath' : '/DoubleEG/Run2016H-03Feb2017_ver2-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-B' : {
                'DASPath' : '/DoubleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-C' : {
                'DASPath' : '/DoubleMuon/Run2016C-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-D' : {
                'DASPath' : '/DoubleMuon/Run2016D-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-E' : {
                'DASPath' : '/DoubleMuon/Run2016E-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-F' : {
                'DASPath' : '/DoubleMuon/Run2016F-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-G' : {
                'DASPath' : '/DoubleMuon/Run2016G-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-H' : {
                'DASPath' : '/DoubleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleE-B' : {
                'DASPath' : '/SingleElectron/Run2016B-03Feb2017_ver2-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleE-C' : {
                'DASPath' : '/SingleElectron/Run2016C-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleE-D' : {
                'DASPath' : '/SingleElectron/Run2016D-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleE-E' : {
                'DASPath' : '/SingleElectron/Run2016E-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleE-F' : {
                'DASPath' : '/SingleElectron/Run2016F-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleE-G' : {
                'DASPath' : '/SingleElectron/Run2016G-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleE-H' : {
                'DASPath' : '/SingleElectron/Run2016H-03Feb2017_ver2-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleM-B' : {
                'DASPath' : '/SingleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleM-C' : {
                'DASPath' : '/SingleMuon/Run2016C-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleM-D' : {
                'DASPath' : '/SingleMuon/Run2016D-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleM-E' : {
                'DASPath' : '/SingleMuon/Run2016E-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleM-F' : {
                'DASPath' : '/SingleMuon/Run2016F-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleM-G' : {
                'DASPath' : '/SingleMuon/Run2016G-03Feb2017-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataSingleM-H' : {
                'DASPath' : '/SingleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
        }, # end AZh data
        'WandDYJets' : {
            'WJets' :      { 
                'DASPath' : '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 50380 * 1.221252,
                'group' : 'wjets'},
            'WJets1' :     { 
                'DASPath' : '/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 9644.5 * 1.221252,
                'group' : 'wjets'},
            'WJets2' :     { 
                'DASPath' : '/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 3144.5 * 1.221252,
                'group' : 'wjets'},
            'WJets3' :     { 
                'DASPath' : '/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 954.8 * 1.221252,
                'group' : 'wjets'},
            'WJets4' :     { 
                'DASPath' : '/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 485.6 * 1.221252,
                'group' : 'wjets'},
            'DYJetsAMCNLO' :     { 
                'DASPath' : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % moriond17, 
                'xsec' : 4954.0 * 1.1638,
                'group' : 'dyj'},
            'DYJets' :     { 
                'DASPath' : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s_ext1-v2/MINIAODSIM' % moriond17, 
                'xsec' : 4954.0 * 1.1638,
                'group' : 'dyj'},
            'DYJets1' :    { 
                'DASPath' : '/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1012.5 * 1.1638,
                'group' : 'dyj'},
            'DYJets2' :    { 
                'DASPath' : '/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 332.8 * 1.1638,
                'group' : 'dyj'},
            'DYJets3' :    { 
                'DASPath' : '/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 101.8 * 1.1638,
                'group' : 'dyj'},
            'DYJets4' :    { 
                'DASPath' : '/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 54.8 * 1.1638,
                'group' : 'dyj'},
            'DYJetsHigh' : {
                'DASPath' : '/DYJetsToLL_M-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 6.657 * 1.1638,
                'group' : 'dyj'},
            'DYJetsLow' :  {
                'DASPath' : '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17, 
                'xsec' : 18610. * 1.1638,
                'group' : 'dyj'},
            'DYJets1Low' :  {
                'DASPath' : '/DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17, 
                'xsec' : -999,
                'group' : 'dyj'},
            'DYJets2Low' :  {
                'DASPath' : '/DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % moriond17, 
                'xsec' : -999,
                'group' : 'dyj'},
        }, # end WJets and DYJets
        'TriBoson' : {
            'WWW' :     { 
                'DASPath' : '/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.2086,
                'group' : 'dib'},
            'WWZ' :     { 
                'DASPath' : '/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.1651,
                'group' : 'dib'},
            'WZZ' :     { 
                'DASPath' : '/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.05565,
                'group' : 'dib'},
            'ZZZ' :     { 
                'DASPath' : '/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.01398,
                'group' : 'dib'},
        }, # end triboson
        'DiBoson' : {
            'WW' :     { 
                'DASPath' : '/WW_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.001,
                'group' : 'dib'},
            'WZ' :     { 
                'DASPath' : '/WZ_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.001,
                'group' : 'dib'},
            'ZZ' :     { 
                'DASPath' : '/ZZ_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.001,
                'group' : 'dib'},
        }, # end diiboson
	'SM-Higgs' : { # See Yellow Report 4: https://twiki.cern.ch/twiki/pub/LHCPhysics/LHCHXSWG/Higgs_XSBR_YR4_update.xlsx
            'ggHtoTauTau110': {
               'DASPath' : '/GluGluHToTauTau_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 57.90 * hBR110,
               'group' : 'higgs'},
            'ggHtoTauTau120': {
               'DASPath' : '/GluGluHToTauTau_M120_13TeV_powheg_pythia8/%s_ext1-v1/MINIAODSIM' % moriond17,
               'xsec' : 52.22 * hBR120,
               'group' : 'higgs'},
            'ggHtoTauTau125': {
               'DASPath' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 48.58 * hBR125,
               'group' : 'higgs'},
            'ggHtoTauTau130': {
               'DASPath' : '/GluGluHToTauTau_M130_13TeV_powheg_pythia8/%s_ext1-v1/MINIAODSIM' % moriond17,
               'xsec' : 45.31 * hBR130,
               'group' : 'higgs'},
            'ggHtoTauTau140': {
               'DASPath' : '/GluGluHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 36.00 * hBR140,
               'group' : 'higgs'},

            #'HtoWW2l2nu110' : { # W -> l+nu = 32.57%, 32.57%^2 = 0.1061
            #    'DASPath' : '/GluGluHToWWTo2L2Nu_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 57.90 * 0.1405 * 0.1061,
            #    'group' : 'higgs'},
            #'HtoWW2l2nu120' : {
            #    'DASPath' : '/GluGluHToWWTo2L2Nu_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 52.22 * 0.1405 * 0.1061,
            #    'group' : 'higgs'},
            'HtoWW2l2nu125' : {
                'DASPath' : '/GluGluHToWWTo2L2Nu_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 48.58 * 0.2137 * 0.1061,
                'group' : 'higgs'},
            #'HtoWW2l2nu130' : {
            #    'DASPath' : '/GluGluHToWWTo2L2Nu_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 45.31 * 0.3021 * 0.1061,
            #    'group' : 'higgs'},
            #'HtoWW2l2nu140' : {
            #    'DASPath' : '/GluGluHToWWTo2L2Nu_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 36.00 * 0.3021 * 0.1061,
            #    'group' : 'higgs'},

            'VBFHtoTauTau110': {
               'DASPath' : '/VBFHToTauTau_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 4.434 * hBR110,
               'group' : 'higgs'},
            'VBFHtoTauTau120': {
               'DASPath' : '/VBFHToTauTau_M120_13TeV_powheg_pythia8/%s_ext1-v1/MINIAODSIM' % moriond17,
               'xsec' : 3.935 * hBR120,
               'group' : 'higgs'},
            'VBFHtoTauTau125': {
               'DASPath' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 3.782 * hBR125,
               'group' : 'higgs'},
            'VBFHtoTauTau130': {
               'DASPath' : '/VBFHToTauTau_M130_13TeV_powheg_pythia8/%s_ext1-v1/MINIAODSIM' % moriond17,
               'xsec' : 3.637 * hBR130,
               'group' : 'higgs'},
            'VBFHtoTauTau140': {
               'DASPath' : '/VBFHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 3.492 * hBR140,
               'group' : 'higgs'},

            #'VBFHtoWW2l2nu110': { # W -> l+nu = 32.57%, 32.57%^2 = 0.1061
            #   'DASPath' : '/VBFHToWWTo2L2Nu_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #   'xsec' : 4.434 * 0.1405 * 0.1061,
            #   'group' : 'higgs'},
            #'VBFHtoWW2l2nu120': {
            #   'DASPath' : '/VBFHToWWTo2L2Nu_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #   'xsec' : 4.086 * 0.1405 * 0.1061,
            #   'group' : 'higgs'},
            'VBFHtoWW2l2nu125': {
               'DASPath' : '/VBFHToWWTo2L2Nu_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 3.925 * 0.2137 * 0.1061,
               'group' : 'higgs'},
            #'VBFHtoWW2l2nu130': {
            #   'DASPath' : '/VBFHToWWTo2L2Nu_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #   'xsec' : 3.773 * 0.3021 * 0.1061,
            #   'group' : 'higgs'},
            #'VBFHtoWW2l2nu140': {
            #   'DASPath' : '/VBFHToWWTo2L2Nu_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #   'xsec' : 3.492 * 0.3021 * 0.1061,
            #   'group' : 'higgs'},

            'WPlusHTauTau110' : {
                'DASPath' : '/WplusHToTauTau_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.335 * hBR110,
                'group' : 'higgs'},
            'WPlusHTauTau120' : {
                'DASPath' : '/WplusHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.9558 * hBR120,
                'group' : 'higgs'},
            'WPlusHTauTau125' : {
                'DASPath' : '/WplusHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.8400 * hBR125,
                'group' : 'higgs'},
            'WPlusHTauTau130' : {
                'DASPath' : '/WplusHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.7414 * hBR130,
                'group' : 'higgs'},
            'WPlusHTauTau140' : {
                'DASPath' : '/WplusHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.6308 * hBR140,
                'group' : 'higgs'},

            'WMinusHTauTau110' : {
                'DASPath' : '/WminusHToTauTau_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.8587 * hBR110,
                'group' : 'higgs'},
            'WMinusHTauTau120' : {
                'DASPath' : '/WminusHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.6092 * hBR120,
                'group' : 'higgs'},
            'WMinusHTauTau125' : {
                'DASPath' : '/WminusHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.5328 * hBR125,
                'group' : 'higgs'},
            'WMinusHTauTau130' : {
                'DASPath' : '/WminusHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.4676 * hBR130,
                'group' : 'higgs'},
            'WMinusHTauTau140' : {
                'DASPath' : '/WminusHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.3940 * hBR140,
                'group' : 'higgs'},

            'WPlusHHWW125' : {
                'DASPath' : '/HWplusJ_HToWW_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.8400 * 0.2137,
                'group' : 'higgs'},
            'WMinusHHWW125' : {
                'DASPath' : '/HWminusJ_HToWW_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.5328 * 0.2137,
                'group' : 'higgs'},

            'ZHTauTau110' : {
                'DASPath' : '/ZHToTauTau_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.309 * hBR110,
                'group' : 'higgs'},
            'ZHTauTau120' : {
                'DASPath' : '/ZHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.994 * hBR120,
                'group' : 'higgs'},
            'ZHTauTau125' : {
                'DASPath' : '/ZHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.884 * hBR125,
                'group' : 'higgs'},
            'ZHTauTau130' : {
                'DASPath' : '/ZHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.790 * hBR130,
                'group' : 'higgs'},
            'ZHTauTau140' : {
                'DASPath' : '/ZHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.6514 * hBR140,
                'group' : 'higgs'},

            #'ttHTauTau110' : {
            #    'DASPath' : '/ttHJetToTT_M110_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 0.570 * 0.0704,
            #    'group' : 'higgs'},
            #'ttHTauTau120' : {
            #    'DASPath' : '/ttHJetToTT_M120_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 0.570 * 0.0704,
            #    'group' : 'higgs'},
            'ttHTauTau125' : {
                'DASPath' : '/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/%s_ext4-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.507 * 0.0632,
                'group' : 'higgs'},
            'ttHNonBB125' : {
                'DASPath' : '/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.507 * (1. - 0.5824), # subtract HBB BR
                'group' : 'higgs'},
            'ttHJNonBB125' : {
                'DASPath' : '/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/%s_ext1-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.507 * (1. - 0.5824), # subtract HBB BR
                'group' : 'higgs'},
            #'ttHTauTau130' : {
            #    'DASPath' : '/ttHJetToTT_M130_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 0.454 * 0.0545,
            #    'group' : 'higgs'},
            #'ttHTauTau140' : {
            #    'DASPath' : '/ttHJetToTT_M140_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 0.454 * 0.0545,
            #    'group' : 'higgs'},
            'ZHWW125' : {
                'DASPath' : '/HZJ_HToWW_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.8839 * 0.2137 * 0.3258 * 0.3258, # From Cecile
                'group' : 'higgs'},
            'HZZ125' : {
                'DASPath' : '/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.01212, # From HZZ 2016 twiki
                'group' : 'higgs'},
            #'ggHtoZZ4l' : {
            #    'DASPath' : '/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/RunIISpring16MiniAODv1-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
            #    'xsec' : 0.01212,
            #    'group' : ''}
	} # end SM-Higgs
    } # end sample Map

    # A to Zh sample masses
    for mass in [220, 240, 260, 280, 300, 320, 340, 350, 400] :
        version = '_ext1-v1'
        if mass in [240, 260] : version = '-v1'
        sampleMap['azh']['azh%i' % mass] = {
                'DASPath' : '/AToZhToLLTauTau_M-%i_13TeV_madgraph_4f_LO/%s%s/MINIAODSIM' % (mass, moriond17, version),
                'xsec' : 1.,
                'group' : 'azh'}

    # Adjust some group codes based on analysis
    if analysis == 'azh' :
        sampleMap['common']['ZZ4l']['group'] = 'zz'
        sampleMap['common']['WZ3l1nu']['group'] = 'rare'
        #sampleMap['common']['TT']['group'] = 'rare'
        #sampleMap['WandDYJets']['DYJets']['group'] = 'rare'
        #sampleMap['WandDYJets']['DYJets1']['group'] = 'rare'
        #sampleMap['WandDYJets']['DYJets2']['group'] = 'rare'
        #sampleMap['WandDYJets']['DYJets3']['group'] = 'rare'
        #sampleMap['WandDYJets']['DYJets4']['group'] = 'rare'
        sampleMap['TriBoson']['WWW']['group'] = 'rare'
        sampleMap['TriBoson']['WWZ']['group'] = 'rare'
        sampleMap['TriBoson']['WZZ']['group'] = 'rare'
        sampleMap['TriBoson']['ZZZ']['group'] = 'rare'
        for mass in [110, 120, 125, 130, 140] :
            if 'WMinusHTauTau%i' % mass in sampleMap['SM-Higgs'] : sampleMap['SM-Higgs']['WMinusHTauTau%i' % mass]['group'] = 'higgs'
            if 'WPlusHTauTau%i' % mass in sampleMap['SM-Higgs'] : sampleMap['SM-Higgs']['WPlusHTauTau%i' % mass]['group'] = 'higgs' 
            if 'ZHWW%i' % mass in sampleMap['SM-Higgs'] : sampleMap['SM-Higgs']['ZHWW%i' % mass]['group'] = 'higgs' 
            if 'HZZ%i' % mass in sampleMap['SM-Higgs'] : sampleMap['SM-Higgs']['HZZ%i' % mass]['group'] = 'higgs' 
            

    # Simplify tracking SM-Higgs and add to all returned maps
    for common in sampleMap['common'].keys() :
        sampleMap[analysis][common] = sampleMap['common'][common]
    for smHiggs in sampleMap['SM-Higgs'].keys() :
        sampleMap[analysis][smHiggs] = sampleMap['SM-Higgs'][smHiggs]
    for di in sampleMap['DiBoson'].keys() :
        sampleMap[analysis][di] = sampleMap['DiBoson'][di]
    for tri in sampleMap['TriBoson'].keys() :
        sampleMap[analysis][tri] = sampleMap['TriBoson'][tri]
    for WorDY in sampleMap['WandDYJets'].keys() :
        sampleMap[analysis][WorDY] = sampleMap['WandDYJets'][WorDY]
            
    return sampleMap[ analysis ]




if __name__ == '__main__' :
    samples = ['ggHtoZZ4l', 'DYJets2', 'Sync-HtoTT']
    rtn = returnSampleDetails( 'htt', samples )
    print rtn



