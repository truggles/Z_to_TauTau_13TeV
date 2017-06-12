#########################################################################
#
#  Function to provide the LO to NNLO reweight of the qqZZ4l sample:
#  
#      /ZZTo4L_13TeV_powheg_pythia8/
#  
#  These values are provided also for reweighting by dPhi(Z1, Z2) and
#  pt(ZZ). I choose genMass because the variable is stored in my
#  FSA ntuples. The documentation can be found here:
#  
#  https://twiki.cern.ch/twiki/bin/view/CMS/HiggsZZ4l2017#qqZZ
#  
#  If groups do not have genMass, they can use k-factor = 1.1 for the time being
#
###########################################################################

import ROOT



def qqZZ4l_nnlo_weight( genMass, hasZee, hasZmumu, hasZtautau ) :

    # Corrections are split into 2 categories
    # - ZZ4l
    # - ZZ2l2l'

    finalState=0
    tot = hasZee + hasZmumu + hasZtautau
    if tot == 1 :   finalState = 1 # 4e/4mu/4tau
    elif tot == 2 : finalState = 2 # 2e2mu/2mutau/2e2tau
    else :          return 1.1       # default k-factor

    if finalState == 1 : 
        if genMass > 0.00  and genMass <= 25.0  : return 1.23613311013
        if genMass > 25.0  and genMass <= 50.0  : return 1.17550314639
        if genMass > 50.0  and genMass <= 75.0  : return 1.17044565911
        if genMass > 75.0  and genMass <= 100.0 : return 1.03141209689
        if genMass > 100.0 and genMass <= 125.0 : return 1.05285574912
        if genMass > 125.0 and genMass <= 150.0 : return 1.11287217794
        if genMass > 150.0 and genMass <= 175.0 : return 1.13361441158
        if genMass > 175.0 and genMass <= 200.0 : return 1.10355603327
        if genMass > 200.0 and genMass <= 225.0 : return 1.10053981637
        if genMass > 225.0 and genMass <= 250.0 : return 1.10972676811
        if genMass > 250.0 and genMass <= 275.0 : return 1.12069120525
        if genMass > 275.0 and genMass <= 300.0 : return 1.11589101635
        if genMass > 300.0 and genMass <= 325.0 : return 1.13906170314
        if genMass > 325.0 and genMass <= 350.0 : return 1.14854594271
        if genMass > 350.0 and genMass <= 375.0 : return 1.14616229031
        if genMass > 375.0 and genMass <= 400.0 : return 1.14573157789
        if genMass > 400.0 and genMass <= 425.0 : return 1.13829430515
        if genMass > 425.0 and genMass <= 450.0 : return 1.15521193686
        if genMass > 450.0 and genMass <= 475.0 : return 1.13679822698
        if genMass > 475.0                      : return 1.13223956942

    if finalState == 2 :
        if genMass > 0.00  and genMass <= 25.0  : return 1.25094466582
        if genMass > 25.0  and genMass <= 50.0  : return 1.22459455362
        if genMass > 50.0  and genMass <= 75.0  : return 1.19287368979
        if genMass > 75.0  and genMass <= 100.0 : return 1.04597506451
        if genMass > 100.0 and genMass <= 125.0 : return 1.08323413771
        if genMass > 125.0 and genMass <= 150.0 : return 1.09994968030
        if genMass > 150.0 and genMass <= 175.0 : return 1.16698455800
        if genMass > 175.0 and genMass <= 200.0 : return 1.10399053155
        if genMass > 200.0 and genMass <= 225.0 : return 1.10592664340
        if genMass > 225.0 and genMass <= 250.0 : return 1.10690381480
        if genMass > 250.0 and genMass <= 275.0 : return 1.11194928918
        if genMass > 275.0 and genMass <= 300.0 : return 1.13522586553
        if genMass > 300.0 and genMass <= 325.0 : return 1.11895090244
        if genMass > 325.0 and genMass <= 350.0 : return 1.13898508615
        if genMass > 350.0 and genMass <= 375.0 : return 1.15463977506
        if genMass > 375.0 and genMass <= 400.0 : return 1.17341664594
        if genMass > 400.0 and genMass <= 425.0 : return 1.20093349763
        if genMass > 425.0 and genMass <= 450.0 : return 1.18915554919
        if genMass > 450.0 and genMass <= 475.0 : return 1.18546007375
        if genMass > 475.0                      : return 1.12864505708

    assert( 2 + 2 == 5), "qqZZ4l reweighting, shouldn't get here"


