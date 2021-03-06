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
def get2DVars( cutName, channel ) :
    if 'LT_higgs' in cutName and 'm_sv' in cutName :
        xBins = array( 'd', [i*20 for i in range( 1, 12 )] )
        if channel in ['eeet','emmt'] :
            yBins = array( 'd', [0,60,10000] )
        elif channel in ['eemt','mmmt'] :
            yBins = array( 'd', [0,60,10000] )
        elif channel in ['eett','mmtt'] :
            yBins = array( 'd', [0,75,10000] )
        elif channel in ['eeem','emmm'] :
            yBins = array( 'd', [0,50,10000] )
        else :
            yBins = array( 'd', [0,20,30,40,50,60,70,80,10000] )
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
def make2DHisto( cutName, channel ) :
    info = get2DVars( cutName, channel )
    xBins = info[0]
    yBins = info[1]
    hist = ROOT.TH2D( cutName, cutName, len(xBins)-1, xBins, len(yBins)-1, yBins )
    return hist



# Get the mass window cuts for AZH
# it was shown that cutting on m_sv mass window increases significance.
# Mass window cut depends on systematic shifts too
def getMassWindowCut( var, sample, genCode, outFileName ) :
    
    if 'data' in sample or 'RedBkg' in genCode or 'RedBkg' in outFileName :
        return '*(90 < m_sv && m_sv < 180)'

    if '_DM0_UP'            in var : return '*(90 < m_sv_DM0_UP && m_sv_DM0_UP < 180)'
    if '_DM0_DOWN'          in var : return '*(90 < m_sv_DM0_DOWN && m_sv_DM0_DOWN < 180)'
    if '_DM1_UP'            in var : return '*(90 < m_sv_DM1_UP && m_sv_DM1_UP < 180)'
    if '_DM1_DOWN'          in var : return '*(90 < m_sv_DM1_DOWN && m_sv_DM1_DOWN < 180)'
    if '_DM10_UP'           in var : return '*(90 < m_sv_DM10_UP && m_sv_DM10_UP < 180)'
    if '_DM10_DOWN'         in var : return '*(90 < m_sv_DM10_DOWN && m_sv_DM10_DOWN < 180)'
    if '_EES_UP'            in var : return '*(90 < m_sv_EES_UP && m_sv_EES_UP < 180)'
    if '_EES_DOWN'          in var : return '*(90 < m_sv_EES_DOWN && m_sv_EES_DOWN < 180)'
    if '_UncMet_UP'         in var : return '*(90 < m_sv_UncMet_UP && m_sv_UncMet_UP < 180)'
    if '_UncMet_DOWN'       in var : return '*(90 < m_sv_UncMet_DOWN && m_sv_UncMet_DOWN < 180)'
    if '_ClusteredMet_UP'   in var : return '*(90 < m_sv_ClusteredMet_UP && m_sv_ClusteredMet_UP < 180)'
    if '_ClusteredMet_DOWN' in var : return '*(90 < m_sv_ClusteredMet_DOWN && m_sv_ClusteredMet_DOWN < 180)'
    else : return '*(90 < m_sv && m_sv < 180)'



def skipSystShapeVar( var, sample, channel, genCode='x', outFileName='x' ) :
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
            if 'RedBkg' in sample : return True
            if 'RedBkg' in genCode : return True

        # prompt MC scaling for reducible background estimation in ZH
        elif '_promptMC' in var :
            if not ('RedBkg' in sample or 'RedBkg' in outFileName) : return True

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
            if 'RedBkg' in genCode : return True
            if 'RedBkg' in sample : return True

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
    if 'data' in sample or 'RedBkg' in sample :
        if channel == 'tt' :
            return '*(pt_1 > %s && pt_2 > %s)' % (tau1PtCut, tau2PtCut)
        if len( channel ) == 4 :
            # list to force copy
            # Data not shifted pT for taus
            return str( ESMap['_NoShift'] ).replace('shiftedPt','pt')

    if 'energyScale' not in var : return ESMap['_NoShift']

    shiftDir = ''
    if 'Up' in var[-2:] : shiftDir = 'Up'
    elif 'Down' in var[-4:] : shiftDir = 'Down'

    if channel == 'tt' :
        if '_energyScaleAll'+shiftDir in var : return ESMap['_energyScaleAll'+shiftDir]
        if '_energyScaleDM0'+shiftDir in var : return ESMap['_energyScaleDM0'+shiftDir]
        if '_energyScaleDM1'+shiftDir in var : return ESMap['_energyScaleDM1'+shiftDir]
        if '_energyScaleDM10'+shiftDir in var : return ESMap['_energyScaleDM10'+shiftDir]
    if len( channel ) == 4 :
        if channel in ['eeet','eemt','eett','eeem','eeee','emmt','emmm'] :
            if '_energyScaleEES'+shiftDir in var : return ESMap['_energyScaleEES'+shiftDir]
        if channel in ['eeet','eemt','eett','emmt','mmmt','mmtt'] :
            if '_energyScaleAll'+shiftDir in var : return ESMap['_energyScaleAll'+shiftDir]
            if '_energyScaleDM0'+shiftDir in var : return ESMap['_energyScaleDM0'+shiftDir]
            if '_energyScaleDM1'+shiftDir in var : return ESMap['_energyScaleDM1'+shiftDir]
            if '_energyScaleDM10'+shiftDir in var : return ESMap['_energyScaleDM10'+shiftDir]
    return ESMap['_NoShift']

