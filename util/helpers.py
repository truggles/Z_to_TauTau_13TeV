import os




# A function to set up our directories and check if we are running
# certain bkg methods
def checkBkgs( samples, params, grouping ) :
    import analysis1BaselineCuts
    bkgMap = analysis1BaselineCuts.getBkgMap()
    if params[ 'bkgs' ] != 'None' :
        bkgs = params[ 'bkgs' ]
        params[ 'cutMapper' ] = bkgMap[ params[ 'bkgs' ] ][0]
        params[ 'cutName' ] = bkgMap[ params[ 'bkgs' ] ][0]
        samples = bkgMap[ params [ 'bkgs' ] ][1]
        if not os.path.exists( 'meta/%sBackgrounds/%s/cut' % (grouping, bkgMap[ bkgs ][0]) ) : 
            os.makedirs( 'meta/%sBackgrounds/%s/cut' % (grouping, bkgMap[ bkgs ][0]) )
            os.makedirs( 'meta/%sBackgrounds/%s/iso' % (grouping, bkgMap[ bkgs ][0]) )
            os.makedirs( 'meta/%sBackgrounds/%s/shape' % (grouping, bkgMap[ bkgs ][0]) )
    else :
        if not os.path.exists( '%s%s' % (grouping, params['mid1']) ) : os.makedirs( '%s%s' % (grouping, params['mid1']) )
        if not os.path.exists( '%s%s' % (grouping, params['mid2']) ) : os.makedirs( '%s%s' % (grouping, params['mid2']) )
        if not os.path.exists( '%s%s' % (grouping, params['mid3']) ) : os.makedirs( '%s%s' % (grouping, params['mid3']) )
    ofile = open('%s%s/config.txt' % (grouping, params['mid3']), "w")
    for sample in samples :
        ofile.write( "%s " % sample )
    ofile.write( "\n" )
    for key in params :
        ofile.write( "%s : %s\n" % (key, params[key]) )
    ofile.close() 
    return samples





