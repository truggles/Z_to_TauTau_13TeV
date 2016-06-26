import os




# A function to set up our directories and check if we are running
# certain bkg methods
def setUpDirs( samples, params, analysis ) :
    if not os.path.exists( '%s%s' % (analysis, params['mid1']) ) : os.makedirs( '%s%s' % (analysis, params['mid1']) )
    if not os.path.exists( '%s%s' % (analysis, params['mid2']) ) : os.makedirs( '%s%s' % (analysis, params['mid2']) )
    if not os.path.exists( '%s%s' % (analysis, params['mid3']) ) : os.makedirs( '%s%s' % (analysis, params['mid3']) )
    ofile = open('%s%s/config.txt' % (analysis, params['mid3']), "w")
    for sample in samples :
        ofile.write( "%s " % sample )
    ofile.write( "\n" )
    for key in params :
        ofile.write( "%s : %s\n" % (key, params[key]) )
    ofile.close() 
    return samples





