//#include "TFile.h"
//TGraph *graph = (TGraph*)gPad->GetPrimitive("Graph");

int QcdStudy() {

TFile *f = new TFile("dataTT.root","READ");
TTree *T = (TTree*)f->Get("Ntuple");

TCanvas *c1 = new TCanvas("c1","c1",600,600);
TPad *p1 = new TPad("p1","p1",0,0,1,1);
p1->Draw();
p1->cd();
//c1->cd(1);
//T->Draw("iso_1:iso_2>>hN(100,0,10,100,0,10)","(iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5)");
double binner[6] = { 0, 1, 3, 4.5, 6.5, 10 };
//for (auto bin : binner) {
//    cout << bin << endl;}
//TH1F *h2 = new TH1F("h2","h2",6,binner);
T->Draw("iso_1:iso_2>>hN(20,0,10,20,0,10)","(iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5)");
//T->Draw("iso_1>>h2(20,0,10)","(iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5)");
TH2F *hN = (TH2F*)gDirectory->Get("hN");
//TH1F *h2 = (TH1F*)gDirectory->Get("h2");
//TH2F *hnew2 = (TH2F*)hN->RebinX(5,"hnew2",binner);
//hN->SetStats(0);
//hN->RebinX( 5 );//, binner );
//hN->Rebin( 6, "reX", binner );
hN->Draw("colz");
//h2->Draw();
//hnew2->Draw();
//hN->SaveAs("tmp.root");
c1->SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/tmp.png");

//TTree *data = nullptr;
//*dataF.GetObject("Ntuple",data);
//
//data->Draw("iso_1")
//TH1F *htemp = (TH1F*)gPad->GetPrimitive("htemp");
//
//htemp->SaveAs("test.root")
return 1;
}
