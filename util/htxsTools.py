

# Map to link our standard naming scheme for signals
# with their rivet/htxs codes
# and to provide the necessary cut to select this group
# from gen level
# and to provide the final DC mapping

# See https://svnweb.cern.ch/cern/wsvn/lhchiggsxs/repository/TemplateXS/HiggsTemplateCrossSections.h for rivet code mappings

# See official HTXS naming scheme here:
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsTemplateCrossSection

def getHtxsCutMapStage0() :
    htxsMap = {
    'ggHtoTauTauNNLOPS' : {
        'stage0GG2H-FWDH'    : ['ggH_fwd', '*(Rivet_stage0_cat == 10)'],
        'stage0GG2H'         : ['ggH', '*(Rivet_stage0_cat == 11)']
    },
    'ggHtoTauTau' : {
        'stage0GG2H-FWDH'    : ['ggH_fwd', '*(Rivet_stage0_cat == 10)'],
        'stage0GG2H'         : ['ggH', '*(Rivet_stage0_cat == 11)']
    },
    'VBFHtoTauTau' : {
        'stage0VBF-FWDH'     : ['qqH_fwd', '*(Rivet_stage0_cat == 20)'],
        'stage0VBF'          : ['qqH', '*(Rivet_stage0_cat == 21)']
    },
    'WMinusHTauTau' : {
        'stage0VH2HQQ'       : ['VH_had', '*(Rivet_stage0_cat == 23)'],
        'stage0QQ2HLNU-FWDH' : ['WH_lep_fwd', '*(Rivet_stage0_cat == 30)'],
        'stage0QQ2HLNU'      : ['WH_lep', '*(Rivet_stage0_cat == 31)']
    },
    'WPlusHTauTau' : {
        'stage0VH2HQQ'       : ['VH_had', '*(Rivet_stage0_cat == 23)'],
        'stage0QQ2HLNU-FWDH' : ['WH_lep_fwd', '*(Rivet_stage0_cat == 30)'],
        'stage0QQ2HLNU'      : ['WH_lep', '*(Rivet_stage0_cat == 31)']
    },
    'ZHTauTau' : {
        'stage0VH2HQQ-FWDH'  : ['VH_had_fwd', '*(Rivet_stage0_cat == 22)'],
        'stage0VH2HQQ'       : ['VH_had', '*(Rivet_stage0_cat == 23)'],
        'stage0QQ2HLL-FWDH'  : ['ZH_lep_fwd', '*(Rivet_stage0_cat == 40)'],
        'stage0QQ2HLL'       : ['ZH_lep', '*(Rivet_stage0_cat == 41)']
    }}

    return htxsMap


