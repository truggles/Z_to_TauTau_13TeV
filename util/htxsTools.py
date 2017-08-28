

# Map to link our standard naming scheme for signals
# with their rivet/htxs codes
# and to provide the necessary cut to select this group
# from gen level
# and to provide the final DC mapping

# See https://svnweb.cern.ch/cern/wsvn/lhchiggsxs/repository/TemplateXS/HiggsTemplateCrossSections.h for rivet code mappings

def getHtxsCutMapStage0() :
    htxsMap = {
    'ggHtoTauTau' : {
        'GG2H' : '*(Rivet_stage0_cat == 11)'
    },
    'VBFHtoTauTau' : {
        'VBF' : '*(Rivet_stage0_cat == 21)'
    },
    'WMinusHTauTau' : {
        'VH2HQQ' : '*(Rivet_stage0_cat == 23)',
        'QQ2HLNU' : '*(Rivet_stage0_cat == 31)'
    },
    'WPlusHTauTau' : {
        'VH2HQQ' : '*(Rivet_stage0_cat == 23)',
        'QQ2HLNU' : '*(Rivet_stage0_cat == 31)'
    },
    'ZHTauTau' : {
        'VH2HQQ' : '*(Rivet_stage0_cat == 23)',
        'QQ2HLL' : '*(Rivet_stage0_cat == 41)'
    }}

    return htxsMap


def getHtxsCutMapStage1() :
    htxsMap = {
    'ggHtoTauTau' : {
        'GG2H-VBFTOPO-JET3VETO' : '*(Rivet_stage1_cat_pTjet30GeV == 101)',
        'GG2H-VBFTOPO-JET3' : '*(Rivet_stage1_cat_pTjet30GeV == 102)',
        'GG2H-0J' : '*(Rivet_stage1_cat_pTjet30GeV == 103)',
        'GG2H-1J-PTH-0-60' : '*(Rivet_stage1_cat_pTjet30GeV == 104)',
        'GG2H-1J-PTH-60-120' : '*(Rivet_stage1_cat_pTjet30GeV == 105)',
        'GG2H-1J-PTH-120-200' : '*(Rivet_stage1_cat_pTjet30GeV == 106)',
        'GG2H-1J-PTH-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 107)',
        'GG2H-GE2J-PTH-0-60' : '*(Rivet_stage1_cat_pTjet30GeV == 108)',
        'GG2H-GE2J-PTH-60-120' : '*(Rivet_stage1_cat_pTjet30GeV == 109)',
        'GG2H-GE2J-PTH-120-200' : '*(Rivet_stage1_cat_pTjet30GeV == 110)',
        'GG2H-GE2J-PTH-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 111)',
    },
    'VBFHtoTauTau' : {
        'QQ2HQQ-VBFTOPO-JET3VETO' : '*(Rivet_stage1_cat_pTjet30GeV == 201)',
        'QQ2HQQ-VBFTOPO-JET3' : '*(Rivet_stage1_cat_pTjet30GeV == 202)',
        'QQ2HQQ-VH2JET' : '*(Rivet_stage1_cat_pTjet30GeV == 203)',
        'QQ2HQQ-REST' : '*(Rivet_stage1_cat_pTjet30GeV == 204)',
        'QQ2HQQ-PTJET1-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 205)',
    },
    'WMinusHTauTau' : {
        'QQ2HQQ-VH2JET' : '*(Rivet_stage1_cat_pTjet30GeV == 203)',
        'QQ2HQQ-REST' : '*(Rivet_stage1_cat_pTjet30GeV == 204)',
        'QQ2HQQ-PTJET1-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 205)',
        'QQ2HLNU-PTV-0-150' : '*(Rivet_stage1_cat_pTjet30GeV == 301)',
        'QQ2HLNU-PTV-150-250-0J' : '*(Rivet_stage1_cat_pTjet30GeV == 302)',
        'QQ2HLNU-PTV-150-250-GE1J' : '*(Rivet_stage1_cat_pTjet30GeV == 303)',
        'QQ2HLNU-PTV-GT250' : '*(Rivet_stage1_cat_pTjet30GeV == 304)',
    },
    'WPlusHTauTau' : {
        'QQ2HQQ-VH2JET' : '*(Rivet_stage1_cat_pTjet30GeV == 203)',
        'QQ2HQQ-REST' : '*(Rivet_stage1_cat_pTjet30GeV == 204)',
        'QQ2HQQ-PTJET1-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 205)',
        'QQ2HLNU-PTV-0-150' : '*(Rivet_stage1_cat_pTjet30GeV == 301)',
        'QQ2HLNU-PTV-150-250-0J' : '*(Rivet_stage1_cat_pTjet30GeV == 302)',
        'QQ2HLNU-PTV-150-250-GE1J' : '*(Rivet_stage1_cat_pTjet30GeV == 303)',
        'QQ2HLNU-PTV-GT250' : '*(Rivet_stage1_cat_pTjet30GeV == 304)',
    },
    'ZHTauTau' : {
        'QQ2HQQ-VH2JET' : '*(Rivet_stage1_cat_pTjet30GeV == 203)',
        'QQ2HQQ-REST' : '*(Rivet_stage1_cat_pTjet30GeV == 204)',
        'QQ2HQQ-PTJET1-GT200' : '*(Rivet_stage1_cat_pTjet30GeV == 205)',
        'QQ2HLL-PTV-0-150' : '*(Rivet_stage1_cat_pTjet30GeV == 401)',
        'QQ2HLL-PTV-150-250-0J' : '*(Rivet_stage1_cat_pTjet30GeV == 402)',
        'QQ2HLL-PTV-150-250-GE1J' : '*(Rivet_stage1_cat_pTjet30GeV == 403)',
        'QQ2HLL-PTV-GT250' : '*(Rivet_stage1_cat_pTjet30GeV == 404)',
    }}

    return htxsMap


if __name__ == '__main__' :
    print getHtxsCutMapStage0()    
    print getHtxsCutMapStage1()