def getESMap( channel ) :
    tau2PtCut = 40.
    tau1PtCut = 50.
    elecPtCut = 10.
    muonPtCut = 10.
    tauPtCut = 20.
    # Copied from analysisCuts.py, this is for the ZEE events where extra events might pass trigger
    # This will not work for now as the trigger filters are applied pre-svFit on the ZEE electrons
    # Perhapse another svFit round will take care of this...
    #eeTrigFilters = 'pt_1 > 27.5 && pt_2 > 17.5 && ( (e1MatchesDoubleE23_12Filter > 0.5 && e2MatchesDoubleE23_12Filter > 0.5 ) || ( pt_1 > 32 && e1MatchesSingleETight27Filter > 0.5 ) || ( pt_2 > 32 && e2MatchesSingleETight27Filter > 0.5 ) )'
    #eeTrigFiltersUp = eeTrigFilters.replace('pt_1','leg1_EES_Up').replace('pt_2','leg2_EES_Up')
    #eeTrigFiltersDown = eeTrigFilters.replace('pt_1','leg1_EES_Down').replace('pt_2','leg2_EES_Down')
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
            '_NoShift' : '*(ptCor_1 > %s && ptCor_2 > %s)' % (tau1PtCut, tau2PtCut)
        },

        # ZH
        'eeet' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && shiftedPt_4 > %s)' % (elecPtCut, elecPtCut, elecPtCut, tauPtCut),
            '_energyScaleEESUp' : '*(leg1_EES_Up > %s && leg2_EES_Up > %s && leg3_EES_Up > %s && shiftedPt_4 > %s)' % (elecPtCut, elecPtCut, elecPtCut, tauPtCut),
            '_energyScaleEESDown' : '*(leg1_EES_Down > %s && leg2_EES_Down > %s && leg3_EES_Down > %s && shiftedPt_4 > %s)' % (elecPtCut, elecPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM0Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM0_Up > %s)' % (elecPtCut, elecPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM0Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM0_Down > %s)' % (elecPtCut, elecPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM1Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM1_Up > %s)' % (elecPtCut, elecPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM1Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM1_Down > %s)' % (elecPtCut, elecPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM10Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM10_Up > %s)' % (elecPtCut, elecPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM10Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM10_Down > %s)' % (elecPtCut, elecPtCut, elecPtCut, tauPtCut),
        },
        'eemt' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && shiftedPt_4 > %s)' % (elecPtCut, elecPtCut, muonPtCut, tauPtCut),
            '_energyScaleEESUp' : '*(leg1_EES_Up > %s && leg2_EES_Up > %s && pt_3 > %s && shiftedPt_4 > %s)' % (elecPtCut, elecPtCut, muonPtCut, tauPtCut),
            '_energyScaleEESDown' : '*(leg1_EES_Down > %s && leg2_EES_Down > %s && pt_3 > %s && shiftedPt_4 > %s)' % (elecPtCut, elecPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM0Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM0_Up > %s)' % (elecPtCut, elecPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM0Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM0_Down > %s)' % (elecPtCut, elecPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM1Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM1_Up > %s)' % (elecPtCut, elecPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM1Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM1_Down > %s)' % (elecPtCut, elecPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM10Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM10_Up > %s)' % (elecPtCut, elecPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM10Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM10_Down > %s)' % (elecPtCut, elecPtCut, muonPtCut, tauPtCut),
        },
        'eett' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && shiftedPt_3 > %s && shiftedPt_4 > %s)' % (elecPtCut, elecPtCut, tauPtCut, tauPtCut),
            '_energyScaleEESUp' : '*(leg1_EES_Up > %s && leg2_EES_Up > %s && shiftedPt_3 > %s && shiftedPt_4 > %s)' % (elecPtCut, elecPtCut, tauPtCut, tauPtCut),
            '_energyScaleEESDown' : '*(leg1_EES_Down > %s && leg2_EES_Down > %s && shiftedPt_3 > %s && shiftedPt_4 > %s)' % (elecPtCut, elecPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM0Up' : '*(pt_1 > %s && pt_2 > %s && leg3_DM0_Up > %s && leg4_DM0_Up > %s)' % (elecPtCut, elecPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM0Down' : '*(pt_1 > %s && pt_2 > %s && leg3_DM0_Down > %s && leg4_DM0_Down > %s)' % (elecPtCut, elecPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM1Up' : '*(pt_1 > %s && pt_2 > %s && leg3_DM1_Up > %s && leg4_DM1_Up > %s)' % (elecPtCut, elecPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM1Down' : '*(pt_1 > %s && pt_2 > %s && leg3_DM1_Down > %s && leg4_DM1_Down > %s)' % (elecPtCut, elecPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM10Up' : '*(pt_1 > %s && pt_2 > %s && leg3_DM10_Up > %s && leg4_DM10_Up > %s)' % (elecPtCut, elecPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM10Down' : '*(pt_1 > %s && pt_2 > %s && leg3_DM10_Down > %s && leg4_DM10_Down > %s)' % (elecPtCut, elecPtCut, tauPtCut, tauPtCut),
        },
        'eeem' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && pt_4 > %s)' % (elecPtCut, elecPtCut, elecPtCut, muonPtCut),
            '_energyScaleEESUp' : '*(leg1_EES_Up > %s && leg2_EES_Up > %s && leg3_EES_Up > %s && pt_4 > %s)' % (elecPtCut, elecPtCut, elecPtCut, muonPtCut),
            '_energyScaleEESDown' : '*(leg1_EES_Down > %s && leg2_EES_Down > %s && leg3_EES_Down > %s && pt_4 > %s)' % (elecPtCut, elecPtCut, elecPtCut, muonPtCut),
        },
        'eeee' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && pt_4 > %s)' % (elecPtCut, elecPtCut, elecPtCut, elecPtCut),
            '_energyScaleEESUp' : '*(leg1_EES_Up > %s && leg2_EES_Up > %s && leg3_EES_Up > %s && leg4_EES_Up > %s)' % (elecPtCut, elecPtCut, elecPtCut, elecPtCut),
            '_energyScaleEESDown' : '*(leg1_EES_Up > %s && leg2_EES_Up > %s && leg3_EES_Down > %s && leg4_EES_Up > %s)' % (elecPtCut, elecPtCut, elecPtCut, elecPtCut),
        },
        'emmt' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && shiftedPt_4 > %s)' % (muonPtCut, muonPtCut, elecPtCut, tauPtCut),
            '_energyScaleEESUp' : '*(pt_1 > %s && pt_2 > %s && leg3_EES_Up > %s && shiftedPt_4 > %s)' % (muonPtCut, muonPtCut, elecPtCut, tauPtCut),
            '_energyScaleEESDown' : '*(pt_1 > %s && pt_2 > %s && leg3_EES_Down > %s && shiftedPt_4 > %s)' % (muonPtCut, muonPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM0Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM0_Up > %s)' % (muonPtCut, muonPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM0Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM0_Down > %s)' % (muonPtCut, muonPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM1Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM1_Up > %s)' % (muonPtCut, muonPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM1Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM1_Down > %s)' % (muonPtCut, muonPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM10Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM10_Up > %s)' % (muonPtCut, muonPtCut, elecPtCut, tauPtCut),
            '_energyScaleDM10Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM10_Down > %s)' % (muonPtCut, muonPtCut, elecPtCut, tauPtCut),
        },
        'mmmt' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && shiftedPt_4 > %s)' % (muonPtCut, muonPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM0Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM0_Up > %s)' % (muonPtCut, muonPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM0Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM0_Down > %s)' % (muonPtCut, muonPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM1Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM1_Up > %s)' % (muonPtCut, muonPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM1Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM1_Down > %s)' % (muonPtCut, muonPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM10Up' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM10_Up > %s)' % (muonPtCut, muonPtCut, muonPtCut, tauPtCut),
            '_energyScaleDM10Down' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && leg4_DM10_Down > %s)' % (muonPtCut, muonPtCut, muonPtCut, tauPtCut),
        },
        'mmtt' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && shiftedPt_3 > %s && shiftedPt_4 > %s)' % (muonPtCut, muonPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM0Up' : '*(pt_1 > %s && pt_2 > %s && leg3_DM0_Up > %s && leg4_DM0_Up > %s)' % (muonPtCut, muonPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM0Down' : '*(pt_1 > %s && pt_2 > %s && leg3_DM0_Down > %s && leg4_DM0_Down > %s)' % (muonPtCut, muonPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM1Up' : '*(pt_1 > %s && pt_2 > %s && leg3_DM1_Up > %s && leg4_DM1_Up > %s)' % (muonPtCut, muonPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM1Down' : '*(pt_1 > %s && pt_2 > %s && leg3_DM1_Down > %s && leg4_DM1_Down > %s)' % (muonPtCut, muonPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM10Up' : '*(pt_1 > %s && pt_2 > %s && leg3_DM10_Up > %s && leg4_DM10_Up > %s)' % (muonPtCut, muonPtCut, tauPtCut, tauPtCut),
            '_energyScaleDM10Down' : '*(pt_1 > %s && pt_2 > %s && leg3_DM10_Down > %s && leg4_DM10_Down > %s)' % (muonPtCut, muonPtCut, tauPtCut, tauPtCut),
        },
        'emmm' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && pt_4 > %s)' % (muonPtCut, muonPtCut, elecPtCut, muonPtCut),
            '_energyScaleEESUp' : '*(pt_1 > %s && pt_2 > %s && leg3_EES_Up > %s && pt_4 > %s)' % (muonPtCut, muonPtCut, elecPtCut, muonPtCut),
            '_energyScaleEESDown' : '*(pt_1 > %s && pt_2 > %s && leg3_EES_Down > %s && pt_4 > %s)' % (muonPtCut, muonPtCut, elecPtCut, muonPtCut),
        },
        'mmmm' : { 
            '_NoShift' : '*(pt_1 > %s && pt_2 > %s && pt_3 > %s && pt_4 > %s)' % (muonPtCut, muonPtCut, muonPtCut, muonPtCut),
        },
    }
    return ESMap[ channel ]


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
def plotHistosProof( analysis, outFileName, chain, sample, channel, isData, additionalCut, blind=False, skipSSQCDDetails=False, genCode='x' ) :
    outFile = ROOT.TFile(outFileName, 'RECREATE')
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
    prodMap = getProdMap()
    if 'ADD_CHANNEL_SPECIFIC_ISO_CUTS' in additionalCut :
        if analysis == 'azh' and 'RedBkgYield' in outFile.GetName() :
            additionalCut = getRedBkgCutsAndWeights(
                    analysis, channel, additionalCut, prodMap )
            # Add channel specific VVLoose cuts for Taus
            if channel in ['eeet','emmt'] :
                additionalCut += '*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)'
                additionalCut += '*(electronMvaHZZ_3 > 0.5 && iso_3 < 0.6)' ### For 3L FRs
            elif channel in ['eemt','mmmt'] :
                additionalCut += '*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)'
                additionalCut += '*(iso_3 < 1.0)' ### For 3L FRs
            elif channel in ['eett','mmtt'] :
                additionalCut += '*(byVVLooseIsolationMVArun2v1DBoldDMwLT_3 > 0.5)'
                additionalCut += '*(byVVLooseIsolationMVArun2v1DBoldDMwLT_4 > 0.5)'
            elif channel in ['eeem','emmm'] : ### For 3L FRs
                additionalCut += '*(electronMvaHZZ_3 > 0.5 && iso_3 < 0.6)' ### For 3L FRs
                additionalCut += '*(iso_4 < 1.0)' ### For 3L FRs
        elif analysis == 'azh' and 'RedBkgShape' in outFile.GetName() :
            additionalCut = getRedBkgShape( 
                    analysis, channel, additionalCut, prodMap )
        else : # No reducible bkg
            additionalCut = getChannelSpecificFinalCuts(
                    analysis, channel, additionalCut, prodMap )

        # Add channel specific LT_higgs cuts from June Optimization
        #if channel in ['eeet','emmt'] :
        #    additionalCut += '*(LT_higgs > 20)'
        #    #additionalCut += '*(LT_higgs > 30)'
        #elif channel in ['eemt','mmmt'] :
        #    additionalCut += '*(LT_higgs > 20)'
        #    #additionalCut += '*(LT_higgs > 40)'
        #elif channel in ['eeem','emmm'] :
        #    additionalCut += '*(LT_higgs > 20)'
        if channel in ['eett','mmtt'] :
            #additionalCut += '*(LT_higgs > 80)' # > 80 GeV is 10% better than 60,
            additionalCut += '*(LT_higgs > 60)' # > 80 GeV is 10% better than 60,
            # 60 is way more stats

        # bJet Veto Tests
        additionalCut += '*(bjetCISVVeto20Medium == 0)'
        additionalCut += '*(const_m_sv > 0 && AMassConst < 600)'
        #additionalCut += '*(gen_match_3 == 6)'
        #additionalCut += '*(gen_match_4==6)'
        #additionalCut += '*(gen_match_3 == 6 && gen_match_4==6)'
        #additionalCut += '*(gen_match_3 == 6 || gen_match_4==6)'



    ''' Combine Gen and Chan specific into one fill section '''
    histos = {}


    ''' Get Energy Scale Map which is now confusing with
        decay mode specific shifts '''
    esMap = getESMap( channel )


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
        if skipSystShapeVar( var, sample, channel, genCode, outFileName ) : continue

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

        # Adjust the additional cuts to grab appropriate FR yield
        # weights
        elif '_promptMC' in var :
            if '_promptMCElecMu' in var :
                if 'Up' in var[-2:] :
                    additionalCutToUse = additionalCutToUse.replace('zhFR0','zhFR0ElecMuUp')
                    additionalCutToUse = additionalCutToUse.replace('zhFR1','zhFR1ElecMuUp')
                    additionalCutToUse = additionalCutToUse.replace('zhFR2','zhFR2ElecMuUp')
                if 'Down' in var[-4:] :
                    additionalCutToUse = additionalCutToUse.replace('zhFR0','zhFR0ElecMuDown')
                    additionalCutToUse = additionalCutToUse.replace('zhFR1','zhFR1ElecMuDown')
                    additionalCutToUse = additionalCutToUse.replace('zhFR2','zhFR2ElecMuDown')
            if '_promptMCTau' in var :
                if 'Up' in var[-2:] :
                    additionalCutToUse = additionalCutToUse.replace('zhFR0','zhFR0TauUp')
                    additionalCutToUse = additionalCutToUse.replace('zhFR1','zhFR1TauUp')
                    additionalCutToUse = additionalCutToUse.replace('zhFR2','zhFR2TauUp')
                if 'Down' in var[-4:] :
                    additionalCutToUse = additionalCutToUse.replace('zhFR0','zhFR0TauDown')
                    additionalCutToUse = additionalCutToUse.replace('zhFR1','zhFR1TauDown')
                    additionalCutToUse = additionalCutToUse.replace('zhFR2','zhFR2TauDown')

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


        # Add the m_sv mass window cut for AZH analysis
        doMassCutForAllVars = True
        if analysis == 'azh' and ('AMassConst' in var or doMassCutForAllVars) :
            additionalCutToUse += getMassWindowCut( var, sample, genCode, outFileName )


        # This addes the Fake Factor shape systematics weights
        # And add the variable specific Fake Factor cut
        # (isolation and gen match change per variable def)
        ffShapeSyst = ''
        if doFF :
            ffRegion = 'anti-iso' if '_ffSub' in var else 'signal'
            ffShapeSyst += getFFShapeSystApp( ffRegion, isData, outFile, var )
            ffShapeSyst += getFFCutsAndWeights( ffRegion, isData, outFile )


        if ":" in var :
    	    histos[ var ] = make2DHisto( var, channel )
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
                if 'LT_higgs:m_sv' in var :
                    if 'All'  in var : plotVar = 'LT_higgs:m_sv_%s' % shiftDir
                    if 'DM0'  in var : plotVar = 'LT_higgs:m_sv_DM0_%s' % shiftDir
                    if 'DM1'  in var : plotVar = 'LT_higgs:m_sv_DM1_%s' % shiftDir
                    if 'DM10' in var : plotVar = 'LT_higgs:m_sv_DM10_%s' % shiftDir
                    if 'EES' in var : plotVar = 'LT_higgs:m_sv_EES_%s' % shiftDir
                elif 'pt_sv:m_sv' in var :
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
                    if 'EES'  in var : plotVar = 'm_sv_EES_%s' % shiftDir
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
                elif 'AMassConst' in var :
                    if 'All'  in var : plotVar = 'AMassConst_%s' % shiftDir
                    if 'DM0'  in var : plotVar = 'AMassConst_DM0_%s' % shiftDir
                    if 'DM1'  in var : plotVar = 'AMassConst_DM1_%s' % shiftDir
                    if 'DM10' in var : plotVar = 'AMassConst_DM10_%s' % shiftDir
                    if 'EES' in var : plotVar = 'AMassConst_EES_%s' % shiftDir
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
                if 'AMassConst' in var :
                    if 'Up' in var[-2:] :
                        plotVar = plotVar.replace('_metClusteredUp','')
                        plotVar = plotVar.replace('AMassConst','AMassConst_ClusteredMet_UP')
                    if 'Down' in var[-4:] :
                        plotVar = plotVar.replace('_metClusteredDown','')
                        plotVar = plotVar.replace('AMassConst','AMassConst_ClusteredMet_DOWN')
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
                if 'AMassConst' in var :
                    if 'Up' in var[-2:] :
                        plotVar = plotVar.replace('_metUnclusteredUp','')
                        plotVar = plotVar.replace('AMassConst','AMassConst_UncMet_UP')
                    if 'Down' in var[-4:] :
                        plotVar = plotVar.replace('_metUnclusteredDown','')
                        plotVar = plotVar.replace('AMassConst','AMassConst_UncMet_DOWN')
            elif 'promptMC' in shapeName :
                if 'm_sv' in var or 'AMassConst' in var :
                    if 'Up' in var[-2:] :
                        plotVar = plotVar.replace('_promptMCElecMuUp','')
                        plotVar = plotVar.replace('_promptMCTauUp','')
                    if 'Down' in var[-4:] :
                        plotVar = plotVar.replace('_promptMCElecMuDown','')
                        plotVar = plotVar.replace('_promptMCTauDown','')
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

                
        #print "Var: %s   VarBase: %s   PlotVar: %s" % (var, varBase, plotVar)

        ### Make sure that if we have no events
        ### we still save a blank histo for use later
        if chain.GetEntries() == 0 :
            print " #### ENTRIES = 0 #### "
            if ":" in var :
                histos[ var ] = make2DHisto( var, channel )
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
                print "DATA CUT"
                print '1%s%s%s' % (additionalCutToUse, dataES, ffShapeSyst)
                chain.Draw( '%s>>%s' % (plotVar, var), '1%s%s%s' % (additionalCutToUse, dataES, ffShapeSyst) )
                histos[ var ] = gPad.GetPrimitive( var )
                #if var == 'm_visCor' or var == 'Mass' :
                if var == 'm_sv' :
                    #print 'm_visCor'
                    #print ' --- XXX m_sv',sample,outFileName,channel,histos[ var ].Integral()
                    #print "Data Count:", histos[ var ].Integral()
                    print "Cut: %s%s%s" % (additionalCutToUse, dataES, ffShapeSyst)
            else :

                chain.Draw( '%s>>%s' % (plotVar, var), '%s' % totalCutAndWeightMC )
                ''' No reweighting at the moment! '''
                histos[ var ] = gPad.GetPrimitive( var )
                integralPost = histos[ var ].Integral()
                if var == 'm_visCor' or var == 'Mass' :
                    #print 'm_visCor'
                    print "tmpIntPost: %f" % integralPost
                    print "Cut: %s" % totalCutAndWeightMC

            # When chain has entries, but the cut string leaves no drawn events
            # ROOT makes a default TH1 with 100 bins which causes problems merging later
            # so make our original binned histo
            if histos[ var ].Integral() == 0.0 :
                if ":" in var :
    	            histos[ var ] = make2DHisto( var, channel )
                else :
    	            histos[ var ] = makeHisto( var, info[0], info[1], info[2])

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
            'pt_sv:m_sv' : [300, 0, 300, 10, 'M_{#tau#tau} [GeV]', ' GeV'],
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
####            #'genpT' : [40, 0, 400, 40, 'Gen Pt [GeV]', ' GeV'],
####            #'genMass' : [90, 100, 550, 40, 'Gen Mass [GeV]', ' GeV'],
####            #'Z_Phi' : [80, -4, 4, 80, 'Z Phi', ' Phi'],
####            #'Z_Eta' : [40, -5, 5, 10, 'Z Eta', ' Eta'],
#            'Z_Pt' : [400, 0, 400, 40, 'Z p_{T} [GeV]', ' GeV'],
#            'm_vis' : [70, 55, 125, 10, 'Z Mass [GeV]', ' GeV'],
####            #'H_Phi' : [40, -4, 4, 80, 'H Phi', ' Phi'],
####            #'H_Eta' : [40, -5, 5, 10, 'H Eta', ' Eta'],
#            'H_Pt' : [300, 0, 300, 30, 'H p_{T} [GeV]', ' GeV'],
#            'H_vis' : [300, 0, 300, 20, 'H Vis Mass [GeV]', ' GeV'],
####            'Z_DR' : [500, 0, 5, 20, 'Z dR(l1,l2)', ' dR'],
####            'H_DR' : [500, 0, 5, 20, 'H dR(l3,l4)', ' dR'],
#####            'Z_DPhi' : [800, -4, 4, 80, 'Z dPhi', ' dPhi'],
#####            'Z_DEta' : [100, -5, 5, 10, 'Z dEta', ' dEta'],
#####            'mjj' : [40, 0, 800, 1, 'M_{jj}', ' [GeV]'],
#####            'jdeta' : [100, -5, 5, 10, 'VBF dEta', ' dEta'],
            'm_sv' : [300, 0, 300, 20, 'm_{#tau#tau} [GeV]', ' GeV'],
            #'const_m_sv' : [30, 110, 140, 1, 'm^{c}_{#tau#tau} [GeV]', ' GeV'],
            'const_m_sv' : [170, -10, 160, 170, 'm^{c}_{#tau#tau} [GeV]', ' GeV'],
