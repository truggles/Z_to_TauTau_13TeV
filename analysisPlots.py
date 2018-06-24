import ROOT
from ROOT import gPad
from array import array
from collections import OrderedDict
from util.helpers import returnSortedDict, getProdMap
from util.azhReducibleBackgroundHelpers import \
    getRedBkgCutsAndWeights, getChannelSpecificFinalCuts, \
    getRedBkgShape
from smart_getenv import getenv
from util.jetEnergyScale import getUncerts



# Make a histo, but fill it later so we can keep track of events for ALL histos at once
def makeHisto( cutName, varBins, varMin, varMax ) :
    hist = ROOT.TH1D( cutName, cutName, varBins, varMin, varMax )
    return hist


# If the sample is an anomalous signal, then
def getAnomalousSignalWeight( sample ) :

    if not 'HtoTauTau' in sample :
        return '*(1.)'
    if 'HtoTauTau0PHf05ph0125' in sample :
        return '*(jhuw_a2int)'
    if 'HtoTauTau0L1f05ph0125' in sample :
        return '*(jhuw_l1int)'
    if 'HtoTauTau0L1125' in sample :
        return '*(jhuw_l1)'
    if 'HtoTauTau0PM125' in sample :
        return '*(jhuw_a1)'
    if 'HtoTauTau0Mf05ph0125' in sample :
        return '*(jhuw_a3int)'
    if 'HtoTauTau0PH125' in sample :
        return '*(jhuw_a2)'
    if 'HtoTauTau0M125' in sample :
        return '*(jhuw_a3)'
    if 'HtoTauTau0L1Zgf05ph0125' in sample :
        return '*(jhuw_l1Zgint)'
    if 'HtoTauTau0L1Zg125' in sample :
        return '*(jhuw_l1Zg)'
    else :
        return '*(1.)'


# Make a 2D histo
def get2DVars( cutName ) :
    #if 'mjj' in cutName and 'm_sv' in cutName and 'melaD0minus' in cutName :
    if 'mjj' in cutName and 'm_sv' in cutName and 'mela' in cutName :
        #xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        xBins = array( 'd', [0,70,80,90,100,120,150,250] )
        yBins = array( 'd', [0,300,500,800,10000] )
        #xBins = array( 'd', [0,95,115,135,155,400] )
        #yBins = array( 'd', [0,300,700,1100,1500,10000] )
        #zBins = array( 'd', [0,.2,.4,.6,.8,1] )
    elif 'mjj' in cutName and 'm_sv' in cutName and 'melaDCP' in cutName :
        #xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        xBins = array( 'd', [0,70,80,90,100,120,150,250] )
        yBins = array( 'd', [0,300,500,800,10000] )
        #xBins = array( 'd', [0,95,115,135,155,400] )
        #yBins = array( 'd', [0,300,700,1100,1500,10000] )
        #zBins = array( 'd', [-1,0,1] )

    elif 'pt_sv' in cutName and 'm_sv' in cutName :
        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,100,170,300,10000] )
    elif 'mjj' in cutName and 'm_sv' in cutName :
        #xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        xBins = array( 'd', [0,70,80,90,100,120,150,250] )
        yBins = array( 'd', [0,300,500,800,10000] )
    elif 'Higgs_PtCor' in cutName and 'm_sv' in cutName :
        #xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        xBins = array( 'd', [0,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,100,170,300,10000] )
    elif 'Higgs_PtCor' in cutName and 'm_visCor' in cutName :
        #xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        xBins = array( 'd', [0,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,100,170,300,10000] )
    elif 'mjj' in cutName and 'm_visCor' in cutName :
        #xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        xBins = array( 'd', [0,70,80,90,100,120,150,250] )
        yBins = array( 'd', [0,300,500,800,10000] )
    return (xBins, yBins)

# Make a 2D histo
def make2DHisto( cutName ) :
    info = get2DVars( cutName )
    xBins = info[0]
    yBins = info[1]
    hist = ROOT.TH2D( cutName, cutName, len(xBins)-1, xBins, len(yBins)-1, yBins )
    return hist


def skipSystShapeVar( var, sample, channel, genCode='x' ) :
        # Tau Pt Scale reweighting only applied to DYJets and signal
        #print "Skip Vars:",sample, var, genCode
        if '_tauPt' in var :
            if 'data' in sample : return True
            # This is QCD with an era
            # thus means fake factor 
            # method which is fully data driven
            if 'QCD-' in sample : return True
            
        # Energy Scale reweighting applied to all MC based on gen_match
        elif '_energyScale' in var :
            if 'data' in sample : return True
            # This is QCD with an era
            # thus means fake factor 
            # method which is fully data driven
            if 'QCD-' in sample : return True

        # z pt reweight only applied to LO DYJets samples, DYJetsLow in amc@nlo
        # do run for DYJetsLow as weight is set to 1
        elif '_zPt' in var :
            if not 'DYJets' in sample : return True

        # top pt reweighting only applied to ttbar
        elif '_topPt' in var :
            if 'TT' not in sample : return True
            elif 'data' in sample : return True # for dataTT
            elif 'DYJets' in sample : return True # for ZTT

        # Jet Energy Scale, no data
        elif '_JES' in var :
            if 'data' in sample : return True
            # This is QCD with an era
            # thus means fake factor 
            # method which is fully data driven
            if 'QCD-' in genCode : return True
            if 'QCD-' in sample : return True

        # Jet Energy Scale, no data
        elif ('_metClustered' in var or '_metUnclustered' in var) :
            if 'data' in sample : return True
            # This is QCD with an era
            # thus means fake factor 
            # method which is fully data driven
            if 'QCD-' in genCode : return True
            if 'QCD-' in sample : return True

        # Jet to Tau Fake, no data
        elif '_JetToTau' in var :
            #if 'data' in sample : return True
            if not ('TTJ' in genCode or 'TTJ' in sample or \
                    'ZJ' in genCode or 'ZJ' in sample or \
                    'VVJ' in genCode or 'VVJ' in sample or \
                    'WJets' in sample) :
                return True
            else : return False # Needed this for some reason, not sure why

        # ggH Scale, only for ggH
        elif '_ggH' in var :
            if not 'ggHtoTauTau' in sample : return True

        # topQuarkggH Scale, only for ggH
        elif '_topQuarkggH' in var :
            if not 'ggHtoTauTau' in sample : return True

        # Zmumu yields by slices, only for DYJets and EWKZ, and only VBF at the moment
        elif '_Zmumu' in var :
            if 'DYJets' in sample : return False
            if 'EWKZ' in sample : return False
            else : return True

        elif 'ffSyst' in var or 'ffStat' in var :
            if not ('ZJ' in genCode or 'ZJ' in sample or \
                    'TTJ' in genCode or 'TTJ' in sample or \
                    'VVJ' in genCode or 'VVJ' in sample or \
                    'QCD-' in genCode or 'QCD-' in sample or \
                    'WJets' in sample) :
                return True

        return False

# Return True for backgrounds to skip
# Only want to plot signals and data
def skipDCPVar( var, sample ) :
    if '_DCPp' in var or '_DCPm' in var :
        # Check if there is a Higgs Mass in the sample, if so, plot it
        if '110' in sample or '120' in sample or '125' in sample or '130' in sample or '140' in sample :
            return False
        elif 'data' in sample : return False
        else : return True # No Higgs mass, therefore Bkg

    return False



# Make specific extra cuts for different TES requirements
def ESCuts( ESMap, sample, channel, var ) :
    tau2PtCut = 40.
    tau1PtCut = 50.
    if len( channel ) == 4 : return '*(1.)'
    if 'data' in sample :
        if channel == 'tt' :
            return '*(pt_1 > %s && pt_2 > %s)' % (tau1PtCut, tau2PtCut)

    shiftDir = ''
    if 'Up' in var[-2:] : shiftDir = 'Up'
    elif 'Down' in var[-4:] : shiftDir = 'Down'
    elif 'energyScale' not in var : return ESMap[ channel ]['_NoShift']

    if '_energyScaleAll'+shiftDir in var : return ESMap[ channel ]['_energyScaleAll'+shiftDir]
    if '_energyScaleDM0'+shiftDir in var : return ESMap[ channel ]['_energyScaleDM0'+shiftDir]
    if '_energyScaleDM1'+shiftDir in var : return ESMap[ channel ]['_energyScaleDM1'+shiftDir]
    if '_energyScaleDM10'+shiftDir in var : return ESMap[ channel ]['_energyScaleDM10'+shiftDir]
    return ESMap[ channel ]['_NoShift']

