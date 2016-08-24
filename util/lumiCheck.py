#
#
# Some helpful stuff for calculating luminosity
#
#

"""
See brilcalc.sh in home dir, this is a copy right here with brilcalc instructions
echo "1) make sure you are on lxplus"
echo "2) append new python path"
echo " "
echo "export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH"
echo " "

export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH

echo "2) complete"
echo "3) run 'brilcalc lumi -b "STABLE BEAMS" --normtag=/afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json -i filenameXXX -u /fb' with filenameXXX as your new json file"

echo "\n\nInfo for reinstalling brilcalc SW is here: http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html"
"""


import json


#with open('Cert_271036-277148_13TeV_PromptReco_Collisions16_JSON.txt') as jsonFile :
base = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/'
with open(base+'Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt') as jsonFile :
    jsonDict = json.load( jsonFile )

runsIn2016C = [
276242,
276243,
276095,
276097,
275836,
275837,
275841,
275960,
275963,
276071,
276072,
276074,
276092,
275769,
275772,
275773,
275774,
276185,
276186,
276190,
276235,
276237,
276049,
276062,
276063,
276064,
275920,
275921,
275922,
275776,
275777,
275838,
275923,
276181,
276183,
276244,
275782,
275783,
275846,
275847,
275886,
275887,
275890,
275911,
275912,
275913,
275918,
275931,
275958,
276271,
275778,
275781,
276276,
276279,
276282,
276283,
275828,
275829,
275831,
275832,
275833,
275834,
275835,
275420,
275476,
275588,
275601,
275603,
275656,
275657,
275658,
275659,
275752,
275757,
275758,
275759,
275761,
275763,
275764,
275766,
275767, 
275768] # runsIn2016C

outJson = {}
for run in jsonDict :
    if int(run) in runsIn2016C :
        print run,"in 2016C"
        continue 
    print run, jsonDict[run]
    outJson[run] = jsonDict[run]

with open('Cert_271036-276811_Sans2016C.txt', 'w') as outFile :
	json.dump( outJson, outFile, indent=2 )
	outFile.close()




