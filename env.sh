

echo " "
echo " "
echo "BASED OFF OF CECILE'S Jan ZH and HTT samples B,C,D,E,F,G,H"
###export LUMI=27916.0 # old lumi for sans H
#export LUMI=27218.1 # adjusted down by 2.5% like whole lumi above
export LUMI=35870.0

echo "Set lumi = $LUMI"
echo "Using Full 2016 Data!"


#echo "Lumi for /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt 20.1 / fb"

#echo "Lumi adjusted down b/c of removal of run 2788808 = 272 / pb"

#export doFF=true
export doFF=false 
echo " "
echo "Setting Fake Factor Method to: $doFF"
echo " "
echo " "

export doFullJES=false
#export doFullJES=true
echo " "
echo "Setting Full JES Method to: $doFullJES"
echo " "
echo " "


export PYTHONPATH=$PYTHONPATH:$CMSSW_BASE/src/Z_to_TauTau_13TeV/



