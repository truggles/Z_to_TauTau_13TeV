// Original setup from:
//https://raw.githubusercontent.com/lovedeepkaursaini/aHVV_HTT/master/anaHTT.C
// 28 June 2017
//

#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <vector>
#include <fstream>
#include <cstdlib>
#include <iomanip>
#include "../interface/Mela.h"
#include "../interface/TUtil.hh"
//#include "ZZMatrixElement/MELA/interface/Mela.h"
#include "TMath.h"
#include "TLorentzVector.h"
#include "TLorentzRotation.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TString.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"


using namespace RooFit;
using namespace std;

void anaHTT(TString InFile, TString OutFile)
{
  int erg_tev=13;
  float mPOLE=125.6;
  float wPOLE=4.07e-3;
  
  TVar::VerbosityLevel verbosity = TVar::ERROR;
  Mela mela(erg_tev, mPOLE, verbosity);
  std::cout << "Starting!!!" << std::endl;
  std::cout << InFile << std::endl;

  
  TFile *finput = new TFile(InFile);//"TauTau_13_SKMD-skmd_mrgd_VBFHIGGS0M.root");//
//  TFile *finput = new TFile("all1234tmpOut2.root");
  TTree *tree = (TTree*) finput->Get("Ntuple");
  
  float ME_sm, ME_bsm, ME_bsm_mlt, KD_sm, KD_bsm, melaD0minus, ME_int, melaDCP,
        ME_sm_ggH, ME_bsm_ggH, ME_int_ggH,
        melaD0hplus, melaDint, melaDL1, melaDL1int, melaDL1Zg, melaDL1Zgint,
        melaD0minusggH, melaDCPggH,
        dPhi_jj, dPhiUnsigned_jj, dEta_jj,
        costhetastar, costheta1, costheta2, melaPhi, melaPhi1, Q2V1, Q2V2,
        sqrtQ2V1, sqrtQ2V2, avgSqrtQ2V12;
  
  Float_t         m_sv;
  Float_t         pt_sv;
  Float_t         eta_sv;
  Float_t         phi_sv;
  Float_t           njets;
  float jmass_1, jpt_1, jeta_1, jphi_1;
  float jmass_2, jpt_2, jeta_2, jphi_2;
  Float_t         pt_2;
  Float_t         phi_2;
  Float_t         eta_2;
  Float_t         m_2;
  Float_t         pt_1;
  Float_t         phi_1;
  Float_t         eta_1;
  Float_t         m_1;
  
  
  TBranch        *b_njets;   //!
  TBranch        *b_jpt_1;   //!
  TBranch        *b_jeta_1;   //!
  TBranch        *b_jphi_1;   //!
  TBranch        *b_jpt_2;   //!
  TBranch        *b_jeta_2;   //!
  TBranch        *b_jphi_2;   //!
  TBranch        *b_m_sv;   //!
  TBranch        *b_pt_sv;   //!
  TBranch        *b_eta_sv;   //!
  TBranch        *b_phi_sv;   //!
  TBranch        *b_pt_2;   //!
  TBranch        *b_phi_2;   //!
  TBranch        *b_eta_2;   //!
  TBranch        *b_m_2;   //!
  TBranch        *b_pt_1;   //!
  TBranch        *b_phi_1;   //!
  TBranch        *b_eta_1;   //!
  TBranch        *b_m_1;   //!
  
  tree->SetBranchAddress("jetVeto30", &njets, &b_njets);
  tree->SetBranchAddress("jpt_1", &jpt_1, &b_jpt_1);
  tree->SetBranchAddress("jeta_1", &jeta_1, &b_jeta_1);
  tree->SetBranchAddress("jphi_1", &jphi_1, &b_jphi_1);
  tree->SetBranchAddress("jpt_2", &jpt_2, &b_jpt_2);
  tree->SetBranchAddress("jeta_2", &jeta_2, &b_jeta_2);
  tree->SetBranchAddress("jphi_2", &jphi_2, &b_jphi_2);
  tree->SetBranchAddress("m_sv", &m_sv, &b_m_sv);
  tree->SetBranchAddress("pt_sv", &pt_sv, &b_pt_sv);
  tree->SetBranchAddress("eta_sv", &eta_sv, &b_eta_sv);
  tree->SetBranchAddress("phi_sv", &phi_sv, &b_phi_sv);
  tree->SetBranchAddress("pt_1", &pt_1, &b_pt_1);
  tree->SetBranchAddress("phi_1", &phi_1, &b_phi_1);
  tree->SetBranchAddress("eta_1", &eta_1, &b_eta_1);
  tree->SetBranchAddress("m_1", &m_1, &b_m_1);
  tree->SetBranchAddress("pt_2", &pt_2, &b_pt_2);
  tree->SetBranchAddress("phi_2", &phi_2, &b_phi_2);
  tree->SetBranchAddress("eta_2", &eta_2, &b_eta_2);
  tree->SetBranchAddress("m_2", &m_2, &b_m_2);

/*  tree->SetBranchStatus("*",0);
  tree->SetBranchStatus("m_sv",1);
  tree->SetBranchStatus("pt_sv",1);
  tree->SetBranchStatus("eta_sv",1);
  tree->SetBranchStatus("phi_sv",1);
*/
  TFile* foutput = new TFile(OutFile, "recreate");
//  TTree *newtree = tree->CloneTree();
//  newtree->SetName("TestTree"); 
  
  TTree* newtree = new TTree("TestTree", "");
  newtree = tree->CloneTree(0);
  newtree->Branch("melaD0minus", &melaD0minus);
  newtree->Branch("melaDCP", &melaDCP);
  newtree->Branch("melaD0hplus", &melaD0hplus);
  newtree->Branch("melaDint", &melaDint);
  newtree->Branch("melaDL1", &melaDL1);
  newtree->Branch("melaDL1int", &melaDL1int);
  newtree->Branch("melaDL1Zg", &melaDL1Zg);
  newtree->Branch("melaDL1Zgint", &melaDL1Zgint);
  newtree->Branch("melaD0minusggH", &melaD0minusggH);
  newtree->Branch("melaDCPggH", &melaDCPggH);
  newtree->Branch("melaDPhijj", &dPhi_jj);
  newtree->Branch("melaDPhiUnsignedjj", &dPhiUnsigned_jj);
  newtree->Branch("melaDEtajj", &dEta_jj);
  newtree->Branch("melacosthetastar", &costhetastar);
  newtree->Branch("melacostheta1", &costheta1);
  newtree->Branch("melacostheta2", &costheta2);
  newtree->Branch("melaPhi", &melaPhi);
  newtree->Branch("melaPhi1", &melaPhi1);
  newtree->Branch("melaQ2V1", &Q2V1);
  newtree->Branch("melaQ2V2", &Q2V2);
  newtree->Branch("melaSqrtQ2V1", &sqrtQ2V1);
  newtree->Branch("melaSqrtQ2V2", &sqrtQ2V2);
  newtree->Branch("melaAvgSqrtQ2V12", &avgSqrtQ2V12);



  //  mela.setCandidateDecayMode(TVar::CandidateDecay_ff);
  mela.setCandidateDecayMode(TVar::CandidateDecay_Stable);
  
 
  Long64_t nentries = tree->GetEntries();
  int recorded=0;
  
  Long64_t nbytes = 0, nb = 0;
  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    if ( jentry % 100 == 0 ) std::cout << jentry << std::endl;
    nb = tree->GetEntry(jentry);   nbytes += nb;
    
    tree->GetEntry(jentry);
    melaD0hplus = -9;
    melaDint = -9;
    melaDL1 = -9;
    melaDL1int = -9;
    melaDL1Zg = -9;
    melaDL1Zgint = -9;
    melaD0minus = -9;
    melaDCP = -9;
    melaD0minusggH = -9;
    melaDCPggH = -9;
    dPhi_jj = -9;
    dPhiUnsigned_jj = -9;
    dEta_jj = -19;
    costhetastar = -9;
    costheta1 = -9;
    costheta2 = -9;
    melaPhi = -9;
    melaPhi1 = -9;
    Q2V1 = -9;
    Q2V2 = -9;
    sqrtQ2V1 = -9;
    sqrtQ2V2 = -9;
    avgSqrtQ2V12 = -9;
    
    if (njets>=2){
      TLorentzVector jet1(0, 0, 1e-3, 1e-3), jet2(0, 0, 1e-3, 1e-3), higgs(0, 0, 0, 0),
        blank1(0, 0, 0, 0);
      jet1.SetPtEtaPhiM(jpt_1, jeta_1, jphi_1, 0);
      jet2.SetPtEtaPhiM(jpt_2, jeta_2, jphi_2, 0);
      higgs.SetPtEtaPhiM(pt_sv, eta_sv, phi_sv, m_sv);
      TVector3 boostH = higgs.BoostVector();

      SimpleParticleCollection_t associated;
      associated.push_back(SimpleParticle_t(0, jet1));
      associated.push_back(SimpleParticle_t(0, jet2));

      TLorentzVector pDaughters1, pDaughters2;
      //     std::vector<TLorentzVector> daus = mela.calculate4Momentum(m_sv, m1, m2, acos(hs), acos(h1), acos(h2), phi1, phi);
      pDaughters1.SetPtEtaPhiM(pt_1, eta_1, phi_1, m_1);
      pDaughters1.SetPtEtaPhiM(pt_2, eta_2, phi_2, m_2);
      
      SimpleParticleCollection_t daughters_ZZ;
      daughters_ZZ.push_back(SimpleParticle_t(25, higgs));
      // daughters_ZZ.push_back(SimpleParticle_t(13, pDaughters1));
      // daughters_ZZ.push_back(SimpleParticle_t(15, pDaughters2));
      mela.setInputEvent(&daughters_ZZ, &associated, (SimpleParticleCollection_t*)0, false);

      //get ME scalar
      mela.setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::JJVBF);
      mela.computeProdP(ME_sm, false);

      //get ME bsm
      mela.setProcess(TVar::H0minus, TVar::JHUGen, TVar::JJVBF);
      mela.computeProdP(ME_bsm, false);
      ME_bsm_mlt = ME_bsm*pow(0.297979, 2);
      //compute D_BSM (eq.5 of HIG-17-011)
      KD_bsm = ME_sm / (ME_sm + ME_bsm);
      melaD0minus = ME_sm / (ME_sm + ME_bsm_mlt);

        
      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
      mela.selfDHzzcoupl[0][gHIGGS_VV_4][0]=1;
      mela.selfDHzzcoupl[0][gHIGGS_VV_1][0]=1;
      mela.computeProdP(ME_int, false);

      //define D_CP
      melaDCP = (0.297979*(ME_int-(ME_sm + ME_bsm)))/(ME_sm + (pow(0.297979, 2)*ME_bsm));
      
      // New from Heshy: 22, Nov 2017
      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
      mela.selfDHzzcoupl[0][gHIGGS_VV_2][0]=1;
      mela.computeProdP(ME_bsm, false);
      ME_bsm_mlt = ME_bsm*pow(0.271899, 2);
      melaD0hplus = ME_sm / (ME_sm + ME_bsm_mlt);

      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
      mela.selfDHzzcoupl[0][gHIGGS_VV_2][0]=1;
      mela.selfDHzzcoupl[0][gHIGGS_VV_1][0]=1;
      mela.computeProdP(ME_int, false);
      melaDint = (0.271899*(ME_int-(ME_sm + ME_bsm)))/(ME_sm + (pow(0.271899, 2)*ME_bsm));


      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
      mela.selfDHzzcoupl[0][gHIGGS_VV_1_PRIME2][0]=1;
      mela.computeProdP(ME_bsm, false);
      ME_bsm_mlt = ME_bsm*pow(2156.43, 2);
      melaDL1 = ME_sm / (ME_sm + ME_bsm_mlt);

      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
      mela.selfDHzzcoupl[0][gHIGGS_VV_1_PRIME2][0]=1;
      mela.selfDHzzcoupl[0][gHIGGS_VV_1][0]=1;
      mela.computeProdP(ME_int, false);
      melaDL1int = (2156.43*(ME_int-(ME_sm + ME_bsm)))/(ME_sm + (pow(2156.43, 2)*ME_bsm));

      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
      mela.selfDHzzcoupl[0][gHIGGS_ZA_1_PRIME2][0]=1;
      mela.computeProdP(ME_bsm, false);
      ME_bsm_mlt = ME_bsm*pow(4091.0, 2);
      melaDL1Zg = ME_sm / (ME_sm + ME_bsm_mlt);

      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
      mela.selfDHzzcoupl[0][gHIGGS_ZA_1_PRIME2][0]=1;
      mela.selfDHzzcoupl[0][gHIGGS_VV_1][0]=1;
      mela.computeProdP(ME_int, false);
      melaDL1Zgint = (4091.0*(ME_int-(ME_sm + ME_bsm)))/(ME_sm + (pow(4091.0, 2)*ME_bsm));
 
      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJQCD);
      mela.selfDHggcoupl[0][gHIGGS_GG_2][0]=1;
      mela.computeProdP(ME_sm_ggH, false);
      
      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJQCD);
      mela.selfDHggcoupl[0][gHIGGS_GG_4][0]=1;
      mela.computeProdP(ME_bsm_ggH, false);
      
      melaD0minusggH = ME_sm_ggH / (ME_sm_ggH + ME_bsm_ggH);
      
      mela.setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJQCD);
      mela.selfDHggcoupl[0][gHIGGS_GG_2][0]=1;
      mela.selfDHggcoupl[0][gHIGGS_GG_4][0]=1;
      mela.computeProdP(ME_int_ggH, false);
      
      melaDCPggH = (ME_int_ggH-(ME_sm_ggH + ME_bsm_ggH))/(ME_sm_ggH + ME_bsm_ggH);

      

      if (jet1.Pz() <= jet2.Pz()) {
        dPhi_jj = jet1.DeltaPhi(jet2);
      }
      else {
        dPhi_jj = jet2.DeltaPhi(jet1);
      }
      dPhiUnsigned_jj = jet1.DeltaPhi(jet2);
      dEta_jj = jet1.Eta()-jet2.Eta();

      // See: https://github.com/usarica/HiggsAnalysis-ZZMatrixElement/blob/newVH/MELA/interface/TUtil.hh#L106-L122
      TUtil::computeVBFangles( 
        costhetastar, costheta1, costheta2, melaPhi, melaPhi1, Q2V1, Q2V2,
        higgs, 25,
        blank1, -9000,
        blank1, -9000,
        blank1, -9000,
        jet1, 0,
        jet2, 0
      );

      sqrtQ2V1 = TMath::Sqrt( Q2V1 );
      sqrtQ2V2 = TMath::Sqrt( Q2V2 );
      avgSqrtQ2V12 = (sqrtQ2V1 + sqrtQ2V2) / 2.;

    }
    newtree->Fill();
    recorded++;
    mela.resetInputEvent();
  }
