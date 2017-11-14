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



# Make a 2D histo
def get2DVars( cutName ) :
    if 'pt_sv' in cutName and 'm_sv' in cutName :
        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,100,170,300,10000] )
    if 'mjj' in cutName and 'm_sv' in cutName :
        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,300,500,800,10000] )
    if 'Higgs_PtCor' in cutName and 'm_sv' in cutName :
        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,100,170,300,10000] )
    if 'Higgs_PtCor' in cutName and 'm_visCor' in cutName :
        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
        yBins = array( 'd', [0,100,170,300,10000] )
    if 'mjj' in cutName and 'm_visCor' in cutName :
        xBins = array( 'd', [0,40,60,70,80,90,100,110,120,130,150,200,250] )
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
        # Also covers the Gluon Fusion WG1 Uncert Scheme now too (wg1-THU-ggH-*)
        elif '_ggH' in var or '-ggH-' in var :
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

    for var, info in newVarMap.iteritems() :
        if skipSSQCDDetails and not (var == 'eta_1' or var == 'm_visCor')  : continue

        ''' Skip plotting 2D vars for 0jet and inclusive selections '''
        if 'ZTTinclusive' in outFile.GetName() or 'ZTT0jet' in outFile.GetName() :
            if ":" in var : continue

        #print var


        ''' Skip plotting unused shape systematics '''
        if skipSystShapeVar( var, sample, channel, genCode ) : continue

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
        elif '_ggH' in var or '-ggH-' in var :
            if 'wg1-THU-ggH-' in var :
                shiftDir = ''
                if   'wg1-THU-ggH-MuUp' in var :      shapeSyst = '*(THU_ggH_Mu)'
                elif 'wg1-THU-ggH-MuDown' in var :    shapeSyst = '*(1./THU_ggH_Mu)'
                elif 'wg1-THU-ggH-ResUp' in var :     shapeSyst = '*(THU_ggH_Res)'
                elif 'wg1-THU-ggH-ResDown' in var :   shapeSyst = '*(1./THU_ggH_Res)'
                elif 'wg1-THU-ggH-Mig01Up' in var :   shapeSyst = '*(THU_ggH_Mig01)'
                elif 'wg1-THU-ggH-Mig01Down' in var : shapeSyst = '*(1./THU_ggH_Mig01)'
                elif 'wg1-THU-ggH-Mig12Up' in var :   shapeSyst = '*(THU_ggH_Mig12)'
                elif 'wg1-THU-ggH-Mig12Down' in var : shapeSyst = '*(1./THU_ggH_Mig12)'
                elif 'wg1-THU-ggH-VBF2jUp' in var :   shapeSyst = '*(THU_ggH_VBF2j)'
                elif 'wg1-THU-ggH-VBF2jDown' in var : shapeSyst = '*(1./THU_ggH_VBF2j)'
                elif 'wg1-THU-ggH-VBF3jUp' in var :   shapeSyst = '*(THU_ggH_VBF3j)'
                elif 'wg1-THU-ggH-VBF3jDown' in var : shapeSyst = '*(1./THU_ggH_VBF3j)'
                elif 'wg1-THU-ggH-PT60Up' in var :    shapeSyst = '*(THU_ggH_PT60)'
                elif 'wg1-THU-ggH-PT60Down' in var :  shapeSyst = '*(1./THU_ggH_PT60)'
                elif 'wg1-THU-ggH-PT120Up' in var :   shapeSyst = '*(THU_ggH_PT120)'
                elif 'wg1-THU-ggH-PT120Down' in var : shapeSyst = '*(1./THU_ggH_PT120)'
                elif 'wg1-THU-ggH-qmtopUp' in var :   shapeSyst = '*(THU_ggH_qmtop)'
                elif 'wg1-THU-ggH-qmtopDown' in var : shapeSyst = '*(1./THU_ggH_qmtop)'
            else : # normal ggH Scale
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
            if '_ZmumuUp' in var and 'ZTTvbf' in outFile.GetName() :
                shapeSyst = '*(1. + zmumuVBFWeight)'
            elif '_ZmumuDown' in var and 'ZTTvbf' in outFile.GetName() :
                shapeSyst = '*(1./(1. + zmumuVBFWeight))'


        # Add the Zmumu CR normalizations from Cecile's studies
        # from Nov 18, 2016 SM-HTT
        # Update 2 Mar, 2017:
        # - VBF has specific shape correction too
        # Removed 2% global normalization adjustment, April 4, 2017
        if 'DYJets' in sample or 'EWKZ' in sample :
            if 'ZTTvbf' in outFile.GetName() :
                shapeSyst += '*(1.00 + zmumuVBFWeight)'
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

        #print "%s     High Pt Tau Weight: %s" % (var, tauW)
        #print var,shapeSyst
        if 'NNLOPS' in sample :
            # Current NNLOPS sample calculated as lheweight9 = lhe[9].wgt / abs(GenWeight), we need to undo that
            totalCutAndWeightMC = '(lheweight9*abs(GenWeight))%s%s%s%s%s' % (additionalCutToUse, sfs, xsec, shapeSyst, ffShapeSyst) 
        else :
            totalCutAndWeightMC = '(GenWeight/abs( GenWeight ))%s%s%s%s%s' % (additionalCutToUse, sfs, xsec, shapeSyst, ffShapeSyst) 
        #print totalCutAndWeightMC


        # Check if the variable to plot is in the chain, if not, skip it
        # don't crash on systematics based variables
        varBase = var.replace('_ffSub','')
        plotVar = var.replace('_ffSub','') # remove the histo naming off the back of the plotting var
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
            #'Z_SS' : [20, -1, 1, 1, 'Z Same Sign', ''],
