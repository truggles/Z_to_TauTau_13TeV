

# Map to link our standard naming scheme for signals
# with their rivet/htxs codes
# and to provide the necessary cut to select this group
# from gen level
# and to provide the final DC mapping

# See https://svnweb.cern.ch/cern/wsvn/lhchiggsxs/repository/TemplateXS/HiggsTemplateCrossSections.h for rivet code mappings

def getHtxsCutMapStage0() :
    htxsMap = {
    'ggHtoTauTau' : {
        'stage0GG2H-FWDH' : '*(Rivet_stage0_cat == 10)',
        'stage0GG2H' : '*(Rivet_stage0_cat == 11)'
    },
    'VBFHtoTauTau' : {
        'stage0VBF-FWDH' : '*(Rivet_stage0_cat == 20)',
        'stage0VBF' : '*(Rivet_stage0_cat == 21)'
    },
    'WMinusHTauTau' : {
        'stage0VH2HQQ' : '*(Rivet_stage0_cat == 23)',
        'stage0QQ2HLNU-FWDH' : '*(Rivet_stage0_cat == 30)',
        'stage0QQ2HLNU' : '*(Rivet_stage0_cat == 31)'
    },
    'WPlusHTauTau' : {
        'stage0VH2HQQ' : '*(Rivet_stage0_cat == 23)',
        'stage0QQ2HLNU-FWDH' : '*(Rivet_stage0_cat == 30)',
        'stage0QQ2HLNU' : '*(Rivet_stage0_cat == 31)'
    },
    'ZHTauTau' : {
        'stage0VH2HQQ-FWDH' : '*(Rivet_stage0_cat == 22)',
        'stage0VH2HQQ' : '*(Rivet_stage0_cat == 23)',
        'stage0QQ2HLL-FWDH' : '*(Rivet_stage0_cat == 40)',
        'stage0QQ2HLL' : '*(Rivet_stage0_cat == 41)'
    }}

    return htxsMap


