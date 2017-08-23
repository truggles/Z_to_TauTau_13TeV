

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


if __name__ == '__main__' :
    print getHtxsCutMapStage0()    
