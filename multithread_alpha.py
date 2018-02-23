#This is a demo for multi threading
import _thread
import time

def print_time( threadName, delay):
   count = 0
   while count < 50:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

try:
   _thread.start_new_thread( print_time, ("Thread-1", 0.5, ) )  # Now I am showing how to multithreading a function that I defined above that showing time. When our function completed, plug it in here.
   _thread.start_new_thread( print_time, ("Thread-2", 0.5, ) ) 
   
except:
   print ("Problem happend")

while 1:
   pass