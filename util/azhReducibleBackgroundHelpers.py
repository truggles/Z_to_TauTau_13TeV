


# provide the reducible background cuts and weights
# for the AZH / ZH analyses
# specifically for the H_OS region where yield is estimated
def getRedBkgCutsAndWeights( analysis, channel, cut, prodMap ) :

    assert (channel in prodMap.keys() and len(channel)>3 ), \
        "The current channel %s is missing from \
        the Red Bkg process, you must define it" % channel

    # Failing cuts
    electronCutF = '(iso_NUM > 0.15 || id_e_mva_nt_tight_NUM < 0.5)'
    muonCutF = '(iso_NUM > 0.15 || CAND_PFIDLoose < 0.5)'
    tauCutF = '(byMediumIsolationMVArun2v1DBoldDMwLT_NUM < 0.5)'
    
    # Passing cuts
    electronCutP = '(iso_NUM < 0.15 && id_e_mva_nt_tight_NUM > 0.5)'
    muonCutP = '(iso_NUM < 0.15 && CAND_PFIDLoose > 0.5)'
    tauCutP = '(byMediumIsolationMVArun2v1DBoldDMwLT_NUM > 0.5)'

    if channel in ['eeet','eeem','emmt','emmm','eeee'] :
        leg3F = electronCutF.replace('NUM', '3').replace('CAND_', prodMap[channel][2] )
        leg3P = electronCutP.replace('NUM', '3').replace('CAND_', prodMap[channel][2] )
    elif channel in ['eemm','eemt','mmmt','mmmm'] :
        leg3F = muonCutF.replace('NUM', '3').replace('CAND_', prodMap[channel][2] )
        leg3P = muonCutP.replace('NUM', '3').replace('CAND_', prodMap[channel][2] )
    elif channel in ['eett','mmtt'] :
        leg3F = tauCutF.replace('NUM', '3').replace('CAND_', prodMap[channel][2] )
        leg3P = tauCutP.replace('NUM', '3').replace('CAND_', prodMap[channel][2] )

    if channel in ['eett','mmtt','eeet','emmt','eemt','mmmt',] :
        leg4F = tauCutF.replace('NUM', '4').replace('CAND_', prodMap[channel][3] )
        leg4P = tauCutP.replace('NUM', '4').replace('CAND_', prodMap[channel][3] )
    elif channel in ['eeem','eemm','emmm','mmmm'] :
        leg4F = muonCutF.replace('NUM', '4').replace('CAND_', prodMap[channel][3] )
        leg4P = muonCutP.replace('NUM', '4').replace('CAND_', prodMap[channel][3] )
    elif channel in ['eeee',] :
        leg4F = electronCutF.replace('NUM', '4').replace('CAND_', prodMap[channel][3] )
        leg4P = electronCutP.replace('NUM', '4').replace('CAND_', prodMap[channel][3] )

    # Add weight based on 1 + 2 - 0 method
    redBkgCut = '(('+leg3F+'&&'+leg4P+')*zhFR1'
    redBkgCut += ' + ('+leg3P+'&&'+leg4F+')*zhFR2'
    redBkgCut += ' - ('+leg3F+'&&'+leg4F+')*zhFR0)'
 
    cut = cut.replace('ADD_CHANNEL_SPECIFIC_ISO_CUTS', '('+redBkgCut+')')

    return '*(H_SS==0)'+cut




# Method of estimating the Reducible Bkg shape from SS region
def getRedBkgShape( analysis, channel, cut, prodMap ) :

    assert (channel in prodMap.keys() and len(channel)>3 ), \
        "The current channel %s is missing from \
        the Red Bkg process, you must define it" % channel

    elec = 'iso_NUM < 2 && id_e_mva_nt_loose_NUM > 0.5'
    muon = 'iso_NUM < 2 && CAND_PFIDLoose > 0.5'
    tau = 'byVVLooseIsolationMVArun2v1DBoldDMwLT_NUM > 0.5'


    newCuts = []
    if analysis == 'azh' :
        if 'e' in prodMap[channel][2] :
            newCuts.append( elec.replace('NUM', '3').replace('CAND_', prodMap[channel][2] ) )
        if 'm' in prodMap[channel][2] :
            newCuts.append( muon.replace('NUM', '3').replace('CAND_', prodMap[channel][2] ) )
        if 't' in prodMap[channel][2] :
            newCuts.append( tau.replace( 'NUM', '3').replace('CAND_', prodMap[channel][2] ) )
        if 'e' in prodMap[channel][3] :
            newCuts.append( elec.replace('NUM', '4').replace('CAND_', prodMap[channel][3] ) )
        if 'm' in prodMap[channel][3] :
            newCuts.append( muon.replace('NUM', '4').replace('CAND_', prodMap[channel][3] ) )
        if 't' in prodMap[channel][3] :
            newCuts.append( tau.replace( 'NUM', '4').replace('CAND_', prodMap[channel][3] ) )


    if newCuts != [] :
        newCut = ' && '.join( newCuts )
        cut = cut.replace('ADD_CHANNEL_SPECIFIC_ISO_CUTS', '('+newCut+')')

    return '*(H_SS==1)'+cut



     
def getChannelSpecificFinalCuts( analysis, channel, cut, prodMap ) :

    assert (channel in prodMap.keys() and len(channel)>3 ), \
        "The current channel %s is missing from \
        the Red Bkg process, you must define it" % channel

    newCuts = []
    # Currently defined for ZH
    elec = 'iso_NUM < 0.15 && id_e_mva_nt_tight_NUM > 0.5'
    muon = 'iso_NUM < 0.15 && CAND_PFIDLoose > 0.5'
    tau = 'byMediumIsolationMVArun2v1DBoldDMwLT_NUM > 0.5'

    if analysis == 'azh' :
        if 'e' in prodMap[channel][2] :
            newCuts.append( elec.replace('NUM', '3').replace('CAND_', prodMap[channel][2] ) )
        if 'm' in prodMap[channel][2] :
            newCuts.append( muon.replace('NUM', '3').replace('CAND_', prodMap[channel][2] ) )
        if 't' in prodMap[channel][2] :
            newCuts.append( tau.replace( 'NUM', '3').replace('CAND_', prodMap[channel][2] ) )
        if 'e' in prodMap[channel][3] :
            newCuts.append( elec.replace('NUM', '4').replace('CAND_', prodMap[channel][3] ) )
        if 'm' in prodMap[channel][3] :
            newCuts.append( muon.replace('NUM', '4').replace('CAND_', prodMap[channel][3] ) )
        if 't' in prodMap[channel][3] :
            newCuts.append( tau.replace( 'NUM', '4').replace('CAND_', prodMap[channel][3] ) )


    if newCuts != [] :
        newCut = ' && '.join( newCuts )
        cut = cut.replace('ADD_CHANNEL_SPECIFIC_ISO_CUTS', '('+newCut+')')

    return '*(H_SS==0)'+cut





