
# Place to hold all sample specific information
# June - 2016

# Excellent Source: https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
# See Kenneth's Log Book for how to find this stuff on MCM: https://twiki.cern.ch/twiki/bin/view/Main/KDLLogBook#LogDay20150106
# The scale factor is for LO -> NNLO scaling see excel sheet below https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#MC_samples

from collections import OrderedDict

def returnSampleDetails( analysis, samples=[] ) :
    sampleMap = sampleDetails( analysis )
    #print sampleMap
    returnMap = OrderedDict()
    for sample in samples :
        if sample in sampleMap.keys() :
            returnMap[ sample ] = sampleMap[ sample ]
    return returnMap


def sampleDetails( analysis ) :
    c74x = 'RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2'
    c76x = 'RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12'
    c80x = 'RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3'
    c80xReHLT = 'RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14'
    c80xMAOD2 = 'RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0'
    sampleMap = {
        'Sync' : {
            'Sync-HtoTT': {
                'DASPath' : '/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 999.,
                'group' : 'sync'
        }}, # end Sync sample

        'htt' : {
            'dataTT' : {
                'DASPath' : '/Tau/Run2015D-16Dec2015-v1/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'VV' :         { 
                'DASPath' : '/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 11.95,
                'group' : 'dib'},
            'ZZ2l2q' :     { 
                'DASPath' : '/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 3.22,
                'group' : 'dib'},
            'WW1l1nu2q' :  { 
                'DASPath' : '/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 49.997,
                'group' : 'dib'},
            'WZ2l2q' :     { 
                'DASPath' : '/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 5.595,
                'group' : 'dib'},
            'WZ1l3nu' :    { 
                'DASPath' : '/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 3.05,
                'group' : 'dib'},
            'WZ1l1nu2q' :  { 
                'DASPath' : '/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 10.71,
                'group' : 'dib'},
            'Tbar-tW' :    { 
                'DASPath' : '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 35.6,
                'group' : 'dib'},
            'T-tW' :       { 
                'DASPath' : '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 35.6,
                'group' : 'dib'},
            'T-tchan' :    { 
                'DASPath' : '/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 136.02,
                'group' : 'dib'},
            'Tbar-tchan' : { 
                'DASPath' : '/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 80.95,
                'group' : 'dib'},
            'TT' :         { 
                'DASPath' : '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/%s_ext3-v1/MINIAODSIM' % c80x,
                'xsec' : 831.76,
                'group' : 'top'},
            'WJets' :      { 
                'DASPath' : '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 50380 * 1.221252,
                'group' : 'wjets'},
            'WJets1' :     { 
                'DASPath' : '/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 9644.5 * 1.221252,
                'group' : 'wjets'},
            'WJets2' :     { 
                'DASPath' : '/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 3144.5 * 1.221252,
                'group' : 'wjets'},
            'WJets3' :     { 
                'DASPath' : '/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 954.8 * 1.221252,
                'group' : 'wjets'},
            'WJets4' :     { 
                'DASPath' : '/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 485.6 * 1.221252,
                'group' : 'wjets'},
            'DYJets' :     { 
                'DASPath' : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s_ext1-v1/MINIAODSIM' % c80x, 
                'xsec' : 4954.0 * 1.216229,
                'group' : 'dyj'},
            'DYJets1' :    { 
                'DASPath' : '/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 1012.5 * 1.216229,
                'group' : 'dyj'},
            'DYJets2' :    { 
                'DASPath' : '/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 332.8 * 1.216229,
                'group' : 'dyj'},
            'DYJets3' :    { 
                'DASPath' : '/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 101.8 * 1.216229,
                'group' : 'dyj'},
            'DYJets4' :    { 
                'DASPath' : '/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 54.8 * 1.216229,
                'group' : 'dyj'},
            'DYJetsHigh' : {
                'DASPath' : '/DYJetsToLL_M-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 6.657,
                'group' : 'dyj'},
            'DYJetsLow' :  {
                'DASPath' : '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80x, 
                'xsec' : 18610.,
                'group' : 'dyj'},
             'ggHtoTauTau120': {
                'DASPath' : '/GluGluHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 47.38 * 0.0698,
                'group' : 'ggh'},
             'ggHtoTauTau125': {
                'DASPath' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 44.14 * 0.0627,
                'group' : 'ggh'},
             'ggHtoTauTau130': {
                'DASPath' : '/GluGluHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 41.23 * 0.0541,
                'group' : 'ggh'},
             'VBFHtoTauTau120': {
                'DASPath' : '/VBFHToTauTau_M120_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 3.935 * 0.0698,
                'group' : 'vbf'},
             'VBFHtoTauTau125': {
                'DASPath' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 3.782 * 0.0627,
                'group' : 'vbf'},
             'VBFHtoTauTau130': {
                'DASPath' : '/VBFHToTauTau_M130_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 3.637 * 0.0541,
                'group' : 'vbf'},
            #'DYJetsBig' : ('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s_ext1-v1/MINIAODSIM' % c80x, 4954.0 * 1.216229 ), 
        }, # end HTT
        'azh' : {
            # See H->ZZ samples: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsZZ4l2016#MC
            #'WZ3l1nu' : ('/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/%s-v1/MINIAODSIM' % c80x, 4.666 ),
            #'ZZ4l' :    ('/ZZTo4L_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c80x, 1.212 ),
            'dataEE' : {
                'DASPath' : '/DoubleEG/Run2016E-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'dataMM' : {
                'DASPath' : '/DoubleMuon/Run2016E-PromptReco-v2/MINIAOD',
                'xsec' : 999.,
                'group' : 'obs'},
            'ZZ4l' : {
                'DASPath' : '/ZZTo4L_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80x,
                'xsec' : 1.256 * 1.1, # See 1.1 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ZZ4lAMCNLO' : {
                'DASPath' : '/ZZTo4L_13TeV-amcatnloFXFX-pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 1.212 * 1.1, # See 1.1 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ2e2m' : {
                'DASPath' : '/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 0.00319 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ2e2tau' : {
                'DASPath' : '/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 0.00319 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ2m2tau' : {
                'DASPath' : '/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 0.00319 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ4e' : {
                'DASPath' : '/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 0.00159 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ4m' : {
                'DASPath' : '/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 0.00159 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'ggZZ4tau' : {
                'DASPath' : '/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 0.00159 * 1.7, # See 1.7 k-factor in Devin's HIG-16-036
                'group' : 'zz'},
            'WZ3l1nu' : {
                'DASPath' : '/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 4.42965, # Devin's
                'group' : 'wz'},
            'DYJets' :     { 
                'DASPath' : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s_ext1-v1/MINIAODSIM' % c80xMAOD2, 
                'xsec' : 4954.0 * 1.216229,
                'group' : 'dyj'},
            'DYJets1' :    { 
                'DASPath' : '/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 1012.5 * 1.216229,
                'group' : 'dyj'},
            'DYJets2' :    { 
                'DASPath' : '/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 332.8 * 1.216229,
                'group' : 'dyj'},
            'DYJets3' :    { 
                'DASPath' : '/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 101.8 * 1.216229,
                'group' : 'dyj'},
            'DYJets4' :    { 
                'DASPath' : '/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/%s-v1/MINIAODSIM' % c80xMAOD2,
                'xsec' : 54.8 * 1.216229,
                'group' : 'dyj'},
            'TT' :         { 
                'DASPath' : '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/%s_ext3-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 831.76,
                'group' : 'top'},
            'WPlusHTauTau' : {
                'DASPath' : '/WplusHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 1.373 * 0.0627 * 0.5,
                'group' : 'sm'},
            'WMinusHTauTau' : {
                'DASPath' : '/WminusHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 1.373 * 0.0627 * 0.5,
                'group' : 'sm'},
            'ZHTauTau' : {
                'DASPath' : '/ZHToTauTau_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 0.884 * 0.0627,
                'group' : 'sm'},
            'ttHTauTau' : {
                'DASPath' : '/ttHToTT_M125_13TeV_powheg_pythia8/%s-v1/MINIAODSIM' % c80xReHLT,
                'xsec' : 0.507 * 0.0632,
                'group' : 'sm'},
            
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
        } # end AtoZh
    } # end sample Map

    # A to Zh sample masses
    for mass in [220, 240, 260, 280, 300, 320, 350, 400] :
        version = 'v1'
        if mass == 260 : version = 'v2'
        sampleMap['azh']['azh%i' % mass] = {
                'DASPath' : '/AToZhToLLTauTau_M-%i_13TeV_madgraph_4f_LO/%s-%s/MINIAODSIM' % (mass, c80xReHLT, version),
                'xsec' : 1.,
                'group' : 'azh'}
            
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



