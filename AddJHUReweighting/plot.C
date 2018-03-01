#define plot_cxx
#include "plot.h"
#include <TH2.h>
#include <TDirectory.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <TH1.h>
#include <TFile.h>

#include <iostream>
#include <sstream>


using namespace std;

void plot::ReadInWeights(TString name)
{
  TFile* fileIn = TFile::Open(name);
  TTree* t1 = (TTree*)fileIn->Get("normalizedWeights");
  if ( t1 == nullptr ) t1 =  (TTree*)fileIn->Get("weights");
  ws_.clear();

  Long64_t eventID;
  Double_t wt_a1, wt_a2, wt_a3, wt_L1, wt_L1Zg;
  Double_t wt_a3int, wt_a2int, wt_L1int, wt_L1Zgint;

  t1->SetBranchAddress("eventID", &eventID);
  t1->SetBranchAddress("wt_a1", &wt_a1);
  t1->SetBranchAddress("wt_a3", &wt_a3);
  t1->SetBranchAddress("wt_a3int", &wt_a3int);

  if (std::string(name).find("ggH")!=std::string::npos) {
    wt_a2 = 0.;
    wt_L1 = 0.;
    wt_L1Zg = 0.;
    wt_a2int = 0.;
    wt_L1int = 0.;
    wt_L1Zgint = 0.;
  }
  else { // ggH only has above 3 branches.
    t1->SetBranchAddress("wt_a2", &wt_a2);
    t1->SetBranchAddress("wt_L1", &wt_L1);
    t1->SetBranchAddress("wt_L1Zg", &wt_L1Zg);
    t1->SetBranchAddress("wt_a2int", &wt_a2int);
    t1->SetBranchAddress("wt_L1int", &wt_L1int);
    t1->SetBranchAddress("wt_L1Zgint", &wt_L1Zgint);
  }

  Long64_t nentries = t1->GetEntries();
  for(Long64_t i = 0; i < nentries; ++i) {
    t1->GetEntry(i);
    weights w;
    w.eventID    = eventID;
    w.wt_a1      = wt_a1;
    w.wt_a2      = wt_a2;
    w.wt_a3      = wt_a3;
    w.wt_L1      = wt_L1;
    w.wt_L1Zg    = wt_L1Zg;
    w.wt_a3int   = wt_a3int;
    w.wt_a2int   = wt_a2int;
    w.wt_L1int   = wt_L1int;
    w.wt_L1Zgint = wt_L1Zgint;
    ws_.push_back(w);
  } // loop over entries of the lhe + higgs info root file
  delete t1;
  fileIn->Close();

  cout << "Done reading in weight factors" << endl;
  return;
}