def getESMap() :
    tau2PtCut = 40.
    tau1PtCut = 50.
    ESMap = {
        'tt' : { 
            '_energyScaleAllUp' : '*( pt_1_UP > %s && pt_2_UP > %s)' % (tau1PtCut, tau2PtCut),
            '_energyScaleAllDown' : '*( pt_1_DOWN > %s && pt_2_DOWN > %s)' % (tau1PtCut, tau2PtCut),
            '_energyScaleDM0Up' : '*( pt_1_DM0_UP > %s && pt_2_DM0_UP > %s)' % (tau1PtCut, tau2PtCut),
            '_energyScaleDM0Down' : '*( pt_1_DM0_DOWN > %s && pt_2_DM0_DOWN > %s)' % (tau1PtCut, tau2PtCut),
            '_energyScaleDM1Up' : '*( pt_1_DM1_UP > %s && pt_2_DM1_UP > %s)' % (tau1PtCut, tau2PtCut),
            '_energyScaleDM1Down' : '*( pt_1_DM1_DOWN > %s && pt_2_DM1_DOWN > %s)' % (tau1PtCut, tau2PtCut),
            '_energyScaleDM10Up' : '*( pt_1_DM10_UP > %s && pt_2_DM10_UP > %s)' % (tau1PtCut, tau2PtCut),
            '_energyScaleDM10Down' : '*( pt_1_DM10_DOWN > %s && pt_2_DM10_DOWN > %s)' % (tau1PtCut, tau2PtCut),
            '_NoShift' : '*(ptCor_1 > %s && ptCor_2 > %s)' % (tau1PtCut, tau2PtCut)},
        }
    return ESMap


# Specific high pt tau reweighting for shape uncertainties
def HighPtTauWeight( var ) :
    if not '_tauPt' in var: return ''
    # see analysis2 for how tauPtWeight is calculated
    elif '_tauPtUp' in var : return '*(tauPtWeightUp)'
    elif '_tauPtDown' in var : return '*(tauPtWeightDown)'
    else : return ''



# Append the correction cuts for Fake Factors
# this includes the MC based coin flip
# and isolation cuts which were removed in
# makeFinalCutsAndPlots.py for convenience
#FIXME direct link to their documentation
# see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauJet2TauFakes
# At the moment VTight is hardcoded here
#
# New (Oct 30, 2016) each sample (data included)
# will have 2 versions of each histo, signal region
# with normal filling for data, and a gen_match
# requirement for MC.  And, an anti-isolated region
# with histos filled using FF method
# anti-isolated histos are for subtracting from
# signal region histos later
def getFFCutsAndWeights( ffRegion, isData, outFile ) :

    fName = outFile.GetName()
    # Removing the coin flip method, this was discussed at
    # Add a factor of 0.5 to account for this removal
    # the FF workshop in early Oct

    dataSignalIsolation = '*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)'
    # mcSignalIsolation fills histso with a weight of 0.5 for each "non-fake" tau
    mcSignalIsolation = '*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_1 < 6) * 0.5 + (gen_match_2 < 6) * 0.5)'
    dataFFIsolation = '*((byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && byVLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5) || (byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5 && byVLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5))*(0.5)' # 0.5 for replacing the coin flip
    mcFFIsolation = '*((byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5 && byVLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && gen_match_2 < 6) || (byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5 && byVLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && gen_match_1 < 6))*(0.5)' # 0.5 for replacing the coin flip, the two different isolation configurations are orthogonal so we don't need to weight based on the gen_match like in mcSignalIsolation

    if ffRegion == 'signal' :
        if isData or 'QCD' in fName and 'tt' in fName :
            return dataSignalIsolation
        else : # not data
            return mcSignalIsolation
    if ffRegion == 'anti-iso' :
        if isData or 'QCD' in fName and 'tt' in fName :
            return dataFFIsolation
        else : # not data
            return mcFFIsolation


### Fake Factor shape systematics
def getFFShapeSystApp( ffRegion, isData, outFile, var ) :

    app = ''

    fName = outFile.GetName()
    # Check if FF sample
    # this one pick up the QCD made from 'data' samples
    # and also provides the weight for the MC jet->tau
    # subtraction
    if ('QCD' in fName and 'tt' in fName) or ffRegion == 'anti-iso' :

        # Choose appropriate weight for the category
        if   'ZTT0jet' in fName     : app = "FFWeight0Jet"
        elif 'ZTTboosted' in fName  : app = "FFWeightBoosted"
        elif 'ZTTvbf' in fName      : app = "FFWeightVBF"
        else                        : app = "FFWeightInc"

        # Check if a FF shape variable
        # Stat
        if '_0jet1prongffStatUp' in var   : app += '_0jet1prongStatUP'
        if '_0jet1prongffStatDown' in var : app += '_0jet1prongStatDOWN'
        if '_0jet3prongffStatUp' in var   : app += '_0jet3prongStatUP'
        if '_0jet3prongffStatDown' in var : app += '_0jet3prongStatDOWN'
        if '_1jet1prongffStatUp' in var   : app += '_1jet1prongStatUP'
        if '_1jet1prongffStatDown' in var : app += '_1jet1prongStatDOWN'
        if '_1jet3prongffStatUp' in var   : app += '_1jet3prongStatUP'
        if '_1jet3prongffStatDown' in var : app += '_1jet3prongStatDOWN'
        # Syst
        if '_qcdffSystUp' in var     : app += '_qcdSystUP'
        if '_qcdffSystDown' in var   : app += '_qcdSystDOWN'
        if '_ttbarffSystUp' in var   : app += '_ttbarSystUP'
        if '_ttbarffSystDown' in var : app += '_ttbarSystDOWN'
        if '_wjetsffSystUp' in var   : app += '_wjetsSystUP'
        if '_wjetsffSystDown' in var : app += '_wjetsSystDOWN'

        # Wrap appropriately
        app = "*("+app+")"

    # Return an empty string or appropriate FF Shape syst
    #print "ffRegion: ",ffRegion
    #print "File Name: ",fName
    #print "Append: ",app
    return app



