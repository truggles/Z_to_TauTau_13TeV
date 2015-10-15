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

If any FSA ntuples have been updated, make a list of the backgrounds and data 
samples in:
```bash
    meta/NtupleInputs_[25/50]ns
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
    python analysis3Plots.py --folder=Oct16NeatCuts --ratio=True --qcd=False
```
analysis3Plots.py makes a niffty html viewing template for smooth web viewing
of plots, consider symlinking your output folder to a web directory.

:-)
