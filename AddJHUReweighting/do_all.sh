IN_DIR=/data/truggles/svFitJune22_aHTT_samples2/
OUT_DIR=/data/truggles/svFitJune22_aHTT_samples3/
YURII_DIR=/afs/cern.ch/work/y/ymaravin/public/Reweighing/

./plot.exe ${IN_DIR}VBFHtoTauTau0L1125_tt.root          ${YURII_DIR}vbf_l1.root  ${OUT_DIR}VBFHtoTauTau0L1125_tt.root
./plot.exe ${IN_DIR}VBFHtoTauTau0L1f05ph0125_tt.root    ${YURII_DIR}vbf_l1f05.root  ${OUT_DIR}VBFHtoTauTau0L1f05ph0125_tt.root
./plot.exe ${IN_DIR}VBFHtoTauTau0M125_tt.root           ${YURII_DIR}vbf_a3.root  ${OUT_DIR}VBFHtoTauTau0M125_tt.root
./plot.exe ${IN_DIR}VBFHtoTauTau0Mf05ph0125_tt.root     ${YURII_DIR}vbf_a3f05.root  ${OUT_DIR}VBFHtoTauTau0Mf05ph0125_tt.root
./plot.exe ${IN_DIR}VBFHtoTauTau0PH125_tt.root          ${YURII_DIR}vbf_a2.root  ${OUT_DIR}VBFHtoTauTau0PH125_tt.root
./plot.exe ${IN_DIR}VBFHtoTauTau0PHf05ph0125_tt.root    ${YURII_DIR}vbf_a2f05.root  ${OUT_DIR}VBFHtoTauTau0PHf05ph0125_tt.root
./plot.exe ${IN_DIR}VBFHtoTauTau0PM125_tt.root          ${YURII_DIR}vbf_sm.root  ${OUT_DIR}VBFHtoTauTau0PM125_tt.root
./plot.exe ${IN_DIR}WHtoTauTau0L1125_tt.root            ${YURII_DIR}wh_l1.root  ${OUT_DIR}WHtoTauTau0L1125_tt.root
./plot.exe ${IN_DIR}WHtoTauTau0L1f05ph0125_tt.root      ${YURII_DIR}wh_l1f05.root  ${OUT_DIR}WHtoTauTau0L1f05ph0125_tt.root
./plot.exe ${IN_DIR}WHtoTauTau0M125_tt.root             ${YURII_DIR}wh_a3.root  ${OUT_DIR}WHtoTauTau0M125_tt.root
./plot.exe ${IN_DIR}WHtoTauTau0Mf05ph0125_tt.root       ${YURII_DIR}wh_a3f05.root  ${OUT_DIR}WHtoTauTau0Mf05ph0125_tt.root
./plot.exe ${IN_DIR}WHtoTauTau0PH125_tt.root            ${YURII_DIR}wh_a2.root  ${OUT_DIR}WHtoTauTau0PH125_tt.root
./plot.exe ${IN_DIR}WHtoTauTau0PHf05ph0125_tt.root      ${YURII_DIR}wh_a2f05.root  ${OUT_DIR}WHtoTauTau0PHf05ph0125_tt.root
./plot.exe ${IN_DIR}WHtoTauTau0PM125_tt.root            ${YURII_DIR}wh_sm.root  ${OUT_DIR}WHtoTauTau0PM125_tt.root
./plot.exe ${IN_DIR}ZHtoTauTau0L1125_tt.root            ${YURII_DIR}zh_l1.root  ${OUT_DIR}ZHtoTauTau0L1125_tt.root
./plot.exe ${IN_DIR}ZHtoTauTau0L1f05ph0125_tt.root      ${YURII_DIR}zh_l1f05.root  ${OUT_DIR}ZHtoTauTau0L1f05ph0125_tt.root
./plot.exe ${IN_DIR}ZHtoTauTau0M125_tt.root             ${YURII_DIR}zh_a3.root  ${OUT_DIR}ZHtoTauTau0M125_tt.root
./plot.exe ${IN_DIR}ZHtoTauTau0Mf05ph0125_tt.root       ${YURII_DIR}zh_a3f05.root  ${OUT_DIR}ZHtoTauTau0Mf05ph0125_tt.root
./plot.exe ${IN_DIR}ZHtoTauTau0PH125_tt.root            ${YURII_DIR}zh_a2.root  ${OUT_DIR}ZHtoTauTau0PH125_tt.root
./plot.exe ${IN_DIR}ZHtoTauTau0PHf05ph0125_tt.root      ${YURII_DIR}zh_a2f05.root  ${OUT_DIR}ZHtoTauTau0PHf05ph0125_tt.root
./plot.exe ${IN_DIR}ZHtoTauTau0PM125_tt.root            ${YURII_DIR}zh_sm.root  ${OUT_DIR}ZHtoTauTau0PM125_tt.root

#./plot.exe ${IN_DIR}ggH125-maxmix_tt.root                 ${YURII_DIR}ggH_a3f05.root  ${OUT_DIR}ggH125-maxmix_tt.root
#./plot.exe ${IN_DIR}ggH125-pseudoscalar_tt.root           ${YURII_DIR}ggH_a3.root  ${OUT_DIR}ggH125-pseudoscalar_tt.root
#./plot.exe ${IN_DIR}ggH125-sm_tt.root                     ${YURII_DIR}ggH_sm.root  ${OUT_DIR}ggH125-sm_tt.root
