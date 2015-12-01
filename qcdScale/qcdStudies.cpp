
void addDetails( TH2F* hist ) {
    hist->SetStats(0);
    hist->GetXaxis()->SetTitle("Leading #tau_{h} DBIsoRawComb3Hits");
    hist->GetYaxis()->SetTitle("Secondary #tau_{h} DBIsoRawComb3Hits");
    return void();
}

int QcdStudy() {

    //0 double spacingX[6] = { 0, 1, 3, 4.5, 6.5, 10 }; 
    //0 double spacingY[6] = { 0, 1, 3, 4.5, 7.5, 10 }; 
    //1 double spacingX[6] = { 0, 1, 3, 5, 7, 10 }; 
    //1 double spacingY[6] = { 0, 1, 3, 5, 7, 10 }; 
    double spacingX[6] = { 0, 1, 3, 4.5, 7, 10 }; 
    double spacingY[6] = { 0, 1, 3, 4.5, 7, 10 }; 
    
    TFile *fd = new TFile("dataTT.root","READ");
    TTree *Td = (TTree*)fd->Get("Ntuple");
    TFile *fmc = new TFile("mcTT.root","READ");
    TTree *Tmc = (TTree*)fmc->Get("Ntuple");
    TFile *fqcd = new TFile("qcdTT.root","READ");
    TTree *Tqcd = (TTree*)fqcd->Get("Ntuple");
    
    const char* iso = "((iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5))";
    const char* XSec = "*( (GenWeight/abs(GenWeight)) * XSecLumiWeight * puweight )";
    //const char* isoMC = "((iso_1 > 3 || t1ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) && ( iso_2 > 3 || t2ByTightCombinedIsolationDeltaBetaCorr3Hits > 0.5))*( (GenWeight/abs(GenWeight)) * XSecLumiWeight * puweight )";
    //const char* qcd = "*( BkgGroup == 5 )";
    //const char* nonQcd = "*( BkgGroup < 5 )";
    char isoMC[230];
    strcpy(isoMC,iso);
    strcat(isoMC,XSec);
    std::vector<const char *> cuts;
    //std::vector<std::string> cuts;
    cuts.push_back("(Z_SS==1)");
    cuts.push_back("(Z_SS==0)");
    int count = 0;
    for ( auto cut : cuts ) {
        count += 1;
        char dataCut[256];
        char mcCut[256];
        strcpy(dataCut,iso);
        strcat(dataCut,"*");
        strcat(dataCut,cut);
        strcpy(mcCut,mcCut);
        strcat(mcCut,"*");
        strcat(mcCut,cut);
        cout << dataCut << ":" << mcCut <<endl;
        TCanvas *c2 = new TCanvas("c2","c2",800,800);
        TPad *p2 = new TPad("p2","p2",0,0,1,1);
        p2->Divide(2,2);
        p2->Draw();
        p2->cd(1);
        TH2F *hData = new TH2F("hData","hData",5,spacingX,5,spacingY);
        Td->Draw("iso_1:iso_2>>hData",dataCut);
        addDetails( hData );
        hData->Draw("colz text");
        p2->cd(2);
        TH2F *hMC = new TH2F("hMC","hMC",5,spacingX,5,spacingY);
        Tmc->Draw("iso_1:iso_2>>hMC",mcCut);
        addDetails( hMC );
        hMC->Draw("colz text");
        p2->cd(3);
        TH2F *hQCDmc = new TH2F("hQCDmc","hQCDmc",5,spacingX,5,spacingY);
        Tqcd->Draw("iso_1:iso_2>>hQCDmc",mcCut);
        addDetails( hQCDmc );
        hQCDmc->Draw("colz text");
        p2->cd(4);
        TH2F *hQCDdd = new TH2F("hQCDdd","hQCDdd",5,spacingX,5,spacingY);
        hQCDdd->Add( hData );
        TH2F *mcInv = (TH2F*) hMC->Clone();
        mcInv->Scale( -1 );
        hQCDdd->Add( mcInv );
        addDetails( hQCDdd );
        hQCDdd->Draw("colz text");
        char save1[256];
        strcpy(save1,"/afs/cern.ch/user/t/truggles/www/qcdScale/qcd");
        strcat(save1, cut);
        strcat(save1, ".png");
        char save2[256];
        strcpy(save2,"/afs/cern.ch/user/t/truggles/www/qcdScale/ratio");
        strcat(save2, cut);
        strcat(save2, ".png");
        //cout << save << endl;
        c2->SaveAs( save1 );
        //c2->SaveAs("/afs/cern.ch/user/t/truggles/www/qcdScale/qcd%s.png" % std::to_string(count) );
        
        TCanvas *c3 = new TCanvas("c3","c3",800,800);
        TPad *p3 = new TPad("p3","p3",0,0,1,1);
        p3->Draw();
        p3->cd();
        TH2F *ratio = new TH2F("ratio","ratio",5,spacingX,5,spacingY);
        ratio->Add( hQCDdd );
        ratio->Divide( hData );
        addDetails( ratio );
        ratio->Draw("colz text");
        c3->SaveAs( save2 );
        delete hData;
        delete hMC;
        delete hQCDmc;
        delete hQCDdd;
        delete c2;
        delete c3;
        delete ratio;
        strcpy(dataCut,"");
        strcpy(mcCut,"");
    }   
    return 1;
}
