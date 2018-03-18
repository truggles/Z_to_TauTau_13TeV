# Z_to_TauTau_13TeV
This repository is for the CMS analysis of Z -> TauTau (emu and di-hadronic tau final states) at 13TeV

Ties with UW - Final State Analysis:
The analysis relies on flat Ntuple output from UW's Final State Analysis: 
https://github.com/uwcms/FinalStateAnalysis/tree/miniAOD_dev_74X
Additionally, before you get going, make sure that you install the 
'highly recommended' python tools (they are necessary!) in FSA located here:
```bash
    recipe/install_python.sh
```
Load from GitHub the measured lepton efficiencies for scale factors
and HLT DoubleTau35 efficiencies
```bash
    source setup.py
```

If any FSA ntuples have been updated, make a list of the backgrounds and data 
samples in:
```bash
    meta/NtupleInputs_[htt/Sync/azh]
```
And, make sure DAS paths and updated cross sections are all in 
```bash
    meta/makeMeta.py
```
Most all portions of the current analysis are run from 'run.py'
Open run.py and edit the fields mid1, mid2, mid3 in the params directory to 
specific 3 folder names to store your output files as they are skimmed and 
turned from TTree to histogram. Do not name them the same thing!

In run.py, make sure to uncomment the region around the makeMetaJSON function and 
the buildAllPUTemplates function.

In run.py, analysis1BaselineCuts.doInitialCutsAndOrder performs our initial skim
based on the params and samples as inputs.  Additionally, it
isolation orders the lepton pairs and chooses the single lepton configuration
to pass selection cuts.

In run.py, analysis1BaselineCuts.drawHistos draws all histograms specified in 
'analysisPlots.py' into a final background specific file ready for plotting.

The first time you run run.py make sure to include the bottom section
with WJets and QCD which procuce high stats smoothed shape templates for
latter plotting.

After configuring:
```bash
    python run.py
```

analysis3Plots.py performs the plotting of histos.  There are a number of
flags for your convenience, with the --folder one being required.
--folder should match 'mid3' from params. --log, --ratio are also
available as is a No QCD option.  The hard coded scaling numbers are
all located at the top of the script.  There are useful, pre-baked
Text outputs onto the TCanvas, search 'text1' to find them and uncomment/
edit.  The samples that are plotted are all listed in the samples ordered
dictionary ~ line 50.  Run similar to this:
```bash
    python analysis3Plots.py --folder=Oct16NeatCuts --ratio=True --qcd=False --qcdShape=[Sync/Loose]
```
analysis3Plots.py makes a niffty html viewing template for smooth web viewing
of plots, consider symlinking your output folder to a web directory.
I added a qcdShape option that has a default of using the 'Sync' triggers for
creating the QCD shape.

Newest Addition:
A draft script to create the 'shape' files for making data cards is now
implemented.  It requires the same --folder=XXX to locate which set of
histos to make the shapes file with.  Note, that, like the analysis3Plots.py
script, there is again a default qcdShape option.
```bash
    python analysisShapesROOT.py --folder=3oct21Sync --qcdShape=Sync
```

:-)


ZH/AZh analysis:
relies on azhRun.py
has ability to use MC based reducible bkg method or data driven RedBkg method
the cuts for the data driven RedBkg method are not in a consolidated place, if updating them please change the cuts in:
util/azhReducibleBackground.py
util/azhReducibleBackgroundHelpers.py
analysisCuts.py


Auxilary Functions:
Tau Tracking Study tools including an analyzer and plotter can be found in
Z_to_TauTau_13TeV/ThreeProngTaus<BR>
To run:<BR>
0 - if you are changing the target runs, you will need to change a number of hardcoded run #s<BR>
1 - find relevant files and put them in the files labeled 'targetRunXXXX.txt'<BR>
2 - update the 'targetRunsJSON.txt' file for good lumi masks<BR>
    - `/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt`<BR>
3 - make a folder for each run with the run number<BR>
4 - `python runTauAnalysis.py`<BR>
5 - `source env.sh`<BR>
6 - `python tauPlotting.py`<BR>
7 - view plots online: `http://truggles.web.cern.ch/truggles/threeProngs/`<BR>

Fake Factors additions:
Fake factors have been derived to estimate QCD, WJets and TTJets from data, initially for the MuTau channel, but are being tested in double hadronic channel.  Find documentations here: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauJet2TauFakes

# MELA Stuff
This relies on CMS package ZZMatrixElement, for checkout instructions see:<BR>
`https://twiki.cern.ch/twiki/bin/viewauth/CMS/MELAProject`<BR>
and, other random MELA notes from Kansas State team:<BR>
`https://twiki.cern.ch/twiki/bin/view/Main/AHVVforHTT#NTuples_with_all_the_FSA_variabl`

For adding the MELA variables to the FSA Ntuples in the tautau channel see below<BR>
You will need to update the file list in `MELA/anaHTT.C` to newest working files then:<BR>
1 - `cp MELA/anaHTT.C ../ZZMatrixElement/MELA/test/anaHTT.C`<BR>
2 - `cd ../ZZMatrixElement/MELA/test/`<BR>
3 - `mkdir mela`<BR>
4 - `root -l loadMELA.C`<BR>
5 - IN ROOT CINT: root [1] `.L anaHTT.C+`<BR>
6 - IN ROOT CINT: root [2] `runAll()`<BR>


Other aHTT notes: To produce the interferance terms between SM and BSM, after making DCs, you need to run:
```
python util/addInterferenceTermAnomHTT.py
```
As of 18, Mar 2018, Senka has been adding the interferance terms so this part is not needed.

# Current Status
Added MELA vars and anomalous higgs reweighting variables to samples in meta/..skimmed...

Added .sh file to hadd aHTT signals and make 1 master file for plotting
```
source prep_reweighted_samples.sh DIRECTORY_FILES_IN
```




