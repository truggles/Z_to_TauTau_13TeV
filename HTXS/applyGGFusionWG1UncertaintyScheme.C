
#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <vector>
#include <fstream>
#include <cstdlib>
#include <iomanip>
#include "TMath.h"
#include "TFile.h"
#include "TH1.h"
#include "TTree.h"
#include "TString.h"
#include "TDirectory.h"


void add_ggH_HTXS_weights(TString InFile, TString OutFile)
{

    std::cout << "Starting!!!" << std::endl;
    std::cout << InFile << std::endl;

    
    TFile *finput = new TFile(InFile);
    TTree *tree = (TTree*) finput->Get("tt/final/Ntuple");
    TH1D *oEvtCnt = (TH1D*) finput->Get("tt/eventCount");
    TH1D *oSumWeights = (TH1D*) finput->Get("tt/summedWeights");
    

    float THU_ggH_Mu, THU_ggH_Res, THU_ggH_Mig01, THU_ggH_Mig12, 
        THU_ggH_VBF2j, THU_ggH_VBF3j, THU_ggH_PT60, THU_ggH_PT120, THU_ggH_qmtop;
    
    Float_t         higgs_pt;
    Float_t         nJets30;
    Float_t         rivet_stage1_nJets30;
    
    tree->SetBranchAddress("Rivet_higgsPt", &higgs_pt);
    tree->SetBranchAddress("Rivet_nJets30", &nJets30);
    //tree->SetBranchAddress("jetVeto30", &nJets30);
    tree->SetBranchAddress("Rivet_stage1_cat_pTjet30GeV", &rivet_stage1_nJets30);

    TFile* foutput = new TFile(OutFile, "recreate");

    // Keep out original TDirectory structure
    TDirectory* d1 = foutput->mkdir("tt");
    TDirectory* d2 = d1->mkdir("final");

    // Copy our event count histos to the new file
    TH1D *eventCount = (TH1D*)oEvtCnt->Clone("eventCount");
    TH1D *summedWeights = (TH1D*)oSumWeights->Clone("summedWeights");
    d1->cd();
    eventCount->Write();
    summedWeights->Write();
    
    
    TTree* newtree = new TTree("TestTree", "");
    newtree = tree->CloneTree(0);
    newtree->Branch("THU_ggH_Mu",    &THU_ggH_Mu);
    newtree->Branch("THU_ggH_Res",   &THU_ggH_Res);
    newtree->Branch("THU_ggH_Mig01", &THU_ggH_Mig01);
    newtree->Branch("THU_ggH_Mig12", &THU_ggH_Mig12);
    newtree->Branch("THU_ggH_VBF2j", &THU_ggH_VBF2j);
    newtree->Branch("THU_ggH_VBF3j", &THU_ggH_VBF3j);
    newtree->Branch("THU_ggH_PT60" , &THU_ggH_PT60);
    newtree->Branch("THU_ggH_PT120", &THU_ggH_PT120);
    newtree->Branch("THU_ggH_qmtop", &THU_ggH_qmtop);


    Long64_t nentries = tree->GetEntries();
    
    Long64_t nbytes = 0, nb = 0;
    for (Long64_t jentry=0; jentry<nentries;jentry++) {
        if ( jentry % 100 == 0 ) std::cout << jentry << std::endl;
        nb = tree->GetEntry(jentry);   nbytes += nb;
        
        tree->GetEntry(jentry);
        //std::cout << "Higgs_Pt: " << higgs_pt << "   nJets30: " << nJets30 << "  Stage1: " << rivet_stage1_nJets30 << std::endl;
        

        // Get uncertainties
        std::vector<double> uncertainties = qcd_ggF_uncertSF_2017( nJets30, higgs_pt, rivet_stage1_nJets30 );


        //std::cout << "post-entries" << std::endl;
        //for (auto entry : uncertainties) {
        //    std::cout << entry << ": ";
        //}
        //std::cout << std::endl;

        THU_ggH_Mu = uncertainties[0];
        THU_ggH_Res = uncertainties[1];
        THU_ggH_Mig01 = uncertainties[2];
        THU_ggH_Mig12 = uncertainties[3];
        THU_ggH_VBF2j = uncertainties[4];
        THU_ggH_VBF3j = uncertainties[5];
        THU_ggH_PT60 = uncertainties[6];
        THU_ggH_PT120 = uncertainties[7];
        THU_ggH_qmtop = uncertainties[8];

 
        newtree->Fill();
    }
    //foutput->WriteTObject(newtree);
    d2->WriteTObject(newtree);
    delete newtree;
    foutput->Close();
    finput->Close();
}

void runAll() {
    std::vector<std::string> files;
    // NO .ROOT HERE!
    //files.push_back("");
    //files.push_back("ggHtoTauTau110_0_tt");
    //files.push_back("ggHtoTauTau110_1_tt");
    //files.push_back("ggHtoTauTau120_0_tt");
    files.push_back("ggHtoTauTau125_0_tt");
    files.push_back("ggHtoTauTau125_1_tt");
    //files.push_back("ggHtoTauTau130_0_tt");
    //files.push_back("ggHtoTauTau140_0_tt");
    //files.push_back("ggHtoTauTau140_1_tt");
    //files.push_back("ggHtoTauTauNNLOPS125_0_tt");
    std::string base = "/data/truggles/HTXS_ggH_svFitted_Sept01_merged/"; // Need last / on path

    for(auto file : files ){
        std::cout << file << std::endl;
        add_ggH_HTXS_weights( base+file+".root", "/data/truggles/HTXS_ggH_svFitted_Sept01_merged2/"+file+".root");    
    }
}

