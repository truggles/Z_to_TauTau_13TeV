//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Dec  4 12:59:33 2017 by ROOT version 6.06/08
// from TTree HTT/Reweighing
// found on file: VBFHiggs0PM_M-125_13TeV-JHUGenV6.root
//////////////////////////////////////////////////////////

#ifndef plot_h
#define plot_h

#include <TROOT.h>
#include <TH1F.h>
#include <TChain.h>
#include <TFile.h>
#include <TString.h>

// Header file for the classes stored in the TTree if any.
#include "vector"

using namespace std;

class weights {
public:
  Long64_t eventID;
  Double_t wt_a1, wt_a2, wt_a3, wt_L1, wt_L1Zg, wt_a1a2, wt_a1a3;
  Double_t wt_a1L1, wt_a1L1Zg, wt_a3int, wt_a2int, wt_L1int, wt_L1Zgint;
};  


class plot {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           run;
   Int_t        evt;
   Int_t           lumi;
   //Int_t           npart;
   //vector<int>     *gen_pdgid;
   //vector<int>     *gen_status;
   //vector<double>  *gen_pt;
   //vector<double>  *gen_eta;
   //vector<double>  *gen_phi;

   std::vector<weights> ws_;
   
   // List of branches
   TBranch        *b_run;   //!
   TBranch        *b_evt;   //!
   TBranch        *b_lumi;   //!
   //TBranch        *b_npart;   //!
   //TBranch        *b_gen_pdgid;   //!
   //TBranch        *b_gen_status;   //!
   //TBranch        *b_gen_pt;   //!
   //TBranch        *b_gen_eta;   //!
   //TBranch        *b_gen_phi;   //!

   plot(TString name);
   virtual ~plot();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(TString OutFile, TTree *oldtree, TH1D *hnevents, TH1D *sumW);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);

   virtual void     ReadInWeights(TString name);
};

#endif

#ifdef plot_cxx
plot::plot(TString nameOfFile) 
{

  TTree* tree = nullptr;
  // if parameter tree is not specified (or zero), connect the file
  // used to generate this class and read the Tree.
  
  TFile* f = new TFile(nameOfFile);
  //TDirectory * dir = (TDirectory*)f->Get(nameOfFile + ":/myana");
  f->GetObject("mutau_tree",tree);

  Init(tree);
}

plot::~plot()
{
   //if (!fChain) return;
   //delete fChain->GetCurrentFile();
}

Int_t plot::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t plot::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void plot::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   //gen_pdgid = 0;
   //gen_status = 0;
   //gen_pt = 0;
   //gen_eta = 0;
   //gen_phi = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("evt", &evt, &b_evt);
   fChain->SetBranchAddress("lumi", &lumi, &b_lumi);
   //fChain->SetBranchAddress("npart", &npart, &b_npart);
   //fChain->SetBranchAddress("gen_pdgid", &gen_pdgid, &b_gen_pdgid);
   //fChain->SetBranchAddress("gen_status", &gen_status, &b_gen_status);
   //fChain->SetBranchAddress("gen_pt", &gen_pt, &b_gen_pt);
   //fChain->SetBranchAddress("gen_eta", &gen_eta, &b_gen_eta);
   //fChain->SetBranchAddress("gen_phi", &gen_phi, &b_gen_phi);
   Notify();
}

Bool_t plot::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void plot::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t plot::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef plot_cxx

