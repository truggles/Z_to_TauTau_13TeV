import ROOT

cutMap = {
    'eeet' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    'emmt' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    'eemt' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || mPFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((iso_3 < 0.15 && mPFIDLoose > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((iso_3 > 0.15 || mPFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    'mmmt' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || m3PFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((iso_3 < 0.15 && m3PFIDLoose > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((iso_3 > 0.15 || m3PFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    'eett' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((byMediumIsolationMVArun2v1DBoldDMwLT_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    'mmtt' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((byMediumIsolationMVArun2v1DBoldDMwLT_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    'eeem' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 < 0.15 && mPFIDLoose > 0.5))*zhFR1 + ((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(iso_4 > 0.15 || mPFIDLoose < 0.5))*zhFR2 - ((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 > 0.15 || mPFIDLoose < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
    'emmm' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 < 0.15 && m3PFIDLoose > 0.5))*zhFR1 + ((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(iso_4 > 0.15 || m3PFIDLoose < 0.5))*zhFR2 - ((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 > 0.15 || m3PFIDLoose < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
}

cutMap2 = {
}
fractions = {
    'emmm' : {
        'total' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 < 0.15 && m3PFIDLoose > 0.5))*zhFR1 + ((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(iso_4 > 0.15 || m3PFIDLoose < 0.5))*zhFR2 - ((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 > 0.15 || m3PFIDLoose < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
        'one' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 < 0.15 && m3PFIDLoose > 0.5))*zhFR1)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
        'two' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 < 0.15 && m3PFIDLoose > 0.5))*zhFR1 + ((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(iso_4 > 0.15 || m3PFIDLoose < 0.5))*zhFR2 - ((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 > 0.15 || m3PFIDLoose < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
        'zero' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 > 0.15 || m3PFIDLoose < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
    },
    'eeem' : {
        'total' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 < 0.15 && mPFIDLoose > 0.5))*zhFR1 + ((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(iso_4 > 0.15 || mPFIDLoose < 0.5))*zhFR2 - ((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 > 0.15 || mPFIDLoose < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
        'one' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 < 0.15 && mPFIDLoose > 0.5))*zhFR1)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
        'two' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(iso_4 > 0.15 || mPFIDLoose < 0.5))*zhFR2)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
        'zero' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(iso_4 > 0.15 || mPFIDLoose < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(LT_higgs > 20)',
    },
    'mmtt' : {
        'total' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((byMediumIsolationMVArun2v1DBoldDMwLT_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'one' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'two' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'zero' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    },
    'eett' : {
        'total' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((byMediumIsolationMVArun2v1DBoldDMwLT_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'one' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'two' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'zero' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((byMediumIsolationMVArun2v1DBoldDMwLT_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    },
    'mmmt' : {
        'total' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || m3PFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((iso_3 < 0.15 && m3PFIDLoose > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((iso_3 > 0.15 || m3PFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'one' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || m3PFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'two' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 < 0.15 && m3PFIDLoose > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'zero' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || m3PFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    },
    'eemt' : {
        'total' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || mPFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((iso_3 < 0.15 && mPFIDLoose > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((iso_3 > 0.15 || mPFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'one' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || mPFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'two' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*((((((iso_3 < 0.15 && mPFIDLoose > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2))))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'zero' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || mPFIDLoose < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    },
    'emmt' : {
        'total' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'one' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'two' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*((((((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2))))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'zero' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    },
    'eeet' : {
        'total' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1 + ((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2 - ((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'one' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 > 0.5))*zhFR1)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'two' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*((((((iso_3 < 0.15 && id_e_mva_nt_tight_3 > 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR2))))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
        'zero' : '(GenWeight/abs( GenWeight ))*(H_SS==0)*(((((iso_3 > 0.15 || id_e_mva_nt_tight_3 < 0.5)&&(byMediumIsolationMVArun2v1DBoldDMwLT_4 < 0.5))*zhFR0)))*(puweight*azhWeight)*(XSecLumiWeight)*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)',
    }
}

for channel, info in fractions.iteritems() :
    fName = 'root_files/totalMC_%s.root' % channel
    f = ROOT.TFile( fName, 'r' )
    
    t = f.Get('Ntuple')
    
    hEta = ROOT.TH1D('hEta','hEta',20,-10,10)
    
    #t.Draw( 'eta_1 >> hEta', cutMap[channel] )
    #print "Channel: %s       Total         %4.2f" % (channel, hEta.Integral())
    
    theMath = 0.
    for rb, cut in info.iteritems() :
        t.Draw( 'eta_1 >> hEta', cut )
        print "Channel: %s        %s        %4.2f" % (channel, rb, hEta.Integral())
        if rb in ['one','two'] : theMath += hEta.Integral()
        if rb == 'zero' : theMath -= hEta.Integral()
    
    print "Channel: %s        1+2-0        %4.2f" % (channel, theMath)
