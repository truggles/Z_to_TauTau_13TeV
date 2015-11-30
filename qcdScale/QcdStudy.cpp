//#include "TFile.h"
//TGraph *graph = (TGraph*)gPad->GetPrimitive("Graph");

std::vector< std::vector< double >> binCounts( TH2F *hist ) {
//double* binCounts( TH2F *hist ) {
    //int nBins = hist->GetXaxis()->GenNbins();
    //std::vector< std::vector< double >> vals(5, std::vector< double >( 5 ));
    std::vector< std::vector< double >> vals;
    //double vals[5][5];
    double nBins = 20.;
    double bottom = 0.;
    double top = 10.;
    double xPerBin = ( top - bottom ) / nBins;
    cout << "xPerBin: " << xPerBin << endl;
    double spacing[6] = { 0, 1, 3, 4.5, 6.5, 10 }; 
    double bins[6]; 
    for (int i = 0; i< 6; i++) {
        bins[i] = spacing[i] / xPerBin;
    }
    //cout << bins[3] << endl;
    int tot = 0;
    for (int i = 0; i< 5; i++) {
        vals.push_back( std::vector< double >() );
        //vals.push_back( );
        for (int j = 0; j< 5; j++) {
            //vals[i][j] = hist->Integral( bins[i], bins[i+1], bins[j], bins[j+1] );
            vals.back().push_back( hist->Integral( bins[i+1], bins[i+2], bins[j+1], bins[j+2] ) );
            //vals[i][j] = hist->Integral( bins[i], bins[i+1], bins[j], bins[j+1] );
            cout << "Bin["<<i<<"]["<<j<<"] "<<vals[i][j] << endl;
            tot += vals[i][j];
        }
    }
    cout << "Total Integral = " << hist->Integral();
    cout << "Finished; total = " << tot << endl;
    return vals;
}

int QcdStudy() {

TFile *fd = new TFile("dataTT.root","READ");
TTree *Td = (TTree*)fd->Get("Ntuple");
TFile *fmc = new TFile("mcTT.root","READ");
TTree *Tmc = (TTree*)fmc->Get("Ntuple");

TCanvas *c1 = new TCanvas("c1","c1",600,600);
TPad *p1 = new TPad("p1","p1",0,0,1,1);
p1->Draw();
p1->cd();
const char* iso = "(iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5)";
//const char* XSec = "*( (GenWeight/abs(GenWeight)) * XSecLumiWeight * puweight )";
//T->Draw("iso_1:iso_2>>hData(20,0,10,20,0,10)","(iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5)");
Td->Draw("iso_1:iso_2>>hData(20,0,10,20,0,10)",iso);
TH2F *hData = (TH2F*)gDirectory->Get("hData");


std::vector< std::vector< double >> vals = binCounts( hData );
//double* vals = binCounts( hData );
cout << vals[0][0] << endl;

//cout << hData->Integral( 1, 2, 1, 2 ) << endl;
//cout << vals[0][0] << endl;
//TH1F *h2 = (TH1F*)gDirectory->Get("h2");
//TH2F *hnew2 = (TH2F*)hData->RebinX(5,"hnew2",binner);
//hData->SetStats(0);
//hData->RebinX( 5 );//, binner );
//hData->Rebin( 6, "reX", binner );
hData->Draw("colz");
//h2->Draw();
//hnew2->Draw();
//hData->SaveAs("tmp.root");
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
