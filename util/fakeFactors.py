import ROOT
from array import array
import os, glob, subprocess


def doFF() :
    f = ROOT.TFile('data_tt2.root','r')
    t = f.Get('Ntuple')
    f2 = ROOT.TFile('data_tt2.root','r')
    t2 = f2.Get('Ntuple')
    
    # Retrieve the fake factor
    cmssw_base = os.getenv('CMSSW_BASE')
    print "CMSSW BASE DIR: ",cmssw_base
    ff_file = ROOT.TFile.Open(cmssw_base+'/src/HTTutilities/Jet2TauFakes/data/fakeFactors_20160425.root')
    ffcomb = ff_file.Get('ff_comb')
    ffqcd = ff_file.Get('ff_qcd_os')
    ffqcdss = ff_file.Get('ff_qcd_ss')
    ffw = ff_file.Get('ff_w')
    fftt = ff_file.Get('ff_tt')
    
    data = ROOT.TH1F('data','data',350,0,350)
    fake = ROOT.TH1F('fake','fake',350,0,350)
    fake2 = ROOT.TH1F('fake2','fake2',350,0,350)
    
    cnt = 0
    for row in t :
        mvis = row.m_vis
        muon_iso = 0.089
        if row.t2ByTightIsolationMVArun2v1DBoldDMwLT < 0.5 and row.t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 : # these are used for Fake Factors
            tau_pt = row.pt_2
            tau_decayMode = row.t2DecayMode
            mt = row.mt_2
    
            # Input names
            # Currently: tau_pt, tau_decay, mvis, mt, muon_iso
            inputscomb = ffcomb.inputs() # this returns a ROOT.vector<string> object
            inputsqcd = ffqcd.inputs() # this returns a ROOT.vector<string> object
            
            # Fill inputs
            inputscomb = [tau_pt, tau_decayMode, mvis, mt, muon_iso]
            inputsqcd = [tau_pt, tau_decayMode, mvis, muon_iso]
            
            # Retrieve fake factors
            ff_nomcomb = ffcomb.value( len(inputscomb),array('d',inputscomb) ) # nominal fake factor
            ff_nomqcd = ffqcd.value( len(inputsqcd),array('d',inputsqcd) ) # nominal fake factor

            #sys = '...'
            #ff_sys = ff.value( len(inputs),array('d',inputs), sys ) # systematic shift
            
            # Apply fake factor as event weight
            #print "Evt: %d    FakeFactor Comb: %f    FF QCD: %f" % (row.evt, ff_nomcomb, ff_nomqcd)
            fake.Fill( row.m_vis, ff_nomqcd )
        elif row.t1ByTightIsolationMVArun2v1DBoldDMwLT < 0.5 and row.t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 : # these are used for Fake Factors
            ''' for lead tau '''
            tau_pt = row.pt_1
            tau_decayMode = row.t1DecayMode
            inputsqcd = ffqcd.inputs() # this returns a ROOT.vector<string> object
            inputsqcd = [tau_pt, tau_decayMode, mvis, muon_iso]
            ff_nomqcd = ffqcd.value( len(inputsqcd),array('d',inputsqcd) ) # nominal fake factor
            fake2.Fill( row.m_vis, ff_nomqcd )

        if row.t1ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 and row.t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 : # these are the real data
            data.Fill( mvis, 1.0 )
            cnt += 1
        #if row.evt == 441073442 :
        #    print "!!!",ff_nomqcd
        #    print inputsqcd
    print cnt
    print "data total = ",data.Integral()
    print "data total = ",data.GetEntries()
    print "qcd total = ",fake.Integral()
    print "qcd total # = ",fake.GetEntries()
    print "qcd2 total = ",fake2.Integral()
    print "qcd2 total # = ",fake2.GetEntries()
    print "TOTAL QCD: %f" % (fake.Integral() + fake2.Integral())

    count = 0
    c2 = 0
    c3 = 0
    cFinal = 0.
    for row in t2 :
        if row.t2ByVTightIsolationMVArun2v1DBoldDMwLT > 0.5 : # these are the real data
            count += 1
        if row.t2ByTightIsolationMVArun2v1DBoldDMwLT < 0.5 : # these are used for Fake Factors
            c2 += row.FFWeightQCD
            c3 += 1

        cFinal += row.FFWeightQCD

    print "data2 total = ",count
    print "data2 qcd = ",c2
    print "data2 qcd # = ",c3
    print "Actual REAL TOTAL = ",cFinal
        

    ffcomb.Delete()
    ffqcd.Delete()
    ffqcdss.Delete()
    ffw.Delete()
    fftt.Delete()
    ff_file.Close()


def mergeFiles( sample, folder1, folder2 ) :
    cmssw_base = os.getenv('CMSSW_BASE')
    files = glob.glob(cmssw_base+'/src/Z_to_TauTau_13TeV/'+folder1+'/%s*_tt.root' % sample )
    destination = cmssw_base+'/src/Z_to_TauTau_13TeV/'+folder2+'/%s_tt.root' % sample
    #print files
    mergeList = ["hadd", "-f", destination]
    for f in files :
        mergeList.append( f )
    #print mergeList
    subprocess.call( mergeList )


if __name__ == '__main__' :
    samples = ['DYJetsBig', 'DYJets1', 'DYJets2', 'DYJets3', 'DYJets4', 'DYJetsHigh', 'T-tchan', 'Tbar-tchan', 'Tbar-tW', 'T-tW', 'WW1l1nu2q', 'WZ1l1nu2q', 'WZ1l3nu', 'WZ3l1nu', 'WZ2l2q', 'WZJets', 'ZZ2l2q', 'ZZ4l', 'VV']

    f1 = 'dataCards2May02_FakeFactors'
    f2 = 'FakeFactor/samples'

    #for sample in samples :
    #    print sample
    #    #mergeFiles( sample, f1, f2 )
    doFF()