#XXX            'mjj' : [20, 0, 1000, 1, 'M_{jj} [GeV]', ' GeV'],
#FIXME            'Z_Pt' : [100, 0, 500, 5, 'Z p_{T} [GeV]', ' GeV'],
#            'Higgs_Pt' : [10, 0, 500, 1, 'Higgs p_{T} Uncor [GeV]', ' GeV'],
#XXX            'Higgs_PtCor' : [10, 0, 500, 1, 'Higgs p_{T} [GeV]', ' GeV'],
#XXX            'pt_sv' : [10, 0, 500, 1, 'Higgs svFit p_{T} [GeV]', ' GeV'],
#FIXME            'jdeta' : [20, 0, 10, 1, 'VBF Jets dEta', ' dEta'],
#FIXME#            'Z_DR' : [500, 0, 5, 20, 'Z dR', ' dR'],
#FIXME#            'Z_DPhi' : [800, -4, 4, 40, 'Z dPhi', ' dPhi'],
#FIXME#            'Z_DEta' : [1000, -5, 5, 40, 'Z dEta', ' dEta'],
#FIXME#            'LT' : [600, 0, 300, 20, 'Total LT [GeV]', ' GeV'],
#FIXME#            'Mt' : [600, 0, 400, 40, 'Total m_{T} [GeV]', ' GeV'],
#FIXME            'met' : [250, 0, 250, 20, 'pfMet [GeV]', ' GeV'],
#FIXME#            't1_t2_MvaMet' : [250, 0, 250, 20, 't1 t2 MvaMet [GeV]', ' GeV'],
#FIXME            'metphi' : [80, -4, 4, 10, 'pfMetPhi', ''],
#FIXME#            'mvamet' : [100, 0, 400, 2, 'mvaMetEt [GeV]', ' GeV'],
#FIXME#            'mvametphi' : [100, -5, 5, 2, 'mvaMetPhi', ''],
#FIXME#            'bjetCISVVeto20Medium' : [60, 0, 6, 5, 'nBTag_20Medium', ''],
#FIXME#            'bjetCISVVeto30Medium' : [60, 0, 6, 5, 'nBTag_30Medium', ''],
#FIXME#            'njetspt20' : [100, 0, 10, 10, 'nJetPt20', ''],
#XXX            'jetVeto30' : [100, 0, 10, 10, 'nJetPt30', ''],
#FIXME            'njetingap20' : [100, 0, 10, 10, 'njetingap20', ''],
#FIXME#            #'jetVeto40' : [100, 0, 10, 10, 'nJetPt40', ''],
#FIXME#            #'nbtag' : [6, 0, 6, 1, 'nBTag', ''],
#FIXME#            'bjetCISVVeto30Tight' : [60, 0, 6, 5, 'nBTag_30Tight', ''],
#FIXME#            #'extraelec_veto' : [20, 0, 2, 1, 'Extra Electron Veto', ''],
#FIXME#            #'extramuon_veto' : [20, 0, 2, 1, 'Extra Muon Veto', ''],
#FIXME            'jpt_1' : [400, 0, 200, 20, 'Leading Jet Pt', ' GeV'],
#FIXME#            'jeta_1' : [100, -5, 5, 10, 'Leading Jet Eta', ' Eta'],
#FIXME            'jpt_2' : [400, 0, 200, 20, 'Second Jet Pt', ' GeV'],
#FIXME#            'jeta_2' : [100, -5, 5, 10, 'Second Jet Eta', ' Eta'],
#FIXME#            #'weight' : [60, -30, 30, 1, 'Gen Weight', ''],
#FIXME#            'npv' : [40, 0, 40, 2, 'Number of Vertices', ''],
#FIXME            #'npu' : [50, 1, 40, 2, 'Number of True PU Vertices', ''],
#            'm_vis' : [30, 0, 300, 1, 'M_{vis} Uncor [GeV]', ' GeV'],
            'm_visCor' : [30, 0, 300, 1, 'M_{vis} [GeV]', ' GeV'],