# Plot histos using TTree::Draw which works very well with Proof
def plotHistosProof( analysis, outFile, chain, sample, channel, isData, additionalCut, blind=False, skipSSQCDDetails=False, genCode='x' ) :
    if genCode == 'x' : genCode = sample

    ''' Make a channel specific selection of desired histos and fill them '''
    newVarMapUnsorted = getHistoDict( analysis, channel )
    newVarMap = returnSortedDict( newVarMapUnsorted )

    #print outFile, channel
    histosDir = outFile.mkdir( "%s_Histos" % channel )
    histosDir.cd()

                
    # Set additionalCut to reflect ZH reducible background estimation
    # process

    # Add in the ability to do Reducible Background estimations for
    # AZH / ZH analysis
    # Add channel specific cuts
    if 'ADD_CHANNEL_SPECIFIC_ISO_CUTS' in additionalCut :
        prodMap = getProdMap()
        if analysis == 'azh' and 'RedBkgYield' in outFile.GetName() :
            additionalCut = getRedBkgCutsAndWeights(
                    analysis, channel, additionalCut, prodMap )
        elif analysis == 'azh' and 'RedBkgShape' in outFile.GetName() :
            additionalCut = getRedBkgShape( 
                    analysis, channel, additionalCut, prodMap )
        else : # No reducible bkg
            additionalCut = getChannelSpecificFinalCuts(
                    analysis, channel, additionalCut, prodMap )


    ''' Combine Gen and Chan specific into one fill section '''
    histos = {}


    ''' Get Energy Scale Map which is now confusing with
        decay mode specific shifts '''
    esMap = getESMap()


    ### Check if we intend to do Fake Factor based MC cuts
    ### These differ because of requiring a random choice
    ### of l1 and l2, then seeing if l1 is gen matched
    ### to anything besides a fake/jet
    ### This is only applied for DYJets, WJets, TT, and QCD MC

    ### Check if doFF is turned on and, if so, double
    ### our output histograms to account for the
    ### required subtractions
    doFF = getenv('doFF', type=bool)
    if doFF :
        tmpDict = {}
        for var, info in newVarMap.iteritems() :
            tmpDict[var] = info
            tmpDict[var+'_ffSub'] = info
        newVarMap = returnSortedDict( tmpDict )

    # Check for per-var adjustments later
    # Full JES shapes if doFullJES
    doFullJES = getenv('doFullJES', type=bool)
    if doFullJES : jesUncerts = getUncerts()

    # Check if sample is an anomalous HTT signal sample
    # If so get the extra weight addition to normalize properly
    anomWeight = getAnomalousSignalWeight( sample )

    for var, info in newVarMap.iteritems() :
        if skipSSQCDDetails and not (var == 'eta_1' or var == 'm_visCor')  : continue

        ''' Skip plotting 2D vars for 0jet and inclusive selections 
            and VBF vars for Boosted and Higgs Pt vars for VBF cat '''
        if 'ZTTinclusive' in outFile.GetName() or 'ZTT0jet' in outFile.GetName() :
            if ":" in var : continue
        elif 'ZTTboosted' in outFile.GetName() :
            if 'mjj:' in var : continue
            if 'm_sv' in var and ":" not in var and var != 'm_sv' : continue # skip m_sv shapes
        elif 'ZTTvbf' in outFile.GetName() :
            if 'Higgs_PtCor:' in var : continue
            if 'm_sv' in var and ":" not in var and var != 'm_sv' : continue # skip m_sv shapes

        #print var


        ''' Skip plotting unused shape systematics '''
        if skipSystShapeVar( var, sample, channel, genCode ) : continue

        ''' Skip plotting backgrounds for DCP+ and DCP- variables '''
        if skipDCPVar( var, sample ) : continue

        ''' Define syst shape weights if applicable '''
        shapeSyst = ''
        # High Pt tau reweighting,
        # not applied to data or FF jetToTauFakes 
        if '_tauPt' in var :
            shapeSyst = HighPtTauWeight( var )

        # top pt reweighting only applied to ttbar
        elif '_topPt' in var :
            if '_topPtUp' in var : shapeSyst = '*(topWeight)'
            elif '_topPtDown' in var : shapeSyst = '*(1./topWeight)'

        # z pt reweight only applied to LO DYJets samples, DYJetsLow in amc@nlo
        elif '_zPt' in var : # Shifts has been changed to 10% of correction
            if '_zPtUp' in var : shapeSyst = '*(1. + (-1. + zPtWeight) * 0.1 )' 
            elif '_zPtDown' in var : shapeSyst = '*(1. - (-1. + zPtWeight) * 0.1 )'

        # ggH scale to ggHtoTauTau signal
        elif '_ggH' in var :
            # Different scale depending on final category
            if 'ZTT0jet2D' in outFile.GetName() :
                if '_ggHUp' in var : shapeSyst = '*(ggHWeight0Jet)'
                elif '_ggHDown' in var : shapeSyst = '*(1./ggHWeight0Jet)'
            elif 'ZTTboosted' in outFile.GetName() :
                if '_ggHUp' in var : shapeSyst = '*(ggHWeightBoost)'
                elif '_ggHDown' in var : shapeSyst = '*(1./ggHWeightBoost)'
            elif 'ZTTvbf' in outFile.GetName() :
                if '_ggHUp' in var : shapeSyst = '*(ggHWeightVBF)'
                elif '_ggHDown' in var : shapeSyst = '*(1./ggHWeightVBF)'
            else : # Probably inclusive
                if '_ggHUp' in var : shapeSyst = '*(ggHWeight0Jet)'
                elif '_ggHDown' in var : shapeSyst = '*(1./ggHWeight0Jet)'

        # topQuarkggH scale to ggHtoTauTau signal
        elif '_topQuarkggH' in var :
            if '_topQuarkggHUp' in var : shapeSyst = '*(ggHtopQuarkWeight)'
            elif '_topQuarkggHDown' in var : shapeSyst = '*(2.-ggHtopQuarkWeight)'

        # Jet to Tau Fake
        # These look to be applied in reverse
        # the shift convention was choosen to match MSSM 2016 ICHEP
        elif '_JetToTau' in var :
            if '_JetToTauUp' in var :
                shapeSyst = '*(2 - jetToTauFakeWeight)' # = to 1 - SF
            elif '_JetToTauDown' in var :
                shapeSyst = '*(jetToTauFakeWeight)'

        # This is the Zmumu CR shape uncertainty from data/MC correction
        # below.  It is currently only applied to VBF
        # This shape will be skipped if not DYJets
        # Update - no shape uncert on boosted
        elif '_Zmumu' in var :
            #if '_ZmumuUp' in var and 'ZTTvbf' in outFile.GetName() :
            #    shapeSyst = '*(1. + zmumuVBFWeight2)'
            #elif '_ZmumuDown' in var and 'ZTTvbf' in outFile.GetName() :
            #    shapeSyst = '*(1./(1. + zmumuVBFWeight2))'
            if '_ZmumuUp' in var and 'ZTTvbf' in outFile.GetName() :
                shapeSyst = '*(zmumuVBFWeight)'
            elif '_ZmumuDown' in var and 'ZTTvbf' in outFile.GetName() :
                shapeSyst = '*(1./zmumuVBFWeight)'


        # Add the Zmumu CR normalizations from Cecile's studies
        # from Nov 18, 2016 SM-HTT
        # Update 2 Mar, 2017:
        # - VBF has specific shape correction too
        # Removed 2% global normalization adjustment, April 4, 2017
        if 'DYJets' in sample or 'EWKZ' in sample :
            if 'ZTTvbf' in outFile.GetName() :
                #shapeSyst += '*(1 + zmumuVBFWeight2)'
                shapeSyst += '*(zmumuVBFWeight)'
            else : # Applied to ALL categories
                shapeSyst += '*(1.00)'
        
            
        # Energy Scale reweighting applied to all Real Hadronic Taus
        # gen_match == 5
        # this is not an "if" style shape b/c we need to apply
        # normal pt cuts if the shape syst is not called
        # so instead we appeand it to what ever else we have
        shapeSyst += ESCuts( esMap, sample, channel, var )
        # Additionally, if we have Energy Scale, we also need
        # to change any Higgs_PtCor vars to Higgs_PtCor_UP/DOWN
        additionalCutToUse = additionalCut
        if 'energyScale' in var and 'data' not in sample :
            dm = ''
            if 'energyScaleAll' in var : dm = '_'
            elif 'energyScaleDM0' in var : dm = '_DM0_'
            elif 'energyScaleDM1' in var : dm = '_DM1_'
            elif 'energyScaleDM10' in var : dm = '_DM10_'

            if 'Up' in var[-2:] : shiftDir = 'UP'
            if 'Down' in var[-4:] : shiftDir = 'DOWN'

            additionalCutToUse = additionalCutToUse.replace('pt_sv','pt_sv%s%s' % (dm, shiftDir) )
            additionalCutToUse = additionalCutToUse.replace('Higgs_PtCor','Higgs_PtCor%s%s' % (dm, shiftDir) )


        # Jet Energy Scale:
        # similar as TES above, edit the additionalCut
        # so that njets is replaced by njets_JESUP
        # make because we unroll in mjj, edit that
        # as well when it's in the plotVar for 2D
        # plotVar is changed below with this happens for other shifts
        jesUnc = 'En'
        if 'JES' in var and 'data' not in sample :
            # with ~30 shifts, get the name of the shift
            if doFullJES :
                for unc in jesUncerts :
                    if unc in var : jesUnc = unc
            if 'Up' in var[-2:] :
                if doFullJES :
                    # jDeta is minimally impacted by JES shifts, so the minor adjustments are not saved atm
                    # and is negligible for mjj > 100
                    additionalCutToUse = additionalCutToUse.replace('jetVeto30','jetVeto30_Jet%sUp' % jesUnc)
                    # We changed naming to simple mjj, njetingap20 and jdeta for sync for nominal
                    additionalCutToUse = additionalCutToUse.replace('mjj','vbfMass_Jet%sUp' % jesUnc)
                else :
                    #additionalCutToUse = additionalCutToUse.replace('njetingap','vbfJetVeto30_JetEnUp') # Cut no long used
                    additionalCutToUse = additionalCutToUse.replace('jdeta','vbfDeta_JetEnUp')
                #print additionalCutToUse+"\n"
            if 'Down' in var[-4:] :
                if doFullJES :
                    additionalCutToUse = additionalCutToUse.replace('jetVeto30','jetVeto30_Jet%sDown' % jesUnc)
                    additionalCutToUse = additionalCutToUse.replace('mjj','vbfMass_Jet%sDown' % jesUnc)
                else :
                    #additionalCutToUse = additionalCutToUse.replace('njetingap','vbfJetVeto30_JetEnDown')
                    additionalCutToUse = additionalCutToUse.replace('jdeta','vbfDeta_JetEnDown')
                #print additionalCutToUse+"\n"

        # Met Systematics propagated to svFit
        # make sure to get proper Higgs_Pt (pt_sv)
        if '_metClustered' in var and 'data' not in sample :
            if 'Up' in var[-2:] :
                additionalCutToUse = additionalCutToUse.replace('pt_sv','pt_sv_ClusteredMet_UP')
                additionalCutToUse = additionalCutToUse.replace('Higgs_PtCor','Higgs_PtCor_ClusteredMet_UP')
            if 'Down' in var[-4:] :
                additionalCutToUse = additionalCutToUse.replace('pt_sv','pt_sv_ClusteredMet_DOWN')
                additionalCutToUse = additionalCutToUse.replace('Higgs_PtCor','Higgs_PtCor_ClusteredMet_DOWN')
        if '_metUnclustered' in var and 'data' not in sample :
            if 'Up' in var[-2:] :
                additionalCutToUse = additionalCutToUse.replace('pt_sv','pt_sv_UncMet_UP')
                additionalCutToUse = additionalCutToUse.replace('Higgs_PtCor','Higgs_PtCor_UncMet_UP')
            if 'Down' in var[-4:] :
                additionalCutToUse = additionalCutToUse.replace('pt_sv','pt_sv_UncMet_DOWN')
                additionalCutToUse = additionalCutToUse.replace('Higgs_PtCor','Higgs_PtCor_UncMet_DOWN')


        # This addes the Fake Factor shape systematics weights
        # And add the variable specific Fake Factor cut
        # (isolation and gen match change per variable def)
        ffShapeSyst = ''
        if doFF :
            ffRegion = 'anti-iso' if '_ffSub' in var else 'signal'
            ffShapeSyst += getFFShapeSystApp( ffRegion, isData, outFile, var )
            ffShapeSyst += getFFCutsAndWeights( ffRegion, isData, outFile )


        if ":" in var :
    	    histos[ var ] = make2DHisto( var )
        else :
    	    histos[ var ] = makeHisto( var, info[0], info[1], info[2])

        # Adding Trigger, ID and Iso, & Efficiency Scale Factors
        # and, top pt reweighting
        # weight is a composition of all applied MC/Data corrections
        sfs = '*(1.)'
        if analysis == 'htt' :
            sfs = '*(weight)'
            if channel == 'tt' :
                # Not currently included in weight for sync ntuple
                sfs += '*(tauIDweight_1 * tauIDweight_2)'
        if analysis == 'azh' :
            sfs = '*(puweight*azhWeight)' 
        xsec = '*(XSecLumiWeight)'

        # Add MELA cuts
        # Primary variables first
        if 'melaDCP' in var :
            if 'melaDCP_DCP_neg1to0' in var :
                additionalCutToUse += '*(melaDCP <= 0)'
            if 'melaDCP_DCP_0to1' in var :
                additionalCutToUse += '*(melaDCP > 0)'
        elif 'melaD0minusggH' in var :
            if 'melaD0minusggH_D0_0to0p25' in var : 
                additionalCutToUse += '*(melaD0minusggH < .25)'
            elif 'melaD0minusggH_D0_0p25to0p5' in var :
                additionalCutToUse += '*(melaD0minusggH >= 0.25 && melaD0minusggH < .5)'
            elif 'melaD0minusggH_D0_0p5to0p75' in var :
                additionalCutToUse += '*(melaD0minusggH >= 0.5 && melaD0minusggH < .75)'
            elif 'melaD0minusggH_D0_0p75to1' in var : 
                additionalCutToUse += '*(melaD0minusggH >= 0.75)'
        elif 'melaD0minus' in var :
            if 'melaD0minus_D0_0to0p2' in var : 
                additionalCutToUse += '*(melaD0minus < .2)'
            elif 'melaD0minus_D0_0p2to0p4' in var :
                additionalCutToUse += '*(melaD0minus >= 0.2 && melaD0minus < .4)'
            elif 'melaD0minus_D0_0p4to0p8' in var :
                additionalCutToUse += '*(melaD0minus >= 0.4 && melaD0minus < .8)'
            elif 'melaD0minus_D0_0p8to1' in var : 
                additionalCutToUse += '*(melaD0minus >= 0.8)'
        elif 'melaD0hplus' in var :
            if 'melaD0hplus_D0hplus_0to0p2' in var : 
                additionalCutToUse += '*(melaD0hplus < .2)'
            elif 'melaD0hplus_D0hplus_0p2to0p4' in var :
                additionalCutToUse += '*(melaD0hplus >= 0.2 && melaD0hplus < .4)'
            elif 'melaD0hplus_D0hplus_0p4to0p8' in var :
                additionalCutToUse += '*(melaD0hplus >= 0.4 && melaD0hplus < .8)'
            elif 'melaD0hplus_D0hplus_0p8to1' in var : 
                additionalCutToUse += '*(melaD0hplus >= 0.8)'
        elif 'melaDL1Zg' in var :
            if 'melaDL1Zg_DL1Zg_0to0p2' in var : 
                additionalCutToUse += '*(melaDL1Zg < .2)'
            elif 'melaDL1Zg_DL1Zg_0p2to0p4' in var :
                additionalCutToUse += '*(melaDL1Zg >= 0.2 && melaDL1Zg < .4)'
            elif 'melaDL1Zg_DL1Zg_0p4to0p8' in var :
                additionalCutToUse += '*(melaDL1Zg >= 0.4 && melaDL1Zg < .8)'
            elif 'melaDL1Zg_DL1Zg_0p8to1' in var : 
                additionalCutToUse += '*(melaDL1Zg >= 0.8)'
        elif 'melaDL1' in var :
            if 'melaDL1_DL1_0to0p2' in var : 
                additionalCutToUse += '*(melaDL1 < .2)'
            elif 'melaDL1_DL1_0p2to0p4' in var :
                additionalCutToUse += '*(melaDL1 >= 0.2 && melaDL1 < .4)'
            elif 'melaDL1_DL1_0p4to0p8' in var :
                additionalCutToUse += '*(melaDL1 >= 0.4 && melaDL1 < .8)'
            elif 'melaDL1_DL1_0p8to1' in var : 
                additionalCutToUse += '*(melaDL1 >= 0.8)'
        elif 'melaDPhijj' in var :
            if 'melaDPhijj_DPhijj_0toPiOver4' in var : 
                additionalCutToUse += '*(abs(melaDPhijj) < TMath::PiOver4())'
            elif 'melaDPhijj_DPhijj_piOver4toPiOver2' in var :
                additionalCutToUse += '*(abs(melaDPhijj) >= TMath::PiOver4() && abs(melaDPhijj) < TMath::PiOver2())'
            elif 'melaDPhijj_DPhijj_piOver2to3PiOver4' in var :
                additionalCutToUse += '*(abs(melaDPhijj) >= TMath::PiOver2() && abs(melaDPhijj) < (3*TMath::PiOver4()) )'
            elif 'melaDPhijj_DPhijj_3PiOver4toPi' in var : 
                additionalCutToUse += '*(abs(melaDPhijj) >= (3*TMath::PiOver4()) )'

        # Add MELA cuts
        # Secondary variables second: DCP portion
        if '_DCPp' in var :
            additionalCutToUse += '*(melaDCP >= 0.0)'
        elif '_DCPm' in var :
            additionalCutToUse += '*(melaDCP < 0.0)'

        # For 1D MELA vars in slices of mjj
        #if 'mela' in var and '_' in var :
        #    melaSplit = var.split('_')
        #    melaVars = ['melaD0hplus', 'melaDint', 'melaDL1', 'melaDL1int', 'melaDL1Zg', 'melaDL1Zgint', 'melaD0minus']
        #    mjjRange = ['mjj0-300', 'mjj300-500', 'mjj500-800', 'mjj800-inf']
        #    if melaSplit[0] in melaVars and melaSplit[1] in mjjRange :
        #        if 'mjj0-300' in var : 
        #            additionalCutToUse += '*(mjj <= 300)'
        #        elif 'mjj300-500' in var : 
        #            additionalCutToUse += '*(mjj > 300 && mjj <= 500)'
        #        elif 'mjj500-800' in var : 
        #            additionalCutToUse += '*(mjj > 500 && mjj <= 800)'
        #        elif 'mjj800-inf' in var : 
        #            additionalCutToUse += '*(mjj > 800)'

        #print "%s     High Pt Tau Weight: %s" % (var, tauW)
        #print var,shapeSyst
        totalCutAndWeightMC = '(GenWeight/abs( GenWeight ))%s%s%s%s%s%s' % (additionalCutToUse, sfs, xsec, shapeSyst, ffShapeSyst, anomWeight) 
        #print totalCutAndWeightMC


        # Check if the variable to plot is in the chain, if not, skip it
        # don't crash on systematics based variables
        varBase = var.replace('_ffSub','')
        plotVar = var.replace('_ffSub','') # remove the histo naming off the back of the plotting var
        if 'mela' in plotVar : # No need to check all vars
            plotVar = plotVar.replace( ':melaDCP_DCP_neg1to0', '' )
            plotVar = plotVar.replace( ':melaDCP_DCP_0to1', '' )
            plotVar = plotVar.replace( ':melaD0minus_D0_0to0p2', '' )
            plotVar = plotVar.replace( ':melaD0minus_D0_0p2to0p4', '' )
            plotVar = plotVar.replace( ':melaD0minus_D0_0p4to0p8', '' )
            plotVar = plotVar.replace( ':melaD0minus_D0_0p8to1', '' )
            plotVar = plotVar.replace( ':melaD0minusggH_D0_0to0p25', '' )
            plotVar = plotVar.replace( ':melaD0minusggH_D0_0p25to0p5', '' )
            plotVar = plotVar.replace( ':melaD0minusggH_D0_0p5to0p75', '' )
            plotVar = plotVar.replace( ':melaD0minusggH_D0_0p75to1', '' )
            plotVar = plotVar.replace( ':melaD0hplus_D0hplus_0to0p2', '' )
            plotVar = plotVar.replace( ':melaD0hplus_D0hplus_0p2to0p4', '' )
            plotVar = plotVar.replace( ':melaD0hplus_D0hplus_0p4to0p8', '' )
            plotVar = plotVar.replace( ':melaD0hplus_D0hplus_0p8to1', '' )
            plotVar = plotVar.replace( ':melaDL1_DL1_0to0p2', '' )
            plotVar = plotVar.replace( ':melaDL1_DL1_0p2to0p4', '' )
            plotVar = plotVar.replace( ':melaDL1_DL1_0p4to0p8', '' )
            plotVar = plotVar.replace( ':melaDL1_DL1_0p8to1', '' )
            plotVar = plotVar.replace( ':melaDL1Zg_DL1Zg_0to0p2', '' )
            plotVar = plotVar.replace( ':melaDL1Zg_DL1Zg_0p2to0p4', '' )
            plotVar = plotVar.replace( ':melaDL1Zg_DL1Zg_0p4to0p8', '' )
            plotVar = plotVar.replace( ':melaDL1Zg_DL1Zg_0p8to1', '' )
            plotVar = plotVar.replace( ':melaDPhijj_DPhijj_0toPiOver4', '' )
            plotVar = plotVar.replace( ':melaDPhijj_DPhijj_piOver4toPiOver2', '' )
            plotVar = plotVar.replace( ':melaDPhijj_DPhijj_piOver2to3PiOver4', '' )
            plotVar = plotVar.replace( ':melaDPhijj_DPhijj_3PiOver4toPi', '' )
            plotVar = plotVar.replace( '_DCPp', '' )
            plotVar = plotVar.replace( '_DCPm', '' )
        #plotVar = plotVar.replace( '_mjj0-300', '' )
        #plotVar = plotVar.replace( '_mjj300-500', '' )
        #plotVar = plotVar.replace( '_mjj500-800', '' )
        #plotVar = plotVar.replace( '_mjj800-inf', '' )
        if 'Up' in var or 'Down' in var :
            tmp = varBase.split('_')
            shapeName = tmp.pop()
            varBase = '_'.join(tmp)
            if 'energyScale' in shapeName :
                shiftDir = 'UP' if 'Up' in var else 'DOWN'
                if 'pt_sv:m_sv' in var :
                    if 'All'  in var : plotVar = 'pt_sv_%s:m_sv_%s' % (shiftDir, shiftDir)
                    if 'DM0'  in var : plotVar = 'pt_sv_DM0_%s:m_sv_DM0_%s' % (shiftDir, shiftDir)
                    if 'DM1'  in var : plotVar = 'pt_sv_DM1_%s:m_sv_DM1_%s' % (shiftDir, shiftDir)
                    if 'DM10' in var : plotVar = 'pt_sv_DM10_%s:m_sv_DM10_%s' % (shiftDir, shiftDir)
                elif 'Higgs_PtCor:m_sv' in var :
                    if 'All'  in var : plotVar = 'Higgs_PtCor_%s:m_sv_%s' % (shiftDir, shiftDir)
                    if 'DM0'  in var : plotVar = 'Higgs_PtCor_DM0_%s:m_sv_DM0_%s' % (shiftDir, shiftDir)
                    if 'DM1'  in var : plotVar = 'Higgs_PtCor_DM1_%s:m_sv_DM1_%s' % (shiftDir, shiftDir)
                    if 'DM10' in var : plotVar = 'Higgs_PtCor_DM10_%s:m_sv_DM10_%s' % (shiftDir, shiftDir)
                elif 'mjj:m_sv' in var :
                    if 'All'  in var : plotVar = 'mjj:m_sv_%s' % shiftDir
                    if 'DM0'  in var : plotVar = 'mjj:m_sv_DM0_%s' % shiftDir
                    if 'DM1'  in var : plotVar = 'mjj:m_sv_DM1_%s' % shiftDir
                    if 'DM10' in var : plotVar = 'mjj:m_sv_DM10_%s' % shiftDir
                elif 'm_sv' in var :
                    if 'All'  in var : plotVar = 'm_sv_%s' % shiftDir
                    if 'DM0'  in var : plotVar = 'm_sv_DM0_%s' % shiftDir
                    if 'DM1'  in var : plotVar = 'm_sv_DM1_%s' % shiftDir
                    if 'DM10' in var : plotVar = 'm_sv_DM10_%s' % shiftDir
                elif 'Higgs_PtCor:m_visCor' in var :
                    if 'All'  in var : plotVar = 'Higgs_PtCor_%s:m_visCor_%s' % (shiftDir, shiftDir)
                    if 'DM0'  in var : plotVar = 'Higgs_PtCor_DM0_%s:m_visCor_DM0_%s' % (shiftDir, shiftDir)
                    if 'DM1'  in var : plotVar = 'Higgs_PtCor_DM1_%s:m_visCor_DM1_%s' % (shiftDir, shiftDir)
                    if 'DM10' in var : plotVar = 'Higgs_PtCor_DM10_%s:m_visCor_DM10_%s' % (shiftDir, shiftDir)
                elif 'mjj:m_visCor' in var :
                    if 'All'  in var : plotVar = 'mjj:m_visCor_%s' % shiftDir
                    if 'DM0'  in var : plotVar = 'mjj:m_visCor_DM0_%s' % shiftDir
                    if 'DM1'  in var : plotVar = 'mjj:m_visCor_DM1_%s' % shiftDir
                    if 'DM10' in var : plotVar = 'mjj:m_visCor_DM10_%s' % shiftDir
                elif 'm_visCor' in var :
                    if 'All'  in var : plotVar = 'm_visCor_%s' % shiftDir
                    if 'DM0'  in var : plotVar = 'm_visCor_DM0_%s' % shiftDir
                    if 'DM1'  in var : plotVar = 'm_visCor_DM1_%s' % shiftDir
                    if 'DM10' in var : plotVar = 'm_visCor_DM10_%s' % shiftDir
                elif 'Up' in var :
                    plotVar = varBase + '_UP'
                elif 'Down' in var :
                    plotVar = varBase + '_DOWN'
            elif 'metClustered' in shapeName :
                if 'm_sv' in var :
                    if 'Up' in var[-2:] :
                        plotVar = plotVar.replace('_metClusteredUp','')
                        plotVar = plotVar.replace('m_sv','m_sv_ClusteredMet_UP')
                        plotVar = plotVar.replace('pt_sv','pt_sv_ClusteredMet_UP')
                        plotVar = plotVar.replace('Higgs_PtCor','Higgs_PtCor_ClusteredMet_UP')
                    if 'Down' in var[-4:] :
                        plotVar = plotVar.replace('_metClusteredDown','')
                        plotVar = plotVar.replace('m_sv','m_sv_ClusteredMet_DOWN')
                        plotVar = plotVar.replace('pt_sv','pt_sv_ClusteredMet_DOWN')
                        plotVar = plotVar.replace('Higgs_PtCor','Higgs_PtCor_ClusteredMet_DOWN')
            elif 'metUnclustered' in shapeName :
                if 'm_sv' in var :
                    if 'Up' in var[-2:] :
                        plotVar = plotVar.replace('_metUnclusteredUp','')
                        plotVar = plotVar.replace('m_sv','m_sv_UncMet_UP')
                        plotVar = plotVar.replace('pt_sv','pt_sv_UncMet_UP')
                        plotVar = plotVar.replace('Higgs_PtCor','Higgs_PtCor_UncMet_UP')
                    if 'Down' in var[-4:] :
                        plotVar = plotVar.replace('_metUnclusteredDown','')
                        plotVar = plotVar.replace('m_sv','m_sv_UncMet_DOWN')
                        plotVar = plotVar.replace('pt_sv','pt_sv_UncMet_DOWN')
                        plotVar = plotVar.replace('Higgs_PtCor','Higgs_PtCor_UncMet_DOWN')
            elif 'JES' in shapeName :
                if 'data' in sample :
                    plotVar = varBase
                #if 'mjj:m_sv' in var :
                if 'mjj:m_sv' in var or 'mjj:m_visCor' in var :
                    # Strip _ffSub off for a comparison with the actual shifts
                    if doFF : compVar = var.replace('_ffSub','')
                    else : compVar = var
                    mass = 'm_sv' if 'm_sv' in var else 'm_visCor'
                    if 'Up' in compVar[-2:] : # Make sure we check the last 2 chars
                        #plotVar = 'vbfMass_Jet%sUp:m_sv' % jesUnc
                        plotVar = 'vbfMass_Jet%sUp:%s' % (jesUnc, mass)
                    if 'Down' in compVar[-4:] : # Make sure we check the last 4 chars
                        #plotVar = 'vbfMass_Jet%sDown:m_sv' % jesUnc
                        plotVar = 'vbfMass_Jet%sDown:%s' % (jesUnc, mass)
                else : # For this one, we adjust the additionalCuts to 
                    # provide different yields
                    plotVar = varBase
            # This is to keep the above MELA replacements intact
            elif varBase.count(':') == 2 :
                if '_Zmumu' in var :
                    plotVar = plotVar.replace('_ZmumuUp','')
                    plotVar = plotVar.replace('_ZmumuDown','')
                elif '_tauPt' in var :
                    plotVar = plotVar.replace('_tauPtUp','')
                    plotVar = plotVar.replace('_tauPtDown','')
                elif '_zPt' in var :
                    plotVar = plotVar.replace('_zPtUp','')
                    plotVar = plotVar.replace('_zPtDown','')
                elif '_JetToTau' in var :
                    plotVar = plotVar.replace('_JetToTauUp','')
                    plotVar = plotVar.replace('_JetToTauDown','')
                elif '_topPt' in var :
                    plotVar = plotVar.replace('_topPtUp','')
                    plotVar = plotVar.replace('_topPtDown','')
                elif '_ggH' in var :
                    plotVar = plotVar.replace('_ggHUp','')
                    plotVar = plotVar.replace('_ggHDown','')
                elif '_topQuarkggH' in var :
                    plotVar = plotVar.replace('_topQuarkggHUp','')
                    plotVar = plotVar.replace('_topQuarkggHDown','')
                else :
                    plotVar = plotVar
            # Else includes zPt and topPt  
            else :
                plotVar = varBase

                
        #print "Var: %s   VarBase: %s" % (var, varBase)

        ### Make sure that if we have no events
        ### we still save a blank histo for use later
        if chain.GetEntries() == 0 :
            print " #### ENTRIES = 0 #### "
            if ":" in var :
                histos[ var ] = make2DHisto( var )
            else :
                histos[ var ] = makeHisto( var, info[0], info[1], info[2])

        ### Check that the target var is in the TTrees
        elif hasattr( chain, plotVar ) or ":" in varBase :
            #print "trying"
            #if sample == 'DYJets' : print sample,"  Var:",var,"   VarBase:",varBase, "    VarPlot:",plotVar
            print "%20s  Var: %40s   VarBase: %30s    VarPlot: %s" % (sample, var, varBase, plotVar)
            if isData : # Data has no GenWeight and by def has puweight = 1
                dataES = ESCuts( esMap, 'data', channel, var )
                #print 'dataES',dataES
                chain.Draw( '%s>>%s' % (plotVar, var), '1%s%s%s' % (additionalCutToUse, dataES, ffShapeSyst) )
                histos[ var ] = gPad.GetPrimitive( var )
                if var == 'm_visCor' :
                    print 'm_visCor'
                    #print "Data Count:", histos[ var ].Integral()
                    print "Cut: %s%s" % (additionalCutToUse, dataES)
            else :

                chain.Draw( '%s>>%s' % (plotVar, var), '%s' % totalCutAndWeightMC )
                ''' No reweighting at the moment! '''
                histos[ var ] = gPad.GetPrimitive( var )
                integralPost = histos[ var ].Integral()
                if var == 'm_visCor' :
                    #print 'm_visCor'
                    print "tmpIntPost: %f" % integralPost
                    print "Cut: %s" % totalCutAndWeightMC

        # didn't have var in chain
        else : 
            del histos[ var ]
            continue

        histos[ var ].Write()

    #outFile.Write()
    #return outFile
    outFile.Close()