//  foutput->Write();
  foutput->WriteTObject(newtree);
//  delete tree;
  delete newtree;
  foutput->Close();
  finput->Close();
}

void runAll() {
 std::vector<std::string> files;
 //files.push_back("");
 files.push_back("DYJets1Low_0_tt");
 files.push_back("DYJets1_0_tt");
 files.push_back("DYJets1_1_tt");
 files.push_back("DYJets1_2_tt");
 files.push_back("DYJets1_3_tt");
 files.push_back("DYJets1_4_tt");
 files.push_back("DYJets1_5_tt");
 files.push_back("DYJets1_6_tt");
 files.push_back("DYJets2Low_0_tt");
 files.push_back("DYJets2_0_tt");
 files.push_back("DYJets2_1_tt");
 files.push_back("DYJets2_2_tt");
 files.push_back("DYJets3_0_tt");
 files.push_back("DYJets4_0_tt");
 files.push_back("DYJetsLow_0_tt");
 files.push_back("DYJets_0_tt");
 files.push_back("DYJets_10_tt");
 files.push_back("DYJets_11_tt");
 files.push_back("DYJets_1_tt");
 files.push_back("DYJets_2_tt");
 files.push_back("DYJets_3_tt");
 files.push_back("DYJets_4_tt");
 files.push_back("DYJets_5_tt");
 files.push_back("DYJets_6_tt");
 files.push_back("DYJets_7_tt");
 files.push_back("DYJets_8_tt");
 files.push_back("DYJets_9_tt");
 files.push_back("EWKWMinus_0_tt");
 files.push_back("EWKWPlus_0_tt");
 files.push_back("EWKZ2l_0_tt");
 files.push_back("EWKZ2nu_0_tt");
 files.push_back("HtoWW2l2nu125_0_tt");
 files.push_back("T-tW_0_tt");
 files.push_back("T-tchan_0_tt");
 files.push_back("T-tchan_1_tt");
 files.push_back("TT_0_tt");
 files.push_back("TT_1_tt");
 files.push_back("TT_2_tt");
 files.push_back("TT_3_tt");
 files.push_back("TT_4_tt");
 files.push_back("Tbar-tW_0_tt");
 files.push_back("Tbar-tchan_0_tt");
 files.push_back("VBFHtoTauTau0L1125_0_tt");
 files.push_back("VBFHtoTauTau0L1125_1_tt");
 files.push_back("VBFHtoTauTau0L1125_2_tt");
 files.push_back("VBFHtoTauTau0L1125_3_tt");
 files.push_back("VBFHtoTauTau0L1f05ph0125_0_tt");
 files.push_back("VBFHtoTauTau0L1f05ph0125_1_tt");
 files.push_back("VBFHtoTauTau0L1f05ph0125_2_tt");
 files.push_back("VBFHtoTauTau0M125_0_tt");
 files.push_back("VBFHtoTauTau0M125_1_tt");
 files.push_back("VBFHtoTauTau0M125_2_tt");
 files.push_back("VBFHtoTauTau0M125_3_tt");
 files.push_back("VBFHtoTauTau0Mf05ph0125_0_tt");
 files.push_back("VBFHtoTauTau0Mf05ph0125_1_tt");
 files.push_back("VBFHtoTauTau0PH125_0_tt");
 files.push_back("VBFHtoTauTau0PH125_1_tt");
 files.push_back("VBFHtoTauTau0PH125_2_tt");
 files.push_back("VBFHtoTauTau0PHf05ph0125_0_tt");
 files.push_back("VBFHtoTauTau0PHf05ph0125_1_tt");
 files.push_back("VBFHtoTauTau0PM125_0_tt");
 files.push_back("VBFHtoTauTau0PM125_1_tt");
 files.push_back("VBFHtoTauTau125_0_tt");
 files.push_back("VBFHtoTauTau125_1_tt");
 files.push_back("VBFHtoTauTau125_2_tt");
 files.push_back("VBFHtoWW2l2nu125_0_tt");
 files.push_back("VV_0_tt");
 files.push_back("VV_1_tt");
 files.push_back("WHtoTauTau0L1125_0_tt");
 files.push_back("WHtoTauTau0L1125_1_tt");
 files.push_back("WHtoTauTau0L1125_2_tt");
 files.push_back("WHtoTauTau0L1f05ph0125_0_tt");
 files.push_back("WHtoTauTau0L1f05ph0125_1_tt");
 files.push_back("WHtoTauTau0L1f05ph0125_2_tt");
 files.push_back("WHtoTauTau0M125_0_tt");
 files.push_back("WHtoTauTau0M125_1_tt");
 files.push_back("WHtoTauTau0M125_2_tt");
 files.push_back("WHtoTauTau0Mf05ph0125_0_tt");
 files.push_back("WHtoTauTau0Mf05ph0125_1_tt");
 files.push_back("WHtoTauTau0PH125_0_tt");
 files.push_back("WHtoTauTau0PH125_1_tt");
 files.push_back("WHtoTauTau0PH125_2_tt");
 files.push_back("WHtoTauTau0PHf05ph0125_0_tt");
 files.push_back("WHtoTauTau0PHf05ph0125_1_tt");
 files.push_back("WHtoTauTau0PHf05ph0125_2_tt");
 files.push_back("WHtoTauTau0PM125_0_tt");
 files.push_back("WJets1_0_tt");
 files.push_back("WJets2_0_tt");
 files.push_back("WJets2_1_tt");
 files.push_back("WJets3_0_tt");
 files.push_back("WJets3_1_tt");
 files.push_back("WJets3_2_tt");
 files.push_back("WJets4_0_tt");
 files.push_back("WJets4_1_tt");
 files.push_back("WJets_0_tt");
 files.push_back("WJets_1_tt");
 files.push_back("WMinusHTauTau125_0_tt");
 files.push_back("WPlusHTauTau125_0_tt");
 files.push_back("WW1l1nu2q_0_tt");
 files.push_back("WWW_0_tt");
 files.push_back("WZ1l1nu2q_0_tt");
 files.push_back("WZ1l1nu2q_1_tt");
 files.push_back("WZ1l3nu_0_tt");
 files.push_back("WZ2l2q_0_tt");
 files.push_back("WZ2l2q_1_tt");
 files.push_back("WZ2l2q_2_tt");
 files.push_back("WZ2l2q_3_tt");
 files.push_back("WZ2l2q_4_tt");
 files.push_back("WZ3l1nu_0_tt");
 files.push_back("ZHTauTau125_0_tt");
 files.push_back("ZHtoTauTau0L1125_0_tt");
 files.push_back("ZHtoTauTau0L1125_1_tt");
 files.push_back("ZHtoTauTau0L1125_2_tt");
 files.push_back("ZHtoTauTau0L1f05ph0125_0_tt");
 files.push_back("ZHtoTauTau0L1f05ph0125_1_tt");
 files.push_back("ZHtoTauTau0M125_0_tt");
 files.push_back("ZHtoTauTau0M125_1_tt");
 files.push_back("ZHtoTauTau0M125_2_tt");
 files.push_back("ZHtoTauTau0Mf05ph0125_0_tt");
 files.push_back("ZHtoTauTau0Mf05ph0125_1_tt");
 files.push_back("ZHtoTauTau0PH125_0_tt");
 files.push_back("ZHtoTauTau0PH125_1_tt");
 files.push_back("ZHtoTauTau0PH125_2_tt");
 files.push_back("ZHtoTauTau0PHf05ph0125_0_tt");
 files.push_back("ZHtoTauTau0PHf05ph0125_1_tt");
 files.push_back("ZHtoTauTau0PHf05ph0125_2_tt");
 files.push_back("ZHtoTauTau0PM125_0_tt");
 files.push_back("ZHtoTauTau0PM125_1_tt");
 files.push_back("ZZ2l2q_0_tt");
 files.push_back("ZZ2l2q_1_tt");
 files.push_back("ZZ2l2q_2_tt");
 files.push_back("ZZ2l2q_3_tt");
 files.push_back("ZZ4l_0_tt");
 files.push_back("ZZ4l_1_tt");
 files.push_back("dataTT-B_0_tt");
 files.push_back("dataTT-B_10_tt");
 files.push_back("dataTT-B_11_tt");
 files.push_back("dataTT-B_12_tt");
 files.push_back("dataTT-B_13_tt");
 files.push_back("dataTT-B_14_tt");
 files.push_back("dataTT-B_15_tt");
 files.push_back("dataTT-B_1_tt");
 files.push_back("dataTT-B_2_tt");
 files.push_back("dataTT-B_3_tt");
 files.push_back("dataTT-B_4_tt");
 files.push_back("dataTT-B_5_tt");
 files.push_back("dataTT-B_6_tt");
 files.push_back("dataTT-B_7_tt");
 files.push_back("dataTT-B_8_tt");
 files.push_back("dataTT-B_9_tt");
 files.push_back("dataTT-C_0_tt");
 files.push_back("dataTT-C_1_tt");
 files.push_back("dataTT-C_2_tt");
 files.push_back("dataTT-C_3_tt");
 files.push_back("dataTT-C_4_tt");
 files.push_back("dataTT-C_5_tt");
 files.push_back("dataTT-C_6_tt");
 files.push_back("dataTT-C_7_tt");
 files.push_back("dataTT-D_0_tt");
 files.push_back("dataTT-D_10_tt");
 files.push_back("dataTT-D_11_tt");
 files.push_back("dataTT-D_12_tt");
 files.push_back("dataTT-D_13_tt");
 files.push_back("dataTT-D_1_tt");
 files.push_back("dataTT-D_2_tt");
 files.push_back("dataTT-D_3_tt");
 files.push_back("dataTT-D_4_tt");
 files.push_back("dataTT-D_5_tt");
 files.push_back("dataTT-D_6_tt");
 files.push_back("dataTT-D_7_tt");
 files.push_back("dataTT-D_8_tt");
 files.push_back("dataTT-D_9_tt");
 files.push_back("dataTT-E_0_tt");
 files.push_back("dataTT-E_10_tt");
 files.push_back("dataTT-E_11_tt");
 files.push_back("dataTT-E_12_tt");
 files.push_back("dataTT-E_1_tt");
 files.push_back("dataTT-E_2_tt");
 files.push_back("dataTT-E_3_tt");
 files.push_back("dataTT-E_4_tt");
 files.push_back("dataTT-E_5_tt");
 files.push_back("dataTT-E_6_tt");
 files.push_back("dataTT-E_7_tt");
 files.push_back("dataTT-E_8_tt");
 files.push_back("dataTT-E_9_tt");
 files.push_back("dataTT-F_0_tt");
 files.push_back("dataTT-F_1_tt");
 files.push_back("dataTT-F_2_tt");
 files.push_back("dataTT-F_3_tt");
 files.push_back("dataTT-F_4_tt");
 files.push_back("dataTT-F_5_tt");
 files.push_back("dataTT-F_6_tt");
 files.push_back("dataTT-F_7_tt");
 files.push_back("dataTT-F_8_tt");
 files.push_back("dataTT-F_9_tt");
 files.push_back("dataTT-G_0_tt");
 files.push_back("dataTT-G_10_tt");
 files.push_back("dataTT-G_11_tt");
 files.push_back("dataTT-G_12_tt");
 files.push_back("dataTT-G_13_tt");
 files.push_back("dataTT-G_14_tt");
 files.push_back("dataTT-G_15_tt");
 files.push_back("dataTT-G_16_tt");
 files.push_back("dataTT-G_17_tt");
 files.push_back("dataTT-G_18_tt");
 files.push_back("dataTT-G_19_tt");
 files.push_back("dataTT-G_1_tt");
 files.push_back("dataTT-G_20_tt");
 files.push_back("dataTT-G_21_tt");
 files.push_back("dataTT-G_2_tt");
 files.push_back("dataTT-G_3_tt");
 files.push_back("dataTT-G_4_tt");
 files.push_back("dataTT-G_5_tt");
 files.push_back("dataTT-G_6_tt");
 files.push_back("dataTT-G_7_tt");
 files.push_back("dataTT-G_8_tt");
 files.push_back("dataTT-G_9_tt");
 files.push_back("dataTT-H_0_tt");
 files.push_back("dataTT-H_10_tt");
 files.push_back("dataTT-H_11_tt");
 files.push_back("dataTT-H_12_tt");
 files.push_back("dataTT-H_13_tt");
 files.push_back("dataTT-H_14_tt");
 files.push_back("dataTT-H_15_tt");
 files.push_back("dataTT-H_16_tt");
 files.push_back("dataTT-H_17_tt");
 files.push_back("dataTT-H_18_tt");
 files.push_back("dataTT-H_19_tt");
 files.push_back("dataTT-H_1_tt");
 files.push_back("dataTT-H_2_tt");
 files.push_back("dataTT-H_3_tt");
 files.push_back("dataTT-H_4_tt");
 files.push_back("dataTT-H_5_tt");
 files.push_back("dataTT-H_6_tt");
 files.push_back("dataTT-H_7_tt");
 files.push_back("dataTT-H_8_tt");
 files.push_back("dataTT-H_9_tt");
 files.push_back("ggHtoTauTau-maxmix125_0_tt");
 files.push_back("ggHtoTauTau-pseudoscalar125_0_tt");
 files.push_back("ggHtoTauTau-sm125_0_tt");
 files.push_back("ggHtoTauTau125_0_tt");
 files.push_back("ggHtoTauTau125_1_tt");
 files.push_back("ttHTauTau125_0_tt");

 std::string base = "/afs/cern.ch/work/t/truggles/Z_to_tautau/CMSSW_8_0_25/src/Z_to_TauTau_13TeV/htt2Jan07NewMela/";

 for(auto file : files ){
    std::cout << file << std::endl;
    anaHTT( base+file+".root", "mela/"+file+".root");    
 }
}