void plot::Loop(TString OutFile, TTree* oldtree, TH1D* hnevents, TH1D* sumW)
{

  cout << "OutFile: " <<  OutFile << "  oldTree: " << oldtree << endl;

  TFile* foutput = new TFile(OutFile, "recreate");

  cout << "Outfile created: " << foutput->GetName() << endl;
  TDirectory* tt_dir = foutput->mkdir( "tt" );
  cout << "Made TDir tt: " << tt_dir << endl;
  tt_dir->cd();
  hnevents->Write();
  sumW->Write();
  cout << "Wrote TH1Ds" << endl;
  TDirectory* final_dir = tt_dir->mkdir( "final" );
  cout << "Made TDir final: " << final_dir << endl;

  ULong64_t evt=-1;
  Int_t lumi=-1;

  TBranch *b_evt;
  TBranch *b_lumi;

  float jhuw_a1=-1;
  float jhuw_a2=-1;
  float jhuw_a3=-1;
  float jhuw_l1=-1;
  float jhuw_l1Zg=-1;
  float jhuw_a2int=-1;
  float jhuw_a3int=-1;
  float jhuw_l1int=-1;
  float jhuw_l1Zgint=-1;

  oldtree->SetBranchAddress("evt", &evt, &b_evt);
  oldtree->SetBranchAddress("lumi", &lumi, &b_lumi);

  TTree* newtree = new TTree("TestTree", "");
  cout << "New TTree created: " << newtree->GetName() << endl;
  newtree = oldtree->CloneTree(0);
  newtree->Branch("jhuw_a1", &jhuw_a1);
  newtree->Branch("jhuw_a2", &jhuw_a2);
  newtree->Branch("jhuw_a3", &jhuw_a3);
  newtree->Branch("jhuw_l1", &jhuw_l1);
  newtree->Branch("jhuw_l1Zg", &jhuw_l1Zg);
  newtree->Branch("jhuw_a2int", &jhuw_a2int);
  newtree->Branch("jhuw_a3int", &jhuw_a3int);
  newtree->Branch("jhuw_l1int", &jhuw_l1int);
  newtree->Branch("jhuw_l1Zgint", &jhuw_l1Zgint);

  cout << "Cloned Tree: " << newtree->GetName() << endl;

  if (newtree == 0) return;
  cout << "newtree not == 0" << endl;
  
  Long64_t nentries = oldtree->GetEntries();
  cout << "newtree->GetEntries: " << nentries << endl;
  
  Long64_t nbytes = 0, nb = 0;
  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    nb = oldtree->GetEntry(jentry);   nbytes += nb;
    newtree->GetEntry(jentry);

    if ( jentry%1000 == 0 ) cout << "Processed " << jentry << " events" << endl;

    Long64_t l = lumi;
    Long64_t eventID = l*1000000 + evt;

    //cout << "Lumi: " << lumi << "  evt: " << evt << "  eventID: " << eventID << endl;

    // Set default values in case not found
	jhuw_a1 = -1;
	jhuw_a2 = -1;
	jhuw_a3 = -1;
    jhuw_l1 = -1;
    jhuw_l1Zg = -1;
    jhuw_a2int = -1;
    jhuw_a3int = -1;
    jhuw_l1int = -1;
    jhuw_l1Zgint = -1;
    for(int i = 0; i != ws_.size(); ++i) {
      weights w = ws_[i];
      //cout<<w.eventID<<" "<<eventID<<endl;
      if ( w.eventID == eventID ) {
	    //cout << "Match " << i << " with " << jentry << endl;
	    jhuw_a1 = w.wt_a1;
	    jhuw_a2 = w.wt_a2;
	    jhuw_a3 = w.wt_a3;
        jhuw_l1 = w.wt_L1;
        jhuw_l1Zg = w.wt_L1Zg;
        jhuw_a2int = w.wt_a2int;
        jhuw_a3int = w.wt_a3int;
        jhuw_l1int = w.wt_L1int;
        jhuw_l1Zgint = w.wt_L1Zgint;
        //cout << "weight found for event: " << eventID << endl;
	    break;
      }
    }
    if (jhuw_a1 == -1) cout << "Didn't find a match for event: " << eventID << " evt: " << evt << " lumi: " << lumi << endl;
    newtree->Fill();

  }

  final_dir->cd();
  final_dir->WriteTObject(newtree);
  delete newtree;
  foutput->Close();

}


int main(int argc, char* argv[]) {
  if ( argc != 4 ) {
    cout << "Usage: ./plot LHEFileName WeightFileName choiceOfReweighing" << endl;
    cout << "Exiting..." << endl;
    return -1;
  }
  TString LHEName = argv[1];
  TString weightFileName = argv[2];
  TString OutFile = argv[3];

  TFile *finput = new TFile(LHEName);//"TauTau_13_SKMD-skmd_mrgd_VBFHIGGS0M.root");//
  TTree *tree = (TTree*) finput->Get("tt/final/Ntuple");
  TH1D *nevents = (TH1D*) finput->Get("tt/eventCount");
  TH1D *sumW = (TH1D*) finput->Get("tt/summedWeights");

  cout << "Using LHE file: " << LHEName << endl;
  cout << "Reweight file:  " << weightFileName << endl;
  cout << "Grabbed input TTree: " << tree << " : " << tree->GetName() << endl;
  cout << "Grabbed TH1Ds:  " << nevents << " : " << sumW << endl;
  
  plot t(LHEName);
  t.ReadInWeights(weightFileName);
  t.Loop(OutFile,tree,nevents,sumW);

  delete tree;
  delete nevents;
  delete sumW;

  finput->Close();
  
  return 0;
}

