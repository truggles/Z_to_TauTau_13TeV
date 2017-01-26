

echo " "
echo " "
echo "BASED OFF OF CECILE'S Jan ZH and HTT samples B,C,D,E,F,G,H"
#export LUMI=21000.0
#export LUMI=12900.0
export LUMI=36773.0
export LUMI=27916.0

echo "Set lumi = $LUMI"
echo "Using Full 2016 Data! Sans run H"


#echo "Lumi for /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt 20.1 / fb"

#echo "Lumi adjusted down b/c of removal of run 2788808 = 272 / pb"

#export doFF=1
export doFF=0
echo " "
echo "Setting Fake Factor Method to: $doFF"
echo " "
echo " "

export doFullJES=1
echo " "
echo "Setting Full JES Method to: $doFullJES"
echo " "
echo " "


export PYTHONPATH=$PYTHONPATH:$CMSSW_BASE/src/Z_to_TauTau_13TeV/



