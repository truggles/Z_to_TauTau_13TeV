
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
    c74x = 'RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2'
    c76x = 'RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12'
    c80x = 'RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3'
    c80xReHLT = 'RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14'
    c80xMAOD2 = 'RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0'
    moriond17 = 'RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6'
    sampleMap = {
        'Sync' : {
            'Sync-SUSY160': {
                'DASPath' : '/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 999.,
                'group' : 'sync'},
             'Sync-VBF125': {
                'DASPath' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 3.782 * 0.0627,
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
                'DASPath' : '/ZZTo4L_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 1.256 * 1.1, # See 1.1 k-factor in Devin's HIG-16-036
                'group' : 'dib'},
            'WZ3l1nu' : {
                'DASPath' : '/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 4.708, # MCM
                'group' : 'dib'},
        }, # end HTT
        'azh' : {
            # See H->ZZ samples: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsZZ4l2016#MC
            #'WZ3l1nu' : ('/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/%s-v1/MINIAODSIM' % c80x, 4.666 ),
            #'ZZ4l' :    ('/ZZTo4L_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c80x, 1.212 ),
            'dataEE-B' : {
                'DASPath' : '/DoubleEG/Run2016B-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-C' : {
                'DASPath' : '/DoubleEG/Run2016C-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-D' : {
                'DASPath' : '/DoubleEG/Run2016D-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-E' : {
                'DASPath' : '/DoubleEG/Run2016E-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-F' : {
                'DASPath' : '/DoubleEG/Run2016F-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-G' : {
                'DASPath' : '/DoubleEG/Run2016G-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataEE-H' : {
                'DASPath' : '/DoubleEG/Run2016H-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-B' : {
                'DASPath' : '/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-C' : {
                'DASPath' : '/DoubleMuon/Run2016C-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-D' : {
                'DASPath' : '/DoubleMuon/Run2016D-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-E' : {
                'DASPath' : '/DoubleMuon/Run2016E-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-F' : {
                'DASPath' : '/DoubleMuon/Run2016F-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-G' : {
                'DASPath' : '/DoubleMuon/Run2016G-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM-H' : {
                'DASPath' : '/DoubleMuon/Run2016H-PromptReco-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'ZZ4l' : {
                'DASPath' : '/ZZTo4L_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.256 * 1.1, # See 1.1 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
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
            'WZ3l1nu' : {
                'DASPath' : '/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 4.42965, # Devin's
                'group' : 'wz'},
            'TT' :         { 
                'DASPath' : '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/%s_ext3-v1/MINIAODSIM' % moriond17,
                'xsec' : 831.76,
                'group' : 'top'},
            
            #'TTZ' : {
            #    'DASPath' : '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/%s-v3/MINIAODSIM' % c80x,
            #    'xsec' : 999.,
            #    'group' : ''},
            #'WZ3l1nu' : {
            #    'DASPath' : '/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/%s-v1/MINIAODSIM' % c80x,
            #    'xsec' : 999.,
            #    'group' : ''},
            #'TTTT' : {
            #    'DASPath' : '/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/%s_ext1-v2/MINIAODSIM' % c80x,
            #    'xsec' : 999.,
            #    'group' : ''},
            #'ggZZ4l' : {
            #    'DASPath' : '/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v3/MINIAODSIM',
            #    'xsec' : 999.,
            #    'group' : ''},
            #'ggHtoZZ4l' : {
            #    'DASPath' : '/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/RunIISpring16MiniAODv1-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
            #    'xsec' : 0.01212,
            #    'group' : ''}
        }, # end AtoZh
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
            'ggHtoTauTauNNLOPS125': { # Special NNLOPS new sample, yes the DAS path is wrong, if you want to verify look at the parent sample
               'DASPath' : '/GluGluHToGG_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8/%s-v3/MINIAODSIM' % moriond17,
               'xsec' : 48.58 * 0.0627,
               'group' : 'higgs'},
            'ggHtoTauTau110': {
               'DASPath' : '/GluGluHToTauTau_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 57.90 * 0.0698,
               'group' : 'higgs'},
            'ggHtoTauTau120': {
               'DASPath' : '/GluGluHToTauTau_M120_13TeV_powheg_pythia8/%s_ext1-v1/MINIAODSIM' % moriond17,
               'xsec' : 52.22 * 0.0698,
               'group' : 'higgs'},
            'ggHtoTauTau125': {
               'DASPath' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 48.58 * 0.0627,
               'group' : 'higgs'},
            'ggHtoTauTau130': {
               'DASPath' : '/GluGluHToTauTau_M130_13TeV_powheg_pythia8/%s_ext1-v1/MINIAODSIM' % moriond17,
               'xsec' : 45.31 * 0.0541,
               'group' : 'higgs'},
            'ggHtoTauTau140': {
               'DASPath' : '/GluGluHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 36.00 * 0.0541,
               'group' : 'higgs'},

            #'HtoWW2l2nu110' : { # W -> l+nu = 32.57%, 32.57%^2 = 0.1061
            #    'DASPath' : '/GluGluHToWWTo2L2Nu_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 57.90 * 0.1405 * 0.1061,
            #    'group' : 'VH'},
            #'HtoWW2l2nu120' : {
            #    'DASPath' : '/GluGluHToWWTo2L2Nu_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 52.22 * 0.1405 * 0.1061,
            #    'group' : 'VH'},
            'HtoWW2l2nu125' : {
                'DASPath' : '/GluGluHToWWTo2L2Nu_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 48.58 * 0.2137 * 0.1061,
                'group' : 'VH'},
            #'HtoWW2l2nu130' : {
            #    'DASPath' : '/GluGluHToWWTo2L2Nu_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 45.31 * 0.3021 * 0.1061,
            #    'group' : 'VH'},
            #'HtoWW2l2nu140' : {
            #    'DASPath' : '/GluGluHToWWTo2L2Nu_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 36.00 * 0.3021 * 0.1061,
            #    'group' : 'VH'},

            'VBFHtoTauTau110': {
               'DASPath' : '/VBFHToTauTau_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 4.434 * 0.0698,
               'group' : 'higgs'},
            'VBFHtoTauTau120': {
               'DASPath' : '/VBFHToTauTau_M120_13TeV_powheg_pythia8/%s_ext1-v1/MINIAODSIM' % moriond17,
               'xsec' : 4.086 * 0.0698,
               'group' : 'higgs'},
            'VBFHtoTauTau125': {
               'DASPath' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 3.925 * 0.0627,
               'group' : 'higgs'},
            'VBFHtoTauTau130': {
               'DASPath' : '/VBFHToTauTau_M130_13TeV_powheg_pythia8/%s_ext1-v1/MINIAODSIM' % moriond17,
               'xsec' : 3.773 * 0.0541,
               'group' : 'higgs'},
            'VBFHtoTauTau140': {
               'DASPath' : '/VBFHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
               'xsec' : 3.492 * 0.0541,
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
                'xsec' : 1.565 * 0.0698 * 0.5,
                'group' : 'VH'},
            'WPlusHTauTau120' : {
                'DASPath' : '/WplusHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.565 * 0.0698 * 0.5,
                'group' : 'VH'},
            'WPlusHTauTau125' : {
                'DASPath' : '/WplusHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.373 * 0.0627 * 0.5,
                'group' : 'VH'},
            'WPlusHTauTau130' : {
                'DASPath' : '/WplusHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.209 * 0.0541 * 0.5,
                'group' : 'VH'},
            'WPlusHTauTau140' : {
                'DASPath' : '/WplusHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.209 * 0.0541 * 0.5,
                'group' : 'VH'},

            'WMinusHTauTau110' : {
                'DASPath' : '/WminusHToTauTau_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.565 * 0.0698 * 0.5,
                'group' : 'VH'},
            'WMinusHTauTau120' : {
                'DASPath' : '/WminusHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.565 * 0.0698 * 0.5,
                'group' : 'VH'},
            'WMinusHTauTau125' : {
                'DASPath' : '/WminusHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.373 * 0.0627 * 0.5,
                'group' : 'VH'},
            'WMinusHTauTau130' : {
                'DASPath' : '/WminusHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.209 * 0.0541 * 0.5 ,
                'group' : 'VH'},
            'WMinusHTauTau140' : {
                'DASPath' : '/WminusHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 1.209 * 0.0541 * 0.5 ,
                'group' : 'VH'},

            'ZHTauTau110' : {
                'DASPath' : '/ZHToTauTau_M110_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.994 * 0.0698,
                'group' : 'VH'},
            'ZHTauTau120' : {
                'DASPath' : '/ZHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.994 * 0.0698,
                'group' : 'VH'},
            'ZHTauTau125' : {
                'DASPath' : '/ZHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.884 * 0.0627,
                'group' : 'VH'},
            'ZHTauTau130' : {
                'DASPath' : '/ZHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.790 * 0.0541,
                'group' : 'VH'},
            'ZHTauTau140' : {
                'DASPath' : '/ZHToTauTau_M140_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.790 * 0.0541,
                'group' : 'VH'},

            #'ttHTauTau110' : {
            #    'DASPath' : '/ttHJetToTT_M110_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 0.570 * 0.0704,
            #    'group' : 'VH'},
            #'ttHTauTau120' : {
            #    'DASPath' : '/ttHJetToTT_M120_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 0.570 * 0.0704,
            #    'group' : 'VH'},
            'ttHTauTau125' : {
                'DASPath' : '/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/%s_ext4-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.507 * 0.0632,
                'group' : 'VH'},
            #'ttHTauTau130' : {
            #    'DASPath' : '/ttHJetToTT_M130_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 0.454 * 0.0545,
            #    'group' : 'VH'},
            #'ttHTauTau140' : {
            #    'DASPath' : '/ttHJetToTT_M140_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % moriond17,
            #    'xsec' : 0.454 * 0.0545,
            #    'group' : 'VH'},
            'ZHWW125' : {
                'DASPath' : '/HZJ_HToWW_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % moriond17,
                'xsec' : 0.8839 * 0.2137 * 0.3258 * 0.3258, # From Cecile
                'group' : 'ZHWW'},
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

    # Simplify tracking SM-Higgs and add to all returned maps
    for smHiggs in sampleMap['SM-Higgs'].keys() :
        sampleMap[analysis][smHiggs] = sampleMap['SM-Higgs'][smHiggs]
    for di in sampleMap['DiBoson'].keys() :
        sampleMap[analysis][di] = sampleMap['DiBoson'][di]
    for tri in sampleMap['TriBoson'].keys() :
        sampleMap[analysis][tri] = sampleMap['TriBoson'][tri]
    for WorDY in sampleMap['WandDYJets'].keys() :
        sampleMap[analysis][WorDY] = sampleMap['WandDYJets'][WorDY]
            
    return sampleMap[ analysis ]
    
    #masses = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
    #for mass in masses :
    #    samplesHTT['ggH%i' % mass] = ('/SUSYGluGluToHToTauTau_M-%i_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % (mass, c80x), 1 )
    #    samplesHTT['bbH%i' % mass] = ('/SUSYGluGluToBBHToTauTau_M-%i_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % (mass, c80x), 1 )
    #samplesHTT['bbH200'] = ('/SUSYGluGluToBBHToTauTau_M-200_TuneCUETP8M1_13TeV-pythia8/%s-v4/MINIAODSIM' % c80x, 1 )
    #samplesHTT['bbH2300'] = ('/SUSYGluGluToBBHToTauTau_M-2300_TuneCUETP8M1_13TeV-pythia8/%s-v4/MINIAODSIM' % c80x, 1 )
    #samplesHTT['ggH250'] = ('/SUSYGluGluToHToTauTau_M-250_TuneCUETP8M1_13TeV-pythia8/%s-v2/MINIAODSIM' % c80x, 1 )
    #samplesHTT['ggH300'] = ('/SUSYGluGluToHToTauTau_M-300_TuneCUETP8M1_13TeV-pythia8/%s-v2/MINIAODSIM' % c80x, 1 )
    #samplesHTT['ggH400'] = ('/SUSYGluGluToHToTauTau_M-400_TuneCUETP8M1_13TeV-pythia8/%s-v3/MINIAODSIM' % c80x, 1 )





if __name__ == '__main__' :
    samples = ['ggHtoZZ4l', 'DYJets2', 'Sync-HtoTT']
    rtn = returnSampleDetails( 'htt', samples )
    print rtn