#            'pt_sv' : [300, 0, 300, 20, 'PT_{#tau#tau} [GeV]', ' GeV'],
#            'const_pt_sv' : [300, 0, 300, 20, 'PT^{c}_{#tau#tau} [GeV]', ' GeV'],
##            'H_vis' : [200, 0, 200, 20, 'H Visible Mass [GeV]', ' GeV'],
##            'Mass' : [600, 0, 600, 40, 'vis M_{ll#tau#tau} [GeV]', ' GeV'],
#            'A_Mass' : [600, 0, 600, 20, 'M_{ll#tau#tau} [GeV]', ' GeV'],
            'AMassConst' : [600, 0, 600, 20, 'M^{c}_{ll#tau#tau} [GeV]', ' GeV'],
#            'LT' : [600, 0, 600, 40, 'Total LT [GeV]', ' GeV'],
#            'Mt' : [600, 0, 600, 40, 'Total m_{T} [GeV]', ' GeV'],
            #'H_SS' : [20, -1, 1, 1, 'H Same Sign', ''],
#            'LT_higgs' : [200, 0, 200, 10, 'LT_{higgs} [GeV]', ' GeV'],
# HIG-18-007            'LT_higgs:m_sv' : [20, 0, 20, 1, 'M_{#tau#tau} [GeV]', ' GeV'],
#            'H_PZeta' : [600, -200, 400, 20, 'PZeta_{higgs} [GeV]', ' GeV'],
#            'H_PZetaVis' : [300, 0, 300, 20, 'PZetaVis_{higgs} [GeV]', ' GeV'],
#            'H_DZeta' : [600, -200, 400, 20, 'DZeta_{higgs} [GeV]', ' GeV'],
#            'met' : [250, 0, 250, 20, 'pfMet [GeV]', ' GeV'],
#            'zhFR0' : [500, 0.001, 0.5, 10, 'ZH FakeRate Weight 0', ''],
#            'zhFR1' : [500, 0.001, 0.5, 10, 'ZH FakeRate Weight 1', ''],
#            'zhFR2' : [500, 0.001, 0.5, 10, 'ZH FakeRate Weight 2', ''],
        #    'pt_1' : [200, 0, 200, 20, 'Leg1 p_{T} [GeV]', ' GeV'],
        #    'pt_2' : [200, 0, 200, 20, 'Leg2 p_{T} [GeV]', ' GeV'],
        #    'pt_3' : [200, 0, 200, 20, 'Leg3 p_{T} [GeV]', ' GeV'],
        #    'pt_4' : [200, 0, 200, 20, 'Leg4 p_{T} [GeV]', ' GeV'],
