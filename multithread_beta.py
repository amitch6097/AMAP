import os
import sys
import _thread


def run(name): #Rub Scanning
    os.system('python RatDecoders/ratdecoder.py '+name)

with open("scan.list", "r") as ins:
    for line in ins:
        print _thread.start_new_thread( run, (line,) ) #Returns Each Thread ID
