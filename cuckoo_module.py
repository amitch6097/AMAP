import requests
import os
import sys
import time
import subprocess
import json

#CLASS that is used to run cuckoo
class CuckooModule:
	#initializer, has to run cuckoo and the api server in a different port than the main program
	def __init__(self):
		#make a directory for the reports to be saved if is does not exist
		self.directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "CuckooReports")
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)
		#checks if cuckoo exists and if so starts cuckoo and the api server
		try:
			self.enabled = True
			self.cuckoo = subprocess.Popen(["cuckoo"])
			time.sleep(5)
			self.server = subprocess.Popen(["cuckoo","api","-H","0.0.0.0","-p","8090"])
			time.sleep(5)
			self.submit_url = "http://0.0.0.0:8090/tasks/create/file"
			self.report_url = "http://0.0.0.0:8090/tasks/report"

		#disable this module if it is on a machine without cuckoo
		except OSError:
			self.enabled = False
	#getter for whether the class is enabled
	#RETURNS self.enabled the attribute that tracks whether the module can be used
	def is_available(self):
		return self.enabled
	
	#destructor for the class, kills cuckoo and the api server if the module is enabled
	def __del__(self):
		if self.enabled:
			self.cuckoo.kill()
			self.server.kill()
	
	#receives a filename to give to cuckoo
	#PARAM filename the name of the file to be processed by cuckoo
	#RETURNS the cuckoo task id or None if the module is not enabled
	def submit_file(self,filename):
		"""submits a file to the cuckoo api and returns the task id that is used to find that file later"""
		if self.enabled:
			with open(filename,"rb") as sample:
				files = {"file":("temp_file_name",sample)}
				request = requests.post(self.submit_url,files=files)
			return request.json()["task_id"]
		else:
			return None
	#receives a task id to find the report of
	#PARAM task_id the integer that represents the id within cuckoo
	#RETURNS a string representing the filename of the report or an empty string if the module is not enabled
	def get_report(self,task_id):
		"""submit a task id and returns the report object, if the task is not done or invalid returns None"""
		print "___IN REPORT____"
		if self.enabled:
			request = requests.get("{}/{}".format(self.report_url,task_id))
			print request
			if request.status_code == 404:
				return ""
			file_path = "/home/cse498/.cuckoo/storage/analyses/{0}/reports/report.json".format(task_id)

			file_name = "task_{0}.json".format(task_id)
			new_path = os.path.join(self.directory, file_name)
			subprocess.Popen(["cp","{}".format(file_path),"{}".format(new_path)])

			return file_name

		else:
			return ""


