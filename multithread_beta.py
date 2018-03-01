import os
import sys
import thread


def run(name): #Rub Scanning
    os.system('python RatDecoders/ratdecoder.py '+name)

with open("scan.list", "r") as ins:
    for line in ins:
        print thread.start_new_thread( run, (line,) ) #Returns Each Thread ID