#XXX            'mjj:m_visCor' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
#XXX            'Higgs_PtCor:m_visCor' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
            'Higgs_PtCor:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
            'm_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
#XXX            'pt_sv:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
            'mjj:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
#            'mt_sv' : [350, 0, 350, 10, 'Total Transverse Mass [svFit] [GeV]', ' GeV'],
#            'mt_tot' : [3900, 0, 3900, 10, 'Total Transverse Mass [GeV]', ' GeV'],
            #'pzetavis' : [300, 0, 300, 20, 'pZetaVis', ' GeV'],
            #'pfpzetamis' : [300, 0, 300, 20, 'pfpZetaMis', ' GeV'],
            #'pzetamiss' : [500, -200, 300, 20, 'pZetaMis', ' GeV'],
        }

        ''' added shape systematics '''
        #toAdd = ['pt_sv:m_sv', 'mjj:m_sv', 'm_visCor', 'm_sv'] # No extra shapes
        toAdd = ['pt_sv:m_sv', 'mjj:m_sv', 'm_sv', 'Higgs_PtCor:m_sv'] # No extra shapes
        #toAdd = ['Higgs_PtCor:m_visCor', 'mjj:m_visCor', 'm_visCor'] # No extra shapes
        #toAdd = ['m_sv', ] # No extra shapes
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
                    'wg1-THU-ggH-Mu' : 'wg1-THU-ggH-Mu',
                    'wg1-THU-ggH-Res' : 'wg1-THU-ggH-Res',
                    'wg1-THU-ggH-Mig01' : 'wg1-THU-ggH-Mig01',
                    'wg1-THU-ggH-Mig12' : 'wg1-THU-ggH-Mig12',
                    'wg1-THU-ggH-VBF2j' : 'wg1-THU-ggH-VBF2j',
                    'wg1-THU-ggH-VBF3j' : 'wg1-THU-ggH-VBF3j',
                    'wg1-THU-ggH-PT60' : 'wg1-THU-ggH-PT60',
                    'wg1-THU-ggH-PT120' : 'wg1-THU-ggH-PT120',
                    'wg1-THU-ggH-qmtop' : 'wg1-THU-ggH-qmtop',
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
            

        # Provides a list of histos to create for 'TT' channel
        if channel == 'tt' :
            chanVarMapTT = {
#                'pt_1' : [200, 0, 200, 5, '#tau_{1} p_{T} Uncor [GeV]', ' GeV'],
#                'pt_2' : [200, 0, 200, 5, '#tau_{2} p_{T} Uncor [GeV]', ' GeV'],
#                'ptCor_1' : [200, 0, 200, 5, '#tau_{1} p_{T} [GeV]', ' GeV'],
#                'ptCor_2' : [200, 0, 200, 5, '#tau_{2} p_{T} [GeV]', ' GeV'],
##FIXME                'gen_match_1' : [14, 0, 7, 1, '#tau_{1} Gen Match', ''],
#                'eta_1' : [60, -3, 3, 4, '#tau_{1} Eta', ' Eta'],
#                'eta_2' : [60, -3, 3, 4, '#tau_{2} Eta', ' Eta'],
#                'decayMode_1' : [15, 0, 15, 1, 't1 Decay Mode', ''],
#                'decayMode_2' : [15, 0, 15, 1, 't2 Decay Mode', ''],
#FIXME                'iso_1' : [100, -1, 1, 1, '#tau_{1} MVArun2v1DBoldDMwLTraw', ''],
#FIXME#                'chargedIsoPtSum_1' : [100, 0, 5, 1, '#tau_{1} charge iso pt sum', ' GeV'],
#FIXME#                'chargedIsoPtSum_2' : [100, 0, 5, 1, '#tau_{2} charge iso pt sum', ' GeV'],
#FIXME#                'chargedIsoPtSumdR03_1' : [100, 0, 5, 1, '#tau_{1} charge iso pt sum dR03', ' GeV'],
#FIXME#                'chargedIsoPtSumdR03_2' : [100, 0, 5, 1, '#tau_{2} charge iso pt sum dR03', ' GeV'],
#FIXME                'gen_match_2' : [14, 0, 7, 1, '#tau_{2} Gen Match', ''],
#FIXME                'iso_2' : [100, -1, 1, 1, '#tau_{2} MVArun2v1DBoldDMwLTraw', ''],
#FIXME#                #'t1JetPt' : [400, 0, 400, 20, 't1 Overlapping Jet Pt', ' GeV'],
#FIXME#                'm_1' : [60, 0, 3, 4, 't1 Mass', ' GeV'],
#                #'t2JetPt' : [400, 0, 400, 20, 't2 Overlapping Jet Pt', ' GeV'],
#                'm_2' : [60, 0, 3, 4, 't2 Mass', ' GeV'],
                #'t1ChargedIsoPtSum' : [0, 10, 8, 't1 ChargedIsoPtSum', ' GeV'],
                #'t1NeutralIsoPtSum' : [0, 10, 8, 't1 NeutralIsoPtSum', ' GeV'],
                #'t1PuCorrPtSum' : [0, 40, 4, 't1 PuCorrPtSum', ' GeV'],
                #'t2ChargedIsoPtSum' : [0, 10, 8, 't2 ChargedIsoPtSum', ' GeV'],
                #'t2NeutralIsoPtSum' : [0, 10, 8, 't2 NeutralIsoPtSum', ' GeV'],
                #'t2PuCorrPtSum' : [0, 40, 4, 't2 PuCorrPtSum', ' GeV'],
            }
            for key in chanVarMapTT.keys() :
                genVarMap[ key ] = chanVarMapTT[ key ]
            return genVarMap
    if analysis == 'azh' :
        genVarMap = {
#            'Z_Pt' : [400, 0, 400, 40, 'Z p_{T} [GeV]', ' GeV'],
#            'Z_DR' : [500, 0, 5, 50, 'Z dR', ' dR'],
#            'Z_DPhi' : [800, -4, 4, 80, 'Z dPhi', ' dPhi'],
#            'Z_DEta' : [100, -5, 5, 10, 'Z dEta', ' dEta'],
#            'mjj' : [40, 0, 800, 1, 'M_{jj}', ' [GeV]'],
#            'jdeta' : [100, -5, 5, 10, 'VBF dEta', ' dEta'],
            'm_vis' : [80, 50, 130, 10, 'Z Mass [GeV]', ' GeV'],
            'H_vis' : [400, 0, 400, 40, 'H Visible Mass [GeV]', ' GeV'],
            'Mass' : [600, 0, 600, 60, 'M_{ll#tau#tau} [GeV]', ' GeV'],
            'LT' : [600, 0, 600, 40, 'Total LT [GeV]', ' GeV'],
            'Mt' : [600, 0, 600, 40, 'Total m_{T} [GeV]', ' GeV'],
            'LT_higgs' : [150, 0, 150, 10, 'LT_{higgs} [GeV]', ' GeV'],
#            'met' : [250, 0, 250, 20, 'pfMet [GeV]', ' GeV'],
            'zhFR0' : [50, 0, 0.5, 2, 'ZH FakeRate Weight 0', ''],
            'zhFR1' : [50, 0, 0.5, 2, 'ZH FakeRate Weight 1', ''],
            'zhFR2' : [50, 0, 0.5, 2, 'ZH FakeRate Weight 2', ''],
            'pt_1' : [200, 0, 200, 10, 'Leg1 p_{T} [GeV]', ' GeV'],
            'pt_2' : [200, 0, 200, 10, 'Leg2 p_{T} [GeV]', ' GeV'],
            'pt_3' : [200, 0, 200, 10, 'Leg3 p_{T} [GeV]', ' GeV'],
            'pt_4' : [200, 0, 200, 10, 'Leg4 p_{T} [GeV]', ' GeV'],
#            'eta_1' : [60, -3, 3, 10, 'Leg1 Eta', ' Eta'],
#            'eta_2' : [60, -3, 3, 10, 'Leg2 Eta', ' Eta'],
#            'eta_3' : [60, -3, 3, 10, 'Leg3 Eta', ' Eta'],
#            'eta_4' : [60, -3, 3, 10, 'Leg4 Eta', ' Eta'],
#            'iso_1' : [20, 0, 0.5, 1, 'Leg1 RelIsoDB03', ''],
#            'iso_2' : [20, 0, 0.5, 1, 'Leg2 RelIsoDB03', ''],
            'iso_3' : [20, 0, 1, 1, 'Leg3 Iso', ''],
            'iso_4' : [20, 0, 1, 1, 'Leg4 Iso', ''],
            #'jpt_1' : [400, 0, 200, 20, 'Leading Jet Pt', ' GeV'],
            #'jeta_1' : [100, -5, 5, 10, 'Leading Jet Eta', ' Eta'],
            #'jpt_2' : [400, 0, 200, 20, 'Second Jet Pt', ' GeV'],
            #'jeta_2' : [100, -5, 5, 10, 'Second Jet Eta', ' Eta'],
            #'weight' : [60, -30, 30, 1, 'Gen Weight', ''],
#            'npv' : [40, 0, 40, 4, 'Number of Vertices', ''],
##            'njetspt20' : [100, 0, 10, 10, 'nJetPt20', ''],
#            'jetVeto30' : [100, 0, 10, 10, 'nJetPt30', ''],
##            'azhWeight' : [50, 0, 2, 1, 'Muon + Electron Weights', ''],
#            'muVetoZTTp001dxyz' : [6, -1, 5, 1, 'muVetoZTTp001dxyz', ''],
#            'eVetoZTTp001dxyz' : [6, -1, 5, 1, 'eVetoZTTp001dxyz', ''],
#            'muVetoZTTp001dxyzR0' : [6, -1, 5, 1, 'muVetoZTTp001dxyzR0', ''],
#            'eVetoZTTp001dxyzR0' : [6, -1, 5, 1, 'eVetoZTTp001dxyzR0', ''],
#            'bjetCISVVeto20Medium' : [60, 0, 6, 5, 'nBTag_20Medium', ''],
#            'bjetCISVVeto30Medium' : [60, 0, 6, 5, 'nBTag_30Medium', ''],
#            'bjetCISVVeto30Tight' : [60, 0, 6, 5, 'nBTag_30Tight', ''],
        }
        llltMap = {
#            'againstElectronVLooseMVA6_4' : [9, -1, 2, 1, 'Against E VL MVA6 Leg 4', ''],
#            'againstElectronLooseMVA6_4' : [9, -1, 2, 1, 'Against E L MVA6 Leg 4', ''],
#            'againstMuonLoose3_4' : [9, -1, 2, 1, 'Against M Loose 3 Leg 4', ''],
#            'againstMuonTight3_4' : [9, -1, 2, 1, 'Against M Tight 3 Leg 4', ''],
        }
        llttMap = {
#            'againstElectronVLooseMVA6_3' : [9, -1, 2, 1, 'Against E VL MVA6 Leg 3', ''],
#            'againstElectronLooseMVA6_3' : [9, -1, 2, 1, 'Against E L MVA6 Leg 3', ''],
#            'againstMuonLoose3_3' : [9, -1, 2, 1, 'Against M Loose 3 Leg 3', ''],
#            'againstMuonTight3_3' : [9, -1, 2, 1, 'Against M Tight 3 Leg 3', ''],
        }
        if channel == 'xxxx' :
            return genVarMap
        if channel in ['eeet', 'eemt', 'eett', 'emmt', 'mmmt', 'mmtt'] :
            for var in llltMap.keys() :
                genVarMap[var] = llltMap[ var ]
        if channel in ['eett', 'mmtt'] :
            for var in llttMap.keys() :
                genVarMap[var] = llttMap[ var ]
        return genVarMap







