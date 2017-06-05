import glob
import os
import argparse

p = argparse.ArgumentParser(description="make a html index file for a given path.")
p.add_argument('--path', action='store', default='', dest='path', help="target path path?")
options = p.parse_args()

def run(path) :
    if path == '' :
        print "Must provide a path path"
        return

    if '~' == path[0] :
        print "Have ~ -> $HOME"
        home = os.getenv( 'HOME' )
        print "$HOME:",home
        newPath = home
        newPath += path[1:]
        path = newPath
        #path.replace('~', home )
        print "new path",path
    
    if not os.path.exists( path ) :
        print "Path does not exist"
        print "Provided path:",path
        return
    
    files = glob.glob( path+"/*.*" )
    #print "Files in list:\n"
    #print files
    
    htmlFile = open('%s/index.html' % path, 'w')
    htmlFile.write( '<html><head><STYLE type="text/css">img { border:0px; }</STYLE>\n' )
    htmlFile.write( '<title>webView</title></head>\n' )
    htmlFile.write( '<body>\n' )
    for file_ in files :
        if '.pdf' in file_ : continue
        htmlFile.write( '<img src="%s">\n' % file_.strip().split('/')[-1] )
        #htmlFile.write( '<br>\n' )
    htmlFile.write( '</body></html>' )
    htmlFile.close()

if __name__ == '__main__' :
    run(options.path)
