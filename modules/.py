
import os
from optparse import OptionParser


__description__ =
__author__ =
__version__ = '1.0'
__date__ =

def my_module(filename):

if __name__ == "__main__":
        parser = OptionParser(usage='usage: %prog file / dir\n' + __description__, version='%prog ' + __version__)
        (options, args) = parser.parse_args()
        is_file = os.path.isfile(args[0])
        if is_file:
            my_module(args[0])
          