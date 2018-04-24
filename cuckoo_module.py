import requests
import os
import sys
import time
import subprocess
import json

class CuckooModule:
	def __init__(self):
		self.directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "CuckooReports")
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

		try:
			self.enabled = True
			self.cuckoo = subprocess.Popen(["cuckoo"])
			time.sleep(5)
			self.server = subprocess.Popen(["cuckoo","api","-H","0.0.0.0","-p","8090"])
			time.sleep(5)
			self.submit_url = "http://0.0.0.0:8090/tasks/create/file"
			self.report_url = "http://0.0.0.0:8090/tasks/report"


		except OSError:
			self.enabled = False

	def is_available(self):
		return self.enabled

	def __del__(self):
		if self.enabled:
			self.cuckoo.kill()
			self.server.kill()

	def submit_file(self,filename):
		"""submits a file to the cuckoo api and returns the task id that is used to find that file later"""
		if self.enabled:
			with open(filename,"rb") as sample:
				files = {"file":("temp_file_name",sample)}
				request = requests.post(self.submit_url,files=files)
			return request.json()["task_id"]
		else:
			return None

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

if __name__ == "__main__":
	mod = CuckooModule()

	task = mod.get_report(2)
	print task
