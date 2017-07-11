# Temporary submit script to submit the user produced anomalous 
# HTT samples through FSA to condor
# 11 July 2017

# You will want to copy this file and the associated VBF* 
# files in this directory to FinalStateAnalysis/NtupleTools/test/


DATE=july11_v3
for SAMPLE in VBFHiggs0L1 VBFHiggs0L1f05ph0 VBFHiggs0Mf05ph0 VBFHiggs0PHf05ph0 VBFHiggs0PM_v6 VBFHiggs0M VBFHiggs0PH VBFHiggs0PM; do

    mkdir -p /data/${USER}/aHTT_signals_${DATE}/${SAMPLE}/dags/daginputs/
    cp ${SAMPLE}.txt /data/${USER}/aHTT_signals_${DATE}/${SAMPLE}/dags/daginputs/${SAMPLE}_inputfiles.txt

    farmoutAnalysisJobs --infer-cmssw-path "--submit-dir=/data/${USER}/aHTT_signals_${DATE}/${SAMPLE}/submit" "--output-dag-file=/data/${USER}/aHTT_signals_${DATE}/${SAMPLE}/dags/dag" "--output-dir=srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/${USER}/aHTT_signals_${DATE}/${SAMPLE}/" --input-files-per-job=50 --job-count=1000000 --extra-usercode-files="src/FinalStateAnalysis/NtupleTools/python/parameters" --input-file-list=/data/${USER}/aHTT_signals_${DATE}/${SAMPLE}/dags/daginputs/${SAMPLE}_inputfiles.txt --assume-input-files-exist --input-dir=/ aHTT_signals_${DATE}-${SAMPLE} make_ntuples_cfg.py channels=em,et,tt,mt isMC=1 skipMET=1 htt=1 fullJES=1 skipGhost=1 runMVAMET=0 paramFile=CMSSW_8_0_26_patch1/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py 'inputFiles=$inputFileNames' 'outputFile=$outputFileName'

done