def getHtxsCutMapStage1() :
    htxsMap = {
    'ggHtoTauTau' : {
        'stage1GG2H-VBFTOPO-JET3VETO' : '*(Rivet_stage1_cat_pTjet30GeV == 101)',
        'stage1GG2H-VBFTOPO-JET3' : '*(Rivet_stage1_cat_pTjet30GeV == 102)',
        'stage1GG2H-0J' : '*(Rivet_stage1_cat_pTjet30GeV == 103)',
        'stage1GG2H-1J-PTH-0-60' : '*(Rivet_stage1_cat_pTjet30GeV == 104)',
        'stage1GG2H-1J-PTH-60-120' : '*(Rivet_stage1_cat_pTjet30GeV == 105)',
        'stage1GG2H-1J-PTH-120-200' : '*(Rivet_stage1_cat_pTjet30GeV == 106)',
        'stage1GG2H-1J-PTH-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 107)',
        'stage1GG2H-GE2J-PTH-0-60' : '*(Rivet_stage1_cat_pTjet30GeV == 108)',
        'stage1GG2H-GE2J-PTH-60-120' : '*(Rivet_stage1_cat_pTjet30GeV == 109)',
        'stage1GG2H-GE2J-PTH-120-200' : '*(Rivet_stage1_cat_pTjet30GeV == 110)',
        'stage1GG2H-GE2J-PTH-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 111)',
    },
    'VBFHtoTauTau' : {
        'stage1QQ2HQQ-FWDH' : '*(Rivet_stage1_cat_pTjet30GeV == 200)',
        'stage1QQ2HQQ-VBFTOPO-JET3VETO' : '*(Rivet_stage1_cat_pTjet30GeV == 201)',
        'stage1QQ2HQQ-VBFTOPO-JET3' : '*(Rivet_stage1_cat_pTjet30GeV == 202)',
        'stage1QQ2HQQ-VH2JET' : '*(Rivet_stage1_cat_pTjet30GeV == 203)',
        'stage1QQ2HQQ-REST' : '*(Rivet_stage1_cat_pTjet30GeV == 204)',
        'stage1QQ2HQQ-PTJET1-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 205)',
    },
    'WMinusHTauTau' : {
        'stage1QQ2HQQ-VBFTOPO-JET3VETO' : '*(Rivet_stage1_cat_pTjet30GeV == 201)',
        'stage1QQ2HQQ-VBFTOPO-JET3' : '*(Rivet_stage1_cat_pTjet30GeV == 202)',
        'stage1QQ2HQQ-VH2JET' : '*(Rivet_stage1_cat_pTjet30GeV == 203)',
        'stage1QQ2HQQ-REST' : '*(Rivet_stage1_cat_pTjet30GeV == 204)',
        'stage1QQ2HQQ-PTJET1-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 205)',
        'stage1QQ2HLNU-FWDH' : '*(Rivet_stage1_cat_pTjet30GeV == 300)',
        'stage1QQ2HLNU-PTV-0-150' : '*(Rivet_stage1_cat_pTjet30GeV == 301)',
        'stage1QQ2HLNU-PTV-150-250-0J' : '*(Rivet_stage1_cat_pTjet30GeV == 302)',
        'stage1QQ2HLNU-PTV-150-250-GE1J' : '*(Rivet_stage1_cat_pTjet30GeV == 303)',
        'stage1QQ2HLNU-PTV-GT250' : '*(Rivet_stage1_cat_pTjet30GeV == 304)',
    },
    'WPlusHTauTau' : {
        'stage1QQ2HQQ-VBFTOPO-JET3VETO' : '*(Rivet_stage1_cat_pTjet30GeV == 201)',
        'stage1QQ2HQQ-VBFTOPO-JET3' : '*(Rivet_stage1_cat_pTjet30GeV == 202)',
        'stage1QQ2HQQ-VH2JET' : '*(Rivet_stage1_cat_pTjet30GeV == 203)',
        'stage1QQ2HQQ-REST' : '*(Rivet_stage1_cat_pTjet30GeV == 204)',
        'stage1QQ2HQQ-PTJET1-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 205)',
        'stage1QQ2HLNU-FWDH' : '*(Rivet_stage1_cat_pTjet30GeV == 300)',
        'stage1QQ2HLNU-PTV-0-150' : '*(Rivet_stage1_cat_pTjet30GeV == 301)',
        'stage1QQ2HLNU-PTV-150-250-0J' : '*(Rivet_stage1_cat_pTjet30GeV == 302)',
        'stage1QQ2HLNU-PTV-150-250-GE1J' : '*(Rivet_stage1_cat_pTjet30GeV == 303)',
        'stage1QQ2HLNU-PTV-GT250' : '*(Rivet_stage1_cat_pTjet30GeV == 304)',
    },
    'ZHTauTau' : {
        'stage1QQ2HQQ-FWDH' : '*(Rivet_stage1_cat_pTjet30GeV == 200)',
        'stage1QQ2HQQ-VBFTOPO-JET3VETO' : '*(Rivet_stage1_cat_pTjet30GeV == 201)',
        'stage1QQ2HQQ-VBFTOPO-JET3' : '*(Rivet_stage1_cat_pTjet30GeV == 202)',
        'stage1QQ2HQQ-VH2JET' : '*(Rivet_stage1_cat_pTjet30GeV == 203)',
        'stage1QQ2HQQ-REST' : '*(Rivet_stage1_cat_pTjet30GeV == 204)',
        'stage1QQ2HQQ-PTJET1-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 205)',
        'stage1QQ2HLL-FWDH' : '*(Rivet_stage1_cat_pTjet30GeV == 400)',
        'stage1QQ2HLL-PTV-0-150' : '*(Rivet_stage1_cat_pTjet30GeV == 401)',
        'stage1QQ2HLL-PTV-150-250-0J' : '*(Rivet_stage1_cat_pTjet30GeV == 402)',
        'stage1QQ2HLL-PTV-150-250-GE1J' : '*(Rivet_stage1_cat_pTjet30GeV == 403)',
        'stage1QQ2HLL-PTV-GT250' : '*(Rivet_stage1_cat_pTjet30GeV == 404)',
    }}

    return htxsMap


if __name__ == '__main__' :
    print getHtxsCutMapStage0()    
    print getHtxsCutMapStage1()
