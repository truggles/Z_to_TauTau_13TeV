# Setup script for ZTT analysis
#
# This makes the required directories for storing .root files and plots

import os

dirs = ['1BaseCut',
        '2IsoOrderAndDups',
        '1Single',
        '2SingleIOAD',
        'Plots',
        'PlotsList',
]        

prefixes = ['Sync', '25ns']#'50ns', '25ns', 'Sync']

for pre_ in prefixes :
    for dir_ in dirs :
        if not os.path.exists("%s%s" % (pre_, dir_) ):
            os.makedirs("%s%s" % (pre_, dir_) )
            if "Plots" in dir_ :
                os.makedirs("%s%s/em" % (pre_, dir_) )
                os.makedirs("%s%s/tt" % (pre_, dir_) )
                
