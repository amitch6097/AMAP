

import os
from optparse import OptionParser


__description__ = 'prints something'
__author__ = "Andrew Mitchell"
__version__ = '1.0'
__date__ = "1/1/1"

def my_module(filename):
    print "something"

if __name__ == "__main__":
        parser = OptionParser(usage='usage: %prog file / dir\n' + __description__, version='%prog ' + __version__)
        (options, args) = parser.parse_args()
        is_file = os.path.isfile(args[0])
        if is_file:
            my_module(args[0])

          