def getHtxsCutMapStage1() :
    htxsMap = {
    'ggHtoTauTauNNLOPS' : {
        'stage1GG2H-VBFTOPO-JET3VETO'    : ['ggH_VBFTOPO_JET3VETO', '*(Rivet_stage1_cat_pTjet30GeV == 101)'],
        'stage1GG2H-VBFTOPO-JET3'        : ['ggH_VBFTOPO_JET3', '*(Rivet_stage1_cat_pTjet30GeV == 102)'],
        'stage1GG2H-0J'                  : ['ggH_0J', '*(Rivet_stage1_cat_pTjet30GeV == 103)'],
        'stage1GG2H-1J-PTH-0-60'         : ['ggH_1J_PTH_0_60', '*(Rivet_stage1_cat_pTjet30GeV == 104)'],
        'stage1GG2H-1J-PTH-60-120'       : ['ggH_1J_PTH_60_120', '*(Rivet_stage1_cat_pTjet30GeV == 105)'],
        'stage1GG2H-1J-PTH-120-200'      : ['ggH_1J_PTH_120_200', '*(Rivet_stage1_cat_pTjet30GeV == 106)'],
        'stage1GG2H-1J-PTH-GT200'        : ['ggH_1J_PTH_GT200', '*(Rivet_stage1_cat_pTjet30GeV == 107)'],
        'stage1GG2H-GE2J-PTH-0-60'       : ['ggH_GE2J_PTH_0_60', '*(Rivet_stage1_cat_pTjet30GeV == 108)'],
        'stage1GG2H-GE2J-PTH-60-120'     : ['ggH_GE2J_PTH_60_120', '*(Rivet_stage1_cat_pTjet30GeV == 109)'],
        'stage1GG2H-GE2J-PTH-120-200'    : ['ggH_GE2J_PTH_120_200', '*(Rivet_stage1_cat_pTjet30GeV == 110)'],
        'stage1GG2H-GE2J-PTH-GT200'      : ['ggH_GE2J_PTH_GT200', '*(Rivet_stage1_cat_pTjet30GeV == 111)'],
    },
    'ggHtoTauTau' : {
        'stage1GG2H-VBFTOPO-JET3VETO'    : ['ggH_VBFTOPO_JET3VETO', '*(Rivet_stage1_cat_pTjet30GeV == 101)'],
        'stage1GG2H-VBFTOPO-JET3'        : ['ggH_VBFTOPO_JET3', '*(Rivet_stage1_cat_pTjet30GeV == 102)'],
        'stage1GG2H-0J'                  : ['ggH_0J', '*(Rivet_stage1_cat_pTjet30GeV == 103)'],
        'stage1GG2H-1J-PTH-0-60'         : ['ggH_1J_PTH_0_60', '*(Rivet_stage1_cat_pTjet30GeV == 104)'],
        'stage1GG2H-1J-PTH-60-120'       : ['ggH_1J_PTH_60_120', '*(Rivet_stage1_cat_pTjet30GeV == 105)'],
        'stage1GG2H-1J-PTH-120-200'      : ['ggH_1J_PTH_120_200', '*(Rivet_stage1_cat_pTjet30GeV == 106)'],
        'stage1GG2H-1J-PTH-GT200'        : ['ggH_1J_PTH_GT200', '*(Rivet_stage1_cat_pTjet30GeV == 107)'],
        'stage1GG2H-GE2J-PTH-0-60'       : ['ggH_GE2J_PTH_0_60', '*(Rivet_stage1_cat_pTjet30GeV == 108)'],
        'stage1GG2H-GE2J-PTH-60-120'     : ['ggH_GE2J_PTH_60_120', '*(Rivet_stage1_cat_pTjet30GeV == 109)'],
        'stage1GG2H-GE2J-PTH-120-200'    : ['ggH_GE2J_PTH_120_200', '*(Rivet_stage1_cat_pTjet30GeV == 110)'],
        'stage1GG2H-GE2J-PTH-GT200'      : ['ggH_GE2J_PTH_GT200', '*(Rivet_stage1_cat_pTjet30GeV == 111)'],
    },
    'VBFHtoTauTau' : {
        'stage1QQ2HQQ-FWDH'              : ['qqH_FWDH', '*(Rivet_stage1_cat_pTjet30GeV == 200)'],
        'stage1QQ2HQQ-VBFTOPO-JET3VETO'  : ['qqH_VBFTOPO_JET3VETO', '*(Rivet_stage1_cat_pTjet30GeV == 201)'],
        'stage1QQ2HQQ-VBFTOPO-JET3'      : ['qqH_VBFTOPO_JET3', '*(Rivet_stage1_cat_pTjet30GeV == 202)'],
        'stage1QQ2HQQ-VH2JET'            : ['qqH_VH2JET', '*(Rivet_stage1_cat_pTjet30GeV == 203)'],
        'stage1QQ2HQQ-REST'              : ['qqH_REST', '*(Rivet_stage1_cat_pTjet30GeV == 204)'],
        'stage1QQ2HQQ-PTJET1-GT200'      : ['qqH_PTJET1_GT200', '*(Rivet_stage1_cat_pTjet30GeV == 205)'],
    },
    'WMinusHTauTau' : {
        'stage1QQ2HQQ-VBFTOPO-JET3VETO'  : ['VH_had_VBFTOPO_JET3VETO', '*(Rivet_stage1_cat_pTjet30GeV == 201)'],
        'stage1QQ2HQQ-VBFTOPO-JET3'      : ['VH_had_VBFTOPO_JET3', '*(Rivet_stage1_cat_pTjet30GeV == 202)'],
        'stage1QQ2HQQ-VH2JET'            : ['VH_had_VH2JET', '*(Rivet_stage1_cat_pTjet30GeV == 203)'],
        'stage1QQ2HQQ-REST'              : ['VH_had_REST', '*(Rivet_stage1_cat_pTjet30GeV == 204)'],
        'stage1QQ2HQQ-PTJET1-GT200'      : ['VH_had_PTJET1_GT200', '*(Rivet_stage1_cat_pTjet30GeV == 205)'],
        'stage1QQ2HLNU-FWDH'             : ['WH_lep_FWDH', '*(Rivet_stage1_cat_pTjet30GeV == 300)'],
        'stage1QQ2HLNU-PTV-0-150'        : ['WH_lep_PTV_0_150', '*(Rivet_stage1_cat_pTjet30GeV == 301)'],
        'stage1QQ2HLNU-PTV-150-250-0J'   : ['WH_lep_PTV_150_250_0J', '*(Rivet_stage1_cat_pTjet30GeV == 302)'],
        'stage1QQ2HLNU-PTV-150-250-GE1J' : ['WH_lep_PTV_150_250_GE1J', '*(Rivet_stage1_cat_pTjet30GeV == 303)'],
        'stage1QQ2HLNU-PTV-GT250'        : ['WH_lep_PTV_GT250', '*(Rivet_stage1_cat_pTjet30GeV == 304)'],
    },
    'WPlusHTauTau' : {
        'stage1QQ2HQQ-VBFTOPO-JET3VETO'  : ['VH_had_VBFTOPO_JET3VETO', '*(Rivet_stage1_cat_pTjet30GeV == 201)'],
        'stage1QQ2HQQ-VBFTOPO-JET3'      : ['VH_had_VBFTOPO_JET3', '*(Rivet_stage1_cat_pTjet30GeV == 202)'],
        'stage1QQ2HQQ-VH2JET'            : ['VH_had_VH2JET', '*(Rivet_stage1_cat_pTjet30GeV == 203)'],
        'stage1QQ2HQQ-REST'              : ['VH_had_REST', '*(Rivet_stage1_cat_pTjet30GeV == 204)'],
        'stage1QQ2HQQ-PTJET1-GT200'      : ['VH_had_PTJET1_GT200', '*(Rivet_stage1_cat_pTjet30GeV == 205)'],
        'stage1QQ2HLNU-FWDH'             : ['WH_lep_FWDH', '*(Rivet_stage1_cat_pTjet30GeV == 300)'],
        'stage1QQ2HLNU-PTV-0-150'        : ['WH_lep_PTV_0_150', '*(Rivet_stage1_cat_pTjet30GeV == 301)'],
        'stage1QQ2HLNU-PTV-150-250-0J'   : ['WH_lep_PTV_150_250_0J', '*(Rivet_stage1_cat_pTjet30GeV == 302)'],
        'stage1QQ2HLNU-PTV-150-250-GE1J' : ['WH_lep_PTV_150_250_GE1J', '*(Rivet_stage1_cat_pTjet30GeV == 303)'],
        'stage1QQ2HLNU-PTV-GT250'        : ['WH_lep_PTV_GT250', '*(Rivet_stage1_cat_pTjet30GeV == 304)'],
    },
    'ZHTauTau' : {
        'stage1QQ2HQQ-FWDH'              : ['VH_had_FWDH', '*(Rivet_stage1_cat_pTjet30GeV == 200)'],
        'stage1QQ2HQQ-VBFTOPO-JET3VETO'  : ['VH_had_VBFTOPO_JET3VETO', '*(Rivet_stage1_cat_pTjet30GeV == 201)'],
        'stage1QQ2HQQ-VBFTOPO-JET3'      : ['VH_had_VBFTOPO_JET3', '*(Rivet_stage1_cat_pTjet30GeV == 202)'],
        'stage1QQ2HQQ-VH2JET'            : ['VH_had_VH2JET', '*(Rivet_stage1_cat_pTjet30GeV == 203)'],
        'stage1QQ2HQQ-REST'              : ['VH_had_REST', '*(Rivet_stage1_cat_pTjet30GeV == 204)'],
        'stage1QQ2HQQ-PTJET1-GT200'      : ['VH_had_PTJET1_GT200', '*(Rivet_stage1_cat_pTjet30GeV == 205)'],
        'stage1QQ2HLL-FWDH'              : ['ZH_lep_FWDH', '*(Rivet_stage1_cat_pTjet30GeV == 400)'],
        'stage1QQ2HLL-PTV-0-150'         : ['ZH_lep_PTV_0_150', '*(Rivet_stage1_cat_pTjet30GeV == 401)'],
        'stage1QQ2HLL-PTV-150-250-0J'    : ['ZH_lep_PTV_150_250_0J', '*(Rivet_stage1_cat_pTjet30GeV == 402)'],
        'stage1QQ2HLL-PTV-150-250-GE1J'  : ['ZH_lep_PTV_150_250_GE1J', '*(Rivet_stage1_cat_pTjet30GeV == 403)'],
        'stage1QQ2HLL-PTV-GT250'         : ['ZH_lep_PTV_GT250', '*(Rivet_stage1_cat_pTjet30GeV == 404)'],
    }}

    return htxsMap


if __name__ == '__main__' :
    print getHtxsCutMapStage0()    
    print getHtxsCutMapStage1()
