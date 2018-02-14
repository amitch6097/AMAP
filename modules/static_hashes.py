import hashlib

def md5_module(filename):
    openedFile = open(filename)
    readFile = openedFile.read()

    md5Hash = hashlib.md5(readFile)
    md5Hashed = md5Hash.hexdigest()
    return md5Hashed

def sha1_module(filename):
    openedFile = open(filename)
    readFile = openedFile.read()

    sha1Hash = hashlib.sha1(readFile)
    sha1Hashed = sha1Hash.hexdigest()

    return sha1Hashed