# Provides a list of histos to create for both channels
def getHistoDict( analysis, channel ) :
    if analysis == 'htt' :
        genVarMap = {
            #'ptCor_1' : [200, 0, 200, 10, '#tau_{1} p_{T} [GeV]', ' GeV'],
            #'ptCor_2' : [200, 0, 200, 10, '#tau_{2} p_{T} [GeV]', ' GeV'],
            #'eta_1' : [60, -3, 3, 4, '#tau_{1} Eta', ' Eta'],
            #'eta_2' : [60, -3, 3, 4, '#tau_{2} Eta', ' Eta'],
            #'phi_1' : [70, -3.5, 3.5, 7, '#tau_{1} Phi', ' Phi'],
            #'phi_2' : [70, -3.5, 3.5, 7, '#tau_{2} Phi', ' Phi'],
            ###'decayMode_1' : [15, 0, 15, 1, 't1 Decay Mode', ''],
            ###'decayMode_2' : [15, 0, 15, 1, 't2 Decay Mode', ''],
            #'m_1' : [60, 0, 3, 4, 't1 Mass [GeV]', ' GeV'],
            #'m_2' : [60, 0, 3, 4, 't2 Mass [GeV]', ' GeV'],
            ###'Z_SS' : [20, -1, 1, 1, 'Z Same Sign', ''],
            #'mjj' : [20, 0, 1000, 2, 'M_{jj} [GeV]', ' GeV'],
            ##'Z_Pt' : [100, 0, 500, 5, 'Z p_{T} [GeV]', ' GeV'],
            ##'Higgs_Pt' : [10, 0, 500, 1, 'Higgs p_{T} Uncor [GeV]', ' GeV'],
            ##'Higgs_PtCor' : [10, 0, 500, 1, 'Higgs p_{T} [GeV]', ' GeV'],
            #'pt_sv' : [10, 0, 500, 1, 'Higgs svFit p_{T} [GeV]', ' GeV'],
            #'eta_sv' : [60, -3, 3, 4, 'Higgs svFit Eta', ' Eta'],
            #'phi_sv' : [70, -3.5, 3.5, 4, 'Higgs svFit Phi', ' Phi'],
            ##'jdeta' : [20, 0, 10, 1, 'VBF Jets dEta', ' dEta'],
            ##'Z_DR' : [500, 0, 5, 20, 'Z dR', ' dR'],
            ##'Z_DPhi' : [800, -4, 4, 40, 'Z dPhi', ' dPhi'],
            ##'Z_DEta' : [1000, -5, 5, 40, 'Z dEta', ' dEta'],
            ##'LT' : [600, 0, 300, 20, 'Total LT [GeV]', ' GeV'],
            ##'Mt' : [600, 0, 400, 40, 'Total m_{T} [GeV]', ' GeV'],
            ##'met' : [250, 0, 250, 20, 'pfMet [GeV]', ' GeV'],
            ##'t1_t2_MvaMet' : [250, 0, 250, 20, 't1 t2 MvaMet [GeV]', ' GeV'],
            ##'metphi' : [80, -4, 4, 10, 'pfMetPhi', ''],
            ##'mvamet' : [100, 0, 400, 2, 'mvaMetEt [GeV]', ' GeV'],
            ##'mvametphi' : [100, -5, 5, 2, 'mvaMetPhi', ''],
            ##'bjetCISVVeto20Medium' : [60, 0, 6, 5, 'nBTag_20Medium', ''],
            ##'bjetCISVVeto30Medium' : [60, 0, 6, 5, 'nBTag_30Medium', ''],
            ##'njetspt20' : [100, 0, 10, 10, 'nJetPt20', ''],
            ##'jetVeto30' : [100, 0, 10, 10, 'nJetPt30', ''],
            ##'njetingap20' : [100, 0, 10, 10, 'njetingap20', ''],
            ###'jetVeto40' : [100, 0, 10, 10, 'nJetPt40', ''],
            ###'nbtag' : [6, 0, 6, 1, 'nBTag', ''],
            ##'bjetCISVVeto30Tight' : [60, 0, 6, 5, 'nBTag_30Tight', ''],
            ###'extraelec_veto' : [20, 0, 2, 1, 'Extra Electron Veto', ''],
            ###'extramuon_veto' : [20, 0, 2, 1, 'Extra Muon Veto', ''],
            #'jpt_1' : [400, 0, 400, 40, 'Leading Jet Pt [GeV]', ' GeV'],
            ##'jmass_1' : [400, 0, 200, 20, 'Leading Jet Mass', ' GeV'],
            #'jeta_1' : [100, -5, 5, 10, 'Leading Jet Eta', ' Eta'],
            #'jphi_1' : [70, -3.5, 3.5, 10, 'Leading Jet Phi', ' Phi'],
            #'jpt_2' : [400, 0, 200, 40, 'Second Jet Pt [GeV]', ' GeV'],
            ##'jmass_2' : [400, 0, 200, 20, 'Second Jet Mass', ' GeV'],
            #'jeta_2' : [100, -5, 5, 10, 'Second Jet Eta', ' Eta'],
            #'jphi_2' : [70, -3.5, 3.5, 10, 'Second Jet Phi', ' Phi'],
            ###'weight' : [60, -30, 30, 1, 'Gen Weight', ''],
            ##'npv' : [40, 0, 40, 2, 'Number of Vertices', ''],
            ###'npu' : [50, 1, 40, 2, 'Number of True PU Vertices', ''],
            ##'m_vis' : [30, 0, 300, 1, 'M_{vis} Uncor [GeV]', ' GeV'],
            ##'mjj:m_visCor' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
            ##'Higgs_PtCor:m_visCor' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
            ##'pt_sv:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
            ##'mt_sv' : [350, 0, 350, 10, 'Total Transverse Mass [svFit] [GeV]', ' GeV'],
            ##'mt_tot' : [3900, 0, 3900, 10, 'Total Transverse Mass [GeV]', ' GeV'],
            ###'pzetavis' : [300, 0, 300, 20, 'pZetaVis', ' GeV'],
            ###'pfpzetamis' : [300, 0, 300, 20, 'pfpZetaMis', ' GeV'],
            ###'pzetamiss' : [500, -200, 300, 20, 'pZetaMis', ' GeV'],
            'm_visCor' : [30, 0, 300, 1, 'M_{vis} [GeV]', ' GeV'],
            'Higgs_PtCor:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
            'm_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
#            'mjj:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
#
            ###'mjj:m_sv:melaD0minus_D0_0to0p2' : [300, 0, 300, 10, 'melaD0minus', ' GeV'],
            ###'mjj:m_sv:melaD0minus_D0_0p2to0p4' : [300, 0, 300, 10, 'melaD0minus', ' GeV'],
            ###'mjj:m_sv:melaD0minus_D0_0p4to0p8' : [300, 0, 300, 10, 'melaD0minus', ' GeV'],
            ###'mjj:m_sv:melaD0minus_D0_0p8to1' : [300, 0, 300, 10, 'melaD0minus', ' GeV'],

            ###'mjj:m_sv:melaD0minus_D0_0to0p2_DCPp' : [300, 0, 300, 10, 'melaD0minus_DCPp', ' GeV'],
            ###'mjj:m_sv:melaD0minus_D0_0p2to0p4_DCPp' : [300, 0, 300, 10, 'melaD0minus_DCPp', ' GeV'],
            ###'mjj:m_sv:melaD0minus_D0_0p4to0p8_DCPp' : [300, 0, 300, 10, 'melaD0minus_DCPp', ' GeV'],
            ###'mjj:m_sv:melaD0minus_D0_0p8to1_DCPp' : [300, 0, 300, 10, 'melaD0minus_DCPp', ' GeV'],

            ###'mjj:m_sv:melaD0minus_D0_0to0p2_DCPm' : [300, 0, 300, 10, 'melaD0minus_DCPm', ' GeV'],
            ###'mjj:m_sv:melaD0minus_D0_0p2to0p4_DCPm' : [300, 0, 300, 10, 'melaD0minus_DCPm', ' GeV'],
            ###'mjj:m_sv:melaD0minus_D0_0p4to0p8_DCPm' : [300, 0, 300, 10, 'melaD0minus_DCPm', ' GeV'],
            ###'mjj:m_sv:melaD0minus_D0_0p8to1_DCPm' : [300, 0, 300, 10, 'melaD0minus_DCPm', ' GeV'],

            ####'mjj:m_sv:melaDCP' : [300, 0, 300, 10, 'melaD0minus', ' GeV'],
            ###'mjj:m_sv:melaDCP_DCP_neg1to0' : [300, 0, 300, 10, 'melaD0minus', ' GeV'],
            ###'mjj:m_sv:melaDCP_DCP_0to1' : [300, 0, 300, 10, 'melaD0minus', ' GeV'],

            ###'mjj:m_sv:melaD0hplus_D0hplus_0to0p2' : [300, 0, 300, 10, 'melaD0hplus', ' GeV'],
            ###'mjj:m_sv:melaD0hplus_D0hplus_0p2to0p4' : [300, 0, 300, 10, 'melaD0hplus', ' GeV'],
            ###'mjj:m_sv:melaD0hplus_D0hplus_0p4to0p8' : [300, 0, 300, 10, 'melaD0hplus', ' GeV'],
            ###'mjj:m_sv:melaD0hplus_D0hplus_0p8to1' : [300, 0, 300, 10, 'melaD0hplus', ' GeV'],

            ###'mjj:m_sv:melaDL1_DL1_0to0p2' : [300, 0, 300, 10, 'melaDL1', ' GeV'],
            ###'mjj:m_sv:melaDL1_DL1_0p2to0p4' : [300, 0, 300, 10, 'melaDL1', ' GeV'],
            ###'mjj:m_sv:melaDL1_DL1_0p4to0p8' : [300, 0, 300, 10, 'melaDL1', ' GeV'],
            ###'mjj:m_sv:melaDL1_DL1_0p8to1' : [300, 0, 300, 10, 'melaDL1', ' GeV'],

            ###'mjj:m_sv:melaDL1Zg_DL1Zg_0to0p2' : [300, 0, 300, 10, 'melaDL1Zg', ' GeV'],
            ###'mjj:m_sv:melaDL1Zg_DL1Zg_0p2to0p4' : [300, 0, 300, 10, 'melaDL1Zg', ' GeV'],
            ###'mjj:m_sv:melaDL1Zg_DL1Zg_0p4to0p8' : [300, 0, 300, 10, 'melaDL1Zg', ' GeV'],
            ###'mjj:m_sv:melaDL1Zg_DL1Zg_0p8to1' : [300, 0, 300, 10, 'melaDL1Zg', ' GeV'],

            # For ggH studies
            'mjj:m_sv:melaDPhijj_DPhijj_0toPiOver4' : [300, 0, 300, 10, 'melaDPhijj', ' GeV'],
            'mjj:m_sv:melaDPhijj_DPhijj_piOver4toPiOver2' : [300, 0, 300, 10, 'melaDPhijj', ' GeV'],
            'mjj:m_sv:melaDPhijj_DPhijj_piOver2to3PiOver4' : [300, 0, 300, 10, 'melaDPhijj', ' GeV'],
            'mjj:m_sv:melaDPhijj_DPhijj_3PiOver4toPi' : [300, 0, 300, 10, 'melaDPhijj', ' GeV'],

            'mjj:m_sv:melaD0minusggH_D0_0to0p25' : [300, 0, 300, 10, 'melaD0minusggH', ' GeV'],
            'mjj:m_sv:melaD0minusggH_D0_0p25to0p5' : [300, 0, 300, 10, 'melaD0minusggH', ' GeV'],
            'mjj:m_sv:melaD0minusggH_D0_0p5to0p75' : [300, 0, 300, 10, 'melaD0minusggH', ' GeV'],
            'mjj:m_sv:melaD0minusggH_D0_0p75to1' : [300, 0, 300, 10, 'melaD0minusggH', ' GeV'],


            #XXX'melaDCP' : [220, -1.1, 1.1, 20, 'DCP', ' GeV'],
            #XXX'melaD0minus' : [120, -0.1, 1.1, 10, 'D0-', ' GeV'],
            #XXX'melaD0hplus' : [120, -0.1, 1.1, 10, 'D0hplus', ' GeV'],
            #XXX'melaDint' : [220, -1.1, 1.1, 20, 'Dint', ' GeV'],
            #XXX'melaDL1' : [120, -0.1, 1.1, 10, 'DL1', ' GeV'],
            #XXX'melaDL1int' : [220, -1.1, 1.1, 20, 'DL1int', ' GeV'],
            #XXX'melaDL1Zg' : [120, -0.1, 1.1, 10, 'DL1Zg', ' GeV'],
            #XXX'melaDL1Zgint' : [120, -0.1, 1.1, 10, 'DL1Zgint', ' GeV'],
            #'melaD0minus_mjj0-300' :   [120, -0.1, 1.1, 10, 'D0- (mjj [0,300])', ' GeV'],
            #'melaD0minus_mjj300-500' : [120, -0.1, 1.1, 10, 'D0- (mjj [300,500])', ' GeV'],
            #'melaD0minus_mjj500-800' : [120, -0.1, 1.1, 10, 'D0- (mjj [500,800])', ' GeV'],
            #'melaD0minus_mjj800-inf' : [120, -0.1, 1.1, 10, 'D0- (mjj [800,inf])', ' GeV'],
            #'melaD0hplus_mjj0-300' :   [120, -0.1, 1.1, 10, 'D0hplus (mjj [0,300])', ' GeV'],
            #'melaD0hplus_mjj300-500' : [120, -0.1, 1.1, 10, 'D0hplus (mjj [300,500])', ' GeV'],
            #'melaD0hplus_mjj500-800' : [120, -0.1, 1.1, 10, 'D0hplus (mjj [500,800])', ' GeV'],
            #'melaD0hplus_mjj800-inf' : [120, -0.1, 1.1, 10, 'D0hplus (mjj [800,inf])', ' GeV'],
            #'melaDint_mjj0-300' :   [240, -1.2, 1.2, 10, 'Dint (mjj [0,300])', ' GeV'],
            #'melaDint_mjj300-500' : [240, -1.2, 1.2, 10, 'Dint (mjj [300,500])', ' GeV'],
            #'melaDint_mjj500-800' : [240, -1.2, 1.2, 10, 'Dint (mjj [500,800])', ' GeV'],
            #'melaDint_mjj800-inf' : [240, -1.2, 1.2, 10, 'Dint (mjj [800,inf])', ' GeV'],
            #'melaDL1_mjj0-300' :   [120, -0.1, 1.1, 10, 'DL1 (mjj [0,300])', ' GeV'],
            #'melaDL1_mjj300-500' : [120, -0.1, 1.1, 10, 'DL1 (mjj [300,500])', ' GeV'],
            #'melaDL1_mjj500-800' : [120, -0.1, 1.1, 10, 'DL1 (mjj [500,800])', ' GeV'],
            #'melaDL1_mjj800-inf' : [120, -0.1, 1.1, 10, 'DL1 (mjj [800,inf])', ' GeV'],
            #'melaDL1int_mjj0-300' :   [240, -1.2, 1.2, 10, 'DL1int (mjj [0,300])', ' GeV'],
            #'melaDL1int_mjj300-500' : [240, -1.2, 1.2, 10, 'DL1int (mjj [300,500])', ' GeV'],
            #'melaDL1int_mjj500-800' : [240, -1.2, 1.2, 10, 'DL1int (mjj [500,800])', ' GeV'],
            #'melaDL1int_mjj800-inf' : [240, -1.2, 1.2, 10, 'DL1int (mjj [800,inf])', ' GeV'],
            #'melaDL1Zg_mjj0-300' :   [120, -0.1, 1.1, 10, 'DL1Zg (mjj [0,300])', ' GeV'],
            #'melaDL1Zg_mjj300-500' : [120, -0.1, 1.1, 10, 'DL1Zg (mjj [300,500])', ' GeV'],
            #'melaDL1Zg_mjj500-800' : [120, -0.1, 1.1, 10, 'DL1Zg (mjj [500,800])', ' GeV'],
            #'melaDL1Zg_mjj800-inf' : [120, -0.1, 1.1, 10, 'DL1Zg (mjj [800,inf])', ' GeV'],
            #'melaDL1Zgint_mjj0-300' :   [120, -0.1, 1.1, 10, 'DL1Zgint (mjj [0,300])', ' GeV'],
            #'melaDL1Zgint_mjj300-500' : [120, -0.1, 1.1, 10, 'DL1Zgint (mjj [300,500])', ' GeV'],
            #'melaDL1Zgint_mjj500-800' : [120, -0.1, 1.1, 10, 'DL1Zgint (mjj [500,800])', ' GeV'],
            #'melaDL1Zgint_mjj800-inf' : [120, -0.1, 1.1, 10, 'DL1Zgint (mjj [800,inf])', ' GeV'],
            #'melaDPhiUnsignedjj' : [100, -4, 4, 5, 'Unsigned dPhi_jj', ' dPhi'],
            #XXX'melaDPhijj' : [100, -4, 4, 10, 'dPhi_jj', ' dPhi'],
            #XXX'melaDEtajj' : [100, -10, 10, 10, 'dEta_jj', ' dEta'],
            #XXX'melaSqrtQ2V1' : [70, 0, 700, 5, 'Q_V1 [GeV]', ' GeV'],
            #XXX'melaSqrtQ2V2' : [70, 0, 700, 5, 'Q_V2 [GeV]', ' GeV'],
            #XXX'melaAvgSqrtQ2V12' : [70, 0, 700, 5, 'Avg(Q_V1,Q_V2) [GeV]', ' GeV'],
            #'melaDPhijj_mjj0-300' :   [100, -4, 4, 5, 'dPhi_jj (mjj [0,300])', ' GeV'],
            #'melaDPhijj_mjj300-500' : [100, -4, 4, 5, 'dPhi_jj (mjj [300,500])', ' GeV'],
            #'melaDPhijj_mjj500-800' : [100, -4, 4, 5, 'dPhi_jj (mjj [500,800])', ' GeV'],
            #'melaDPhijj_mjj800-inf' : [100, -4, 4, 5, 'dPhi_jj (mjj [800,inf])', ' GeV'],
        }

        ''' added shape systematics '''
        #toAdd = ['pt_sv:m_sv', 'mjj:m_sv', 'm_visCor', 'm_sv'] # No extra shapes
        #toAdd = ['pt_sv:m_sv', 'mjj:m_sv', 'm_sv', 'Higgs_PtCor:m_sv'] # No extra shapes
        #toAdd = ['Higgs_PtCor:m_visCor', 'mjj:m_visCor', 'm_visCor'] # No extra shapes
        #toAdd = [] # No extra shapes
        toAdd = [
            'mjj:m_sv', 
            'm_sv',
            'Higgs_PtCor:m_sv',

            'mjj:m_sv:melaDPhijj_DPhijj_0toPiOver4',
            'mjj:m_sv:melaDPhijj_DPhijj_piOver4toPiOver2',
            'mjj:m_sv:melaDPhijj_DPhijj_piOver2to3PiOver4',
            'mjj:m_sv:melaDPhijj_DPhijj_3PiOver4toPi',

            'mjj:m_sv:melaD0minusggH_D0_0to0p25',
            'mjj:m_sv:melaD0minusggH_D0_0p25to0p5',
            'mjj:m_sv:melaD0minusggH_D0_0p5to0p75',
            'mjj:m_sv:melaD0minusggH_D0_0p75to1',

            ###'mjj:m_sv:melaD0minus_D0_0to0p2',
            ###'mjj:m_sv:melaD0minus_D0_0p2to0p4',
            ###'mjj:m_sv:melaD0minus_D0_0p4to0p8',
            ###'mjj:m_sv:melaD0minus_D0_0p8to1',

            ###'mjj:m_sv:melaD0minus_D0_0to0p2_DCPp',
            ###'mjj:m_sv:melaD0minus_D0_0p2to0p4_DCPp',
            ###'mjj:m_sv:melaD0minus_D0_0p4to0p8_DCPp',
            ###'mjj:m_sv:melaD0minus_D0_0p8to1_DCPp',

            ###'mjj:m_sv:melaD0minus_D0_0to0p2_DCPm',
            ###'mjj:m_sv:melaD0minus_D0_0p2to0p4_DCPm',
            ###'mjj:m_sv:melaD0minus_D0_0p4to0p8_DCPm',
            ###'mjj:m_sv:melaD0minus_D0_0p8to1_DCPm',

            ###'mjj:m_sv:melaD0hplus_D0hplus_0to0p2',
            ###'mjj:m_sv:melaD0hplus_D0hplus_0p2to0p4',
            ###'mjj:m_sv:melaD0hplus_D0hplus_0p4to0p8',
            ###'mjj:m_sv:melaD0hplus_D0hplus_0p8to1',

            ###'mjj:m_sv:melaDL1_DL1_0to0p2',
            ###'mjj:m_sv:melaDL1_DL1_0p2to0p4',
            ###'mjj:m_sv:melaDL1_DL1_0p4to0p8',
            ###'mjj:m_sv:melaDL1_DL1_0p8to1',

            ###'mjj:m_sv:melaDL1Zg_DL1Zg_0to0p2',
            ###'mjj:m_sv:melaDL1Zg_DL1Zg_0p2to0p4',
            ###'mjj:m_sv:melaDL1Zg_DL1Zg_0p4to0p8',
            ###'mjj:m_sv:melaDL1Zg_DL1Zg_0p8to1',

            ###'mjj:m_sv:melaDCP_DCP_neg1to0',
            ###'mjj:m_sv:melaDCP_DCP_0to1',
        ] # All aHTT Shapes
        #toAdd = [] # No extra shapes
        varsForShapeSyst = []
        for item in toAdd :
            varsForShapeSyst.append( item )
        #shapesToAdd = ['energyScale', 'tauPt', 'topPt', 'zPt']
        shapesToAdd = {
                    'energyScaleAll':'TES All',
                    'energyScaleDM0':'TES DM0',
                    'energyScaleDM1':'TES DM1',
                    'energyScaleDM10':'TES DM10',
                    'zPt':'Z p_{T}/Mass Reweight',
                    #'metResponse':'Met Response',
                    #'metResolution':'Met Resolution',
                    'tauPt':'High P_{T} Tau',
                    'topPt':'Top P_{T} Reweight',
                    'JES' : 'Jet Energy Scale',
                    'JetToTau' : 'Jet to Tau Fake',
                    'ggH' : 'ggH Scale',
                    'topQuarkggH' : 'Top Quark Scale for ggH',
                    'Zmumu' : 'Z mumu DY Reweight',
                    'metClustered':'Clustered MET',
                    'metUnclustered':'Unclustered MET',
                    }

        # Add FF shape systs if doFF
        doFF = getenv('doFF', type=bool)
        if doFF :
            shapesToAdd['qcdffSyst']   = 'FF QCD Syst'
            shapesToAdd['ttbarffSyst'] = 'FF ttbar Syst'
            shapesToAdd['wjetsffSyst'] = 'FF WJets Syst'
            shapesToAdd['0jet1prongffStat'] = 'FF 0Jet 1Prong Stat'
            shapesToAdd['0jet3prongffStat'] = 'FF 0Jet 3Prong Stat'
            shapesToAdd['1jet1prongffStat'] = 'FF 1Jet 1Prong Stat'
            shapesToAdd['1jet3prongffStat'] = 'FF 1Jet 3Prong Stat'

        # Add Full JES shapes if doFullJES
        doFullJES = getenv('doFullJES', type=bool)
        if doFullJES :
            # Remove standard JES
            if 'JES' in shapesToAdd.keys() : del shapesToAdd['JES']
            from util.jetEnergyScale import getUncerts
            uncerts = getUncerts()
            for uncert in uncerts :
                shapesToAdd['JES'+uncert] = 'JES '+uncert 
                shapesToAdd['JES'+uncert] = 'JES '+uncert


        for var in genVarMap.keys() :
            if var in varsForShapeSyst :
                for shape, app in shapesToAdd.iteritems() :
                    genVarMap[ var+'_'+shape+'Up' ] = list(genVarMap[ var ])
                    genVarMap[ var+'_'+shape+'Up' ][4] = genVarMap[ var+'_'+shape+'Up' ][4]+' '+app+' UP'
                    genVarMap[ var+'_'+shape+'Down' ] = list(genVarMap[ var ])
                    genVarMap[ var+'_'+shape+'Down' ][4] = genVarMap[ var+'_'+shape+'Down' ][4]+' '+app+' Down'
            

        return genVarMap