#            'pfmt_3' : [200, 0, 200, 20, 'Leg3 M_{T} [GeV]', ' GeV'],
#            'pfmt_4' : [200, 0, 200, 20, 'Leg4 M_{T} [GeV]', ' GeV'],
#            'gen_match_3' : [7, -0.5, 6.5, 1, 'Gen Match Leg 3', ''],
#            'gen_match_4' : [7, -0.5, 6.5, 1, 'Gen Match Leg 4', ''],
####XXX            'eta_1' : [60, -3, 3, 10, 'Leg1 Eta', ' Eta'],
####XXX            'eta_2' : [60, -3, 3, 10, 'Leg2 Eta', ' Eta'],
####XXX            'eta_3' : [60, -3, 3, 10, 'Leg3 Eta', ' Eta'],
####XXX            'eta_4' : [60, -3, 3, 10, 'Leg4 Eta', ' Eta'],
####            'iso_1' : [20, 0, 0.5, 1, 'Leg1 RelIsoDB03', ''],
####            'iso_2' : [20, 0, 0.5, 1, 'Leg2 RelIsoDB03', ''],
#            'iso_3' : [20, 0, 1, 1, 'Leg3 Iso', ''],
#            'iso_4' : [20, 0, 1, 1, 'Leg4 Iso', ''],
###            'jpt_1' : [200, 0, 200, 20, 'Leading Jet Pt', ' GeV'],
###            #'jeta_1' : [100, -5, 5, 10, 'Leading Jet Eta', ' Eta'],
###            'jpt_2' : [200, 0, 200, 20, 'Second Jet Pt', ' GeV'],
###            #'jeta_2' : [100, -5, 5, 10, 'Second Jet Eta', ' Eta'],
###            #'weight' : [60, -30, 30, 1, 'Gen Weight', ''],
####            'npv' : [40, 0, 40, 4, 'Number of Vertices', ''],
####XXX            'njetspt20' : [100, 0, 10, 10, 'nJetPt20', ''],
#            'jetVeto30' : [10, -0.5, 9.5, 1, 'nJetPt30', ''],
#####            'azhWeight' : [50, 0, 2, 1, 'Muon + Electron Weights', ''],
####            'muVetoZTTp001dxyz' : [6, -1, 5, 1, 'muVetoZTTp001dxyz', ''],
####            'eVetoZTTp001dxyz' : [6, -1, 5, 1, 'eVetoZTTp001dxyz', ''],
####            'muVetoZTTp001dxyzR0' : [6, -1, 5, 1, 'muVetoZTTp001dxyzR0', ''],
####            'eVetoZTTp001dxyzR0' : [6, -1, 5, 1, 'eVetoZTTp001dxyzR0', ''],
#            'bjetCISVVeto20Tight' : [5, -0.5, 4.5, 1, 'nBTag_20Tight', ''],
#            'bjetCISVVeto20Medium' : [5, -0.5, 4.5, 1, 'nBTag_20Medium', ''],
#            'bjetCISVVeto20Loose' : [5, -0.5, 4.5, 1, 'nBTag_20Loose', ''],
#XXX            'bjetCISVVeto30Medium' : [60, 0, 6, 5, 'nBTag_30Medium', ''],
#XXX            'bjetCISVVeto30Tight' : [60, 0, 6, 5, 'nBTag_30Tight', ''],
        }
