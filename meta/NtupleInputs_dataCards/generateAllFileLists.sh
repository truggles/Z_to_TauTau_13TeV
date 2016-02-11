
DATA=feb10_data
TT=feb10_TT
DY=feb10_dyjets
BKGS=feb10_bkgsAndSignals


ls /data/truggles/${DATA}/data_Tau_Run2015D_16Dec2015_25ns/submit/make_ntuples_cfg-*/*.root > data_tt.txt 
ls /data/truggles/${DATA}/data_MuonEG_Run2015D_16Dec2015_25ns/submit/make_ntuples_cfg-*/*.root > data_em.txt 
ls /data/truggles/${DY}/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > DYJets.txt 
ls /data/truggles/${BKGS}/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > DYJets1.txt 
ls /data/truggles/${BKGS}/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > DYJets2.txt 
ls /data/truggles/${BKGS}/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > DYJets3.txt 
ls /data/truggles/${BKGS}/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > DYJets4.txt 
#ls /data/truggles/${BKGS}/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > DYJets100-200.txt
#ls /data/truggles/${BKGS}/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > DYJets200-400.txt
#ls /data/truggles/${BKGS}/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > DYJets400-600.txt
#ls /data/truggles/${BKGS}/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > DYJets600-Inf.txt
ls /data/truggles/${BKGS}/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/*/*/*.root > T-tchan.txt 
ls /data/truggles/${BKGS}/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/*/*/*.root > T-tchan.txt 
ls /data/truggles/${BKGS}/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/*/*/*.root > Tbar-tW.txt 
ls /data/truggles/${BKGS}/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/*/*/*.root > T-tW.txt 
ls /data/truggles/${TT}/TT_TuneCUETP8M1_13TeV-powheg-pythia8/*/*/*.root > TT.txt 
ls /data/truggles/${BKGS}/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/*/*/*.root > WJets.txt 
#ls /data/truggles/${BKGS}/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > WJets100-200.txt 
#ls /data/truggles/${BKGS}/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > WJets200-400.txt 
#ls /data/truggles/${BKGS}/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > WJets400-600.txt 
#ls /data/truggles/${BKGS}/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*.root > WJets600-Inf.txt 
ls /data/truggles/${BKGS}/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root > WW1l1nu2q.txt 
ls /data/truggles/${BKGS}/WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/*/*/*.root > WZJets.txt
ls /data/truggles/${BKGS}/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/*/*/*.root > WZ1l3nu.txt 
ls /data/truggles/${BKGS}/ZZTo4L_13TeV-amcatnloFXFX-pythia8/*/*/*.root > ZZ4l.txt 
