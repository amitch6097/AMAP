import os
import sys
import thread
<<<<<<< HEAD
=======
import time
import subprocess
import threading

class decoder(threading.Thread):
	def __init__(self,name):
		threading.Thread.__init__(self)
		self.name=name
	def run(self):
		#os.system('python RatDecoders/ratdecoder.py '+ "-o test.txt " + name)
	    #p = subprocess.call(['python', 'RatDecoders/ratdecoder.py', name])
	    # os.popen('python RatDecoders/ratdecoder.py '+ "-o test.txt " + name).read()
	    output = subprocess.check_output('python RatDecoders/ratdecoder.py '+ "-o test.txt " + self.name, shell=True)
>>>>>>> e491b48fce649ff1ddeee2f0fdda8ffbfb598f6a


def run(name): #Rub Scanning
    #os.system('python RatDecoders/ratdecoder.py '+ "-o test.txt " + name)
    #p = subprocess.call(['python', 'RatDecoders/ratdecoder.py', name])
    # os.popen('python RatDecoders/ratdecoder.py '+ "-o test.txt " + name).read()
    output = subprocess.check_output('python RatDecoders/ratdecoder.py '+ "-o test.txt " + name, shell=True)

def printSpacers():
	print "---"
	print "---"
	print "---"
	print "---"


def multithreaded():
	printSpacers()
	print "*** RUNNING IN MULTI-THREADED ENVIRONMENT ***"
	printSpacers()

	threadList = []
	with open("scan.list", "r") as ins:
		for line in ins:
			thread = decoder(line)
			thread.start()
			threadList.append(thread)
			#print "Thread ID: " + str(thread.start_new_thread( run, (line,) ) )#Returns Each Thread ID


	count = 0
	startTime = time.clock()
	for thread in threadList:
		count += 1
		thread.join()
		print "Files Analyzed:" + str(count)

	elapsedTime = time.clock() - startTime

	print str(elapsedTime*1000) + " seconds"
	return elapsedTime*1000



def singleThread():
	printSpacers()
	print "*** RUNNING IN SINGLE THREADED ENVIRONMENT ***"
	printSpacers()

	startTime = time.clock()
	with open("scan.list", "r") as ins:
		count = 0
		for line in ins:
			run(line)
			count += 1
			print "Files Analyzed:" + str(count)
	elapsedTime = time.clock() - startTime

	print str(elapsedTime*1000) + " seconds"
	return elapsedTime*1000

def printSummary(singleTime,multiTime):
	printSpacers()
	print "Time Comparison Summary"
	printSpacers()
	print "Single Threaded Runtime: " + str(singleTime) + " seconds"
	print "Multi-Threaded Runtime: " + str(multiTime) + " seconds"
	printSpacers()


singleTime = singleThread()
multiTime = multithreaded()
printSummary(singleTime,multiTime)
