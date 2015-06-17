
This directory stores the locations of our samples Ntuple files in NtuplesInputs.
Define the 'short' names for samples and provide their DAS path to look up their
basic info and store it in a JSON file.

What the user needs to do it:

1. provide a list of FSA Ntuple sample files in ./NtupleInputs/[short name].txt

2. provide a "short name" and the DAS path & cross section to each sample in 
	makeMeta.py's 'samples' dictionary

3. run 'python makeMeta.py' from the meta directory which will provide a JSON
	file withthe info we need to get going