#        llltMap = {
#            'againstElectronVLooseMVA6_4' : [9, -1, 2, 1, 'Against E VL MVA6 Leg 4', ''],
#            'againstElectronLooseMVA6_4' : [9, -1, 2, 1, 'Against E L MVA6 Leg 4', ''],
#            'againstMuonLoose3_4' : [9, -1, 2, 1, 'Against M Loose 3 Leg 4', ''],
#            'againstMuonTight3_4' : [9, -1, 2, 1, 'Against M Tight 3 Leg 4', ''],
#        }
#        llttMap = {
#            'againstElectronVLooseMVA6_3' : [9, -1, 2, 1, 'Against E VL MVA6 Leg 3', ''],
#            'againstElectronLooseMVA6_3' : [9, -1, 2, 1, 'Against E L MVA6 Leg 3', ''],
#            'againstMuonLoose3_3' : [9, -1, 2, 1, 'Against M Loose 3 Leg 3', ''],
#            'againstMuonTight3_3' : [9, -1, 2, 1, 'Against M Tight 3 Leg 3', ''],
#       }
#        zeeMap = {
#            #'id_e_mva_nt_loose_1' : [2, -0.5, 1.5, 1, 'elec1 MVA90', ''],
#            'id_e_mva_nt_tight_1' : [2, -0.5, 1.5, 1, 'elec1 MVA80', ''],
#            #'id_e_mva_nt_loose_2' : [2, -0.5, 1.5, 1, 'elec2 MVA90', ''],
#            'id_e_mva_nt_tight_2' : [2, -0.5, 1.5, 1, 'elec2 MVA80', ''],
#            'iso_1' : [20, 0, 1, 1, 'elec1 RelIsoDB03', ''],
#            'iso_2' : [20, 0, 1, 1, 'elec2 RelIsoDB03', ''],
#        }
#        llexMap = {
#            #'id_e_mva_nt_loose_3' : [2, -0.5, 1.5, 1, 'leg3 MVA90', ''],
#            'id_e_mva_nt_tight_3' : [2, -0.5, 1.5, 1, 'leg3 MVA80', ''],
#            'iso_3' : [20, 0, 1, 1, 'leg3 RelIsoDB03', ''],
#        }
        #if channel == 'xxxx' :
        #    return genVarMap
        #if channel in ['eeet', 'eemt', 'eett', 'emmt', 'mmmt', 'mmtt'] :
        #    for var in llltMap.keys() :
        #        genVarMap[var] = llltMap[ var ]
        #if channel in ['eett', 'mmtt'] :
        #    for var in llttMap.keys() :
        #        genVarMap[var] = llttMap[ var ]
        #if channel in ['eeet','eett','eemt','eeem','eeee',] :
        #    for k, v in zeeMap.iteritems() :
        #        genVarMap[k] = v
        #if channel in ['eeet', 'eeem', 'emmt', 'emmm'] :
        #    for k, v in llexMap.iteritems() :
        #        genVarMap[k] = v


        ''' added shape systematics '''
        #toAdd = ['m_sv','LT_higgs:m_sv' ] # No extra shapes
        #toAdd = ['LT_higgs:m_sv', ] # No extra shapes
        #toAdd = ['Mass','A_Mass' ] # No extra shapes
        toAdd = ['AMassConst', ] # No extra shapes
        varsForShapeSyst = []
        for item in toAdd :
            varsForShapeSyst.append( item )
        shapesToAdd = {
                    #'energyScaleEES':'Electron Energy Scale',
                    #'energyScaleDM0':'TES DM0',
                    #'energyScaleDM1':'TES DM1',
                    #'energyScaleDM10':'TES DM10',
                    #'metClustered':'Clustered MET',
                    #'metUnclustered':'Unclustered MET',
                    #'promptMCElecMu':'RedBkg Prompt MC Elec/Mu',
                    #'promptMCTau':'RedBkg Prompt MC Tau',
                    }

        for var in genVarMap.keys() :
            if var in varsForShapeSyst :
                for shape, app in shapesToAdd.iteritems() :
                    genVarMap[ var+'_'+shape+'Up' ] = list(genVarMap[ var ])
                    genVarMap[ var+'_'+shape+'Up' ][4] = genVarMap[ var+'_'+shape+'Up' ][4]+' '+app+' UP'
                    genVarMap[ var+'_'+shape+'Down' ] = list(genVarMap[ var ])
                    genVarMap[ var+'_'+shape+'Down' ][4] = genVarMap[ var+'_'+shape+'Down' ][4]+' '+app+' Down'

        return genVarMap







