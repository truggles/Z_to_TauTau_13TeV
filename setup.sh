
# For smart access to environment varialbes
pip install smart-getenv


pushd data
# Get the histograms with lepton scale factors
git clone https://github.com/CMS-HTT/LeptonEfficiencies.git

# Get the double tau trigger efficiencies provided by Riccardo Manzoni
git clone -b moriond17 https://github.com/rmanzoni/triggerSF.git
popd


# For using the Fake Factor method
pushd $CMSSW_BASE/src
git clone https://github.com/CMS-HTT/Jet2TauFakes.git HTTutilities/Jet2TauFakes
cd HTTutilities/Jet2TauFakes
git checkout v0.2.1
#mkdir data
#cp -r /afs/cern.ch/user/j/jbrandst/public/Htautau/FakeRate/20160914/* data/
popd

echo "Hopefully temporary fix, using special FF files from Johannes"
pushd $CMSSW_BASE/Z_to_TauTau_13TeV/data
mkdir -p FakeFactors/tt
cp -r /afs/cern.ch/user/j/jbrandst/public/Htautau/FakeRate/2016/20170215/tt/* ./FakeFactors/tt/
popd


echo "You must <scram b -j 8>"
