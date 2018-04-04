import os
import hashlib
from optparse import OptionParser


__description__ = 'SHA256'
__author__ = 'Andrew Mitchell'
__version__ = '1.0'
__date__ = '2016/04'

def sha1_module(filepath):
    openedFile = open(filepath)
    readFile = openedFile.read()
    # print filename

    sha1Hash = hashlib.sha1(readFile)
    sha1Hash = hashlib.sha256(readFile)
    md5 = hashlib.md5(readFile)

    sha1Hashed = sha1Hash.hexdigest()

    print sha1Hashed

if __name__ == "__main__":
        parser = OptionParser(usage='usage: %prog file / dir\n' + __description__, version='%prog ' + __version__)
        (options, args) = parser.parse_args()
        is_file = os.path.isfile(args[0])
        if is_file:
            sha1_module(args[0])
