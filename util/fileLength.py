def file_len(fname):
    i = -1
    try :
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
    except IOError :
        print "No such file or directory %s. Setting length = 0" % fname
    return i + 1
