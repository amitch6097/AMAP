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

<<<<<<< HEAD
		self.submit_url = "http://0.0.0.0:8090/tasks/create/file"
		self.report_url = "http://0.0.0.0:8090/tasks/report"
=======
		try:
			self.enabled = True
			self.cuckoo = subprocess.Popen(["cuckoo"])
			time.sleep(5)
			self.server = subprocess.Popen(["cuckoo","api","-H","0.0.0.0","-p","8090"])
			time.sleep(5)
			self.submit_url = "http://0.0.0.0:8090/tasks/create/file"
			self.report_url = "http://0.0.0.0:8090/tasks/report"
>>>>>>> d43ea640da98283aeb956f50dde6f7e999589111

		except OSError:
			self.enabled = False

<<<<<<< HEAD

=======
	def __del__(self):
		if self.enabled:
			self.cuckoo.kill()
			self.server.kill()
>>>>>>> d43ea640da98283aeb956f50dde6f7e999589111
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

		if self.enabled:
			request = requests.post("{}/{}".format(self.report_url,task_id))
			if request.status_code == 404:
				return None
			file_path = os.path.join(self.directory, "task_{0}".format(task_id))
			if not os.path.isfile(file_path):
				file = open(file_path, "w")
				file.write(request.text)
			return file_path
		else:
			return None
<<<<<<< HEAD
		file_path = os.path.join(self.directory, "task_{0}".format(task_id))
		if not os.path.isfile(file_path):
			file = open(file_path, "w")
			file.write(request.text)

		print file_path
		return file_path
=======
>>>>>>> d43ea640da98283aeb956f50dde6f7e999589111
		# return json.loads(request.text)

if __name__ == "__main__":
	mod = CuckooModule()

	task = mod.get_report(2)
	print task
