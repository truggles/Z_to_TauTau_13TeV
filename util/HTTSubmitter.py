
import subprocess

# HTT Strings
configsHTT='channels=tt skipMET=1 paramFile=CMSSW_8_0_8/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/data/Fal* src/FinalStateAnalysis/NtupleTools/python/parameters --output-dir=.'
dataHTT='--das-replace=/afs/cern.ch/work/t/truggles/Z_to_tautau/CMSSW_8_0_8/src/FinalStateAnalysis/MetaData/tuples/MiniAOD-13TeV_Data.json --apply-cmsRun-lumimask --samples data_Tau_Run2016*_25ns --data -o'
sync='--campaign-tag=RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3* --samples SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8 -o' 
TT='--campaign-tag=RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext3-v1 --samples TT_TuneCUETP8M1_13TeV-powheg-pythia8 -o' 
MC='--campaign-tag=RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3* --samples GluGluHToTauTau_M125_13TeV_powheg_pythia8 ZZTo4L_13TeV-amcatnloFXFX-pythia8 WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8 WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8 ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1 ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1 ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1 ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1 DY[1,2,3,4]JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8 WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8 DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8 WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8 WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8 DYJetsToLL_M-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 W*JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -o' 
htt='--campaign-tag=RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v* --samples GluGluHToTauTau_M125_13TeV_powheg_pythia8 VBFHToTauTau_M125_13TeV_powheg_pythia8 -o' 

# AZH Strings
configsAZH='channels=eeee,mmmm,eeet,eemt,eett,eeem,mmet,mmmt,mmtt,mmem,eemm skipMET=1 paramFile=CMSSW_8_0_8/src/FinalStateAnalysis/NtupleTools/python/parameters/azh.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/data/Fal* src/FinalStateAnalysis/NtupleTools/python/parameters --output-dir=.'
#DYJetsJB='--campaign-tag=RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3* --samples DY[1,2,3,4]JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -o' 
#ZZ_WZ='--campaign-tag=RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1 --samples ZZTo4L_13TeV_powheg_pythia8 WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8 -o' 
#AZH='--campaign-tag=RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v* --samples AToZhToLLTauTau_M-*_13TeV_madgraph_4f_LO -o' 
dataAZH='--das-replace=/afs/cern.ch/work/t/truggles/Z_to_tautau/CMSSW_8_0_8/src/FinalStateAnalysis/MetaData/tuples/MiniAOD-13TeV_Data.json --apply-cmsRun-lumimask --samples data_DoubleEG_Run2016*_25ns data_DoubleMuon_Run2016*_25ns --data -o'
#ZZamcnlo='--campaign-tag=RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1 --samples ZZTo4L_13TeV-amcatnloFXFX-pythia8 -o' 
reHLT='--campaign-tag=RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14* --samples WplusHToTauTau_M125_13TeV_powheg_pythia8 WminusHToTauTau_M125_13TeV_powheg_pythia8 ZHToTauTau_M125_13TeV_powheg_pythia8 ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8 ZZTo4L_13TeV-amcatnloFXFX-pythia8 AToZhToLLTauTau_M-*_13TeV_madgraph_4f_LO -o'
reHLTExt='--campaign-tag=RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext* --samples TT_TuneCUETP8M1_13TeV-powheg-pythia8 -o'
miniAODv2='--campaign-tag=RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1 --samples GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8 GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8 GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8 GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8 GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8 GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8 DY[1,2,3,4]JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8 -o'
miniAODv2Ext='--campaign-tag=RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1 --samples DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -o'
# TT is the same for both




mapper = {
    # HTT double hadronic channel
    'htt' : {
    'data' : ['isMC=0', dataHTT],
    'sync' : ['isMC=1', sync],
    'TT' : ['isMC=1', TT],
    'MC' : ['isMC=1', MC],
    'HTT' : ['isMC=1', htt],
    }, # end HTT
    # AZH 11 channels (eeee,mmmm,eemm included)
    'azh' : {
    'data' : ['isMC=0', dataAZH],
    #'TT' : ['isMC=1', TT],
    #'DYJetsJB' : ['isMC=1', DYJetsJB],
    #'ZZ_WZ' : ['isMC=1', ZZ_WZ],
    #'reHLT' : ['isMC=1', reHLT],
    #'reHLTExt' : ['isMC=1', reHLTExt],
    #'miniAODv2' : ['isMC=1', miniAODv2],
    #'miniAODv2Ext' : ['isMC=1', miniAODv2Ext],
    }, # end AZH
}


def makeSubmitScripts( analysis, jobid ) :
    if analysis == 'htt' :
        configs = configsHTT
    if analysis == 'azh' :
        configs = configsAZH
    else : print "ERROR, no configs specified"

    for key in mapper[analysis].keys() :
        standardProcess = ["submit_job.py",jobid+'_'+analysis,"make_ntuples_cfg.py"]
        standardProcess.append( mapper[analysis][key][0] )
        info = configs.split(' ')
        for item in info :
            standardProcess.append( item )
        info = mapper[analysis][key][1].split(' ')
        for item in info :
            standardProcess.append( item )
        
        
        standardProcess.append( jobid+'_'+analysis+'_'+key+'.sh' )
        
        print standardProcess
        subprocess.call( standardProcess )




if __name__ == '__main__' :    
    jobid='aug03'
    analysis='azh'
    
    if analysis == 'azh' :
        print "\n\n\n REMEMBER THAT AZH SIGNAL SAMPLE IS A ReHLT SAMPLE"
        print " --- edit file ../../PatTools/python/finalStates/patFinalStateEventProducer_cfi.py"
        print " --- so that line 34 is 'HLT2' not 'HLT' and re-run this"
        print "\n\n\n"


    makeSubmitScripts( analysis, jobid )

    if analysis == 'azh' :
        print "\n\n\n REMEMBER THAT AZH SIGNAL SAMPLE IS A ReHLT SAMPLE"
        print " --- edit file ../../PatTools/python/finalStates/patFinalStateEventProducer_cfi.py"
        print " --- so that line 34 is 'HLT2' not 'HLT' and re-run this"
        print "\n\n\n"




