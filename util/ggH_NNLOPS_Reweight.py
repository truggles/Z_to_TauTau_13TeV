'''
A class to apply the Gluon Fusion NNLOPS reweighting
See: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/SignalModelingTools 
'''


import ROOT

class ggH_NNLOPS_Reweight :
    """A class to provide Gluon Fusion NNLOPS reweighting""" 
    

    def __init__( self ):

        ### From: https://twiki.cern.ch/twiki/pub/CMS/HiggsWG/SignalModelingTools/NNLOPS_reweight.root
        self.nnlopsFile = ROOT.TFile( 'data/NNLOPS_reweight.root', 'r' )
        self.nJet0 = self.nnlopsFile.Get( 'gr_NNLOPSratio_pt_powheg_0jet' )
        self.nJet1 = self.nnlopsFile.Get( 'gr_NNLOPSratio_pt_powheg_1jet' )
        self.nJet2 = self.nnlopsFile.Get( 'gr_NNLOPSratio_pt_powheg_2jet' )
        self.nJet3 = self.nnlopsFile.Get( 'gr_NNLOPSratio_pt_powheg_3jet' )


    def get_ggH_NNLOPS_Reweight( self, njets, higgs_pt ) :
        if (njets==0):
            return self.nJet0.Eval(min(higgs_pt,125.0))
        elif (njets==1):
            return self.nJet1.Eval(min(higgs_pt,625.0))
        elif (njets==2):
            return self.nJet2.Eval(min(higgs_pt,800.0))
        elif (njets>=3):
            return self.nJet3.Eval(min(higgs_pt,925.0))
        else:
            return 1.0


        

if __name__ == '__main__' :
    reweighter = ggH_NNLOPS_Reweight()
    print reweighter.get_ggH_NNLOPS_Reweight( 0, 154 )
    print reweighter.get_ggH_NNLOPS_Reweight( 0, 1549 )
    print reweighter.get_ggH_NNLOPS_Reweight( 1, 154 )
    print reweighter.get_ggH_NNLOPS_Reweight( 1, 1549 )
    print reweighter.get_ggH_NNLOPS_Reweight( 2, 154 )
    print reweighter.get_ggH_NNLOPS_Reweight( 2, 1549 )
    print reweighter.get_ggH_NNLOPS_Reweight( 3, 154 )
    print reweighter.get_ggH_NNLOPS_Reweight( 3, 1549 )



