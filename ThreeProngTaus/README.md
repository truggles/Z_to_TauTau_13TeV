DAS paths:
/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD
/SingleMuon/CMSSW_8_0_0_pre6-80X_dataRun2_v4_RelVal_sigMu2015HLHT-v1/MINIAOD
/SingleMuon/CMSSW_8_0_0_pre6-80X_dataRun2_v4_RelVal_sgMuPrpt2015D-v1/MINIAOD
/SingleMuon/CMSSW_8_0_0_pre6-80X_dataRun2_v4_RelVal_sigMu2015D-v1/MINIAOD

file dataset=/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD run=256677

Make sure to run 80X samples in an 80X CMSSW and 76X samples in 76X CMSSW



Updates as of April 2016:
New comparisons are between different pixel tracker configurations, either as is, or 2017 upgrade.  They need to be run in 810_pre3 or later.

1. Use the python scripts in '2017TrackerScripts' and cmsRun to generate miniAODSim files for use later in the process.
2. use 'runTauAnalysis80x.py' were you can list the path to local miniAODSim files you created in step 1.
3. Changes from the data comparisons before include ignoring triggers b/c CMS doesn't do triggers in MC right now, ignore lumi sections.
4. use 'tauPlotting.py' to plot to any directory, currently set up to my public html enabled one.
